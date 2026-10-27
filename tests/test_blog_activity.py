"""Execute real producer success/failure branches with offline mail/gh/model stand-ins.

The scripts are cron entrypoints, not importable libraries. As with the existing
packet tests, slice actual source at stable section boundaries. No cron setup,
credentials, real mail, GitHub, git publish, model invocation or ledger is loaded.
Set INTENT_ACTIVITY_SHARED_SOURCE to the reviewed activity_spool.py for the
separate cross-repository durable-outbox integration test.
"""

import hashlib
import json
import os
import shlex
import shutil
import sqlite3
import subprocess
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts/blog"


def section(name, start, end=None):
    text = (SCRIPTS / name).read_text()
    offset = text.index(start)
    return text[offset : text.index(end, offset) if end else None]


def daily():
    return section("blog-backfill-daily.sh", "# Map land rc", "# Deploy patience")


def packet():
    return section(
        "blog-posting-packet.sh",
        'if send_packet "$TMP_HTML"',
        '\nif [ "$DRY_RUN" -eq 1 ]; then log',
    )


def rollup():
    return section("blog-team-rollup.sh", "# Success gate:", "# Notifications.")


def recommendation():
    return section(
        "blog-recommendation-worker.sh", "if PR_URL=$(gh pr create", '\nlog "=== worker end (1 bead'
    )


def quiet_recommendation():
    return section("blog-recommendation-worker.sh", "pick_bead() {", "# Re-read the bead")


def quiet_packet():
    return section("blog-posting-packet.sh", "GAP_ALERTED=0", "# Build each post's HTML")


class Harness:
    def __init__(self, path):
        self.path = path
        self.record = path / "calls.jsonl"
        bridge = path / "bridge.py"
        bridge.write_text(
            "import json, os, sys\n"
            "with open(os.environ['ACTIVITY_RECORD'], 'a') as f:\n"
            "    f.write(json.dumps(sys.argv[1:]) + '\\n')\n"
            "raise SystemExit(int(os.environ.get('BRIDGE_RC', '0')))\n"
        )
        self.env = {
            "PATH": "/usr/local/bin:/usr/bin:/bin",
            "HOME": str(path),
            "INTENT_ACTIVITY_ENABLED": "1",
            "INTENT_ACTIVITY_BRIDGE": str(bridge),
            "ACTIVITY_RECORD": str(self.record),
        }
        # External commands below are shell functions. Unexpected real effects
        # refuse instead of reaching an installed mailer or authenticated CLI.
        self.setup = """
set -uo pipefail
log() { :; }
node() { return "${MAIL_RC:-0}"; }
bd() { return 1; }
bd-sync() { :; }
git() { return 99; }
gh() { printf '%s' "${GH_OUTPUT:-}"; return "${GH_RC:-0}"; }
blog_ops_post() { :; }
"""
        self.setup += section("lib-cron-common.sh", "blog_activity_emit() {")
        self.setup += """
LOG=/dev/null
BLOG_DIR=.
DRY_RUN=0
MODE=single
LAND_RC=0
LAND_RESULT=OK
PRODUCER_STATUS=OK
PRODUCER_ACCEPTED=1
BLOG_PIPELINE_LOCK_HELD=1
YESTERDAY=2026-10-25
TODAY=2026-10-26
STATUS=""
EMAIL_SCRIPT=fixture-mailer-never-run
TEAM_EMAILS=synthetic@example.invalid
BLOG_DEPLOY_BRANCH=master
DEPLOY_BRANCH=master
BEAD=synthetic-task
TITLE='PRIVATE TITLE MUST NOT LEAVE'
PR_BODY='PRIVATE BODY MUST NOT LEAVE'
BRANCH=fixture-branch
TMP_HTML=fixture.html
SUBJECT='PRIVATE SUBJECT MUST NOT LEAVE'
EZEKIEL_EMAIL=synthetic@example.invalid
PACKET_FAILURES=0
PACKET_PLANE_CARD=0
SENT_SLUGS=(public-fixture-post)
SENT_STATUS=(sent)
SENT_CARDS=()
send_packet() { return "${MAIL_RC:-0}"; }
mark_sent() { return "${RECEIPT_RC:-0}"; }
"""

    def run(self, body, prelude="", env=None):
        return subprocess.run(
            ["bash", "-c", self.setup + "\n" + prelude + "\n" + body],
            cwd=self.path,
            env=self.env | (env or {}),
            text=True,
            capture_output=True,
            timeout=20,
        )

    def calls(self):
        return (
            [json.loads(line) for line in self.record.read_text().splitlines()]
            if self.record.exists()
            else []
        )

    def expected(self, producer, kind, identity):
        key = hashlib.sha256(f"blog-activity-v1:{producer}:{kind}:{identity}".encode()).hexdigest()
        return ["--result", kind, "--observation-key", key]


