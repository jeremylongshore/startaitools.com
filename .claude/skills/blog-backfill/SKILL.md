---
name: blog-backfill
description: 'Backfill daily blog posts to startaitools.com for a date range.

  Auto-classifies content into 3 tiers (Field Note / Deep-Dive / Case Study).

  Tracks methodology decisions in JSONL for calibration analysis.

  Dual-publishes to tonsofskills.com/blog, cross-posts to Dev.to, Hashnode, Medium,
  and Substack.

  Generates weekly recaps and monthly retrospectives on cadence.

  Use when backfilling missed blog posts. Trigger with /blog-backfill.

  '
version: 4.0.0
author: Jeremy Longshore <jeremy@intentsolutions.io>
license: Proprietary
tags:
- content
- blog
- cross-posting
- backfill
- automation
- methodology
allowed-tools: Read,Write,Edit,Glob,Grep,Bash(command:*),Agent
argument-hint: START_DATE END_DATE
model: opus
compatibility: Designed for Claude Code
---
# blog-backfill

## Overview

Automated blog post pipeline that generates one post per day for startaitools.com from git activity across the Intent Solutions project portfolio. Each day is auto-classified into a content tier (Field Note, Deep-Dive, or Case Study) that determines post structure, depth, and quality gates. All classification decisions are recorded in an auditable methodology tracking system.

Also generates weekly recaps and monthly retrospectives on automated cadence.

Dual-publishes to tonsofskills.com/blog, queues staggered cross-posts to Dev.to/Hashnode/Medium, and emails social content bundles (X thread + LinkedIn + Substack).

## Prerequisites

- Hugo installed locally (v0.150.0)
- All project repos cloned at `/home/jeremy/000-projects/`
- `gh` CLI authenticated for PR data
- API keys in `~/000-projects/blog/.env` for cross-posting (optional — scripts skip gracefully if missing)

## Arguments

`$ARGUMENTS` = `START_DATE END_DATE` (YYYY-MM-DD format)
Example: `/blog-backfill 2026-03-01 2026-03-15`

If no arguments: START = day after most recent post date, END = yesterday.

**Special arguments:**
- `weekly` — generate a weekly recap for the current week
- `monthly` — generate a monthly retrospective for the previous month

## Instructions

### Phase 0: Process Cross-Post Queue

Check and publish any pending cross-posts from previous runs:
```bash
${CLAUDE_SKILL_DIR}/scripts/check-crosspost-queue.sh
```
No-op if queue file doesn't exist.

### Phase 1: Date Range Setup

Parse dates from `$ARGUMENTS`, verify last published post date, calculate total days.

### Phase 2: For Each Day (oldest first)

**Phase-2 Subagent Preflight Checklist (MANDATORY — read before step 0)**

Before generating any post content, you MUST have dispatched each applicable agent below. If you end Phase 2 without these dispatches in the tool-call log, you violated the skill — even if the posts look fine. `/blog-calibrate` measures this.

| Step | Agent | When required |
|------|-------|---------------|
| 2 | `blog-classifier` | Every day — no exceptions |
| 4 | `content-marketer` or `docs-architect` | Every day — no exceptions |
| 4 (parallel) | `code-reviewer` | Every draft containing code blocks |
| 5 | `blog-consistency-checker` + `article-consistency-checker` | Every Tier 2+ day |
| 5 | `blog-fact-checker` + `fact-checker` | Every Tier 3 day |
| 6 | `seo-meta-optimizer` | Every tier |
| 6 | `seo-structure-architect` + `seo-snippet-hunter` + `seo-keyword-strategist` | Every Tier 2+ day |
| 6 | `seo-authority-builder` + `seo-content-auditor` | Every Tier 3 day |
| 8 | email social bundle (if dispatching the send script) | Every Tier 2+ day |

**Reading these in context is not a substitute for dispatching them.** Main-thread context and agent-context are different pools; the agent works on the brief you hand it with a clean slate, which is the point. If briefing feels expensive, use `references/writer-briefing-template.md` — it turns four briefings into a four-parallel tool-call.

