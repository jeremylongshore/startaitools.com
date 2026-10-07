"""Per-run cost of the bounded search-phrasing step: tokens, wall time and tool calls.

Blog Recovery Phase I, E03-T05 (startaitools-9a8.3.5, governing contract intent-os
000-docs/228 S07/S08). The search-phrasing step (blogpipe/phrasing.py) stays OFF unless
BLOG_SEARCH_PHRASING=1, and it may only expand after its cost is known. This module
measures that cost from evidence the producer cannot edit: the research step runs as one
subagent whose description starts with "search phrasing", and Claude Code writes that
subagent's own transcript next to the producer's (`<session>/subagents/agent-*.jsonl`
plus a `.meta.json` carrying the description).

From that transcript it counts, per run:

- assistant turns and tokens (input, cache creation, cache read, output), each API
  message counted once: the transcript repeats it per content block, with the input
  counts repeated and output_tokens growing, so each field keeps its maximum;
- tool calls by tool name, and `web_calls` = WebSearch + WebFetch (the step's budget is 6);
- wall seconds from the first to the last transcript timestamp.

`python3 -B -m blogpipe search-phrasing-cost` prints one JSON object and, with --ledger,
appends it to an append-only JSONL budget ledger (one row per run and subagent, never
duplicated). The daily wrapper calls it only when BLOG_SEARCH_PHRASING=1. Like the step
itself it never fails a run: every content outcome exits 0, only a usage error exits 64.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from collections import Counter
from pathlib import Path
from typing import Any

SCHEMA = "search-phrasing-cost/v1"
MARKER = "search phrasing"
WEB_TOOLS = ("WebSearch", "WebFetch")
TOKEN_KEYS = (
    "input_tokens",
    "cache_creation_input_tokens",
    "cache_read_input_tokens",
    "output_tokens",
)


def _ts(value: Any) -> dt.datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def measure(path: Path) -> dict[str, Any]:
    """Cost of one subagent transcript. Unreadable lines are skipped, never fatal."""
    per_message: dict[str, dict[str, int]] = {}
    tools: Counter[str] = Counter()
    seen_tools: set[str] = set()
    stamps: list[dt.datetime] = []
    model = None
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(entry, dict):
                continue
            stamp = _ts(entry.get("timestamp"))
            if stamp:
                stamps.append(stamp)
            message = entry.get("message")
            if entry.get("type") != "assistant" or not isinstance(message, dict):
                continue
            key = message.get("id") or entry.get("uuid") or str(len(per_message))
            usage = message.get("usage")
            if isinstance(usage, dict):
                # One API message is written as several lines (one per content block);
                # the input counts repeat and output_tokens grows, so keep the maximum.
                seen = per_message.setdefault(key, dict.fromkeys(TOKEN_KEYS, 0))
                model = message.get("model") or model
                for name in TOKEN_KEYS:
                    value = usage.get(name)
                    if type(value) is int and value > seen[name]:
                        seen[name] = value
            for block in message.get("content") or []:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    ident = block.get("id") or f"{key}:{len(seen_tools)}"
                    if ident not in seen_tools:
                        seen_tools.add(ident)
                        tools[str(block.get("name"))] += 1
    wall = (max(stamps) - min(stamps)).total_seconds() if len(stamps) > 1 else 0.0
    tokens = {name: sum(m[name] for m in per_message.values()) for name in TOKEN_KEYS}
    turns = len(per_message)
    return {
        "schema": SCHEMA,
        "measured": True,
        "turns": turns,
        **tokens,
        "total_tokens": sum(tokens.values()),
        "tool_calls": dict(sorted(tools.items())),
        "web_calls": sum(tools[name] for name in WEB_TOOLS),
        "wall_seconds": round(wall, 1),
        "model": model,
    }


def find_subagents(transcript: Path, marker: str = MARKER) -> list[Path]:
    """Subagent transcripts of this producer session whose description starts with marker."""
    folder = transcript.with_suffix("") / "subagents"
    found = []
    for meta in sorted(folder.glob("agent-*.meta.json")):
        try:
            description = json.loads(meta.read_text(encoding="utf-8")).get("description")
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, AttributeError):
            continue
        if isinstance(description, str) and description.strip().lower().startswith(marker):
            log = meta.with_name(meta.name.replace(".meta.json", ".jsonl"))
            if log.is_file():
                found.append(log)
    return found


def not_measured(reason: str) -> dict[str, Any]:
    return {"schema": SCHEMA, "measured": False, "reason": reason}


def append_ledger(ledger: Path, row: dict[str, Any]) -> bool:
    """Append once per (run_id, subagent); True when a row was written."""
    key = (row.get("run_id"), row.get("subagent"))
    if ledger.exists():
        for line in ledger.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                old = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(old, dict) and (old.get("run_id"), old.get("subagent")) == key:
                return False
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True) + "\n")
    return True


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python3 -B -m blogpipe search-phrasing-cost",
        description="Measure the search-phrasing subagent's tokens, time and tool calls. "
        "Exits 0 on every content outcome.",
    )
    source = ap.add_mutually_exclusive_group(required=True)
    source.add_argument("--transcript", help="the producer session transcript (JSONL)")
    source.add_argument("--subagent", help="one subagent transcript (JSONL), measured directly")
    ap.add_argument("--date")
    ap.add_argument("--run-id")
    ap.add_argument("--label", help="free-text arm label for comparisons (e.g. plain, skill)")
    ap.add_argument("--ledger", help="append-only JSONL budget ledger")
    try:
        args = ap.parse_args(argv)
    except SystemExit as exc:
        return 64 if exc.code else 0
    if args.subagent:
        logs = [Path(args.subagent)] if Path(args.subagent).is_file() else []
    else:
        transcript = Path(args.transcript)
        logs = find_subagents(transcript) if transcript.is_file() else []
    rows = []
    if not logs:
        rows.append(not_measured("no search-phrasing subagent transcript found"))
    for log in logs:
        try:
            row = measure(log)
        except OSError as exc:
            row = not_measured(f"{type(exc).__name__}: {exc}"[:200])
        row["subagent"] = log.stem
        rows.append(row)
    for row in rows:
        row.update({k: v for k, v in (("date", args.date), ("run_id", args.run_id),
                                      ("label", args.label)) if v})
        if args.ledger and row.get("measured"):
            row["ledger"] = "appended" if append_ledger(Path(args.ledger), row) else "present"
        print(json.dumps(row, sort_keys=True))
    return 0
