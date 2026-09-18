"""Execute release/deploy shell guards against local bare Git; no external transport."""

import os
import re
import subprocess
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RELEASE = Path(
    os.environ.get("BLOG_RELEASE_WORKFLOW_UNDER_TEST", ROOT / ".github/workflows/release.yml")
)
DEPLOY = Path(
    os.environ.get("BLOG_DEPLOY_WORKFLOW_UNDER_TEST", ROOT / ".github/workflows/deploy.yml")
)
VERSION = "1.2.4"
TAG = "v" + VERSION
REPO_NAME = "jeremylongshore/startaitools.com"


def shell_step(workflow, name):
    body = workflow.read_text().split(f"      - name: {name}\n", 1)[1]
    body = re.split(r"\n(?:      - |  [a-z][a-z-]*:)", body, maxsplit=1)[0]
    script = textwrap.dedent(body.split("        run: |\n", 1)[1])
    for expression, value in (
        ("steps.ver.outputs.new", VERSION),
        ("steps.ver.outputs.tag", TAG),
        ("steps.clog.outputs.notes", "fixture-notes"),
        ("steps.prev.outputs.prev", TAG),
        ("steps.ver.outputs.tag || steps.prev.outputs.prev", TAG),
        ("steps.clog.outputs.notes || steps.resume.outputs.notes", "fixture-notes"),
    ):
        script = script.replace("${{ " + expression + " }}", value)
    assert "${{" not in script
    return script


def job_body(workflow, name):
    return re.search(
        r"(?ms)^  " + re.escape(name) + r":\n(.*?)(?=^  [a-z][a-z-]*:|\Z)", workflow.read_text()
    ).group(1)


def condition_matches(condition, fields):
    # Evaluate only the actual workflow's comparisons with explicit fixture
    # context; no provider/GitHub event is dispatched by these offline tests.
    expression = re.sub(
        r"\b(?:github|needs|steps)\.[A-Za-z0-9_.-]+",
        lambda m: repr(fields.get(m[0], "")),
        condition,
    )
    expression = expression.replace("&&", " and ").replace("||", " or ")
    return eval(expression, {"__builtins__": {}}, {})


def condition(body):
    return re.search(r"(?m)^    if: (.+)$", body)[1]


