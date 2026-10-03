"""Fault-injection proofs that the lander never reports an unqualified OK after a
post-publication stage failed (startaitools-8oc.15 follow-on, intent-os 227 §4).

The post itself is published and verified before these stages run, so a failure
here must keep the publish successful while the run reports DEGRADED: a distinct
exit code, an alert, no success line for the failed stage, and a wrapper status
that withholds the liveness `.ok` marker.

Also covers the Hashnode pause switch and the ambiguous-row resolution tool
(startaitools-8oc.20) and the posting-packet reply instruction.
"""

import json
import os
import shlex
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts/blog"
LAND = (SCRIPTS / "blog-land.sh").read_text(encoding="utf-8")
DAILY = (SCRIPTS / "blog-backfill-daily.sh").read_text(encoding="utf-8")
ARTICLE = "https://startaitools.com/posts/fixture/"


def shell(source, tmp_path, env=None):
    return subprocess.run(
        ["/bin/bash", "-c", source],
        cwd=tmp_path,
        env={**os.environ, "INTENT_RUNTIME": "/nonexistent-offline-runtime", **(env or {})},
        capture_output=True,
        text=True,
        timeout=20,
    )


def lander_tail(tmp_path, *, push_ok=True, crosspost_rc=0, live=True):
    """Run blog-land.sh from the image stage to the end with every effect stubbed."""
    block = LAND[LAND.index("# ---- Per-post image") :]
    skills = tmp_path / "skills"
    skills.mkdir()
    crosspost = skills / "check-crosspost-queue.sh"
    crosspost.write_text(f"#!/bin/bash\nexit {crosspost_rc}\n")
    crosspost.chmod(0o755)
    sentinel = tmp_path / "sentinel.json"
    sentinel.write_text("{}")
    return shell(
        f"""
set -o pipefail
POST=/offline/post.md
BLOG_DIR={shlex.quote(str(tmp_path))}
SKILL_SCRIPTS={shlex.quote(str(skills))}
SENTINEL={shlex.quote(str(sentinel))}
CANONICAL={shlex.quote(ARTICLE)}
LIVENESS_MAX_SECS=1
TARGET_DATE=2026-10-02
SLUG=fixture
DEPLOY_BRANCH=master
LOG=/dev/null
BLOG_IMAGE_GEN=0
log() {{ printf '%s\\n' "$*"; }}
urgent_alert() {{ printf 'ALERT: %s\\n' "$1"; }}
timeout() {{ return 0; }}
git() {{
  case "$*" in
    *"diff --cached --quiet"*) return 1 ;;   # there ARE new image assets
    *) return 0 ;;
  esac
}}
push_with_rebase() {{ return {0 if push_ok else 1}; }}
remote_live_check() {{ return {0 if live else 1}; }}
{block}
""",
        tmp_path,
    )


