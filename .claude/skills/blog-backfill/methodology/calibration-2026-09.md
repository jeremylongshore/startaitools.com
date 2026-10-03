# Calibration Report: September 2026

## Analysis boundary and record counts

- **Window:** `[2026-09-01T00:00, 2026-10-01T00:00)` in `Etc/GMT+6` (UTC−6). Inclusive of
  09-01, exclusive of 10-01.
- **Date field used:** each `decisions.jsonl` record carries a date-only `date` (the post's
  local publish date). Where a record also carries `frontmatter.date`, it was checked. All
  three in-window instances (09-24 `08:00-05:00` = 07:00 UTC−6, 09-28 and 09-30
  `08:00-06:00`) fall on the same calendar day, so no record changes side of the boundary.
- **Edge records excluded:** 2026-08-31 (1 decision + 1 addendum) and 2026-10-01
  (1 decision + 1 addendum).
- **Feedback date field used:** `date_assessed`.

| Source | Total lines | In window | Used |
|---|---|---|---|
| `decisions.jsonl` | 400 | 60 | **30 classifier decisions** (one per day, 09-01..09-30) + 30 audit addenda |
| `feedback.jsonl` | 255 | 26 assessed 09-06..09-27 | **24** grade a September decision; the other 2 grade pre-September posts and are excluded |
| `patterns.jsonl` | 3 | n/a (rule state, not dated events) | read only; unchanged by this report |

**Record-shape anomaly:** the 2026-09-12 classifier decision has `"audit_addendum": true`
because it was recovered from quarantine (`recovery_from_quarantine`). It still carries
`dimensions`, `tier`, `confidence` and a `pattern_engine` receipt, so this report counts it
as that day's decision. Any filter that drops records with `audit_addendum == true` will
silently lose 09-12 and report 29 decisions.

Source data was read from this repository without modification.
The first pass lost shell output when the session's temp filesystem filled (ENOSPC). The
per-project breakdown and the historical backtest were completed in a second read-only
pass on 2026-10-03 from the committed files (`git show origin/master:<path>` for
`decisions.jsonl`, `feedback.jsonl`, `patterns.jsonl` and the post bodies). The committed
`patterns.jsonl` is byte-identical to the working copy.

---

## Summary

- Classifier decisions analyzed: **30** (every day, cadence 100% daily)
- Feedback records: **24** of 30 (09-25..09-30 not yet swept)
- Overall health: **NEEDS ATTENTION. Distribution recovered and is now trending toward over-deflation.**

September was the first full month under the 2026-09-01 fix bundle (CHANGELOG
`4e6e3071`: *deterministic length gate, duration-escalating creep guard, recalibrated
anchors*, plus the closed flag enum in `content-tier-classification.md`). That bundle
executed August's recommendations 1, 2, 5 and 6.

The fixes worked, and they worked fast:

- Classifier tier distribution moved from **26/65/10** in August to **67/30/3** in
  September. T1 and T2 are both inside their target bands for the first time since this
  system began tracking.
- The `>=4` award rate fell from 84% of posts to 43%. That matches June's 46% baseline,
  which was August's stated precondition for trusting score-keyed rules again.
- `auto-2026-08-001` produced **3 effective downgrades**, against zero in August. The rule
  did not change. It started binding because the anchors underneath it were fixed.
- The length gate fired 3 times and logged each one to `feedback.jsonl`.

Four new problems surfaced, and the summary health rating reflects them:

1. **The second half has overshot.** Classifier T1 was 80% for 09-16..09-30, and 87% after
   the length gate. That is above the 70% ceiling and heading toward the Jan/Feb 2026
   over-deflation (93–100% T1).
2. **SCP is now the Tier-2 escalator.** 8 of 9 Tier-2 posts carry SCP=4. Two of them have
   SCP as their *only* standout, which rule 7 prohibits. Neither carried the
   `high-scope-not-escalating` flag.
3. **Flag-enum compliance collapsed when the producer changed on 09-15.** 26 of 28 flags
   conformed in the first half and 13 of 32 in the second. The same switch dropped
   `cadence_type` and introduced a dict-valued `rhetorical_structure`.
4. **`decisions.jsonl` does not record the tier that shipped.** The length gate's
   downgrades exist only in `feedback.jsonl`, so every distribution computed from decisions
   alone overstates shipped Tier 2.

---

## Tier Distribution

### Classifier tier (as recorded in `decisions.jsonl`)

