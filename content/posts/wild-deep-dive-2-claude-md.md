+++
title = 'Deep Dive Part 2: CLAUDE.md — The Missing Manual for Human–AI Software Collaboration'
slug = 'wild-deep-dive-2-claude-md'
date = 2026-03-26T14:00:00-05:00
draft = false
tags = ["wild-ecosystem", "claude-code", "ai-collaboration", "developer-tools", "best-practices"]
categories = ["Wild Ecosystem Deep Dive"]
description = "How per-repo CLAUDE.md files act as binding contracts between human architects and AI implementers. Read against the literature on long-context attention degradation, sycophancy, and module boundary information distribution."
toc = true
bibliography = "citations/wild-citations.bib"
+++

When an engineer works with a language-model coding assistant across multiple sessions, something breaks down around the third task. The assistant remembers the current file but forgets why a particular library was ruled out. It recalls the mission statement but reinvents the directory structure. It knows what was built in session one but has no model of what was explicitly decided *not* to build.

This is sometimes diagnosed as a context-window problem. It is closer to a *contract* problem. Liu and colleagues' work on long-context language models showed that information placed in the middle of a large prompt is retrieved much less reliably than information placed at the start or end[^liu2024lostmiddle]; subsequent work on sycophancy[^sharma2023sycophancy] documents a second failure mode in which the assistant aligns with whatever the operator says most recently rather than with what was established earlier in the session. Both effects compound. The assistant is not lying; it is *attending differently* over the session length.

A README tells a reader what a codebase does. It does not tell a language-model implementer what it must *not* do, which assumptions are non-negotiable, which safety rules are load-bearing, or how the work sequence must unfold. A README is written for humans reading once. An AI assistant working across multiple sessions needs a different artefact: a binding contract that governs every decision it makes, placed in a position where the attention budget will reliably reach it.

That artefact is `CLAUDE.md`.

This is Part 2 of the [Wild Ecosystem Deep Dive](/wild-ecosystem/) series.

---

## The CLAUDE.md Pattern

A `CLAUDE.md` file is a contract between operator and AI system. It specifies:

- **Identity** — what this repo is, where it lives in the ecosystem, what it does
- **Mission** — the problem it solves, the constraints that govern it
- **What It Does NOT Do** — explicit non-goals that prevent scope creep
- **Safety Rules** — non-negotiable constraints, especially for mutation-heavy code
- **Directory Layout** — the canonical structure the AI must respect
- **Build Commands** — how to test, lint, install dependencies
- **Canonical Docs** — where to find the decisions that constrain this work
- **Task Tracking** — how work is sequenced and closed

`CLAUDE.md` comes in two flavours: ecosystem-level and repo-level.

An **ecosystem-level `CLAUDE.md`** coordinates across multiple repositories. The wild ecosystem has one at `wild/CLAUDE.md`. It establishes that the ecosystem is not a monorepo. It defines build philosophy (safety-first, auditable, privacy-aware). It specifies that Beads is the required task tracker across all repos. It enforces the rule: *do not start coding before planning docs exist*.

A **repo-level `CLAUDE.md`** lives inside each repository. The introspection repo has one. The admin-tools repo has one. Each is specific to that repo's constraints.

Here is what a repo-level `CLAUDE.md` looks like, from `wild-rails-safe-introspection-mcp`:

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

The file does not just describe what the repo does. It explicitly lists what it does *not* do. This is not ceremony. It is architecture. It tells the assistant: *if you are tempted to add a write operation, stop. That belongs elsewhere.* Parnas argued in 1971 that the boundaries between modules ought to encode the design decisions most likely to change, and that information about non-membership in a module is as load-bearing as information about membership[^parnas1971information]. The negative-space section of a `CLAUDE.md` is the modern instance of that argument.

---

## Safety Rules That Actually Work

The introspection repo is read-only. The admin-tools repo executes mutations. Both have safety rules. The introspection repo has six:

1. **Never introduce write paths.** No `save`, `create`, `update`, `destroy`, or write SQL.
2. **Never bypass the query guard.** All data access goes through the guard. No direct adapter calls.
3. **Never skip audit logging.** Every invocation produces an audit record.
4. **Never expose blocked resources.** Denylist columns must be stripped before data leaves.
5. **Never accept arbitrary code as input.** Tool parameters are data, not code. No `eval`.
6. **Prefer restrictive defaults.** When uncertain, deny access — the *fail-safe defaults* principle Saltzer and Schroeder identified in 1975[^saltzer1975protection].

These are not aspirational principles. They are enforced constraints. The test suite includes adversarial tests that explicitly try to break each rule — an audit-logging test verifies that denials produce records, a denylist test confirms that blocked columns never appear in responses, a mutation test tries to call `update` and verifies that the code rejects it. The construction mirrors the *constitutional* training regime Bai and colleagues described for harmlessness in language-model assistants[^bai2022constitutional]: the rule is declared, the system is then evaluated against deliberate violations of it, and the evaluation result is part of the artefact's standing.