@pytest.fixture
def release_fixture(tmp_path):
    repo = tmp_path / "candidate"
    remote = tmp_path / "origin.git"
    repo.mkdir()
    home = tmp_path / "home"
    home.mkdir()
    binary = home / "bin"
    binary.mkdir()
    output = tmp_path / "outputs"
    gh_called = tmp_path / "gh-called"
    env = {
        "PATH": f"{binary}:/usr/local/bin:/usr/bin:/bin",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_ALLOW_PROTOCOL": "file",
        "GIT_TERMINAL_PROMPT": "0",
        "GITHUB_REPOSITORY": REPO_NAME,
        "GITHUB_REF": "refs/heads/master",
        "GITHUB_EVENT_NAME": "push",
        "DEFAULT_BRANCH": "master",
        "GITHUB_OUTPUT": str(output),
        "GH_FIXTURE_CALLED": str(gh_called),
        "GH_FIXTURE_EXIT": "0",
        "RELEASE_EXISTS": "",
        "GH_FIXTURE_API_STATUS": "auto",
        "GH_FIXTURE_CREATED": str(tmp_path / "server-created-release"),
        "GH_FIXTURE_CREATE_MISSING": "0",
        "GH_FIXTURE_API_EXIT": "1",
        "GH_FIXTURE_API_BODY": '{"message":"Not Found"}',
        "EXPECTED_RELEASE_SHA": "",
        "EXPECTED_RELEASE_TAG": "",
    }
    gh = binary / "gh"
    gh.write_text(
        "#!/bin/sh\n"
        'if [ "$1" = api ]; then\n'
        '  if [ "$GH_FIXTURE_API_STATUS" = auto ]; then\n'
        '    if [ -f "$GH_FIXTURE_CREATED" ]; then\n'
        "      GH_FIXTURE_API_STATUS=200; GH_FIXTURE_API_EXIT=0\n"
        '      GH_FIXTURE_API_BODY=\'{"tag_name":"v1.2.4","draft":false,"prerelease":false,'
        '"published_at":"2030-01-02T03:04:05Z"}\'\n'
        "    else\n"
        "      GH_FIXTURE_API_STATUS=404\n"
        "    fi\n"
        "  fi\n"
        '  printf "HTTP/2.0 %s Fixture\\r\\n\\r\\n%s\\n" '
        '"$GH_FIXTURE_API_STATUS" "$GH_FIXTURE_API_BODY"\n'
        '  exit "$GH_FIXTURE_API_EXIT"\n'
        "fi\n"
        'printf "%s\\n" "$*" > "$GH_FIXTURE_CALLED"\n'
        'if [ "$GH_FIXTURE_EXIT" = 0 ] && [ "$GH_FIXTURE_CREATE_MISSING" = 0 ]; then\n'
        '  printf "created\\n" > "$GH_FIXTURE_CREATED"\n'
        "fi\n"
        'exit "$GH_FIXTURE_EXIT"\n'
    )
    gh.chmod(0o755)

    def git(where, *args, check=True):
        return subprocess.run(
            ["git", "-C", str(where), *args],
            env=env,
            capture_output=True,
            text=True,
            check=check,
            timeout=20,
        )

    git(repo, "init", "--initial-branch=master")
    git(repo, "config", "user.name", "Offline release fixture")
    git(repo, "config", "user.email", "fixture@example.invalid")
    (repo / "version.txt").write_text("1.2.3\n")
    (repo / "CHANGELOG.md").write_text("# Release v1.2.3\n")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "Offline release baseline")
    old = git(repo, "rev-parse", "HEAD").stdout.strip()
    git(tmp_path, "init", "--bare", "--initial-branch=master", str(remote))
    git(repo, "remote", "add", "origin", str(remote))
    git(repo, "push", "origin", "HEAD:refs/heads/master")
    git(repo, "config", "user.name", "github-actions[bot]")
    git(repo, "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    (repo / "version.txt").write_text(VERSION + "\n")
    git(repo, "add", "version.txt")
    git(repo, "commit", "-m", f"chore: release {TAG} [skip ci]")
    (repo / "CHANGELOG.md").write_text("# Release " + TAG + "\n")
    git(repo, "add", "CHANGELOG.md")
    git(repo, "commit", "-m", f"docs: update changelog for {TAG} [skip ci]")
    env["GITHUB_SHA"] = old
    new = git(repo, "rev-parse", "HEAD").stdout.strip()
    return {
        "repo": repo,
        "remote": remote,
        "env": env,
        "git": git,
        "old": old,
        "new": new,
        "output": output,
        "gh_called": gh_called,
    }


def execute(fixture, script, **env):
    return subprocess.run(
        ["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", script],
        cwd=fixture["repo"],
        env={**fixture["env"], **env},
        capture_output=True,
        text=True,
        timeout=25,
    )


def publish(fixture, *, github_release=True):
    script = shell_step(RELEASE, "Create tag and push")
    if github_release:
        script += "\n" + shell_step(RELEASE, "Create GitHub Release")
    return execute(fixture, script)


def remote_revision(fixture, ref):
    return fixture["git"](fixture["remote"], "rev-parse", "--verify", ref, check=False)


def assert_no_published_output(fixture):
    assert not fixture["output"].exists() or "published=true" not in fixture["output"].read_text()


def reject_ref(fixture, ref):
    hook = fixture["remote"] / "hooks/update"
    hook.write_text(
        f'#!/bin/sh\nif [ "$1" = "{ref}" ]; then\n'
        '  echo "offline protected ref refusal" >&2\n  exit 42\nfi\n'
    )
    hook.chmod(0o755)


def test_atomic_success_publishes_same_release_branch_and_annotated_tag(release_fixture):
    f = release_fixture
    result = publish(f)
    assert result.returncode == 0, result.stderr
    assert remote_revision(f, "refs/heads/master").stdout.strip() == f["new"]
    assert remote_revision(f, f"refs/tags/{TAG}^{{commit}}").stdout.strip() == f["new"]
    assert f["git"](f["remote"], "cat-file", "-t", "refs/tags/" + TAG).stdout.strip() == "tag"
    assert f["git"](f["remote"], "show", "master:version.txt").stdout == VERSION + "\n"
    assert f["output"].read_text().splitlines() == [
        "release-sha=" + f["new"],
        "release-tag=" + TAG,
        "published=true",
    ]
    assert f["gh_called"].exists()


@pytest.mark.parametrize("rejected", ["refs/heads/master", "refs/tags/" + TAG])
def test_ref_rejection_cannot_publish_either_ref_or_claim_release(release_fixture, rejected):
    f = release_fixture
    reject_ref(f, rejected)
    result = publish(f)
    assert "offline protected ref refusal" in result.stderr
    assert result.returncode != 0
    assert remote_revision(f, "refs/heads/master").stdout.strip() == f["old"]
    assert remote_revision(f, "refs/tags/" + TAG).returncode != 0
    assert not f["gh_called"].exists()
    assert_no_published_output(f)


def advance_remote(fixture):
    f = fixture
    clone = f["repo"].parent / "independent-writer"
    f["git"](f["repo"].parent, "clone", str(f["remote"]), str(clone))
    f["git"](clone, "config", "user.name", "Independent fixture")
    f["git"](clone, "config", "user.email", "fixture@example.invalid")
    (clone / "new-source.txt").write_text("Independent later source\n")
    f["git"](clone, "add", ".")
    f["git"](clone, "commit", "-m", "Offline concurrent master update")
    f["git"](clone, "push", "origin", "master")
    return f["git"](clone, "rev-parse", "HEAD").stdout.strip()


def test_non_fast_forward_preserves_new_owner_branch_and_does_not_orphan_tag(release_fixture):
    f = release_fixture
    owner = advance_remote(f)
    result = publish(f)
    assert result.returncode != 0
    assert remote_revision(f, "refs/heads/master").stdout.strip() == owner
    assert remote_revision(f, "refs/tags/" + TAG).returncode != 0
    assert not f["gh_called"].exists()
    assert_no_published_output(f)


def test_historical_workflow_reproduces_parallel_deploy_and_orphan_release(release_fixture):
    f = release_fixture
    baseline = "ecd3b1b9d7763aadc2966bb972c5f54b5bb32c3d"
    old_release = f["repo"].parent / "historical-release.yml"
    old_release.write_text(
        f["git"](ROOT, "show", baseline + ":.github/workflows/release.yml").stdout
    )
    old_deploy = f["git"](ROOT, "show", baseline + ":.github/workflows/deploy.yml").stdout
    assert "  push:\n    branches: [master]" in old_deploy
    # The old independent push-triggered deploy can read master before the
    # release bot commits land. A refused later branch push leaves it there.
    deployed_revision = remote_revision(f, "refs/heads/master").stdout.strip()
    reject_ref(f, "refs/heads/master")
    result = execute(
        f,
        shell_step(old_release, "Create tag and push")
        + "\n"
        + shell_step(old_release, "Create GitHub Release"),
    )
    assert result.returncode == 0
    assert "offline protected ref refusal" in result.stderr
    assert f["gh_called"].exists()
    assert deployed_revision == remote_revision(f, "refs/heads/master").stdout.strip()
    assert deployed_revision == f["old"]
    assert remote_revision(f, f"refs/tags/{TAG}^{{commit}}").stdout.strip() == f["new"]
    assert f["git"](f["remote"], "show", "master:version.txt").stdout == "1.2.3\n"
    assert f["git"](f["remote"], "show", TAG + ":version.txt").stdout == VERSION + "\n"


def test_server_without_atomic_support_fails_without_partial_publication(release_fixture):
    f = release_fixture
    f["git"](f["remote"], "config", "receive.advertiseAtomic", "false")
    assert publish(f).returncode != 0
    assert remote_revision(f, "refs/heads/master").stdout.strip() == f["old"]
    assert remote_revision(f, "refs/tags/" + TAG).returncode != 0
    assert not f["gh_called"].exists()
    assert_no_published_output(f)


def test_github_release_failure_withholds_deployment_authorization(release_fixture):
    f = release_fixture
    f["env"]["GH_FIXTURE_EXIT"] = "23"
    assert publish(f).returncode == 23
    assert remote_revision(f, "refs/heads/master").stdout.strip() == f["new"]
    assert remote_revision(f, f"refs/tags/{TAG}^{{commit}}").stdout.strip() == f["new"]
    assert_no_published_output(f)


def test_existing_tag_collision_is_fatal_without_replacing_or_claiming_it(release_fixture):
    f = release_fixture
    f["git"](f["repo"], "tag", "-a", TAG, f["old"], "-m", "Existing fixture tag")
    old_tag = f["git"](f["repo"], "rev-parse", "refs/tags/" + TAG).stdout
    assert publish(f).returncode != 0
    assert f["git"](f["repo"], "rev-parse", "refs/tags/" + TAG).stdout == old_tag
    assert remote_revision(f, "refs/heads/master").stdout.strip() == f["old"]
    assert not f["gh_called"].exists()
    assert_no_published_output(f)


@pytest.mark.parametrize(
    "field,value",
    [
        ("GITHUB_REPOSITORY", "foreign/fork"),
        ("GITHUB_REF", "refs/heads/feature"),
        ("DEFAULT_BRANCH", "main"),
    ],
)
def test_release_target_refuses_foreign_repository_or_nondefault_branch(
    release_fixture, field, value
):
    f = release_fixture
    f["env"][field] = value
    assert execute(f, shell_step(RELEASE, "Verify release target")).returncode != 0
    assert publish(f).returncode != 0
    assert remote_revision(f, "refs/heads/master").stdout.strip() == f["old"]
    assert remote_revision(f, "refs/tags/" + TAG).returncode != 0


def identity(fixture, *, manual=False):
    f = fixture
    return execute(
        f,
        shell_step(DEPLOY, "Verify released master before deployment"),
        EXPECTED_RELEASE_SHA="" if manual else f["new"],
        EXPECTED_RELEASE_TAG="" if manual else TAG,
        GITHUB_EVENT_NAME="workflow_dispatch" if manual else "push",
    )


@pytest.mark.parametrize("manual", [False, True])
def test_deploy_guard_accepts_only_committed_released_master(release_fixture, manual):
    f = release_fixture
    assert publish(f, github_release=False).returncode == 0
    result = identity(f, manual=manual)
    assert result.returncode == 0, result.stderr
    assert "release-sha=" + f["new"] in f["output"].read_text()


@pytest.mark.parametrize(
    "bad",
    [
        "unpublished",
        "branch-lag",
        "wrong-sha",
        "wrong-tag",
        "lightweight",
        "wrong-version",
        "wrong-changelog",
        "partial-input",
        "missing-call-inputs",
    ],
)
def test_deploy_guard_refuses_unpublished_or_mismatched_artifact(release_fixture, bad):
    f = release_fixture
    if bad == "branch-lag":
        f["git"](f["repo"], "tag", "-a", TAG, "-m", "Offline orphan tag")
        f["git"](f["repo"], "push", "origin", TAG)
    elif bad == "lightweight":
        f["git"](f["repo"], "tag", TAG)
        f["git"](f["repo"], "push", "origin", "HEAD:master", TAG)
    elif bad != "unpublished":
        if bad in ("wrong-version", "wrong-changelog"):
            path = f["repo"] / ("version.txt" if bad == "wrong-version" else "CHANGELOG.md")
            path.write_text("mismatched artifact\n")
            f["git"](f["repo"], "add", ".")
            f["git"](f["repo"], "commit", "-m", "Offline invalid artifact")
            f["new"] = f["git"](f["repo"], "rev-parse", "HEAD").stdout.strip()
        assert publish(f, github_release=False).returncode == 0
    sha = f["old"] if bad == "wrong-sha" else f["new"]
    tag = "v9.9.9" if bad == "wrong-tag" else TAG
    if bad == "partial-input":
        tag = ""
    elif bad == "missing-call-inputs":
        sha = tag = ""
    result = execute(
        f,
        shell_step(DEPLOY, "Verify released master before deployment"),
        EXPECTED_RELEASE_SHA=sha,
        EXPECTED_RELEASE_TAG=tag,
    )
    assert result.returncode != 0
    assert not f["output"].exists()


def test_post_deploy_guard_exposes_concurrent_master_movement(release_fixture):
    f = release_fixture
    assert publish(f, github_release=False).returncode == 0
    tag_object = remote_revision(f, "refs/tags/" + TAG).stdout.strip()
    assert identity(f).returncode == 0
    script = shell_step(DEPLOY, "Verify release refs stayed unchanged during deployment")
    env = {
        "EXPECTED_RELEASE_SHA": f["new"],
        "EXPECTED_RELEASE_TAG": TAG,
        "EXPECTED_TAG_OBJECT": tag_object,
    }
    assert execute(f, script, **env).returncode == 0
    advance_remote(f)
    assert execute(f, script, **env).returncode != 0


def test_deployment_is_called_after_release_instead_of_racing_source_push():
    deploy = DEPLOY.read_text()
    events = deploy.split("on:\n", 1)[1].split("\npermissions:", 1)[0]
    assert "  push:" not in events
    assert "  workflow_run:" not in events
    assert "  workflow_call:" in events and "  workflow_dispatch:" in events
    release_deploy = job_body(RELEASE, "deploy")
    assert "needs: release" in release_deploy
    assert "uses: ./.github/workflows/deploy.yml" in release_deploy
    assert "needs.release.outputs.release-sha" in release_deploy
    assert "needs.release.outputs.release-tag" in release_deploy
    for status in ("", "false", "true"):
        assert condition_matches(
            condition(release_deploy), {"needs.release.outputs.published": status}
        ) is (status == "true")
    for name in ("Create tag and push", "Create GitHub Release"):
        body = (
            RELEASE.read_text().split(f"      - name: {name}\n", 1)[1].split("        run: |", 1)[0]
        )
        expression = re.search(r"(?m)^        if: (.+)$", body)[1]
        for needed, dry_run in (("true", "true"), ("false", "false"), ("true", "false")):
            assert condition_matches(
                expression,
                {"steps.check.outputs.needed": needed, "github.event.inputs.dry_run": dry_run},
            ) is (needed == "true" and dry_run == "false")
    assert "group: release-${{ github.repository }}" in RELEASE.read_text()
    assert "group: deploy-vps-${{ github.repository }}" in deploy


@pytest.mark.parametrize(
    "field,value",
    [
        (None, None),
        ("github.repository", "foreign/fork"),
        ("github.ref", "refs/heads/feature"),
        ("github.event.repository.default_branch", "main"),
    ],
)
def test_caller_and_manual_dispatch_job_gate_require_canonical_default_master(field, value):
    fields = {
        "github.repository": REPO_NAME,
        "github.ref": "refs/heads/master",
        "github.event.repository.default_branch": "master",
    }
    if field:
        fields[field] = value
    for workflow, job in ((RELEASE, "verify"), (DEPLOY, "test")):
        assert condition_matches(condition(job_body(workflow, job)), fields) is (field is None)


def test_central_forced_transport_and_postcheck_dependencies_are_preserved():
    body = job_body(DEPLOY, "deploy")
    assert "needs: test" in body
    assert "vps-deploy.yml@53d6be37d6c046818157b954acb33667ac095dd8" in body
    supplied = body.split("    with:\n", 1)[1].split("    secrets:\n", 1)[0]
    assert set(re.findall(r"(?m)^      ([a-z-]+):", supplied)) == {
        "variant",
        "srv-path",
        "health-check-url",
        "vps-tailnet-ip",
        "vps-public-ip",
        "vps-host",
        "vps-user",
        "smoke-validation",
    }
    assert "needs: [test, deploy]" in job_body(DEPLOY, "verify-release-refs")
    assert "id-token: write" in job_body(RELEASE, "deploy")
    assert "needs: verify" in job_body(RELEASE, "release")
    assert "--force" not in shell_step(RELEASE, "Create tag and push")


def release_check(fixture):
    return execute(fixture, shell_step(RELEASE, "Check if release needed"))


def published_api(fixture):
    fixture["env"].update(
        GH_FIXTURE_API_STATUS="200",
        GH_FIXTURE_API_EXIT="0",
        GH_FIXTURE_API_BODY=(
            '{"tag_name":"v1.2.4","draft":false,"prerelease":false,'
            '"published_at":"2030-01-02T03:04:05Z"}'
        ),
    )


def test_same_event_retry_reconciles_missing_release_without_bump_or_ref_rewrite(release_fixture):
    f = release_fixture
    f["env"]["GH_FIXTURE_EXIT"] = "23"
    assert publish(f).returncode == 23
    assert_no_published_output(f)
    published_refs = f["git"](f["remote"], "show-ref").stdout
    # Actions reruns retain the original triggering SHA, before the bot's two
    # metadata commits. Only the exact already-published chain may be adopted.
    f["git"](f["repo"], "checkout", "--detach", f["old"])
    checked = release_check(f)
    assert checked.returncode == 0, checked.stderr
    assert f["output"].read_text() == "needed=false\nresume=true\n"
    assert f["git"](f["repo"], "rev-parse", "HEAD").stdout.strip() == f["new"]
    assert_no_published_output(f)
    notes = execute(f, shell_step(RELEASE, "Prepare existing release notes"))
    assert notes.returncode == 0, notes.stderr
    note_path = Path(f["output"].read_text().split("notes=", 1)[1].strip())
    assert note_path.read_text() == "# Release " + TAG + "\n"
    f["env"]["GH_FIXTURE_EXIT"] = "0"
    recovered = execute(f, shell_step(RELEASE, "Create GitHub Release"))
    assert recovered.returncode == 0, recovered.stderr
    assert (
        f["output"]
        .read_text()
        .endswith(f"release-sha={f['new']}\nrelease-tag={TAG}\npublished=true\n")
    )
    assert f["git"](f["remote"], "show-ref").stdout == published_refs
    assert f["git"](f["repo"], "rev-list", f["old"] + "..HEAD", "--count").stdout == "2\n"
    assert "--verify-tag --target " + f["new"] in f["gh_called"].read_text()


def test_server_accepted_release_with_client_failure_resumes_without_second_create(release_fixture):
    f = release_fixture
    f["env"]["GH_FIXTURE_EXIT"] = "23"
    assert publish(f).returncode == 23
    first_call = f["gh_called"].read_bytes()
    published_api(f)
    f["git"](f["repo"], "checkout", "--detach", f["old"])
    result = release_check(f)
    assert result.returncode == 0, result.stderr
    assert f["output"].read_text() == "needed=false\nresume=true\nrelease-exists=true\n"
    assert_no_published_output(f)
    # The stub still fails any create. Success here must reuse the independently
    # verified published API record, not make a second mutating API request.
    result = execute(f, shell_step(RELEASE, "Create GitHub Release"), RELEASE_EXISTS="true")
    assert result.returncode == 0, result.stderr
    assert f["gh_called"].read_bytes() == first_call
    assert "published=true" in f["output"].read_text()


def test_current_released_head_is_no_work_and_does_not_deploy(release_fixture):
    f = release_fixture
    assert publish(f, github_release=False).returncode == 0
    published_api(f)
    result = release_check(f)
    assert result.returncode == 0, result.stderr
    assert f["output"].read_text() == "needed=false\n"
    assert not f["gh_called"].exists()


@pytest.mark.parametrize(
    "status,exit_code,body",
    [
        ("401", "1", '{"message":"Bad credentials"}'),
        ("403", "1", '{"message":"Forbidden"}'),
        ("429", "1", '{"message":"Rate limited"}'),
        ("500", "1", '{"message":"Server error"}'),
        ("", "1", ""),
        ("404", "1", '{"message":"Malformed response"}'),
        ("404", "0", '{"message":"Not Found"}'),
        ("200", "0", '{"tag_name":"v9.9.9"}'),
        ("200", "0", '{"tag_name":"v1.2.4","draft":true}'),
        ("200", "0", '{"tag_name":"v1.2.4","draft":false,"prerelease":true}'),
        ("200", "0", '{"tag_name":"v1.2.4","draft":false,"prerelease":false}'),
        ("200", "0", "malformed"),
    ],
)
def test_release_lookup_failures_never_mean_missing_or_published(
    release_fixture, status, exit_code, body
):
    f = release_fixture
    assert publish(f, github_release=False).returncode == 0
    f["env"].update(
        GH_FIXTURE_API_STATUS=status, GH_FIXTURE_API_EXIT=exit_code, GH_FIXTURE_API_BODY=body
    )
    result = release_check(f)
    assert result.returncode != 0
    assert not f["gh_called"].exists()
    assert not f["output"].exists()


@pytest.mark.parametrize("bad", ["owner-commit", "wrong-trigger", "remote-advance", "missing-tag"])
def test_retry_adoption_refuses_independent_source_or_missing_identity(release_fixture, bad):
    f = release_fixture
    if bad == "owner-commit":
        (f["repo"] / "unreviewed-source.txt").write_text("Independent owner source\n")
        f["git"](f["repo"], "add", ".")
        f["git"](f["repo"], "commit", "-m", "Independent owner change")
    if bad != "missing-tag":
        assert publish(f, github_release=False).returncode == 0
    if bad == "remote-advance":
        advance_remote(f)
    if bad == "wrong-trigger":
        f["env"]["GITHUB_SHA"] = "0" * 40
    f["git"](f["repo"], "checkout", "--detach", f["old"])
    result = release_check(f)
    assert result.returncode != 0
    assert f["git"](f["repo"], "rev-parse", "HEAD").stdout.strip() == f["old"]
    assert not f["gh_called"].exists()
    assert not f["output"].exists()


@pytest.mark.parametrize("bad", ["author", "message", "mode", "source", "merge"])
def test_retry_adoption_requires_exact_two_generated_metadata_commits(release_fixture, bad):
    f = release_fixture
    f["git"](f["repo"], "checkout", "-b", "invalid-chain", f["old"])
    if bad == "author":
        f["git"](f["repo"], "config", "user.name", "Independent owner")
    (f["repo"] / "version.txt").write_text(VERSION + "\n")
    if bad == "mode":
        (f["repo"] / "version.txt").chmod(0o755)
    if bad == "source":
        (f["repo"] / "other-source.txt").write_text("Not a generated release artifact\n")
    f["git"](f["repo"], "add", ".")
    message = "Owner metadata update" if bad == "message" else f"chore: release {TAG} [skip ci]"
    f["git"](f["repo"], "commit", "-m", message)
    if bad == "merge":
        f["git"](f["repo"], "merge", "--no-ff", "-m", "Unexpected merge", f["new"])
    else:
        (f["repo"] / "CHANGELOG.md").write_text("# Release " + TAG + "\n")
        f["git"](f["repo"], "add", ".")
        f["git"](f["repo"], "commit", "-m", f"docs: update changelog for {TAG} [skip ci]")
    assert publish(f, github_release=False).returncode == 0
    f["git"](f["repo"], "checkout", "--detach", f["old"])
    result = release_check(f)
    assert result.returncode != 0
    assert f["git"](f["repo"], "rev-parse", "HEAD").stdout.strip() == f["old"]
    assert not f["output"].exists()


def test_resume_dry_run_cannot_create_refs_release_or_deployment_outputs():
    source = RELEASE.read_text()
    for name in ("Create tag and push", "Create GitHub Release"):
        block = source.split(f"      - name: {name}\n", 1)[1].split("        run: |", 1)[0]
        expression = re.search(r"(?m)^        if: (.+)$", block)[1]
        for dry_run in ("true", "false"):
            allowed = condition_matches(
                expression,
                {
                    "steps.check.outputs.needed": "false",
                    "steps.check.outputs.resume": "true",
                    "github.event.inputs.dry_run": dry_run,
                },
            )
            assert allowed is (name == "Create GitHub Release" and dry_run == "false")
    assert (
        "if: steps.check.outputs.needed == 'true'"
        in source.split("      - name: Decide bump", 1)[1]
    )


def test_zero_exit_without_created_github_release_never_emits_deployment_output(release_fixture):
    f = release_fixture
    f["env"]["GH_FIXTURE_CREATE_MISSING"] = "1"
    result = publish(f)
    assert result.returncode != 0
    assert f["gh_called"].exists()
    assert remote_revision(f, "refs/heads/master").stdout.strip() == f["new"]
    assert remote_revision(f, f"refs/tags/{TAG}^{{commit}}").stdout.strip() == f["new"]
    assert_no_published_output(f)


def test_changed_release_payload_after_create_fails_before_deployment(release_fixture):
    f = release_fixture
    f["env"].update(
        GH_FIXTURE_API_STATUS="200",
        GH_FIXTURE_API_EXIT="0",
        GH_FIXTURE_API_BODY='{"tag_name":"v9.9.9","draft":false,"prerelease":false}',
    )
    assert publish(f).returncode != 0
    assert f["gh_called"].exists()
    assert_no_published_output(f)
