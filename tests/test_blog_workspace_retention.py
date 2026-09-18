"""Disposable Git registries only: retirement must retain proof and owner work."""

from __future__ import annotations

import contextlib
import fcntl
import json
import os
from pathlib import Path
from types import SimpleNamespace

import pytest
from test_blog_publication_state import (
    git,
    publish,
    reconcile,
    seal,
    workspace,
)
from test_blog_publication_state import (
    run as run,
)


@contextlib.contextmanager
def pipeline_lock(tmp_path, monkeypatch):
    path = tmp_path / "fixture-pipeline.lock"
    monkeypatch.setattr(workspace, "PIPELINE_LOCK", path)
    try:
        original = os.dup(9)
    except OSError:
        original = None
    with path.open("a") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        os.dup2(stream.fileno(), 9)
        try:
            yield
        finally:
            if original is not None:
                os.dup2(original, 9)
                os.close(original)
            else:
                os.close(9)


def next_args(run):
    manifest = json.loads(run["manifest"].read_text())
    return SimpleNamespace(
        repo=run["owner"],
        expected_remote=manifest["remote_url"],
        date="2026-09-17",
        run_id="next-run",
        state_dir=run["manifest"].parents[4],
        recover_abandoned=True,
        retain_checkouts=0,
        retirement_min_age_hours=0,
    )


def test_completed_checkout_retires_before_next_create_preserving_proof(run, tmp_path, monkeypatch):
    seal(run)
    publish(run)
    reconcile(run)
    owner_head = git(run["owner"], "rev-parse", "HEAD")
    owner_draft = run["owner"] / "private-owner-draft.txt"
    owner_draft.write_text("Owner work must not change")
    before = git(run["owner"], "status", "--porcelain")
    proof = (run["manifest"].parent / "quality-proof" / "sentinel.json").read_bytes()
    with pipeline_lock(tmp_path, monkeypatch):
        created = workspace.create(next_args(run))
    assert not run["root"].exists(), "completed old checkout must retire before admission"
    assert Path(created["workspace"]).exists()
    assert json.loads(run["manifest"].read_text())["status"] == "published"
    assert (run["manifest"].parent / "quality-proof" / "sentinel.json").read_bytes() == proof
    assert git(run["owner"], "rev-parse", "HEAD") == owner_head
    assert git(run["owner"], "status", "--porcelain") == before
    assert owner_draft.read_text() == "Owner work must not change"


def completed(run):
    seal(run)
    publish(run)
    reconcile(run)
    return json.loads(run["manifest"].read_text())


def retire(run, tmp_path, monkeypatch, **kwargs):
    args = next_args(run)
    with pipeline_lock(tmp_path, monkeypatch):
        return workspace.retire_registry(
            args.repo,
            args.state_dir,
            args.expected_remote,
            keep=kwargs.get("keep", 0),
            min_age_hours=kwargs.get("age", 0),
        )


@pytest.mark.parametrize(
    "stage", ["ready", "sealed", "pending_publication", "published", "quarantined"]
)
def test_unfinished_or_quarantined_checkout_is_never_removed(run, tmp_path, monkeypatch, stage):
    manifest = json.loads(run["manifest"].read_text())
    manifest["status"] = stage
    if stage == "published":
        manifest["delivery_status"] = "pending"
    workspace.atomic_json(run["manifest"], manifest)
    before = (run["root"] / "content/posts/delivery-fixture.md").read_bytes()
    result = retire(run, tmp_path, monkeypatch)
    assert result["retired_runs"] == []
    assert result["protected_bytes"] > 0
    assert (run["root"] / "content/posts/delivery-fixture.md").read_bytes() == before
    assert not (run["manifest"].parent / "checkout-retirement.json").exists()


@pytest.mark.parametrize(
    "corruption", ["proof", "seal", "symlink", "tracked", "untracked", "ignored"]
)
def test_bad_evidence_or_foreign_work_protects_entire_checkout(
    run, tmp_path, monkeypatch, corruption
):
    completed(run)
    if corruption == "proof":
        (run["manifest"].parent / "quality-proof/sentinel.json").write_text("{}")
    elif corruption == "seal":
        (run["manifest"].parent / "quality-seal.json").write_text("{}")
    elif corruption == "symlink":
        proof = run["manifest"].parent / "quality-proof/sentinel.json"
        raw = proof.read_bytes()
        proof.unlink()
        external = tmp_path / "external-sentinel"
        external.write_bytes(raw)
        proof.symlink_to(external)
    elif corruption == "tracked":
        (run["root"] / "content/posts/delivery-fixture.md").write_text("changed")
    elif corruption == "untracked":
        (run["root"] / "foreign.txt").write_text("preserve")
    else:
        (run["root"] / ".blog-staging/unrelated.json").write_text("preserve")
    result = retire(run, tmp_path, monkeypatch)
    assert result["retired_runs"] == []
    assert result["protected_runs"]
    assert run["root"].exists()


