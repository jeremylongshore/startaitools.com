+++
title = 'Executive Intent UI Polish and Bounty Tracker Airtable Sync'
slug = 'executive-intent-ui-polish-bounty-airtable-sync'
date = 2026-01-13T10:00:00-06:00
draft = false
tags = ["web-development", "automation", "ci-cd", "full-stack"]
categories = ["Development Journey"]
description = "Six commits across two repos. Five contrast and styling fixes on Executive Intent. One GitHub Actions workflow connecting the bounty tracker to Airtable."
+++

Light day after yesterday's twenty-nine commit marathon. Six commits, two repos. The kind of focused polish work that's easy to skip and hard to go back and do later.

The pattern with UI polish is that each individual fix seems trivial — change a color, fix an alignment, adjust a width. But the cumulative effect is the difference between "this looks like a prototype" and "this looks like a product." Five small fixes can shift user perception more than one large feature.

## Executive Intent: Five Contrast and Styling Fixes

The UI design system from yesterday looked solid in Storybook. On a real screen with real data, it had problems.

**Card contrast.** The evidence citation cards used a background color that was too close to the page background. On a projector or a low-contrast laptop display, the cards disappeared into the surface. Bumped the card background from `#1a1f2e` to `#1e2436` — enough separation to read as distinct elements without breaking the dark theme. The contrast ratio went from 1.08:1 to 1.15:1 against the page surface. Still subtle, but the human eye picks up the difference.

**Badge legibility.** The confidence score badges (HIGH, MEDIUM, LOW) used white text on colored backgrounds. The MEDIUM badge's amber background was too bright — the white text washed out. Switched to dark text for the amber and yellow badges, kept white for the darker colors.

**Table header alignment.** The pipeline health table had headers left-aligned but data cells center-aligned. Mixed alignment makes tables harder to scan. Aligned everything left. Numbers in a column are easier to compare when they share a left edge, despite what design tutorials say about centering numeric data. The exception is short status columns (OK/WARN/ERR) where centering does improve scannability — but those are the only centered columns in the entire dashboard.

**Sidebar width on narrow screens.** The navigation sidebar was a fixed 280px, which ate too much horizontal space on 1366px displays — the most common laptop resolution. Changed to a collapsible sidebar that defaults to collapsed on viewports under 1440px. The sidebar state persists in localStorage, same pattern as the Braves dashboard column sizes. Set it once, forget about it.

**Loading state flicker.** The evidence panel showed a loading skeleton, then the content, then briefly flashed back to the skeleton before settling. The cause was a React state update ordering issue — the "loading" state was being set after the data had already arrived, then immediately cleared. Moved the `setLoading(false)` call inside the data fetch callback instead of after it.

```typescript
// Before: flicker
setLoading(true);
const data = await fetchEvidence();
setEvidence(data);
setLoading(false); // runs after re-render from setEvidence

// After: no flicker
setLoading(true);
const data = await fetchEvidence();
setLoading(false);
setEvidence(data);
```

The ordering matters because React batches state updates within the same microtask but not across async boundaries in older React versions. Setting loading to false after setting the data triggers two separate renders. Setting loading to false before the data triggers one batched render.

Five fixes. None of them are architectural. All of them are things a user would notice in the first ten seconds.

## Bounty Tracker: Airtable Auto-Sync

The bounty tracker has been accumulating data locally. The team uses Airtable as the shared visibility layer — PMs check Airtable, not GitHub. So the tracker needs to push its data there.

Built a GitHub Actions workflow that syncs on every push to main and on a daily schedule:

```yaml
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 6 * * *'
```

The sync reads the tracker's JSON data file, maps each bounty to an Airtable record, and upserts via the Airtable API. New bounties create records. Status changes update existing records. The Airtable base has views for "Open," "In Progress," "Submitted," and "Paid" — each auto-filtered from the synced data.

The workflow authenticates via an `AIRTABLE_PAT` stored in GitHub Secrets. The personal access token is scoped to the single base — if it leaks, the blast radius is one Airtable workspace, not the entire Airtable org.

The upsert logic uses the bounty's GitHub issue URL as the unique key. If a record with that URL exists, update it. If not, create it. This means the sync is idempotent — running it twice produces the same result. No duplicate records, no orphaned entries.

One workflow file. One sync script. The team sees bounty status in Airtable without anyone manually updating a spreadsheet. The push-on-main trigger catches real-time changes. The daily cron catches anything that the push trigger missed (webhook failures, manual edits to the JSON file outside of the normal workflow).

## Why Airtable Instead of a Custom Dashboard

The bounty tracker could have its own web UI. But the team already checks Airtable daily for project tracking. Adding bounty data to the existing tool means zero behavior change required. The best internal tool is the one people already use.

The sync approach also means the source of truth stays in git. The JSON file in the repo is canonical. Airtable is a read-only view. If Airtable data gets accidentally edited, the next sync overwrites it with the correct data. One-way data flow keeps things simple.

---

Six commits. Executive Intent's UI went from "works in Storybook" to "works on a real screen." The bounty tracker's data left the repo and landed where the team actually looks. Small day, clean results.

### Related Posts

- [Executive Intent Proof System and git-with-intent Audit Pipeline](/posts/executive-intent-proof-system-gwi-audit-pipeline/)
- [Resizable Columns and WCAG Contrast Fixes on the Braves Dashboard](/posts/resizable-columns-wcag-contrast-braves-dashboard/)
