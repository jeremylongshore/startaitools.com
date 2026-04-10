+++
title = 'Governance Day: Proprietary Licenses, Portfolio Refresh, and STCI Dashboard v0.5.0'
slug = 'governance-day-licenses-portfolio-stci-dashboard'
date = 2026-01-07T10:00:00-06:00
draft = false
tags = ["devops", "architecture", "full-stack"]
categories = ["Development Journey"]
description = "Slapping proprietary licenses on two repos, updating the personal landing page with 22 projects, and shipping an enterprise usage dashboard at v0.5.0."
+++

Not every productive day involves writing application code. Some days the work is governance — the legal and organizational scaffolding that lets everything else move faster.

January 7th was four commits across four repos. All housekeeping. All overdue.

The kind of work that sits on a TODO list for weeks because there's always a more interesting problem to solve. But governance debt compounds. A missing license today is a legal question tomorrow. A stale portfolio today is a missed opportunity next week.

## Proprietary Licenses on Lumera-Emanuel and Local-RAG-Agent

Both repos had been running with no explicit license, which under copyright law means "all rights reserved" by default. That's fine legally, but it creates ambiguity. Contributors don't know what they can do. Forks don't know what they can't. And anyone running a compliance scan on your org flags "no license" as a risk even though the default is restrictive.

The fix was straightforward: apply the Intent Solutions proprietary license template to both repositories. The template is a standard restrictive license — source viewable, no redistribution, no derivative works without written permission.

Why not MIT or Apache 2.0? For developer tools and CLI utilities, permissive licenses make sense. They lower the barrier to adoption and signal that you're building in the open. But for core product components — the memory system, the retrieval pipeline — a permissive license is giving away the thing you're trying to sell. It's the right default for tools that contain business logic you don't want cloned.

Lumera-Emanuel is the agent memory layer — the component that stores and retrieves agent context across sessions. Letting someone fork that means giving them the memory architecture for free. Local-RAG-Agent is the retrieval stack that powers document search. Same logic: the retrieval pipeline is a differentiator, not a commodity.

The decision matrix is simple. Open-source the utilities and CLI tools — they attract contributors and cost nothing to share. Protect the components where the architecture itself is the product. Both repos sit at the core of the product architecture, so proprietary is the correct call.

The actual license text is templated. A `LICENSE-TEMPLATE-PROPRIETARY.txt` lives in the org's meta-repo with placeholders for project name and year. Apply it to a new repo by copying the file and filling in two values. The goal is that adding a license to any repo takes under sixty seconds, so "I'll do it later" has no excuse.

There's a bulk automation script (`add-licenses-github.py`) that applies the license to repos via the GitHub API. For today's two repos, manual application was faster. For the next batch of unlicensed repos — and there will be a next batch — the script is waiting. It uses `gh api` under the hood, creating a commit on each repo's default branch with the LICENSE file. One command, N repos licensed.

Two commits. Two `LICENSE` files. Legal exposure closed.

## Landing Page: 22 Projects, One Page

The personal landing page at jeremylongshore.com was stale. It listed maybe eight projects, several of which had evolved or been renamed since the last update. The portfolio had grown to 22 active projects without the front door reflecting it.

The update was a content refresh, not a redesign. Every project got a one-liner description and a link to its repo or live URL. Grouped by category: production platforms, AI agents, developer tools, infrastructure. The goal is that someone landing on the page can understand the scope of the portfolio in under thirty seconds.

The grouping matters more than it seems. A flat list of 22 projects looks like chaos. The same 22 projects organized into four categories look like a deliberate portfolio. Production platforms first (the things that make money), AI agents second (the things that are interesting), developer tools third (the things other engineers use), infrastructure last (the things nobody sees but everything depends on).

No new components. No CSS changes. Just accurate content where outdated content used to be. The whole update was maybe forty-five minutes of writing project descriptions. That's the advantage of a content refresh over a redesign — the existing layout works, so the only variable is whether the content is current.

The test is simple: can a hiring manager or potential collaborator understand what you do in thirty seconds? If the answer is "no," the portfolio is broken regardless of how good the CSS is.

Each project entry links directly to its GitHub repo or live URL. No intermediary pages, no "click here to learn more" funnels. The landing page is a routing table, not a sales pitch. People who land here already know who I am — they just need to find the right link quickly.

## STCI Enterprise Usage Dashboard v0.5.0

The STCI dashboard tracks enterprise usage metrics — API call volumes, active users, feature adoption rates. v0.5.0 added the first real visualization layer on top of the raw data.

Before this release, the dashboard was a table. Rows of numbers. Useful if you already knew what you were looking for, useless for spotting trends. The v0.5.0 update added time-series charts for the core metrics and a summary card row at the top showing the numbers that matter: total API calls this month, month-over-month growth, and active enterprise accounts.

The summary cards follow a simple pattern: big number, label, trend indicator. Green up-arrow if the metric is growing, red down-arrow if it's shrinking, gray dash if it's flat. An executive glances at four cards and knows the health of the platform in two seconds. The time-series charts below give the detail for anyone who wants to drill in.

The chart library is Recharts — lightweight, React-native, and good enough for internal dashboards. No custom D3 work needed for basic line and bar charts. The data pipeline feeds from Firestore aggregation queries that run on a daily schedule. The aggregation is done server-side in a Cloud Function that writes summary documents, so the dashboard reads pre-computed data instead of running queries on every page load.

The v0.5.0 release also added a date range selector so users can narrow the charts to a specific week or month. Sounds trivial, but without it every chart shows "all time" data where recent trends get buried under historical noise.

The dashboard is internal-only for now. No authentication beyond the Firebase project-level access controls. If it ever needs to be shared with external stakeholders, the auth layer is already there via Firebase Auth — it just needs login UI and permission rules. Building on Firebase means the security primitives are available even when you're not using them yet.

The data was already there. The dashboard just wasn't showing it in a way that told a story. That's the recurring theme with internal dashboards — the backend work gets done because it's engineering, but the presentation layer gets deferred because it's "just UI." Meanwhile, the people who need the data can't find it in a spreadsheet-looking table with no visual hierarchy.

## The Governance Tax

The total time investment for all four commits was maybe three hours. Two hours for the portfolio content, thirty minutes for the dashboard charts, thirty minutes for the license files. That's a low price for closing three different categories of technical debt.

The pattern I've settled into is dedicating one day per week to pure governance. No feature work, no bug fixes. Just licenses, documentation, dependency updates, and portfolio maintenance. The alternative — sprinkling governance work into feature days — doesn't work. It always gets deprioritized in favor of the next shiny thing.

---

Four commits, four repos. License gaps closed, portfolio updated, dashboard shipped. Zero features added, three categories of debt eliminated. The kind of day that doesn't make for dramatic reading but prevents problems that would.

Governance days feel unproductive while you're doing them. You don't ship anything visible. No demo, no changelog, no PR with a feature title. But the portfolio is accurate, the repos are legally clean, and the dashboard tells a story. Tomorrow's feature work will happen faster because today's foundation work is done.

### Related Posts

- [Beads Rollout: Twenty-Two Repos and Org-Wide Governance](/posts/beads-rollout-twenty-two-repos-org-governance/)
- [Intent Solutions Portfolio 2025: Production Deployment Velocity](/posts/intent-solutions-portfolio-2025-production-deployment-velocity/)
- [Lumera-Emanuel Launch and git-with-intent Open Source Release](/posts/lumera-emanuel-launch-gwi-open-source-release/)