def test_live_child_lock_protects_completed_checkout(run, tmp_path, monkeypatch):
    completed(run)
    with (run["manifest"].parent / "producer.lock").open("a") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        result = retire(run, tmp_path, monkeypatch)
    assert result["retired_runs"] == []
    assert "producer is still running" in result["protected_runs"][0]["reason"]
    assert run["root"].exists()


@pytest.mark.parametrize("keep,age", [(2, 0), (0, 24)])
def test_default_count_and_age_protect_recent_completed_runs(run, tmp_path, monkeypatch, keep, age):
    completed(run)
    result = retire(run, tmp_path, monkeypatch, keep=keep, age=age)
    assert result["retired_runs"] == []
    assert result["protected_runs"][0]["reason"] == "retention-window"
    assert run["root"].exists()


@pytest.mark.parametrize("point", ["prepared", "removed"])
def test_crash_retry_is_idempotent_and_retains_archive(run, tmp_path, monkeypatch, point):
    completed(run)
    original = workspace.git

    class SimulatedTermination(BaseException):
        pass

    def interrupted(repo, *args):
        if args[:2] == ("worktree", "remove"):
            if point == "removed":
                original(repo, *args)
            raise SimulatedTermination()
        return original(repo, *args)

    monkeypatch.setattr(workspace, "git", interrupted)
    with pytest.raises(SimulatedTermination):
        retire(run, tmp_path, monkeypatch)
    receipt = json.loads((run["manifest"].parent / "checkout-retirement.json").read_text())
    assert receipt["state"] == "prepared"
    archive = (run["manifest"].parent / "checkout-evidence.tar").read_bytes()
    monkeypatch.setattr(workspace, "git", original)
    assert retire(run, tmp_path, monkeypatch)["retired_runs"]
    assert not run["root"].exists()
    assert retire(run, tmp_path, monkeypatch)["retired_runs"] == []
    assert (run["manifest"].parent / "checkout-evidence.tar").read_bytes() == archive


def test_noop_retirement_retains_exact_published_target_archive(run, tmp_path, monkeypatch):
    import tarfile

    completed(run)
    args = next_args(run)
    args.date = "2026-09-16"
    args.recover_abandoned = False
    noop = workspace.create(args)
    path = Path(noop["manifest"])
    workspace.complete_noop(path)
    result = retire(run, tmp_path, monkeypatch)
    assert noop["run_id"] in result["retired_runs"]
    assert not Path(noop["workspace"]).exists()
    with tarfile.open(path.parent / "checkout-evidence.tar") as archive:
        content = archive.extractfile("committed/content/posts/delivery-fixture.md").read()
    assert b"Offline delivery fixture" in content
    assert json.loads(path.read_text())["status"] == "noop"


def test_census_counts_external_quarantine_and_has_no_mutations(run):
    path = run["manifest"].parent / "quarantine"
    path.mkdir()
    (path / "owned.md").write_bytes(b"evidence" * 1000)
    before = run["manifest"].read_bytes()
    args = next_args(run)
    result = workspace.census(args.repo, args.state_dir)
    assert result["runs"][0]["quarantine_bytes"] >= 8000
    assert result["protected_bytes"] == result["workspace_bytes"] > 0
    assert run["manifest"].read_bytes() == before
    assert not (run["manifest"].parent / "checkout-retirement.json").exists()


def test_admission_fails_before_new_checkout_without_reclaiming_protected_run(run, monkeypatch):
    args = next_args(run)
    manifest = json.loads(run["manifest"].read_text())
    # Protect the existing failed run; admission must not discard it for capacity.
    manifest["status"] = "quarantined"
    workspace.atomic_json(run["manifest"], manifest)
    monkeypatch.setattr(workspace.shutil, "disk_usage", lambda _path: SimpleNamespace(free=1))
    args.recover_abandoned = False
    with pytest.raises(workspace.WorkspaceError, match="admission refused"):
        workspace.create(args)
    assert run["root"].exists()
    assert len(list(run["manifest"].parents[3].glob("runs/*/*/manifest.json"))) == 1


