# Calibration Report: April 2026

## Summary

- Decisions analyzed: 22 (of 33 total April records — 11 are agent-audit addenda or untiered backfill notes)
- Feedback records: 0 (file is empty — Brier score unavailable)
- Patterns file: empty
- Overall health: **NEEDS ATTENTION** — first month with significant Tier 3 presence, and the rate is ~3x the expected ceiling

The April dataset is the first month in the 7-month history where Tier 3 was assigned at all. It immediately landed at 27.3%, well above the 5–10% expected band. Dimension scoring discipline looks fine; the issue is the rate at which the algorithm now reaches the Tier 3 gate.

---

## Tier Distribution

| Tier | Count | Actual % | Expected % | Status |
|------|-------|----------|------------|--------|
| 1    | 8     | 36.4%    | 60–70%     | **WARN** — far below floor |
| 2    | 8     | 36.4%    | 25–35%     | borderline-high, within tolerance |
| 3    | 6     | 27.3%    | 5–10%      | **WARN** — ~3x ceiling |

### Trend vs prior months

| Month | n   | T1%   | T2%   | T3%   |
|-------|-----|-------|-------|-------|
| 2025-10 | 11 | 45.5% | 54.5% | 0%    |
| 2025-11 | 16 | 68.8% | 31.2% | 0%    |
| 2025-12 | 24 | 79.2% | 20.8% | 0%    |
| 2026-01 | 30 | 93.3% | 6.7%  | 0%    |
| 2026-02 | 15 | 100%  | 0%    | 0%    |
| 2026-03 | 1  | 0%    | 100%  | 0%    |
| **2026-04** | **22** | **36.4%** | **36.4%** | **27.3%** |

**Trend: regime shift, not gradual creep.** February was 100% Tier 1 (15-of-15). April flipped to a markedly higher escalation rate. This is more consistent with a step-change in either input quality (April was demonstrably a heavy-narrative month: FLOPs correction, schema debacle, propagation day, broadcast fallback) or in classifier calibration than with month-over-month creep.

The T3 cluster is concentrated in the second half of the month: 4/15, 4/19, 4/23, 4/28, 4/29, 4/30. Three consecutive T3s on 4/28–4/30 deserve scrutiny — by the algorithm's own anti-inflation rule "tier-3-rarity," consecutive Tier 3s should be a stop-and-reconsider trigger.

### Coverage

22 of 30 April days have classification decisions. Missing dates: 4/2, 4/3, 4/4, 4/5, 4/12, 4/13, 4/16, 4/27. These predate the active backfill streak; they are either no-post days or unrecorded. Not a calibration issue, but a tracking gap.

---

## Calibration Accuracy (Brier Score)

**Unavailable.** `feedback.jsonl` is empty — 0 retrospective feedback records have been entered for any of the 130 historical decisions. The Brier score, the primary tool for detecting whether the confidence numbers are honest, cannot be computed.

This is the single biggest calibration gap in the system. The algorithm can score consistently and produce coherent reasoning, but without feedback we have no observable measure of whether the tier assignments were *correct* — only that they were *internally consistent*.

Confidence statistics for April (without ground truth):

| Tier | Mean confidence | Min  | Max  | n |
|------|-----------------|------|------|---|
| T1   | 0.909           | 0.82 | 0.95 | 8 |
| T2   | 0.810           | 0.72 | 0.88 | 8 |
| T3   | 0.820           | 0.78 | 0.90 | 6 |

T3 confidence at 0.82 is *lower* than T1 confidence at 0.91, which suggests the classifier is appropriately less certain on the harder calls — a healthy signal in the absence of Brier validation.

---

## Decision Quality Matrix (Annie Duke 2x2)

Cannot be populated — requires feedback records mapping decision → outcome. Currently every decision sits in the "outcome unknown" cell.

When feedback exists, the cell to focus on is "high confidence + bad outcome" (good decision, bad outcome — surfaces blind spots in dimension scoring) and "low confidence + good outcome" (lucky — surfaces under-confidence and possible over-application of anti-inflation rules).

---

## Dimension Analysis

Average dimension score per tier (n=22, dimensions on 0–5 scale):

| tier  | novelty | arc  | nar  | tch  | scp  | rpr  |
|-------|---------|------|------|------|------|------|
| T1 (n=8) | 1.12 | 1.50 | 0.75 | 1.50 | 2.12 | 1.12 |
| T2 (n=8) | 2.75 | 3.38 | 2.75 | 3.25 | 4.12 | 3.00 |
| T3 (n=6) | 3.67 | 4.00 | 4.33 | 4.00 | 4.67 | 3.33 |