def test_clean_post_publication_stages_still_land_ok(tmp_path):
    result = lander_tail(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "LAND-RESULT: OK" in result.stdout
    assert "Image assets committed and pushed" in result.stdout
    assert "DEGRADED" not in result.stdout


def test_failed_image_asset_push_is_degraded_not_ok(tmp_path):
    result = lander_tail(tmp_path, push_ok=False)
    assert result.returncode == 15, result.stdout + result.stderr
    assert "LAND-RESULT: DEGRADED" in result.stdout
    assert "image-assets" in result.stdout.split("LAND-RESULT: DEGRADED", 1)[1]
    assert "LAND-RESULT: OK" not in result.stdout
    # No success line for the stage that failed.
    assert "Image assets committed and pushed" not in result.stdout
    assert "ALERT:" in result.stdout


def test_failed_crosspost_queue_processor_is_degraded_and_alerts(tmp_path):
    result = lander_tail(tmp_path, crosspost_rc=1)
    assert result.returncode == 15, result.stdout + result.stderr
    tail = result.stdout.split("LAND-RESULT: DEGRADED", 1)[1]
    assert "crosspost-queue" in tail
    assert "LAND-RESULT: OK" not in result.stdout
    assert "ALERT:" in result.stdout and "cross-post" in result.stdout.lower()


def test_both_stages_failing_are_both_named(tmp_path):
    result = lander_tail(tmp_path, push_ok=False, crosspost_rc=1)
    assert result.returncode == 15
    tail = result.stdout.split("LAND-RESULT: DEGRADED", 1)[1]
    assert "image-assets" in tail and "crosspost-queue" in tail


def test_unavailable_public_article_still_outranks_degraded(tmp_path):
    result = lander_tail(tmp_path, push_ok=False, live=False)
    assert result.returncode == 13
    assert "LAND-RESULT: FAILED" in result.stdout
    assert "LAND-RESULT: OK" not in result.stdout


def test_failed_queue_insert_is_a_failed_delivery_never_ok(tmp_path):
    """The queue row is inserted by the publication helper's reconcile; its failure
    must stop the lander with the delivery-pending code before any OK path."""
    start = LAND.index('python3 "$PUBLICATION_HELPER" reconcile')
    block = LAND[start : LAND.index("# ---- Dual-publish", start)]
    result = shell(
        f"""
LOG=/dev/null
BLOG_RUN_MANIFEST=/offline/manifest.json
PUBLICATION_HELPER=/offline/helper.py
log() {{ printf '%s\\n' "$*"; }}
python3() {{ return 1; }}
{block}
printf 'REACHED-OPTIONAL-STAGES\\n'
""",
        tmp_path,
    )
    assert result.returncode == 14
    assert "LAND-RESULT: FAILED" in result.stdout
    assert "REACHED-OPTIONAL-STAGES" not in result.stdout


def wrapper_status(tmp_path, land_rc):
    status = DAILY.split('case "$LAND_RC" in', 1)[1].split("\nesac", 1)[0]
    return shell(
        f"""
LAND_RC={land_rc}
PRODUCER_STATUS=OK
LAND_RESULT='DEGRADED (published and live; failed stages: image-assets)'
case "$LAND_RC" in{status}
esac
printf '%s\\n' "$STATUS"
""",
        tmp_path,
    )


def test_wrapper_maps_degraded_land_to_degraded_status(tmp_path):
    result = wrapper_status(tmp_path, 15)
    assert result.stdout.startswith("DEGRADED"), result.stdout
    assert "published" in result.stdout


def final_exit(tmp_path, status):
    tail = DAILY[DAILY.rindex('case "$STATUS" in OK*') :]
    return shell(
        f"STATUS={shlex.quote(status)}\nrun_catch_up() {{ :; }}\n{tail}\nexit 0\n", tmp_path
    )


@pytest.mark.parametrize(
    "status,code",
    [
        ("OK", 0),
        ("PENDING (published; page not live)", 0),
        ("DEGRADED (published)", 2),
        ("FAILED (x)", 1),
    ],
)
def test_wrapper_exit_withholds_ok_marker_for_degraded(tmp_path, status, code):
    assert final_exit(tmp_path, status).returncode == code


def test_wrapper_pages_on_degraded(tmp_path):
    start = DAILY.index("# Buzz sys-automation on a hard failure only")
    block = DAILY[start : DAILY.index("# --- Summary email", start)]
    result = shell(
        f"""
STATUS='DEGRADED (published)'
ESCALATE_PREFIX=''
YESTERDAY=2026-10-02
CONSEC_FAILS=0
LOG=/dev/null
log() {{ :; }}
cron_fail() {{ printf 'CRON_FAIL %s\\n' "$1"; }}
{block}
""",
        tmp_path,
    )
    assert "CRON_FAIL blog-backfill-daily" in result.stdout


def test_failover_child_that_published_degraded_never_lets_the_parent_write_ok():
    block = DAILY[DAILY.index("FAILOVER_RC=$?") : DAILY.index('FAILOVER_NOTE="; failover')]
    assert "DEGRADED" in block
    assert "exit 2" in block


# ---- Hashnode pause + ambiguous resolution (startaitools-8oc.20) ------------------

DISPATCH = SCRIPTS / "blog_crosspost_dispatch.py"


def queue(tmp_path, rows):
    path = tmp_path / ".crosspost-queue.json"
    path.write_text(json.dumps(rows))
    return path


def row(slug, hashnode):
    return {
        "slug": slug,
        "title": "Fixture",
        "canonical_url": f"https://startaitools.com/posts/{slug}/",
        "published_at": "2026-09-30T10:30:00+00:00",
        "tier": 2,
        "devto": {"status": "published", "url": "https://dev.to/x"},
        "hashnode": hashnode,
        "medium": {"status": "skipped"},
    }


def resolve(path, slug, *extra):
    return subprocess.run(
        [
            "python3",
            str(DISPATCH),
            "resolve",
            "--queue",
            str(path),
            "--slug",
            slug,
            "--platform",
            "hashnode",
            "--reason",
            "abandoned: paid-api-required (owner decision 2026-10-03)",
            *extra,
        ],
        capture_output=True,
        text=True,
        timeout=20,
    )


def test_resolve_moves_an_ambiguous_row_to_terminal_and_keeps_history(tmp_path):
    prior = {
        "status": "ambiguous",
        "error": "remote acceptance unverified; reconcile before retry",
        "attempts": 1,
        "dispatch_id": "abc",
    }
    path = queue(tmp_path, [row("a", dict(prior))])
    result = resolve(path, "a")
    assert result.returncode == 0, result.stderr
    state = json.loads(path.read_text())[0]["hashnode"]
    assert state["status"] == "skipped"
    assert state["error"] == "abandoned: paid-api-required (owner decision 2026-10-03)"
    assert state["attempts"] == 1 and state["dispatch_id"] == "abc"
    (entry,) = state["resolutions"]
    assert entry["from"] == "ambiguous" and entry["prior_error"] == prior["error"]
    assert entry["reason"].startswith("abandoned:") and entry["at"].endswith("Z")


@pytest.mark.parametrize("status", ["published", "dispatching", "pending", "skipped"])
def test_resolve_refuses_rows_not_in_the_allowed_from_set(tmp_path, status):
    path = queue(tmp_path, [row("a", {"status": status, "url": "https://h/x"})])
    before = path.read_text()
    result = resolve(path, "a")
    assert result.returncode == 1
    assert path.read_text() == before


def test_resolve_refuses_published_even_when_explicitly_allowed(tmp_path):
    path = queue(tmp_path, [row("a", {"status": "published", "url": "https://h/x"})])
    result = resolve(path, "a", "--from", "published")
    assert result.returncode != 0


def test_hashnode_pause_switch_is_recorded_in_tracked_config():
    config = json.loads((SCRIPTS / "crosspost-destinations.json").read_text())
    assert config["hashnode"]["enabled"] is False
    assert "paid-api-required" in config["hashnode"]["reason"]


def run_processor(tmp_path, rows, config):
    blog = tmp_path / "blog"
    (blog / "scripts/blog").mkdir(parents=True)
    (blog / "scripts/blog/lib-cron-common.sh").write_bytes(
        (SCRIPTS / "lib-cron-common.sh").read_bytes()
    )
    if config is not None:
        (blog / "scripts/blog/crosspost-destinations.json").write_text(json.dumps(config))
    path = blog / ".crosspost-queue.json"
    path.write_text(json.dumps(rows))
    marker = tmp_path / "hashnode-called"
    provider = tmp_path / "hashnode"
    provider.write_text(
        f"#!/bin/sh\nprintf called > {shlex.quote(str(marker))}\necho https://h/x\n"
    )
    provider.chmod(0o755)
    env = {
        **os.environ,
        "BLOG_DIR": str(blog),
        "HASHNODE_SCRIPT": str(provider),
        "HASHNODE_PAT": "test",
        "HASHNODE_PUBLICATION_ID": "test",
        "DEVTO_API_KEY": "",
    }
    result = subprocess.run(
        ["bash", str(ROOT / ".claude/skills/blog-backfill/scripts/check-crosspost-queue.sh")],
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result, json.loads(path.read_text()), marker


PAUSED = {
    "hashnode": {
        "enabled": False,
        "reason": "paused: paid-api-required (owner decision 2026-10-03)",
    }
}


def test_paused_hashnode_is_never_dispatched_and_pending_rows_become_terminal(tmp_path):
    pending = {"status": "pending", "publish_after": "1970-01-01T00:00:00Z"}
    result, rows, marker = run_processor(tmp_path, [row("a", pending)], PAUSED)
    assert result.returncode == 0, result.stderr
    assert not marker.exists()
    assert rows[0]["hashnode"]["status"] == "skipped"
    assert rows[0]["hashnode"]["resolutions"][0]["from"] == "pending"
    assert "paused" in result.stderr.lower()


def test_resolved_held_rows_let_the_sweep_exit_zero(tmp_path):
    resolved = {
        "status": "skipped",
        "error": "abandoned: paid-api-required (owner decision 2026-10-03)",
    }
    result, _, _ = run_processor(tmp_path, [row("a", resolved), row("b", resolved)], PAUSED)
    assert result.returncode == 0, result.stderr
    assert "Held entries (verify remote acceptance before retry): 0" in result.stderr


def test_ambiguous_rows_still_hold_the_sweep_until_resolved(tmp_path):
    held = {"status": "ambiguous", "error": "remote acceptance unverified; reconcile before retry"}
    result, rows, _ = run_processor(tmp_path, [row("a", held)], PAUSED)
    assert result.returncode == 1
    assert rows[0]["hashnode"]["status"] == "ambiguous"  # pause never silently clears a held row


def test_missing_config_keeps_hashnode_enabled(tmp_path):
    pending = {"status": "pending", "publish_after": "1970-01-01T00:00:00Z"}
    result, rows, _ = run_processor(tmp_path, [row("a", pending)], None)
    assert rows[0]["hashnode"]["status"] == "pending"
    assert "paused" not in result.stderr.lower()


# ---- Posting packet reply instruction (E04) --------------------------------------


def test_packet_footer_asks_for_live_urls_or_the_weekly_paste():
    text = (SCRIPTS / "blog-posting-packet.sh").read_text(encoding="utf-8")
    assert "reply with the live URLs (or use the weekly paste)" in text
