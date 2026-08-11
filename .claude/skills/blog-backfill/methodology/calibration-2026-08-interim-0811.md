# Calibration Report: August 2026 (interim, through 2026-08-09)

**Run:** mid-cycle, on request, 2026-08-11. Named `-interim-0811` so the Sept 1 cron
can still write the full `calibration-2026-08.md` without a collision, following the
`calibration-2026-07-interim-0703.md` precedent.

## Summary

- Decisions analyzed: **9** (August 1 to 9). Sample is below the 10-record floor, so
  every August-only figure here is directional, not conclusive. The corpus-wide
  findings below are not sample-limited and are the load-bearing part of this report.
- Feedback records: 8 paired
- Overall health: **MISCALIBRATED**, and for the same three reasons July was, none of
  which have been repaired.

**The one-line finding: the anti-inflation engine has still never fired, and the fix
shipped on August 1 could not have changed that, because the problem was never the
rule's conditions. Nothing verifies the engine was invoked.**

## Tier Distribution

| Tier | Count | Actual % | Expected % | Status |
|------|-------|----------|------------|--------|
| 1    | 1     | 11%      | 60-70%     | **WARN** |
| 2    | 7     | 77%      | 25-35%     | **WARN** |
| 3    | 1     | 11%      | 5-10%      | WARN |

Trend: **inflating**, fourth consecutive month out of band.

| Month | T1 | T2 | T3 | n |
|---|---|---|---|---|
| June | 45% | 50% | 4% | 24 |
| July | 17% | 68% | 14% | 35 |
| August (partial) | **11%** | **77%** | 11% | 9 |

Tier 1 has fallen every month since June and is now at one sixth of its floor. This
figure comes from `decisions.jsonl` directly and is independent of the grader defect
described below, so it survives that correction intact.

## Calibration Accuracy

- Headline Brier: **0.5368** (seriously miscalibrated, > 0.30)
- Brier against the structural signal alone, title gate removed: **0.2643**
- Sample: 8 paired records

The gap between those two numbers is measurement error, not classifier error, and
isolating it is the most important thing in this report.

### The grader cannot report "too low." It is structurally incapable of it.

`feedback-sweep.py:apparent_tier()` applies a title heuristic on top of the structural
(line-count) tier:

```
if apparent == 2 and not has_artifact: apparent = 1
if apparent == 3 and not (has_artifact and has_drama): apparent = 2
```

`has_artifact` is true only if the title contains one of **15 literal words**:
pattern, framework, methodology, principle, guard, guards, rubric, playbook, contract,
cascade, dual-layer, three-act, anti-pattern, checklist, protocol.

Measured across the whole live corpus (206 posts resolvable on disk):

| Measurement | Result |
|---|---|
| Titles containing any artifact word | **19 of 206 (9%)** |
| Titles containing any drama word | 7 of 206 (3%) |
| Structurally Tier 2+ posts (over 145 lines) | 79 |
| Of those, demoted to Tier 1 by the title gate alone | **72 of 79 (91%)** |
| Posts ineligible for a Tier 2 grade at any length or depth | **187 of 206** |

The house title voice is narrative by design ("The Drills Passed. Reality Did Not.",
"Empty Is Not Clean", "Three Copies of the Key, None of the Passphrase"). None of
those contain a jargon noun, because the voice deliberately avoids them. **The grader
therefore demotes the style and calls it a depth finding.**

And the function has no branch that raises a tier. `apparent <= struct_tier` always.
So a 100% one-directional downgrade rate is not evidence of classifier bias. **It is
the only output this function can produce when it disagrees at all.**

Corpus-wide, this is exactly what the record shows: of 201 graded posts, 90 mismatched
and **all 90 were downgrades, zero upgrades**. That number has been read as a
systematically over-confident classifier. It is not. It is a systematically
one-directional grader, and any conclusion drawn from the mismatch direction is void
until the gate is fixed.

## Decision Quality Matrix (Annie Duke 2x2), August

| | Good outcome (graded correct) | Bad outcome (graded incorrect) |
|---|---|---|
| **High confidence (>0.7)** | 2 | **6** |
| **Low confidence (<0.7)** | 0 | 0 |

Every August decision was made at high confidence. There is no low-confidence row at
all, which means the classifier never expressed doubt in nine consecutive calls. On a
month whose distribution is this far out of band, an absent low-confidence row is
itself a finding: the confidence signal is not carrying information.

The 6 in the high-confidence/incorrect quadrant is the quadrant the framework says to
study, but it is contaminated by the grader defect above and cannot be read yet.

## Dimension Analysis

Mean scores, June to August:

| Dimension | Jun | Jul | Aug | Aug rate of awarding >= 4 |
|---|---|---|---|---|
| novelty | 2.50 | 2.68 | 2.44 | 0% |
| arc | 2.50 | 3.03 | **3.44** | 55% |
| nar | 2.29 | 3.10 | **3.56** | 66% |
| tch | 3.12 | 3.48 | 3.11 | 33% |
| scp | 2.71 | 2.94 | **3.67** | 66% |
| rpr | 2.62 | 3.00 | 2.56 | 0% |

**NAR and SCP are the inflation carriers.** Both rose every month and both now award a
standout on two thirds of posts. SCP at 3.67 is the clearest anti-pattern: the rubric
holds that high scope alone must not escalate a tier, and SCP is now the highest-mean
dimension in the set. NOV fell while ARC, NAR and SCP rose, which is the signature of
tier being driven by how much the day touched rather than by how novel the work was.

## Anti-Inflation Effectiveness

This is the finding that matters, and it is worse than July reported.

| Check | Result |
|---|---|
| `auto-2026-08-001` active | yes, adopted 2026-08-01 |
| Historical decisions its rule matches | **25 of 294** |
| `v_pattern_usage` (live firings, whole corpus) | **empty** |
| August records carrying a non-empty `applied_patterns` | **0 of 9** |

All nine August posts logged `applied_patterns: []`.

July's report concluded "two months of apparent anti-inflation tooling, zero live
corrections," and shipped a fix: retire `auto-2026-07-001`, adopt `auto-2026-08-001`
with the drift-routed clause removed. That fix was correct on its own terms and
changed nothing, because the diagnosis was one layer too shallow. The rule was never
the problem. **The engine is not enforced.**

`SKILL.md:130` instructs the writing agent to pipe the classifier JSON through
`apply-patterns.py apply`. That is an instruction in prose. `blog-land.sh` verifies a
readiness sentinel, a classifier record, a step-8 audit addendum, append-only
integrity, the voice lint and a Hugo build. **It does not verify that the pattern
engine ran.** So an agent that skips step 2b, or runs it and discards the output,
produces `applied_patterns: []` and publishes with no gate objecting.

Three months, three rules, zero live corrections. The tooling exists, is tested,
matches 25 historical records, and has never once altered a published tier.

This is the same defect class the blog itself documented on 2026-08-09: a contract
that lives in prose with no required check behind it. The methodology system wrote
that post and is subject to it.

## Emergent Patterns

**No new pattern is proposed this cycle, deliberately.** Adding a fourth rule to a
file nothing reads at classification time would raise the count of dead rules and
change no outcome. The next pattern should be authored only after a gate exists that
proves patterns ran. Recorded here so the absence is not read as "no drift found."

## Recommendations

Ranked by leverage. Items 1 and 2 are the only ones that change behavior; everything
below them is downstream of both.

1. **Gate on the engine, do not instruct on it.** Add a precondition to
   `blog-land.sh`: if the classifier record for the target slug has no
   `applied_patterns` key, quarantine. Make it verify the engine ran, not that the
   agent said it would. This is a ten-line change to the existing precondition block
   and it is the single change that converts three months of dead tooling into live
   tooling. Everything else in this list is cosmetic until it lands.

2. **Fix or delete the grader's title gate.** 187 of 206 posts cannot be graded above
   Tier 1 at any length. Grade on the structural signal plus the dimension record,
   which the grader already computes and then overrides. Deleting `apparent_tier()`
   outright is defensible and takes the corpus Brier from 0.5368 to roughly 0.2643 by
   removing measurement error alone, with no change to classifier behavior. Until this
   lands, treat every mismatch-direction statistic in this system as void, including
   the 90-to-0 figure.

3. **Add a deterministic tier-to-length gate at land time.** Line count is the one
   signal a self-grading classifier cannot talk up. A Tier 2 record on an 83-line post
   should not publish. July flagged this; it was not built.

4. **Make the Step-0 distribution check binding.** Two July records noted Tier 1 at
   0% and classified Tier 2 anyway. An advisory check that is read and then overruled
   is not a check.

5. **Re-anchor NAR and SCP.** Both award a standout on two thirds of August posts.
   Use August's own records as negative examples when recalibrating the >= 4 anchors.

6. **Give the tier-creep guard a second metric.** It watches distribution only, and
   its hysteresis correctly suppressed a persistent breach while the underlying
   condition worsened. See the cadence note below.

## What this report does not claim

- The August sample is 9 records. Every August-only number is directional. The
  corpus-wide grader measurements (206 posts) and the pattern-firing findings are not
  sample-limited.
- The grader defect makes the classifier's true accuracy **unknown**, not good. The
  tier distribution breach is independently real and does not depend on the grader.
- No causal claim is made here about tone or subject matter. That is a separate audit.