**Inline fallback ONLY after a real Agent-tool error.** See `references/write-post.md § Inline-Writer Fallback` for the strict definition. Efficiency is not a qualifying reason.

**Phase markers (MANDATORY for cron diagnosability)** — Before starting each of steps 0–8 below, emit a single Bash echo so the cron wrapper's log can be bisected by phase without parsing `~/.claude/projects/*.jsonl`:

```bash
echo "[phase: <name>] <one-line context>"
```

Allowed `<name>` values, in order: `preflight`, `gather`, `classify`, `record-decision`, `write`, `quality-gates`, `seo-polish`, `publish`, `audit-trail`, `crosspost-queue`, `social-bundle`. The `<one-line context>` is free text — typically the target date, the chosen tier, the agent being dispatched, or the artifact path. Examples:

```bash
echo "[phase: classify] dispatching blog-classifier for 2026-05-27"
echo "[phase: write] dispatching docs-architect for Tier 2 vite post"
echo "[phase: publish] hugo build + git commit on master"
```

This is **load-bearing**: the 2026-05-28 root-cause work depended on these markers to bisect a 23-minute run into per-phase wall time. Skipping them turns the next timeout opaque again.

---

0. **Check for existing post** — Search `content/posts/` for any file whose front matter contains a `date` starting with this day's `YYYY-MM-DD`. Use: `grep -rl "^date = '$YYYY-MM-DD" content/posts/` (TOML) or `grep -rl "^date: $YYYY-MM-DD" content/posts/` (YAML). If a post already exists for this date, **skip this day entirely**. Log: `"Post exists for YYYY-MM-DD, skipping."` This allows safe full-month ranges (e.g., `/blog-backfill 2025-09-01 2025-09-30`) without overwriting existing posts.

1. **Gather source material** — Read `references/gather-material.md` for git log commands, PR fetching, beads history, session transcripts, email signals (optional), and CLAUDE.md context gathering.

2. **Classify the day** — Invoke the `blog-classifier` agent (defined in `agents/blog-classifier.md`) with all gathered material. The agent returns a JSON classification object with tier, confidence, dimension scores, thesis candidate, and rhetorical structure. Read `references/classify-day.md` for the full classifier prompt and `references/content-tier-classification.md` for tier definitions and scoring anchors.

3. **Record decision** — Append the classification result to `${CLAUDE_SKILL_DIR}/methodology/decisions.jsonl` as a single JSON line:
   ```json
   {
     "date": "YYYY-MM-DD",
     "slug": "post-slug",
     "tier": 2,
     "tier_name": "Technical Deep-Dive",
     "confidence": 0.85,
     "dimensions": { "novelty": 3, "arc": 4, "nar": 3, "tch": 4, "scp": 5, "rpr": 3 },
     "reasoning": "...",
     "alternatives_considered": "...",
     "thesis_candidate": "...",
     "rhetorical_structure": "problem-solution",
     "source_signals": { "git": "strong", "prs": "strong", "session": "moderate", "beads": "absent", "email": "absent" },
     "anti_inflation_flags": ["none triggered"],
     "cadence_type": "daily"
   }
   ```

4. **Write the post** — Dispatch a tier-specific **writer agent** via the Agent tool. Read `references/write-post.md` for the full selection matrix, briefing template, and fallback rules.
   - **Tier 1 (Field Note):** `content-marketer` agent, 80-140 lines, concise narrative log
   - **Tier 2 (Deep-Dive):** `content-marketer` or `docs-architect` agent (pick by subject), 150-250 lines, problem/approach/result arc
   - **Tier 3 (Case Study):** `docs-architect` agent, 300-500 lines, thesis-driven structure
   - **All tiers with code blocks:** `code-reviewer` agent runs on the draft in parallel with the first quality gate