| Tier | Count | Actual % | Expected % | Status |
|------|-------|----------|------------|--------|
| 1 | 20 | 66.7% | 60–70% | OK |
| 2 | 9 | 30.0% | 25–35% | OK |
| 3 | 1 | 3.3% | 5–10% | Slightly below the band. No warning rule fires; one post of 30 is a 1-post gap |

### Shipped tier (classifier tier, capped by the tier-length gate)

The gate downgraded 09-08, 09-12 and 09-24 from T2 to T1 at landing.

| Tier | Count | Shipped % | Expected % | Status |
|------|-------|-----------|------------|--------|
| 1 | 23 | 76.7% | 60–70% | **WARN: above ceiling (deflation)** |
| 2 | 6 | 20.0% | 25–35% | **WARN: below floor** |
| 3 | 1 | 3.3% | 5–10% | Below band |

Trend: **deflating, sharply.** This is a correction from two months of saturation, and the
second half is overshooting.

| Month | n | T1 | T2 | T3 |
|-------|---|-----|-----|-----|
| 2026-04 | 22 | 36% | 36% | 27% |
| 2026-05 | 21 | 5% | 62% | 33% |
| 2026-06 | 24 | 46% | 50% | 4% |
| 2026-07 | 31 | 19% | 65% | 16% |
| 2026-08 | 31 | 26% | 65% | 10% |
| **2026-09 (classifier)** | 30 | **67%** | **30%** | **3%** |
| **2026-09 (shipped)** | 30 | **77%** | **20%** | **3%** |

Within the month:

| Half | n | Classifier T1/T2/T3 | Shipped T1/T2/T3 |
|---|---|---|---|
| 09-01 .. 09-15 | 15 | 8 / 6 / 1 (53% / 40% / 7%) | 10 / 4 / 1 (67% / 27% / 7%) |
| 09-16 .. 09-30 | 15 | 12 / 3 / 0 (80% / 20% / 0%) | 13 / 2 / 0 (87% / 13% / 0%) |

The first half is the healthy one. Its shipped distribution sits exactly on the target
bands. The second half had no Tier 3 and, after the gate, only two Tier 2s in 15 days.

Inflation-detection rules: T1 < 55% did not fire. T3 > 15% did not fire. "T2 rising three
months running" did not fire; T2 fell 35 points.

---

## Calibration Accuracy

| Cohort | n | Brier | Accuracy |
|---|---|---|---|
| September decisions with in-window feedback | 24 | **0.137** (acceptable) | 20/24 (83%) |
| Supplementary: all 30, with 09-25..09-30 checked against post length directly* | 30 | 0.115 | 26/30 (87%) |
| August, for comparison (clean grader, post-08-11) | 21 | 0.0965 | 90% |

\*The six unswept posts have raw file lengths of 204, 75, 90, 204, 76 and 80 lines. Each
is far enough from the 145/260 thresholds that its structural tier is unambiguous once
frontmatter is stripped, and all six match their classifier tier. These six are outside
the feedback window and should not be read as feedback records.

Brier got worse, from 0.0965 to 0.137. That reflects the new gate doing its job, not the
classifier getting worse. All four misses are length disagreements:

| Date | Classifier | Grader | Lines | Source | Read |
|---|---|---|---|---|---|
| 09-08 | T2 (0.78) | T1 | 92 | `length_gate_downgrade` | Real inflation. SCP=4 was the only standout (see Dimension Analysis) |
| 09-12 | T2 (0.87) | T1 | 145 | `length_gate_downgrade` | **Boundary noise.** The T1 ceiling is ≤145, so this missed by 1 line. Strongest dims of the month: 3/4/4/4/4/4 |
| 09-24 | T2 (0.85) | T1 | 133 | `length_gate_downgrade` | The writer under-delivered on a TCH4/SCP4 call, or the call was soft |
| 09-06 | T2 (0.86) | T3 | 344 | `structural_auto_confirm` | Writer overshoot. The gate only downgrades, so this shipped as T2 at T3 length |

August's circularity caveat still holds: the grader measures length, and the classifier's
tier sets the writer's target length. The difference now is that the length gate makes
that comparison binding at landing. Brier in this system measures **writer compliance
plus gate activity**. It does not independently assess whether the classification was
right.

Confidence histogram (30 decisions, mean **0.846**, against 0.834 in August):

```
0.72  #           1
0.78  ###         3
0.80  ###         3
0.82  ####        4
0.84  #           1
0.85  ###         3
0.86  ####        4
0.87  #           1
0.88  ####        4
0.90  #####       5
0.92  #           1
```

