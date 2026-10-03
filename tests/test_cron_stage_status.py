"""Truthful cron status: reconcile_repo refusal, calibration period, worker PATH.

Hermetic: temp repos and a stub HOME. Nothing here runs a real cron wrapper body
against real state, sends mail, or alerts.
"""

import os
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts/blog"
LIB = SCRIPTS / "lib-cron-common.sh"

GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@example.invalid",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@example.invalid",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
    "INTENT_RUNTIME": "/nonexistent",
}


def git(cwd, *args):
    return subprocess.run(
        ["git", "-C", str(cwd), *args], env=GIT_ENV, check=True, capture_output=True, text=True
    ).stdout.strip()


def lib(snippet, env=None):
    return subprocess.run(
        ["bash", "-c", f'source "{LIB}"; {snippet}'],
        env={**GIT_ENV, **(env or {})},
        capture_output=True,
        text=True,
    )


# --------------------------------------------------------------------------- #
# reconcile_repo (startaitools-8oc.16)
# --------------------------------------------------------------------------- #
@pytest.fixture
def shared(tmp_path):
    bare = tmp_path / "remote.git"
    git(tmp_path, "init", "-q", "--bare", "--initial-branch=main", str(bare))
    work = tmp_path / "shared"
    git(tmp_path, "clone", "-q", str(bare), str(work))
    (work / "a.md").write_text("a\n")
    git(work, "add", ".")
    git(work, "commit", "-qm", "seed")
    git(work, "push", "-q", "origin", "HEAD:main")
    return bare, work


def reconcile(work, tmp_path, branch="main"):
    log = tmp_path / "reconcile.log"
    proc = lib(
        f'RECONCILED=""; reconcile_repo "{work}" tonsofskills "{log}" {branch}; '
        f'rc=$?; printf "%b" "$RECONCILED"; exit $rc'
    )
    return proc.returncode, proc.stdout, log.read_text() if log.exists() else ""


def test_reconcile_refuses_a_feature_branch_and_pushes_nothing(shared, tmp_path):
    bare, work = shared
    before = git(bare, "rev-parse", "main")
    git(work, "checkout", "-q", "-b", "fix/curated-promotion-cohort-parity")
    (work / "b.md").write_text("someone else's work\n")
    git(work, "add", ".")
    git(work, "commit", "-qm", "wip")
    rc, summary, log = reconcile(work, tmp_path)
    assert rc == 2
    assert "REFUSED" in summary and "REFUSED" in log
    assert git(bare, "rev-parse", "main") == before
    assert git(work, "rev-parse", "--abbrev-ref", "HEAD") == "fix/curated-promotion-cohort-parity"


def test_reconcile_refuses_even_with_default_resolved_automatically(shared, tmp_path):
    bare, work = shared
    git(work, "remote", "set-head", "origin", "main")
    git(work, "checkout", "-q", "-b", "feat/x")
    rc, summary, _ = reconcile(work, tmp_path, branch="")
    assert rc == 2 and "not 'main'" in summary


def test_reconcile_on_default_fast_forwards_unpushed_commits(shared, tmp_path):
    bare, work = shared
    (work / "retro.md").write_text("retro\n")
    git(work, "add", ".")
    git(work, "commit", "-qm", "retro")
    rc, summary, _ = reconcile(work, tmp_path)
    assert rc == 0 and "pushed 1 commit" in summary
    assert git(bare, "rev-parse", "main") == git(work, "rev-parse", "HEAD")
    rc, summary, _ = reconcile(work, tmp_path)
    assert rc == 0 and "nothing unpushed" in summary


def test_reconcile_rejected_fast_forward_is_unpushed_and_never_rebases(shared, tmp_path):
    bare, work = shared
    other = tmp_path / "other"
    git(tmp_path, "clone", "-q", str(bare), str(other))
    (other / "bot.md").write_text("bot\n")
    git(other, "add", ".")
    git(other, "commit", "-qm", "bot")
    git(other, "push", "-q", "origin", "HEAD:main")
    (work / "late.md").write_text("late\n")
    git(work, "add", ".")
    git(work, "commit", "-qm", "late")
    head = git(work, "rev-parse", "HEAD")
    rc, summary, _ = reconcile(work, tmp_path)
    assert rc == 1 and "UNPUSHED" in summary
    assert git(work, "rev-parse", "HEAD") == head  # not rebased
    assert not (work / ".git/rebase-merge").exists()
    assert not (work / ".git/rebase-apply").exists()


