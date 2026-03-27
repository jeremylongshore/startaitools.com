+++
title = 'Deep Dive Part 2: CLAUDE.md — The Missing Manual for Human-AI Software Collaboration'
date = 2026-03-26T14:00:00-05:00
draft = false
tags = ["wild-ecosystem", "claude-code", "ai-collaboration", "developer-tools", "best-practices"]
categories = ["Wild Ecosystem Deep Dive"]
description = "How per-repo CLAUDE.md files act as binding contracts between human architects and AI implementers. The pattern that coordinated 10 Ruby gems across the wild ecosystem."
toc = true
+++

When you work with an AI coding assistant over multiple sessions, something breaks down around the third task. The assistant remembers the current file, but forgets why you decided not to use that library. It recalls the mission statement, but reinvents the directory structure. It knows what you built in session one, but doesn't know what you explicitly decided NOT to build.

This is not a context window problem. It's a contract problem.

A README tells you what a codebase does. It doesn't tell an AI what it must not do, what assumptions are non-negotiable, what safety rules are load-bearing, or how the work sequence must unfold. A README is written for humans reading once. An AI assistant working across multiple sessions needs something different: a binding contract that governs every decision it makes.

That contract is CLAUDE.md.

This is Part 2 of the [Wild Ecosystem Deep Dive](/wild-ecosystem/) series.

---

## The CLAUDE.md Pattern

A CLAUDE.md file is a contract between you and the AI system. It specifies:

- **Identity** -- what this repo is, where it lives in the ecosystem, what it does
- **Mission** -- the problem it solves, the constraints that govern it
- **What It Does NOT Do** -- explicit non-goals that prevent scope creep
- **Safety Rules** -- non-negotiable constraints, especially for mutation-heavy code
- **Directory Layout** -- the canonical structure the AI must respect
- **Build Commands** -- how to test, lint, install dependencies
- **Canonical Docs** -- where to find the decisions that constrain this work
- **Task Tracking** -- how work is sequenced and closed

CLAUDE.md comes in two flavors: ecosystem-level and repo-level.

An **ecosystem-level CLAUDE.md** coordinates across multiple repositories. The wild ecosystem has one at `wild/CLAUDE.md`. It establishes that the ecosystem is not a monorepo. It defines build philosophy (safety-first, auditable, privacy-aware). It specifies that Beads is the required task tracker across all repos. It enforces the rule: "Do NOT start coding before planning docs exist."

A **repo-level CLAUDE.md** lives inside each repository. The introspection repo has one. The admin-tools repo has one. Each is specific to that repo's constraints.

Here's what a repo-level CLAUDE.md looks like, from `wild-rails-safe-introspection-mcp`:

```
## Identity

- **Repo:** `wild-rails-safe-introspection-mcp`
- **Ecosystem:** wild (see `../CLAUDE.md` for ecosystem-level rules)
- **Mission:** Safe, governed, read-only Rails production introspection
              for AI agents via MCP
- **Language:** Ruby
- **Status:** v1 complete -- all 10 epics finished

## What This Repo Does

Provides a curated set of MCP tools that let AI agents inspect live Rails
application state -- models, schema, records -- without granting raw console
access or permitting mutation.

## What This Repo Does NOT Do

- No write operations. Read-only by design.
- No arbitrary Ruby/Rails console execution.
- No admin actions (that's `wild-admin-tools-mcp`).
- No analytics queries or reporting pipelines.
- No multi-framework support in v1 (Rails/ActiveRecord only).
```

Notice what's happening here. The file doesn't just describe what the repo does. It explicitly lists what it doesn't do. This is not ceremony. This is architecture. It tells the AI: "If you're tempted to add a write operation, stop. That belongs elsewhere. Read-only by design. Full stop."

---

## Safety Rules That Actually Work

The introspection repo is read-only. The admin-tools repo executes mutations. Both have safety rules. The introspection repo has six:

1. **Never introduce write paths.** No `save`, `create`, `update`, `destroy`, or write SQL.
2. **Never bypass the query guard.** All data access goes through the guard. No direct adapter calls.
3. **Never skip audit logging.** Every invocation produces an audit record.
4. **Never expose blocked resources.** Denylist columns must be stripped before data leaves.
5. **Never accept arbitrary code as input.** Tool parameters are data, not code. No `eval`.
6. **Prefer restrictive defaults.** When uncertain, deny access.