5. **Quality gates (tier-dependent, all run in parallel per tier):**

   | Gate | Tier 1 | Tier 2 | Tier 3 |
   |------|:------:|:------:|:------:|
   | Hugo build | ✓ | ✓ | ✓ |
   | `code-reviewer` agent (if code present) | ✓ | ✓ | ✓ |
   | `blog-consistency-checker` agent (skill-local, tier-aware) | — | ✓ | ✓ |
   | `article-consistency-checker` agent (global, second pair of eyes) | — | ✓ | ✓ |
   | `blog-fact-checker` agent (skill-local) | — | — | ✓ |
   | `fact-checker` agent (global) | — | — | ✓ |

   If any agent returns `BLOCK`, revise the post and re-run the failing gate. `REVISE` suggestions are applied if confidence is high; otherwise flagged in the audit trail. `PASS` proceeds to step 6.

6. **SEO polish (Tier 1–3, tier-scaled)** — Read `references/polish-seo.md` for the full pipeline. Runs after quality gates pass, before first commit:
   - **Tier 1:** `seo-meta-optimizer`
   - **Tier 2:** add `seo-structure-architect`, `seo-snippet-hunter`, `seo-keyword-strategist`
   - **Tier 3:** add `seo-authority-builder`, `seo-content-auditor` (must PASS)

7. **Verify and publish** — Hugo build, commit, push to master, dual-publish to tonsofskills.com, conditional sync to intentsolutions.io. Read `references/publish-verify.md` for exact commands.

8. **Record agent audit trail** — Update the decision record in `decisions.jsonl` with the `agent_audit` block listing every agent invocation and verdict. Schema in `references/polish-seo.md`.

7. **Queue cross-posts** — Tier-specific distribution per `references/content-strategy.md`:
   - **Tier 1:** startaitools + tonsofskills only (no cross-posting)
   - **Tier 2+:** Full cross-post queue (+24h Dev.to/Hashnode, +48h Medium). Read `references/crosspost-queue.md` for schema and logic.

8. **Social email bundle** — Tier-specific per `references/content-strategy.md`:
   - **Tier 1:** Optional X post only
   - **Tier 2+:** X thread (3 tweets) + LinkedIn post + Substack draft. Read `references/social-bundle.md` for format specs.

### Phase 2W: Weekly Recap (if `weekly` argument or cron trigger)

Generate a weekly recap post. Read `references/cadence-system.md` for the full template and generation logic. Writes to `content/posts/week-NN-recap-YYYY.md`.

### Phase 2M: Monthly Retrospective (if `monthly` argument or cron trigger)

Generate a monthly retrospective. Read `references/cadence-system.md` for the full template and generation logic. Includes methodology calibration snapshot from `methodology/decisions.jsonl`. Writes to `content/monthly-recaps/MONTH-YYYY.md` (e.g., `content/monthly-recaps/september-2025.md`).

### Phase 3: Final Verification

Read `references/final-verification.md` for the complete checklist including methodology decision record verification, tier distribution sanity check, and quality gate compliance audit.

**Always-run at the end of every batch:**
```bash
${CLAUDE_SKILL_DIR}/scripts/rebuild-methodology-index.sh
```
This derives the SQLite analytics index (`methodology/index.db`) from the append-only JSONL source-of-truth files so `/blog-calibrate` and `/blog-feedback` queries stay current.

## Output

| Artifact | Location |
|----------|----------|
| Hugo blog post | `content/posts/SLUG.md` |
| Decision record | `methodology/decisions.jsonl` (appended) |
| Astro copy | `claude-code-plugins/marketplace/src/content/blog-posts/SLUG.md` |
| Field notes (conditional) | `intent-solutions-landing/astro-site/src/content/field-notes/SLUG.md` |
| Cross-post queue | `.crosspost-queue.json` |
| X thread | `x-threads/YYYY-MM-DD-SLUG-backfill-x3.txt` |
| LinkedIn post | `linkedin-posts/YYYY-MM-DD-SLUG.txt` |
| Social bundle | `/tmp/social-bundle-SLUG.txt` |
| Weekly recap | `content/posts/week-NN-recap-YYYY.md` |
| Monthly retro | `content/monthly-recaps/MONTH-YYYY.md` |

## Error Handling