**Dimension separation is clean.** Each tier occupies a distinct dimensional region — T1 around 1, T2 around 3, T3 around 4. There is no overlap that would indicate the algorithm is collapsing tiers or misapplying scoring anchors.

**Scope dominance check:** SCP averages 4.12 (T2) and 4.67 (T3). If high scope alone were driving escalations, we would expect SCP to be *the* dimension that pulls a tier up while others lag. Instead, T3 carries NAR=4.33 and TCH=4.00, both above scope-only-floor levels. The "high-scope-alone" anti-inflation rule is firing correctly (2 of 22 decisions explicitly note it).

**NAR-as-gate check:** Tier 3 should require NAR ≥ 3 (narrative arc strong enough to carry a 300–500 line case study). T3 NAR average is 4.33 — well past the gate. T2 NAR=2.75 is right at the boundary, which is appropriate for that tier.

**No dimension is misbehaving.** The leak, if any, is upstream of dimension scoring — at the input-selection / day-classification step.

---

## Anti-Inflation Effectiveness

38 anti-inflation flags across 22 decisions = 1.73 flags per decision. The algorithm is *enforcing* its own rules at high frequency.

Top flags:

| Count | Flag |
|-------|------|
| 7 | "none triggered" (decision deemed clean of inflation risk) |
| 4 | volume-not-quality (checked or applied) |
| 4 | volume-not-quality watch |
| 2 | first-time-for-me-not-novel |
| 2 | busy-not-distinguished |
| 2 | high-scope-alone |
| 2 | year-from-now test passes |

**Gap:** the explicit "tier-3-rarity" flag fires only twice in a month with 6 T3 decisions. If consecutive T3 days were triggering the rarity check, we would expect it on 4/28 *and* 4/29 *and* 4/30. It triggered on 4/30 (acknowledged) but not 4/28 or 4/29. This is the most concrete operational gap surfaced by the data.

**Likely root cause:** the rarity check is per-decision, not windowed across recent history. Three consecutive T3 days should auto-fire it.

---

## Emergent Patterns

Sample size (22 active decisions in one month) is below the 30-decision threshold the skill recommends for adding to `patterns.jsonl`. No new rules promoted this cycle.

Candidate observations to monitor:

1. **April is a regime change, not creep.** February was 100% T1; April is 36% T1 / 36% T2 / 27% T3. The change is too sharp to be cumulative drift — it's either input-driven (genuinely heavier work) or algorithm-step-changed. Two more months of data will distinguish.
2. **Consecutive T3 streak detection is not in the algorithm.** The 4/28–4/30 cluster suggests adding a windowed rule: if the previous 2 posts were T3, the third defaults to T2 absent a stronger NAR-and-NOV double gate.
3. **Confidence is lower on harder calls (T3 < T1).** Healthy signal. The classifier knows when it's reaching.

Defer pattern promotion until next month's data confirms or refutes the regime shift.

---

## Recommendations

1. **Backfill `feedback.jsonl` for the 6 April Tier 3 posts.** Without feedback the calibration system has no ground-truth signal. Run `/blog-feedback` on each T3 post 7+ days post-publish (engagement window) and record whether tier assignment proved correct in retrospect. This is the highest-leverage action — it unblocks Brier scoring next month.
2. **Add a windowed Tier 3 rarity rule to the algorithm.** If the previous 2 decisions were T3, the current decision must clear a higher gate to also be T3 — e.g., NOV ≥ 4 *and* NAR ≥ 4, not the standard "≥ 3 dimensions ≥ 4." The 4/28–4/30 streak should have forced 4/30 down to T2 by default.
3. **Set a monthly T3 budget of 2 and surface it in `/blog-backfill`.** When the running monthly count hits 2 T3s, the next candidate must clear an explicit "Tier 3 budget exceeded — justify" check. April spent 6 T3s; that's 3x what a healthy monthly distribution sustains.
4. **Re-examine 4/28, 4/29, 4/30 specifically.** Read the three posts side by side. If any reads more like a Tier 2 deep-dive than a Tier 3 case study, log it as a feedback record (`was_correct: false`) — that single retrospective data point is worth more than another calibration cycle without ground truth.
5. **Defer pattern promotion.** Sample size too small (22 < 30); regime-shift hypothesis needs a second data point. Re-evaluate with May data on 2026-06-01.

---

## Status of Step 9 (pattern updates)

No patterns appended to `patterns.jsonl` this cycle — sample size below threshold and the candidate observations need a second month of confirmation.

## Status of Step 10 (SQLite rebuild)

Index rebuild attempted as part of this skill run — see following section in the run log.
