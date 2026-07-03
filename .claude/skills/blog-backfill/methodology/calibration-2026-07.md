# Calibration Report: July 2026 (mid-cycle tier-creep check)

Generated 2026-07-03. This is an **interim** check requested to look for tier creep — July has only 3 classifications so far (below the 5-decision reliability floor), so the finding leans on the **month-over-month trend** and **rolling windows**, not July alone.

## Summary

- Decisions analyzed: 167 total (July-to-date: 3)
- Feedback records: 167 (160 matchable to a confidence)
- **Overall health: NEEDS ATTENTION** — persistent Tier-2 creep + deteriorating confidence calibration.

## Tier Distribution — the creep is at Tier 2

| Month | N | T1 | T2 | T3 | T2+T3 |
|-------|---|----|----|----|-------|
| 2026-01 | 30 | 93% | 6% | 0% | 6% |
| 2026-02 | 15 | 100% | 0% | 0% | 0% |
| 2026-04 | 22 | 36% | 36% | **27%** | 63% |
| 2026-05 | 21 | **4%** | 61% | **33%** | **95%** |
| 2026-06 | 24 | 45% | **50%** | 4% | 54% |
| 2026-07 (partial) | 3 | 33% | **66%** | 0% | 66% |
| **Rolling last 14** | 14 | 50% | **50%** | 0% | 50% |
| **Rolling last 30** | 30 | 43% | **53%** | 3% | 56% |

Target: **T1 60–70% · T2 25–35% · T3 5–10%**

**Reading it:**
- **Jan–Feb 2026 were over-*deflated*** (T1 93–100%) — the classifier was too timid.
- **April–May 2026 was the inflation blowout** — May hit T1 4% / T3 33% (the "calibration reckoning").
- **The T3 overuse is fixed.** May 33% → June 4% → July 0%. The always-on TCH/SCP gate closure worked; T3 is back inside 5–10%.
- **T2 is the unresolved creep.** It has sat at ~50% for June, July-to-date, and both rolling windows — **~15–25 points above the 25–35% target** — with T1 correspondingly starved at 43–50% (target 60–70%). This is not a spike; it's a two-month-plus plateau.

**Trend: T3 stable-healthy; T2 persistently inflated; T1 chronically suppressed.**

## Calibration Accuracy (Brier)

- **Brier, all matched pairs: 0.264** (160 pairs) → *miscalibrated* (0.20–0.30 band).
- **Brier, June-onward: 0.378** (22 pairs) → *seriously miscalibrated* (>0.30).

Recent calibration is **worse** than the all-time average — the classifier is over-confident (mean confidence 0.866) and, per the June-logged pattern, its disagreements with the structural grader are **one-directional**: the classifier scores *higher* than the grader nearly every time. That one-directional error is the signature of inflation, not noise.

## Root Cause — the novelty escalator

The already-logged pattern `auto-2026-06-001` ("Novelty is the successor Tier-2 inflation driver") named it: after the May TCH/SCP always-on gate was closed, **NOV≥3 became the mechanism escalating ~46% of daily posts to Tier 2** — 11 of 12 June Tier-2 posts carried NOV≥3, only 1 was a bare TCH/SCP-floor escalation. That pattern is `active: true` but **`times_applied: 0`** — it was discovered and recorded, but the classifier's scoring path never actually enforces it.

## Anti-Inflation Effectiveness

The confidence-gated downgrade IS firing — recent examples: 2026-07-01 readiness-audit (T3 gates passed → downgraded to T2) and 2026-07-02 backlog-zero (T2 gate fired → downgraded to T1). So the guardrail works *at the margin*. But it only catches gate-floor cases; it does nothing about the NOV≥3 escalator pushing mid-confidence posts to T2 in the first place. That's why T2 stays at 50% despite the downgrades.

## Recommendations

1. **Activate `auto-2026-06-001` in the scoring path** (highest leverage). Its condition — `NOV≥3` but `NAR≤2` and `RPR≤2` on routine ops/CI/gate subject matter → one-tier downgrade — is exactly the mechanism holding T2 at 50%. Wiring it into `classify-day` (not just leaving it logged with `times_applied: 0`) should pull T2 toward the 25–35% target.
2. **Raise the bar on NOV as a sole escalator.** NOV≥3 should not by itself clear the Tier-2 gate unless a second subjective dimension (NAR or a named TCH artifact) also clears. Novelty is the easiest dimension to over-score.
3. **Watch T1 recovery.** Success = T1 back above 55% and T2 under 40% over the next 14 days. Re-check at the August monthly calibrate.
4. **Do not over-correct into the Jan/Feb deflation** (T1 93–100%). The goal is 60/30/10, not a return to all-Field-Notes.

## Implemented 2026-07-03 (same-session follow-through)

Recommendation 1 was acted on, with a correction the data forced:

- The **literal** `auto-2026-06-001` rule (downgrade when NOV≥3 but NAR≤2 AND TCH≤2 AND RPR≤2) was implemented, then **simulated against all 167 decisions — and downgraded 0 posts.** Every recent Tier-2 post has TCH≥3 (usually TCH=4) corroborating NOV; the inflation runs through NOV≥3 + a borderline **TCH=3**, not novelty alone.
- The rule was therefore replaced by its **operative form — the "narrative-or-standout floor"** (pattern `auto-2026-07-001`): a Tier-2 call requires `NAR≥3` OR at least one dimension `≥4`; a flat wall of 3s (`NAR≤2`, nothing `≥4`) is Tier 1.
- **Simulated impact:** downgrades 4 flat-narrative posts (`iae-product-architecture`, `the-api-is-the-real-boundary`, `agent-allowlist-consistency-gate`, `coverage-vs-mutation-testing-rules-engine`) → **June T2 50%→38%, T1 46%→58%** (last-30: T2 53%→43%). Every genuinely-strong post is preserved (each has NAR≥3 or a dimension≥4), and it does not re-create the Jan/Feb over-deflation.
- Wired into `references/content-tier-classification.md`, `references/classify-day.md`, and `agents/blog-classifier.md` (gate + override + anchor enforcement). Takes effect on the next daily run; re-verify the *live* distribution at the August calibrate.

## Note

June 2026 has its own completed report (`calibration-2026-06.md`); this file is the interim creep check and does not supersede it. The August 1 monthly cron will produce the full July report once July has a complete sample.