Mean confidence is 0.851 on Tier-1 calls and 0.833 on Tier-2 calls. The classifier is
slightly surer of its Field Notes than of its Deep-Dives, which is the right direction.
It is the first month in which confidence has risen alongside a shift toward Tier 1.

---

## Decision Quality Matrix

24 graded decisions:

|  | Good Outcome (correct) | Bad Outcome (incorrect) |
|---|---|---|
| **High Confidence (>0.7)** | 20 | 4 (09-06, 09-08, 09-12, 09-24) |
| **Low Confidence (<0.7)** | 0 | 0 |

The lowest confidence of the month is 0.72 (09-17). For the third straight month, no
decision falls below 0.7.

In the Good-Decision + Bad-Outcome cell:

- **09-12 is pure outcome variance.** A strong decision missed the boundary by one line.
  August had the identical case at 144 lines. Two boundary misses in two months means the
  gate's hard edge without tolerance is now a recurring source of false downgrades. See
  recommendation 4.
- **09-08 is a process miss mislabeled as a good decision.** At confidence 0.78, the only
  gate-firing dimension at threshold was max(NOV,TCH,NAR)=3. The standout was SCP=4. The
  confidence-gated downgrade should have fired, and rule 7 forbids SCP alone from
  escalating. The length gate caught it downstream. The classifier did not.
- **09-06 and 09-24 are writer-side variance:** one overshot, one undershot.

There is still no "Lucky" quadrant. The classifier never registers real uncertainty in
its confidence number. It registers uncertainty in its prose and its flags.

---

## Dimension Analysis

September averages (30 posts):

| Dim | Avg | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|---|
| NOV | 2.37 | | 3 | 13 | 14 | 0 | |
| ARC | 2.30 | | 7 | 10 | 10 | 3 | |
| NAR | 2.33 | 1 | 5 | 11 | 9 | 4 | |
| TCH | 2.73 | | 2 | 9 | 14 | 5 | |
| SCP | 2.80 | | 1 | 13 | 7 | 9 | |
| RPR | 2.47 | | 4 | 11 | 12 | 3 | |

By assigned tier:

| Tier | n | NOV | ARC | NAR | TCH | SCP | RPR |
|---|---|---|---|---|---|---|---|
| 1 | 20 | 2.20 | 1.95 | 2.00 | 2.35 | 2.30 | 2.25 |
| 2 | 9 | 2.67 | 3.00 | 2.89 | 3.44 | **3.89** | 2.89 |
| 3 | 1 | 3 | 3 | 4 | 4 | 3 | 3 |

In August, T1 and T2 were about a third of a point apart on every dimension. In September
the gap is 0.5–1.6 points. **Tier is a real category boundary again.**

Share of posts awarded `>=4`, by month:

| Month | NOV | ARC | NAR | TCH | SCP | RPR | any >=4 | max <=3 |
|---|---|---|---|---|---|---|---|---|
| 2026-06 | 4% | 12% | 12% | 29% | 17% | 8% | 46% | 54% |
| 2026-07 | 6% | 39% | 42% | 58% | 32% | 23% | 77% | 23% |
| 2026-08 | 0% | 32% | 52% | 52% | 42% | 16% | 84% | 16% |
| **2026-09** | **0%** | **10%** | **13%** | **17%** | **30%** | **10%** | **43%** | **57%** |

The 09-01 NAR hard rules hit their target. NAR's `>=4` rate fell from 52% to 13% and
TCH's from 52% to 17%. The overall standout rate is back at June's level.

### Anti-pattern: SCP is the new Tier-2 escalator

When the NAR/TCH escalation path closed, the load moved to SCP. This is the same shift
the June report saw with NOV and the August report saw with NAR/TCH.

- SCP is the **only** dimension still awarding `>=4` to more than 17% of posts (30%).
- **8 of 9** Tier-2 posts carry SCP=4. The exception is 09-25. T2 mean SCP is 3.89.
- On **2 posts, SCP=4 is the only standout behind a Tier-2 call**:

| Date | Dims (NOV ARC NAR TCH SCP RPR) | Conf | Shipped | Flag recorded |
|---|---|---|---|---|
| 09-08 | 2 3 2 3 **4** 3 | 0.78 | T1 (length gate, 92 lines) | `flat-wall-of-threes on three dims` (misapplied: it is not a flat wall, since SCP=4) |
| 09-28 | 2 2 2 3 **4** 3 | 0.78 | **T2** (194-ish body lines, passes the gate) | none |
| 09-09 | 2 1 1 2 **4** 2 | 0.82 | T1 | correct: SCP=4 did not escalate |