def test_admission_reserves_expansion_and_floor_on_registry_filesystem(run, monkeypatch):
    args = next_args(run)
    head = git(run["owner"], "rev-parse", "origin/master")
    calls = []

    def disk(path):
        calls.append(path)
        return SimpleNamespace(free=workspace.RESERVE_BYTES)

    monkeypatch.setattr(workspace.shutil, "disk_usage", disk)
    result = workspace.admission(args.repo, args.state_dir, head)
    assert result["required_free_bytes"] == 2 * result["tracked_allocated_estimate"] + 500 * 1024**2
    assert result["admitted"] is False
    assert calls == [run["manifest"].parents[3]]


def test_retirement_requires_real_canonical_lock(run, monkeypatch, tmp_path):
    monkeypatch.setattr(workspace, "PIPELINE_LOCK", tmp_path / "absent-lock")
    args = next_args(run)
    with pytest.raises(workspace.WorkspaceError, match="canonical FD9"):
        workspace.retire_registry(args.repo, args.state_dir, args.expected_remote)
    assert run["root"].exists()


def test_actual_cli_loads_verifier_without_creating_source_bytecode(run, tmp_path, monkeypatch):
    import shutil
    import subprocess
    import sys

    completed(run)
    scripts = tmp_path / "installed-scripts"
    scripts.mkdir()
    source = Path(workspace.__file__).parent
    for name in ("blog-run-workspace.py", "blog_publication_state.py"):
        shutil.copyfile(source / name, scripts / name)
    # The CLI must prove a real inherited fixture lock, not touch the canonical lock.
    helper = scripts / "blog-run-workspace.py"
    text = helper.read_text().replace(
        'Path("/tmp/blog-pipeline.lock")', f"Path({str(tmp_path / 'fixture-pipeline.lock')!r})"
    )
    helper.write_text(text)
    args = next_args(run)
    env = dict(os.environ)
    env.pop("PYTHONDONTWRITEBYTECODE", None)
    with pipeline_lock(tmp_path, monkeypatch):
        result = subprocess.run(
            [
                sys.executable,
                str(helper),
                "retire",
                "--repo",
                str(args.repo),
                "--state-dir",
                str(args.state_dir),
                "--expected-remote",
                args.expected_remote,
                "--retain-checkouts",
                "0",
                "--retirement-min-age-hours",
                "0",
            ],
            env=env,
            pass_fds=(9,),
            text=True,
            capture_output=True,
            timeout=30,
        )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["retired_runs"]
    assert not (scripts / "__pycache__").exists()


def test_local_beads_runtime_is_protected_not_archived_as_disposable(run, tmp_path, monkeypatch):
    completed(run)
    local = run["root"] / ".beads/embeddeddolt"
    local.mkdir(parents=True)
    (local / "unknown-history").write_bytes(b"retain private task history")
    # Existing ignore may vary, but either ignored or untracked runtime is protected.
    result = retire(run, tmp_path, monkeypatch)
    assert result["retired_runs"] == []
    assert "local Beads state" in result["protected_runs"][0]["reason"]
    assert not (run["manifest"].parent / "checkout-evidence.tar").exists()
    assert (local / "unknown-history").read_bytes() == b"retain private task history"


def test_read_only_census_treats_completed_candidate_as_unverified(run):
    completed(run)
    args = next_args(run)
    result = workspace.census(args.repo, args.state_dir)
    assert result["protected_bytes"] == result["workspace_bytes"] > 0
    assert result["runs"][0]["protected_reason"] == "completed-requires-verification"


def test_derived_output_is_not_duplicated_into_durable_archive(run, tmp_path, monkeypatch):
    import tarfile

    completed(run)
    public = run["root"] / "public"
    public.mkdir()
    (public / "generated.html").write_bytes(b"generated output" * 1000)
    result = retire(run, tmp_path, monkeypatch)
    assert result["retired_runs"]
    with tarfile.open(run["manifest"].parent / "checkout-evidence.tar") as archive:
        assert not any("public/" in name for name in archive.getnames())
    receipt = json.loads((run["manifest"].parent / "checkout-retirement.json").read_text())
    assert "public/" in receipt["discarded_derived_categories"]


