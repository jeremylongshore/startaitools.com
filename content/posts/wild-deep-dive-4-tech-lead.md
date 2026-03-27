+++
title = 'Deep Dive Part 4: Building 10 Production Gems with Claude Code as Tech Lead'
date = 2026-03-26T16:00:00-05:00
draft = false
tags = ["wild-ecosystem", "ruby", "claude-code", "ai-collaboration", "software-architecture", "ai-agents"]
categories = ["Wild Ecosystem Deep Dive"]
description = "What it means when the AI makes the architectural decisions. How Claude Code served as tech lead across 10 Ruby gems with 2,924 tests and 60+ canonical docs."
toc = true
+++

Jeremy Longshore set out to build a family of production-grade Ruby gems that would form a governed operational intelligence layer for AI agents. That ecosystem is now complete: 10 repositories, 2,924 tests, zero RuboCop offenses, 60+ canonical documents, all v1 implementations shipped.

This article is about how that was built, and what a collaboration between a human architect and AI as tech lead actually looks like.

This is Part 4 of the [Wild Ecosystem Deep Dive](/wild-ecosystem/) series.

---

## The Collaboration Model

The wild ecosystem was not built with Claude Code as a copilot -- autocompleting code fragments, implementing features described in natural language, staying within pre-set guardrails.

Instead, Claude Code served as tech lead: making architecture decisions, choosing implementation patterns, catching its own bugs, testing its own code adversarially, and maintaining cross-repository consistency.

**Jeremy Longshore** operated as product owner and architect. He defined:

- The mission of each repository
- The boundaries (what each repo does and does not do)
- The 10-epic structure for each repo
- The key architectural decisions that needed to be made
- The non-negotiable safety rules for each context

**Claude Code** operated as implementer and technical decision-maker within those constraints. It:

- Made sound implementation choices (e.g., should this authorization check be a constant or a hash?)
- Wrote adversarial tests against its own code
- Identified and fixed bugs
- Maintained patterns across repositories to prevent divergence
- Surfaced architectural questions when the constraints left room for multiple valid approaches

This model flips the typical AI-in-development relationship. Jeremy was not directing Claude Code line-by-line. Claude Code was not waiting for approval on every design choice. They were collaborating as peers with clear ownership.

---

## The Numbers: What Actually Got Built

| Gem | Tests | Purpose |
|-----|-------|---------|
| wild-capability-gate | 224 | Cross-cutting access control |
| wild-rails-safe-introspection-mcp | 468 | Safe, read-only Rails introspection via MCP |
| wild-admin-tools-mcp | 439 | Governed admin operations via MCP |
| wild-session-telemetry | 325 | Privacy-first telemetry collection |
| wild-transcript-pipeline | 200+ | Transcript normalization with PII redaction |
| wild-gap-miner | 276 | Gap analysis from telemetry data |
| wild-hook-ops | 247 | Hook lifecycle management |
| wild-permission-analyzer | 217 | Static permission auditing |
| wild-test-flake-forensics | 277 | Flake detection + root cause analysis |
| wild-skillops-registry | 251 | Skills registry + coordination |
| **Total** | **~2,924** | **10 repos, 10 epics each, 60+ canonical docs** |

All written to pass zero RuboCop offenses. All with explicit safety rules documented and tested. All with clear data contracts and cross-repo dependencies mapped.

---

## What "AI as Tech Lead" Actually Means

This model is not about code generation. It is about technical decision-making under constraints.

Consider the capability gate -- the access control layer that guards privileged tool access across the ecosystem. When Jeremy defined the mission ("answer whether this agent can call this tool in this context"), Claude Code had to decide:

- What is the shape of a capability ID? Is it a string like `"admin.job.retry"`, or is there a structured format?
- How are policies stored? In memory, in YAML, in a DSL?
- What is the runtime interface? Do calls check a constant hash, call a method on a gate object, or something else?

Jeremy provided the safety rules: "authorization must be logged," "denials must never propagate as exceptions," "configuration must freeze after startup." Within those constraints, Claude Code made implementation choices.

These choices had downstream effects. When wild-admin-tools-mcp needed to integrate the capability gate, the decisions Claude Code made in the gate repo directly shaped the integration pattern. When wild-rails-safe-introspection-mcp followed, it inherited those patterns.

