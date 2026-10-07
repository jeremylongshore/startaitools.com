"""E03-T05 (startaitools-9a8.3.5): per-run cost of the bounded search-phrasing step."""

import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts/blog"
sys.path.insert(0, str(SCRIPTS))
cost = importlib.import_module("blogpipe.phrasing_cost")


def assistant(msg_id, ts, usage, blocks):
    return {
        "type": "assistant",
        "timestamp": ts,
        "message": {"id": msg_id, "model": "m-1", "usage": usage, "content": blocks},
    }


def tool(ident, name):
    return {"type": "tool_use", "id": ident, "name": name, "input": {}}


USAGE_1 = {"input_tokens": 10, "cache_creation_input_tokens": 1000,
           "cache_read_input_tokens": 0, "output_tokens": 50}
USAGE_2 = {"input_tokens": 5, "cache_creation_input_tokens": 0,
           "cache_read_input_tokens": 1200, "output_tokens": 80}
LINES = [
    {"type": "user", "timestamp": "2026-10-06T10:00:00.000Z", "message": {"content": "brief"}},
    # One API message split over two lines (one per content block), same usage repeated.
    assistant("msg_1", "2026-10-06T10:00:05.000Z", USAGE_1, [{"type": "text", "text": "x"}]),
    assistant("msg_1", "2026-10-06T10:00:05.100Z", {**USAGE_1, "output_tokens": 90},
              [tool("t1", "WebSearch")]),
    {"type": "user", "timestamp": "2026-10-06T10:00:09.000Z", "message": {"content": "r"}},
    assistant("msg_2", "2026-10-06T10:00:20.000Z", USAGE_2,
              [tool("t2", "WebSearch"), tool("t3", "WebFetch"), tool("t4", "Write")]),
    "not json at all",
]


def write_session(tmp_path, description="search phrasing 2026-10-05"):
    tmp_path.mkdir(parents=True, exist_ok=True)
    transcript = tmp_path / "session.jsonl"
    transcript.write_text("{}\n")
    sub = tmp_path / "session" / "subagents"
    sub.mkdir(parents=True)
    log = sub / "agent-abc.jsonl"
    log.write_text("".join((x if isinstance(x, str) else json.dumps(x)) + "\n" for x in LINES))
    (sub / "agent-abc.meta.json").write_text(json.dumps({"description": description}))
    other = sub / "agent-zzz.jsonl"
    other.write_text(json.dumps(assistant("w", "2026-10-06T11:00:00Z", USAGE_1, [])) + "\n")
    (sub / "agent-zzz.meta.json").write_text(json.dumps({"description": "Write the post"}))
    return transcript, log


def test_measure_counts_each_api_message_once_and_every_tool_call(tmp_path):
    _, log = write_session(tmp_path)
    row = cost.measure(log)
    assert row["turns"] == 2
    # msg_1's output grows 50 -> 90 across its two lines; the maximum is the message's.
    assert row["input_tokens"] == 15 and row["output_tokens"] == 90 + 80
    assert row["cache_creation_input_tokens"] == 1000 and row["cache_read_input_tokens"] == 1200
    assert row["total_tokens"] == 15 + 170 + 1000 + 1200
    assert row["tool_calls"] == {"WebFetch": 1, "WebSearch": 2, "Write": 1}
    assert row["web_calls"] == 3
    assert row["wall_seconds"] == 20.0
    assert row["model"] == "m-1" and row["measured"] is True


def test_only_the_marked_subagent_is_measured(tmp_path):
    transcript, log = write_session(tmp_path)
    assert cost.find_subagents(transcript) == [log]
    transcript2, _ = write_session(tmp_path / "b", description="Outsider test")
    assert cost.find_subagents(transcript2) == []


def run(*args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("BLOG_")}
    return subprocess.run(
        [sys.executable, "-B", "-m", "blogpipe", "search-phrasing-cost", *args],
        cwd=SCRIPTS, capture_output=True, text=True, env=env, timeout=60,
    )


def test_cli_appends_one_ledger_row_per_run_and_never_duplicates(tmp_path):
    transcript, _ = write_session(tmp_path)
    ledger = tmp_path / "ledger.jsonl"
    args = ("--transcript", str(transcript), "--date", "2026-10-05", "--run-id", "r1",
            "--ledger", str(ledger))
    first = run(*args)
    assert first.returncode == 0, first.stderr
    row = json.loads(first.stdout)
    assert row["ledger"] == "appended" and row["web_calls"] == 3 and row["run_id"] == "r1"
    again = run(*args)
    assert json.loads(again.stdout)["ledger"] == "present"
    rows = [json.loads(x) for x in ledger.read_text().splitlines()]
    assert len(rows) == 1 and rows[0]["subagent"] == "agent-abc" and "ledger" not in rows[0]


def test_cli_without_a_subagent_reports_not_measured_and_exits_0(tmp_path):
    missing = run("--transcript", str(tmp_path / "nope.jsonl"), "--ledger",
                  str(tmp_path / "l.jsonl"))
    assert missing.returncode == 0
    assert json.loads(missing.stdout) == {
        "schema": "search-phrasing-cost/v1", "measured": False,
        "reason": "no search-phrasing subagent transcript found",
    }
    assert not (tmp_path / "l.jsonl").exists()


def test_cli_measures_a_subagent_directly_with_an_arm_label(tmp_path):
    _, log = write_session(tmp_path)
    out = run("--subagent", str(log), "--label", "plain")
    assert out.returncode == 0 and json.loads(out.stdout)["label"] == "plain"


def test_cli_usage_error_exits_64():
    assert run().returncode == 64


def test_wrapper_records_cost_only_when_the_step_is_on():
    text = (SCRIPTS / "blog-backfill-daily.sh").read_text()
    block = text.split('if [ "${BLOG_SEARCH_PHRASING:-0}" = "1" ] && [ -n "$transcript" ]', 1)[1]
    block = block.split("\n  fi\n", 1)[0]
    assert "search-phrasing-cost --transcript" in block
    assert '--ledger "$LOG_DIR/search-phrasing-cost.jsonl"' in block