@pytest.fixture
def h(tmp_path):
    return Harness(tmp_path)


@pytest.mark.parametrize(
    "rc,kind",
    [
        (0, "published"),
        (15, "published"),
        (21, "published"),
        (13, "pending"),
        (14, "failed"),
        (20, "failed"),
        (22, "failed"),
    ],
)
def test_daily_uses_actual_lander_verdict(h, rc, kind):
    result = h.run(daily(), f"LAND_RC={rc}")
    assert result.returncode == 0, result.stderr
    assert h.calls() == [h.expected("blog-daily", kind, "2026-10-25")]


@pytest.mark.parametrize(
    "prelude", ["BLOG_CANARY=1", "PRODUCER_ACCEPTED=0", "BLOG_PIPELINE_LOCK_HELD=0"]
)
def test_daily_never_infers_publication_from_dryrun_rejection_or_lock_noop(h, prelude):
    result = h.run(daily(), prelude)
    assert result.returncode == 0, result.stderr
    assert h.calls() == []


@pytest.mark.parametrize(
    "failure,canary,expected",
    [
        ("", 0, 1),
        ("LIVE_RC=1", 0, 0),
        ("CHECK_RC=1", 0, 0),
        ("INDEX_RC=1", 0, 0),
        ("NOOP_RC=1", 0, 0),
        ("RECOVERY_DEGRADED=1", 0, 0),
        ("", 1, 0),
    ],
)
def test_daily_nothing_due_requires_completed_existing_publication_checks(
    h, failure, canary, expected
):
    crosspost = h.path / "scripts/blog/blog-crosspost-sweep.sh"
    crosspost.parent.mkdir(parents=True)
    crosspost.write_text("#!/bin/sh\nexit 0\n")
    crosspost.chmod(0o700)
    (h.path / "publication.py").write_text(
        "import os,sys\n"
        "name='CHECK_RC' if sys.argv[1]=='check-existing' else 'NOOP_RC'\n"
        "raise SystemExit(int(os.environ.get(name,'0')))\n"
    )
    body = section(
        "blog-backfill-daily.sh", "if EXISTING=$(published_post_for_date", "# Hugo theme"
    )
    prelude = f"""
BLOG_SOURCE_DIR=.
POSTS_DIR=.
PUBLICATION_HELPER=publication.py
WORKSPACE_HELPER=publication.py
BLOG_RUN_MANIFEST=fixture-manifest
RECOVERY_DEGRADED=0
BLOG_CANARY={canary}
published_post_for_date() {{ echo /fixture/public-post.md; }}
remote_live_check() {{ return "${{LIVE_RC:-0}}"; }}
rebuild_canonical_index() {{ return "${{INDEX_RC:-0}}"; }}
export {failure or "CHECK_RC=0"}
"""
    result = h.run(body, prelude)
    assert result.returncode == (1 if failure else 0), result.stderr
    assert h.calls() == [h.expected("blog-daily", "nothing_due", "2026-10-25")] * expected


@pytest.mark.parametrize(
    "prelude,expected",
    [("", 1), ("DRY_RUN=1", 0), ("SENT_STATUS=(held)", 0), ("MAIL_RC=1", 0), ("RECEIPT_RC=1", 0)],
)
def test_packet_requires_real_mail_and_sent_ledger_receipt(h, prelude, expected):
    result = h.run(packet(), prelude)
    assert result.returncode == (1 if "MAIL_RC=1" in prelude else 0), result.stderr
    assert h.calls() == [h.expected("blog-packet", "sent", "public-fixture-post")] * expected


def test_packet_mixed_hold_batch_only_emits_real_distribution(h):
    result = h.run(packet(), "SENT_SLUGS=(public-held public-sent); SENT_STATUS=(held sent)")
    assert result.returncode == 0, result.stderr
    assert h.calls() == [h.expected("blog-packet", "sent", "public-sent")]


