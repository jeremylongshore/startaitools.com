"""Owner status card for the Buzz blog-ops channel (scripts/blog/lib-blog-ops-notify.sh).

buzz_post is always a stub here: the runtime file the library sources is written by the
test, so nothing can reach a real relay. The properties that matter:
  * the card says what happened, in at most 11 lines (the transport adds one more);
  * it never carries a local path;
  * it goes to topic blog-ops at info, with the floor lowered, no model rewrite, no
    email floor and no dead-man ping;
  * a Buzz failure of any kind (error, hang, missing runtime) never changes the run.
"""

import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "scripts/blog/lib-blog-ops-notify.sh"
WRAPPER = ROOT / "scripts/blog/blog-backfill-daily.sh"

START = "[2026-10-04T04:00:00-06:00] === Daily blog-backfill start (target: 2026-10-03) ===\n"
SUCCESS_LOG = START + """\
PRODUCER-CONTRACT: ADVISORY: amended contract (observation until 2026-10-14): complete
PRODUCER-CONTRACT: ADVISORY: record schema (observation until 2026-10-17): complete
[2026-10-04T04:28:14-06:00] PRODUCER-CONTRACT: complete incident=blog-daily-2026-10-03 run=x
[2026-10-04T04:28:45-06:00] Title: Verify The Push, Not Exit 0 | Tier: 1 (classifier 2, 144 lines)
[t] Liveness OK: https://startaitools.com/posts/verify-the-push/ (after 232s)
[2026-10-04T04:33:20-06:00] Dual-published to tonsofskills (origin/main)
[2026-10-04T04:34:13-06:00] LAND-RESULT: OK
[2026-10-04T04:34:13-06:00] Overall STATUS: OK
[2026-10-04T04:40:00-06:00] CATCH-UP: 2026-10-01 recovered; no human involved
"""


def stub_runtime(tmp_path, body):
    runtime = tmp_path / "intent-runtime.sh"
    runtime.write_text(body)
    return runtime


RECORDING = """buzz_post() {
  { printf 'TOPIC=%s\\nSEV=%s\\nMIN=%s\\nLLM=%s\\nEMAIL=%s\\nHC=[%s]\\nSRC=%s\\n---\\n' \
      "$2" "$3" "$AF_MIN_SEVERITY" "$AF_LLM_NORMALIZE" "$AF_EMAIL_FLOOR" "$AF_HC_URL" "$AF_SOURCE"
    printf '%s' "$1"; } > "$RECORD"
}
"""


def run(script, tmp_path, runtime=None, **extra):
    env = dict(os.environ, RECORD=str(tmp_path / "record.txt"), LIB=str(LIB))
    env.pop("BLOG_OPS_BUZZ", None)
    if runtime is not None:
        env["BLOG_OPS_RUNTIME"] = str(runtime)
    env.update(extra)
    return subprocess.run(
        ["bash", "-c", 'set -uo pipefail; . "$LIB"; ' + script],
        env=env, capture_output=True, text=True, timeout=60,
    )


def digest(tmp_path, log_text, status, land, urgent="0"):
    log = tmp_path / "run.log"
    log.write_text(log_text)
    result = run(f'blog_ops_daily_digest 2026-10-03 "{status}" "{land}" "{log}" {urgent}', tmp_path)
    assert result.returncode == 0, result.stderr
    return result.stdout


def test_success_card_names_the_post_tier_switches_and_dual_publish(tmp_path):
    card = digest(tmp_path, SUCCESS_LOG, "OK", "OK")
    lines = card.splitlines()
    assert lines == [
        "Blog daily: 2026-10-03",
        "Post: Verify The Push, Not Exit 0",
        "Live: https://startaitools.com/posts/verify-the-push/",
        "Tier: classifier 2 -> shipped 1",
        "Land: OK | Status: OK",
        "Producer contract: complete",
        "Brief switch (observation until 2026-10-14): complete",
        "Record schema switch (observation until 2026-10-17): complete",
        "Catch-up: 1 published, gave up on none",
        "Dual-publish to tonsofskills: yes",
    ]
    assert not any(line.startswith("needs you") for line in lines)


def test_only_the_current_run_is_read(tmp_path):
    earlier = SUCCESS_LOG.replace("Verify The Push", "Yesterday's Rerun")
    later = START + "[x] LAND-RESULT: NO-POST\n"
    card = digest(tmp_path, earlier + later, "OK", "NO-POST")
    assert "Yesterday's Rerun" not in card
    assert "Post: nothing to publish" in card
    assert "Catch-up: 0 published" in card


def test_nothing_to_publish_card_has_no_post_lines_and_no_needs_you(tmp_path):
    card = digest(tmp_path, START + "[x] LAND-RESULT: NO-POST\n", "OK", "NO-POST")
    assert "Post: nothing to publish" in card
    assert "Live:" not in card and "Tier:" not in card
    assert "Producer contract: not run" in card
    assert "Dual-publish to tonsofskills: no (nothing landed)" in card
    assert "needs you" not in card
    assert len(card.splitlines()) <= 11


def test_degraded_card_says_what_needs_the_owner_in_one_line(tmp_path):
    text = SUCCESS_LOG.replace(
        "Dual-published to tonsofskills (origin/main)",
        "WARN: dual-publish to tonsofskills failed after retries (canonical already live)",
    ) + "[x] CATCH-UP: GAVE UP on 2026-09-30 after 3 attempts; this needs a human\n"
    status = "DEGRADED (published and live; failed stages: dual-publish)"
    card = digest(tmp_path, text, status, status, urgent="1")
    lines = card.splitlines()
    assert "Dual-publish to tonsofskills: no (failed after retries)" in lines
    needs = [line for line in lines if line.startswith("needs you:")]
    assert len(needs) == 1
    assert "sys-automation" in needs[0] and "2026-09-30" in needs[0]
    assert "contract switch" in needs[0]
    assert len(lines) <= 11