def test_archive_size_limit_protects_original_staging_bytes(run, tmp_path, monkeypatch):
    completed(run)
    marker = run["root"] / ".blog-staging/2026-09-16.offline-delivery-run.large.json"
    marker.write_bytes(b"private evidence" * 100)
    monkeypatch.setattr(workspace, "ARCHIVE_LIMIT_BYTES", 10)
    result = retire(run, tmp_path, monkeypatch)
    assert result["retired_runs"] == []
    assert "archive exceeds" in result["protected_runs"][0]["reason"]
    assert marker.exists()


def test_git_deadline_is_bounded_and_reports_category(monkeypatch, tmp_path):
    import subprocess

    def stalled(*args, **kwargs):
        assert kwargs["timeout"] == 60
        raise subprocess.TimeoutExpired(args[0], 60)

    monkeypatch.setattr(workspace.subprocess, "run", stalled)
    with pytest.raises(workspace.WorkspaceError, match="60-second deadline"):
        workspace.git(tmp_path, "fetch", "origin")


@pytest.fixture
def initialized_module_run(run, tmp_path):
    import subprocess

    completed(run)
    git(run["owner"], "pull", "--ff-only", "origin", "master")
    module_source = tmp_path / "local-theme-source"
    module_source.mkdir()
    git(module_source, "init", "--initial-branch=master")
    git(module_source, "config", "user.email", "fixture@example.invalid")
    git(module_source, "config", "user.name", "Offline fixture")
    (module_source / "theme.txt").write_text("Theme bytes with retained local Git history")
    (module_source / ".gitignore").write_text("ignored-*\n")
    git(module_source, "add", ".")
    git(module_source, "commit", "-m", "offline theme")
    git(
        run["owner"],
        "-c",
        "protocol.file.allow=always",
        "submodule",
        "add",
        str(module_source),
        "themes/archie",
    )
    git(run["owner"], "commit", "-am", "offline theme dependency")
    git(run["owner"], "push", "origin", "master")
    args = next_args(run)
    args.date, args.run_id, args.recover_abandoned = "2026-09-16", "module-noop", False
    created = workspace.create(args)
    root, path = Path(created["workspace"]), Path(created["manifest"])
    git(root, "-c", "protocol.file.allow=always", "submodule", "update", "--init")
    workspace.complete_noop(path)
    # The Git-specific guard itself is part of the regression, not an assumption.
    guard = subprocess.run(
        ["git", "-C", str(run["owner"]), "worktree", "remove", str(root)],
        text=True,
        capture_output=True,
    )
    assert guard.returncode == 128
    assert "working trees containing submodules" in guard.stderr
    return {**run, "root": root, "manifest": path, "module": root / "themes/archie"}


def test_clean_owned_submodule_retires_with_complete_offline_restorable_archive(
    initialized_module_run, tmp_path, monkeypatch
):
    import hashlib
    import tarfile

    run = initialized_module_run
    config = run["owner"] / ".git/config"
    before = config.read_bytes()
    owner_module = run["owner"] / "themes/archie/theme.txt"
    owner_bytes = owner_module.read_bytes()
    owner_refs = git(run["owner"], "show-ref")
    module_refs = git(run["module"], "show-ref")
    gitdir = Path(git(run["module"], "rev-parse", "--absolute-git-dir"))
    expected = {
        str(p.relative_to(gitdir)): p.read_bytes() for p in gitdir.rglob("*") if p.is_file()
    }
    result = retire(run, tmp_path, monkeypatch)
    assert "module-noop" in result["retired_runs"], result
    assert not run["root"].exists()
    assert config.read_bytes() == before
    assert owner_module.read_bytes() == owner_bytes
    assert git(run["owner"], "show-ref") == owner_refs
    with tarfile.open(run["manifest"].parent / "checkout-evidence.tar") as archive:
        assert (
            archive.extractfile("submodule-workspace/themes/archie/theme.txt").read() == owner_bytes
        )
        for name, raw in expected.items():
            assert archive.extractfile(f"submodule-git/modules/themes/archie/{name}").read() == raw
        # Restore only this known fixture's regular archive entries, offline.
        restored = tmp_path / "restored-module.git"
        restored.mkdir()
        for name, raw in expected.items():
            p = restored / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(raw)
    assert git(restored, "--work-tree", str(tmp_path), "show-ref") == module_refs
    assert (
        git(restored, "--work-tree", str(tmp_path), "show", "HEAD:theme.txt")
        == owner_bytes.decode()
    )
    receipt = json.loads((run["manifest"].parent / "checkout-retirement.json").read_text())
    assert (
        receipt["submodule_hashes"]["submodule-workspace/themes/archie/theme.txt"]
        == hashlib.sha256(owner_bytes).hexdigest()
    )


