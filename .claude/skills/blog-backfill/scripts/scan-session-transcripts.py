#!/usr/bin/env python3
"""Scan Claude Code session transcripts for blog-backfill material.

Reads JSONL session files from ~/.claude/projects/*/*.jsonl, filters by date
range, extracts user/assistant text exchanges, groups by project and day.

Output is a condensed summary suitable for feeding into the blog-backfill
pipeline as additional source material alongside git logs, PRs, and beads.

WARNING: Session transcripts may contain sensitive data (.env contents, API
keys, credentials) that appeared during debugging. Output is for internal
use only — do not publish raw scanner output.

Usage:
    python3 scan-session-transcripts.py --start 2026-04-01 --end 2026-04-02
    python3 scan-session-transcripts.py --start 2026-04-01 --end 2026-04-02 \\
        --output /tmp/sessions.txt
    python3 scan-session-transcripts.py --start 2026-04-01  # single day (end defaults to start+1)
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

PROJECTS_DIR = Path.home() / ".claude" / "projects"

# Max chars of assistant text to include per message (avoid dumping 10MB agent results)
MAX_ASSISTANT_CHARS = 500

# Entry types to skip entirely
SKIP_TYPES = frozenset({
    "permission-mode",
    "file-history-snapshot",
    "custom-title",
    "progress",
    "agent-name",
    "attachment",
    "system",
})


def parse_date(s: str) -> datetime:
    """Parse YYYY-MM-DD date string."""
    return datetime.strptime(s, "%Y-%m-%d")


def project_name_from_dir(dirname: str) -> str:
    """Convert directory name to readable project name.

    e.g. '-home-jeremy-000-projects-irsb-monorepo' -> 'irsb-monorepo'
         '-home-jeremy-000-projects-blog-startaitools' -> 'blog-startaitools'
         '-home-jeremy' -> 'home'
    """
    # Strip leading dash
    name = dirname.lstrip("-")
    # Remove common prefixes
    for prefix in ("home-jeremy-000-projects-", "home-jeremy-"):
        if name.startswith(prefix):
            name = name[len(prefix):]
            break
    # Strip worktree suffixes (e.g. --claude-worktrees-sorted-imagining-raccoon)
    if "--claude-worktrees" in name:
        name = name.split("--claude-worktrees")[0]
    return name or dirname


def extract_text_from_content(content, role: str) -> str | None:
    """Extract plain text from message content blocks.

    For user messages: skip tool_result blocks (too verbose).
    For assistant messages: skip thinking and tool_use blocks.
    """
    if isinstance(content, str):
        return content.strip() or None

    if not isinstance(content, list):
        return None

    texts = []
    for block in content:
        if not isinstance(block, dict):
            continue
        block_type = block.get("type", "")

        if role == "user":
            # Only include text blocks from user, skip tool_result
            if block_type == "text":
                t = block.get("text", "").strip()
                if t:
                    texts.append(t)
        elif role == "assistant":
            # Only include text blocks, skip thinking and tool_use
            if block_type == "text":
                t = block.get("text", "").strip()
                if t:
                    texts.append(t)

    return "\n".join(texts) if texts else None


def scan_jsonl_file(
    filepath: Path,
    start_ts: datetime,
    end_ts: datetime,
) -> list[dict]:
    """Stream-read a JSONL file, extract relevant entries in date range.

    Returns list of dicts: {timestamp, role, text, is_sidechain}
    """
    entries = []
    try:
        with open(filepath, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue

                entry_type = obj.get("type", "")

                # Skip non-message types
                if entry_type in SKIP_TYPES:
                    continue

                # Must have a timestamp
                ts_str = obj.get("timestamp")
                if not ts_str:
                    continue

                # Parse timestamp (ISO-8601, may have Z or offset)
                try:
                    # Strip timezone for naive comparison (all timestamps are UTC)
                    ts_clean = ts_str.replace("Z", "+00:00")
                    ts = datetime.fromisoformat(ts_clean).replace(tzinfo=None)
                except (ValueError, TypeError):
                    continue

                # Filter by date range
                if ts < start_ts or ts >= end_ts:
                    continue

                # Only process user and assistant messages
                if entry_type not in ("user", "assistant"):
                    continue

                msg = obj.get("message", {})
                if not isinstance(msg, dict):
                    continue

                role = msg.get("role", entry_type)
                content = msg.get("content", "")
                text = extract_text_from_content(content, role)

                if not text:
                    continue

                # Truncate long assistant responses
                if role == "assistant" and len(text) > MAX_ASSISTANT_CHARS:
                    text = text[:MAX_ASSISTANT_CHARS] + "..."

                entries.append({
                    "timestamp": ts,
                    "role": role,
                    "text": text,
                    "is_sidechain": obj.get("isSidechain", False),
                })

    except (OSError, PermissionError) as e:
        print(f"  [WARN] Could not read {filepath}: {e}", file=sys.stderr)

    return entries


def scan_all_projects(start_ts: datetime, end_ts: datetime) -> dict:
    """Scan all project directories, return {project_name: {date_str: [entries]}}."""
    results = defaultdict(lambda: defaultdict(list))

    if not PROJECTS_DIR.exists():
        print(f"Projects directory not found: {PROJECTS_DIR}", file=sys.stderr)
        return results

    for project_dir in sorted(PROJECTS_DIR.iterdir()):
        if not project_dir.is_dir():
            continue

        project_name = project_name_from_dir(project_dir.name)

        # Find all JSONL files in this project directory
        jsonl_files = sorted(project_dir.glob("*.jsonl"))
        if not jsonl_files:
            continue

        for jf in jsonl_files:
            entries = scan_jsonl_file(jf, start_ts, end_ts)
            for entry in entries:
                date_str = entry["timestamp"].strftime("%Y-%m-%d")
                results[project_name][date_str].append(entry)

    return results


def format_output(results: dict) -> str:
    """Format results into readable output."""
    lines = []

    if not results:
        lines.append("No session activity found in the given date range.")
        return "\n".join(lines)

    for project_name in sorted(results.keys()):
        dates = results[project_name]
        for date_str in sorted(dates.keys()):
            entries = sorted(dates[date_str], key=lambda e: e["timestamp"])

            # Count sessions (gaps > 30 min = new session)
            session_count = 1
            for i in range(1, len(entries)):
                gap = (entries[i]["timestamp"] - entries[i - 1]["timestamp"]).total_seconds()
                if gap > 1800:
                    session_count += 1

            lines.append(f"=== PROJECT: {project_name} ({date_str}) ===")
            lines.append(f"Sessions: ~{session_count} | Messages: {len(entries)}")
            lines.append("")

            for entry in entries:
                ts = entry["timestamp"].strftime("%H:%M")
                role = entry["role"].capitalize()
                sidechain = " [background]" if entry.get("is_sidechain") else ""
                text = entry["text"]

                # Indent multi-line text
                text_lines = text.split("\n")
                if len(text_lines) > 1:
                    indented = text_lines[0] + "\n" + "\n".join(
                        "  " + tl for tl in text_lines[1:]
                    )
                    lines.append(f"[{ts}] {role}{sidechain}: {indented}")
                else:
                    lines.append(f"[{ts}] {role}{sidechain}: {text}")
                lines.append("")

            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Scan Claude Code session transcripts for blog-backfill material."
    )
    parser.add_argument(
        "--start",
        required=True,
        help="Start date (YYYY-MM-DD, inclusive)",
    )
    parser.add_argument(
        "--end",
        default=None,
        help="End date (YYYY-MM-DD, exclusive). Defaults to start + 1 day.",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output file path. Defaults to stdout.",
    )
    parser.add_argument(
        "--project", "-p",
        default=None,
        help="Filter to a single project name (substring match).",
    )

    args = parser.parse_args()

    start_ts = parse_date(args.start)
    if args.end:
        end_ts = parse_date(args.end)
    else:
        end_ts = start_ts + timedelta(days=1)

    print(
        f"Scanning sessions: {start_ts.date()} to {end_ts.date()} "
        f"(~{(end_ts - start_ts).days} day(s))",
        file=sys.stderr,
    )

    results = scan_all_projects(start_ts, end_ts)

    # Filter by project if requested
    if args.project:
        filtered = {}
        for name, dates in results.items():
            if args.project.lower() in name.lower():
                filtered[name] = dates
        results = filtered

    output = format_output(results)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Output written to: {args.output}", file=sys.stderr)
    else:
        print(output)

    # Summary stats
    total_projects = len(results)
    total_messages = sum(
        len(entries)
        for dates in results.values()
        for entries in dates.values()
    )
    print(
        f"Summary: {total_projects} project(s), {total_messages} message(s)",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
