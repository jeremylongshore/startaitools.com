# Calibration Report: May 2026

**Overall health:** MISCALIBRATED — severe tier inflation, classifier rubric structurally broken, audit-trail compliance at 71%.

Generated 2026-05-16 from retrospective rubric grading of 15 May 2026 posts. Brier score still unavailable until user reviews the retrospective grades and confirms/overrides via `/blog-feedback <slug> --correct|--wrong N`.

## Summary

| Metric | Value | Target |
|---|---|---|
| Decisions analyzed | 10 (May 2026) | — |
| Feedback records | 15 (this report) + 0 prior | — |
| Audit-addendum coverage | 71% (10/14 records) | 100% |
| Classifier ↔ rubric agreement | 47% (7/15 graded posts) | ≥80% |

## Tier Distribution (classifier vs rubric)

| Tier | Classifier | Rubric (strict) | Expected |
|------|:---:|:---:|:---:|
| 1 | 0 (0%) | 9 (60%) | 60-70% |
| 2 | 4 (40%) | 6 (40%) | 25-35% |
| 3 | 6 (60%) | 0 (0%) | 5-10% |

**The classifier is producing zero Tier 1 and zero genuine Tier 3 under rubric review.** Strict rubric grading recovered the expected 60-70% Tier 1 distribution.

## Classifier dimension behavior (May 2026)

| Dim | Mean | Range | Issue |
|---|:---:|:---:|---|
| NOV | 3.20 | 2-4 | High, but bounded — least inflated |
| ARC | 3.40 | 2-5 | Reasonable spread |
| NAR | 3.70 | 2-5 | Inflated — drama anchor not enforced |
| TCH | 3.90 | **3-5** | **Floor at 3 — anchor enforcement broken** |
| SCP | 3.90 | **3-5** | **Floor at 3 — anchor enforcement broken** |
| RPR | 3.30 | 2-5 | Reasonable spread |

### Root cause: TCH + SCP floor at 3

Per the algorithm:

- Tier 2 gate: `max(NOV, TCH, NAR) >= 3 AND 2+ dims >= 3`

With TCH ≥ 3 every day **and** SCP ≥ 3 every day, the Tier 2 gate is **structurally always true** — `max(_,TCH,_) ≥ 3` because TCH ≥ 3, and `2+ dims ≥ 3` is satisfied automatically by TCH + SCP. Tier 1 is therefore unreachable.

### Anchor-mismatch evidence

Per `references/content-tier-classification.md`:

- TCH=3 requires *"Changes how someone thinks about a category of problems"*
- SCP=3 requires *"Multiple systems, coordinated changes"*

Examples of May 2026 posts that were scored TCH≥4 / SCP≥4 but, by content, do not meet those anchors:

| Post | Classifier TCH/SCP | Actual content |
|------|------|---|
| transitive-cve-clearance-dual-layer-pattern (Tier 2) | high | 99 lines, single-repo dep bump, single-pattern explanation. Anchors say TCH=1-2, SCP=1-2. |
| two-false-positive-fixes-same-root-cause (Tier 2) | high | 181 lines, two Docker-healthcheck fixes. SCP=2 max (multiple files, single system). |
| three-guards-against-shipping-slop (Tier 3) | high | 114 lines — does not satisfy Tier 3 length anchor (300-500), and content is review-process narrative, not first-principles methodology. |
| coherence-day-drift-detection-strategic-spine (Tier 2) | high | **84 lines** — below Tier 2 minimum (150). Structural Tier 1. |

## Decision Quality Matrix (Annie Duke 2×2)

Unavailable until the user reviews the 15 retrospective grades. Run:

```
/blog-feedback <slug> --correct   # confirm rubric grade
/blog-feedback <slug> --wrong N   # override to user's tier
```

across the 15 records currently marked `source: "agent_retrospective_grading"`. Then re-run `/blog-calibrate 2026-05` for Brier score and full 2×2.

## Audit-trail compliance

