+++
title = 'Proposal Template Launch and IRSB CLAUDE.md Cleanup'
slug = 'proposal-template-launch-irsb-cleanup'
date = 2026-01-16T10:00:00-06:00
draft = false
tags = ["proposal-template", "irsb", "documentation", "commercial-safety", "claude-md"]
categories = ["Development Journey"]
description = "Releasing the proposal-template with commercial safety standards and cleaning up the IRSB monorepo's CLAUDE.md for accurate project guidance."
+++

Three commits across two repos. A light day by commit count, but both changes address real gaps that were causing friction in daily operations.

## Proposal Template: Initial Release

The proposal-template repo shipped its first version. The template standardizes how Intent Solutions writes client proposals -- consistent structure, consistent safety language, consistent pricing presentation. Before this, each proposal was a one-off Google Doc with whatever structure felt right at the time. Some had safety sections, some didn't. Some quoted hourly, some quoted fixed-price. The inconsistency was starting to show.

### Why Commercial Safety Standards Matter

Every proposal includes a safety and liability section. Not because clients ask for it (they usually don't), but because AI agent work carries real operational risk. An agent that modifies production data, sends emails on behalf of a client, or interacts with financial APIs needs clear boundaries documented before work begins.

The template includes:

- **Scope boundaries** -- explicit list of what the agent will and will not do
- **Rollback procedures** -- how to undo agent actions if something goes wrong
- **Monitoring commitments** -- what telemetry the agent produces and who watches it
- **Liability caps** -- standard language limiting exposure to the contract value
- **Incident response** -- SLA for responding to agent misbehavior reports

These sections are pre-filled with Intent Solutions' defaults. Each proposal customizes them based on the specific engagement, but the baseline ensures nothing gets forgotten.

### Template Structure

The template uses markdown with TOML frontmatter for metadata (client name, project code, estimated value, timeline). Sections follow the standard consulting proposal flow:

1. Executive Summary
2. Problem Statement
3. Proposed Solution
4. Technical Approach
5. Safety and Liability
6. Timeline and Milestones
7. Pricing
8. Terms and Conditions

A render script converts the markdown to a styled PDF using Pandoc with a custom LaTeX template. The output looks professional without requiring Word or Google Docs.

The template also includes a version field in the frontmatter. When a proposal gets revised during negotiation, the version increments and the render script stamps the version number and date on the PDF header. This prevents the "which version did we agree to?" problem that plagues email-based proposal workflows.

## IRSB CLAUDE.md Cleanup

The IRSB monorepo's CLAUDE.md had drifted from reality. It still referenced the old multi-repo structure, listed commands that didn't work after the monorepo migration, and described contract interfaces that had changed during the DisputeModule work.

The cleanup:

- Updated the project overview to reflect the monorepo structure
- Fixed all build and test commands to use the current workspace setup
- Removed references to deprecated contract interfaces
- Added the new DisputeModule and ComplianceOracle to the architecture section
- Updated the dependency list (Node 22, Hardhat 2.x, Foundry)

Not glamorous work, but a stale CLAUDE.md is worse than no CLAUDE.md. It actively misleads anyone (human or AI) trying to understand the project.

The biggest catch: the old CLAUDE.md listed `npm run test:all` as the test command. The monorepo migration changed it to `npx turbo run test`. Anyone following the old instructions would get a "script not found" error and waste time figuring out why. Six of the twelve corrections were similarly broken commands -- the kind of thing that costs someone 15 minutes each time and compounds across contributors.

The architecture section also needed a diagram update. The old diagram showed three separate repos with arrows between them. The new diagram shows the monorepo workspace structure with `packages/`, `apps/`, and `contracts/` directories. The diagram lives in the CLAUDE.md as ASCII art since Mermaid isn't supported in all contexts where CLAUDE.md gets read.

## The Day in Numbers

| Metric | Value |
|--------|-------|
| Commits | 3 |
| Repos | 2 (proposal-template, irsb) |
| New template sections | 8 |
| CLAUDE.md corrections | 12 |
| Broken commands fixed | 6 |

## Related Posts

- [IRSB Protocol MVP, Vertex AI Embeddings, and GWI Violation Pipeline](/posts/irsb-protocol-mvp-vertex-embeddings-gwi-violations/) -- the DisputeModule work that made this CLAUDE.md update necessary
- [IRSB Monorepo v1.0.0: Extracting Shared Packages](/posts/irsb-monorepo-v1-extracting-shared-packages/) -- the later monorepo restructuring
- [Building an AI-Friendly Codebase: Real-Time CLAUDE.md Creation](/posts/building-ai-friendly-codebase-documentation-real-time-claude-md-creation-journey/) -- the philosophy behind keeping CLAUDE.md files accurate