The admin-tools repo has seven safety rules, because it executes mutations:

1. **Never bypass the capability gate.** Operations fail closed if the gate is unavailable.
2. **Never skip dry-run support.** Every action has preview and execute paths. Preview has no side effects.
3. **Never skip confirmation for destructive operations.** Two-phase confirmation with server-generated nonce.
4. **Never skip audit logging.** Every invocation produces before/after snapshots.
5. **Never accept arbitrary code as input.** Parameters are data.
6. **Never exceed blast-radius caps.** Hard ceilings enforced in code.
7. **Prefer restrictive defaults.** Deny by default.

Notice the pattern. Rules 3–7 are nearly identical to the introspection repo (audit, parameters, defaults). Rules 1–2 are mutation-specific (capability gate, dry-run). The pattern scales. As repos with different safety profiles are added, the rules adapt; the discipline is consistent.

The structure also operates as a counter-force to the sycophancy failure mode Sharma and colleagues documented[^sharma2023sycophancy]. When a written rule says "never bypass the capability gate," and an operator mid-session asks the assistant to "just skip the gate this once for debugging," the contract is the anchor that lets the assistant decline without negotiating away the safety property.

---

## The Ecosystem-Level CLAUDE.md

`CLAUDE.md` is not only a per-repo file. The ecosystem-level file coordinates across all ten repositories.

The wild ecosystem's `CLAUDE.md` establishes five core principles:

- **Safety first, always** — every tool defaults to safe, non-destructive behaviour
- **Auditability by default** — actions are logged, decisions are traceable
- **Privacy-aware telemetry** — collect what is needed, nothing more
- **Modular repos, not one giant codebase** — each repo has clear boundaries
- **Documentation-led execution** — planning artefacts exist before code

It then specifies work-sequence rules:

- Do not start coding before planning docs exist
- Do not create implementation tasks before the repo mission and boundaries are clear
- Work one repo at a time unless a cross-repo dependency explicitly requires coordination
- Prefer small, reviewable phases over large batch changes
- Avoid speculative infrastructure with no near-term use
- Avoid copy-paste divergence across repos

These are not guidelines. They are enforced through Beads (the task tracker). If a repo has not filed its mission-and-boundaries document, the AI cannot create Beads. If Beads have not been created, implementation cannot begin. The sequence is locked in.

---

## Negative Space as Architecture

One of the most powerful aspects of `CLAUDE.md` is what it explicitly excludes. The "What This Repo Does NOT Do" section is load-bearing architecture.

The introspection repo says: "No write operations. No admin actions. No analytics pipelines." This is not helpful context. It is a boundary. It tells the assistant: *if you are tempted to add caching, you are in the wrong repo. If you are thinking about administrative tooling, that belongs in `wild-admin-tools-mcp`. Do not merge these repos.*

The ecosystem-level `CLAUDE.md` reinforces this. It specifies that introspection is read-only by design, that admin-tools is for writes, and that they have separate safety models for a reason. They are not features of the same system. They are separate repos with separate concerns, separate safety rules, and separate operational lifecycles.

This prevents a common failure mode in ecosystem-scale projects: feature silo erosion. Without explicit boundaries, the introspection repo gradually accumulates write operations. The admin-tools repo duplicates read logic. The capability-gate repo becomes a catch-all. The erosion is subtle and pervasive — and it is exactly the failure mode Parnas warned against in his 1971 paper on information distribution, where he argued that module boundaries must hide the design decisions most likely to change[^parnas1971information].

`CLAUDE.md` prevents this by making the boundaries explicit and front-loaded. The assistant sees "What This Repo Does NOT Do" on the first page of the contract. It becomes a filter for every architectural decision — and, by virtue of being at the *start* of the prompt rather than the middle, it is exactly where the long-context attention curve is most reliable[^liu2024lostmiddle].

---

## The 10-Epic Pattern

Every repo in the wild ecosystem follows the same structure: ten epics, minimum.

This is not arbitrary. The ten-epic pattern is a predictable framework that helps the assistant understand its location in the work. An epic is not a sprint. It is a major outcome area covering the full scope of the repo.

The master blueprint specifies the pattern for the wild ecosystem:

- **Wave 1** — Foundation (3 repos): capability-gate, introspection, admin-tools
- **Wave 2** — Observability pipeline (3 repos): telemetry, transcript pipeline, gap miner
- **Wave 3** — SDLC companions (3 repos): hook ops, permission analyzer, test flake forensics
- **Wave 4** — Coordination (1 repo): skills registry

Each repo is independently broken into ten epics. The introspection repo's epics cover authorisation, query guards, audit logging, policy, threat modelling, architecture decisions, safety evaluation, deployment, operations, and confirmed out-of-scope items.