- **Hugo build fails:** Fix the post, rebuild. Do not push broken builds.
- **Classification returns invalid JSON:** Re-run classifier with explicit schema reminder. If still fails, default to Tier 1.
- **Consistency/fact-check agent returns BLOCK:** Fix the flagged issues and re-run the quality gate. Do not publish until PASS or REVISE.
- **Cross-post API key missing:** Scripts skip gracefully with `SKIP:` message. No error.
- **Cross-post API fails:** Logged in `.crosspost-queue.json` as `"status": "failed"` with error. Re-run queue processor after fixing.
- **Email send fails:** Print bundle path (`/tmp/social-bundle-SLUG.txt`) for manual copy.
- **No git activity for a day:** Skip that day. Do not generate filler posts.
- **decisions.jsonl append fails:** Non-fatal warning. JSONL is append-only; retry once. The post can still publish without the decision record.

## Efficiency Tips

- Process 3-4 days at a time: gather material, run classifiers in parallel
- Commit in batches (4-5 posts per commit) to reduce push overhead
- Hugo build check once per batch, not per post
- Push once per batch
- Tier 2+ quality gates can run in parallel with the next day's material gathering

## Automation (RemoteTrigger)

Three persistent cron triggers automate the cadence system. Set up via `/schedule`:

- **Daily:** `cron "17 6 * * *"` — runs `/blog-backfill` for yesterday
- **Weekly:** `cron "42 17 * * 5"` — generates weekly recap
- **Monthly:** `cron "23 8 1 * *"` — generates monthly retrospective

See `references/cadence-system.md` for full trigger specifications and prompts.

## Related Skills

- `/blog-calibrate` — monthly calibration report from decisions.jsonl + feedback.jsonl
- `/blog-feedback <slug>` — post-publication assessment (was the tier correct?)
- `/blog-research-article` — Tier 4 Distinguished Paper workflow (manual, interactive)

## Examples

**Backfill a specific date range with auto-classification:**
```
/blog-backfill 2026-03-01 2026-03-15
```
Generates 15 posts, each auto-classified into the appropriate tier. Records all classification decisions. Applies tier-specific quality gates. Publishes to startaitools.com, dual-publishes to tonsofskills.com, queues cross-posts for Tier 2+ posts.

**Auto-detect and fill the gap:**
```
/blog-backfill
```
No arguments — automatically determines START (day after last post) and END (yesterday).

**Generate weekly recap:**
```
/blog-backfill weekly
```
Rolls up the current week's daily posts into a recap with metrics and highlights.

**Generate monthly retrospective:**
```
/blog-backfill monthly
```
Generates the previous month's retrospective with velocity dashboard, tier distribution, and calibration snapshot.

## Critical Reminders

- Deploy branch is `master` (not main)
- Netlify auto-deploys on push (no GitHub Actions needed)
- Filename is `slug.md` (no date prefix)
- Front matter is TOML (`+++` delimiters)
- All repos are local at `/home/jeremy/000-projects/` — no cloning needed
- No mermaid diagrams — site never uses them
- Hugo v0.150.0 locked in netlify.toml
- Use `--buildFuture` in build commands
- decisions.jsonl is append-only — never edit existing records
- Tier 4 is NEVER auto-assigned — it's a separate manual workflow

## Resources

**Reference files:** [gather-material](references/gather-material.md), [classify-day](references/classify-day.md), [content-tier-classification](references/content-tier-classification.md), [write-post](references/write-post.md), [polish-seo](references/polish-seo.md), [content-strategy](references/content-strategy.md), [cadence-system](references/cadence-system.md), [publish-verify](references/publish-verify.md), [crosspost-queue](references/crosspost-queue.md), [social-bundle](references/social-bundle.md), [final-verification](references/final-verification.md).

**Agent definitions:** [blog-classifier](agents/blog-classifier.md), [blog-consistency-checker](agents/blog-consistency-checker.md), [blog-fact-checker](agents/blog-fact-checker.md).

**Methodology tracking:** [decisions.jsonl](methodology/decisions.jsonl), [feedback.jsonl](methodology/feedback.jsonl), [patterns.jsonl](methodology/patterns.jsonl), [rebuild-index.sql](methodology/rebuild-index.sql).
