"""Exercise actual wrapper functions without invoking a provider or publishing."""
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/blog/blog-backfill-daily.sh"


@pytest.mark.parametrize(("producer", "status", "expected"), [
    ("claude", 1, "claude exit 1"),
    ("claude", 124, "claude timeout exit 124"),
    ("grok", 42, "grok exit 42"),
    ("minimax", 2, "minimax max-turns"),
    ("minimax", 3, "minimax timeout"),
    ("minimax", 124, "minimax timeout"),
])
def test_producer_preserves_failure_exit(producer, status, expected, tmp_path):
    source = SCRIPT.read_text()
    functions = source.split("run_claude_producer() {", 1)[1].split("\nPRODUCER_HEAD=", 1)[0]
    harness = f"""
set -uo pipefail
LOG={tmp_path / 'run.log'}
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
    branch = source.split('  auto|*)\n', 1)[1].split('\nesac', 1)[0]
    output = subprocess.run(['bash', '-c', '''
run_claude_producer() { echo primary-failed; return 69; }
run_minimax_producer() { echo unsafe-fallback; }
run_grok_producer() { echo unsafe-fallback; }
case auto in
  auto|*)
''' + branch + '\nesac'], capture_output=True, text=True, check=True)
    assert output.stdout.strip() == 'primary-failed'
