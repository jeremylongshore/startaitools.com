# Calibration Report: July 2026

> Full-month report, generated 2026-08-01. The mid-cycle check written 2026-07-03
> (3 July decisions, effectively a June post-mortem) is preserved at
> `calibration-2026-07-interim-0703.md`.

## Summary

- Decisions analyzed: **35** classifier records (31 unique dates; 3 multi-post days)
- Feedback records available: **26** of 35 (sweep last ran 2026-07-26)
- Overall health: **MISCALIBRATED**

July is the worst month on record for tier discipline, and it failed in two
independent ways that must not be conflated:

1. **Real inflation.** Tier 1 collapsed to 17.1% against a 60–70% target. Every
   dimension's mean rose month-over-month. Seven posts wore a Tier-2 badge at
   Tier-1 *length*.
2. **A broken measuring instrument.** The auto-sweep grader demoted 54% of July
   posts on a 14-word title keyword list. The headline Brier of 0.5524 is mostly
   grader error, not classifier error. Graded against its own structural signal
   the Brier is 0.2609.

The third finding is the one that matters most: **the anti-inflation pattern
adopted on 2026-07-03 never fired once all month.** It gates on `NAR<=2`, and
July's NAR scores inflated past the gate. A downgrade rule keyed to raw scores
cannot survive drift in those same scores.

## Tier Distribution

| Tier | Count | Actual % | Expected % | Status |
|------|-------|----------|------------|--------|
| 1    | 6     | 17.1%    | 60–70%     | **WARN** — starved, 43 pts below floor |
| 2    | 24    | 68.6%    | 25–35%     | **WARN** — 34 pts above ceiling |
| 3    | 5     | 14.3%    | 5–10%      | **WARN** — overuse |

Trend: **inflating** and accelerating.

| Month | n | T1 | T2 | T3 |
|-------|---|-----|-----|-----|
| 2026-04 | 22 | 36.4% | 36.4% | 27.3% |
| 2026-05 | 21 | 4.8% | 61.9% | 33.3% |
| 2026-06 | 24 | 45.8% | 50.0% | 4.2% |
| **2026-07** | **35** | **17.1%** | **68.6%** | **14.3%** |

June's partial recovery (T1 45.8%) did not hold. Tier 2 has now been above its
band for three consecutive months — the grade-creep trigger from Step 2 fires.

**The tripwire worked; the response loop did not.** `blog-tier-creep-guard.py`
detected the breach and stayed breached the entire month (state:
`t2_high: 67, t1_low: 20, t3_high: 13`, span `2026-06-26..2026-07-25`). Weekly
guard logs exist for Jul 5, 12, 19, 26. Hysteresis correctly suppressed repeat
alerts after onset — working as designed, but it means a persistent breach went
four weeks without a corrective action. Detection is not the gap. Correction is.

## Calibration Accuracy

- **Brier score as graded: 0.5524** (n=26) — "seriously miscalibrated" band
- **Brier score vs. the grader's own structural signal: 0.2609**
- Accuracy as graded: 6/26 (23.1%); vs structural: 17/26 (65%)
- Mean confidence: 0.840

**The as-graded number is not trustworthy.** `feedback-sweep.py` computes two
signals and then throws the better one away:

```
structural_tier(lines)          # <=145 -> T1, <=260 -> T2, else T3
apparent_tier(struct, title)    # demote unless the TITLE contains a keyword
```

`apparent_tier` demotes any Tier-2 whose title lacks a word from a 14-item list
(`pattern`, `framework`, `playbook`, `rubric`, `protocol`, …) and any Tier-3
lacking both an artifact word *and* a drama word. This blog's house title voice
is declarative negation — "Exit 0 Is Not Success", "Empty Is Not Clean",
"Temporary Is Not a Plan" — which contains none of those keywords by
construction. So the grader demotes the house style.

Demotion rate by month, all one-directional:

| Month | title-demoted | Brier as-graded | Brier vs structural |
|-------|---------------|-----------------|---------------------|
| 2026-06 | 8/24 (33%) | 0.4083 | 0.2025 |
| 2026-07 | 14/26 (54%) | 0.5524 | 0.2609 |
| all-time | 50/188 (27%) | 0.3087 | 0.1654 |

Worked example — 2026-07-22, "Wrong-Mode Green Is Not a Gate", 209 lines:
`structural_tier=2`, classifier said 2, **they agree**. The title heuristic saw
no keyword, demoted to 1, and the sweep recorded `was_correct: 0`. Thirteen more
July records are the same shape.