These are not aspirational principles. They are enforced constraints. The test suite includes adversarial tests that explicitly try to break each rule. An audit logging test verifies that denials produce records. A denylist test confirms that blocked columns never appear in responses. A mutation test tries to call `update` and confirms the code rejects it.

The admin-tools repo has seven safety rules, because it executes mutations:

1. **Never bypass the capability gate.** Operations fail closed if the gate is unavailable.
2. **Never skip dry-run support.** Every action has preview and execute paths. Preview has no side effects.
3. **Never skip confirmation for destructive operations.** Two-phase confirmation with server-generated nonce.
4. **Never skip audit logging.** Every invocation produces before/after snapshots.
5. **Never accept arbitrary code as input.** Parameters are data.
6. **Never exceed blast radius caps.** Hard ceilings enforced in code.
7. **Prefer restrictive defaults.** Deny by default.

Notice the pattern: rules 3-7 are nearly identical to the introspection repo (audit, parameters, defaults). Rules 1-2 are mutation-specific (capability gate, dry-run). The pattern scales. As you add repos with different safety profiles, the rules adapt, but the discipline is consistent.

---

## The Ecosystem-Level CLAUDE.md

CLAUDE.md isn't just for individual repos. The ecosystem-level file coordinates across all ten repositories.

The wild ecosystem's CLAUDE.md establishes five core principles:

- **Safety first, always** -- every tool defaults to safe, non-destructive behavior
- **Auditability by default** -- actions are logged, decisions are traceable
- **Privacy-aware telemetry** -- collect what's needed, nothing more
- **Modular repos, not one giant codebase** -- each repo has clear boundaries
- **Documentation-led execution** -- planning artifacts exist before code

Then it specifies work sequence rules:

- Do NOT start coding before planning docs exist
- Do NOT create implementation tasks before the repo mission and boundaries are clear
- Work one repo at a time unless a cross-repo dependency explicitly requires coordination
- Prefer small, reviewable phases over large batch changes
- Avoid creating speculative infrastructure with no near-term use
- Avoid copy-paste divergence across repos

These aren't guidelines. They're enforced through Beads (the task tracker). If a repo hasn't filed its mission and boundaries document, the AI can't create Beads. If Beads haven't been created, implementation can't begin. The sequence is locked in.

---

## Negative Space as Architecture

One of the most powerful aspects of CLAUDE.md is what it explicitly excludes. The "What This Repo Does NOT Do" section is load-bearing architecture.

The introspection repo says: "No write operations. No admin actions. No analytics pipelines." This isn't just helpful context. It's a boundary. It tells the AI: "If you're tempted to add caching, you're in the wrong repo. If you're thinking about administrative tooling, that belongs in `wild-admin-tools-mcp`. Do not merge these repos."

The ecosystem-level CLAUDE.md reinforces this. It specifies that introspection is read-only by design, and admin-tools is for writes, and they have separate safety models for a reason. They are not features of the same system. They are separate repos with separate concerns, separate safety rules, and separate operational lifecycles.

This prevents a common failure mode in ecosystem-scale projects: feature silos. Without explicit boundaries, the introspection repo accumulates write operations. The admin-tools repo duplicates read logic. The capability-gate repo becomes a catch-all for access control concerns that should be distributed. The boundary erosion is subtle and pervasive.

CLAUDE.md prevents this by making the boundaries explicit and front-loaded. The AI sees "What This Repo Does NOT Do" on the first page of the contract. It becomes a filter for every architectural decision.

---

## The 10-Epic Pattern

Every repo in the wild ecosystem follows the same structure: 10 epics, minimum.

This is not arbitrary. The 10-epic pattern is a predictable framework that helps the AI understand its location in the work. An epic is not a sprint. It's a major outcome area covering the full scope of the repo.

The master blueprint specifies the pattern for the wild ecosystem:

- **Wave 1** -- Foundation (3 repos): capability-gate, introspection, admin-tools
- **Wave 2** -- Observability pipeline (3 repos): telemetry, transcript pipeline, gap miner
- **Wave 3** -- SDLC companions (3 repos): hook ops, permission analyzer, test flake forensics
- **Wave 4** -- Coordination (1 repo): skills registry

