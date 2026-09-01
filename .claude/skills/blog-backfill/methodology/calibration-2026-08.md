# Calibration Report: August 2026

## Summary

- Classifier decisions analyzed: **31** (every day of the month; cadence 100% daily)
- Feedback records covering them: **29** (all `structural_auto_confirm`; 08-30 and 08-31 not yet swept)
- Overall health: **MISCALIBRATED — Tier-2 saturation, second consecutive month**

Two things happened in August, and they point in opposite directions.

July's top recommendation was executed: the title heuristic in `feedback-sweep.py` was
retired on 2026-08-11, and the grader now reads line count alone. That repaired the
measurement instrument. Post-retirement Brier is **0.0965** against **0.5524** in July.

July's other two recommendations — recalibrate the `>=4` anchors, and add a
deterministic tier-length gate — were **not** executed. August is the clean
demonstration of what July's own report predicted would happen without them: the
learned cap rule that shipped on 2026-08-01 caught **zero** Tier-2 posts all month, and
the tier distribution did not move at all.

The distribution is not creeping any more. It has saturated, and it is stable at
roughly twice the Tier-2 ceiling.

## Tier Distribution

| Tier | Count | Actual % | Expected % | Status |
|------|-------|----------|------------|--------|
| 1 | 8 | 25.8% | 60-70% | **WARN — severe deflation (34 pts below floor)** |
| 2 | 20 | 64.5% | 25-35% | **WARN — 30 pts above ceiling** |
| 3 | 3 | 9.7% | 5-10% | OK (at ceiling) |

Trend: **saturated, worsening within the month.**

| Month | n | T1 | T2 | T3 |
|-------|---|-----|-----|-----|
| 2026-04 | 22 | 36% | 36% | 27% |
| 2026-05 | 21 | 5% | 62% | 33% |
| 2026-06 | 24 | 46% | 50% | 4% |
| 2026-07 | 31 | 19% | 65% | 16% |
| 2026-08 | 31 | **26%** | **65%** | **10%** |

Tier 2 held at 64.5% for two months running. Tier 3 came back into band (16% → 10%),
which is the one genuine improvement in the distribution — the T3 gate is holding.
All of that recovery came out of Tier 2's neighbour, not out of Tier 2.

Within August the split got worse, not better:

| Half | n | T1 | T2 | T3 |
|------|---|-----|-----|-----|
| 08-01 .. 08-15 | 15 | 33% | 60% | 7% |
| 08-16 .. 08-31 | 16 | 19% | 69% | 12% |

The tier-creep guard is aware and has gone quiet by design. Its state file
(`~/.local/state/blog-tier-creep-guard/state.json`) reads `"status": "breached"` with
high-water marks `t2_high: 73, t1_low: 13, t3_high: 13` over span
`2026-07-31..2026-08-29`. Hysteresis is suppressing the weekly alert because the breach
is persistent rather than worsening past its high-water. That is correct behaviour and
it is also why nobody has been paged about a two-month breach.

## Calibration Accuracy

**Brier score must be reported in two parts this month, because the grader changed
mid-month.**

| Cohort | n | Brier | Accuracy |
|---|---|---|---|
| Graded before 2026-08-11 (retired title heuristic) | 8 | — contaminated | 2/8 |
| Graded 2026-08-11 onward (structural grader) | 21 | **0.0965** | **90%** |
| All-time as stored in feedback.jsonl | 222 | 0.3031 | 59% |

The all-time 0.3031 is not a real signal. 201 of those 222 records were graded by the
title heuristic, which the sweep's own retirement note documents as making 187 of 206
posts ineligible for a Tier-2 grade at any length and having no branch that could ever
raise a tier. Six of August's eight recorded mismatches (08-01 through 08-08) are
artifacts of that broken grader, not classification errors.

**Do not read 0.0965 as "the classifier is well calibrated." It is close to circular.**
The classifier assigns a tier, the tier tells the writer a target length, and the grader
checks whether the post hit that length. It measures writer compliance with the assigned
tier. It cannot detect an inflated tier that the writer then dutifully wrote 200 lines
for — which is precisely the failure mode the distribution table above is showing.