Real classifier drift and grader noise are moving in the same direction, which
is why the two must be separated before either is acted on. **Both are real.**
Even scored against the structural signal alone, July's 0.2609 is the worst
month on the honest metric too (all-time 0.1654).

## Decision Quality Matrix

| | Good Outcome (correct) | Bad Outcome (incorrect) |
|---|---|---|
| **High Confidence (>0.7)** | 6 | **20** |
| **Low Confidence (<0.7)** | 0 | 0 |

Every July decision was made above 0.70 confidence — the classifier was never
once unsure. Combined with 20 disagreements, this is the textbook
high-confidence/bad-outcome quadrant: not bad luck, a blind spot. There is no
"lucky" quadrant to learn from because the classifier never expressed doubt.

Confidence range 0.76–0.90 with mean 0.840, essentially flat against June's
0.850 — confidence did not move while accuracy fell. Confidence is currently
carrying no information.

## Dimension Analysis

Mean score, June → July:

| Dim | Jun | Jul | Δ |
|-----|-----|-----|-----|
| NOV | 2.50 | 2.68 | +0.18 |
| ARC | 2.50 | 3.03 | **+0.53** |
| NAR | 2.29 | 3.10 | **+0.81** |
| TCH | 3.12 | 3.48 | +0.36 |
| SCP | 2.71 | 2.94 | +0.23 |
| RPR | 2.62 | 3.00 | +0.38 |

**Every dimension rose. Nothing in the underlying work changed that much.**

The sharper signal is the rate at which a `>=4` was awarded at all:

| Dim | Jun (n=24) | Jul (n=35) | award rate Jun → Jul |
|-----|-----------|-----------|----------------------|
| ARC | 3 | 12 | 12.5% → 34.3% |
| NAR | 3 | 13 | 12.5% → 37.1% |
| TCH | 7 | 18 | 29.2% → 51.4% |
| SCP | 4 | 10 | 16.7% → 28.6% |
| RPR | 2 | 7 | 8.3% → 20.0% |
| NOV | 1 | 2 | 4.2% → 5.7% |

A `4` is supposed to be a standout. In July, TCH awarded one on **half** of all
posts, and NAR — the dimension that gates Tier 2 — tripled its award rate. NOV
is the only dimension that held its anchor, which is itself telling: NOV is the
dimension the June pattern taught the classifier to be suspicious of, and it is
the one that did not drift. **The anti-inflation attention moved to NOV and the
pressure escaped through ARC/NAR/TCH.**

Anchor collapse is clearest on the short posts:

| Date | Lines | Dims | dims ≥4 |
|------|-------|------|---------|
| 2026-07-14 | **95** | NOV3 ARC4 NAR3 TCH4 SCP4 RPR4 | 4 |
| 2026-07-15 | **83** | NOV3 ARC3 NAR4 TCH4 SCP3 RPR4 | 3 |
| 2026-07-20 | 127 | NOV3 ARC4 NAR3 TCH4 SCP3 RPR4 | 3 |
| 2026-07-23 | 137 | NOV3 ARC4 NAR2 TCH3 SCP4 RPR3 | 2 |

An 83-line post carrying three standout dimensions is not a scoring judgment
call, it is a broken anchor.

Seven July posts were classified Tier 2+ but written at Tier-1 length (≤145
lines): 07-01 (116), 07-02 (116), 07-14 (95), 07-15 (83), 07-18 (134), 07-20
(127), 07-23 (137). The classification and the artifact disagree with each
other, deterministically and after the fact. **Nothing in the pipeline currently
checks that.**

## Anti-Inflation Effectiveness

Flags recorded across 35 July decisions (free-text, so counts are indicative):

| Count | Flag |
|-------|------|
| 3 | `none triggered` |
| 2 | `tier2-share-50pct-past-14d-conservative` |
| 2 | `14-day distribution self-check applied: Tier 1 at 0%` |
| 1 | `narrative-or-standout floor (2026-07-03): NAR=2 and no dimension>=4` |
| 1 | `novelty-alone-doesnt-escalate (rule 8)` |
| 1 | `high-scope-alone-not-escalation` |
| 1 | `tier3-gate-failed-on-NAR (reference not narrative)` |
| 1 each | ~12 further one-off prose flags |

Two structural problems:

1. **The Step-0 distribution check fired and was overruled.** Two records
   explicitly note "Tier 1 at 0%" over the trailing window and classified Tier 2
   anyway. An advisory check that is acknowledged and then ignored is not a gate.
2. **Flags are free text.** Nineteen distinct flag strings across 35 decisions
   means trigger frequency cannot be counted reliably month over month. This is
   the third calibration cycle where flag analysis has been degraded by this.

### The learned pattern was routed around

`auto-2026-07-001` ("Tier-2 narrative-or-standout floor", adopted 2026-07-03)
requires:

```
max_nov_tch_nar >= 3  AND  count_ge3 >= 2  AND  nar <= 2  AND  max_all <= 3  ->  cap at Tier 1
```

Every one of the 14 July records that ran the pattern engine logged
`applied_patterns: []`. **Simulated over all 35 July decisions, the rule fires
zero times.**

Why: `nar <= 2` held on 16 of 24 June posts but only 8 of 35 July posts, and
`max_all <= 3` is defeated by the ARC/NAR/TCH `>=4` award-rate tripling above.
The rule was calibrated on June's score distribution and July's distribution
moved out from under both of its clauses within four weeks of adoption.

Worse, verified against the rebuilt index: **`v_pattern_usage` is empty. No
pattern has ever fired at classification time, across the entire corpus.** Of
the 14 decisions that carry an `applied_patterns` field, 0 have a non-empty
list. The `times_applied: 7` on `auto-2026-07-001` is a *retroactive backfill*
count — historical decisions whose scores the rule would have matched — not
production firings. The pattern engine has never downgraded a single post in
the live pipeline.

This is the central lesson of the month. A cap rule expressed on raw dimension
scores is only as stable as the anchors behind those scores. When the anchors
erode, the rule silently stops binding — and reports `applied_patterns: []`,
which reads identically to "nothing needed downgrading." Two months of
apparent anti-inflation machinery have produced zero live corrections.

## Emergent Patterns

**Candidate rules simulated against all 199 historical classifier decisions.**
Percentages are T1/T2/T3 after applying the cap:

| Rule | Apr | May | Jun | Jul |
|------|-----|-----|-----|-----|
| *(current, `auto-2026-07-001`)* | no change | no change | no change | **no change** |
| **A**: T2 needs NAR≥4 or two dims≥4 | 59/14/27 | 24/43/33 | 75/21/4 | 34/51/14 |
| **B**: nothing ≥4 at all → T1 | 36/36/27 | 14/52/33 | 63/33/4 | 20/66/14 |
| **C**: T2 needs NAR≥3 AND a dim≥4; T3 needs NAR≥4 AND two dims≥4 | 50/23/27 | 19/48/33 | 75/21/4 | 29/57/14 |

**No score-keyed cap rule fixes July.** The most aggressive candidate (A) still
leaves July at 51% Tier 2 while over-deflating June to 20.8% Tier 2 — below the
band, trading one breach for another. That is the diagnosis, not a failure of
search: you cannot cap your way out of anchor drift, because the cap reads the
drifted scores.

Candidate **B** is the one honest, low-risk change available: it is
`auto-2026-07-001` with the `nar <= 2` clause removed — precisely the clause the
drift routed around. It moves every month toward its band and pushes no month
out of one (T2 floor held at ≥25% in all four months; T1 never exceeds 70%). It
catches 11 historical decisions including 2026-07-05, which scored a flat
NOV2/ARC2/NAR3/TCH3/SCP2/RPR2 and still shipped as Tier 2.

It is a strict improvement, not a fix. Adopted below with that caveat recorded.

## Recommendations

1. **Fix the grader before trusting another Brier score.** `apparent_tier()` in
   `scripts/feedback-sweep.py` should not demote on a title keyword list —
   against this blog's declarative-negation title voice it demotes over half of
   all posts one-directionally. Options: drop the title heuristic and grade on
   `structural_tier` alone (restores all-time Brier to 0.1654), or replace it
   with a body-scan for the artifact signal instead of a title-scan. Until then,
   `was_correct` in `feedback.jsonl` is measuring the title style, not the
   classification. **This is the highest-leverage item — every other metric here
   is downstream of it.**

2. **Recalibrate the `>=4` anchors — this is the real inflation fix.** ARC and
   NAR tripled their `>=4` award rate in one month; TCH now awards a standout on
   half of all posts. Add explicit negative examples to
   `~/.claude/skills/blog-backfill/references/content-tier-classification.md`
   using July's own records: an 83-line post cannot carry three dimensions at 4
   (2026-07-15), and a 95-line post cannot carry four (2026-07-14). Anchor
   erosion is the root cause; cap rules are downstream of it and the simulation
   above shows they cannot substitute for it.

