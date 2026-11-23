"""The cron checkout updates itself, and a checkout that does not is reported.

blog-checkout-sync.sh fast-forwards the checkout host cron runs the blog jobs
from; host-drift-check.py is the backstop that reports one left behind. Hermetic:
temp repos, a stub HOME and a stub alert runtime. No real checkout is touched.
"""

import importlib.util
import os
import subprocess
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SYNC = ROOT / "scripts/blog/blog-checkout-sync.sh"
SPEC = importlib.util.spec_from_file_location(
    "host_drift_for_sync", ROOT / "scripts/blog/host-drift-check.py")
drift = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(drift)

GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@example.invalid",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@example.invalid",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
}


def git(cwd, *args, env=None):
    return subprocess.run(["git", "-C", str(cwd), *args], env={**GIT_ENV, **(env or {})},
                          check=True, capture_output=True, text=True).stdout.strip()


@pytest.fixture
def host(tmp_path):
    """A bare origin, the cron checkout, and a second clone that merges work."""
    bare = tmp_path / "origin.git"
    git(tmp_path, "init", "-q", "--bare", "--initial-branch=master", str(bare))
    cron = tmp_path / "cron"
    git(tmp_path, "clone", "-q", str(bare), str(cron))
    (cron / "scripts/blog").mkdir(parents=True)
    (cron / "scripts/blog/job.sh").write_text("echo v1\n")
    (cron / "notes.md").write_text("notes\n")
    git(cron, "add", ".")
    git(cron, "commit", "-qm", "seed")
    git(cron, "push", "-q", "origin", "HEAD:master")
    dev = tmp_path / "dev"
    git(tmp_path, "clone", "-q", str(bare), str(dev))
    return bare, cron, dev


def merge_upstream(dev, path="scripts/blog/job.sh", text="echo v2\n", when=None):
    (dev / path).write_text(text)
    git(dev, "add", ".")
    env = {"GIT_COMMITTER_DATE": f"@{int(when)} +0000"} if when else None
    git(dev, "commit", "-qm", f"change {path}", env=env)
    git(dev, "push", "-q", "origin", "HEAD:master")


def sync(tmp_path, cron, lock=None):
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    alerts = tmp_path / "alerts.log"
    runtime = tmp_path / "runtime.sh"
    runtime.write_text(f'cron_fail() {{ printf "%s|%s\\n" "$1" "$2" >> "{alerts}"; }}\n')
    proc = subprocess.run(
        ["bash", str(SYNC)],
        env={**GIT_ENV, "HOME": str(home), "INTENT_RUNTIME": str(runtime),
             "BLOG_CHECKOUT_SYNC_REPO": str(cron),
             "BLOG_PIPELINE_LOCK": str(lock or tmp_path / "pipeline.lock")},
        capture_output=True, text=True, timeout=120)
    ok = (home / ".local/state/intent-os/liveness/blog-checkout-sync.ok").exists()
    return proc, ok, alerts.read_text() if alerts.exists() else ""


def test_a_merged_script_change_reaches_the_cron_checkout(host, tmp_path):
    _, cron, dev = host
    merge_upstream(dev)
    proc, ok, alerts = sync(tmp_path, cron)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (cron / "scripts/blog/job.sh").read_text() == "echo v2\n"
    assert "UPDATED" in proc.stdout and "1 pipeline file(s) changed" in proc.stdout
    assert ok and alerts == ""


def test_an_already_current_checkout_is_a_quiet_success(host, tmp_path):
    _, cron, _ = host
    proc, ok, alerts = sync(tmp_path, cron)
    assert proc.returncode == 0 and "CURRENT" in proc.stdout
    assert ok and alerts == ""


def test_unrelated_uncommitted_work_survives_the_update(host, tmp_path):
    _, cron, dev = host
    (cron / "notes.md").write_text("someone's unsaved edit\n")
    (cron / "untracked.md").write_text("draft\n")
    merge_upstream(dev)
    proc, ok, _ = sync(tmp_path, cron)
    assert proc.returncode == 0, proc.stdout
    assert (cron / "scripts/blog/job.sh").read_text() == "echo v2\n"
    assert (cron / "notes.md").read_text() == "someone's unsaved edit\n"
    assert (cron / "untracked.md").read_text() == "draft\n"
    assert ok