Why this structure? Because it is predictable. After an assistant reads the master blueprint and understands Wave 1, it knows: *we are building three foundation repos first. Each one has ten epics. We finish one epic, then move to the next. When all three repos are complete, we move to Wave 2.* The structure creates narrative coherence. The assistant does not wander. It knows where it is and what comes next.

---

## Beads: Task Tracking for AI Agents

Beads is a task tracker designed for post-compaction recovery. It is the required task-tracking system for the wild ecosystem.

Traditional ticketing systems are inadequate for AI collaboration. Jira tickets are written for human teams to estimate and track progress. They are not designed for AI sessions that might be interrupted, resumed hours later, and resumed again by a different session. They do not enforce sequence. They do not capture evidence. They do not require annotations.

Beads does.

Every repo's work is broken into:

- ten epics covering full scope
- child tasks under each epic with clear acceptance criteria
- explicit dependency blocks between tasks and across repos
- annotations that explain context and blocking assumptions

A task closure requires evidence: *done* means the work exists, it is verifiable, and the close reason states what was produced. A weak annotation says `In progress`. A strong annotation says: `Started schema definition. Blocking question: are capability IDs scoped per-repo or globally? Needs a decision before authorisation logic can be written.`

The Beads workflow is simple:

```bash
bd ready                # Find unblocked work
bd update <id> --status in_progress  # Claim a task
bd close <id> --reason "evidence"    # Close with evidence
bd sync                 # Persist to disk
```

No task starts without a marked Beads entry. No task closes without evidence. This enforces sequence. An assistant cannot skip planning and jump to code because implementation tasks are blocked until planning tasks are closed. The pattern is, structurally, a *protocol* in the session-typed sense[^honda1998session]: the legal transitions between states are encoded in the tooling, not in the assistant's discretion.

---

## Adopting This Today

If a team is working with Claude Code on a project, `CLAUDE.md` can be adopted today. The practical template is short. Create a `CLAUDE.md` file at the root of the repository:

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

That is enough. A `CLAUDE.md` can be minimal and grow over time. Early versions might not have safety rules or ecosystem-level coordination. That is fine. Add what is needed as the project matures.

The pattern evolves with the project. A v1 `CLAUDE.md` is lean: mission, non-goals, build commands. A v2 adds safety rules, testing strategies, expanded canonical docs. An ecosystem-level `CLAUDE.md` adds wave sequencing, dependency thinking, and cross-repo standards.

The key is to start. Write the identity block. Write the non-goals. Write the build commands. Make it a contract. The assistant will follow it.

---

## What Comes Next

- **Part 1**: [The Safety Architecture](/posts/wild-deep-dive-1-safety-architecture/) — defence in depth, adversarial testing, hard safety ceilings.
- **Part 3**: [The Observability Loop](/posts/wild-deep-dive-3-observability/) — how telemetry, transcripts, and gap mining create a self-improving feedback loop.
- **Part 4**: [Claude Code as Tech Lead](/posts/wild-deep-dive-4-tech-lead/) — what happens when the AI makes the architectural decisions.

Build the `CLAUDE.md` first. Before the code. Before the architecture. It focuses the decisions, constrains the AI appropriately, and keeps the project coherent across sessions.

---

*Part of the [Wild Ecosystem](/wild-ecosystem/) — 10 Ruby gems for governed AI agent operations in production Rails. Built with [Claude Code](https://claude.ai/code).*

---

## References

[^bai2022constitutional]: Bai, Y., Kadavath, S., Kundu, S., Askell, A., Kernion, J., et al. (2022). *Constitutional AI: Harmlessness from AI Feedback.* arXiv:2212.08073.
[^honda1998session]: Honda, K., Vasconcelos, V. T., & Kubo, M. (1998). Language Primitives and Type Discipline for Structured Communication-Based Programming. *European Symposium on Programming (ESOP).* <https://doi.org/10.1007/BFb0053567>
[^liu2024lostmiddle]: Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2023). Lost in the Middle: How Language Models Use Long Contexts. *Transactions of the Association for Computational Linguistics*, 12, 157–173. <https://doi.org/10.1162/tacl_a_00638>
[^parnas1971information]: Parnas, D. L. (1971). Information Distribution Aspects of Design Methodology. *Proceedings of the IFIP Congress.* <https://doi.org/10.1184/R1/6606470.V1>
[^saltzer1975protection]: Saltzer, J. H., & Schroeder, M. D. (1975). The Protection of Information in Computer Systems. *Proceedings of the IEEE*, 63(9), 1278–1308. <https://doi.org/10.1109/PROC.1975.9939>
[^sharma2023sycophancy]: Sharma, M., Tong, M., Korbak, T., Duvenaud, D., Askell, A., Bowman, S. R., et al. (2024). Towards Understanding Sycophancy in Language Models. *ICLR.* arXiv:2310.13548.
