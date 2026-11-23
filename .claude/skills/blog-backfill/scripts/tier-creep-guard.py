#!/usr/bin/env python3
"""tier-creep-guard.py — deterministic tier-distribution tripwire with hysteresis.

Reads the append-only decisions.jsonl, computes the rolling tier distribution
over the last N daily classifications, and alerts when it crosses a threshold:
T2 > 40, T1 < 52, T3 > 12, T1 > 85 (percent; BANDS below is the authority and
alert_summary() prints it). The targets the thresholds sit around are T1 60-70 /
T2 25-35 / T3 5-10; being outside a target alone does not alert. Catches creep in
BOTH directions — Tier-2/3 inflation AND the Jan/Feb-style Tier-1 over-deflation.

HYSTERESIS (so a persistent breach isn't a weekly nag): a JSON state file records
the last-alerted snapshot. The guard signals an ALERT only on breach *onset* or
*worsening* (a newly-breached band, or a breached metric passing its previous
high-water mark by >= WORSEN_MARGIN). A breach that merely persists (same or
improving, still out of band) is SUPPRESSED -- but only for ESCALATE_RUNS quiet
runs in a row. After that the guard escalates on DURATION ALONE and re-alerts
even though nothing got worse: distribution drift that sits stable out of band
for weeks is not "handled" just because it stopped getting worse (August 2026
sat 30 points out of band for two months and never paged anyone, because
hysteresis only escalated on depth). When the distribution returns to healthy
after a breach, it signals RECOVER once (all-clear), then resets.

SECOND METRIC -- dead pattern engine: the tier distribution can look healthy
while the thing that is supposed to be correcting it has quietly stopped
running. `applied_patterns: []` on a classifier record is ambiguous by itself
(the engine ran and nothing matched, or an agent filled the field by hand
without running the engine at all). A long trailing run of empty results is
only treated as a dead-engine signal when at least one ACTIVE pattern's rule
can be shown to match SOME decision somewhere in the full history -- a rule
that has never once matched anything is not evidence the engine died, it is
evidence the rule never fired in the first place. See check_dead_engine().

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
import importlib.util
import json
import os
import sys
from collections import Counter
from pathlib import Path

# Default: the decisions.jsonl beside this script's own copy of the repository, never
# a hard-coded primary checkout. The weekly wrapper runs this script from a `git archive`
# snapshot of fresh origin, so the default reads fresh origin data (authority map
# 000-docs/014 section 4.4).
DECISIONS = os.environ.get(
    "TIER_CREEP_DECISIONS",
    str(Path(__file__).resolve().parents[1] / "methodology" / "decisions.jsonl"),
)
STATE_PATH = os.environ.get(
    "TIER_CREEP_STATE",
    "/home/jeremy/.local/state/blog-tier-creep-guard/state.json",
)
WINDOW = int(os.environ.get("TIER_CREEP_WINDOW", "30"))          # rolling sample size
MIN_N = int(os.environ.get("TIER_CREEP_MIN_N", "10"))            # too-small-to-judge floor
# pts past high-water to re-alert
WORSEN_MARGIN = int(os.environ.get("TIER_CREEP_WORSEN_MARGIN", "5"))
# Consecutive SUPPRESSED runs before a persistent breach re-escalates on DURATION.
# The guard runs weekly, so 3 ~= three weeks of a stable breach. Without this a
# breach that never worsens is silent forever: August 2026 sat 30 pts out of band
# for two months and never paged anyone because hysteresis only escalates on
# depth. Escalate on age too, then reset the counter so it re-pages roughly
# monthly rather than weekly (a nag) or never (the bug).
ESCALATE_RUNS = int(os.environ.get("TIER_CREEP_ESCALATE_RUNS", "3"))
# consecutive trailing classifier runs with an empty applied_patterns list, while
# an active rule matches history, before the pattern engine is called dead.
ENGINE_DEAD_MIN = int(os.environ.get("TIER_CREEP_ENGINE_DEAD_MIN", "5"))
# Test-only override of apply-patterns.py's patterns.jsonl location. Unset in
# production, where check_dead_engine reads the real file.
PATTERNS_OVERRIDE = os.environ.get("TIER_CREEP_PATTERNS")

# tolerance bands (percentages). Target: T1 60-70 / T2 25-35 / T3 5-10.
# Each band: (metric key, direction). direction "high" = worse when larger;
# "low" = worse when smaller.
# BANDS is the tier-DISTRIBUTION bands only -- alert_summary(BANDS) and the
# authority-map tests pin its rendered string, so the dead-engine band lives
# in ENGINE_BANDS instead and the two are merged into ALL_BANDS for breach
# detection / hysteresis, which do not care which dict a band came from.
BANDS = {
    "t2_high": ("t2", "high", int(os.environ.get("TIER_CREEP_T2_HIGH", "40"))),  # T2 inflation
    "t1_low":  ("t1", "low",  int(os.environ.get("TIER_CREEP_T1_LOW", "52"))),   # T1 starved
    "t3_high": ("t3", "high", int(os.environ.get("TIER_CREEP_T3_HIGH", "12"))),  # T3 overuse
    "t1_high": ("t1", "high", int(os.environ.get("TIER_CREEP_T1_HIGH", "85"))),  # T1 over-deflation
}
ENGINE_BANDS = {
    "engine_dead": ("engine_dead_streak", "high", ENGINE_DEAD_MIN),  # dead pattern engine
}
ALL_BANDS = {**BANDS, **ENGINE_BANDS}
BAND_UNIT = {"engine_dead": " posts"}  # everything else in ALL_BANDS is a percent
_OP = {"high": ">", "low": "<"}


def alert_summary(bands=None):
    """The real alert thresholds, rendered from BANDS (e.g. 'T2 > 40, T1 < 52')."""
    return ", ".join(f"{key.upper()} {_OP[direction]} {value}"
                     for key, direction, value in (bands or BANDS).values())


BAND_LABEL = {
    "t2_high": "Tier-2 INFLATION (target 25-35%)",
    "t1_low":  "Tier-1 STARVED (target 60-70%)",
    "t3_high": "Tier-3 OVERUSE (target 5-10%)",
    "t1_high": "Tier-1 OVER-DEFLATION (Jan/Feb failure mode)",
    "engine_dead": "PATTERN ENGINE DEAD (empty matches despite a rule with real history)",
}


def load_records():
    """scripts/blog/blogpipe/records.py: the one definition of decisions.jsonl record kinds.

    Loaded by path (this script runs outside the package). No bytecode is written, so a
    run workspace's write-set stays exact.
    """
    sys.dont_write_bytecode = True
    path = Path(__file__).resolve().parents[4] / "scripts/blog/blogpipe/records.py"
    spec = importlib.util.spec_from_file_location("blogpipe_records", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_apply_patterns_module():
    """.claude/skills/blog-backfill/scripts/apply-patterns.py, loaded by path (same
    technique as load_records): this script can run from a `git archive` snapshot
    outside any installed package, so a normal sibling `import` is not available.
    """
    sys.dont_write_bytecode = True
    path = Path(__file__).resolve().parent / "apply-patterns.py"
    spec = importlib.util.spec_from_file_location("blog_apply_patterns", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_classifier_records(path):
    """Full classifier record dicts -- needed for both the tier-distribution metric
    (date, tier) and the pattern-engine health check (dimensions, applied_patterns).
    """
    try:
        fh = open(path)
    except OSError as e:
        print(f"FATAL: cannot read {path}: {e}", file=sys.stderr)
        sys.exit(2)
    try:
        records = load_records()
    except OSError as exc:
        print(f"FATAL: record-kind module unavailable: {exc}", file=sys.stderr)
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
            # Select the classifier decision by record kind. The old audit_addendum
            # filter dropped the recovered 2026-09-12 decision (audit_addendum:true but
            # tier + dimensions) and would count a shipped_tier record if it had a tier.
            if not records.is_classifier(o):
                continue
            if o.get("cadence_type") == "monthly":
                continue
            if "date" in o:
                rows.append(o)
    rows.sort(key=lambda o: o["date"])
    return rows


def load_daily_tiers(path):
    """(date, tier) tuples -- the tier-distribution metric's input shape."""
    return [(o["date"][:10], o["tier"]) for o in load_classifier_records(path)]