@pytest.mark.parametrize(
    "mail_rc,dryrun,valid,expected",
    [(0, 0, True, 1), (1, 0, True, 0), (0, 1, True, 0), (0, 0, False, 0)],
)
def test_rollup_requires_validated_report_and_successful_mail(h, mail_rc, dryrun, valid, expected):
    (h.path / "report.html").write_text("x" * 500)
    (h.path / "registry.py").write_text(f"raise SystemExit({0 if valid else 1})\n")
    prelude = f"""
OUTPUT_HTML=report.html
REGISTRY_HELPER=registry.py
HEADER_SCRIPT=registry.py
RESET_MARKER=fixture-marker
DICTIONARY_FILE=fixture-dictionary
LOG_DIR=.
MAIL_RC={mail_rc}
ROLLUP_DRY_RUN={dryrun}
"""
    result = h.run(rollup(), prelude)
    assert result.returncode == 0, result.stderr
    assert h.calls() == [h.expected("blog-rollup", "sent", "2026-10-26")] * expected


@pytest.mark.parametrize(
    "gh_rc,url,expected",
    [
        (0, "https://github.com/jeremylongshore/startaitools.com/pull/123", 1),
        (1, "https://github.com/jeremylongshore/startaitools.com/pull/123", 0),
        (0, "", 0),
        (0, "https://example.invalid/private/customer", 0),
    ],
)
def test_recommendation_requires_actual_ready_pr_output(h, gh_rc, url, expected):
    result = h.run(recommendation(), f"GH_RC={gh_rc}\nGH_OUTPUT={shlex.quote(url)}")
    assert result.returncode == (14 if gh_rc else 0), result.stderr
    assert h.calls() == [h.expected("blog-recommendation", "ready", "123")] * expected


@pytest.mark.parametrize("success,dryrun,expected", [(True, 0, 1), (False, 0, 0), (True, 1, 0)])
def test_recommendation_empty_queue_requires_successful_read_not_error(
    h, success, dryrun, expected
):
    prelude = f"""
TARGET_BEAD=""
LABEL_ALLOW=auto-ok
LABEL_DENY=owner-gated
DRY_RUN={dryrun}
bd() {{ printf '[]'; return {0 if success else 1}; }}
"""
    result = h.run(quiet_recommendation(), prelude)
    assert result.returncode == 0, result.stderr
    assert len(h.calls()) == expected
    if expected:
        assert h.calls()[0][:2] == ["--result", "nothing_due"]


@pytest.mark.parametrize(
    "response", ["", "[{}]", '[{"priority":1}]', "[] []", "null", '[{"id":""}]', '[{"id":42}]']
)
def test_recommendation_no_data_or_invalid_records_are_not_an_empty_queue(h, response):
    prelude = f"""
TARGET_BEAD=""
LABEL_ALLOW=auto-ok
LABEL_DENY=owner-gated
bd() {{ printf '%s' {shlex.quote(response)}; }}
"""
    result = h.run(quiet_recommendation(), prelude)
    assert result.returncode == 0, result.stderr  # preserve the legacy heartbeat outcome
    assert h.calls() == []


@pytest.mark.parametrize(
    "ledger,dryrun,gap_mail_rc,expected",
    [
        ([{"date": "2026-10-25", "packet_sent": True}], 0, 0, 1),
        ([{"date": "2026-10-25", "packet_sent": True}], 1, 0, 0),
        ([{"date": "2026-10-25", "packet_sent": False}], 0, 0, 0),
        ([], 0, 1, 0),
        ({"bad": "ledger"}, 0, 1, 0),
        (None, 0, 1, 0),
    ],
)
def test_packet_empty_selection_needs_healthy_ledger_even_if_gap_email_fails(
    h, ledger, dryrun, gap_mail_rc, expected
):
    (h.path / "ledger.json").write_text(json.dumps(ledger) if ledger is not None else "broken")
    prelude = f"""
MODE=sweep
ENTRIES=()
LEDGER_FILE=ledger.json
DRY_RUN={dryrun}
MAIL_RC={gap_mail_rc}
date() {{ if [ "${{1:-}}" = -d ]; then echo 2026-10-25; else echo 2026-10-26; fi; }}
"""
    result = h.run(quiet_packet(), prelude)
    assert result.returncode == 0, result.stderr
    assert h.calls() == [h.expected("blog-packet", "nothing_due", "2026-10-26")] * expected


