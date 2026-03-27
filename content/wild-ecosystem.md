+++
title = 'Wild Ecosystem'
date = 2026-03-26T12:00:00-05:00
menu = 'main'
weight = 15
+++

# The Wild Ecosystem

**10 Ruby gems. ~2,924 tests. One mission: make AI agents safe in production Rails.**

The wild ecosystem is a family of focused, open-source Ruby gems that together form a governed operational intelligence layer for AI-assisted development workflows. Every gem enforces safety by default — read-only where it matters, audited everywhere, bounded always.

Built collaboratively with [Claude Code](https://claude.ai/code).

---

## The Problem

AI agents are getting tool access to production systems. MCP is becoming the standard protocol. But most implementations give agents unrestricted access — raw console, arbitrary queries, no audit trail. One bad tool call mutates data. One expensive query kills a replica.

Wild takes a different approach: **governed, audited, bounded access with hard safety ceilings that cannot be overridden.**

---

## Architecture

Five layers, ten gems, clear boundaries between each.

```
┌─────────────────────────────────────────────────────────┐
│  Layer 5: Skill Governance                              │
│  wild-skillops-registry                                 │
├─────────────────────────────────────────────────────────┤
│  Layer 4: Workflow Enforcement                          │
│  wild-hook-ops · wild-permission-analyzer               │
│  wild-test-flake-forensics                              │
├─────────────────────────────────────────────────────────┤
│  Layer 3: Observability & Learning Loop                 │
│  wild-session-telemetry → wild-transcript-pipeline      │
│                          → wild-gap-miner               │
├─────────────────────────────────────────────────────────┤
│  Layer 2: Governed Access                               │
│  wild-capability-gate                                   │
├─────────────────────────────────────────────────────────┤
│  Layer 1: Safe Production Visibility                    │
│  wild-rails-safe-introspection-mcp                      │
│  wild-admin-tools-mcp                                   │
└─────────────────────────────────────────────────────────┘
```

---

## The 10 Gems

### Layer 1 — Safe Production Visibility

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 2rem;">
<div>

**[wild-rails-safe-introspection-mcp](https://github.com/jeremylongshore/wild-rails-safe-introspection-mcp)** | 468 tests

Safe, read-only Rails introspection via MCP. Three tools: `inspect_model_schema`, `lookup_record_by_id`, `find_records_by_filter`. Allowlist-enforced, row-capped, query-timed-out, fully audited. No write paths exist in the codebase.

</div>
<div>

**[wild-admin-tools-mcp](https://github.com/jeremylongshore/wild-admin-tools-mcp)** | 439 tests

Governed admin operations via MCP. 19 actions across background jobs, cache, and feature flags. Every mutation requires two-phase nonce confirmation (SHA-256 bound to action + params + caller). Dry-run previews with zero side effects. Blast radius caps with hard ceilings.

</div>
</div>

### Layer 2 — Governed Access

**[wild-capability-gate](https://github.com/jeremylongshore/wild-capability-gate)** | 224 tests

Cross-cutting access control. Defines what capabilities exist, who can use them, and what prerequisites must be met. Fail-closed (errors produce denial, never permission). No implicit grants. Configuration frozen after startup. Complete audit trail of every evaluation.

### Layer 3 — Observability & Learning Loop

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1.5rem; margin-bottom: 2rem;">
<div>

**[wild-session-telemetry](https://github.com/jeremylongshore/wild-session-telemetry)** | 325 tests

Privacy-first telemetry collection. 22 hardcoded forbidden fields. Per-event-type metadata allowlists. Fire-and-forget semantics — telemetry failures never break upstream tools. Aggregation engine with pattern detection.

</div>
<div>

**[wild-transcript-pipeline](https://github.com/jeremylongshore/wild-transcript-pipeline)** | 200+ tests

Transcript normalization with PII redaction. Three format adapters (Claude Code JSONL, MCP protocol logs, generic JSON). Strips emails, IPs, API keys, AWS creds, GitHub tokens, absolute paths. Zero runtime dependencies.

</div>
<div>

**[wild-gap-miner](https://github.com/jeremylongshore/wild-gap-miner)** | 276 tests

Gap analysis from telemetry and transcript data. Six analyzers: denial rate, failure rate, latency outliers, low utilization, poor coverage, recurring patterns. Severity scoring with actionable recommendations. Pure Ruby stdlib.

</div>
</div>

### Layer 4 — Workflow Enforcement

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1.5rem; margin-bottom: 2rem;">
<div>

**[wild-hook-ops](https://github.com/jeremylongshore/wild-hook-ops)** | 247 tests

Hook lifecycle management. Registration, priority-ordered execution, per-handler timeout isolation, error isolation, health monitoring with metrics. Audit trail of every hook execution.

</div>
<div>

**[wild-permission-analyzer](https://github.com/jeremylongshore/wild-permission-analyzer)** | 217 tests

Static analysis of capability-gate configs before deployment. Six analyzers: consistency, risk, prerequisites, coverage, orphans, shadows. Catches permission model mistakes before they reach production.

</div>
<div>

**[wild-test-flake-forensics](https://github.com/jeremylongshore/wild-test-flake-forensics)** | 277 tests

Flaky test detection with confidence-scored root cause hypotheses. Supports RSpec JSON, JUnit XML, minitest. History tracking with trend detection (worsening/stable/improving). Triage reports with severity scoring.

</div>
</div>

### Layer 5 — Skill Governance

**[wild-skillops-registry](https://github.com/jeremylongshore/wild-skillops-registry)** | 251 tests

Skills registry and coordination control plane. Lifecycle management (draft → active → deprecated → retired), health tracking with staleness detection, full-text search with relevance scoring, version management with changelogs. The coordination layer that ties the ecosystem together.

---

## Safety Innovations

**Allowlist-first access.** Models must be explicitly permitted. Unknown models and blocked models produce identical denial responses — no enumeration possible.

**Read-only by design.** No write paths in the introspection tools. No `eval`, no `constantize`, no dynamic method dispatch on user input. Enforced at adapter, guard, and audit layers independently.

**Two-phase nonce confirmation.** Admin mutations bind a SHA-256 nonce to the specific action, parameters, and caller identity. Single-use. Time-limited. Opaque failure reasons prevent oracle attacks.

**Hard ceilings.** Row caps (default 50, ceiling 1000) and query timeouts (default 5s, ceiling 30s) that cannot be overridden by configuration. Exceeding the cap is an error, not a silent truncation.

**Adversarial testing.** SQL injection payloads, Ruby code execution attempts, null byte injection, prompt injection via model names — all verified as inert data. Database state snapshots before and after prove zero mutations.

**Privacy-first telemetry.** Hardcoded forbidden field lists (not configurable). Per-event-type metadata allowlists. PII is never collected, not just "redacted after the fact."

---

## Built with Claude Code

The wild ecosystem was designed and implemented collaboratively with [Claude Code](https://claude.ai/code), Anthropic's AI coding agent. Claude Code served as technical lead — making architectural decisions, implementing all ten gems, writing adversarial test suites, and managing cross-repo consistency.

The coordination mechanism: every repo has a `CLAUDE.md` file that acts as a binding contract between human architect and AI implementer. Safety rules, scope boundaries, and non-negotiable constraints are enforced through this pattern.

**Deep dive series:**
- [Part 1: The Safety Architecture](/posts/wild-deep-dive-1-safety-architecture/) *(coming soon)*
- [Part 2: CLAUDE.md — Human-AI Collaboration Pattern](/posts/wild-deep-dive-2-claude-md/) *(coming soon)*
- [Part 3: The Observability Loop](/posts/wild-deep-dive-3-observability/) *(coming soon)*
- [Part 4: Claude Code as Tech Lead](/posts/wild-deep-dive-4-tech-lead/) *(coming soon)*

---

## Quick Stats

| | |
|---|---|
| **Gems** | 10 |
| **Total tests** | ~2,924 |
| **Canonical docs** | 60+ |
| **Language** | Ruby 3.2+ |
| **Test framework** | RSpec |
| **Lint** | RuboCop (zero offenses across all repos) |
| **CI** | GitHub Actions (every repo) |
| **License** | Intent Solutions Proprietary |

---

## Get Started

All ten repos are public on GitHub:

```
github.com/jeremylongshore/wild-rails-safe-introspection-mcp
github.com/jeremylongshore/wild-admin-tools-mcp
github.com/jeremylongshore/wild-capability-gate
github.com/jeremylongshore/wild-session-telemetry
github.com/jeremylongshore/wild-transcript-pipeline
github.com/jeremylongshore/wild-gap-miner
github.com/jeremylongshore/wild-hook-ops
github.com/jeremylongshore/wild-permission-analyzer
github.com/jeremylongshore/wild-test-flake-forensics
github.com/jeremylongshore/wild-skillops-registry
```

---

*Built with [Claude Code](https://claude.ai/code). Governed by design.*
