"""Offline ownership/restart fixtures; no production content or Git state is changed."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

HELPER = Path(__file__).resolve().parents[1] / "scripts/blog/blog-run-workspace.py"
DECISIONS = ".claude/skills/blog-backfill/methodology/decisions.jsonl"
DATE = "2026-09-16"
SLUG = "owned-fixture-post"
POST = f"content/posts/{SLUG}.md"


def command(*args, cwd=None):
    env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
    return subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, check=False)


def git(repo, *args):
    result = command("git", "-C", str(repo), *args)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


@pytest.fixture
def repository(tmp_path):
    remote = tmp_path / "remote.git"
    owner = tmp_path / "owner"
    git(tmp_path, "init", "--bare", "--initial-branch=master", str(remote))
    git(tmp_path, "clone", str(remote), str(owner))
    git(owner, "config", "user.email", "fixture@example.invalid")
    git(owner, "config", "user.name", "Offline fixture")
    (owner / "content/posts").mkdir(parents=True)
    (owner / "content/posts/old-fixture.md").write_text(
        "+++\ndate = 2026-09-01T08:00:00-06:00\n+++\nHistorical offline fixture.\n"
    )
    (owner / "layouts/partials").mkdir(parents=True)
    (owner / "layouts/partials/schema.html").write_text("committed schema\n")
    (owner / DECISIONS).parent.mkdir(parents=True)
    (owner / DECISIONS).write_text('{"date":"2026-09-01","slug":"old-fixture"}\n')
    (owner / ".gitignore").write_text(".blog-staging/\npublic/\nresources/\n.hugo_build.lock\n")
    git(owner, "add", ".")
    git(owner, "commit", "-m", "fixture baseline")
    git(owner, "push", "origin", "master")
    git(owner, "remote", "set-head", "origin", "master")
    return owner, remote, tmp_path / "state"


def create(repository, *, run_id="offline-run", date=DATE, success=True):
    owner, remote, state = repository
    result = command(sys.executable, str(HELPER), "create", "--repo", str(owner),
                     "--expected-remote", str(remote), "--date", date, "--run-id", run_id,
                     "--state-dir", str(state))
    if success:
        assert result.returncode == 0, result.stderr
        return json.loads(result.stdout)
    assert result.returncode != 0, result.stdout
    return result.stderr


def action(run, name, *args, success=True):
    result = command(sys.executable, str(HELPER), name, "--manifest", run["manifest"], *args)
    if success:
        assert result.returncode == 0, result.stderr
        return json.loads(result.stdout)
    assert result.returncode != 0, result.stdout
    return result.stderr


def produce(run, *, date=DATE, slug=SLUG):
    workspace = Path(run["workspace"])
    (workspace / f"content/posts/{slug}.md").write_text(
        f"+++\ntitle = 'Offline workspace fixture'\nslug = '{slug}'\n"
        f"date = {date}T08:00:00-06:00\ndraft = false\n+++\n\nFixture body.\n"
    )
    with (workspace / DECISIONS).open("a") as stream:
        stream.write(json.dumps({"date": date, "slug": slug, "tier": 1}) + "\n")
    staging = workspace / f".blog-staging/{date}.intent.json"
    staging.parent.mkdir(exist_ok=True)
    staging.write_text(json.dumps({"ready": False, "fixture": True, "date": date,
                                   "run_id": run["run_id"]}) + "\n")
    return workspace


def test_dirty_owner_and_untracked_preexisting_files_remain_byte_identical(repository):
    owner, _, _ = repository
    schema = owner / "layouts/partials/schema.html"
    schema.write_text("owner's uncommitted schema edit\n")
    git(owner, "add", "layouts/partials/schema.html")
    schema.write_text("owner's newer unstaged schema edit\n")
    old_post = owner / "content/posts/unrelated-august-14.md"
    old_post.write_text("unrelated owner post\n")
    drafts = owner / "drafts"
    drafts.mkdir()
    (drafts / "owner.md").write_text("unfinished owner draft\n")
    before_status = git(owner, "status", "--porcelain=v1")
    before_index = git(owner, "diff", "--cached")
    before_head = git(owner, "rev-parse", "HEAD")
    run = create(repository)
    workspace = produce(run)
    validated = action(run, "validate")
    assert validated["publish_paths"] == [POST, DECISIONS]
    action(run, "quarantine", "--reason", "offline failed-gate fixture")
    assert git(owner, "status", "--porcelain=v1") == before_status
    assert git(owner, "diff", "--cached") == before_index
    assert git(owner, "rev-parse", "HEAD") == before_head
    assert schema.read_text() == "owner's newer unstaged schema edit\n"
    assert old_post.read_text() == "unrelated owner post\n"
    assert (drafts / "owner.md").read_text() == "unfinished owner draft\n"
    assert (workspace / POST).exists(), "quarantine retains original workspace evidence"


def test_remote_master_is_baseline_even_when_owner_has_local_commits(repository):
    owner, _, _ = repository
    expected = git(owner, "rev-parse", "origin/master")
    (owner / "owner-only.txt").write_text("local only\n")
    git(owner, "add", "owner-only.txt")
    git(owner, "commit", "-m", "owner local commit")
    run = create(repository)
    assert run["baseline_sha"] == expected
    assert not (Path(run["workspace"]) / "owner-only.txt").exists()
    assert git(owner, "rev-parse", "HEAD") != expected


def test_repeat_resumes_same_workspace_and_manifest_after_partial_work(repository):
    run = create(repository)
    workspace = produce(run)
    repeated = create(repository)
    assert repeated["workspace"] == run["workspace"]
    assert (workspace / POST).exists()
    assert action(repeated, "validate")["post"] == POST


def test_crash_after_worktree_creation_recovers_from_creating_manifest(repository):
    run = create(repository)
    manifest_path = Path(run["manifest"])
    manifest = json.loads(manifest_path.read_text())
    manifest["status"] = "creating"
    manifest_path.write_text(json.dumps(manifest))
    assert create(repository)["status"] == "ready"


@pytest.mark.parametrize("other_date", [DATE, "2026-09-15"])
def test_overlapping_runs_refuse_until_previous_run_quarantined(repository, other_date):
    run = create(repository)
    assert "unfinished run" in create(repository, run_id="overlap", date=other_date, success=False)
    action(run, "quarantine", "--reason", "abandoned fixture recovered")
    assert create(repository, run_id="overlap", date=other_date)["status"] == "ready"


@pytest.mark.parametrize("date,run_id", [
    ("../../outside", "run"), ("2026-02-30", "run"), (DATE, "../escape"),
    (DATE, "run/name"), (DATE, ""),
])
def test_identifier_escape_rejected_before_workspace_creation(repository, date, run_id):
    create(repository, date=date, run_id=run_id, success=False)
    assert not repository[2].exists()


def test_state_inside_owner_checkout_is_rejected(repository):
    owner, remote, _ = repository
    error = create((owner, remote, owner / "run-state"), success=False)
    assert "outside the owner checkout" in error
    assert not (owner / "run-state").exists()


def test_wrong_remote_and_wrong_default_branch_are_rejected(repository):
    owner, remote, state = repository
    assert "approved remote" in create((owner, remote.parent / "wrong.git", state), success=False)
    git(remote, "symbolic-ref", "HEAD", "refs/heads/main")
    assert "default branch must be master" in create(repository, success=False)


def test_tracked_change_outside_write_set_refuses_without_cleanup(repository):
    run = create(repository)
    workspace = produce(run)
    schema = workspace / "layouts/partials/schema.html"
    schema.write_text("unexpected producer edit\n")
    assert "outside run write-set" in action(run, "validate", success=False)
    action(run, "quarantine", "--reason", "unexpected producer scope")
    assert schema.read_text() == "unexpected producer edit\n"


def test_wrong_date_and_duplicate_posts_cannot_land(repository):
    run = create(repository)
    workspace = produce(run, date="2026-09-15")
    assert "post date differs" in action(run, "validate", success=False)
    (workspace / "content/posts/second-post.md").write_text("partial second post\n")
    assert "exactly one" in action(run, "validate", success=False)


@pytest.mark.parametrize("mutation", ["rewrite", "other-date", "other-slug", "truncated"])
def test_decisions_are_append_only_and_scoped(repository, mutation):
    run = create(repository)
    workspace = produce(run)
    decisions = workspace / DECISIONS
    if mutation == "rewrite":
        decisions.write_text(decisions.read_text().replace("old-fixture", "rewritten"))
    elif mutation in {"other-date", "other-slug"}:
        with decisions.open("a") as stream:
            record = {"date": DATE if mutation == "other-slug" else "2026-09-15",
                      "slug": SLUG if mutation == "other-date" else "another"}
            stream.write(json.dumps(record) + "\n")
    else:
        decisions.write_text(decisions.read_text().rstrip("\n"))
    action(run, "validate", success=False)
    assert decisions.exists(), "validation never restores decisions"


def test_post_symlink_escape_is_refused_without_reading_or_altering_target(repository):
    run = create(repository)
    workspace = produce(run)
    external = repository[0].parent / "external.txt"
    external.write_text("external owner's data\n")
    post = workspace / POST
    post.unlink()
    post.symlink_to(external)
    assert "symlink" in action(run, "validate", success=False)
    receipt = action(run, "quarantine", "--reason", "unsafe fixture symlink")
    assert receipt["skipped_unsafe_artifacts"] == [POST]
    assert not (Path(receipt["quarantine"]) / "posts" / f"{SLUG}.md").exists()
    assert external.read_text() == "external owner's data\n"


def test_manifest_cannot_redirect_workspace_to_owner(repository):
    run = create(repository)
    manifest_path = Path(run["manifest"])
    manifest = json.loads(manifest_path.read_text())
    manifest["workspace"] = str(repository[0])
    manifest_path.write_text(json.dumps(manifest))
    assert "escaped" in action(run, "validate", success=False)


def test_quarantine_is_idempotent_and_keeps_workspace_manifest_and_log(repository):
    run = create(repository)
    workspace = produce(run)
    first = action(run, "quarantine", "--reason", "offline fixture failure")
    repeated = action(run, "quarantine", "--reason", "repeat")
    assert first == repeated
    snapshot = Path(first["quarantine"])
    assert (snapshot / "posts" / f"{SLUG}.md").read_bytes() == (workspace / POST).read_bytes()
    assert (snapshot / "decisions.diff").read_text()
    assert Path(run["manifest"]).exists()
    assert (Path(run["manifest"]).parent / "run.log").exists()
    assert "terminal run retained" in create(repository, success=False)


def test_hugo_ignored_outputs_are_runtime_only_never_publish_paths(repository):
    run = create(repository)
    workspace = produce(run)
    (workspace / "public").mkdir()
    (workspace / "public/index.html").write_text("offline build output\n")
    validated = action(run, "validate")
    assert validated["runtime_artifacts"] == ["public/index.html"]
    assert validated["publish_paths"] == [POST, DECISIONS]


def test_committed_ff_candidate_and_publication_receipt_are_workspace_only(repository):
    run = create(repository)
    workspace = produce(run)
    action(run, "validate")
    git(workspace, "add", POST, DECISIONS)
    git(workspace, "commit", "-m", "offline owned publication fixture")
    assert "changed Git HEAD" in action(run, "validate", success=False)
    checked = action(run, "publication-check")
    assert checked["push_refspec"] == "HEAD:refs/heads/master"
    assert "not published" in action(run, "complete", success=False)
    owner_head = git(repository[0], "rev-parse", "HEAD")
    git(workspace, "push", "origin", checked["push_refspec"])
    receipt = action(run, "complete")
    assert receipt["status"] == "published"
    assert git(repository[0], "rev-parse", "HEAD") == owner_head
    assert workspace.exists()


def test_remote_advancement_blocks_publication_instead_of_rebase_or_owner_pull(repository):
    run = create(repository)
    workspace = produce(run)
    git(workspace, "add", POST, DECISIONS)
    git(workspace, "commit", "-m", "offline run commit")
    owner = repository[0]
    (owner / "release-fixture.txt").write_text("remote release advancement\n")
    git(owner, "add", "release-fixture.txt")
    git(owner, "commit", "-m", "offline remote movement")
    git(owner, "push", "origin", "master")
    head = git(workspace, "rev-parse", "HEAD")
    assert "moved or diverged" in action(run, "publication-check", success=False)
    assert git(workspace, "rev-parse", "HEAD") == head


def recover(repository, *, run_id="recovered-run", hold=True):
    owner, remote, state = repository
    lock = state / "offline-canonical.lock"
    script = (
        "import importlib.util,os,fcntl,sys; "
        f"s=importlib.util.spec_from_file_location('workspace',{str(HELPER)!r}); "
        "m=importlib.util.module_from_spec(s);s.loader.exec_module(m); "
        f"m.PIPELINE_LOCK=m.Path({str(lock)!r}); "
        f"f=os.open({str(lock)!r},os.O_CREAT|os.O_WRONLY,0o600);os.dup2(f,9); "
        + ("fcntl.flock(9,fcntl.LOCK_EX); " if hold else "")
        + "sys.exit(m.main())"
    )
    return command(sys.executable, "-c", script, "create", "--repo", str(owner),
                   "--expected-remote", str(remote), "--date", DATE, "--run-id", run_id,
                   "--state-dir", str(state), "--recover-abandoned")


def test_abandoned_recovery_requires_a_real_already_held_canonical_fd9(repository):
    run = create(repository)
    workspace = produce(run)
    rejected = recover(repository, hold=False)
    assert rejected.returncode != 0
    assert "not already held" in rejected.stderr
    recovered = recover(repository)
    assert recovered.returncode == 0, recovered.stderr
    assert json.loads(Path(run["manifest"]).read_text())["status"] == "quarantined"
    assert (workspace / POST).exists()


def test_committed_unpublished_run_survives_auto_recovery_and_blocks_visibly(repository):
    run = create(repository)
    workspace = produce(run)
    git(workspace, "add", POST, DECISIONS)
    git(workspace, "commit", "-m", "offline pending publication")
    head = git(workspace, "rev-parse", "HEAD")
    result = recover(repository)
    assert result.returncode != 0
    assert "publication reconciliation" in result.stderr
    assert json.loads(Path(run["manifest"]).read_text())["status"] == "pending_publication"
    assert git(workspace, "rev-parse", "HEAD") == head


def test_committed_published_crash_is_reconciled_before_new_run(repository):
    run = create(repository)
    workspace = produce(run)
    git(workspace, "add", POST, DECISIONS)
    git(workspace, "commit", "-m", "offline publication before crash")
    git(workspace, "push", "origin", "HEAD:refs/heads/master")
    result = recover(repository)
    assert result.returncode == 0, result.stderr
    assert json.loads(Path(run["manifest"]).read_text())["status"] == "published"
    assert workspace.exists()


def test_existing_published_target_closes_noop_without_new_post(repository):
    run = create(repository, date="2026-09-01")
    receipt = action(run, "complete-noop")
    assert receipt["status"] == "noop"
    assert receipt["existing_posts"] == ["content/posts/old-fixture.md"]


def test_noop_cannot_hide_a_missing_target_or_producer_change(repository):
    run = create(repository)
    assert "existing target-date" in action(run, "complete-noop", success=False)
    produce(run)
    assert "producer changes" in action(run, "complete-noop", success=False)


def test_staging_scope_and_sentinel_identity_are_enforced(repository):
    run = create(repository)
    workspace = produce(run)
    stage = workspace / ".blog-staging"
    owned = stage / f"{DATE}.{run['run_id']}.classifier.json"
    owned.write_text('{"fixture":"classifier"}\n')
    assert action(run, "validate")["publish_paths"] == [POST, DECISIONS]
    other = stage / f"{DATE}.another-run.audit.json"
    other.write_text('{}\n')
    assert "outside run write-set" in action(run, "validate", success=False)
    other.unlink()
    sentinel = stage / f"{DATE}.intent.json"
    sentinel.write_text(json.dumps({"date": DATE, "run_id": "another-run"}))
    assert "another run or date" in action(run, "validate", success=False)


def test_feedback_append_requires_owned_slug_run_and_preserved_prefix(repository):
    run = create(repository)
    workspace = produce(run)
    feedback = workspace / ".claude/skills/blog-backfill/methodology/feedback.jsonl"
    record = {"slug": SLUG, "run_id": run["run_id"], "date_assessed": "2026-09-17"}
    feedback.write_text(json.dumps(record) + "\n")
    assert (action(run, "validate")["publish_paths"][-1]
            == feedback.relative_to(workspace).as_posix())
    record["run_id"] = "someone-else"
    feedback.write_text(json.dumps(record) + "\n")
    assert "another slug or run" in action(run, "validate", success=False)


def test_producer_runner_preserves_actual_exit_and_appends_logs(repository):
    run = create(repository)
    result = command(sys.executable, str(HELPER), "run", "--manifest", run["manifest"],
                     "--", sys.executable, "-c", "print('offline real execution');exit(7)")
    assert result.returncode == 7
    assert "offline real execution" in Path(run["producer_log"]).read_text()
    action(run, "run", "--", sys.executable, "-c", "print('second execution')")
    assert "offline real execution" in Path(run["producer_log"]).read_text()
    assert "second execution" in Path(run["producer_log"]).read_text()


def test_live_producer_blocks_repeat_and_quarantine(repository):
    run = create(repository)
    started = Path(run["manifest"]).parent / "started-fixture"
    code = f"from pathlib import Path;import time;Path({str(started)!r}).touch();time.sleep(2)"
    env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
    proc = subprocess.Popen([sys.executable, str(HELPER), "run", "--manifest", run["manifest"],
                             "--", sys.executable, "-c", code], env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        deadline = time.monotonic() + 3
        while not started.exists() and time.monotonic() < deadline:
            time.sleep(.02)
        assert started.exists()
        assert "still running" in action(run, "quarantine", "--reason", "race", success=False)
        assert "still running" in action(run, "run", "--", sys.executable, "-c", "pass",
                                         success=False)
    finally:
        proc.communicate(timeout=5)


def bootstrap_runtime_fixture(repository):
    owner, _, _ = repository
    beads = owner / ".beads"
    beads.mkdir()
    (beads / ".gitignore").write_text(
        "backup/\nembeddeddolt/\nexport-state.json\nunknown/\n"
    )
    (beads / "config.yaml").write_text("fixture_authority: unchanged\n")
    with (owner / ".gitignore").open("a") as stream:
        stream.write(".claude/skills/blog-backfill/methodology/index.db.rebuild.lock\n")
    git(owner, "add", ".beads/.gitignore", ".beads/config.yaml", ".gitignore")
    git(owner, "commit", "-m", "fixture: known bootstrap runtime exclusions")
    git(owner, "push", "origin", "master")


def test_known_ignored_beads_bootstrap_and_index_lock_are_nonpublic_runtime(repository):
    bootstrap_runtime_fixture(repository)
    run = create(repository)
    workspace = produce(run)
    runtime = [
        ".beads/backup/manifest",
        ".beads/embeddeddolt/startaitools/.dolt/config.json",
        ".beads/export-state.json",
        ".claude/skills/blog-backfill/methodology/index.db.rebuild.lock",
    ]
    for relative in runtime:
        path = workspace / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("offline bootstrap runtime fixture\n")
    result = action(run, "validate")
    assert result["publish_paths"] == [POST, DECISIONS]
    assert set(runtime) <= set(result["runtime_artifacts"])


@pytest.mark.parametrize("relative", [".beads/config.yaml", ".beads/unknown/authority.json"])
def test_beads_authority_or_unknown_ignored_files_still_fail_write_set(repository, relative):
    bootstrap_runtime_fixture(repository)
    run = create(repository)
    workspace = produce(run)
    path = workspace / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("unexpected authority mutation\n")
    assert "write-set" in action(run, "validate", success=False)
