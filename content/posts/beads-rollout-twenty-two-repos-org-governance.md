+++
title = 'Beads Rollout: 22 Repos, One Governance Pattern'
slug = 'beads-rollout-twenty-two-repos-org-governance'
date = 2025-12-19T10:00:00-06:00
draft = false
tags = ["beads", "task-tracking", "git-with-intent", "devops", "governance", "jeremylongshore"]
categories = ["Development Journey"]
description = "76 commits across 22 repos deploying the beads task tracking system to every active project, plus git-with-intent security work and jeremylongshore.com Linkyee migration."
+++

Seventy-six commits. Twenty-two repos. One day. And most of it was the same two commits repeated eleven times.

December 19th was a governance rollout day. The beads task tracking system had been running in three repos for a week. It was time to deploy it everywhere.

## The Beads Pattern

Beads (`bd`) is the post-compaction recovery system for AI-assisted development. When Claude Code compacts a long conversation, it loses context about what you were working on. Beads persists task state in git so you can recover after compaction.

Each repo gets the same setup:

1. A `.beads/` directory with configuration
2. A `beads.json` tracking file for active tasks
3. Integration hooks that sync task state on commit

Two commits per repo. First commit adds the directory and config. Second commit adds the tracking file and hooks. Clean, repeatable, tested.

## The Rollout

Twenty-two repos got beads on December 19th. Here's the full list grouped by project area:

**Core products** (4 repos): git-with-intent, intentvision, project-template, blog

**Client projects** (3 repos): hustlestats, braves, cad-dxf-agent

**Plugins ecosystem** (4 repos): claude-code-plugins, nixtla, perception-agent, pipelinepilot

**Infrastructure** (3 repos): prompts-intent-solutions, bob-brain, automaton

**Research and tools** (4 repos): NWSL content pipeline, IRSB ecosystem, wild ecosystem, landing pages

**Personal** (4 repos): jeremylongshore.com, startaitools.com, resume, dotfiles

Forty-four commits just from the beads rollout (2 per repo). The remaining 32 commits were actual work.

## Why All at Once

The alternative was a gradual rollout — add beads to repos as I work on them. That approach has a problem: when you context-switch between repos (which happens constantly in a multi-project portfolio), you can't rely on beads being available in the target repo. Sometimes you have it, sometimes you don't. That inconsistency defeats the purpose.

The whole-portfolio rollout means that from December 19th forward, every repo supports the same workflow:

```
bd ready           # see available tasks
bd update <id> --status in_progress  # claim work
# ... do work ...
bd close <id> --reason "evidence"    # close with evidence
bd sync            # push state
```

No exceptions. No "this repo doesn't have beads yet." One workflow, everywhere.

## The Non-Beads Work

Thirty-two commits across the portfolio that weren't beads setup.

### git-with-intent: Security and Idempotency

The git-with-intent commits on December 19th focused on hardening:

**Idempotent operations.** The connector framework's retry logic could trigger duplicate side effects. If a connector call succeeded but the response was lost (network timeout after the server processed the request), the retry would re-execute the operation. For read operations this is harmless. For write operations (creating webhooks, updating configurations) it creates duplicates.

The fix was idempotency keys. Each operation gets a UUID generated client-side. The server tracks which keys have been processed and returns the cached response for duplicate keys. Redis stores the keys with a 24-hour TTL — long enough to cover any reasonable retry window.

**Input validation tightening.** The API endpoints accepted request bodies without validating field lengths, character sets, or nesting depth. A malicious request with a 50MB JSON body or 1000 levels of nesting could crash the service. Added Zod schemas with explicit limits: string fields max 10KB, nesting max 10 levels, array fields max 1000 items.

**Rate limiting per endpoint.** The existing rate limiting was global per tenant. A tenant hitting the health check endpoint 1000 times would exhaust their quota, preventing them from making actual analysis requests. Split rate limits into tiers: health/status endpoints get a generous limit, analysis endpoints get a strict limit, admin endpoints get the strictest limit.

### jeremylongshore.com: Linkyee Migration

The personal site migrated from a standard about page to a Linkyee-style link hub. Linkyee is the link-in-bio format — a single page with a profile photo, bio, and a vertical stack of links to your various presences.

The migration involved:

- Redesigning the about page layout from long-form bio to link cards
- Adding social profile links (GitHub, LinkedIn, X, blog)
- Adding project links (each active project gets a card)
- Mobile-first responsive design since link-in-bio pages are predominantly accessed on phones

This is a straightforward layout change. The interesting part is that it replaced approximately 800 words of bio text with 12 links. The links convey more information faster. Nobody reads an 800-word bio on a personal developer site. They scan for links to code and social profiles.

## The Governance Argument

Twenty-two repos with consistent task tracking isn't just convenience. It's organizational governance for a solo developer.

When you maintain 22+ active repos, the hardest problem isn't writing code. It's knowing what you were doing in each repo. Tuesday morning you're fixing a Docker build in git-with-intent. Tuesday afternoon you're debugging a Prisma migration in hustlestats. Wednesday you're writing tests for the CAD agent. By Thursday, you've lost context on all three.

Beads solves this by making task state a first-class artifact. Every repo tells you what's in progress, what's blocked, and what's done. The overhead is two commands per task (claim and close). The payoff is never starting a session with "what was I working on?"

Seventy-six commits for one day sounds like a lot. Forty-four of them were mechanical. The remaining thirty-two were real work. The mechanical commits enable the real work to be tracked, recovered, and resumed. That's the trade.

---

## Related Posts

- [Building Post-Compaction Recovery for AI Agent Workflows with Beads](/posts/building-post-compaction-recovery-beads/) — The deep dive into how beads works
- [Production Push: 70 Phases, Cloud Deploy, and the Docker Build Gauntlet](/posts/gwi-production-push-seventy-phases-cloud-deploy/) — The git-with-intent security work this day extended
- [February 2026 State of Affairs: 255 Commits Across 12 Projects](/posts/february-2026-state-of-affairs-255-commits-12-projects/) — Where the multi-repo portfolio ended up two months later
