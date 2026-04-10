+++
title = 'Executive Intent Proof System and git-with-intent Audit Pipeline'
slug = 'executive-intent-proof-system-gwi-audit-pipeline'
date = 2026-01-12T10:00:00-06:00
draft = false
tags = ["architecture", "gcp", "testing", "ci-cd", "devops"]
categories = ["Development Journey"]
description = "Twenty-nine commits across four repos. Executive Intent gets a full proof system with evidence taxonomy and pipeline health. git-with-intent ships an audit log with policy violation detection."
+++

Twenty-nine commits. The highest single-day count since the marketplace launch sprint in October. January 12th was about making systems provable — building the infrastructure to demonstrate that things work, not just assert that they do.

Two projects, one principle: if you can't show your evidence chain, your conclusions are opinions. Executive Intent got a proof system that traces every recommendation back to data. git-with-intent got an audit log that traces every code change back to a declared intent.

## Executive Intent: The Proof System

The MVP scaffold from yesterday gave Executive Intent its skeleton. Today filled it with a proof system — the mechanism by which the platform demonstrates that its recommendations are grounded in real data rather than hallucinated confidence.

**Evidence taxonomy.** Every recommendation the system produces must cite its sources. The taxonomy classifies evidence into five types:

- **Metric** — a quantitative measurement from a connected data source
- **Document** — a referenced policy, report, or analysis
- **Pattern** — a recurring signal detected across multiple data points
- **Expert** — a human-validated judgment or override
- **Derived** — a conclusion drawn from combining other evidence types

Each evidence item carries a confidence score (0-1), a freshness timestamp, and a provenance chain showing how it was obtained. The UI renders this as collapsible citation blocks beneath each recommendation.

The taxonomy isn't arbitrary. It maps to the five ways executives actually evaluate information. A metric is the strongest signal. A document is context. A pattern is a hypothesis. Expert input is a sanity check. Derived evidence is the platform's own synthesis. By labeling each type explicitly, the decision-maker can weight the evidence appropriately instead of treating all citations as equally reliable.

**Pipeline health.** The proof system is only as good as the data flowing into it. Added a health dashboard that tracks:

- Data source connectivity (is each integration alive?)
- Evidence freshness (when was the last update from each source?)
- Pipeline latency (how long does it take from data change to evidence availability?)
- Coverage gaps (which recommendation types lack supporting evidence?)

When a data source goes stale or a pipeline segment fails, the health dashboard flags it. Recommendations based on stale evidence get a visual warning. The system degrades visibly instead of silently.

Visible degradation is a design choice, not a limitation. A system that hides its failures is a system that produces confident-looking outputs from stale data. An executive who sees "data source offline for 6 hours" knows to treat that recommendation cautiously. An executive who sees a clean recommendation based on 6-hour-old data makes a bad decision and blames the platform.

**UI design system.** Established the component library — cards, tables, badges, and the evidence citation component. Built with a dark theme from the start (executives review dashboards in dimmed conference rooms). Consistent spacing, consistent typography, consistent color palette. The design system is in the repo as a Storybook instance, not a Figma file.

Storybook over Figma is a deliberate choice. Design files drift from implementation. A Storybook instance runs the actual React components with actual data — what you see in Storybook is what ships to production. The tradeoff is that designers who prefer visual tools can't edit the system directly. For a team of one, that tradeoff is easy.

**Secret Manager CI.** Wired Google Cloud Secret Manager into the CI pipeline. API keys and service account credentials are loaded from Secret Manager at build time, not from environment variables or `.env` files. The CI pipeline authenticates via Workload Identity Federation — no long-lived service account keys in GitHub Secrets.

Workload Identity Federation is the right approach but annoying to set up. You need a GCP workload identity pool, a provider linked to GitHub's OIDC, and IAM bindings that scope access to the specific repo. Once configured, the GitHub Actions workflow requests a short-lived token from GCP on every run. No secrets to rotate, no keys to leak. The setup is a one-time cost that eliminates an entire category of security incidents.

## git-with-intent: Audit Log and Policy Violations

git-with-intent (GWI) gained two capabilities that turn it from a commit tool into a governance tool.

**Audit log.** Every GWI operation now writes a structured log entry: who ran the command, what intent was declared, which files were affected, and the outcome (success/failure/warning). The log is append-only and stored alongside the git history. Running `gwi audit` dumps the log for a given time range.

The audit log entries span phases D3.4 through D5.1 of the development lifecycle — from the point where a developer declares intent through the point where the change is verified in production. This gives you a complete chain: "developer declared intent X, committed files Y, pipeline ran checks Z, change deployed at time T."

The log format is JSONL — one JSON object per line. This makes it trivially parseable with `jq`, grepable with standard tools, and appendable without reading the entire file. A month of developer activity in a single repo produces maybe 500KB of audit log. Small enough to keep forever, structured enough to query meaningfully.

**Policy violation detection.** GWI now checks each commit against a configurable policy set. Policies include:

- Maximum file count per commit (prevent monolithic commits)
- Required intent declaration (no "misc fixes" allowed)
- Protected path patterns (certain directories require review)
- Time-based restrictions (no deploys during incident windows)

Violations are logged but not blocked — the tool warns rather than prevents. The philosophy is that developers should know when they're breaking policy, but the tool shouldn't be a gate that stops production hotfixes. A tool that blocks a critical fix at 2 AM because the commit message is too short is a tool that gets bypassed permanently. Warning and logging preserves the audit trail without creating adversarial incentives.

The policy configuration is YAML. Each rule has a severity (info, warning, error), a pattern, and a human-readable message. Teams can customize policies per repository by overriding the defaults in their repo's `.gwi/policies.yml`. The defaults are deliberately conservative — they flag common problems without being opinionated about workflow.

---

Twenty-nine commits across four repos. Executive Intent now proves its recommendations with evidence chains. git-with-intent now records what happened and flags when it shouldn't have. Both systems share the same principle: trust comes from transparency, not assertion. Show your work, or your conclusions are opinions.

The day was a sprint, but the output is infrastructure that compounds. Every recommendation Executive Intent produces will cite its evidence. Every commit through git-with-intent will be auditable. The proof system and the audit log are the foundations that everything else builds on.

### Related Posts

- [git-with-intent v0.9.0-v0.10.0: Docker Upgrades and Audit Features](/posts/git-with-intent-v090-v0100-docker-upgrades/)
- [GWI RBAC Governance and Hustle CI Stabilization](/posts/gwi-rbac-governance-hustle-ci-stabilization/)
- [Executive Intent MVP Scaffold, Drop Coaching Curriculum, and Bounty Tracker Buildout](/posts/executive-intent-mvp-drop-coaching-bounty-buildout/)