@pytest.mark.parametrize(
    "change", ["tracked", "staged", "untracked", "ignored", "head", "external"]
)
def test_submodule_foreign_state_is_protected(
    initialized_module_run, tmp_path, monkeypatch, change
):
    run = initialized_module_run
    module = run["module"]
    if change in ("tracked", "staged"):
        (module / "theme.txt").write_text("Uncommitted owner bytes")
        if change == "staged":
            git(module, "add", "theme.txt")
    elif change == "head":
        (module / "theme.txt").write_text("Unpublished module commit")
        git(
            module,
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-am",
            "unpublished",
        )
    elif change == "external":
        gitdir = Path(git(module, "rev-parse", "--absolute-git-dir"))
        (module / ".git").write_text(f"gitdir: {run['owner'] / '.git/modules/themes/archie'}\n")
        assert gitdir.exists()
    else:
        (module / ("ignored-private" if change == "ignored" else "foreign.txt")).write_text("keep")
    config = (run["owner"] / ".git/config").read_bytes()
    result = retire(run, tmp_path, monkeypatch)
    assert "module-noop" not in result["retired_runs"]
    assert run["root"].exists()
    assert (run["owner"] / ".git/config").read_bytes() == config


def test_uninitialized_committed_gitlink_noop_retires_without_network_module_fetch(
    initialized_module_run, tmp_path, monkeypatch
):
    args = next_args(initialized_module_run)
    args.date, args.run_id, args.recover_abandoned = "2026-09-16", "empty-module-noop", False
    created = workspace.create(args)
    path, root = Path(created["manifest"]), Path(created["workspace"])
    workspace.complete_noop(path)
    assert not (root / "themes/archie/.git").exists()
    result = retire(initialized_module_run, tmp_path, monkeypatch)
    assert "empty-module-noop" in result["retired_runs"], result
    receipt = json.loads((path.parent / "checkout-retirement.json").read_text())
    assert receipt["gitlinks"]["themes/archie"]["initialized"] is False
    assert receipt["submodule_files"] == {}


def test_native_tracked_beads_metadata_uses_preserved_external_owner_db(run, tmp_path, monkeypatch):
    completed(run)
    git(run["owner"], "pull", "--ff-only", "origin", "master")
    beads = run["owner"] / ".beads"
    beads.mkdir()
    (beads / "config.yaml").write_text("issue-prefix: fixture\n")
    (beads / ".gitignore").write_text("embeddeddolt/\nbackup/\nexport-state.json\n")
    git(run["owner"], "add", ".beads")
    git(run["owner"], "commit", "-m", "tracked task metadata")
    git(run["owner"], "push", "origin", "master")
    canonical = beads / "embeddeddolt"
    canonical.mkdir()
    (canonical / "authoritative-data").write_bytes(b"preserve authoritative tasks")
    args = next_args(run)
    args.date, args.run_id, args.recover_abandoned = "2026-09-16", "native-beads-noop", False
    created = workspace.create(args)
    root, path = Path(created["workspace"]), Path(created["manifest"])
    assert (root / ".beads/config.yaml").exists()
    assert not (root / ".beads/embeddeddolt").exists()
    workspace.complete_noop(path)
    result = retire(run, tmp_path, monkeypatch)
    assert "native-beads-noop" in result["retired_runs"], result
    assert (canonical / "authoritative-data").read_bytes() == b"preserve authoritative tasks"
    assert (beads / "config.yaml").read_text() == "issue-prefix: fixture\n"


def test_locked_worktree_never_uses_double_force(run, tmp_path, monkeypatch):
    completed(run)
    git(run["owner"], "worktree", "lock", str(run["root"]))
    result = retire(run, tmp_path, monkeypatch)
    assert result["retired_runs"] == []
    assert "locked" in result["protected_runs"][0]["reason"]
    assert run["root"].exists()