@pytest.mark.parametrize("body", [daily(), packet(), rollup(), recommendation()])
def test_default_off_and_bridge_failure_never_change_producer_outcome(h, body):
    (h.path / "report.html").write_text("x" * 500)
    (h.path / "registry.py").write_text("raise SystemExit(0)\n")
    prelude = """
OUTPUT_HTML=report.html
REGISTRY_HELPER=registry.py
HEADER_SCRIPT=registry.py
RESET_MARKER=fixture
DICTIONARY_FILE=fixture
LOG_DIR=.
GH_OUTPUT=https://github.com/jeremylongshore/startaitools.com/pull/123
"""
    result = h.run(body, prelude, {"INTENT_ACTIVITY_ENABLED": "0"})
    assert result.returncode == 0, result.stderr
    assert h.calls() == []
    result = h.run(body, prelude, {"BRIDGE_RC": "27"})
    assert result.returncode == 0, result.stderr
    assert "PRIVATE" not in result.stderr


@pytest.mark.parametrize(
    "producer,kind,identity",
    [
        ("arbitrary", "sent", "2026-10-26"),
        ("blog-packet", "sent", "customer@example.invalid"),
        ("blog-daily", "raw log", "2026-10-26"),
        ("blog-recommendation", "ready", "private-bead-123"),
    ],
)
def test_helper_refuses_unapproved_identity_or_kind(h, producer, kind, identity):
    result = h.run("blog_activity_emit " + " ".join(map(shlex.quote, (producer, kind, identity))))
    assert result.returncode == 0
    assert h.calls() == []


@pytest.mark.parametrize(
    "producer", ["blog-daily", "blog-packet", "blog-rollup", "blog-recommendation"]
)
def test_wrapper_binds_fixed_producer_and_deduplication(tmp_path, producer):
    (tmp_path / "activity_spool.py").write_text(
        "import json\ndef main(producer, outcomes, *, deduplicate):\n"
        " print(json.dumps([producer, outcomes, deduplicate]))\n return 0\n"
    )
    result = subprocess.run(
        ["python3", str(SCRIPTS / f"{producer}-event.py")],
        env={"PATH": "/usr/local/bin:/usr/bin:/bin", "PYTHONPATH": str(tmp_path)},
        capture_output=True,
        text=True,
        check=True,
    )
    bound, outcomes, dedup = json.loads(result.stdout)
    assert bound == producer
    assert dedup is True
    assert all(key == value for key, value in outcomes.items())


@pytest.mark.skipif(
    not os.environ.get("INTENT_ACTIVITY_SHARED_SOURCE"),
    reason="explicit reviewed cross-repo activity_spool.py required",
)
def test_real_shared_outbox_retry_and_ack_never_recreate_public_observation(h):
    source = Path(os.environ["INTENT_ACTIVITY_SHARED_SOURCE"])
    installed = h.path / "installed"
    installed.mkdir()
    shutil.copyfile(source, installed / "activity_spool.py")
    spool = h.path / "spool"
    cases = [
        ("blog-daily", "published", "2026-10-25"),
        ("blog-packet", "sent", "public-fixture-post"),
        ("blog-rollup", "sent", "2026-10-26"),
        ("blog-recommendation", "ready", "123"),
    ]
    for producer, kind, identity in cases:
        wrapper = installed / f"{producer}-event.py"
        shutil.copyfile(SCRIPTS / wrapper.name, wrapper)
        env = {"INTENT_ACTIVITY_BRIDGE": str(wrapper), "INTENT_ACTIVITY_SPOOL_DIR": str(spool)}
        for _ in range(2):
            result = h.run(f"blog_activity_emit {producer} {kind} {identity}", env=env)
            assert result.returncode == 0 and not result.stderr, result.stderr
    db_files = list(spool.glob("activity.db"))
    assert len(db_files) == 1
    with sqlite3.connect(db_files[0]) as db:
        rows = db.execute("SELECT event_id,producer,kind FROM pending").fetchall()
        assert len(rows) == 4
        assert len({row[0] for row in rows}) == 4
        assert {(row[1], row[2]) for row in rows} == {(p, k) for p, k, _ in cases}
        # Model acknowledged intake by removing pending rows, retaining the
        # shared module's observation tombstones. Replay must stay silent.
        db.execute("DELETE FROM pending")
    for producer, kind, identity in cases:
        result = h.run(
            f"blog_activity_emit {producer} {kind} {identity}",
            env={
                "INTENT_ACTIVITY_BRIDGE": str(installed / f"{producer}-event.py"),
                "INTENT_ACTIVITY_SPOOL_DIR": str(spool),
            },
        )
        assert result.returncode == 0 and not result.stderr, result.stderr
    with sqlite3.connect(db_files[0]) as db:
        assert db.execute("SELECT COUNT(*) FROM pending").fetchone()[0] == 0
        assert db.execute("SELECT COUNT(*) FROM observations").fetchone()[0] == 4