def test_failed_run_never_says_nothing_to_publish_and_strips_local_paths(tmp_path):
    status = "FAILED (producer rejected; log /home/someone/.local/state/x.log; land not invoked)"
    card = digest(tmp_path, START, status, "SKIPPED (producer was not accepted)")
    assert "Post: none landed (the run failed)" in card
    assert "/home/" not in card and "[local]" in card
    assert "needs you:" in card


def test_post_goes_to_blog_ops_at_info_without_escalation(tmp_path):
    runtime = stub_runtime(tmp_path, RECORDING)
    result = run('blog_ops_post "hello card" blog-backfill-daily; echo "rc=$?"', tmp_path, runtime)
    assert result.returncode == 0
    assert "BLOG-OPS: card handed to buzz_post" in result.stdout
    assert result.stdout.strip().endswith("rc=0")
    record = (tmp_path / "record.txt").read_text()
    header, body = record.split("---\n", 1)
    assert body == "hello card"
    assert "TOPIC=blog-ops" in header and "SEV=info" in header and "MIN=info" in header
    assert "LLM=0" in header and "EMAIL=0" in header and "HC=[]" in header
    assert "SRC=blog-backfill-daily" in header


@pytest.mark.parametrize(
    "runtime_body, expected",
    [
        ("buzz_post() { exit 3; }\n", "post failed (rc=3)"),
        ("true\n", "buzz_post unavailable"),
        ("buzz_post() { sleep 30; }\n", "timed out"),
    ],
    ids=["relay-error", "no-buzz-post", "relay-hang"],
)
def test_buzz_down_never_changes_the_caller(tmp_path, runtime_body, expected):
    runtime = stub_runtime(tmp_path, runtime_body)
    script = 'STATUS=OK; blog_ops_post "card" x; echo "rc=$? STATUS=$STATUS"'
    result = run(script, tmp_path, runtime, BLOG_OPS_TIMEOUT="2")
    assert result.returncode == 0, result.stderr
    assert expected in result.stdout
    assert result.stdout.strip().endswith("rc=0 STATUS=OK")


def test_missing_runtime_and_kill_switch_are_quiet_no_ops(tmp_path):
    missing = run('blog_ops_post "card" x; echo "rc=$?"', tmp_path, tmp_path / "absent.sh")
    assert "runtime unavailable" in missing.stdout and missing.stdout.strip().endswith("rc=0")
    runtime = stub_runtime(tmp_path, RECORDING)
    off = run('blog_ops_post "card" x; echo "rc=$?"', tmp_path, runtime, BLOG_OPS_BUZZ="0")
    assert "disabled" in off.stdout and not (tmp_path / "record.txt").exists()


def wrapper_card_function():
    text = WRAPPER.read_text()
    start = text.index("blog_ops_daily_card() {")
    end = text.index("\n}\n", start) + 3
    return text[start:end]


@pytest.mark.parametrize(
    "status, expected_exit",
    [("OK", 0), ("DEGRADED (published and live; failed stages: x)", 2), ("FAILED (x)", 1)],
)
def test_wrapper_exit_is_unchanged_when_buzz_is_down(tmp_path, status, expected_exit):
    log = tmp_path / "run.log"
    log.write_text(SUCCESS_LOG)
    runtime = stub_runtime(tmp_path, "buzz_post() { exit 7; }\n")
    script = (
        f'LOG="{log}"; YESTERDAY=2026-10-03; STATUS="{status}"; LAND_RESULT=OK; BRIEF_URGENT=0\n'
        'log() { echo "[t] $*" >> "$LOG"; }\n'
        + wrapper_card_function()
        + 'blog_ops_daily_card "$STATUS" "$LAND_RESULT"\n'
        'case "$STATUS" in OK*|PENDING*) : ;; DEGRADED*) exit 2 ;; *) exit 1 ;; esac\n'
    )
    result = run(script, tmp_path, runtime)
    assert result.returncode == expected_exit, result.stderr
    assert "BLOG-OPS: post failed (rc=7)" in log.read_text()


@pytest.mark.parametrize("child", ["BLOG_CANARY=1", "BLOG_FAILOVER_DEPTH=1",
                                   "BLOG_QUIET_FAILURE=1", "BLOG_CATCHUP_CHILD=1"])
def test_children_and_canaries_never_post(tmp_path, child):
    log = tmp_path / "run.log"
    log.write_text(SUCCESS_LOG)
    runtime = stub_runtime(tmp_path, RECORDING)
    script = (
        f'LOG="{log}"; YESTERDAY=2026-10-03; BRIEF_URGENT=0\n'
        'log() { echo "[t] $*" >> "$LOG"; }\n'
        + wrapper_card_function()
        + 'blog_ops_daily_card OK OK\n'
    )
    key, value = child.split("=")
    result = run(script, tmp_path, runtime, **{key: value})
    assert result.returncode == 0
    assert not (tmp_path / "record.txt").exists()


def test_wrapper_posts_after_catch_up_and_before_the_truthful_exit():
    text = WRAPPER.read_text()
    tail = text[text.rindex("\nrun_catch_up\n"):]
    assert tail.index("blog_ops_daily_card") < tail.index('case "$STATUS" in OK*|PENDING*)')
    assert text.index("lib-blog-ops-notify.sh") < text.index("blog_ops_daily_card() {")
