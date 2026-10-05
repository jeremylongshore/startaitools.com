# 012 — September 2026 retrospective and calibration: decisions

| Field | Value |
|---|---|
| Date | 2026-10-05 |
| Status | Decided by the acting lead under the owner's delegation of 2026-10-03 |
| Scope | Recovery epics E06 (September retrospective as a decision record) and E07 (calibration describes what shipped) |
| Frozen input | This repository at `a5496e46` (release v1.27.0) |
| Private record | Full evidence, per-repository counts and replay outputs live in the private ledger store, `blog-growth-impl-20261003/e06-e07/` (not in this repository) |

## 1. Estate activity is counted one way

Monthly retrospectives count estate activity with `scripts/blog/estate-activity.py` (method
`estate-activity/1`). The previous lens read each checkout's local `HEAD` at the top level only. That
undercounted any checkout nobody had pulled, counted two clones of this blog as separate
repositories, and missed the nested canonical checkout. The new method finds checkouts to depth 3.
It resolves each one to its `owner/repo` remote identity and keeps one checkout per identity. It
counts on the remote default branch after a fetch, over a half-open window on committer date. Linked
worktrees, duplicate clones, checkouts without a remote and third-party repositories are listed as
exclusions, not dropped silently. With `--github` it also lists owned repositories that were pushed
in the window but have no local checkout, which is the gap a local count can never see. Counts are
activity, never outcomes. Wiring the monthly retrospective to call the script is a tracked follow-up.

## 2. One set of definitions for tier counts

- A **classifier decision** is a record selected by `blogpipe.records.record_type`, one per date and
  slug. Audit addenda never count, even when they carry a `tier` field. A classifier record recovered
  from quarantine counts, so September has 30 decisions, not 29.
- The **shipped tier** is the latest `shipped_tier` record, else the lander's legacy
  `length_gate_downgrade` feedback row, else the classifier tier.
- The reader is `python3 -m blogpipe tier-ledger`. For September it reports classifier 20/9/1 and
  shipped 23/6/1. For 2026-10-01 to 10-03 it reports classifier 2/1/0 and shipped 3/0/0, and the 10-03
  downgrade is the first live `shipped_tier` record.

Two monthly rows in the drafts were cohort substitutions, and both are corrected here. The April row
copied from the August retrospective (n=28) counted six audit addenda that carry a tier; the
canonical April count is 22. The calibration's July row (n=31) kept one decision per date; July had
35 decisions on 31 dates.

The September calibration report (merged in #116) is publication only. None of its proposed patterns
was activated: `patterns.jsonl` is unchanged and the pattern-engine digest is `c5339adab15f48ae` on
every decision from 09-01 to 10-03.

## 3. The length gate measures formatting as well as length

These are findings from a read-only replay of 163 classifier decisions from 2026-04-01 to 10-03. No
gate was changed.

- **The lander and the grader disagree by one line.** `blog-land.sh` counts the lines after the
  front matter. `feedback-sweep.py` counts newlines after splitting on the fence, which is one more
  on every `+++` post. The CI test asserts only that the two threshold constants match. The
  2026-09-12 post (145 / 146 lines) was downgraded because of that one line.
- **Wrapping changes the count.** The same 09-12 content measures 145 lines with paragraphs on one
  line each and 373 lines when hard-wrapped at 72 columns, which is structural Tier 3. Across the
  corpus, hard-wrapping multiplies the line count by 1.04 to 4.23 (median 1.77), and 52 of 163 posts
  are already hard-wrapped. The 2026-09-06 "under-tier" case was a formatting artifact: with
  paragraphs joined it is 149 lines, inside the Tier 2 band the classifier chose.
- **Words are not a drop-in replacement.** At the same overall strictness, a word gate needs
  thresholds of about 1,900 and 3,200 words. That contradicts the writer instructions' cap of about
  1,500 prose words for every tier, and words separate Tier 1 from Tier 2 less well than lines
  (AUC 0.91 against 0.97).
- **The best formatting-invariant unit is the paragraph-unwrapped line count.** It keeps the
  existing 145 and 260 thresholds and removes wrap sensitivity, and in the replay it separates tiers
  best (AUC 0.977 / 0.907).

**Decision:** no gate change now. Any change ships later as one shared counter for the lander and
the grader, with a same-content rewrap fixture, a replay attached to the pull request and owner
sign-off. It does not start until person-written tier verdicts exist for the boundary posts.

## 4. Scope-only Tier 2 calls and patterns P1/P2

16 of 259 dimensioned classifier decisions since 2025-10 are Tier 2 calls where scope (SCP=4) is the
only standout, with max(NOV, TCH, NAR) = 3. Scope then satisfies the narrative-or-standout floor and
also shields the call from the confidence-gated downgrade. The fix belongs upstream, in the rubric
wording: scope and reproducibility are not standouts, and the confidence gate reads the highest
narrative-bearing dimension. That fix is owner-gated.

**P1 and P2 stay inactive for Phase I.** Each may return only through a separate reviewed PR. That
PR must follow the upstream wording fix, replay all 259 decisions (including the 7 matches before
April) and carry a rollback, which is `active: false` with the digest back at `c5339adab15f48ae`.

## 5. The September retrospective stays internal

No September retrospective and no short public lesson will be published. The draft's tables carried
the two errors corrected above, and its activity counts used the retired method. A lesson about a
gate that has not changed yet would be a claim without an outcome. If the counter change ships, the
daily post for that date may cover it like any other day's work.
