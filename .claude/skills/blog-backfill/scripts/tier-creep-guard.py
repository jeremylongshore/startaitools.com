#!/usr/bin/env python3
"""tier-creep-guard.py — deterministic tier-distribution tripwire (no LLM).

Reads the append-only decisions.jsonl, computes the rolling tier distribution
over the last N daily classifications, and checks it against tolerance bands
around the target (T1 60-70% / T2 25-35% / T3 5-10%). Catches creep in BOTH
directions — Tier-2/3 inflation AND the Jan/Feb-style Tier-1 over-deflation.

Exit 0 = healthy (within tolerance). Exit 1 = one or more bands breached.
Prints a short human-readable report to stdout either way; the cron wrapper
(blog-tier-creep-guard.sh) decides whether to alert based on the exit code.

Thresholds are overridable via env vars (defaults in THRESHOLDS below).
Deterministic and side-effect-free: reads one file, writes nothing.
"""
import json
import os
import sys
from collections import Counter

DECISIONS = os.environ.get(
    "TIER_CREEP_DECISIONS",
    "/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/methodology/decisions.jsonl",
)
WINDOW = int(os.environ.get("TIER_CREEP_WINDOW", "30"))          # rolling sample size
MIN_N = int(os.environ.get("TIER_CREEP_MIN_N", "10"))            # too-small-to-judge floor

# tolerance bands (percentages). Target: T1 60-70 / T2 25-35 / T3 5-10.
THRESHOLDS = {
    "t2_high": int(os.environ.get("TIER_CREEP_T2_HIGH", "40")),  # T2 > this -> inflation
    "t1_low": int(os.environ.get("TIER_CREEP_T1_LOW", "52")),    # T1 < this -> starved
    "t3_high": int(os.environ.get("TIER_CREEP_T3_HIGH", "12")),  # T3 > this -> overuse
    "t1_high": int(os.environ.get("TIER_CREEP_T1_HIGH", "85")),  # T1 > this -> over-deflation
}


def load_daily_tiers(path):
    rows = []
    try:
        fh = open(path)
    except OSError as e:
        print(f"FATAL: cannot read {path}: {e}", file=sys.stderr)
        sys.exit(2)
    with fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue
            if o.get("event") == "agent_audit" or o.get("audit_addendum"):
                continue
            if o.get("cadence_type") == "monthly":
                continue
            if "tier" in o and "date" in o:
                rows.append((o["date"][:10], o["tier"]))
    rows.sort()
    return rows


def pct(c, n):
    return round(100 * c / n) if n else 0


def check(rows):
    breaches = []
    if len(rows) < MIN_N:
        print(f"HEALTHY (insufficient sample: {len(rows)} < {MIN_N} classifications)")
        return 0
    last = rows[-WINDOW:]
    n = len(last)
    c = Counter(t for _, t in last)
    p1, p2, p3 = pct(c[1], n), pct(c[2], n), pct(c[3], n)

    if p2 > THRESHOLDS["t2_high"]:
        breaches.append(f"Tier-2 INFLATION: {p2}% > {THRESHOLDS['t2_high']}% (target 25-35%)")
    if p1 < THRESHOLDS["t1_low"]:
        breaches.append(f"Tier-1 STARVED: {p1}% < {THRESHOLDS['t1_low']}% (target 60-70%)")
    if p3 > THRESHOLDS["t3_high"]:
        breaches.append(f"Tier-3 OVERUSE: {p3}% > {THRESHOLDS['t3_high']}% (target 5-10%)")
    if p1 > THRESHOLDS["t1_high"]:
        breaches.append(f"Tier-1 OVER-DEFLATION: {p1}% > {THRESHOLDS['t1_high']}% (Jan/Feb failure mode)")

    span = f"{last[0][0]}..{last[-1][0]}"
    print(f"Rolling last {n} classifications ({span}):")
    print(f"  T1 {p1}%  |  T2 {p2}%  |  T3 {p3}%     (target T1 60-70 / T2 25-35 / T3 5-10)")
    if breaches:
        print("\nCREEP DETECTED:")
        for b in breaches:
            print(f"  - {b}")
        print("\nDeep-dive: run /blog-calibrate. Tighten the Tier-2 narrative-or-standout "
              "floor (pattern auto-2026-07-001) if T2 stays inflated.")
        return 1
    print("\nHEALTHY: distribution within tolerance bands.")
    return 0


if __name__ == "__main__":
    sys.exit(check(load_daily_tiers(DECISIONS)))
