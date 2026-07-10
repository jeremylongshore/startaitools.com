#!/usr/bin/env python3
"""tier-creep-guard.py — deterministic tier-distribution tripwire with hysteresis.

Reads the append-only decisions.jsonl, computes the rolling tier distribution
over the last N daily classifications, and checks it against tolerance bands
around the target (T1 60-70% / T2 25-35% / T3 5-10%). Catches creep in BOTH
directions — Tier-2/3 inflation AND the Jan/Feb-style Tier-1 over-deflation.

HYSTERESIS (so a persistent breach isn't a weekly nag): a JSON state file records
the last-alerted snapshot. The guard signals an ALERT only on breach *onset* or
*worsening* (a newly-breached band, or a breached metric passing its previous
high-water mark by >= WORSEN_MARGIN). A breach that merely persists (same or
improving, still out of band) is SUPPRESSED. When the distribution returns to
healthy after a breach, it signals RECOVER once (all-clear), then resets.

Exit codes (the cron wrapper acts on these):
  0 = no notification  (healthy-and-was-healthy, or a suppressed persistent breach)
  1 = ALERT            (breach onset or worsening)
  3 = RECOVER          (was breached, now healthy — send a one-time all-clear)
  2 = error            (decisions.jsonl unreadable)

Prints a human-readable report + an `ACTION:` line to stdout every run.
State file lives OUTSIDE the repo (default ~/.local/state/...), so this never
dirties the git tree. `--stateless` skips all state read/write (pure check;
exit 0 healthy / 1 breach) for manual runs and tests.
"""
import argparse
import json
import os
import sys
from collections import Counter

DECISIONS = os.environ.get(
    "TIER_CREEP_DECISIONS",
    "/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/methodology/decisions.jsonl",
)
STATE_PATH = os.environ.get(
    "TIER_CREEP_STATE",
    "/home/jeremy/.local/state/blog-tier-creep-guard/state.json",
)
WINDOW = int(os.environ.get("TIER_CREEP_WINDOW", "30"))          # rolling sample size
MIN_N = int(os.environ.get("TIER_CREEP_MIN_N", "10"))            # too-small-to-judge floor
# pts past high-water to re-alert
WORSEN_MARGIN = int(os.environ.get("TIER_CREEP_WORSEN_MARGIN", "5"))

# tolerance bands (percentages). Target: T1 60-70 / T2 25-35 / T3 5-10.
# Each band: (metric key, direction). direction "high" = worse when larger;
# "low" = worse when smaller.
BANDS = {
    "t2_high": ("t2", "high", int(os.environ.get("TIER_CREEP_T2_HIGH", "40"))),  # T2 inflation
    "t1_low":  ("t1", "low",  int(os.environ.get("TIER_CREEP_T1_LOW", "52"))),   # T1 starved
    "t3_high": ("t3", "high", int(os.environ.get("TIER_CREEP_T3_HIGH", "12"))),  # T3 overuse
    "t1_high": ("t1", "high", int(os.environ.get("TIER_CREEP_T1_HIGH", "85"))),  # T1 over-deflation
}
BAND_LABEL = {
    "t2_high": "Tier-2 INFLATION (target 25-35%)",
    "t1_low":  "Tier-1 STARVED (target 60-70%)",
    "t3_high": "Tier-3 OVERUSE (target 5-10%)",
    "t1_high": "Tier-1 OVER-DEFLATION (Jan/Feb failure mode)",
}


def load_daily_tiers(path):
    try:
        fh = open(path)
    except OSError as e:
        print(f"FATAL: cannot read {path}: {e}", file=sys.stderr)
        sys.exit(2)
    rows = []
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


def compute(rows):
    """Return (n, span, metrics, breaches). breaches: {band: value} for breached bands."""
    last = rows[-WINDOW:]
    n = len(last)
    c = Counter(t for _, t in last)
    metrics = {"t1": pct(c[1], n), "t2": pct(c[2], n), "t3": pct(c[3], n)}
    breaches = {}
    for band, (mkey, direction, thresh) in BANDS.items():
        v = metrics[mkey]
        if (direction == "high" and v > thresh) or (direction == "low" and v < thresh):
            breaches[band] = v
    span = f"{last[0][0]}..{last[-1][0]}"
    return n, span, metrics, breaches