Both surviving mismatches under the clean grader are threshold noise, not judgment:

| Date | Classifier | Grader | Lines | Boundary |
|---|---|---|---|---|
| 2026-08-18 | T2 | T1 | 144 | T1 ceiling is 145 — missed by 1 line |
| 2026-08-27 | T2 | T3 | 263 | T2 ceiling is 260 — missed by 3 lines |

Twenty-one posts, zero substantive disagreements, two off-by-a-few-lines. That is a
grader with almost no resolution, not a classifier with almost no errors.

Confidence histogram (August, 31 decisions), mean **0.834**:

```
0.78  ######      6
0.80  ###         3
0.82  ####        4
0.84  #           1
0.85  #####       5
0.86  ########    8
0.87  #           1
0.88  ##          2
0.90  #           1
```

Confidence is drifting down very slightly month over month (0.850 → 0.840 → 0.834),
which is the classifier registering its own discomfort without changing its output.

## Decision Quality Matrix

|  | Good Outcome (correct) | Bad Outcome (incorrect) |
|---|---|---|
| **High Confidence (>0.7)** | 21 | 8 |
| **Low Confidence (<0.7)** | 0 | 0 |

Every August decision was made above 0.78. There is no "Lucky" quadrant and no low-
confidence quadrant at all — the classifier is never unsure. Six of the eight
high-confidence-wrong cells belong to the retired grader; under the clean grader the
cell holds only the two boundary cases above.

The empty bottom row is itself the finding. A classifier that has been 30 points outside
its Tier-2 band for two months and never once drops below 0.78 confidence is not
modelling its own uncertainty. The anti-inflation flags are where that uncertainty is
being written down, and they are not connected to anything that binds.

## Dimension Analysis

August averages across 31 posts:

| Dim | Avg | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| NOV | 2.58 | 13 | 18 | 0 | 0 |
| ARC | 3.06 | 8 | 13 | 10 | 0 |
| NAR | 3.48 | 1 | 14 | 16 | 0 |
| TCH | 3.42 | 3 | 12 | 16 | 0 |
| SCP | 3.42 | 1 | 17 | 12 | 1 |
| RPR | 2.90 | 8 | 18 | 5 | 0 |

By assigned tier:

| Tier | n | NOV | ARC | NAR | TCH | SCP | RPR |
|---|---|---|---|---|---|---|---|
| 1 | 8 | 2.25 | 2.50 | 2.88 | 2.88 | 3.00 | 2.38 |
| 2 | 20 | 2.65 | 3.25 | 3.65 | 3.55 | 3.50 | 3.05 |
| 3 | 3 | 3.00 | 3.33 | 4.00 | 4.00 | 4.00 | 3.33 |

Tiers 1 and 2 are separated by about a third of a point on every dimension. That is not
a category boundary, it is a rounding difference, and it is why the boundary is not
holding.

**Anchor inflation is the root cause, and it is measurable.** Share of posts awarded
`>=4` on each dimension:

| Month | NOV | ARC | NAR | TCH | SCP | RPR | any >=4 | max <=3 |
|---|---|---|---|---|---|---|---|---|
| 2026-04 | 23% | 36% | 32% | 36% | 59% | 14% | 64% | 36% |
| 2026-06 | 4% | 12% | 12% | 29% | 17% | 8% | 46% | 54% |
| 2026-07 | 6% | 39% | 42% | 58% | 32% | 23% | 77% | 23% |
| 2026-08 | **0%** | 32% | **52%** | **52%** | 42% | 16% | **84%** | **16%** |

NAR and TCH now award a standout to more than half of all posts. A `>=4` that fires on
half the corpus is not a standout, it is the median. In June, 54% of posts topped out at
3; in August only 16% do. The anchors have eroded exactly as July's report warned, and
nothing was done to the reference file to stop it.