def check_dead_engine(records_rows, patterns_path=None):
    """Detect a pattern-apply engine that has gone silent.

    streak = count of the most recent classifier records -- restricted to those
    carrying an `applied_patterns` field at all, i.e. only records produced after
    the pattern engine was wired in -- with an empty list, counted backward from
    the newest record until a non-empty one breaks the run.

    matched_history = True iff some currently-ACTIVE pattern's rule matches at
    least one decision anywhere in the full history. A rule that has never once
    matched a real decision cannot prove the engine died; it is just a rule that
    has not applied yet. Returns (streak, matched_history); the caller treats the
    metric as 0 (healthy) unless matched_history is also True.

    patterns_path overrides apply-patterns.py's own patterns.jsonl location (tests
    only; production always reads the real file).
    """
    engine_rows = [o for o in records_rows if o.get("applied_patterns") is not None]
    if not engine_rows:
        return 0, False

    streak = 0
    for o in reversed(engine_rows):
        if o.get("applied_patterns") == []:
            streak += 1
        else:
            break
    if streak == 0:
        return 0, False

    try:
        patterns_mod = load_apply_patterns_module()
    except OSError as e:
        print(f"WARN: could not load apply-patterns.py for dead-engine check: {e}",
              file=sys.stderr)
        return streak, False

    active = patterns_mod.load_patterns(patterns_path or patterns_mod.PATTERNS_PATH)
    if not active:
        return streak, False

    for o in records_rows:
        dims = o.get("dimensions") or {}
        if not dims:
            continue
        feats = patterns_mod.features(dims, o.get("tier"))
        for p in active:
            if patterns_mod.rule_matches(p["rule"], feats):
                return streak, True
    return streak, False


