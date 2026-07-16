#!/usr/bin/env python3
"""next-topics.py: deterministic manager for the analytics-driven topic queue.

Thread D Phase 1 (2026-07-16), the front-of-funnel performance loop:
  Umami content-performance  ->  content-seo agent (LLM)  ->  THIS queue  ->  writers

The LLM half only PRODUCES candidate objects into a staging file. This script is
the deterministic half: it validates, assigns ids, dedups, ranks by score, and
appends to the real queue, so a bad model run can never corrupt it (same
produce/land split the blog pipeline uses everywhere else).

Queue file: .next-topics.jsonl at the repo root (gitignored, transient). Each
line is one candidate:
  {
    "id": "nt-YYYYMMDD-NNN",        # assigned on ingest
    "generated_at": "ISO8601",       # assigned on ingest
    "topic": "short human title",    # required
    "slug_hint": "kebab-slug",       # required, the dedup key
    "angle": "the specific thesis / angle",
    "rationale": "why now, grounded in real traffic numbers",
    "source_signals": { ... },       # top performers / gap / cluster that drove it
    "score": 0.0-1.0,                # required, ranking priority
    "target_tier": 1-4,              # suggested tier (4 => blog-research-article)
    "status": "open",                # open | consumed
    "consumed_by": null,             # post slug, once written
    "consumed_at": null
  }

Subcommands:
  ingest [--staging PATH]   validate staged candidates, dedup vs open items, append
  top [--tier N] [--json]   print the single highest-score OPEN candidate
  list [--all]              list open (or all) candidates, ranked
  consume <id|slug> --by S  mark an item consumed by post slug S
  validate                  validate the whole queue, non-zero exit on any bad line

Never corrupts the queue: ingest writes atomically (temp + replace). Read paths
never raise on a missing queue (they treat it as empty).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent  # scripts/blog/ -> repo root
QUEUE = REPO / ".next-topics.jsonl"
STAGING = REPO / ".next-topics.staging.jsonl"

REQUIRED = ("topic", "slug_hint", "score")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")


def _read(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as e:
            raise ValueError(f"{path.name}:{i}: invalid JSON ({e})") from e
    return out


def _write_atomic(path: Path, rows: list[dict]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def _valid_candidate(c: dict) -> str | None:
    for k in REQUIRED:
        if k not in c or c[k] in (None, ""):
            return f"missing required field '{k}'"
    try:
        s = float(c["score"])
    except (TypeError, ValueError):
        return "score is not a number"
    if not 0.0 <= s <= 1.0:
        return "score out of range 0.0-1.0"
    return None


def cmd_ingest(args) -> int:
    staging = Path(args.staging) if args.staging else STAGING
    try:
        staged = _read(staging)
    except ValueError as e:
        print(f"ingest: {e}", file=sys.stderr)
        return 1
    if not staged:
        print("ingest: no staged candidates (nothing to do)")
        return 0

    existing = _read(QUEUE)
    open_slugs = {_slug(r.get("slug_hint", "")) for r in existing if r.get("status") == "open"}

    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    seq = 1 + sum(1 for r in existing if r.get("id", "").startswith(f"nt-{today}-"))

    added, skipped = [], []
    for c in staged:
        err = _valid_candidate(c)
        if err:
            skipped.append((c.get("topic", "?"), err))
            continue
        sl = _slug(c["slug_hint"])
        if sl in open_slugs:
            skipped.append((c.get("topic", "?"), "duplicate of an open item"))
            continue
        rec = {
            "id": f"nt-{today}-{seq:03d}",
            "generated_at": _now(),
            "topic": c["topic"],
            "slug_hint": sl,
            "angle": c.get("angle", ""),
            "rationale": c.get("rationale", ""),
            "source_signals": c.get("source_signals", {}),
            "score": round(float(c["score"]), 3),
            "target_tier": int(c.get("target_tier", 2)),
            "status": "open",
            "consumed_by": None,
            "consumed_at": None,
        }
        existing.append(rec)
        open_slugs.add(sl)
        added.append(rec)
        seq += 1

    if added:
        _write_atomic(QUEUE, existing)
    if not args.keep_staging:
        staging.unlink(missing_ok=True)

    print(f"ingest: added {len(added)}, skipped {len(skipped)}")
    for topic, why in skipped:
        print(f"  skipped: {topic!r} ({why})")
    return 0


def _open_ranked(rows: list[dict], tier: int | None = None) -> list[dict]:
    items = [r for r in rows if r.get("status") == "open"]
    if tier is not None:
        items = [r for r in items if int(r.get("target_tier", 2)) == tier]
    return sorted(items, key=lambda r: float(r.get("score", 0)), reverse=True)


def cmd_top(args) -> int:
    ranked = _open_ranked(_read(QUEUE), args.tier)
    if not ranked:
        print("", end="") if args.json else print("(no open topics in the queue)")
        return 0 if not args.json else 3
    top = ranked[0]
    if args.json:
        json.dump(top, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        print(f"{top['id']}  [score {top['score']}  tier {top['target_tier']}]  {top['topic']}")
        print(f"  slug: {top['slug_hint']}")
        print(f"  angle: {top.get('angle','')}")
        print(f"  why: {top.get('rationale','')}")
    return 0


def cmd_list(args) -> int:
    rows = _read(QUEUE)
    items = rows if args.all else [r for r in rows if r.get("status") == "open"]
    items = sorted(items, key=lambda r: float(r.get("score", 0)), reverse=True)
    if not items:
        print("(queue empty)")
        return 0
    for r in items:
        mark = r.get("status", "open")
        print(f"{r.get('id','?')}  [{r.get('score','?')} t{r.get('target_tier','?')} {mark}]  {r.get('topic','?')}")
    return 0


def cmd_consume(args) -> int:
    rows = _read(QUEUE)
    key = args.item
    keyslug = _slug(key)
    hit = None
    for r in rows:
        if r.get("id") == key or _slug(r.get("slug_hint", "")) == keyslug:
            hit = r
            break
    if not hit:
        print(f"consume: no queue item matching {key!r}", file=sys.stderr)
        return 1
    if hit.get("status") == "consumed":
        print(f"consume: {hit['id']} already consumed by {hit.get('consumed_by')}")
        return 0
    hit["status"] = "consumed"
    hit["consumed_by"] = args.by
    hit["consumed_at"] = _now()
    _write_atomic(QUEUE, rows)
    print(f"consume: {hit['id']} -> consumed by {args.by}")
    return 0


def cmd_validate(args) -> int:
    try:
        rows = _read(QUEUE)
    except ValueError as e:
        print(f"validate: {e}", file=sys.stderr)
        return 1
    bad = 0
    for r in rows:
        err = _valid_candidate(r)
        if err:
            print(f"validate: {r.get('id','?')}: {err}", file=sys.stderr)
            bad += 1
    n_open = sum(1 for r in rows if r.get("status") == "open")
    print(f"validate: {len(rows)} items ({n_open} open), {bad} invalid")
    return 1 if bad else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    i = sub.add_parser("ingest", help="validate + dedup + append staged candidates")
    i.add_argument("--staging", help="staging JSONL path (default .next-topics.staging.jsonl)")
    i.add_argument("--keep-staging", action="store_true", help="do not delete staging after ingest")
    i.set_defaults(func=cmd_ingest)

    t = sub.add_parser("top", help="print the highest-score open candidate")
    t.add_argument("--tier", type=int, help="restrict to a target_tier")
    t.add_argument("--json", action="store_true", help="emit the full JSON object")
    t.set_defaults(func=cmd_top)

    l = sub.add_parser("list", help="list ranked candidates")
    l.add_argument("--all", action="store_true", help="include consumed items")
    l.set_defaults(func=cmd_list)

    c = sub.add_parser("consume", help="mark an item consumed")
    c.add_argument("item", help="queue id or slug_hint")
    c.add_argument("--by", required=True, help="the post slug that consumed it")
    c.set_defaults(func=cmd_consume)

    v = sub.add_parser("validate", help="validate the whole queue")
    v.set_defaults(func=cmd_validate)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
