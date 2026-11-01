# Calibration Report: October 2026

## Analysis boundary and record counts

- **Window:** `[2026-10-01, 2026-11-01)`, local publish `date` on each record (UTC-06:00 host).
- **Ledger:** `python3 -B -m blogpipe tier-ledger --month 2026-10` is the count authority.
  It reports 22 classifier decisions, no duplicate classifiers, and 5 `shipped_tier`
  records. No record changes side of the boundary.
- **Record kinds in window:** 20 `classifier` + 2 legacy classifier records without
  `record_type` (10-01, 10-02, written by the pre-fix producer path) = 22 decisions;
  22 audit addenda; 5 `shipped_tier` records.
- **Feedback:** 21 records, each grading one October decision (date_assessed 10-04..10-25).
  The 10-25 decision has no feedback yet.
- **Patterns:** 3 rows; ruleset digest `c5339adab15f48ae` on all 22 receipts (unchanged
  since September).

| Source | Total lines | Used |
|---|---|---|
| `decisions.jsonl` | 447 | 22 classifier decisions + 5 shipped-tier records |
| `feedback.jsonl` | 282 | 21 (all grade an October decision) |
| `patterns.jsonl` | 3 | read; `times_applied` recomputed (see Step 9) |

### Coverage gap: 9 days with no decision

October has 22 decisions for 31 days. **10-22, 10-23, 10-24 and 10-26 through 10-31 never
produced a post.** This is a pipeline outage, not a classification result, but it shrinks
the sample and it is the most urgent finding in this report. From the run logs
(`~/.local/state/blog-backfill-daily/run-2026-10-{22..31}.log`) and the 10-31 producer logs:

1. The primary `auto` producer (MiniMax-M3) dies on `429 · Token Plan usage limit reached`.
2. The failover to `claude` starts **without `--agents`**, so `blog-classifier` resolves to
   `Agent type 'blog-classifier' not found`. The producer correctly refuses to write a post
   without a classifier and exits 0 with an empty write set, which the wrapper rejects as
   `FAILED (run write-set integrity)`.
3. Every daily retry re-fails the same way. Quarantine grew from 36 to 78 entries over the
   week (`QUARANTINE OVER LINE`).

The gates did their job: nothing half-made shipped. The fix is outside calibration
(quota, and `--agents` on the failover and repair launches). See recommendation 1.

---

## Summary

- Classifier decisions analyzed: **22** (71% daily cadence; 9-day outage at month end)
- Feedback records: **21** of 22
- Overall health: **NEEDS ATTENTION. The classifier is inflating again and the length
  gate is absorbing it.**

October's two tiers point in opposite directions:

- **Classifier T1 = 54.5% (12/22).** That trips the `T1 < 55%` inflation warning for the
  first time since August. Classifier T2 rose from 30% to 45%.
- **Shipped T1 = 77.3% (17/22).** That is above the 70% ceiling, as in September.
- The gap between them is the tier-length gate: **5 of 10 Tier-2 calls shipped as Tier 1**
  because the writer produced Field-Note length. In September it was 3 of 10.

The mechanism is specific and repeatable. **TCH is the new Tier-2 escalator.** TCH's `>=4`
rate went from 17% in September to 41% in October, and every TCH-only Tier-2 call this
month (4 of 4) shipped as Tier 1 by length. This is the fourth migration of the same
dynamic: NOV (June), NAR/TCH (July-August), SCP (September), TCH (October).