That consistency across 10 independent repositories did not happen by accident. It happened because Claude Code maintained internal coherence -- asking itself "am I following the pattern established in the capability gate?" and "will future implementers understand why I chose this way?"

---

## The CLAUDE.md Coordination Mechanism

Each repository has its own `CLAUDE.md` file. These files are not documentation -- they are contracts.

Example from wild-admin-tools-mcp:

```
## Safety Rules for Claude Code

These are non-negotiable when working in this repo:

1. Never bypass the capability gate. All operations require gate
   authorization. If the gate is unavailable, operations fail closed.
2. Never skip dry-run support. Every action handler must implement
   both preview and execute paths. Dry-run must never trigger side effects.
3. Never skip confirmation for destructive operations. Two-phase
   confirmation with server-generated nonce is mandatory.
```

These are not suggestions. They are rules that Claude Code follows and tests against. A change that violates these rules is rejected, even if it would otherwise be a clean implementation.

The CLAUDE.md file is the binding contract between Jeremy (as architect) and Claude Code (as implementer). It prevents scope creep. It enforces consistency. It makes the constraints explicit so they can be tested.

---

## Cross-Repo Dependency Management

Ten independent repositories need consistent patterns. The wild ecosystem used three mechanisms:

### 1. Beads (Task Tracking)

Each repository uses Beads for task tracking. All 10 repositories follow the same structure:

- 10 epics per repo (named for outcomes, not technical nouns)
- Child tasks under each epic with clear acceptance criteria
- Explicit dependency blocks between tasks and across repositories
- Annotations that read like operator progress notes, not machine scraps

Moving from one repo to another felt natural. The task structure was familiar. The acceptance criteria patterns were consistent.

### 2. Canonical Documentation in `000-docs/`

Every repo has a `000-docs/` directory with filed documents following `/doc-filing` conventions:

- `001-PP-PLAN-repo-blueprint.md` (mission, boundaries, architecture)
- `002-PP-PLAN-epic-build-plan.md` (10-epic breakdown)
- `003-TQ-STND-privacy-model.md` (privacy guarantees)
- `004-AT-ADEC-architecture-decisions.md` (why things are shaped this way)

Understanding a new repo required reading predictable documents in a predictable order. The cognitive load for moving between repositories was minimal.

### 3. Shared Notes

When a pattern emerged that applied across multiple repos, it was documented once and linked from affected repos. When multiple repos needed to validate configuration, a shared note on "Configuration Freezing Patterns" was filed. Each repo referenced it, preventing copy-paste divergence.

---

## Quality Metrics: What a Human Reviewer Would Find

Zero RuboCop offenses across all 10 repositories is notable but expected. More interesting are the quality choices:

### Adversarial Testing

Every safety rule gets tested by code that tries to break it.

Example from wild-admin-tools-mcp: the safety rule is "never bypass the capability gate." The test creates a scenario where an action is configured as allowed, but the capability gate denies it for a specific caller. The test verifies that even though the action is configured, the gate denial is respected.

### Privacy Invariant Tests

The session-telemetry library claims "22 field patterns must never be stored." The test creates an event with all 22 forbidden fields, feeds it to the ingestion layer, and verifies that after storage, none of those fields exist in the stored record.

### Data Contract Tests

Each repo that exports data has tests verifying the output contract. Example from wild-gap-miner: the export schema specifies that gap severity is always 0.0-1.0. The test creates gaps with invalid severity (e.g., 1.5, -0.1) and verifies that the export layer rejects them.

### Cross-Repo Integration Tests

When wild-gap-miner depends on output from wild-session-telemetry and wild-transcript-pipeline, integration tests create realistic exports from both upstream repos, feed them to the gap-miner, and verify that analysis runs correctly. These tests prevent contract drift.

---

## What This Changes

The developer becomes architect. The AI handles implementation depth.

In a traditional model, the architect specifies features, and the developer implements them. In this model, Jeremy specified constraints and outcomes, and Claude Code made the technical decisions that transformed those constraints into working, tested, documented code.

The implications:

1. **Architectural leverage increases.** One architect can oversee 10 repositories with thousands of tests because the AI is making sound decisions within specified constraints -- not asking for permission on every detail.