def pct(c, n):
    return round(100 * c / n) if n else 0


def compute(rows, extra_metrics=None):
    """Return (n, span, metrics, breaches). breaches: {band: value} for breached bands.

    extra_metrics merges in non-distribution metrics (e.g. engine_dead_streak) so
    they go through the same ALL_BANDS threshold check as the distribution ones.
    """
    last = rows[-WINDOW:]
    n = len(last)
    c = Counter(t for _, t in last)
    metrics = {"t1": pct(c[1], n), "t2": pct(c[2], n), "t3": pct(c[3], n)}
    if extra_metrics:
        metrics.update(extra_metrics)
    breaches = {}
    for band, (mkey, direction, thresh) in ALL_BANDS.items():
        v = metrics.get(mkey)
        if v is None:
            continue
        if (direction == "high" and v > thresh) or (direction == "low" and v < thresh):
            breaches[band] = v
    span = f"{last[0][0]}..{last[-1][0]}"
    return n, span, metrics, breaches


def is_worse(current, alerted):
    """True if current breaches are worse than the last-alerted snapshot."""
    for band, val in current.items():
        if band not in alerted:
            return True  # a newly-breached band
        direction = ALL_BANDS[band][1]
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
          f"     (target T1 60-70 / T2 25-35 / T3 5-10; alerts at {alert_summary()})")
    if "engine_dead_streak" in metrics:
        print(f"  Pattern engine: empty-match streak {metrics['engine_dead_streak']}"
              f" (alerts at {ENGINE_DEAD_MIN}+ while an active rule matches history)")
    if breaches:
        print("\nOut-of-band:")
        for band, v in breaches.items():
            thresh = ALL_BANDS[band][2]
            unit = BAND_UNIT.get(band, "%")
            print(f"  - {BAND_LABEL[band]}: {v}{unit} vs threshold {thresh}{unit}")


def _deep_dive_hint(breaches):
    """The recalibration advice applies to distribution breaches only; a dead
    pattern engine needs a different fix, so point at it separately."""
    if set(breaches) == {"engine_dead"}:
        return ("Deep-dive: run `apply-patterns.py apply` by hand against a recent "
                "classification and compare to the land-time record -- a rule with "
                "real history has stopped firing somewhere in the classify/land path.")
    return ("Deep-dive: run /blog-calibrate. The score-keyed cap rules cannot fix "
            "this — recalibrate the NAR/TCH anchors in "
            "references/content-tier-classification.md.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stateless", action="store_true",
                    help="pure check, no state read/write (exit 0 healthy / 1 breach)")
    args = ap.parse_args()

    records_rows = load_classifier_records(DECISIONS)
    rows = [(o["date"][:10], o["tier"]) for o in records_rows]
    if len(rows) < MIN_N:
        print(f"HEALTHY (insufficient sample: {len(rows)} < {MIN_N} classifications)")
        print("ACTION: healthy")
        return 0

    engine_streak, engine_matched = check_dead_engine(
        records_rows, Path(PATTERNS_OVERRIDE) if PATTERNS_OVERRIDE else None
    )
    extra_metrics = {"engine_dead_streak": engine_streak if engine_matched else 0}

    n, span, metrics, breaches = compute(rows, extra_metrics)
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
                direction = ALL_BANDS[band][1]
                new_alerted[band] = (max(new_alerted[band], val) if direction == "high"
                                     else min(new_alerted[band], val))
        # drop bands no longer breached from the high-water record
        new_alerted = {b: v for b, v in new_alerted.items() if b in breaches}
        # A real alert resets the duration counter: the clock on "how long has
        # this been quietly breached" starts over from a paged event.
        write_state(STATE_PATH, {"status": "breached", "alerted": new_alerted,
                                 "last_span": span, "suppressed_runs": 0})
        print(f"\nACTION: alert ({why})")
        print(_deep_dive_hint(breaches))
        return 1

    # Breach persists and is not worse. Count the quiet runs; escalate on DURATION
    # once the breach has been silently open for ESCALATE_RUNS runs, then reset the
    # counter so it re-pages periodically instead of never.
    suppressed = int(state.get("suppressed_runs", 0)) + 1
    if suppressed >= ESCALATE_RUNS:
        write_state(STATE_PATH, {"status": "breached", "alerted": alerted,
                                 "last_span": span, "suppressed_runs": 0})
        print(f"\nACTION: alert (persistent — breached for {suppressed}+ runs without improving)")
        print("This breach has been open and stable for weeks. Hysteresis was hiding it. "
              + _deep_dive_hint(breaches))
        return 1

    write_state(STATE_PATH, {"status": "breached", "alerted": alerted,
                             "last_span": span, "suppressed_runs": suppressed})
    print(f"\nACTION: suppress ({why}) — no alert; "
          f"quiet run {suppressed}/{ESCALATE_RUNS}, high-water {alerted}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