09-28 is the clean failure. Rule 7 says high SCP alone never escalates. The
narrative-or-standout floor reads SCP=4 as a standout. The confidence-gated downgrade
checks only "the highest qualifying dimension", and SCP=4 sits above the threshold of 3,
so that check does not fire either. The same loophole appears verbatim in a prior record:
*"highest qualifying dimension is SCP=4 (above threshold-3 floor) — does not fire."*
**SCP satisfies the floor and also shields the call from the confidence gate. That
combination is the gap.**

### NOV is a dead dimension, second consecutive month

NOV awarded `>=4` zero times in August and zero times in September (61 posts). August's
report set this condition: *"If that holds through September, NOV should either be
re-anchored or formally retired from escalation."* It has held, and the decision is now
due. See recommendation 3.

---

## Anti-Inflation Effectiveness

**Coverage:** 60 flag strings across 26 posts. 7 posts carry no real flag: 09-13, 09-20,
09-22, 09-24, 09-25, 09-28 and 09-30. Some of these record a placeholder such as
`none triggered`, `none_triggered` or `[]`. In August, 31 of 31 posts carried a flag.

### Closed-enum compliance (enum added 2026-09-01)

| Category | Count |
|---|---|
| Exact enum string | 32 (53%) |
| Enum string with an appended annotation (`flat-wall-of-threes on three dims`, `volume-not-quality: 180 commits…`) | 7 |
| Off-enum free text (`anchor-enforcement: …`, `TCH capped at 2 …`, `standout-floor-downgrade`, `past-14 …`, `none triggered`, …) | 21 |

| Period | Flags | Enum-conformant (exact or annotated) |
|---|---|---|
| 09-01 .. 09-14 | 28 | **26 (93%)** |
| 09-15 .. 09-30 | 32 | **13 (41%)** |

The break lines up exactly with the producer switch on 09-15. That is when records start
carrying a `run_id`, `cadence_type` goes to `null` on every record, and one record
(09-22) writes `rhetorical_structure` as a dict instead of a string. The new producer path
is either not loading the enum section of `content-tier-classification.md` or not
treating it as binding. **This is a regression introduced mid-month, not a slow drift.**

### Trigger counts (exact-enum only)

| Count | Flag |
|---|---|
| 15 | `distribution-pressure` |
| 5 (+3 annotated) | `volume-not-quality` |
| 5 (+1 annotated) | `busy-not-distinguished` |
| 3 | `no-named-artifact` |
| 2 (+3 annotated) | `flat-wall-of-threes` |
| 1 | `high-scope-not-escalating` |
| 1 | `first-time-for-me-not-novel` |
| 0 | `linear-narrative-scored-as-drama` |

### Flags that misfired

**`distribution-pressure` fired mechanically.** The enum defines it as *"the 14-day window
is already Tier-2-heavy **and this call adds to it**."* Nine of its 15 firings were on
Tier-1 calls, which by definition do not add Tier-2 weight. It also fired on 09-16, 09-17
and 09-26. By then the trailing 14-day window was 57%, 57% and 71% Tier 1, which is above
the Step-0 trigger of 50%. In the 09-26 case the window was above the 70% ceiling. The
09-29 record states it outright (*"past-14 T1 share is already above target"*). The flag
is being used to mean "I looked at the window", and the enum does not define it that way.

### Flags that should have fired and didn't

- `high-scope-not-escalating` on 09-08 and 09-28, the SCP-sole-standout Tier-2 calls above.
  It fired once all month, on 09-01, which is a T2 post with three standouts.
- `linear-narrative-scored-as-drama` never fired. With NAR's `>=4` rate down to 13%, that
  may be correct. Without session signals (13 of 30 decisions had `session: absent`),
  nothing checks it.

### Overrides that changed the tier

| Mechanism | Fired on | Effect |
|---|---|---|
| Pattern engine `auto-2026-08-001` | 09-04, 09-10, 09-20 | T2→T1 (`tier_before 2 → tier_after 1`) |
| Pattern engine, no-op | 09-03, 09-07, 09-16, 09-17, 09-27 | rule matched an already-T1 call |
| Confidence-gated downgrade | explicitly applied on 09-17 (0.72) and 09-27 (0.80); evaluated and held on 09-05 (0.86) | T2→T1 |
| Tier-length gate (`blog-land.sh`) | 09-08, 09-12, 09-24 | T2→T1 at landing, recorded in `feedback.jsonl` only |

At least 8 Tier-2 claims were stopped before shipping. In August the count was 0.

### Pattern-engine receipt coverage

