"""Execute the actual release shell steps with offline, isolated Git repositories."""

import os
import re
import subprocess
import textwrap
from pathlib import Path

import pytest

WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/release.yml"
VERSION = "1.2.4"


def step(name):
    source = WORKFLOW.read_text()
    marker = f"      - name: {name}\n"
    body = source.split(marker, 1)[1].split("\n      - name:", 1)[0]
    script = textwrap.dedent(body.split("        run: |\n", 1)[1])
    for expression, value in (
        ("steps.ver.outputs.new", VERSION),
        ("steps.ver.outputs.tag", f"v{VERSION}"),
        ("steps.prev.outputs.prev", "v0.0.0"),
    ):
        script = script.replace("${{ " + expression + " }}", value)
    assert "${{" not in script
    return script


def git(repo, *args, check=True):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=check,
        env={**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1"},
    )


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "--initial-branch=master")
    git(root, "config", "user.name", "Offline release fixture")
    git(root, "config", "user.email", "fixture@example.invalid")
    (root / "version.txt").write_text("1.2.3\n")
    (root / "CHANGELOG.md").write_text("# Previous history\n\nPreserve this entry.\n")
    (root / "tracked.txt").write_text("Original tracked content.\n")
    git(root, "add", ".")
    git(root, "commit", "-m", "Offline baseline")
    return root


def execute(repo, script):
    # Step fixtures never execute push, tag or gh. Only Git read/add/commit are allowed.
    assert not re.search(r"^\s*(?:git (?:push|tag)\b|gh\b)", script, re.MULTILINE)
    return subprocess.run(
        ["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", script],
        cwd=repo,
        capture_output=True,
        text=True,
        timeout=15,
        env={
            **os.environ,
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GITHUB_OUTPUT": str(repo.parent / "github-output"),
            "TMPDIR": str(repo.parent),
        },
    )


def rejecting_hook(repo):
    hook = repo / ".git/hooks/pre-commit"
    hook.write_text("#!/bin/sh\nprintf 'offline pre-commit rejection\\n' >&2\nexit 42\n")
    hook.chmod(0o755)


@pytest.mark.parametrize("name", ["Update version files", "Generate changelog entry"])
def test_commit_hook_failure_is_fatal_and_cannot_claim_outputs(repo, name):
    before = git(repo, "rev-parse", "HEAD").stdout
    rejecting_hook(repo)
    result = execute(repo, step(name))
    assert "offline pre-commit rejection" in result.stderr
    assert git(repo, "rev-parse", "HEAD").stdout == before
    assert git(repo, "show", "HEAD:version.txt").stdout == "1.2.3\n"
    assert git(repo, "show", "HEAD:CHANGELOG.md").stdout.startswith("# Previous history")
    assert git(repo, "diff", "--staged", "--quiet", check=False).returncode == 1
    assert result.returncode != 0
    output = repo.parent / "github-output"
    assert not output.exists() or "notes=" not in output.read_text()


def committed_release(repo):
    for name in ("Update version files", "Generate changelog entry"):
        result = execute(repo, step(name))
        assert result.returncode == 0, (result.stdout, result.stderr)


def test_committed_release_contains_exact_required_outputs_and_history(repo):
    committed_release(repo)
    assert git(repo, "show", "HEAD:version.txt").stdout == f"{VERSION}\n"
    changelog = git(repo, "show", "HEAD:CHANGELOG.md").stdout
    assert changelog.startswith(f"# Release v{VERSION}\n")
    assert "# Previous history\n\nPreserve this entry." in changelog
    result = execute(repo, step("Verify committed release artifacts"))
    assert result.returncode == 0, result.stderr
    assert git(repo, "status", "--porcelain", "--untracked-files=no").stdout == ""


@pytest.mark.parametrize("stage", [False, True])
def test_pre_tag_gate_rejects_dirty_tracked_content(repo, stage):
    committed_release(repo)
    (repo / "tracked.txt").write_text("Unexpected hook or later step modification.\n")
    if stage:
        git(repo, "add", "tracked.txt")
    result = execute(repo, step("Verify committed release artifacts"))
    assert result.returncode != 0


@pytest.mark.parametrize("artifact", ["version", "extra-version-line", "changelog", "missing"])
def test_pre_tag_gate_rejects_clean_commit_without_exact_release_artifacts(repo, artifact):
    committed_release(repo)
    if artifact == "missing":
        (repo / "version.txt").unlink()
    elif artifact == "changelog":
        (repo / "CHANGELOG.md").write_text(f"# Old header\n\n# Release v{VERSION}\n")
    else:
        (repo / "version.txt").write_text(
            "1.2.3\n" if artifact == "version" else f"{VERSION}\nextra\n"
        )
    git(repo, "add", "-A")
    git(repo, "commit", "-m", "Offline invalid release artifact fixture")
    result = execute(repo, step("Verify committed release artifacts"))
    assert result.returncode != 0


def test_version_no_change_is_success_without_an_unneeded_commit(repo):
    assert execute(repo, step("Update version files")).returncode == 0
    before = git(repo, "rev-parse", "HEAD").stdout
    rejecting_hook(repo)
    assert execute(repo, step("Update version files")).returncode == 0
    assert git(repo, "rev-parse", "HEAD").stdout == before


def test_required_verification_precedes_tag_and_also_runs_for_dry_run():
    source = WORKFLOW.read_text()
    start = source.index("      - name: Verify committed release artifacts\n")
    end = source.index("      - name: Create tag and push\n")
    assert start < end
    gate = source[start:end]
    assert "if: steps.check.outputs.needed == 'true'" in gate
    assert "dry_run" not in gate
    assert 'git push origin HEAD || echo "Branch push rejected' in source
