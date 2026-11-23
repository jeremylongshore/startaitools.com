"""tier-creep-guard.py's second metric: a dead pattern-apply engine, plus
duration-based re-alerting on a breach that never worsens.

startaitools-8oc.6. The distribution-only guard's hysteresis correctly
suppressed a persistent breach for five weeks while the mismatch rate roughly
doubled: "not getting worse" read as "handled". This file pins two things:

  1. check_dead_engine() flags a pattern engine whose applied_patterns has gone
     empty on recent classifier runs, but ONLY when an active rule can be shown
     to match something in history (so a rule that has simply never fired does
     not manufacture a false alarm).
  2. The guard's existing duration escalation (ESCALATE_RUNS) still re-pages a
     stable, non-worsening breach after enough quiet runs -- exercised here
     against the new engine_dead band so the two features are proven together,
     not just each in isolation.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".claude/skills/blog-backfill/scripts/tier-creep-guard.py"


def load_guard():
    spec = importlib.util.spec_from_file_location("tier_creep_guard", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


guard = load_guard()

MATCHING_DIMS = {"novelty": 3, "arc": 3, "nar": 0, "tch": 0, "scp": 0, "rpr": 0}
# A rule that matches MATCHING_DIMS: two dims >= 3 (count_ge3 >= 2), nothing a
# standout (max_all <= 3).
LIVE_RULE = {
    "all": [
        {"feature": "count_ge3", "op": ">=", "value": 2},
        {"feature": "max_all", "op": "<=", "value": 3},
    ],
    "action": {"type": "cap_tier", "tier": 1},
}
# A rule that cannot match anything built from MATCHING_DIMS (or any real
# dimension set, since dims are 0-5): proves the gate, not just the streak.
UNMATCHABLE_RULE = {
    "all": [{"feature": "nov", "op": ">=", "value": 99}],
    "action": {"type": "cap_tier", "tier": 1},
}


def classifier_row(date, *, dims=None, applied_patterns=None, tier=2):
    row = {"date": date, "tier": tier, "record_type": "classifier"}
    if dims is not None:
        row["dimensions"] = dims
    if applied_patterns is not None:
        row["applied_patterns"] = applied_patterns
    return row


def write_patterns(tmp_path, rule, *, active=True):
    path = tmp_path / "patterns.jsonl"
    path.write_text(json.dumps({
        "pattern_id": "test-001", "active": active, "rule": rule, "times_applied": 1,
    }) + "\n")
    return path


# --- check_dead_engine(): streak + the historical-match gate -------------------------


def test_streak_counts_trailing_empty_runs_and_stops_at_the_first_nonempty_one():
    rows = [
        classifier_row("2026-10-01", dims=MATCHING_DIMS, applied_patterns=["some-pattern"]),
        classifier_row("2026-10-02", dims=MATCHING_DIMS, applied_patterns=[]),
        classifier_row("2026-10-03", dims=MATCHING_DIMS, applied_patterns=[]),
        classifier_row("2026-10-04", dims=MATCHING_DIMS, applied_patterns=[]),
    ]
    streak, _ = guard.check_dead_engine(rows)
    assert streak == 3  # the 10-01 nonempty row breaks the trailing run


def test_gate_requires_an_active_rule_to_match_somewhere_in_history(tmp_path):
    rows = [classifier_row(f"2026-10-{d:02d}", dims=MATCHING_DIMS, applied_patterns=[])
            for d in range(1, 7)]

    # An active rule that CAN match -> the streak counts as a real dead-engine signal.
    live = write_patterns(tmp_path, LIVE_RULE)
    streak, matched = guard.check_dead_engine(rows, patterns_path=live)
    assert streak == 6 and matched is True

    # An active rule that can NEVER match -> same empty streak, but no history to
    # prove the engine should have fired, so it is not treated as a dead-engine
    # signal. This is the false-alarm guard named in the bead.
    dead = write_patterns(tmp_path, UNMATCHABLE_RULE)
    streak, matched = guard.check_dead_engine(rows, patterns_path=dead)
    assert streak == 6 and matched is False


def test_no_active_patterns_at_all_cannot_be_a_dead_engine(tmp_path):
    rows = [classifier_row(f"2026-10-{d:02d}", dims=MATCHING_DIMS, applied_patterns=[])
            for d in range(1, 7)]
    none_active = write_patterns(tmp_path, LIVE_RULE, active=False)
    streak, matched = guard.check_dead_engine(rows, patterns_path=none_active)
    assert streak == 6 and matched is False


def test_a_nonempty_trailing_run_is_never_a_dead_engine():
    rows = [classifier_row(f"2026-10-{d:02d}", dims=MATCHING_DIMS, applied_patterns=["x"])
            for d in range(1, 7)]
    streak, matched = guard.check_dead_engine(rows)
    assert (streak, matched) == (0, False)


def test_pre_engine_records_with_no_applied_patterns_field_are_ignored():
    # Records from before the pattern engine existed carry no applied_patterns key
    # at all (None, not []). They must not count toward the streak either way.
    rows = [classifier_row("2026-09-01", dims=MATCHING_DIMS)]  # applied_patterns absent
    streak, matched = guard.check_dead_engine(rows)
    assert (streak, matched) == (0, False)


def test_the_gate_has_teeth_removing_it_would_false_alarm_on_an_unfired_rule(tmp_path, monkeypatch):
    """Prove the historical-match requirement is load-bearing: simulate the engine
    WITHOUT it (matched_history forced True) and show the same inputs that pass
    cleanly above would then wrongly report a dead engine for a rule that has
    simply never had a chance to fire."""
    rows = [classifier_row(f"2026-10-{d:02d}", dims=MATCHING_DIMS, applied_patterns=[])
            for d in range(1, 7)]
    dead = write_patterns(tmp_path, UNMATCHABLE_RULE)
    streak, matched = guard.check_dead_engine(rows, patterns_path=dead)
    assert matched is False  # the real, gated behavior: no false alarm

    # Now remove the gate the way an unguarded implementation would: treat any
    # active pattern as sufficient regardless of whether it ever matched.
    def ungated(records_rows, patterns_path=None):
        patterns_mod = guard.load_apply_patterns_module()
        active = patterns_mod.load_patterns(patterns_path or patterns_mod.PATTERNS_PATH)
        engine_rows = [o for o in records_rows if o.get("applied_patterns") is not None]
        streak = 0
        for o in reversed(engine_rows):
            if o.get("applied_patterns") == []:
                streak += 1
            else:
                break
        return streak, bool(active)  # <-- the bug: no history check at all

    monkeypatch.setattr(guard, "check_dead_engine", ungated)
    broken_streak, broken_matched = guard.check_dead_engine(rows, patterns_path=dead)
    assert broken_matched is True  # confirms the ungated version DOES false-alarm
    assert broken_streak == streak


# --- compute(): the engine_dead band feeds the same breach/hysteresis machinery ------


def test_compute_breaches_on_a_dead_engine_streak_past_the_threshold():
    rows = [(f"2026-10-{d:02d}", 1) for d in range(1, 15)]  # healthy distribution
    _, _, metrics, breaches = guard.compute(rows, {"engine_dead_streak": guard.ENGINE_DEAD_MIN + 1})
    assert "engine_dead" in breaches
    assert "t2_high" not in breaches and "t1_low" not in breaches


def test_compute_does_not_breach_below_the_engine_dead_threshold():
    rows = [(f"2026-10-{d:02d}", 1) for d in range(1, 15)]
    _, _, metrics, breaches = guard.compute(rows, {"engine_dead_streak": guard.ENGINE_DEAD_MIN})
    assert "engine_dead" not in breaches


def test_bands_dict_itself_is_unchanged_distribution_only():
    # Locks the contract test_one_authority_per_concern.py relies on: BANDS is
    # still exactly the four distribution bands, so alert_summary(BANDS) keeps
    # rendering the documented string even though ALL_BANDS now has a fifth.
    assert set(guard.BANDS) == {"t2_high", "t1_low", "t3_high", "t1_high"}
    assert set(guard.ALL_BANDS) == set(guard.BANDS) | {"engine_dead"}


# --- end-to-end CLI: engine-dead alert + duration-based re-alert on persistence ------


def write_decisions(tmp_path, rows):
    path = tmp_path / "decisions.jsonl"
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    return path


def run_guard(decisions, patterns, state_path, *, extra_env=None):
    env = {
        "TIER_CREEP_DECISIONS": str(decisions),
        "TIER_CREEP_PATTERNS": str(patterns),
        "TIER_CREEP_STATE": str(state_path),
        "PATH": "/usr/bin:/bin",
    }
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [sys.executable, str(SCRIPT)], capture_output=True, text=True, env=env, timeout=30,
    )


def _distribution_tiers(n):
    """~65% T1 / 30% T2 / 5% T3 -- inside every BANDS target, so these fixtures
    never trip a distribution breach; only the engine_dead band can fire."""
    pattern = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3]
    return [pattern[i % len(pattern)] for i in range(n)]


def _fixture_rows(dead_streak_len):
    """A healthy-distribution history (applied_patterns always matched) followed
    by `dead_streak_len` trailing classifier runs with an empty applied_patterns,
    all sharing dims that satisfy LIVE_RULE so matched_history is always available
    once an active rule is wired up."""
    healthy_n = 14
    tiers = _distribution_tiers(healthy_n + dead_streak_len)
    rows = [
        classifier_row(f"2026-09-{d:02d}", dims=MATCHING_DIMS, tier=tiers[d - 1],
                        applied_patterns=["test-001"])
        for d in range(1, healthy_n + 1)
    ]
    rows += [
        classifier_row(f"2026-10-{d:02d}", dims=MATCHING_DIMS, tier=tiers[healthy_n + d - 1],
                        applied_patterns=[])
        for d in range(1, dead_streak_len + 1)
    ]
    return rows


def test_cli_alerts_on_dead_engine_onset(tmp_path):
    rows = _fixture_rows(guard.ENGINE_DEAD_MIN + 2)
    decisions = write_decisions(tmp_path, rows)
    patterns = write_patterns(tmp_path, LIVE_RULE)
    result = run_guard(decisions, patterns, tmp_path / "state.json")
    assert result.returncode == 1, result.stdout + result.stderr
    assert "PATTERN ENGINE DEAD" in result.stdout
    assert "ACTION: alert (onset)" in result.stdout


def test_cli_does_not_alert_when_the_rule_never_matched_history(tmp_path):
    rows = _fixture_rows(guard.ENGINE_DEAD_MIN + 2)
    decisions = write_decisions(tmp_path, rows)
    patterns = write_patterns(tmp_path, UNMATCHABLE_RULE)
    result = run_guard(decisions, patterns, tmp_path / "state.json")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PATTERN ENGINE DEAD" not in result.stdout


def test_cli_re_pages_on_duration_even_though_the_streak_never_worsens(tmp_path):
    """The acceptance criterion: a breach that persists N weeks re-pages even when
    not worsening. Run the identical dead-engine input ESCALATE_RUNS+1 times (as
    the weekly cron would) and confirm: onset alerts, the next (ESCALATE_RUNS - 1)
    runs suppress (same severity, not worse), then the run at ESCALATE_RUNS
    re-alerts purely on duration."""
    rows = _fixture_rows(guard.ENGINE_DEAD_MIN + 2)
    decisions = write_decisions(tmp_path, rows)
    patterns = write_patterns(tmp_path, LIVE_RULE)
    state = tmp_path / "state.json"

    first = run_guard(decisions, patterns, state)
    assert first.returncode == 1 and "ACTION: alert (onset)" in first.stdout

    for _ in range(guard.ESCALATE_RUNS - 1):
        result = run_guard(decisions, patterns, state)
        assert result.returncode == 0, result.stdout
        assert "ACTION: suppress" in result.stdout

    escalated = run_guard(decisions, patterns, state)
    assert escalated.returncode == 1, escalated.stdout
    assert "persistent" in escalated.stdout
    assert "breached for" in escalated.stdout


def test_the_duration_escalation_has_teeth_disabling_it_would_silence_the_breach_forever(
    tmp_path,
):
    """Prove ESCALATE_RUNS is load-bearing: with it effectively infinite, the same
    never-worsening breach in the previous test suppresses indefinitely instead of
    re-paging -- exactly the August 2026 failure mode the bead describes."""
    rows = _fixture_rows(guard.ENGINE_DEAD_MIN + 2)
    decisions = write_decisions(tmp_path, rows)
    patterns = write_patterns(tmp_path, LIVE_RULE)
    state = tmp_path / "state.json"

    first = run_guard(decisions, patterns, state, extra_env={"TIER_CREEP_ESCALATE_RUNS": "999999"})
    assert first.returncode == 1

    for _ in range(guard.ESCALATE_RUNS + 2):
        result = run_guard(decisions, patterns, state,
                            extra_env={"TIER_CREEP_ESCALATE_RUNS": "999999"})
        assert result.returncode == 0, result.stdout  # never escalates: the bug, reproduced
        assert "ACTION: suppress" in result.stdout