def test_an_update_that_would_overwrite_a_local_edit_is_refused_and_alerted(host, tmp_path):
    _, cron, dev = host
    (cron / "scripts/blog/job.sh").write_text("echo local hotfix\n")
    merge_upstream(dev)
    before = git(cron, "rev-parse", "HEAD")
    proc, ok, alerts = sync(tmp_path, cron)
    assert proc.returncode == 1
    assert git(cron, "rev-parse", "HEAD") == before
    assert (cron / "scripts/blog/job.sh").read_text() == "echo local hotfix\n"
    assert "blog-checkout-sync|" in alerts and "NOT updated" in alerts
    assert not ok


def test_local_commits_origin_lacks_are_refused_not_rebased(host, tmp_path):
    _, cron, dev = host
    (cron / "notes.md").write_text("committed here only\n")
    git(cron, "commit", "-qam", "local only")
    local = git(cron, "rev-parse", "HEAD")
    merge_upstream(dev)
    proc, ok, alerts = sync(tmp_path, cron)
    assert proc.returncode == 1
    assert git(cron, "rev-parse", "HEAD") == local
    assert "1 local commit(s)" in alerts
    assert not ok


def test_a_checkout_on_a_feature_branch_is_refused_and_left_there(host, tmp_path):
    _, cron, dev = host
    git(cron, "checkout", "-q", "-b", "fix/in-progress")
    merge_upstream(dev)
    proc, ok, alerts = sync(tmp_path, cron)
    assert proc.returncode == 1
    assert git(cron, "rev-parse", "--abbrev-ref", "HEAD") == "fix/in-progress"
    assert "never switches branch" in alerts
    assert not ok


def test_scripts_are_not_swapped_under_a_running_pipeline(host, tmp_path):
    _, cron, dev = host
    merge_upstream(dev)
    lock = tmp_path / "pipeline.lock"
    holder = subprocess.Popen(["flock", "-n", str(lock), "sleep", "30"])
    try:
        for _ in range(50):
            if lock.exists():
                break
            time.sleep(0.1)
        time.sleep(0.2)
        proc, ok, alerts = sync(tmp_path, cron, lock=lock)
    finally:
        holder.kill()
        holder.wait()
    assert proc.returncode == 0 and "SKIPPED" in proc.stdout
    assert (cron / "scripts/blog/job.sh").read_text() == "echo v1\n"
    assert alerts == ""


# --------------------------------------------------------------------------- #
# The backstop: host-drift-check.py reports a checkout left behind.
# --------------------------------------------------------------------------- #
def test_drift_check_reports_a_checkout_left_behind_for_days(host):
    _, cron, dev = host
    merge_upstream(dev, when=time.time() - 3 * 86400)
    git(cron, "fetch", "-q", "origin")
    result = drift.check_checkout(cron, stale_hours=36)
    assert result["status"] == "DRIFT" and result["behind"] == 1
    assert result["waiting_hours"] > 36


def test_drift_check_tolerates_a_change_merged_since_the_last_sync(host):
    _, cron, dev = host
    merge_upstream(dev, when=time.time() - 3600)
    git(cron, "fetch", "-q", "origin")
    result = drift.check_checkout(cron, stale_hours=36)
    assert result["status"] == "OK" and result["behind"] == 1


def test_drift_check_skips_a_tree_with_no_origin_ref(tmp_path):
    lone = tmp_path / "lone"
    git(tmp_path, "init", "-q", "--initial-branch=master", str(lone))
    assert drift.check_checkout(lone, stale_hours=36)["status"] == "SKIPPED"
    assert drift.check_checkout(tmp_path / "not-a-repo", stale_hours=36)["status"] == "SKIPPED"


def test_the_sync_job_is_scheduled_before_the_daily_producer():
    lines = drift.manifest_entries()
    sync_line = next(e for e in lines if "blog-checkout-sync.sh" in e)
    producer = next(e for e in lines if "blog-backfill-daily.sh" in e)
    minute, hour = (int(x) for x in sync_line.split()[:2])
    p_minute, p_hour = (int(x) for x in producer.split()[:2])
    assert sync_line.split()[2:5] == ["*", "*", "*"], "the sync must run every day"
    assert (hour, minute) < (p_hour, p_minute)
