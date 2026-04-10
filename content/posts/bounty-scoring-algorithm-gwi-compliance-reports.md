+++
title = 'Bounty Scoring Algorithm, GWI Compliance Reports, and Kilo Image Support'
slug = 'bounty-scoring-algorithm-gwi-compliance-reports'
date = 2026-01-17T10:00:00-06:00
draft = false
tags = ["bounty", "scoring-algorithm", "git-with-intent", "compliance", "github-api", "kilo"]
categories = ["Development Journey"]
description = "Building the bounty scoring algorithm with GitHub API integration and a discovery page, adding compliance report infrastructure to git-with-intent, and shipping image support for Kilo."
+++

Eight commits across three repos. The bounty work was the biggest chunk -- a scoring algorithm that needed to balance multiple competing signals. GWI compliance reports filled a gap in the audit story. Kilo image support was a feature request that took two commits.

## Bounty Scoring Algorithm

The bounty tracker needed a way to rank available bounties. Not just by dollar value -- a $5,000 bounty on an unfamiliar codebase in a language you don't know isn't worth more than a $500 bounty you can close in an hour.

### The Scoring Formula

The algorithm weighs five factors:

**Expected Value (40%)** -- bounty amount divided by estimated hours. Estimated hours come from the issue's label metadata (if the project uses size labels) or a heuristic based on issue age and comment count. Older issues with many comments tend to be harder.

**Familiarity (25%)** -- has the developer contributed to this repo before? How recently? How substantially? The GitHub API provides contributor statistics per repo. Recent, substantial contributions score highest.

**Competition (20%)** -- how many other people are working on this bounty? The algorithm checks for linked PRs, recent forks, and comment activity from non-maintainers. High competition reduces the score.

**Complexity (10%)** -- estimated from the issue description length, number of referenced files, and whether the issue links to other issues (dependency chains are harder).

**Freshness (5%)** -- newer bounties score slightly higher because they're less likely to have hidden gotchas that discouraged previous attempts.

### GitHub API Integration

The scoring engine pulls data from three GitHub API endpoints:

- `GET /repos/{owner}/{repo}/issues/{number}` -- issue metadata
- `GET /repos/{owner}/{repo}/stats/contributors` -- contributor history
- `GET /search/issues` -- discover new bounties across indexed organizations

Rate limiting is the main constraint. The authenticated API allows 5,000 requests per hour, but scanning across organizations burns through that fast. The engine caches contributor stats (they change slowly) and only refreshes issue data for bounties in the active queue.

### Discovery Page

A static HTML page generated from the scoring engine's output. It shows the top 20 bounties ranked by composite score, with filters for language, minimum value, and familiarity threshold. The page regenerates on each scoring run.

## GWI Compliance Reports (D4.1-D4.4)

git-with-intent's compliance reporting adds the paper trail that organizations need for audits.

### D4.1: Report Templates

Four report templates covering different compliance needs:

- **Agent Activity Report** -- all actions taken by a specific agent in a time window
- **Violation Summary** -- aggregated violation counts by category and severity
- **Intent Compliance** -- percentage of agent actions that matched declared intents
- **Remediation Status** -- open violations and their remediation progress

### D4.2: Evidence Collection

Each report template has an evidence collector that gathers supporting data. The agent activity report pulls git logs, API call records, and token usage. The violation summary pulls from the violation event store built in D5.x. Evidence is timestamped and signed with the organization's GPG key.

### D4.3: Scheduling

Reports can run on-demand or on a schedule. The scheduler uses cron expressions stored in the tenant config. Most organizations want weekly violation summaries and monthly intent compliance reports.

### D4.4: Report Signing

Generated reports get a detached GPG signature. The signing key is the organization's key, not the platform's, so reports are independently verifiable. The signed report plus its evidence bundle exports as a single tarball for archival.

## Kilo Image Support

Kilo (the internal knowledge base tool) gained image support in two commits. Previously, all content was text-only. The implementation stores images as base64 in the knowledge document (simple, no external storage dependency) with lazy decoding on render. A size cap of 2MB per image keeps the knowledge base from bloating.

## Numbers

| Metric | Value |
|--------|-------|
| Commits | 8 |
| Repos | 3 |
| Scoring factors | 5 |
| Report templates | 4 |
| Image size cap | 2MB |

## Related Posts

- [IRSB Protocol MVP, Vertex AI Embeddings, and GWI Violation Pipeline](/posts/irsb-protocol-mvp-vertex-embeddings-gwi-violations/) -- the violation detection pipeline that these compliance reports consume
- [GWI RBAC Governance and Hustle CI Stabilization](/posts/gwi-rbac-governance-hustle-ci-stabilization/) -- earlier GWI governance work
- [Knowledge Base: Zero to API Lifecycle State Machine](/posts/knowledge-base-zero-to-api-lifecycle-state-machine/) -- related knowledge base infrastructure
