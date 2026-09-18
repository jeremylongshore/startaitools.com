"""Committed-source handoff tests; no production lease, provider or state writes."""

import importlib.util
import json
import os
import shutil
import sqlite3
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
METH = ".claude/skills/blog-backfill/methodology"
SPEC = importlib.util.spec_from_file_location(
    "published_index", ROOT / "scripts/blog/blog-methodology-published-index.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE)


def classifier(slug):
    return {
        "date": "2026-09-15",
        "slug": slug,
        "tier": 1,
        "tier_name": "Field Note",
        "confidence": 0.8,
    }


@pytest.fixture
def published(tmp_path):
    primary = tmp_path / "primary"
    primary.mkdir()
    git(primary, "init", "-b", "master")
    git(primary, "config", "user.name", "Fixture")
    git(primary, "config", "user.email", "fixture@example.invalid")
    sources = primary / METH
    sources.mkdir(parents=True)
    (sources / "decisions.jsonl").write_text(json.dumps(classifier("first-post")) + "\n")
    for name in ("feedback.jsonl", "patterns.jsonl"):
        (sources / name).write_text("")
    (sources / "legacy-index-migration-v2.json").write_text(
        json.dumps({"schema_version": 2, "entries": []})
    )
    shutil.copyfile(ROOT / METH / "rebuild-index.sql", sources / "rebuild-index.sql")
    git(primary, "add", ".claude")
    git(primary, "commit", "-m", "fixture baseline")
    initial = git(primary, "rev-parse", "HEAD").decode().strip()
    remote = tmp_path / "remote.git"
    subprocess.run(
        ["git", "clone", "--bare", str(primary), str(remote)], check=True, capture_output=True
    )
    git(primary, "remote", "add", "origin", str(remote))
    git(primary, "fetch", "origin")
    isolated = tmp_path / "isolated"
    git(primary, "worktree", "add", "-b", "run-fixture", str(isolated))
    with (isolated / METH / "decisions.jsonl").open("a") as stream:
        stream.write(json.dumps(classifier("second-post")) + "\n")
    git(isolated, "add", METH + "/decisions.jsonl")
    git(isolated, "commit", "-m", "fixture independently published source")
    git(isolated, "push", "origin", "HEAD:refs/heads/master")
    output = sources / "index.db"
    MODULE.rebuild(primary, output, str(remote))
    # Seed an old one-record canonical index to reproduce the old daily path.
    spec = importlib.util.spec_from_file_location(
        "fixture_index", ROOT / METH / "../scripts/rebuild-methodology-index.py"
    )
    index = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(index)
    index.build(sources, primary, output)
    return primary, isolated, remote, output, initial


def counts(output):
    with sqlite3.connect(output) as db:
        return db.execute("SELECT count(*) FROM decisions").fetchone()[0]


def test_published_sources_ignore_old_head_and_dirty_owner_files(published):
    primary, _, remote, output, head = published
    decisions = primary / METH / "decisions.jsonl"
    decisions.write_text("{unrelated owner edit\n")
    before = decisions.read_bytes()
    worktrees = git(primary, "worktree", "list", "--porcelain")
    result = MODULE.rebuild(primary, output, str(remote))
    assert result["classifications"] == counts(output) == 2
    assert git(primary, "rev-parse", "HEAD").decode().strip() == head
    assert decisions.read_bytes() == before
    assert git(primary, "worktree", "list", "--porcelain") == worktrees
    assert result["source_commit"] != head


def test_unpublished_failed_candidate_cannot_enter_canonical_index(published):
    primary, isolated, remote, output, _ = published
    with (isolated / METH / "decisions.jsonl").open("a") as stream:
        stream.write(json.dumps(classifier("unpublished-candidate")) + "\n")
    git(isolated, "add", METH + "/decisions.jsonl")
    git(isolated, "commit", "-m", "fixture never published")
    result = MODULE.rebuild(primary, output, str(remote))
    assert result["classifications"] == counts(output) == 2
    assert result["source_commit"] != git(isolated, "rev-parse", "HEAD").decode().strip()


def test_repeat_snapshot_idempotent_and_source_provenance(published):
    primary, isolated, remote, output, _ = published
    first = MODULE.rebuild(primary, output, str(remote))
    assert MODULE.rebuild(primary, output, str(remote)) == first
    with sqlite3.connect(output) as db:
        commit = db.execute(
            "SELECT value FROM index_metadata WHERE key='content_commit'"
        ).fetchone()[0]
        assert commit == git(isolated, "rev-parse", "HEAD").decode().strip()
        assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []


def test_wrong_approved_remote_keeps_last_good(published):
    primary, _, _, output, _ = published
    before = output.read_bytes()
    with pytest.raises(ValueError, match="approved remote"):
        MODULE.rebuild(primary, output, "https://example.invalid/wrong.git")
    assert output.read_bytes() == before


def test_canary_entry_refused_before_fetch_or_write(published, monkeypatch):
    primary, _, remote, output, _ = published
    before = output.read_bytes()
    monkeypatch.setenv("BLOG_CANARY", "1")

    def forbidden_fetch(*args):
        pytest.fail("canary reached the authoritative fetch")

    monkeypatch.setattr(MODULE, "authoritative_commit", forbidden_fetch)
    with pytest.raises(ValueError, match="canary execution"):
        MODULE.rebuild(primary, output, str(remote))
    assert output.read_bytes() == before


def test_unrelated_output_refused_before_any_write(published, tmp_path):
    primary, _, remote, output, _ = published
    unrelated = tmp_path / "owner-file"
    unrelated.write_text("preserve me")
    with pytest.raises(ValueError, match="canonical methodology"):
        MODULE.rebuild(primary, unrelated, str(remote))
    assert unrelated.read_text() == "preserve me"
    assert counts(output) == 1


def test_symlinked_canonical_output_refused(published, tmp_path):
    primary, _, remote, output, _ = published
    saved = tmp_path / "saved.db"
    output.rename(saved)
    output.symlink_to(saved)
    before = saved.read_bytes()
    with pytest.raises(ValueError, match="symlinked"):
        MODULE.rebuild(primary, output, str(remote))
    assert saved.read_bytes() == before


def test_symlinked_committed_source_refused_without_index_loss(published):
    primary, isolated, remote, output, _ = published
    source = isolated / METH / "patterns.jsonl"
    source.unlink()
    source.symlink_to("decisions.jsonl")
    git(isolated, "add", METH + "/patterns.jsonl")
    git(isolated, "commit", "-m", "fixture invalid symlinked source")
    git(isolated, "push", "origin", "HEAD:refs/heads/master")
    before = output.read_bytes()
    worktrees = git(primary, "worktree", "list", "--porcelain")
    with pytest.raises(ValueError, match="regular committed blob"):
        MODULE.rebuild(primary, output, str(remote))
    assert output.read_bytes() == before
    assert git(primary, "worktree", "list", "--porcelain") == worktrees


def test_cli_without_inherited_lease_cannot_publish(published):
    primary, _, remote, output, _ = published
    before = output.read_bytes()
    result = subprocess.run(
        [
            "python3",
            str(ROOT / "scripts/blog/blog-methodology-published-index.py"),
            "--repo",
            str(primary),
            "--output",
            str(output),
            "--expected-remote",
            str(remote),
        ],
        capture_output=True,
        text=True,
        close_fds=True,
    )
    assert result.returncode == 1
    assert "canonical FD9 lock" in result.stderr
    assert output.read_bytes() == before


def test_malformed_committed_record_keeps_last_good_and_cleans_snapshot(published):
    primary, isolated, remote, output, _ = published
    before = output.read_bytes()
    with (isolated / METH / "decisions.jsonl").open("a") as stream:
        stream.write("{broken\n")
    git(isolated, "add", METH + "/decisions.jsonl")
    git(isolated, "commit", "-m", "fixture malformed authoritative source")
    git(isolated, "push", "origin", "HEAD:refs/heads/master")
    worktrees = git(primary, "worktree", "list", "--porcelain")
    with pytest.raises(ValueError):
        MODULE.rebuild(primary, output, str(remote))
    assert output.read_bytes() == before
    assert git(primary, "worktree", "list", "--porcelain") == worktrees


def test_actual_daily_rebuild_updates_canonical_after_isolated_publication(published, tmp_path):
    primary, isolated, remote, output, head = published
    scripts = primary / "scripts/blog"
    scripts.mkdir(parents=True)
    for name in ("blog-methodology-published-index.py", "blog-run-workspace.py"):
        shutil.copyfile(ROOT / "scripts/blog" / name, scripts / name)
    # Only this disposable runtime substitutes its own lease inode. Never touch
    # /tmp/blog-pipeline.lock, which may belong to a real production recovery.
    lease = tmp_path / "fixture-pipeline.lock"
    helper = scripts / "blog-run-workspace.py"
    helper.write_text(
        helper.read_text().replace('Path("/tmp/blog-pipeline.lock")', f"Path({str(lease)!r})")
    )
    for repo in (primary, isolated):
        destination = repo / METH / "../scripts"
        destination.mkdir(exist_ok=True)
        for name in ("rebuild-methodology-index.py", "rebuild-methodology-index.sh"):
            shutil.copyfile(ROOT / METH / "../scripts" / name, destination / name)
        (destination / "rebuild-methodology-index.sh").chmod(0o700)
    wrapper = (ROOT / "scripts/blog/blog-backfill-daily.sh").read_text()
    start = wrapper.index("\nREBUILD=")
    end = wrapper.index('\nif [ "${BLOG_CANARY:-0}" = "1" ]; then\n  log "CANARY-RESULT', start)
    block = tmp_path / "actual-rebuild-block.sh"
    block.write_text(
        'set -euo pipefail\nexec 9>"$TEST_LEASE"\nflock -n 9\nlog() { echo "$*"; }\n'
        + "rebuild_canonical_index() {"
        + wrapper.split("rebuild_canonical_index() {", 1)[1].split("\nPUBLICATION_HELPER=", 1)[0]
        + "\n"
        + wrapper[start:end]
        + '\n[ "$STATUS" = OK ]\n'
    )
    env = dict(
        os.environ,
        TEST_LEASE=str(lease),
        BLOG_SOURCE_DIR=str(primary),
        BLOG_DIR=str(isolated),
        SELF=str(scripts / "blog-backfill-daily.sh"),
        BLOG_EXPECTED_REMOTE=str(remote),
        BLOG_CANARY="0",
        STATUS="OK",
        LOG=str(tmp_path / "index.log"),
    )
    result = subprocess.run(["bash", str(block)], env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr + result.stdout
    assert counts(output) == 2
    assert git(primary, "rev-parse", "HEAD").decode().strip() == head