NOV is the mirror-image anomaly: it awarded `>=4` on **zero** posts in August, down from
23% in April. The anti-novelty rules (rule 8, `first-time-for-me-not-novel`) have worked
so thoroughly that NOV has stopped contributing signal at all. It is now a dead
dimension, and the escalation load it used to carry has moved onto NAR and TCH.

## Anti-Inflation Effectiveness

**All 31 of 31 August posts carry at least one anti-inflation flag.** The distribution
did not move. A control that fires on 100% of cases and changes no outcome is not a
control, it is a log line.

Flag frequencies:

| Count | Flag |
|---|---|
| 16 | volume-not-quality |
| 10 | busy-not-distinguished |
| 6 | first-time-for-me-not-novel |
| 5 | confidence-gated downgrade applied |
| 4 | high-scope-alone-does-not-escalate |
| 4 | volume-not-quality checked |
| 3 | distribution-pressure |
| 3 | tch-capped-at-3 |
| 3 | scp-capped-at-3 |
| 3 | no-dimension-reaches-4 |
| 3 | step-0-distribution-breached |

Three of these deserve comment. `distribution-pressure` and `step-0-distribution-breached`
fired only 3 times each in a month where the distribution was breached on all 31 days —
Step 0 is reading the rolling window but only occasionally acting on it. And
`volume-not-quality` appears under two different spellings (16 + 4), as does the TCH cap
(`tch-capped-at-3` 3 times, `TCH capped at 3 under anchor enforcement` 3 times). The flag
vocabulary is free text, so flag counts undercount by an unknown amount and cannot be
trended reliably.

### The learned pattern is already fully routed around

`auto-2026-08-001` (Tier-2 standout floor) shipped 2026-08-01, superseding
`auto-2026-07-001` after its `nar<=2` clause was defeated by anchor drift. It fires on
`count_ge3 >= 2 AND max_all <= 3 → cap_tier(1)`.

Its rule-match count is 25 across the whole corpus. Its effect on August:

| Month | tier>=2 posts | rule would cap | % |
|---|---|---|---|
| 2026-06 | 13 | 4 | 31% |
| 2026-07 | 25 | 1 | 4% |
| 2026-08 | 23 | **0** | **0%** |

**Zero.** Not one Tier-2 or Tier-3 post in August had `max_all <= 3`, because 84% of
posts now carry a dimension at 4. The rule fired 5 times in August (08-12 through
08-16), and all five were on posts already classified Tier 1, where `cap_tier(1)` is a
no-op. The engine correctly recorded `applied_patterns` on those five and empty
elsewhere — the receipt is honest; there was simply nothing to cap.

This is the second consecutive supersession defeated by the same mechanism within one
month of shipping. The pattern's own evidence field predicted it verbatim: *"no
score-keyed cap rule fixes July, because the drift is in the anchors the rule reads."*
August confirms it. **Stop writing cap rules keyed on scores until the anchors that
produce the scores are fixed.** A third supersession will be routed around in September
the same way.

### Pattern-engine receipt coverage

Ten of 31 August decisions carry no `pattern_engine` receipt: 08-01 through 08-09 and
08-11. Coverage becomes continuous from 08-10 onward (08-11 excepted). `blog-land.sh`
gates on the receipt at line 209, so these predate the gate being effective. Not a
current defect; noted so the gap in the audit trail is explained rather than
rediscovered.

## Emergent Patterns

**The tier-length contradiction has a second, unreported half.** July flagged that
Tier-2 posts were shipping at Tier-1 length. August shows Tier 1 has the same problem in
the other direction — every Tier-1 post undershoots its own declared band.

August line counts against the declared bands (T1 80-140, T2 150-250, T3 300-500):

| Tier | Lines |
|---|---|
| T1 | 18, 43, 72, 72, 73, 73, 76, 78 |
| T2 | 105, 124, 144, 154, 157, 162, 162, 166, 186, 191, 197, 200, 209, 217, 229, 233, 263, 301 |
| T3 | 314, 537, 556 |