What improved: September's producer regression is fixed. Since the 10-06 enum sync
(PR #152) every flag is in the closed enum, `cadence_type` is populated, and
`rhetorical_structure` is a string on every record. The shipped tier is now recorded in
`decisions.jsonl` (September recommendation 1).

---

## Tier Distribution

### Classifier tier

| Tier | Count | Actual % | Expected % | Status |
|------|-------|----------|------------|--------|
| 1 | 12 | 54.5% | 60-70% | **WARN: below 55%, probable inflation** |
| 2 | 10 | 45.5% | 25-35% | **WARN: above ceiling** |
| 3 | 0 | 0.0% | 5-10% | Below band (first month with zero T3) |

### Shipped tier (after the `blog-land.sh` length gate)

| Tier | Count | Shipped % | Expected % | Status |
|------|-------|-----------|------------|--------|
| 1 | 17 | 77.3% | 60-70% | **WARN: above ceiling (deflation)** |
| 2 | 5 | 22.7% | 25-35% | **WARN: below floor** |
| 3 | 0 | 0.0% | 5-10% | Below band |

Breach attribution: the **T1 < 55% inflation rule fires on the classifier tier**. The
shipped tier breaches only the target bands, in the deflation direction. T3 > 15% did not
fire on either. "T2 rising three months running" did not fire: classifier T2 went
65% (Aug) → 30% (Sep) → 45% (Oct).

Trend: **classifier inflating, shipped stable and over-deflated.**

| Month | n | Classifier T1/T2/T3 | Shipped T1/T2/T3 |
|---|---|---|---|
| 2026-08 | 31 | 26% / 65% / 10% | 26% / 65% / 10% (gate not yet live) |
| 2026-09 | 30 | 67% / 30% / 3% | 77% / 20% / 3% |
| **2026-10** | **22** | **55% / 45% / 0%** | **77% / 23% / 0%** |

Within the month:

| Span | n | Classifier T1/T2 | Shipped T1/T2 |
|---|---|---|---|
| 10-01 .. 10-15 | 15 | 9 / 6 (60% / 40%) | 13 / 2 (87% / 13%) |
| 10-16 .. 10-25 | 7 | 3 / 4 (43% / 57%) | 4 / 3 (57% / 43%) |

September's recommendation 2 set a trigger: *"If October's first half also runs above 80%
T1, treat it as a regression of the Jan/Feb 2026 kind."* Shipped first-half T1 was 87%, so
the trigger literally fires. The cause is not the Jan/Feb one. The classifier was at 60%
T1, inside the band; the 87% comes from the length gate overruling four Tier-2 calls.
The second half then swung the classifier to 57% Tier 2.

---

## Calibration Accuracy

| Cohort | n | Brier | Accuracy |
|---|---|---|---|
| **October** | 21 | **0.191** (acceptable, above the 0.15 target) | 16/21 (76%) |
| September | 24 | 0.137 | 83% |
| August (clean grader) | 21 | 0.097 | 90% |

All five misses are length-gate downgrades on Tier-2 calls:

| Date | Conf | Dims NOV ARC NAR TCH SCP RPR | Body lines (lander) | Standouts (>=4) |
|---|---|---|---|---|
| 10-03 | 0.82 | 2 2 4 4 2 3 | **144** | NAR, TCH |
| 10-05 | **0.90** | 2 1 2 4 2 3 | 116 | TCH only |
| 10-07 | 0.82 | 2 2 3 4 3 3 | 132 | TCH only |
| 10-11 | 0.85 | 3 3 3 4 2 4 | 133 | TCH (+RPR) |
| 10-18 | 0.85 | 3 3 3 4 2 3 | 93 | TCH only |

- 10-03 is boundary noise: 144 lines against a ≤145 Tier-1 ceiling, with two real
  standouts. This is the third consecutive month with a 1-to-2-line downgrade (08-18 at
  144, 09-12 at 145, 10-03 at 144). The 10-06 single-authority change (PR #155) kept the
  hard edge; no tolerance was added.
- The other four are the TCH-only escalation described below. The month's most confident
  Tier-2 call (10-05, 0.90) is the clearest one: ARC=1, NAR=2, one TCH=4, 116 lines.

The circularity caveat from August and September still holds. The grader measures length,
and the classifier's tier sets the writer's length target. A Tier-2 call that ships at
Field-Note length means the day did not yield Deep-Dive material even when the writer was
told to produce it. That is a meaningful signal, but it is writer-mediated.

Confidence histogram (22 decisions, mean **0.845**; T1 0.848, T2 0.841):

```
0.78  ###      3
0.82  ######   6
0.83  #        1
0.84  #        1
0.85  ####     4
0.86  #        1
0.88  ##       2
0.90  ##       2
0.91  #        1
0.93  #        1
```

Confidence carries almost no tier information: mean T1 and T2 confidence differ by 0.007,
and the five missed calls average 0.848, the same as the month.

---

## Decision Quality Matrix

21 graded decisions:

|  | Good Outcome (correct) | Bad Outcome (incorrect) |
|---|---|---|
| **High Confidence (>0.7)** | 16 | 5 (10-03, 10-05, 10-07, 10-11, 10-18) |
| **Low Confidence (<0.7)** | 0 | 0 |

- **Good Decision + Bad Outcome, real outcome variance:** 10-03 only (two standouts,
  2 lines short).
- **Good Decision + Bad Outcome, actually a process miss:** 10-05, 10-07, 10-11, 10-18. Each
  rests on one TCH=4 with every narrative dimension at 3 or below. The confidence-gated
  downgrade cannot reach them: it fires only when "the highest qualifying dimension is
  exactly at the threshold", and TCH=4 sits above it. This is the loophole September found
  with SCP, now carried by TCH.
- Lowest confidence of the month is 0.78. No decision has fallen below 0.7 for four months;
  the "Lucky" quadrant stays empty because confidence never expresses doubt.

---

## Dimension Analysis

October averages (22 posts):

| Dim | Avg | 0 | 1 | 2 | 3 | 4 | 5 | T1 mean | T2 mean |
|---|---|---|---|---|---|---|---|---|---|
| NOV | 2.32 | | 2 | 12 | 7 | 1 | | 2.08 | 2.60 |
| ARC | 2.23 | | 4 | 10 | 7 | 1 | | 1.83 | 2.70 |
| NAR | 2.50 | | 2 | 9 | 9 | 2 | | 2.17 | 2.90 |
| TCH | **3.14** | | 2 | 2 | 9 | **9** | | 2.50 | **3.90** |
| SCP | 2.45 | | 1 | 13 | 5 | 3 | | 2.17 | 2.80 |
| RPR | 2.91 | | 1 | 4 | 13 | 4 | | 2.67 | 3.20 |

Share of posts awarded `>=4`:

| Month | NOV | ARC | NAR | TCH | SCP | RPR | any >=4 |
|---|---|---|---|---|---|---|---|
| 2026-06 | 4% | 12% | 12% | 29% | 17% | 8% | 46% |
| 2026-08 | 0% | 32% | 52% | 52% | 42% | 16% | 84% |
| 2026-09 | 0% | 10% | 13% | 17% | 30% | 10% | 43% |
| **2026-10** | **5%** | **5%** | **9%** | **41%** | **14%** | **18%** | **55%** |

### Anti-pattern: TCH is the Tier-2 escalator

- **9 of 10** Tier-2 calls carry TCH=4 (the exception is 10-21, NAR=4). T2 mean TCH is 3.90.
- TCH `>=4` more than doubled (17% → 41%) while every other dimension fell or held.
- The `no-named-artifact` flag **never fired**, on 9 TCH=4 awards. Reading the reasoning,
  the named artifact is usually the post's own thesis phrase: "release-from-tested-commit,
  not bot-commit" (10-18), "the library can never cost you the PDF" (10-05), "the
  three-pass settlement pattern" (10-07). Every daily post is written around a named rule,
  so the TCH hard rule ("requires an explicit, named, transferable artifact") is
  structurally always satisfiable. The posts whose TCH=4 pointed at an artifact outside the
  post (10-16: a pre-installed VPS deploy script; 10-17: a reusable-workflow toggle) both
  had a second standout and shipped as Tier 2.

Outcome split by standout structure, October:

| Tier-2 calls whose standouts are... | n | Shipped T2 |
|---|---|---|
| TCH only (RPR ignored) | 4 | **0** |
| two or more of NOV/ARC/NAR/TCH/SCP, or NAR=4 | 6 | 5 (the miss is 10-03 at 144 lines) |

### NOV, SCP and RPR

- NOV scored `>=4` once (10-08), the first time since July. 1 in 83 posts since August.
  Effectively still retired from escalation; September's recommendation 3 remains open.
- No SCP-sole-standout Tier-2 call occurred, so September's loophole did not recur, but
  the reference still lists SCP and RPR as standouts (`content-tier-classification.md`
  line 153), so it is closed by behavior, not by rule.
- RPR=4 was the only standout on 10-01 and 10-10; both were called Tier 1, and 10-01's
  record explicitly says RPR "is source-richness, not content-quality standout". The
  classifier is applying September's recommendation 4 in prose without the reference
  saying so.

---

## Anti-Inflation Effectiveness

### Closed-enum compliance

| Period | Flags | Exact enum |
|---|---|---|
| 10-01 .. 10-04 (pre-fix) | 11 | 0 |
| 10-05 .. 10-25 | 21 | **21 (100%)** |

The 11 off-enum flags are free-text strings on 10-01 and 10-02 (legacy records without
`record_type`) and `scope-alone-no-escalate` on 10-04. September recommendation 5 is
**done**.

### Trigger counts

| Count | Flag |
|---|---|
| 6 | `busy-not-distinguished` |
| 6 | `distribution-pressure` |
| 4 | `flat-wall-of-threes` |
| 2 | `high-scope-not-escalating` |
| 2 | `first-time-for-me-not-novel` |
| 1 | `volume-not-quality` |
| 0 | `no-named-artifact` |
| 0 | `linear-narrative-scored-as-drama` |

**Six Tier-2 calls carry no flag at all** (10-03, 10-05, 10-07, 10-08, 10-11, 10-16). Three of
them were length-gate downgrades. The no-flag posts are exactly the ones that most needed
a check.

### `distribution-pressure`: correct usage improved, effect is nil

| Date | Call | Trailing-14 T1 / T2 | Reading |
|---|---|---|---|
| 10-10 | T1 | 64% / 36% | misfire (a T1 call does not add to T2) |
| 10-12 | T2 | 57% / 43% | correct |
| 10-17 | T2 | 50% / 50% | correct |
| 10-18 | T2 | 50% / 50% | correct |
| 10-21 | T2 | 50% / 50% | correct |
| 10-25 | T1 | 45% / 55% | misfire (window T2-heavy, but a T1 call) |

Misfire rate fell from 9 of 15 to 2 of 6. But in all four correct firings the call stayed
Tier 2. The flag is now an accurate label with no consequence: by 10-17 the trailing
window was 50% Tier 2 and the Step-0 self-check (which triggers when T1 share is below
50%) sat exactly at its edge and did not fire.

### Overrides that changed the tier

| Mechanism | Fired on | Effect |
|---|---|---|
| Pattern engine `auto-2026-08-001` | 10-04, 06, 09, 13, 14, 19, 25 | 7 matches, **0 effective** (all already T1) |
| Confidence-gated downgrade | cited on 10-01 | T1 call already |
| Tier-length gate (`blog-land.sh`) | 10-03, 05, 07, 11, 18 | **T2 → T1, 5 times**, now recorded as `shipped_tier` |

The length gate is now the only layer actually changing tiers. That is the drift-proof
design the reference describes, but it means the classifier and the shipped tier disagree
on half the Tier-2 calls, and the writer is briefed for a tier the post will not ship as.

---

## Emergent Patterns

n = 22, below the skill's 30-decision threshold for pattern learning. The candidate below
is reported because it extends back across six months, not because October alone
supports it.

1. **TCH-only Tier-2 calls ship short.** In October, 4 of 4 shipped Tier 1 by length.
2. **The confidence gate's loophole is dimension-agnostic.** September it was SCP; October
   it is TCH. Any single non-narrative 4 lifts "the highest qualifying dimension" off the
   threshold.
3. **Classifier and gate have decoupled.** First half: classifier 60% T1, shipped 87%.
4. **Day-of-week:** none. The 10 Tier-2 calls fall on six different weekdays (4 on weekends,
   against 41% weekend days).
5. **Project-specific:** not computed. 22 posts and no project field; September showed that
   groups of 1 to 4 posts cannot support a project rule.

### Proposed pattern (not appended)

```json
{
  "pattern_id": "auto-2026-10-001",
  "name": "A technical standout alone is a Field Note",
  "direction": "downgrade",
  "conditions": "TCH>=4 AND NOV, ARC, NAR, SCP all <=3 (RPR ignored)",
  "rule": {
    "all": [
      { "feature": "tch", "op": ">=", "value": 4 },
      { "feature": "nov", "op": "<=", "value": 3 },
      { "feature": "arc", "op": "<=", "value": 3 },
      { "feature": "nar", "op": "<=", "value": 3 },
      { "feature": "scp", "op": "<=", "value": 3 }
    ],
    "action": { "type": "cap_tier", "tier": 1 }
  },
  "active": false
}
```

**Backtest (all classifier records, read-only):** the rule matches 19 Tier-2 decisions,
May through October (May 2, Jun 4, Jul 5, Aug 3, Sep 1, Oct 4). Against the structural
(length) tier:

| Era | Matches | Structural T1 (agrees) | Structural T2 | Structural T3 |
|---|---|---|---|---|
| May-Aug (no length gate) | 14 | 4 | 9 | 1 (08-27, 263 lines) |
| Sep-Oct (gated) | 5 | 4 | 1 (09-25) | 0 |
| **Total** | **19** | **8** | **10** | **1** |

The `correct_tier: 1` values on most May-July rows come from the old title heuristic
("apparent tier 1"), not an independent grade, so they were not counted as agreement.

**Verdict: not appended.** 8 of 19 agreement is chance-level on the full history, and in
the gated era, where it agrees 4 of 5 times, the length gate already enforced every
agreeing case. Activating it would change no October shipped tier. It would make the
classifier record honest, at the cost of a fourth score-keyed cap rule, which the
reference explicitly forbids. The cause is upstream in the TCH anchor (recommendation 3).
Revisit if the anchor fix fails and the gated-era sample reaches 10.

---

## Recommendations

1. **Restore the producer before anything else.** Nine days are missing. Restore the
   MiniMax token-plan quota, make the `claude` failover and repair launches pass
   `--agents` so `blog-classifier` resolves, then backfill each day with
   `scripts/blog/blog-backfill-daily.sh --date 2026-10-DD` (22, 23, 24, 26-31) and
   `blog-posting-packet.sh --sweep`. Also correct the repair-round prompt that tells the
   producer "you already produced the post" when no post exists (noted in the 10-31
   producer log). Triage the 78-entry quarantine after recovery.

2. **Make the failover path fail loud as a failover.** A producer that refuses because its
   classifier agent is missing should surface `agent not registered`, not a generic
   `write-set integrity` failure that reads like a content problem. Nine identical failures
   ran before this report noticed.

3. **Fix the TCH anchor at the source.** In `content-tier-classification.md`, state that the
   post's own thesis phrase is **not** a named artifact for TCH≥4. The artifact has to
   exist outside the post: a script, workflow, test, doc or schema that someone else could
   reuse. Make `no-named-artifact` mandatory whenever TCH=4 is claimed without a path or
   URL to the artifact. October evidence: 9 TCH=4 awards, 0 `no-named-artifact` flags, and
   the 4 TCH-only Tier-2 calls all shipped as Tier 1.

4. **Close the confidence-gate loophole generically.** Change the gate to evaluate the
   *second*-highest qualifying dimension (or "count of dimensions >=4 < 2") instead of the
   highest. A single standout of any kind then counts as "at threshold" for the gate.
   This covers September's SCP case and October's TCH case with one edit and no new cap
   rule.

5. **Carry forward September's open items:** two-sided Step 0 (add the >70% T1 inverse
   self-check, and restrict `distribution-pressure` to Tier-2+ calls; 2 of 6 still
   misfire), the NOV re-anchor-or-retire decision (1 award `>=4` in 83 posts), and an
   explicit "SCP and RPR are not standouts" line. The classifier already follows the last
   one in prose; the reference does not say it.

6. **Require at least one flag on every Tier-2 call.** Six Tier-2 calls carried no flag and
   three of them were downgraded at landing. Have the producer contract refuse a Tier-2
   record with an empty `anti_inflation_flags` list, or require an explicit
   `none-applicable` entry with a reason.

7. **Decide the boundary once and write it down.** 144, 145, 144: three months, three
   downgrades within two lines of the Tier-1 ceiling. PR #155 chose the hard edge. If that
   is the decision, record it in the reference and stop counting these as classifier
   misses in Brier (they inflate October's score by roughly 0.03).

---

## Steps run

- `apply-patterns.py backfill`: run. `times_applied` recomputed to honest counts:
  `auto-2026-08-001` 25 → **45**, `auto-2026-07-001` (inactive) 7 → 14. Verified that the 45
  are 45 unique date/slug classifier decisions, not audit duplicates. The ruleset digest
  covers only id + rule of applicable patterns, so it is unchanged (`c5339adab15f48ae`).
- No pattern appended (see verdict above).
- Methodology index rebuilt with `rebuild-methodology-index.sh` after writing this report.
