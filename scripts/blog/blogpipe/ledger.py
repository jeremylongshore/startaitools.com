"""Classifier tier vs shipped tier: the lander's append and the calibration ledger.

E07-T02 (startaitools.com#127). Until now decisions.jsonl recorded only the tier the
classifier chose. When the lander's length gate shipped a lower tier, that fact lived
only in feedback.jsonl, so every distribution computed from decisions alone overstated
shipped Tier 2 (September 2026: classifier 20/9/1, shipped 23/6/1).

- `shipped-tier` (called by blog-land.sh when the gate downgrades) APPENDS one
  `record_type: "shipped_tier"` record. History is never rewritten; a record equal to
  the latest one for its date/slug is a no-op, so a re-entered lander cannot
  double-count a downgrade. `--regate-cleared` (gate did not fire on a re-land of a
  retained workspace) appends a superseding record only if the latest one was a
  downgrade; readers take the latest per (date, slug).
- `tier-ledger` prints both distributions for a window, selecting decisions by
  record_type (with the historical fallback) and reading pre-E07 downgrades from the
  lander's feedback rows. /blog-calibrate starts from this instead of grepping JSONL.
"""

from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import json
import os
import sys
from pathlib import Path

from .jsonio import records
from .records import (
    LENGTH_GATE,
    REGATE_CLEARED,
    distribution,
    duplicate_classifiers,
    latest_shipped,
    shipped_record,
    tier_ledger,
)

METHODOLOGY = Path(".claude/skills/blog-backfill/methodology")


def append_shipped(path: Path, record: dict) -> bool:
    """Append `record`; False (no write) when it equals the latest for its date/slug."""
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"{path.name} must be an existing regular file")
    encoded = json.dumps(record, sort_keys=True, allow_nan=False) + "\n"
    descriptor = os.open(path, os.O_RDWR | os.O_APPEND | os.O_NOFOLLOW)
    with os.fdopen(descriptor, "a+") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        handle.seek(0)
        existing = handle.read()
        # Idempotent against the LATEST record for this (date, slug) only: a downgrade,
        # a regate-cleared and the same downgrade again must still read as downgraded.
        rows = [json.loads(line) for line in existing.splitlines() if line.strip()]
        key = (record["date"], record["slug"])
        if latest_shipped(rows).get(key) == record:
            return False
        if existing and not existing.endswith("\n"):
            raise ValueError(f"{path.name} lacks a final newline; refusing an ambiguous append")
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())
    return True


def append_main() -> int:
    parser = argparse.ArgumentParser(description="Record a length-gate tier downgrade")
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--source-run", default="")
    parser.add_argument("--classifier-tier", type=int, required=True)
    parser.add_argument("--shipped-tier", type=int, required=True)
    parser.add_argument("--body-lines", type=int, required=True)
    parser.add_argument("--tier1-max-lines", type=int, required=True)
    parser.add_argument("--tier2-max-lines", type=int, required=True)
    parser.add_argument(
        "--regate-cleared",
        action="store_true",
        help="the gate did not fire on this landing: supersede an earlier downgrade, if any",
    )
    args = parser.parse_args()
    try:
        dt.date.fromisoformat(args.date)
        reason = REGATE_CLEARED if args.regate_cleared else LENGTH_GATE
        if args.regate_cleared:
            prior = latest_shipped(records(args.decisions)).get((args.date, args.slug))
            if prior is None or prior.get("shipped_tier") == prior.get("classifier_tier"):
                return 0  # nothing to supersede: the common case, silent
        record = shipped_record(
            date=args.date,
            slug=args.slug,
            run_id=args.run_id,
            source_run=args.source_run,
            classifier_tier=args.classifier_tier,
            shipped_tier=args.shipped_tier,
            body_lines=args.body_lines,
            tier1_max_lines=args.tier1_max_lines,
            tier2_max_lines=args.tier2_max_lines,
            reason=reason,
        )
        written = append_shipped(args.decisions, record)
    except (OSError, ValueError) as exc:
        print(f"SHIPPED-TIER: FAILED: {exc}", file=sys.stderr)
        return 65
    state = ("recorded" if written else "already recorded") + f" ({reason})"
    print(
        f"SHIPPED-TIER: {state}: {args.slug} classifier tier {args.classifier_tier}, "
        f"shipped tier {args.shipped_tier}"
    )
    return 0


def month_window(month: str) -> tuple[str, str]:
    first = dt.date.fromisoformat(f"{month}-01")
    following = (first.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
    return first.isoformat(), following.isoformat()


def main() -> int:
    parser = argparse.ArgumentParser(description="Classifier vs shipped tier for a window")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--decisions", type=Path)
    parser.add_argument("--feedback", type=Path)
    window = parser.add_mutually_exclusive_group(required=True)
    window.add_argument("--month", help="YYYY-MM")
    window.add_argument("--start", help="YYYY-MM-DD (inclusive; needs --end)")
    parser.add_argument("--end", help="YYYY-MM-DD (exclusive)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        start, end = month_window(args.month) if args.month else (args.start, args.end)
        if not end:
            raise ValueError("--start requires --end")
        decisions = args.decisions or args.repo / METHODOLOGY / "decisions.jsonl"
        feedback = args.feedback or args.repo / METHODOLOGY / "feedback.jsonl"
        rows = tier_ledger(
            records(decisions),
            records(feedback) if feedback.is_file() else [],
            start=start,
            end=end,
        )
    except (OSError, ValueError) as exc:
        print(f"TIER-LEDGER: FAILED: {exc}", file=sys.stderr)
        return 65
    duplicates = duplicate_classifiers(records(decisions), start=start, end=end)
    summary = {
        "window": [start, end],
        "duplicate_classifiers": duplicates,
        "decisions": len(rows),
        "classifier": distribution(rows, "classifier_tier"),
        "shipped": distribution(rows, "shipped_tier"),
        "rows": rows,
    }
    if args.json:
        print(json.dumps(summary, indent=2))
        return 0
    print(f"tier-ledger [{start}, {end}): {len(rows)} classifier decisions")
    print("classifier T1/T2/T3: {}/{}/{}".format(*summary["classifier"]))
    print("shipped    T1/T2/T3: {}/{}/{}".format(*summary["shipped"]))
    for slug, count in duplicates.items():
        print(f"  WARN duplicate classifier decisions: {slug} x{count} (ledger counts the last)")
    for row in rows:
        if row["shipped_tier"] != row["classifier_tier"]:
            print(
                f"  downgraded {row['date']} {row['slug']}: T{row['classifier_tier']} -> "
                f"T{row['shipped_tier']} ({row['shipped_source']})"
            )
        if row["recovered"]:
            print(f"  recovered from quarantine {row['date']} {row['slug']}")
    return 0
