+++
title = 'Drop Monorepo Restructure, /ship-shelly Reporting Skill, and Diagram Automation'
slug = 'drop-monorepo-restructure-ship-shelly-skill'
date = 2026-01-09T10:00:00-06:00
draft = false
tags = ["architecture", "devops", "claude-code", "automation"]
categories = ["Development Journey"]
description = "Eight commits across two repos. The Drop monorepo moves to a packages/ layout, a reporting skill gets its first real workflow, and the changelog gets an overhaul."
+++

Monorepos have a half-life. They start simple, grow organically, and eventually reach a point where the directory structure actively fights the development workflow. January 9th was the day the Drop monorepo hit that threshold.

Eight commits across two repos. The big one was the Drop restructure — moving from a flat `src/` layout to a proper `packages/` workspace. The smaller one was file cleanup on the Nixtla repo.

## Packages Layout Migration

The Drop repo had been a flat structure — all source code in `src/`, all tests in `tests/`, shared utilities mixed in with domain logic. It worked when the repo had three modules. It stopped working at seven.

The restructure moved to a `packages/` layout:

```
packages/
  core/        # Shared types, utilities, config
  reporting/   # Ship-Shelly and output generation
  diagrams/    # Mermaid and architecture diagram automation
  cli/         # Command-line interface
```

Each package gets its own `package.json`, its own test suite, and its own dependency list. The root `package.json` uses workspaces to link them. Imports between packages use the package name, not relative paths:

```typescript
// Before: fragile relative paths
import { formatReport } from '../../utils/formatting';

// After: package imports
import { formatReport } from '@drop/core';
```

The migration itself was mechanical — move files, update imports, verify tests pass. The tedious part was untangling circular dependencies. The reporting module imported from core, but core also imported a type definition from reporting. Breaking that cycle meant extracting the shared types into their own file in `core/types.ts` and having both packages import from there.

The value is in what comes after. Adding a new package no longer requires understanding the entire codebase. Each package has a clear boundary and a clear owner. When CI runs, each package's tests run independently — a failure in `diagrams/` doesn't block a deploy of `cli/`.

## /ship-shelly Reporting Skill

The `/ship-shelly` skill is a reporting workflow for generating project status summaries. It reads git history, beads status, and PR metadata, then produces a formatted report suitable for stakeholder updates.

Before this commit, the skill existed as a stub. Today it got its first real implementation: read the last N days of git activity, group by repository, summarize commit themes, and output a markdown report with commit counts, PR links, and a narrative summary.

The skill also generates architecture diagrams automatically. When it detects structural changes (new packages, new services, modified config files), it produces a Mermaid diagram showing the current module layout. The diagram goes into the report alongside the text summary.

This is the kind of automation that pays for itself after two uses. Writing a weekly status report by hand takes thirty minutes of context-switching between repos, PR pages, and commit logs. The skill does it in seconds.

The diagram generation is the part I'm most interested in long-term. Architecture diagrams rot faster than any other documentation. The code changes, the diagram doesn't, and within a month the diagram is a historical artifact that actively misleads anyone who reads it. Auto-generating diagrams from the actual package structure means the diagram is always current because it's derived from the source of truth.

## Changelog Overhaul

The Drop changelog had fallen behind by about three weeks. Entries were inconsistent — some had PR links, some didn't. Some followed Keep a Changelog format, others were freeform paragraphs.

Cleaned it up. Every entry now follows the same structure: version header, date, categorized changes (Added, Changed, Fixed, Removed), PR links where applicable. Backdated the missing entries from git history.

A changelog that's three weeks stale is worse than no changelog. It implies currency while delivering outdated information. Better to either keep it current or delete it.

Going forward, the `/ship-shelly` reporting skill can generate changelog entries as part of its output. That's the real payoff of the automation — not just status reports, but structured artifacts like changelog entries that would otherwise be written by hand and inevitably fall behind.

## Nixtla Sensitive File Cleanup

Quick hit on the Nixtla repo. A `.env.example` file had been committed with actual API key prefixes (not full keys, but enough to identify the provider and account tier). Scrubbed the values and replaced them with generic placeholders.

Also removed two files that shouldn't have been tracked: a local SQLite database from development and a temporary export file from a data migration script. Both added to `.gitignore`.

This is a recurring pattern across repos. Development artifacts sneak into version control because `.gitignore` is written at project init and never updated. The SQLite file was 12MB — every clone of the repo downloaded 12MB of someone's local dev data. Gone now.

---

Eight commits, two repos. The Drop monorepo has a structure that scales, the reporting skill does real work, and two repos are cleaner than they were yesterday.

### Related Posts

- [IRSB Monorepo v1: Extracting Shared Packages](/posts/irsb-monorepo-v1-extracting-shared-packages/)
- [GitHub Release Workflow: Uncommitted Changes and Semantic Versioning](/posts/github-release-workflow-uncommitted-changes-semantic-versioning/)
