"""Exercise actual wrapper functions without invoking a provider or publishing."""

import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/blog/blog-backfill-daily.sh"


@pytest.mark.parametrize(
    ("producer", "status", "expected"),
    [
        ("claude", 1, "claude exit 1"),
        ("claude", 124, "claude timeout exit 124"),
        ("grok", 42, "grok exit 42"),
        ("minimax", 2, "minimax max-turns"),
        ("minimax", 3, "minimax timeout"),
        ("minimax", 124, "minimax timeout"),
    ],
)
def test_producer_preserves_failure_exit(producer, status, expected, tmp_path):
    source = SCRIPT.read_text()
    functions = source.split("run_claude_producer() {", 1)[1].split("\nPRODUCER_HEAD=", 1)[0]
    harness = f"""
set -uo pipefail
LOG={tmp_path / "run.log"}
GROK_BIN=/bin/true
MINIMAX_AGENT=/bin/true
YESTERDAY=2026-09-12
TIMEOUT_SECS=2700
BLOG_DIR={tmp_path}
PRODUCER_GUARD_DIR={tmp_path}
PRODUCER_STATUS=NOT-RUN
log() {{ printf '%s\\n' "$*"; }}
env() {{ return {status}; }}
run_claude_producer() {{{functions}
run_{producer}_producer
result=$?
printf 'RESULT:%s STATUS:%s\\n' "$result" "$PRODUCER_STATUS"
"""
    result = subprocess.run(["bash", "-c", harness], text=True, capture_output=True, check=True)
    assert "RESULT:1" in result.stdout
    assert expected in result.stdout
    assert "exit 0" not in result.stdout


def test_auto_never_falls_back_to_tool_incomplete_shell_agent():
    source = SCRIPT.read_text()
    branch = source.split("  auto|*)\n", 1)[1].split("\nesac", 1)[0]
    output = subprocess.run(
        [
            "bash",
            "-c",
            """
run_claude_producer() { echo primary-failed; return 69; }
run_minimax_producer() { echo unsafe-fallback; }
run_grok_producer() { echo unsafe-fallback; }
case auto in
  auto|*)
"""
            + branch
            + "\nesac",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert output.stdout.strip() == "primary-failed"


def test_regression_exit_zero_without_artifacts_was_healthy_before_fix(tmp_path):
    old = (SCRIPT.parents[2] / "tests/fixtures/blog-producer-before-contract.sh").read_text()
    current = SCRIPT.read_text()
    outcomes = []
    for source in (old, current):
        functions = source.split("run_claude_producer() {", 1)[1].split("\nPRODUCER_HEAD=", 1)[0]
        harness = f"""
set -uo pipefail
LOG={tmp_path / "run.log"}
YESTERDAY=2026-09-15
TIMEOUT_SECS=2700
BLOG_DIR={tmp_path}
PRODUCER_GUARD_DIR={tmp_path}
PRODUCER_STATUS=NOT-RUN
log() {{ printf '%s\\n' "$*"; }}
env() {{ return 0; }}
verify_producer_contract() {{ PRODUCER_STATUS="FAILED (missing artifacts)"; return 1; }}
run_claude_producer() {{{functions}
run_claude_producer
printf 'RESULT:%s STATUS:%s\\n' "$?" "$PRODUCER_STATUS"
"""
        outcomes.append(
            subprocess.run(
                ["bash", "-c", harness], text=True, capture_output=True, check=True
            ).stdout
        )
    assert "RESULT:0 STATUS:OK" in outcomes[0]
    assert "RESULT:1 STATUS:FAILED" in outcomes[1]


@pytest.mark.parametrize("canary", ["0", "1"])
def test_canary_heartbeat_isolation_preserves_normal_scheduler_signal(tmp_path, canary):
    marker = "# Liveness heartbeat:"
    current = marker + SCRIPT.read_text().split(marker, 1)[1].split(
        "\nEMAIL_SCRIPT=", 1
    )[0]
    fixture = SCRIPT.parents[2] / "tests/fixtures/blog-canary-heartbeat-before-isolation.sh"
    old = fixture.read_text()
    outcomes = []
    for index, source in enumerate((old, current)):
        home = tmp_path / str(index)
        home.mkdir()
        subprocess.run(
            ["bash", "-c", source],
            env={"HOME": str(home), "PATH": "/usr/bin:/bin", "BLOG_CANARY": canary},
            check=True,
        )
        beat = home / ".local/state/intent-os/liveness/blog-backfill-daily.beat"
        outcomes.append(beat.exists())
    assert outcomes[0] is True
    assert outcomes[1] is (canary == "0")