Each repo is independently broken into 10 epics. The introspection repo's epics cover: authorization, query guards, audit logging, policy, threat modeling, architecture decisions, safety evaluation, deployment, operations, and confirmed out-of-scope items.

Why this structure? Because it's predictable. After an AI reads the master blueprint and understands Wave 1, it knows: "We're building three foundation repos first. Each one has 10 epics. We'll finish one epic, then move to the next. When all three repos are complete, we move to Wave 2." The structure creates narrative coherence. The AI doesn't wander. It knows where it is and what comes next.

---

## Beads: Task Tracking for AI Agents

Beads is a task tracker designed for post-compaction recovery. It's the required task tracking system for the wild ecosystem.

Traditional ticketing systems are inadequate for AI collaboration. Jira tickets are written for human teams to estimate and track progress. They're not designed for AI sessions that might be interrupted, resumed hours later, and resumed again by a different session. They don't enforce sequence. They don't capture evidence. They don't require annotations.

Beads does.

Every repo's work is broken into:
- 10 epics covering full scope
- Child tasks under each epic with clear acceptance criteria
- Explicit dependency blocks between tasks and across repos
- Annotations that explain context and blocking assumptions

A task closure requires evidence: "Done" means the work exists, it is verifiable, and the close reason states what was produced. A weak annotation says `In progress`. A strong annotation says: `Started schema definition. Blocking question: are capability IDs scoped per-repo or globally? Needs a decision before authorization logic can be written.`

The Beads workflow is simple:

```bash
bd ready                # Find unblocked work
bd update <id> --status in_progress  # Claim a task
bd close <id> --reason "evidence"    # Close with evidence
bd sync                 # Persist to disk
```

No task starts without a marked Beads task. No task closes without evidence. This enforces sequence. An AI cannot skip planning and jump to code because implementation tasks are blocked until planning tasks are closed.

---

## Adopting This Today

If you're working with Claude Code on a project, you can adopt CLAUDE.md today. Here's the practical template.

Create a `CLAUDE.md` file at the root of your repository:

```markdown
# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Identity

- **Repo:** `your-repo-name`
- **Mission:** One clear sentence. What this repo does and why.
- **Language:** Your primary language
- **Status:** v1 scaffolding / v1 complete / v2 in progress

## What This Repo Does

One paragraph describing the repo's scope and primary responsibility.

## What This Repo Does NOT Do

- Explicit list of things this repo will not do
- This prevents scope creep and feature confusion
- Makes boundaries clear to both humans and AI

## Build Commands

bundle install    # Install dependencies
bundle exec rspec # Run tests

## Key Docs

| Doc | Purpose |
|-----|---------|
| `docs/mission.md` | Mission and boundaries |

## Before Working Here

1. Read this file completely
2. Check current work state
3. Read the relevant doc for the active task
4. Do not skip ahead to later phases
```

That's it. A CLAUDE.md file can be minimal and grow over time. Early versions might not have safety rules or ecosystem-level coordination. That's fine. Add what you need as the project matures.

The pattern evolves with the project. A v1 CLAUDE.md is lean: mission, non-goals, build commands. A v2 adds safety rules, testing strategies, expanded canonical docs. An ecosystem-level CLAUDE.md adds wave sequencing, dependency thinking, and cross-repo standards.

The key is to start. Write the identity block. Write the non-goals. Write the build commands. Make it a contract. The AI will follow it.

---

## What Comes Next

- **Part 1**: [The Safety Architecture](/posts/wild-deep-dive-1-safety-architecture/) -- Defense in depth, adversarial testing, hard safety ceilings
- **Part 3**: [The Observability Loop](/posts/wild-deep-dive-3-observability/) -- How telemetry, transcripts, and gap mining create a self-improving feedback loop
- **Part 4**: [Claude Code as Tech Lead](/posts/wild-deep-dive-4-tech-lead/) -- What happens when the AI makes the architectural decisions

Build your CLAUDE.md first. Before the code. Before the architecture. It will focus your decisions, constrain the AI appropriately, and keep your project coherent across sessions.

---

*Part of the [Wild Ecosystem](/wild-ecosystem/) -- 10 Ruby gems for governed AI agent operations in production Rails. Built with [Claude Code](https://claude.ai/code).*