3. **Add a deterministic tier↔length consistency gate.** Seven July posts shipped
   a Tier-2 classification at Tier-1 length. That contradiction is checkable in
   bash after drafting and before landing — no LLM judgment required. Wire it
   into `blog-land.sh` as a precondition (quarantine or auto-downgrade on
   mismatch), the same way the sentinel and hugo-build gates already work. It is
   the one signal in the whole system that cannot be talked up by a classifier
   grading itself. Note this needs a new feature in `apply-patterns.py` (length
   is not currently an available feature) or, better, enforcement at the land
   step where the artifact actually exists.

4. **Promote the Step-0 distribution check from advisory to binding.** Two July
   records observed "Tier 1 at 0%" over the trailing 14 days and classified Tier
   2 regardless. If the trailing window is out of band, a Tier-2+ classification
   should require an explicit named artifact or be capped. An advisory check that
   is overruled in-record is worse than no check — it produces an audit trail
   that looks like diligence.

5. **Close the tier-creep-guard loop.** The guard detected the breach on Jul 5
   and it stayed breached through Jul 26 with no corrective action. Hysteresis is
   right to suppress weekly nagging, but a breach persisting past ~2 weeks should
   escalate rather than stay quiet — currently the only escalation path is this
   monthly report, which arrives up to 30 days late.

6. **Make `anti_inflation_flags` an enum.** Nineteen distinct free-text strings
   across 35 decisions makes trigger-frequency analysis unreliable, for the third
   calibration cycle running. A fixed vocabulary with an optional free-text note
   field preserves the prose without destroying the counts.

7. **Data hygiene.** Four July classifier records (07-27 ×2, 07-28, 07-30) carry
   `tier` and `confidence` but no `dimensions` block, and are invisible to
   dimension analysis and to the pattern engine. Nine July decisions still have
   no feedback record (sweep last ran 2026-07-26) — re-run
   `blog-feedback-sweep.sh` after recommendation 1 lands, not before, or it will
   write 9 more title-heuristic verdicts into the append-only log.

## Actions Taken

- Appended **`auto-2026-08-001`** to `patterns.jsonl` (candidate B — the `nar<=2`
  clause removed from the July rule); marked `auto-2026-07-001` inactive with a
  `retired_reason` recording that it never fired.
- Ran `apply-patterns.py backfill`: `auto-2026-08-001` matches 25 of 275
  decisions, of which **11 are effective downgrades** (tier ≥2 → 1). The other 14
  are Tier-1 records where `cap_tier(1)` is a no-op. `times_applied` counts rule
  matches, not effective downgrades — noted in the pattern record so the number
  is not misread later.
- Rebuilt `index.db` — imported decisions=199, feedback=188, patterns=3.

### Defect found and fixed while authoring the rule

The first draft of `auto-2026-08-001` was a bare `max_all <= 3`. Backfill
reported 180 matches against an expected 11, which surfaced a real defect:
`features()` in `apply-patterns.py` defaults **every absent dimension to 0**, so
`max_all <= 3` is trivially true for the **80 corpus records that carry no
`dimensions` block at all** — including four July records (07-27 ×2, 07-28,
07-30). The rule would have silently capped those to Tier 1.

`auto-2026-07-001` was shielded from this only by accident, via clauses it had
for unrelated reasons. The shipped rule adds `count_ge3 >= 2` as an explicit
guard: false for an all-zeros record, true for any genuine flat-wall-of-3s post
(2026-07-05 has `count_ge3 == 2`). Re-verified: 25 matches, **0** with a missing
dimensions block, 11 effective downgrades — matching the simulation exactly.

**This is a latent trap for every future pattern**, and a candidate eighth
recommendation: `features()` should distinguish "scored 0" from "not scored" and
refuse to evaluate rules against records with no dimensions, rather than
silently treating them as all-zeros.

### Known non-fatal issues observed during rebuild

- 7 `feedback.jsonl` records were skipped on import (`NOT NULL constraint failed:
  feedback.original_tier`). JSONL remains source of truth; the index undercounts
  feedback by 7 (188 of 195). Pre-existing, not introduced here.

Recommendations 1–7 are **not** implemented — they touch the grader, the rubric
references, and `blog-land.sh`, and are Jeremy's call.