**All 8 Tier-1 posts fall below the 80-line floor** (median 72.5). **3 of 20 Tier-2 posts
fall below the 150-line floor.** Both tiers are systematically short, and the two facts
together suggest the writer has settled on two habitual lengths — roughly 72 and roughly
190 — largely independent of the declared band.

This is not a new rule for `patterns.jsonl`. A cap rule cannot express it, and adding a
fourth score-keyed pattern would repeat the mistake documented above. It belongs in a
deterministic gate in bash. **No new pattern is being written this month, deliberately.**

Two smaller observations, both below the 10-decision reliability bar and recorded only
for next month to test:

- The 08-12..08-16 Tier-1 run is the month's only sustained Tier-1 stretch and is the
  only window where the cap rule fired. Worth checking in September whether an explicit
  Step-0 breach response, rather than the rule, produced it.
- NOV has awarded `>=4` zero times in 31 days. If that holds through September, NOV
  should either be re-anchored or formally retired from escalation, since a dimension
  that never reaches standout adds nothing to a standout-floor test.

## Recommendations

1. **Recalibrate the `>=4` anchors in
   `~/.claude/skills/blog-backfill/references/content-tier-classification.md`. This is
   the only item that matters and it is now two months overdue.** It was July's
   recommendation 2, it was not done, and August is the controlled experiment proving
   nothing downstream substitutes for it: the pattern engine's catch rate went 31% → 4%
   → 0% while flags fired on 100% of posts. Use August's own records as negative
   examples — a 105-line post scoring SCP=4 (08-01), and a 124-line post scoring NAR=4
   (08-06). Target NAR and TCH specifically; both now award a standout to more than half
   the corpus. The reference currently contains exactly one length-based negative example
   (line 218, the 114-line Tier-3 lesson) and no July- or August-derived ones.

2. **Add the deterministic tier-length gate to `blog-land.sh`.** July's recommendation 3,
   also not done — `blog-land.sh` contains no line-count check of any kind today. The
   contradiction is checkable in bash with no LLM judgment: read `.tier` from the
   classifier record, count body lines, and quarantine or auto-downgrade on a band
   mismatch, alongside the existing sentinel, pattern-receipt, and hugo-build
   preconditions. August gives it work to do on day one: all 8 Tier-1 posts and 3 Tier-2
   posts violate their band. Land it with the band floors relaxed to match reality (a
   72-line Field Note is fine) or fix the declared bands — but stop shipping a declared
   band that 11 of 31 posts contradict.

3. **Make the grader measure something the classifier does not already determine.** The
   0.0965 Brier is close to unfalsifiable: tier sets target length, grader checks length.
   Either grade the body for the artifact signal the rubric actually claims to reward
   (the retirement note explicitly recommended a body-scan over the title-scan, and only
   the removal half was implemented), or stop reporting Brier as a classifier-quality
   metric and label it what it is — a writer-compliance metric.

4. **Do not ship a fourth score-keyed cap pattern.** Two supersessions have now been
   routed around by anchor drift within a month each. `auto-2026-08-001` stays active —
   it is still a strict improvement and would bind again once the anchors are fixed — but
   no new cap rule should be written until recommendation 1 lands and the `>=4` award
   rate drops back toward June's 46%-any-standout level.

5. **Normalize the anti-inflation flag vocabulary to a fixed enum.** Free-text flags
   produced at least two duplicate spellings this month (`volume-not-quality` /
   `volume-not-quality checked`, and two forms of the TCH cap), so trigger counts are
   undercounted by an unknown margin and cannot be trended. A closed list in the skill
   reference makes this table trustworthy next month.

6. **Consider lowering the tier-creep guard's suppression on a multi-month breach.** The
   guard is behaving exactly as designed — the breach is persistent, not worsening, so it
   is silent. But a breach that has been open since July and is 30 points wide should
   escalate on duration, not only on depth. A monthly re-alert at breach-age 30 days
   would have surfaced this without the calibration run.
