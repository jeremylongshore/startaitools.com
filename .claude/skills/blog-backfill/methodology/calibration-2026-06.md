# Calibration Report: June 2026

Generated 2026-07-01 from 24 classification decisions + 22 matched feedback records.
Grounded in Annie Duke's decision-quality framework: a good *decision* (well-anchored, flags fired) can still produce a bad *outcome* (grader disagreement). This report separates the two.

## Summary

- **Decisions analyzed:** 24 (real classifications; 8 `event: agent_audit` trail records and 4 audit addenda excluded)
- **Feedback records matched:** 22
- **Overall health:** **NEEDS ATTENTION** — recovered sharply from May's MISCALIBRATED collapse, but the correction overshot: Tier 1 is still below floor, Tier 2 still over-target, Tier 3 over-corrected to near-zero, and the confidence signal is fully compressed.

**The headline:** the May fix worked and it worked hard. Tier 1 went from 4.8% → 45.8% (a 10× recovery) and the Tier 3 overuse (33%) collapsed to 4%. But the pendulum swung past center. This is a *correcting* system that has not yet *converged*.

## Tier Distribution

| Tier | Count | Actual % | Expected % | Status |
|------|-------|----------|------------|--------|
| 1 | 11 | 45.8% | 60-70% | **WARN — below floor** |
| 2 | 12 | 50.0% | 25-35% | **WARN — inflated** |
| 3 | 1 | 4.2% | 5-10% | WARN — slightly under |
| 4 | 0 | 0.0% | rare | OK |

**Trend: sharp correction from collapse — improving, not yet converged.**

| Month | n | Tier 1 | Tier 2 | Tier 3 | Regime |
|-------|---|--------|--------|--------|--------|
| Apr 2026 | 22 | 36.4% | 36.4% | 27.3% | Tier 3 overuse (~3× ceiling) |
| May 2026 | 21 | **4.8%** | **61.9%** | 33.3% | Collapse — Tier 1 extinct, Tier 2 gate structurally always-true |
| Jun 2026 | 24 | **45.8%** | 50.0% | **4.2%** | Correction — Tier 1 recovered 10×, Tier 3 overuse cured |

The May report's three recommendations (inject the running 14-day distribution into the classify prompt; operationalize the confidence-gated downgrade; tighten the Tier 2 gate) were clearly **implemented** — the `distribution-self-check` anti-inflation flag fired on 11 of 24 June decisions, with explicit "past 14 days Tier 1 = X%" reasoning in the logs. The effect was large and in the right direction. Two residual gaps remain (below).

## Calibration Accuracy (Brier Score)

- **Brier score: 0.3782** (nominal band: "seriously miscalibrated")
- **Sample:** 22 matched feedback pairs
- **Agreement with structural grader: 50.0%**

**Read this number with three heavy caveats — it overstates the problem:**

1. **The "ground truth" is a deterministic structural grader, not human judgment.** The 152 `structural_auto_confirm` feedback records come from the Sunday `feedback-sweep.py` rubric grader, which credits line-count and structure and applies a hard Tier-1 floor. It does **not** credit novelty or narrative tension — the exact dimensions the LLM classifier keys on. So this Brier measures *classifier-vs-structural-grader divergence*, not calibration against a trusted oracle.
2. **All 11 disagreements are one-directional** — every single one is the classifier scoring *higher* than the structural grader. There is not one case of the classifier under-tiering. A one-directional error is a **bias**, not noise, and bias is fixable at the gate.
3. **The confidence signal is fully compressed** — every June decision lands between 0.72 and 0.93 (mean 0.850). The classifier **never expresses low confidence.** A confidence score that is always ≈0.85 carries no information and cannot gate a downgrade. This compression is itself the core calibration defect (see Recommendation 3).

## Decision Quality Matrix (Annie Duke 2×2)

| | Good Outcome (grader agrees) | Bad Outcome (grader disagrees) |
|---|---|---|
| **High Confidence (≥0.7)** | 11 | 11 |
| **Low Confidence (<0.7)** | 0 | 0 |

**The bottom row is empty — that is the finding.** The classifier operates exclusively in the high-confidence regime. The 11 "High Confidence + Bad Outcome" cells are the "good decision, bad outcome — learn why" quadrant: well-reasoned calls (all carry fired anti-inflation flags) that the structural grader still rejects, all in the over-tier direction. The absence of any low-confidence call means the confidence-gated downgrade rule can never trigger — it has no low-confidence inputs to act on.

## Dimension Analysis

| Dim | Avg | Distribution | Note |
|-----|-----|--------------|------|
| NOV (novelty) | 2.50 | 1:1 · 2:11 · 3:11 · 4:1 | **New inflation driver** — NOV≥3 on 46% of posts |
| ARC (arc) | 2.50 | 1:3 · 2:9 · 3:9 · 4:3 | balanced |
| NAR (narrative) | 2.29 | 1:4 · 2:12 · 3:5 · 4:3 | healthy — the discriminator is doing its job |
| TCH (technical) | 3.12 | 1:1 · 2:2 · 3:14 · 4:7 | TCH≥3 on 66% (was ~100% in May — improved) |
| SCP (scope) | 2.71 | 2:12 · 3:8 · 4:3 · 5:1 | SCP=2 on 50% (was always ≥3 in May — improved) |
| RPR (reproducibility) | 2.62 | 1:1 · 2:9 · 3:12 · 4:2 | balanced |

