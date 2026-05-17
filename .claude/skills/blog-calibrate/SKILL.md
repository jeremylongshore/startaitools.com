---
name: blog-calibrate
description: 'Monthly calibration report for the blog content tier classification
  system.

  Analyzes decisions.jsonl and feedback.jsonl to detect tier inflation,

  assess calibration accuracy, and surface emergent patterns.

  Trigger with /blog-calibrate.

  '
version: 1.0.0
author: Jeremy Longshore <jeremy@intentsolutions.io>
license: Proprietary
tags:
- content
- blog
- methodology
- calibration
- analytics
allowed-tools: Read,Write,Edit,Glob,Grep,Bash(command:*),Agent
argument-hint: '[YYYY-MM]'
model: opus
compatibility: Designed for Claude Code
---
# blog-calibrate

## Overview

Generates a monthly calibration report from the blog-backfill methodology tracking system. Analyzes classification decisions, feedback assessments, and accumulated patterns to detect drift, validate the classification algorithm, and surface actionable improvements.

Grounded in Annie Duke's decision quality framework (Thinking in Bets): good decisions can have bad outcomes and vice versa. The calibration report separates decision quality from outcome quality.

## Prerequisites

- `/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/methodology/decisions.jsonl` — at least 10 entries
- `/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/methodology/feedback.jsonl` — optional but improves accuracy
- `/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/methodology/patterns.jsonl` — optional, accumulated rules

## Arguments

`$ARGUMENTS` = `YYYY-MM` (month to calibrate). If omitted, uses previous month.

## Instructions

### Step 1: Load Data

Read all three JSONL files. Filter decisions to the target month. Load all feedback (may reference earlier decisions). Load all patterns.

```bash
# Count records for the month
grep "\"date\": \"$YEAR-$MONTH" /home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/methodology/decisions.jsonl | wc -l
```

If fewer than 5 decisions exist for the month, warn that sample size is too small for reliable calibration.

### Step 2: Tier Distribution Analysis

Calculate:
- Tier 1/2/3 counts and percentages for the month
- Compare against expected distribution (60-70% T1, 25-35% T2, 5-10% T3)
- Compare against previous month (if data exists)
- Trend direction: inflating, stable, or deflating

**Inflation detection rules:**
- Tier 1 < 55% → WARNING: probable inflation
- Tier 3 > 15% → WARNING: Tier 3 overuse
- Tier 2 increasing month-over-month for 3+ months → WARNING: grade creep

### Step 3: Confidence Calibration (Brier Score)

For decisions that have feedback records:
- Calculate Brier score: avg((confidence - was_correct)^2)
- Perfect calibration = 0.0, worst = 1.0
- Target: < 0.15

**Interpretation:**
- < 0.10: Well calibrated
- 0.10-0.20: Acceptable, minor adjustments needed
- 0.20-0.30: Miscalibrated, review dimension scoring anchors
- > 0.30: Seriously miscalibrated, retrain on calibration examples

### Step 4: Decision Quality Matrix (Annie Duke 2x2)

Cross-tabulate confidence vs correctness:

| | Good Outcome (correct) | Bad Outcome (incorrect) |
|---|---|---|
| **High Confidence (>0.7)** | Good Decision + Good Outcome | Good Decision + Bad Outcome (learn why) |
| **Low Confidence (<0.7)** | Lucky (examine why unsure) | Bad Decision + Bad Outcome (fix process) |

Focus attention on:
- "Good Decision + Bad Outcome" quadrant → these reveal blind spots in the dimension scoring
- "Lucky" quadrant → these reveal under-confidence, possibly over-applying anti-inflation rules

### Step 5: Dimension Analysis

For each dimension (NOV, ARC, NAR, TCH, SCP, RPR):
- Average score across all decisions
- Score distribution (histogram)
- Most common score level
- Correlation with tier assignment

**Anti-pattern detection:**
- If one dimension consistently drives tier upgrades (e.g., SCP always high), check if the anti-inflation rule "high scope alone doesn't escalate" is being enforced
- If NAR is consistently 0-1 but posts are being classified Tier 2+, the algorithm may be too lenient on the Tier 2 gate

### Step 6: Anti-Inflation Flag Analysis

- Count how often each flag was triggered
- Check for flags that should have triggered but didn't
- Identify posts where anti-inflation overrides changed the tier

### Step 7: Pattern Learning

If 30+ decisions exist in the dataset:
- Look for emergent classification rules not in the original algorithm
- Check for day-of-week effects (e.g., Mondays consistently Tier 1)
- Check for project-specific patterns (e.g., repo X work always scores high on ARC)
- Surface any patterns worth adding to `patterns.jsonl`

### Step 8: Generate Report

Write the calibration report to `/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/methodology/calibration-$YEAR-$MONTH.md`.

## Output Format

```markdown
# Calibration Report: {Month YYYY}

## Summary
- Decisions analyzed: {N}
- Feedback records: {N}
- Overall health: HEALTHY / NEEDS ATTENTION / MISCALIBRATED

## Tier Distribution
| Tier | Count | Actual % | Expected % | Status |
|------|-------|----------|------------|--------|
| 1    | {N}   | {%}      | 60-70%     | OK/WARN |
| 2    | {N}   | {%}      | 25-35%     | OK/WARN |
| 3    | {N}   | {%}      | 5-10%      | OK/WARN |

Trend: {inflating / stable / deflating} (vs previous month)

## Calibration Accuracy
- Brier score: {N} ({interpretation})
- Sample size: {N} feedback records
- Confidence histogram: ...

## Decision Quality Matrix
{2x2 table with counts and key takeaways}

## Dimension Analysis
{Per-dimension stats and anti-pattern flags}

## Anti-Inflation Effectiveness
{Flag trigger counts and gaps}

## Emergent Patterns
{New rules discovered, if any — candidates for patterns.jsonl}

## Recommendations
1. {Specific actionable recommendation}
2. {Specific actionable recommendation}
3. {Specific actionable recommendation}
```

### Step 9: Update Patterns (if warranted)

If Step 7 discovered reliable patterns (consistent across 10+ decisions), append them to `methodology/patterns.jsonl`:

```json
{
  "pattern_id": "auto-YYYY-MM-NNN",
  "name": "Pattern name",
  "description": "What the pattern is",
  "direction": "upgrade|downgrade|neutral",
  "conditions": "When it applies",
  "evidence": "Data supporting it",
  "discovered_date": "YYYY-MM-DD",
  "times_applied": 0,
  "active": true
}
```

### Step 10: Rebuild SQLite Index

```bash
cd /home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill
sqlite3 methodology/index.db < methodology/rebuild-index.sql
```

## Error Handling

- **No decisions for month:** Print "No classification data for {month}. Run /blog-backfill first."
- **No feedback records:** Run report without calibration accuracy. Note: "Brier score unavailable — run /blog-feedback on past posts to populate."
- **SQLite rebuild fails:** Non-fatal. JSONL files are source of truth.

## Examples

```
/blog-calibrate 2026-04
```
Generates calibration report for April 2026. Analyzes tier distribution, Brier score, dimension patterns, and surfaces recommendations.

```
/blog-calibrate
```
No argument — calibrates previous month automatically.