def is_worse(current, alerted):
    """True if current breaches are worse than the last-alerted snapshot."""
    for band, val in current.items():
        if band not in alerted:
            return True  # a newly-breached band
        direction = BANDS[band][1]
        prev = alerted[band]
        if direction == "high" and val >= prev + WORSEN_MARGIN:
            return True
        if direction == "low" and val <= prev - WORSEN_MARGIN:
            return True
    return False


def read_state(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {"status": "healthy", "alerted": {}}


def write_state(path, state):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(state, f, indent=2)
    except OSError as e:
        print(f"WARN: could not write state {path}: {e}", file=sys.stderr)


def report(n, span, metrics, breaches):
    print(f"Rolling last {n} classifications ({span}):")
    print(f"  T1 {metrics['t1']}%  |  T2 {metrics['t2']}%  |  T3 {metrics['t3']}%"
          f"     (target T1 60-70 / T2 25-35 / T3 5-10)")
    if breaches:
        print("\nOut-of-band:")
        for band, v in breaches.items():
            thresh = BANDS[band][2]
            print(f"  - {BAND_LABEL[band]}: {v}% vs threshold {thresh}%")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stateless", action="store_true",
                    help="pure check, no state read/write (exit 0 healthy / 1 breach)")
    args = ap.parse_args()

    rows = load_daily_tiers(DECISIONS)
    if len(rows) < MIN_N:
        print(f"HEALTHY (insufficient sample: {len(rows)} < {MIN_N} classifications)")
        print("ACTION: healthy")
        return 0

    n, span, metrics, breaches = compute(rows)
    report(n, span, metrics, breaches)

    if args.stateless:
        if breaches:
            print("\nACTION: breach (stateless)")
            print("Deep-dive: run /blog-calibrate.")
            return 1
        print("\nACTION: healthy (stateless)")
        return 0

    state = read_state(STATE_PATH)
    was_breached = state.get("status") == "breached"
    alerted = state.get("alerted", {})

    if not breaches:
        if was_breached:
            write_state(STATE_PATH, {"status": "healthy", "alerted": {}, "last_span": span})
            print("\nACTION: recover — distribution back within tolerance (all-clear)")
            return 3
        write_state(STATE_PATH, {"status": "healthy", "alerted": {}, "last_span": span})
        print("\nACTION: healthy")
        return 0

    # Breached now.
    if not was_breached:
        action, why = "alert", "onset"
    elif is_worse(breaches, alerted):
        action, why = "alert", "worsening"
    else:
        action, why = "suppress", "persists (not worse than last alert)"

    if action == "alert":
        # record the new high-water mark: for each band, max-severity of prev vs current
        new_alerted = dict(alerted)
        for band, val in breaches.items():
            if band not in new_alerted:
                new_alerted[band] = val
            else:
                direction = BANDS[band][1]
                new_alerted[band] = (max(new_alerted[band], val) if direction == "high"
                                     else min(new_alerted[band], val))
        # drop bands no longer breached from the high-water record
        new_alerted = {b: v for b, v in new_alerted.items() if b in breaches}
        write_state(STATE_PATH, {"status": "breached", "alerted": new_alerted, "last_span": span})
        print(f"\nACTION: alert ({why})")
        print("Deep-dive: run /blog-calibrate. Tighten the Tier-2 narrative-or-standout "
              "floor (pattern auto-2026-07-001) if T2 stays inflated.")
        return 1

    # Suppress: keep the high-water mark, stay breached, no notification.
    write_state(STATE_PATH, {"status": "breached", "alerted": alerted, "last_span": span})
    print(f"\nACTION: suppress ({why}) — no alert; last-alerted high-water {alerted}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
