+++
title = 'IRSB v0.1.0 Milestone, Perception YAML Feeds, and HN Expansion'
slug = 'irsb-v010-milestone-perception-yaml-feeds-hn-expansion'
date = 2026-02-05T10:00:00-06:00
draft = false
tags = ["irsb", "perception", "release-engineering", "ci", "hacker-news", "yaml", "firestore"]
categories = ["Development Journey"]
description = "IRSB monorepo reaches v0.1.0 with Phase 3-7 AARs, CI drift enforcement, and a CLAUDE.md rewrite. Perception adds 92 HN popular blog feeds and moves to YAML config with a named Firestore database."
+++

Two projects dominated February 5th. IRSB hit its first tagged release. Perception expanded its feed coverage by 72%.

## IRSB Monorepo: v0.1.0

Fourteen commits pushing the monorepo to its first milestone release. The version number is modest — v0.1.0, not v1.0.0 — because the protocol's smart contracts haven't been audited by a third party yet. But the infrastructure around the contracts is now release-quality.

### Phase 3-7 AARs

After-Action Reviews for each completed development phase. These aren't retrospective essays — they're structured documents covering what was planned, what actually happened, what went wrong, and what changes to apply in the next phase.

Phase 4's AAR caught that the CI pipeline was taking 12 minutes because it was running Solidity compilation, Slither analysis, and Foundry tests sequentially. Phase 5 parallelized them to 4 minutes.

Phase 6's AAR identified that the shared metrics package (built during Epic 1) was missing error counter instrumentation — errors were logged but not metered. You can't alert on what you don't measure.

The AARs aren't optional ceremony. They're the mechanism that prevents the same mistake from compounding across phases. Writing them takes 20 minutes per phase. The Phase 4 CI fix alone saved 8 minutes per pipeline run across every subsequent commit. At 14 commits on release day, that's nearly two hours of CI time saved from a 20-minute AAR.

### CI Drift Enforcement

The CI pipeline now fails if Terraform plan shows any drift from the declared state. The enforcement job runs `terraform plan -detailed-exitcode` and fails the check if the exit code is 2 (changes detected).

This closes the loop on the drift detection work from two days ago — detection without enforcement is just monitoring. With enforcement, you can't merge a PR if someone has been clicking around in the GCP console creating resources manually. The pipeline doesn't tell you what to do about the drift. It just blocks the merge until drift is zero.

### CLAUDE.md Rewrite

The project's Claude Code guidance file was still describing the repo as it existed during the initial security sprint. The architecture section described a flat directory structure when the repo had been reorganized into a monorepo with packages. The testing section mentioned `npm test` when the Solidity tests use `forge test`. The deployment section referenced manual gcloud commands when Terraform manages everything.

The rewrite reflects the current state: monorepo structure, shared packages (metrics, errors, config), deployment targets (Cloud Run for services, Sepolia for contracts), testing conventions (Foundry for Solidity, Vitest for TypeScript), and the phase-based development workflow with AAR requirements. A stale CLAUDE.md is worse than no CLAUDE.md because it actively misleads the AI assistant about the codebase.

## Perception: 92 HN Popular Blog Feeds

Five commits expanding Perception's feed coverage.

### Feed Selection

Ninety-two RSS feeds from blogs that regularly appear on the HN front page. The selection criteria:

- At least 3 front-page appearances in the last 6 months
- Active (posted within the last 30 days)
- The RSS feed actually works

That last criterion eliminated about 15 candidates — popular blogs with broken XML in their RSS feed, feeds that return HTML instead of XML, and feeds behind Cloudflare challenges that block automated readers.

This brings Perception's total feed count to 128. The original 36 feeds were curated technology and AI sources — the Verge, Ars Technica, Simon Willison, Julia Evans, that tier. The HN expansion adds developer blogs, startup founders, and independent researchers — the voices that don't show up in curated tech news aggregators.

### YAML Configuration

The feed list moved from a hardcoded JSON array to a YAML configuration file. Each feed entry includes the URL, category, expected update frequency, and a reliability score based on historical uptime.

The YAML format is easier to review in pull requests than JSON — you can add a comment explaining why a particular feed is included. The file supports feed groups (AI, Systems, Security, Career) so the dashboard can filter by category.

### Named Firestore Database

Perception moved from the default `(default)` Firestore database to a named database called `perception-prod`. Named databases in Firestore provide better isolation — different retention policies, security rules, and backup schedules per database.

The Perception database gets a 90-day retention policy (articles older than 90 days are archived to a GCS bucket for cold storage) and hourly backups. The default database is still used by other services in the project. Separating them means Perception's backup and retention schedules don't affect unrelated data.

## The Supporting Cast

**kilo** got one commit — a scrollbar fix. The horizontal scrollbar was appearing on pages where content didn't overflow. A CSS `overflow-x: hidden` on the wrong container was masking the root cause: a full-width element with margin that pushed past the viewport by 16px. The fix removed the margin instead of hiding the overflow.

**prompts** got one commit — doc filing v4.3. Updated the document organization conventions to handle the growing number of specification documents from the git-with-intent IDP work. Specs get their own category code (SPE) rather than being filed under technical documentation (TEC). The distinction matters when you have 20+ spec documents — they need their own namespace in the filing system.

Two projects, two milestones. IRSB v0.1.0 draws a line under the infrastructure phase. Perception's 128 feeds give it enough coverage to be genuinely useful as a daily reading tool rather than a proof of concept.

---

## Related Posts

- [Perception Agent System: Zero to MCP Dashboard in One Day](/posts/perception-agent-system-zero-to-mcp-dashboard/) — Perception's initial build with its first 36 feeds
- [IRSB Monorepo v1: Extracting Shared Packages from a Growing Solidity Codebase](/posts/irsb-monorepo-v1-extracting-shared-packages/) — The monorepo restructuring that made v0.1.0 possible
- [Perception Dashboard: Real Triggers and Topic Watchlists](/posts/perception-dashboard-real-triggers-topic-watchlists/) — Perception's dashboard features that consume these feeds
