#!/usr/bin/env python3
"""syndication-reconcile.py: age `pending` syndication rows into `assumed_posted`.

WHY THIS EXISTS
---------------
`.blog-syndication-ledger.json` carries a per-post `syndication` block with one
row per surface (x, li_personal, li_company, substack, medium). `blog-land.sh`
writes every row as `pending` when the post lands, and **nothing has ever written
to it again**. Ezekiel posts manually from the emailed packet; there is no reply
path, no webhook, no confirmation step. As of 2026-08-11 all 195 rows across 39
posts were `pending`.

`pending` therefore never meant "he did not post." It meant "nobody has ever told
this file anything." The weekly team rollup read it as the former and reported a
38-post backlog to the whole team, which was an accusation manufactured out of a
field with no writer. Same defect as the backup coverage manifest that had no word
for "verified, there is none": a vocabulary that cannot distinguish a work gap
from a data gap will eventually report one as the other.

THE STATE MACHINE
-----------------
    pending          packet sent, nothing known yet
    assumed_posted   aged past the window with no contrary report. Owner standing
                     instruction 2026-08-11: "assume he has posted unless I tell
                     you otherwise". Carries provenance, NOT a fabricated receipt.
    not_posted       the owner said so explicitly (--mark-missed)
    posted           a real receipt exists (URL + timestamp). Only the future
                     reply-ingester writes this. This script never does.
    n/a              surface does not apply to this post's tier

The distinction between `assumed_posted` and `posted` is the entire point. This
script records WHY we believe a thing, and never invents evidence that it happened.
A fake `posted_at` would be exactly the kind of receipt this estate keeps finding
in other people's systems.

USAGE
    syndication-reconcile.py --dry-run          # show what would change
    syndication-reconcile.py                    # age eligible rows
    syndication-reconcile.py --mark-missed 2026-08-07 --surface x
    syndication-reconcile.py --report           # current state, no writes

Idempotent. Only ever moves `pending` forward; never touches `posted`, `not_posted`
or `n/a`.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

LEDGER = Path("/home/jeremy/000-projects/blog/startaitools/.blog-syndication-ledger.json")
SURFACES = ("x", "li_personal", "li_company", "substack", "medium")

# How long after the packet goes out before silence is read as "he posted".
# One day: the packet lands at 05:00 and Ezekiel's SOP is same-day posting, so a
# post whose packet went out yesterday or earlier has had its chance.
ASSUME_AFTER_DAYS = 1
PROVENANCE = (
    "owner standing instruction 2026-08-11: assume posted unless told otherwise; "
    "no reply path exists yet (bead startaitools-v8j)"
)


def load() -> list:
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def save(rows: list) -> None:
    tmp = LEDGER.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    json.loads(tmp.read_text(encoding="utf-8"))  # validate before swapping
    tmp.replace(LEDGER)


def report(rows: list) -> int:
    counts: dict[str, int] = {}
    for e in rows:
        for s in (e.get("syndication") or {}).values():
            st = (s or {}).get("status", "missing")
            counts[st] = counts.get(st, 0) + 1
    total = sum(counts.values())
    print(f"{len(rows)} posts, {total} surface rows")
    for st in sorted(counts, key=lambda k: -counts[k]):
        print(f"  {st:16} {counts[st]:4d}  ({counts[st]*100//total if total else 0}%)")
    if counts.get("posted"):
        print("\n'posted' rows carry a real receipt (url + timestamp).")
    print("'assumed_posted' rows record a belief and its provenance, never a receipt.")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="show changes, write nothing")
    ap.add_argument("--report", action="store_true", help="print current state and exit")
    ap.add_argument("--mark-missed", metavar="YYYY-MM-DD",
                    help="the owner says this post was NOT posted")
    ap.add_argument("--surface", choices=SURFACES,
                    help="limit --mark-missed to one surface (default: all)")
    args = ap.parse_args(argv)

    if not LEDGER.exists():
        print(f"no ledger at {LEDGER}", file=sys.stderr)
        return 1
    rows = load()

    if args.report:
        return report(rows)

    if args.mark_missed:
        hit = 0
        for e in rows:
            if e.get("date") != args.mark_missed:
                continue
            for name, s in (e.get("syndication") or {}).items():
                if args.surface and name != args.surface:
                    continue
                if (s or {}).get("status") in ("pending", "assumed_posted"):
                    s["status"] = "not_posted"
                    s["by"] = "owner report"
                    hit += 1
        if not hit:
            print(f"no eligible rows for {args.mark_missed}", file=sys.stderr)
            return 1
        if not args.dry_run:
            save(rows)
        print(f"{'would mark' if args.dry_run else 'marked'} {hit} row(s) not_posted "
              f"for {args.mark_missed}")
        return 0

    cutoff = (date.today() - timedelta(days=ASSUME_AFTER_DAYS)).isoformat()
    changed = 0
    touched: list[str] = []
    for e in rows:
        d = e.get("date")
        # Only age a post whose packet actually went out, and only once it is old
        # enough that Ezekiel has had his window.
        if not d or d > cutoff or not e.get("packet_sent"):
            continue
        for s in (e.get("syndication") or {}).values():
            if (s or {}).get("status") == "pending":
                s["status"] = "assumed_posted"
                s["by"] = PROVENANCE
                changed += 1
        if changed and (not touched or touched[-1] != d):
            touched.append(d)

    if not changed:
        print("nothing to reconcile; no pending rows past the window")
        return 0
    if not args.dry_run:
        save(rows)
    print(f"{'would age' if args.dry_run else 'aged'} {changed} pending row(s) to "
          f"assumed_posted across {len(touched)} post(s) "
          f"({touched[0]} .. {touched[-1]})")
    print("These are BELIEFS with provenance, not receipts. A real receipt needs "
          "the reply ingester (bead startaitools-v8j).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