def test_live_child_inherits_lock_after_parent_holder_closes(run, tmp_path, monkeypatch):
    import subprocess
    import sys

    completed(run)
    stream = (run["manifest"].parent / "producer.lock").open("a")
    fcntl.flock(stream, fcntl.LOCK_EX)
    child = subprocess.Popen(
        [sys.executable, "-c", "import sys; sys.stdin.read()"],
        stdin=subprocess.PIPE,
        pass_fds=(stream.fileno(),),
    )
    stream.close()
    try:
        result = retire(run, tmp_path, monkeypatch)
        assert result["retired_runs"] == []
        assert "producer is still running" in result["protected_runs"][0]["reason"]
    finally:
        child.communicate(timeout=10)
    assert retire(run, tmp_path, monkeypatch)["retired_runs"]


def test_canary_cannot_retire_existing_checkout(run, tmp_path, monkeypatch):
    completed(run)
    monkeypatch.setenv("BLOG_CANARY", "1")
    with pytest.raises(workspace.WorkspaceError, match="canary cannot retire"):
        retire(run, tmp_path, monkeypatch)
    assert run["root"].exists()
    with pipeline_lock(tmp_path, monkeypatch):
        created = workspace.create(next_args(run))
    assert created["retention"] is None
    assert run["root"].exists()


def test_registry_symlink_refused_before_any_mutation(run, tmp_path):
    args = next_args(run)
    link = tmp_path / "registry-link"
    link.symlink_to(args.state_dir, target_is_directory=True)
    args.state_dir = link
    before = run["manifest"].read_bytes()
    with pytest.raises(workspace.WorkspaceError, match="symlinks"):
        workspace.create(args)
    assert run["manifest"].read_bytes() == before


def test_corrupted_prepared_archive_never_authorizes_missing_checkout(run, tmp_path, monkeypatch):
    completed(run)
    original = workspace.git

    class SimulatedTermination(BaseException):
        pass

    def interrupted(repo, *args):
        if args[:2] == ("worktree", "remove"):
            original(repo, *args)
            raise SimulatedTermination()
        return original(repo, *args)

    monkeypatch.setattr(workspace, "git", interrupted)
    with pytest.raises(SimulatedTermination):
        retire(run, tmp_path, monkeypatch)
    monkeypatch.setattr(workspace, "git", original)
    (run["manifest"].parent / "checkout-evidence.tar").write_bytes(b"corrupted")
    result = retire(run, tmp_path, monkeypatch)
    assert result["retired_runs"] == []
    assert "evidence archive changed" in result["protected_runs"][0]["reason"]
    assert "checkout_retirement" not in json.loads(run["manifest"].read_text())


def test_foreign_write_after_git_submodule_guard_is_not_force_removed(
    initialized_module_run, tmp_path, monkeypatch
):
    run = initialized_module_run
    original = workspace.git
    calls = []

    def race(repo, *args):
        calls.append(args)
        if args == ("worktree", "remove", str(run["root"])):
            (run["root"] / "foreign-after-check.txt").write_text("must survive")
        return original(repo, *args)

    monkeypatch.setattr(workspace, "git", race)
    result = retire(run, tmp_path, monkeypatch)
    assert "module-noop" not in result["retired_runs"]
    assert (run["root"] / "foreign-after-check.txt").read_text() == "must survive"
    assert not any(args[:3] == ("worktree", "remove", "--force") for args in calls)


