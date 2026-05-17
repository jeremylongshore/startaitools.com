# Multi-Cadence Publishing System

Four cadences: daily (auto), weekly (auto), monthly (auto), on-demand (manual Tier 4).

---

## Cadence Overview

| Cadence | Content | Schedule | Automation |
|---------|---------|----------|------------|
| Daily | Work journal post (Tier 1-3) | Every day, 6:17 AM CT | RemoteTrigger cron |
| Weekly | Recap rolling up the week's posts | Friday 5:42 PM CT | RemoteTrigger cron |
| Monthly | Retrospective — trends, wins, lessons, velocity | 1st of month, 8:23 AM CT | RemoteTrigger cron |
| On-demand | Distinguished Paper (Tier 4) | When user has an article | Manual `/blog-research-article` |

---

## Weekly Recap Structure

**Filename:** `content/posts/week-NN-recap-YYYY.md`
**Category:** `Weekly Recap`
**Tags:** `["weekly-recap", "metrics", ...]` (add tags for major themes of the week)

### Template

```markdown
## Week {NN}: {Date Range}

### What Shipped

{Bulleted list of concrete deliverables — releases, features, fixes. Link to daily posts.}

### Posts This Week

| Day | Tier | Title | Key Topic |
|-----|------|-------|-----------|
| Mon | 1 | [Title](/posts/slug/) | ... |
| Tue | 2 | [Title](/posts/slug/) | ... |
| ... | ... | ... | ... |

### By the Numbers

- **Repos active:** {N}
- **Commits:** {N}
- **PRs merged:** {N}
- **Posts published:** {N} ({N} Tier 1, {N} Tier 2, {N} Tier 3)

### Highlight of the Week

{1-2 paragraphs on the most interesting debugging journey, biggest ship, or most consequential design decision. This is the section that makes someone want to click through to the daily post.}

### Patterns & Observations

{What recurred this week? What's building momentum? What should change next week?}
```

### Generation Logic

1. Read all daily posts from the week (Mon-Fri or Mon-Sun depending on activity)
2. Read `methodology/decisions.jsonl` for the week's tier classifications
3. Gather aggregate git stats: `git log --oneline --after="MONDAY" --before="SATURDAY"` across all repos
4. Gather merged PRs: `gh pr list --state merged` filtered by merge date
5. Synthesize — don't just list, find the thread connecting the week
6. Write directly to `content/posts/week-NN-recap-YYYY.md`
7. Hugo build, commit, push to master

---

## Monthly Retrospective Structure

**Filename:** `content/monthly-recaps/MONTH-YYYY.md` (e.g., `september-2025.md`)
**Category:** `Monthly Retrospective`
**Tags:** `["monthly-retro", "metrics", "retrospective", ...]`

### Template

```markdown
## {Month YYYY} Retrospective

### Velocity Dashboard

| Metric | This Month | Last Month | Delta |
|--------|-----------|------------|-------|
| Commits | {N} | {N} | {+/-N} |
| PRs merged | {N} | {N} | {+/-N} |
| Releases | {N} | {N} | {+/-N} |
| Posts published | {N} | {N} | {+/-N} |
| Tier 1 posts | {N} ({%}) | {N} ({%}) | |
| Tier 2 posts | {N} ({%}) | {N} ({%}) | |
| Tier 3 posts | {N} ({%}) | {N} ({%}) | |

### Top 3 Posts by Teaching Potential

{Ranked by TCH dimension score from decisions.jsonl. Brief description of why each matters.}

1. [{Title}](/posts/slug/) — TCH: {N}. {One-sentence summary.}
2. [{Title}](/posts/slug/) — TCH: {N}. {One-sentence summary.}
3. [{Title}](/posts/slug/) — TCH: {N}. {One-sentence summary.}

### Projects: Started / Shipped / In Progress

| Status | Project | Notes |
|--------|---------|-------|
| Shipped | ... | ... |
| In Progress | ... | ... |
| Started | ... | ... |

### Methodology Calibration

{Snapshot from decisions.jsonl analysis:}
- **Tier distribution:** {histogram}
- **Average confidence:** {N}
- **Anti-inflation flags triggered:** {count and most common}
- **Calibration drift:** {Are we inflating? Stable? Deflating?}

### Content Strategy Metrics

- **Cross-post performance:** {Dev.to / Hashnode / Medium engagement if available}
- **Subscriber growth:** {If tracked}
- **Most-shared post:** {If data available}

### Wins

{3-5 bullet points — things that went well}

### Lessons Learned

{3-5 bullet points — things to do differently}

### Next Month Focus

{2-3 priorities for the coming month}
```