Every one of the 30 decisions carries a `pattern_engine` receipt, against 21 of 31 in
August. All 30 report the same `ruleset_digest` (`c5339adab15f48ae`). The ruleset did not
change mid-month, so the second-half shift is not a rules change.

---

## Per-project breakdown

**Method.** `decisions.jsonl` has no project field, so each September classifier record
was attributed mechanically. The corpus is the post body (front matter stripped) plus the
record's `reasoning` and `thesis_candidate`. Within it, each repository name under
the estate's project directory or in those repos' GitHub remotes is counted with
word-boundary matching. Owner names, the generic words `blog`/`tools`/`twenty`, and file
names such as `CLAUDE.md` are excluded. `omarchy-*` repos and `omaTrail` fold into
"omarchy fleet", and `claude-code-plugins` folds into `tons-of-skills-marketplace`. The
primary project is the top count when it is at least 2 and strictly ahead of the second;
otherwise the post is unattributed. Shipped tier is the classifier tier after the
`length_gate_downgrade` feedback records. "Disagreements" are feedback records with
`was_correct` false.

| Project | Posts | Dates | Classifier T1/T2/T3 | Shipped T1/T2/T3 | Mean conf. | Mean NOV/ARC/NAR/TCH/SCP/RPR | Feedback (disagree) |
|---|---|---|---|---|---|---|---|
| unattributed (tie or <2 mentions) | 8 | 06, 09, 17, 20, 23, 24, 26, 27 | 6/2/0 | 7/1/0 | 0.835 | 2.5/2.3/2.5/2.9/3.0/2.4 | 6 (2: 09-06 structural, 09-24 length gate) |
| intent-longbox | 4 | 01–04 | 3/1/0 | 3/1/0 | 0.838 | 2.5/2.8/2.3/3.0/2.8/2.0 | 4 (0) |
| omarchy fleet | 3 | 07, 08, 10 | 2/1/0 | 3/0/0 | 0.793 | 2.7/2.3/2.0/3.0/3.0/3.0 | 3 (1: 09-08 length gate) |
| intent-blue-gold | 3 | 12, 13, 15 | 1/2/0 | 2/1/0 | 0.883 | 2.7/3.0/2.7/3.0/3.3/3.3 | 3 (1: 09-12 length gate) |
| intent-os | 2 | 16, 30 | 2/0/0 | 2/0/0 | 0.850 | 1.5/2.0/2.0/1.5/2.5/1.5 | 1 (0) |
| hustle | 2 | 18, 19 | 2/0/0 | 2/0/0 | 0.880 | 2.0/2.5/2.0/2.0/2.0/1.5 | 2 (0) |
| now-lms | 2 | 28, 29 | 1/1/0 | 1/1/0 | 0.830 | 1.5/1.5/2.0/2.5/2.5/3.5 | 0 |
| startaitools blog | 1 | 05 | 0/0/1 | 0/0/1 | 0.860 | 3/3/4/4/3/3 | 1 (0) |
| perception | 1 | 11 | 0/1/0 | 0/1/0 | 0.820 | 3/3/4/3/4/3 | 1 (0) |
| tons-of-skills-marketplace | 1 | 14 | 1/0/0 | 1/0/0 | 0.900 | 1/1/0/1/2/2 | 1 (0) |
| comehomealabama | 1 | 21 | 1/0/0 | 1/0/0 | 0.900 | 2/1/2/2/2/1 | 1 (0) |
| searchcarriers | 1 | 22 | 1/0/0 | 1/0/0 | 0.900 | 3/2/2/3/2/4 | 1 (0) |
| jeremylongshore.com | 1 | 25 | 0/1/0 | 0/1/0 | 0.820 | 3/2/3/4/3/2 | 0 |

Totals reconcile: 30 posts; classifier 20/9/1 and shipped 23/6/1 match the distribution
sections above; 24 posts have feedback, and the 4 disagreements are the 3 length-gate
downgrades plus the 09-06 structural under-tier.

**Reading.** Groups are too small for a project-specific rule. Three observations only:
(1) two of the three length-gate downgrades fell on the two multi-day hardening streams
(omarchy fleet 09-08, intent-blue-gold 09-12), whose posts carry the month's highest SCP
and RPR means, consistent with SCP being the Tier-2 escalator described above; (2) every
single-repo product-feature day (hustle, intent-os, comehomealabama, the marketplace) was
called Tier 1 at confidence 0.85 or above; (3) more than a quarter of posts (8 of 30) are
cross-repo days with no dominant project, so a per-project lens structurally misses a
large share of this blog.