| Date | Slug | Tier | Class record | Audit addendum |
|---|---|:---:|:---:|:---:|
| 05-02 | five-releases-fifteen-minutes | 3 | ✓ | **missing** |
| 05-03 | anti-slop-framework-found-three-bugs | 3 | ✓ | ✓ (partial — 7 SEO/fact-check gates missing) |
| 05-05 | postgres-approval-sink | 3 | ✓ | **missing** |
| 05-06 | guidewire-mcp-three-releases | 3 | ✓ | **missing** |
| 05-08 | coherence-day | 2 | ✓ | ✓ |
| 05-09 | spec-graduation-engagement-arch | 3 | ✓ | ✓ |
| 05-11 | two-false-positive-fixes | 2 | ✓ | ✓ |
| 05-12 | three-guards | 3 | ✓ | ✓ (partial — 8 gates missing incl. blog-fact-checker, code-reviewer) |
| 05-13 | transitive-cve-clearance | 2 | ✓ | ✓ |
| 05-14 | self-improving-skills | 2 | ✓ | **missing** |
| 05-15 | deterministic-first-llm-advisory | 2 | **missing** | **missing** |

5 of 11 days fully compliant. The pattern in the most recent week (05-14, 05-15) suggests bookkeeping (Step 3 / Step 8) is being skipped under headless `claude -p` runs — possibly token-budget exhaustion before the final audit-record write.

## Recommendations

### Rubric fixes (urgent)

1. **TCH anchor enforcement** — add a hard rule to `agents/blog-classifier.md`: *"TCH ≥ 4 requires explicit named transferable artifact (framework, methodology, named pattern). Default TCH for daily ops / debugging / single-PR work is 1-2."* Currently the classifier reads TCH=5 ("Framework-level insight — reader can apply this to problems you haven't imagined") into routine CI tweaks.

2. **SCP anchor enforcement** — same pattern. SCP ≥ 3 requires *"Multiple systems, coordinated changes."* Single-repo, single-PR work is SCP=1-2.

3. **Confidence-gated downgrade** — current rule "Default down when in doubt" is qualitative. Operationalize: *"If classifier confidence < 0.85 AND the gate-firing dimension is at its minimum threshold value (e.g., TCH=3 fires Tier 2), downgrade one tier."*

4. **Distribution feedback loop** — in the classify-day prompt, inject the running 14-day tier distribution. If Tier 1 = 0% for past 14 days, prepend: *"You have classified zero Tier 1 posts in the past 14 days. The expected baseline is 60-70%. Justify why today is not Tier 1."*

5. **Refresh calibration examples** — `references/content-tier-classification.md` Examples A/B/C are from April. Add 2-3 May 2026 examples showing what an inflated decision looks like and the corrected grade.

### Bookkeeping fixes

6. **Hard-fail the cron on missing audit record** — modify `~/bin/blog-backfill-daily.sh` to verify `decisions.jsonl` gained ≥1 line for today's date before pushing. If not, fail the run and ntfy-push, do not advance to the git push step.

7. **Reactivate the methodology index rebuild step** — line 173 of SKILL.md mandates `rebuild-methodology-index.sh` at end of every batch. Confirm this is firing in cron runs (current 2026-05-15 log does not show it).

### Process

8. **Both skills now active again** — `blog-calibrate` and `blog-feedback` restored from `~/.claude/skills/inactive/`. Monthly cron at 09:00 on the 1st will now actually run. Next firing: 2026-06-01.

9. **15 retrospective grades pending user review** — `feedback.jsonl` now has 15 records sourced from this agent's rubric application. User should sweep them via `/blog-feedback <slug> --correct|--wrong N` to make them user-judged calibration data rather than agent-judged.

## Files touched this run

- `/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-calibrate/` — moved out of `inactive/`
- `/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-feedback/` — moved out of `inactive/`
- `/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/methodology/feedback.jsonl` — appended 15 retrospective grades (May 2026 posts)
- `/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/methodology/calibration-2026-05.md` — this report

## Bead

OPS-rge tracks this work. Close after the user has reviewed the 15 retrospective grades and decided which classifier-rubric edits to land.