**The inflation mechanism has shifted.** In May the Tier 2 gate was structurally *always true* because TCH≥3 and SCP≥3 fired every day. June fixed that — TCH and SCP now vary. But a new driver replaced it: **novelty**. Of the 12 Tier-2 posts, **11 carry NOV≥3**; only one (`coverage-vs-mutation-testing-rules-engine`) is a bare TCH/SCP-floor escalation. So the residual Tier-2 inflation is now: *the classifier credits a novelty score of 3 on nearly half of daily backfill posts about routine CI/gate/healthcheck work, and NOV=3 is enough to clear the Tier 2 gate.*

This is a healthier failure than May's (novelty is at least a defensible escalation reason), but it is still the lever pulling Tier 1 below its 55% floor.

## Anti-Inflation Effectiveness

- **All 24 decisions carry ≥1 anti-inflation flag** (100% — up from May, strong process discipline).
- Flag frequency: `distribution-self-check` 11 · `scope-cap-held` 10 · `confidence-gated-downgrade evaluated` 9 · `narrative-gate` 3 · `novelty-cap` 1 · `arc-cap` 1.

The flags that fired are the *right* flags — the distribution self-check is directly responsible for the Tier 1 recovery. **The gap:** `novelty-cap` fired only once, even though novelty is now the dominant escalation dimension. The anti-inflation machinery is watching scope (10×) and distribution (11×) but is nearly blind to novelty inflation — precisely the lever that is now over-firing.

## Emergent Patterns

1. **Novelty is the successor inflation driver.** With the TCH/SCP always-on gate closed, NOV≥3 became the mechanism that escalates ~46% of posts to Tier 2 (11 of 12 Tier-2 posts). Candidate for `patterns.jsonl` — recorded this cycle.
2. **One-directional over-tiering vs the structural grader persists** (11/11 disagreements, classifier-higher). The two graders systematically disagree in one direction; they need reconciling — either the classifier trusts novelty too much, or the structural grader's Tier-1 floor is too aggressive. Both being one-directional means it is a bias, not variance.
3. **Confidence compression** — 0.72-0.93 range, zero low-confidence calls, ever. The confidence number is not currently a usable signal.

## Recommendations

1. **Cap novelty's escalation power at the Tier 2 gate.** NOV=3 alone should not clear Tier 2 for routine operational posts. Require the Tier 2 gate to key on a *narrative or reproducibility* second dimension (`NAR≥3 OR RPR≥3`) alongside a technical floor — not novelty alone. Novelty is the most subjective dimension and the one now driving the residual inflation; it should support a tier call, not create one. This directly targets the 11 over-tiered posts and should pull Tier 1 up toward its 60% floor without reviving Tier 3 overuse.

2. **Restore Tier 3 to its 5-10% band without re-inflating.** June produced exactly one Tier 3 (`the-wrong-product-built-perfectly`), and even that one the structural grader graded Tier 1. April/May over-produced Tier 3 (27%/33%); June over-corrected (4%). The target is a genuine 1-2 Tier 3s/month backed by a *reversal-with-insight* NAR≥4 signal — do not loosen the gate to hit the band; only escalate when the narrative genuinely earns it. Watch this next month; if it stays at 0-4%, the correction has overshot permanently.

3. **De-compress the confidence signal so the downgrade rule can fire.** The confidence-gated downgrade rule cannot work when confidence never drops below 0.85. Recalibrate the confidence anchors so that a Tier 2 call resting on a *single* gate-firing dimension at its floor (e.g., NOV=3 with NAR≤2) is emitted at confidence <0.80 — which should then trigger the automatic downgrade to Tier 1. Tie confidence to *how many independent dimensions* support the tier, not to how sure the model feels.

4. **Reconcile the LLM classifier and the structural grader (or annotate the divergence).** The 0.38 Brier is dominated by a known, one-directional, structural-vs-narrative disagreement. Either (a) teach the structural grader to credit a strong NAR/NOV signal so it stops floor-pulling every 150-line post to Tier 1, or (b) accept the divergence and report Brier *excluding* structural_auto_confirm records, using only human-confirmed feedback as ground truth. Right now the headline Brier looks alarming for the wrong reason.

5. **Restore the agent-audit trail.** `event: agent_audit` records exist for 06-05 → 06-13 then stop entirely (8 of 24 posts, 33%). The detailed agent-dispatch audit logging degraded mid-month. Classification records themselves are 100% complete, but the audit trail that proves *which quality-gate agents ran* is missing for the back two-thirds of the month.