---

## Emergent Patterns

n = 30. The skill's pattern-learning threshold is 30+, so September qualifies, but only
just. None of the candidates below reaches the 10-decision consistency bar, and the
sample-size caveat applies to every claim here.

1. **SCP-sole-standout escalation** (described above). In September it applied to 3
   decisions: 2 Tier-2 escalations and 1 correct non-escalation. It reproduces the
   recurring "escalator migrates to the dimension left unanchored" dynamic:
   NOV (June) → NAR/TCH (July–August) → SCP (September).
2. **Confidence-gate loophole.** The gate keys on "the highest qualifying dimension". A
   single dimension at 4 that does not carry the narrative (SCP, or RPR on 09-22 and
   09-29) lifts that highest value off the threshold and shields every other at-threshold
   dimension. The two September cases are the same pair as above.
3. **Second-half over-deflation.** 12 of 15 classifier calls after 09-15 were Tier 1, with
   no Tier 3. It coincides with the producer switch, and with `distribution-pressure`
   still firing after the window had already corrected. One reading is that Step 0 keeps
   pushing downward after the target is reached. That is the mirror image of August's
   breach suppression.
4. **Day-of-week:** nothing detectable. The 10 T2/T3 calls are spread across six weekdays.
5. **Project-specific:** no project shows a scoring signature distinct from the month.
   See the per-project breakdown below; every group is 1 to 4 posts, so nothing there
   qualifies as a pattern.

---

## Proposed patterns (not applied)

This report was produced by a manual run on 2026-10-03 after the scheduled 2026-10-01 run failed; these were **not** appended to `patterns.jsonl`, and the
`apply-patterns.py backfill` and index rebuild steps were **not** run. August's
recommendation 4 put a moratorium on new score-keyed cap rules "until … the `>=4` award
rate drops back toward June's 46%". September's rate of 43% satisfies that condition, so
a cap rule is eligible for proposal again. Neither candidate below meets the
10-consistent-decisions reliability bar. **Neither should be applied without a full
historical simulation first.**

### P1: SCP-sole-standout cap (codifies existing rule 7 deterministically)

```json
{
  "pattern_id": "auto-2026-09-001",
  "name": "Scope is not a standout",
  "description": "A Tier-2 call whose ONLY dimension >=4 is SCP is a Tier-1 Field Note. Deterministic form of anti-inflation rule 7 ('high SCP alone never escalates'), which the narrative-or-standout floor currently routes around by counting SCP=4 as a standout.",
  "direction": "downgrade",
  "conditions": "SCP>=4 AND every other dimension <=3",
  "rule": {
    "all": [
      { "feature": "scp", "op": ">=", "value": 4 },
      { "feature": "nov", "op": "<=", "value": 3 },
      { "feature": "arc", "op": "<=", "value": 3 },
      { "feature": "nar", "op": "<=", "value": 3 },
      { "feature": "tch", "op": "<=", "value": 3 },
      { "feature": "rpr", "op": "<=", "value": 3 }
    ],
    "action": { "type": "cap_tier", "tier": 1 }
  },
  "evidence": "Sep 2026: matches 09-08 (T2, conf 0.78; caught downstream by length gate at 92 lines), 09-28 (T2, conf 0.78; shipped T2 unchecked), 09-09 (T1 no-op). 8/9 Sep T2 posts carry SCP=4; SCP is the only dimension still awarding >=4 to >17% of posts after the 09-01 NAR/TCH anchor fix. Historical backtest (2026-10-03, read only; see 'Historical backtest'): would have changed 7 of 129 Apr-Aug decisions (T2->T1); 3 agree with the structural/length tier, 4 contradict it; pushes April T2 to 18.2% (below band) and September classifier T1 to 73.3% (above band).",
  "discovered_date": "2026-10-03",
  "times_applied": 0,
  "active": false
}
```

Why propose it despite the "no fourth cap rule" caution: this rule does not respond to
drift. It enforces a rule the reference already states, using only raw-score features the
engine supports today. Risk: it would add further downward pressure during the
second-half overshoot. **If adopted, adopt it together with recommendation 2.**

### P2: confidence-gated downgrade as a deterministic rule (needs an engine change)

`apply-patterns.py` has no `confidence` feature, so this rule cannot be expressed in the
current engine. Proposed shape, documentation-only until the engine grows the feature:

```text
tier >= 2 AND confidence < 0.85 AND max(nov, tch, nar) == 3
  AND the only dimensions >= 4 are in {scp, rpr}
  → cap_tier(provisional_tier - 1)
```