def test_monthly_retro_turns_a_failed_reconcile_into_a_non_ok_status():
    text = (SCRIPTS / "blog-monthly-retro.sh").read_text()
    assert re.search(r'reconcile_repo "\$BLOG_DIR" "startaitools" "\$LOG" \|\|', text)
    assert re.search(
        r'reconcile_repo "/home/jeremy/000-projects/claude-code-plugins" '
        r'"tonsofskills" "\$LOG" \|\|',
        text,
    )
    assert 'STATUS="DEGRADED (reconcile' in text
    assert "FAILED*|DEGRADED*) cron_fail" in text
    assert 'case "$STATUS" in OK*) : ;; *) exit 1 ;; esac' in text


# --------------------------------------------------------------------------- #
# calibration_period (startaitools-8oc.17)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "arg,today,expected",
    [
        ("", "2026-10-01", "2026-09 2026-09-01 2026-10-01"),  # the cron case
        ("", "2026-10-31", "2026-09 2026-09-01 2026-10-01"),
        ("", "2026-01-01", "2025-12 2025-12-01 2026-01-01"),  # January -> December, prior year
        ("", "2026-03-31", "2026-02 2026-02-01 2026-03-01"),  # no 31-day overflow
        ("", "2024-03-01", "2024-02 2024-02-01 2024-03-01"),  # leap year
        ("2025-12", "2026-10-01", "2025-12 2025-12-01 2026-01-01"),  # explicit override
        ("2026-01", "2026-10-01", "2026-01 2026-01-01 2026-02-01"),
    ],
)
def test_calibration_period(arg, today, expected):
    proc = lib(f'calibration_period "{arg}" "{today}"')
    assert proc.returncode == 0 and proc.stdout.strip() == expected


@pytest.mark.parametrize(
    "bad", ["2026-13", "2026-00", "26-09", "2026-9", "september", "2026-09-01"]
)
def test_calibration_period_rejects_malformed_overrides(bad):
    proc = lib(f'calibration_period "{bad}" 2026-10-01')
    assert proc.returncode == 2 and proc.stdout == ""


def test_calibrate_wrapper_passes_the_period_to_the_skill_and_labels_with_it():
    text = (SCRIPTS / "blog-monthly-calibrate.sh").read_text()
    assert "YM=$(date +%Y-%m)" not in text
    assert 'calibration_period "${1:-}"' in text
    assert "claude -p '/blog-calibrate ${YM}'" in text
    assert "[$PERIOD_START, $PERIOD_END)" in text
    assert 'PER_RUN_LOG="$LOG_DIR/target-${YM}.log"' in text
    assert '"target-*.log"' in text
    # A push failure is no longer an OK run.
    assert 'STATUS="DEGRADED (report committed locally, push failed)"' in text


def test_calibrate_wrapper_rejects_a_bad_override_before_doing_anything(tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    proc = subprocess.run(
        ["bash", str(SCRIPTS / "blog-monthly-calibrate.sh"), "2026-13"],
        env={**GIT_ENV, "HOME": str(home)},
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 64 and "usage" in proc.stderr
    assert not (home / ".local/state/intent-os/liveness/blog-monthly-calibrate.ok").exists()


# --------------------------------------------------------------------------- #
# Recommendation worker PATH (startaitools-8oc.17)
# --------------------------------------------------------------------------- #
def test_worker_exports_a_path_that_finds_bd_under_cron(tmp_path):
    text = (SCRIPTS / "blog-recommendation-worker.sh").read_text()
    export = next(x for x in text.splitlines() if x.startswith("export PATH="))
    assert text.index(export) < text.index("command -v bd")
    home = tmp_path / "home"
    (home / ".local/bin").mkdir(parents=True)
    fake = home / ".local/bin/bd"
    fake.write_text("#!/bin/sh\nexit 0\n")
    fake.chmod(0o755)
    proc = subprocess.run(
        [
            "/usr/bin/env",
            "-i",
            f"HOME={home}",
            "PATH=/usr/bin:/bin",
            "/bin/bash",
            "-c",
            f"{export}; command -v bd",
        ],
        capture_output=True,
        text=True,
    )
    assert proc.stdout.strip() == str(fake)