### Generation Logic

1. Read all daily posts and weekly recaps from the month
2. Read all entries from `methodology/decisions.jsonl` for the month
3. Read `methodology/feedback.jsonl` for any post-publication assessments
4. Read `methodology/patterns.jsonl` for accumulated rules
5. Gather aggregate git stats for the full month across all repos
6. Compare with previous month's retrospective (if exists)
7. Run calibration analysis (see `references/calibration-report.md` when created via `/blog-calibrate`)
8. Write directly to `content/monthly-recaps/MONTH-YYYY.md` (e.g., `content/monthly-recaps/september-2025.md`)
9. Hugo build, commit, push to master

---

## RemoteTrigger Specifications

### Daily Backfill Trigger

```
Schedule: cron "17 6 * * *" (6:17 AM CT daily)
Context: startaitools repo
Prompt:
  Run /blog-backfill for yesterday's date. Use the content tier classification
  system to auto-classify the day. Record the decision in methodology/decisions.jsonl.
  Apply tier-appropriate quality gates. Commit, push to master, verify Netlify deploy.
  Email jeremy@intentsolutions.io with subject "Daily Post Published: {title} (Tier {N})"
  or "Daily Post Skipped: no git activity" if no activity detected.
```

### Weekly Recap Trigger

```
Schedule: cron "42 17 * * 5" (Friday 5:42 PM CT)
Context: startaitools repo
Prompt:
  Generate a weekly recap post for this week. Read all daily posts published
  Mon-Fri this week from content/posts/. Read methodology/decisions.jsonl for
  tier classifications. Gather aggregate git stats and PR counts. Follow the
  weekly recap template in references/cadence-system.md. Write to
  content/posts/week-NN-recap-YYYY.md. Hugo build, commit, push to master.
  Email jeremy@intentsolutions.io with subject "Weekly Recap Published: Week {NN}".
```

### Monthly Retrospective Trigger

```
Schedule: cron "23 8 1 * *" (1st of month, 8:23 AM CT)
Context: startaitools repo
Prompt:
  Generate a monthly retrospective for the previous month. Read all daily posts
  and weekly recaps. Read methodology/decisions.jsonl, feedback.jsonl, and
  patterns.jsonl. Follow the monthly retrospective template in
  references/cadence-system.md. Compare with previous month if available.
  Run calibration analysis. Write to content/monthly-recaps/MONTH-YYYY.md (e.g., september-2025.md).
  Hugo build, commit, push to master.
  Email jeremy@intentsolutions.io with subject "Monthly Retro Published: {Month YYYY}".
```

---

## CronCreate vs RemoteTrigger

| Mechanism | Persistence | Use Case |
|-----------|-------------|----------|
| RemoteTrigger | Persistent, survives session restarts | Daily/weekly/monthly cadence automation |
| CronCreate | Session-scoped, 7-day max | In-session monitoring (e.g., check backfill progress every 30 min) |

RemoteTrigger creates remote agents on claude.ai that wake up on cron schedule, run autonomously, commit, push, and deploy. No active session needed.

CronCreate is for ephemeral monitoring only. Do not use it for persistent automation.

---

## /monitor Integration

For long-running backfill operations (e.g., backfilling 2+ weeks), use `/monitor` to live-stream pipeline progress:

```
Monitor the blog-backfill pipeline:
- Watch for new post files in content/posts/
- Report tier classification results as they come in
- Flag any Hugo build failures immediately
- Show progress: {N}/{total} days processed
```

This uses CronCreate internally (session-scoped) and provides real-time visibility into batch operations. Particularly useful when running the full pipeline for the first time after implementing the tier system.