It closes the loophole that let 09-28 through: SCP or RPR at 4 lifting the
"highest qualifying dimension" off the threshold. September evidence: 09-08 and 09-28.
That is 2 decisions, far below the bar.

### Historical backtest (April–August 2026)

**Method.** Each rule was evaluated against every prior classifier record: records in
`decisions.jsonl` (committed `origin/master`) with a `dimensions` object and a `tier`, dated
2026-04-01 to 2026-08-31, deduplicated to the latest record per `(date, slug)`. That gives
129 decisions: April 22, May 21, June 24, July 31, August 31. A "change" is a match whose
recorded tier is above the rule's output. P1 caps at Tier 1. P2 is evaluated in its strict
reading (tier ≥ 2, confidence < 0.85, max(NOV,TCH,NAR) = 3, at least one dimension ≥ 4, and
every dimension ≥ 4 in {SCP, RPR}) and caps at tier − 1. The comparison is against the
recorded tier, not against `auto-2026-08-001`. P1 and `auto-2026-08-001` are disjoint by
construction, because P1 needs SCP ≥ 4 and the August rule needs every dimension ≤ 3.
Agreement is checked against every `feedback.jsonl` record for the slug. The structural
(length) tier in `metadata.structural_tier` is what the September length gate would have
capped to; `agent_retrospective_grading` supplies `correct_tier`.

| Month | n | P1 matches | P1 changes | P2 matches | P2 changes |
|---|---|---|---|---|---|
| 2026-04 | 22 | 4 | 4 | 2 | 2 |
| 2026-05 | 21 | 1 | 1 | 1 | 1 |
| 2026-06 | 24 | 1 | 0 (already T1) | 0 | 0 |
| 2026-07 | 31 | 1 | 1 | 1 | 1 |
| 2026-08 | 31 | 2 | 1 (one already T1) | 1 | 1 |
| **Apr–Aug** | **129** | **9** | **7** | **5** | **5** |
| 2026-09 (reference) | 30 | 3 | 2 (09-08, 09-28) | 2 | 2 (same two) |

Every change was T2 → T1. P2's five changes are a subset of P1's seven, so P2 adds no
historical case that P1 does not already catch.

**Do the changes agree with outcomes?**

| Date | Lines | Structural tier | Other feedback | P1 → T1 agrees with length? | Also P2? |
|---|---|---|---|---|---|
| 04-11 | 113 | 1 | auto-confirm | yes | no (conf 0.85) |
| 04-14 | 152 | 2 | auto-confirm | no | yes |
| 04-18 | 143 | 1 | auto-confirm | yes | yes |
| 04-20 | 160 | 2 | auto-confirm | no | no (conf 0.85) |
| 05-11 | 181 | 2 | agent grading: correct tier 1 | no by length; **yes** by the agent grade | yes |
| 07-11 | 178 | 2 | auto-confirm | no | yes |
| 08-01 | 105 | 1 | auto-confirm | yes | yes |
| 09-08 (ref) | 92 | 1 | length-gate downgrade | yes (gate already did it) | yes |
| 09-28 (ref) | n/a | n/a | no feedback yet | unknown | yes |

- **P1, April–August:** 3 of 7 changes agree with the structural tier, and in all 3 the
  length gate would have capped the post anyway, so P1 adds nothing there. 4 of 7
  contradict the structural tier. The only independent grade, 05-11, agrees with P1.
- **P2, April–August:** 2 of 5 agree with the structural tier (04-18, 08-01); 3 contradict
  it (04-14, 05-11, 07-11); the 05-11 agent grade agrees.
- **Circularity caveat:** line count is measured on posts written to the tier the
  classifier assigned, so "contradicts the structural tier" partly means "the writer
  produced Tier-2 length because it was told Tier 2". The structural tier is a weak
  arbiter for exactly these cases. The one non-structural grade available favours the rule.
- **Distribution effect:** P1 would have pushed **April's Tier 2 from 36.4% to 18.2%,
  below the 25–35% band**, while improving May, July and August by 3 to 5 points toward
  band. Applied to September's classifier, it moves Tier 1 from 66.7% to **73.3%, above
  the 70% ceiling**. Only 09-28 changes the shipped tier, because the gate had already
  downgraded 09-08, so shipped Tier 1 goes from 76.7% to 80.0%.

