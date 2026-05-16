---
name: blog-feedback
description: 'Post-publication assessment for blog posts classified by the tier system.

  Records whether the classification was correct, captures engagement data,

  and feeds the calibration loop.

  Trigger with /blog-feedback.

  '
version: 1.0.0
author: Jeremy Longshore <jeremy@intentsolutions.io>
license: Proprietary
tags:
- content
- blog
- methodology
- feedback
- calibration
allowed-tools: Read,Write,Edit,Glob,Grep,Bash(command:*),Agent,AskUserQuestion
argument-hint: <slug> [--correct|--wrong TIER] [--notes 'text']
model: opus
compatibility: Designed for Claude Code
---
# blog-feedback

## Overview

Records post-publication assessments for posts classified by the blog-backfill tier system. Each feedback record captures whether the original classification was correct, optional engagement data, and qualitative notes. This data feeds `/blog-calibrate` for Brier score calculation and decision quality analysis.

Decoupled from classification time by design — you can assess a post days or weeks after publication, once you've seen how it performs.

## Prerequisites

- Post must exist in `content/posts/` with a matching decision record in `methodology/decisions.jsonl`
- `/blog-calibrate` uses this data — more feedback = better calibration

## Arguments

`$ARGUMENTS` parsing:

- `<slug>` — required. The post slug (kebab-case, matches filename without .md)
- `--correct` — flag indicating the original classification was correct
- `--wrong <TIER>` — the tier it should have been (1, 2, or 3)
- `--notes "text"` — optional qualitative notes

**Examples:**
```
/blog-feedback knowledge-os-bootstrap --correct
/blog-feedback wcag-color-audit --wrong 2 --notes "Had more teaching value than expected"
/blog-feedback plugin-registry-design --correct --notes "Good call on Tier 3, got 2 backlinks"
```

If no flags provided, enter interactive mode (ask the user).

## Instructions

### Step 1: Find the Decision Record

Search `methodology/decisions.jsonl` for the slug:

```bash
grep "\"slug\": \"$SLUG\"" /home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/methodology/decisions.jsonl
```

If not found, check if the post exists in `content/posts/$SLUG.md`. If the post exists but has no decision record, it was published before the tier system — offer to create a retroactive classification.

### Step 2: Display Context

Show the user:
- Post title and date
- Original tier classification and confidence
- Dimension scores
- Reasoning from the original classification
- Thesis candidate

### Step 3: Collect Assessment

**If flags provided in arguments:**
- Parse `--correct` or `--wrong <TIER>`
- Parse `--notes` if present

**If interactive mode:**
Ask the user:
1. "Was Tier {N} the right call?" → Yes/No
2. If No: "What tier should it have been?" → 1/2/3
3. "Any notes on why?" → Free text (optional)
4. "Any engagement data to record?" → Views, shares, comments, backlinks (optional)

### Step 4: Record Feedback

Append to `methodology/feedback.jsonl`:

```json
{
  "slug": "the-post-slug",
  "date_assessed": "2026-04-09",
  "original_tier": 2,
  "correct_tier": null,
  "was_correct": 1,
  "reasoning": "User confirmed classification was appropriate",
  "year_from_now_useful": null,
  "engagement_data": null
}
```

**Schema fields:**
- `slug` — matches decisions.jsonl
- `date_assessed` — today's date
- `original_tier` — from the decision record
- `correct_tier` — null if correct, integer if wrong
- `was_correct` — 1 if correct, 0 if wrong
- `reasoning` — why the user agrees/disagrees
- `year_from_now_useful` — 1/0/null, assessed retrospectively
- `engagement_data` — JSON object with available metrics, or null

### Step 5: Confirm

Print summary:
```
Feedback recorded for "{title}":
  Original: Tier {N} ({name}) @ {confidence}
  Assessment: {CORRECT / WRONG → Tier N}
  Notes: {notes or "none"}
  Feedback records total: {count in feedback.jsonl}
```

### Step 6: Pattern Detection (if 10+ feedback records exist)

Quick check:
- Are we consistently over-classifying or under-classifying?
- Is any dimension systematically misleading?
- Print a one-line observation if a pattern is visible.

## Batch Mode

For assessing multiple posts at once:

```
/blog-feedback --batch 2026-04-01 2026-04-07
```

Shows each post from the date range with its classification and asks for quick assessment (correct/wrong + optional tier). Efficient for weekly review sessions.

## Auto-Sweep Mode (added 2026-05-16)

The original flow assumed human-judgment-is-truth. At ~30 posts/month with autonomous publishing, manual sweep proved unrealistic — `feedback.jsonl` sat empty from 2026-04-09 onward, and `/blog-calibrate` lost its Brier-score input. Auto-sweep fixes that with a deterministic, no-LLM rubric grader.

**Script**: `/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/scripts/feedback-sweep.py`
**Cron wrapper**: `~/bin/blog-feedback-sweep.sh` (Sunday 10:00 local)

**Logic** (deterministic, no LLM, no API calls):
1. For every classifier record in `decisions.jsonl` without a matching `feedback.jsonl` entry,
2. Read the post's markdown file (line count, title),
3. Apply structural tier rule (≤145 lines → T1, ≤260 → T2, else T3),
4. Apply title heuristics: T2 demotes to T1 without a named transferable artifact in the title; T3 demotes to T2 without both named-artifact AND drama markers,
5. Write a `feedback.jsonl` entry with `source: "structural_auto_confirm"`,
6. Email a digest highlighting mismatches the user should manually review.

**User override**: any auto-sweep record can be overridden by running `/blog-feedback <slug> --correct` or `/blog-feedback <slug> --wrong N`. `feedback.jsonl` is append-only and the latest record for a slug wins for calibration purposes.

**Why deterministic (not LLM)**: the inflation problem this fixes was caused by an LLM-classifier reading anchors generously. Pasting another LLM on top to grade the first LLM's output reproduces the failure mode. The structural rubric is crude but auditable — when it's wrong, the user can see exactly why (line count, title words) and adjust the heuristic.

**v2 (future)**: layer Umami engagement signal on top of structural grading. High views + low bounce on a Tier 1 → maybe under-classified. Low engagement on a Tier 3 → likely over-classified. Use engagement as a tiebreaker for borderline structural calls. Requires Umami API creds in cron env (currently MCP-only).

## Output

| Artifact | Location |
|----------|----------|
| Feedback record | `methodology/feedback.jsonl` (appended) |
| Console summary | Printed to screen |

## Error Handling

- **Slug not found:** Check for typos, suggest closest matches from decisions.jsonl.
- **Duplicate feedback:** Warn if slug already has a feedback record. Allow override with confirmation.
- **No decision record:** Offer retroactive classification or skip.

## Examples

**Quick correct:**
```
/blog-feedback knowledge-os-bootstrap --correct
```
Records that the classification was correct. Takes 2 seconds.

**Wrong classification:**
```
/blog-feedback wcag-color-audit --wrong 2 --notes "The WCAG debugging journey was more transferable than I expected"
```
Records that Tier 1 was wrong, should have been Tier 2. Valuable calibration data.

**Interactive:**
```
/blog-feedback plugin-registry-design
```
No flags — enters interactive mode, walks through the assessment questions.

**Batch review:**
```
/blog-feedback --batch 2026-04-01 2026-04-07
```
Reviews all posts from that week sequentially.