def interrupt_inside_git_removal(run, tmp_path, monkeypatch):
    """Kill the actual Git child after generated-file unlink begins, with owned files remaining."""
    import signal
    import subprocess
    import time

    public = run["root"] / "public"
    public.mkdir(exist_ok=True)
    for index in range(6000):
        (public / f"generated-{index:05}.html").write_text("Disposable generated fixture\n")
    original = workspace.git

    class InterruptedGitRemoval(BaseException):
        pass

    def interrupted(repo, *args):
        if args[:2] != ("worktree", "remove") or args[-1] != str(run["root"]):
            return original(repo, *args)
        process = subprocess.Popen(
            ["git", "-C", str(repo), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        limit = time.monotonic() + 10
        stopped = False
        while time.monotonic() < limit and process.poll() is None:
            if any(
                not (public / f"generated-{index:05}.html").exists()
                for index in range(0, 6000, 500)
            ):
                os.kill(process.pid, signal.SIGSTOP)
                stopped = True
                break
            time.sleep(0.0005)
        if not stopped:
            output, error = process.communicate(timeout=10)
            raise AssertionError(f"Git removal was not interrupted: {process.returncode} {error!r}")
        process.kill()
        process.communicate(timeout=10)
        assert process.returncode == -signal.SIGKILL
        assert run["root"].exists()
        assert any(public.iterdir()), "actual owned remainder must exist at the crash boundary"
        raise InterruptedGitRemoval()

    monkeypatch.setattr(workspace, "git", interrupted)
    try:
        with pytest.raises(InterruptedGitRemoval):
            retire(run, tmp_path, monkeypatch)
    finally:
        monkeypatch.setattr(workspace, "git", original)
    receipt = json.loads((run["manifest"].parent / "checkout-retirement.json").read_text())
    assert receipt["removal_started_at"]
    assert (run["manifest"].parent / "checkout-inventory.json").stat().st_mode & 0o777 == 0o600
    return receipt


def test_actual_killed_git_removal_finishes_unchanged_owned_remnants(run, tmp_path, monkeypatch):
    completed(run)
    refs = git(run["owner"], "show-ref")
    config = (run["owner"] / ".git/config").read_bytes()
    receipt = interrupt_inside_git_removal(run, tmp_path, monkeypatch)
    result = retire(run, tmp_path, monkeypatch)
    assert result["retired_runs"], result
    assert not run["root"].exists()
    assert not Path(receipt["worktree_gitdir"]).exists()
    assert not (run["manifest"].parent / "checkout-inventory.json").exists()
    assert git(run["owner"], "show-ref") == refs
    assert (run["owner"] / ".git/config").read_bytes() == config
    assert retire(run, tmp_path, monkeypatch)["retired_runs"] == []


@pytest.mark.parametrize("change", ["modified", "new", "symlink", "mode", "new-directory"])
def test_changed_remnants_after_killed_git_are_never_deleted(run, tmp_path, monkeypatch, change):
    completed(run)
    interrupt_inside_git_removal(run, tmp_path, monkeypatch)
    marker = next((run["root"] / "public").iterdir())
    if change == "modified":
        marker.write_text("New owner bytes must remain")
    elif change == "new":
        marker = run["root"] / "new-foreign-file"
        marker.write_text("New owner bytes must remain")
    elif change == "symlink":
        marker = run["root"] / "new-linked-file"
        target = tmp_path / "external-must-remain"
        target.write_text("Outside registry")
        marker.symlink_to(target)
    elif change == "mode":
        marker.chmod(0o700)
    else:
        marker = run["root"] / "new-foreign-directory"
        marker.mkdir()
    result = retire(run, tmp_path, monkeypatch)
    assert result["retired_runs"] == []
    assert marker.exists()
    assert (run["manifest"].parent / "checkout-inventory.json").exists()
    assert run["root"].exists()


@pytest.mark.parametrize("change", [None, "new", "modified", "symlink"])
def test_partial_private_git_admin_cleanup_is_proved_or_protected(
    run, tmp_path, monkeypatch, change
):
    completed(run)
    original = workspace.git

    class InterruptedPrivateAdmin(BaseException):
        pass

    def interrupted(repo, *args):
        if args[:2] == ("worktree", "remove"):
            inventory = json.loads((run["manifest"].parent / "checkout-inventory.json").read_text())
            workspace.remove_proved_remainder(run["root"], inventory["checkout"])
            admin = Path(inventory["git_admin"]["path"])
            (admin / "HEAD").unlink()
            (admin / "gitdir").unlink()
            raise InterruptedPrivateAdmin()
        return original(repo, *args)

    monkeypatch.setattr(workspace, "git", interrupted)
    with pytest.raises(InterruptedPrivateAdmin):
        retire(run, tmp_path, monkeypatch)
    monkeypatch.setattr(workspace, "git", original)
    receipt = json.loads((run["manifest"].parent / "checkout-retirement.json").read_text())
    admin = Path(receipt["worktree_gitdir"])
    if change == "new":
        (admin / "foreign-ref").write_text("must remain")
    elif change == "modified":
        (admin / "commondir").write_text("different Git ownership")
    elif change == "symlink":
        (admin / "foreign-link").symlink_to(tmp_path / "outside")
    result = retire(run, tmp_path, monkeypatch)
    if change is None:
        assert result["retired_runs"], result
        assert not admin.exists()
        assert not (run["manifest"].parent / "checkout-inventory.json").exists()
    else:
        assert result["retired_runs"] == []
        assert admin.exists()
        assert (run["manifest"].parent / "checkout-inventory.json").exists()


@pytest.mark.parametrize("change", ["new-public", "changed-public", "new-resources", "admin"])
def test_ignored_or_git_metadata_changes_before_force_are_preserved(
    initialized_module_run, tmp_path, monkeypatch, change
):
    run = initialized_module_run
    public = run["root"] / "public"
    public.mkdir()
    (public / "original.html").write_text("Originally generated bytes")
    original = workspace.git
    touched = []

    def race(repo, *args):
        if args == ("worktree", "remove", str(run["root"])):
            if change == "admin":
                admin = Path(
                    original(run["root"], "rev-parse", "--absolute-git-dir").decode().strip()
                )
                marker = admin / "foreign-new-metadata"
            elif change == "new-resources":
                marker = run["root"] / "resources/_gen/new.txt"
                marker.parent.mkdir(parents=True)
            else:
                marker = public / ("original.html" if change == "changed-public" else "new.html")
            marker.write_text("New bytes after preparation must survive")
            touched.append(marker)
        assert args[:3] != ("worktree", "remove", "--force"), (
            "changed evidence must never reach force"
        )
        return original(repo, *args)

    monkeypatch.setattr(workspace, "git", race)
    result = retire(run, tmp_path, monkeypatch)
    assert "module-noop" not in result["retired_runs"], result
    assert touched and touched[0].read_text() == "New bytes after preparation must survive"
    assert run["root"].exists()


def test_directory_only_inventory_is_bounded_before_scan(tmp_path, monkeypatch):
    root = tmp_path / "only-directories"
    root.mkdir()
    for index in range(12):
        (root / str(index)).mkdir()
    monkeypatch.setattr(workspace, "INVENTORY_MAX_FILES", 5)
    with pytest.raises(workspace.WorkspaceError, match="bounded checkout limit"):
        workspace.tree_inventory(root)


def test_tar_header_and_padding_bytes_are_included_in_archive_bound(run, tmp_path, monkeypatch):
    completed(run)
    manifest = json.loads(run["manifest"].read_text())
    details = workspace.retirement_proof(run["manifest"], manifest)
    admin = Path(git(run["root"], "rev-parse", "--absolute-git-dir"))
    size = sum(
        len(workspace.git(run["root"], "show", f"{details['published_sha']}:{name}"))
        for name in details["artifacts"]
    )
    size += sum((run["root"] / name).stat().st_size for name in details["auxiliary_files"])
    size += sum(path.stat().st_size for path in admin.rglob("*") if path.is_file())
    limit = size + 128  # Payload fits; tar's headers and record padding do not.
    monkeypatch.setattr(workspace, "ARCHIVE_LIMIT_BYTES", limit)
    result = retire(run, tmp_path, monkeypatch)
    assert result["retired_runs"] == []
    assert "serialized retirement archive" in result["protected_runs"][0]["reason"]
    assert run["root"].exists()
    assert not (run["manifest"].parent / "checkout-retirement.json").exists()
    assert not (run["manifest"].parent / "checkout-evidence.tar").exists()
    assert (run["manifest"].parent / "checkout-evidence.tmp").stat().st_size <= limit


def test_pretty_inventory_serialization_cannot_exceed_retained_bound(run, tmp_path, monkeypatch):
    completed(run)
    admin = Path(git(run["root"], "rev-parse", "--absolute-git-dir"))
    inventory = {
        "schema_version": 1,
        "checkout": workspace.tree_inventory(run["root"]),
        "git_admin": workspace.tree_inventory(admin),
    }
    exact = len((json.dumps(inventory, indent=2, sort_keys=True) + "\n").encode())
    assert len(json.dumps(inventory).encode()) < exact
    monkeypatch.setattr(workspace, "INVENTORY_LIMIT_BYTES", exact - 1)
    result = retire(run, tmp_path, monkeypatch)
    assert result["retired_runs"] == []
    assert "bounded metadata limit" in result["protected_runs"][0]["reason"]
    assert run["root"].exists()
    assert not (run["manifest"].parent / "checkout-inventory.json").exists()
    assert not (run["manifest"].parent / "checkout-retirement.json").exists()