**Verdict.** Neither rule is supported strongly enough to activate. P1 changes 7 of 129
historical decisions (5.4%). Its agreement with length outcomes is 3 of 7, which is no
better than chance, and those 3 were already covered by the length gate. It would push
one past month and the current month out of band. P2 is strictly dominated by P1 on
history. Both remain below the 10-consistent-decisions bar. This supports recommendation 4:
fix the SCP-as-standout wording at the anchor, and do not add P1 downstream during the
current over-deflation.

### Not proposed as a pattern: NOV retirement

This belongs in the anchor reference, not in a cap rule. See recommendation 3.

---

## Recommendations

1. **Record the shipped tier in the decision trail.** The length gate writes its
   downgrade to `feedback.jsonl`, but the classifier record and its audit addendum still
   say T2. Have `blog-land.sh` write an `effective_tier`/`shipped_tier` field, either on
   the addendum or as a landing record. Until then, every tier distribution computed from
   `decisions.jsonl` (including the tier-creep guard's, if it reads that file) overstates
   shipped Tier 2. In September the overstatement was 10 points: 30% recorded against 20%
   shipped.

2. **Watch for over-deflation, and fix the `distribution-pressure` misfire before it
   compounds it.** Second-half shipped T1 was 87% with no T3. Make Step 0 two-sided: when
   the trailing 14-day T1 share is **above 70%**, prepend the inverse self-check ("I may be
   deflating; justify why this is NOT a Tier 2"). Restrict `distribution-pressure` to its
   enum definition: Tier-2+ calls only, with the window actually T2-heavy. If October's
   first half also runs above 80% T1, treat it as a regression of the Jan/Feb 2026 kind.

3. **Re-anchor or retire NOV.** It has scored `>=4` zero times in 61 consecutive posts, so
   it contributes nothing to the standout floor or the Tier-3 gate
   (max(NOV,TCH) >= 4 now means TCH >= 4). Either write a reachable 4-anchor with a
   September-era positive example, or drop NOV from the Tier-3 gate and the standout floor
   and keep it descriptive only. This was August's conditional recommendation, and the
   condition has now been met.

4. **Close the SCP loophole upstream before adding P1 downstream.** In
   `content-tier-classification.md`, state that SCP and RPR **do not count as standouts**
   for the narrative-or-standout floor, and that the confidence-gated downgrade evaluates
   the highest *narrative-bearing* dimension (NOV/NAR/TCH). That edit fixes the cause.
   P1 is the backstop. Also give the tier-length gate a small tolerance band (for example,
   ±3 lines at 145 and 260), or accept and document boundary noise. Two consecutive months
   produced a 1-line false downgrade (08-18 at 144, 09-12 at 145).

5. **Fix the 09-15 producer regression.** In the run-ID producer path, flag-enum compliance
   fell from 93% to 41%, `cadence_type` went null on every record, and one record wrote
   `rhetorical_structure` as an object. Add a deterministic validation step before append:
   reject any `anti_inflation_flags` entry not in the closed enum (annotations go in
   `reasoning`), require `cadence_type`, and type-check `rhetorical_structure`. The
   landing path already gates on the pattern receipt, so this belongs alongside that gate.

6. **Normalize the 09-12 recovery record.** A classifier decision carrying
   `audit_addendum: true` will be dropped by any addendum filter. Either clear the flag on
   recovered classifier records or add an explicit `record_type`, so 09-12 is counted
   deterministically rather than by a dimensions-present heuristic.

7. **Keep `auto-2026-08-001` active.** It is now doing work: 3 effective downgrades in
   September after 0 in August. Its `times_applied` will rise on the next backfill. That
   recompute was deliberately not run in this manual pass.

---

## Not done

- **Nothing was appended to `patterns.jsonl`.** `apply-patterns.py backfill` and the
  methodology index rebuild were not run, so `times_applied` on `auto-2026-08-001` is
  unchanged. This was a deliberate scope limit of the manual run.
- **P2 cannot be simulated through the engine.** `apply-patterns.py` has no `confidence`
  feature, so P2 was backtested by an equivalent read-only evaluation, not by the engine.
  P1 was evaluated with the engine's own feature semantics; `apply-patterns.py` itself was
  not executed.
- **Per-project attribution is heuristic.** It uses name-mention counts. 8 of 30 posts are
  unattributed, and a misattribution is possible where a post discusses several repos.
- **Feedback for 09-25..09-30 has not been swept**, so 09-28, a P1/P2 match, has no
  outcome to check against.
- **Months before April were not backtested.** The request covered April–August.
  `decisions.jsonl` also holds 97 classifier records dated 2025-10 to 2026-03, mostly
  backfill from the January–February over-deflation era; running both rules over them is
  the next step if P1 is reconsidered.