2. **Code review focus shifts.** Instead of reviewing line-by-line implementations, review focuses on whether constraints were honored, whether safety rules were tested, whether documentation is clear.

3. **Consistency improves.** Because the AI makes decisions within constraints, patterns emerge naturally. Divergence has to be intentional, not accidental.

4. **Knowledge transfer becomes feasible.** Documentation-first execution means future implementers (human or AI) can read the decisions and understand the reasoning.

---

## Practical Takeaways: How to Replicate This

### 1. Define the CLAUDE.md Template

Create a standard CLAUDE.md structure that every repo follows. Include mission, scope, non-goals, directory layout, build commands, safety rules (numbered, binding, tested), canonical doc index, and task tracking rules. Make it a contract, not guidance.

### 2. Use the 10-Epic Structure

Every repository starts with the same epic breakdown:

- Epic 1: Foundations (schema, configuration, core interfaces)
- Epics 2-9: Feature areas (each focused and complete)
- Epic 10: Quality (adversarial testing, documentation, release)

This forces completeness. You cannot ship a repo that skips Epic 10.

### 3. Track Tasks with Explicit Dependencies

Use Beads or an equivalent that enforces dependency blocks between tasks, cross-repo dependency visibility, narrative annotations, and no task closure without evidence.

### 4. Document Decisions as You Build

When a question arises ("should we store denied capabilities in the gate log?"), answer it in a filed document, not just in code comments. Use numbered documents with category and type codes. Maintain an INDEX.

### 5. Establish Clear Data Contracts

When a repository exports data, the output schema is a living document: filed, typed, versioned, and validated by integration tests.

### 6. Test Safety Rules Adversarially

For every safety rule, write a test that tries to violate it:

```ruby
describe "Safety: never bypass the gate" do
  it "fails closed when gate denies, even if action is in allowlist" do
    gate.deny_action(:retry_job, for: specific_caller)
    result = executor.execute(Action.new(:retry_job, caller: specific_caller))

    expect(result).to be_denied
    expect(result.reason).to eq "gate_denied"
  end
end
```

These tests are your safety ratchet. They prevent regressions.

---

## The Reality Check

Building 10 production repositories with this model required:

- Clear architectural vision upfront (the master blueprint)
- Detailed per-repo planning before any code (the CLAUDE.md files)
- Disciplined task tracking (Beads, with explicit dependencies)
- Aggressive testing (~300 tests per repo on average)
- Extensive documentation (60+ filed documents)

This is not a lightweight approach. It is intentional, documented, and exhaustive.

But it produced something most teams do not achieve: 10 independent repositories that work together cohesively, with zero accidental divergence, clear contracts, testable safety rules, and documentation that future implementers can actually read and understand.

---

## Summary

Claude Code as tech lead works when:

1. The architect defines missions, boundaries, and non-negotiable rules
2. The implementer makes sound technical decisions within those constraints
3. The coordination layer (CLAUDE.md, Beads, canonical docs) makes decisions explicit and testable
4. Safety is treated as a first-class concern, not an afterthought

The result is not faster development. It is better development: less divergence, more consistency, more testable, more documentable.

The wild ecosystem is proof that this model scales to 10 independent repositories, multiple layers of abstraction, cross-repo dependencies, and production-grade quality standards.

What changed is not AI capabilities. It is the collaboration model. Human architect, AI tech lead, structured constraints, explicit contracts, and rigorous testing produce something neither could build alone.

---

## The Full Series

- **Part 1**: [The Safety Architecture](/posts/wild-deep-dive-1-safety-architecture/) -- Defense in depth, adversarial testing, hard safety ceilings
- **Part 2**: [CLAUDE.md -- Human-AI Collaboration Pattern](/posts/wild-deep-dive-2-claude-md/) -- Per-repo contracts that prevent scope creep and enforce safety
- **Part 3**: [The Observability Loop](/posts/wild-deep-dive-3-observability/) -- Telemetry, transcripts, and gap mining as a self-improving feedback loop
- **Part 4**: This article -- Claude Code as tech lead across 10 production gems

---

*Part of the [Wild Ecosystem](/wild-ecosystem/) -- 10 Ruby gems for governed AI agent operations in production Rails. Built with [Claude Code](https://claude.ai/code).*
