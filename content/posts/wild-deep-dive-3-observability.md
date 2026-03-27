+++
title = 'Deep Dive Part 3: The Observability Loop — Teaching AI Tools to Improve Themselves'
date = 2026-03-26T15:00:00-05:00
draft = false
tags = ["wild-ecosystem", "ruby", "observability", "telemetry", "privacy", "claude-code", "ai-agents"]
categories = ["Wild Ecosystem Deep Dive"]
description = "How the wild ecosystem's three-repo pipeline — telemetry, transcript normalization, and gap mining — creates a feedback loop that teaches AI tools what they're struggling with."
toc = true
+++

Most AI tool ecosystems follow a pattern: build the tools, ship them, hope they work. Updates happen when someone reports a problem or a human reviewer notices something is broken.

For AI agents operating with tool access in production Rails systems, with real stakes and real blast radius, hoping is not a strategy.

The [wild ecosystem](/wild-ecosystem/) was built with a different assumption: **agents operating with access need external feedback about what they struggle with.** Not logging for compliance. Not metrics for observability dashboards. But structured signals about denial rates, failure patterns, latency outliers, and capability gaps.

Three repositories make this work. They share no code. They have independent test suites, independent release cycles, and clear data contracts. Together, they answer a question most AI-in-production deployments never ask: what is this system actually struggling with?

This is Part 3 of the [Wild Ecosystem Deep Dive](/wild-ecosystem/) series.

---

## The Three-Repo Pipeline

The observability loop is implemented as three independent gems. Each has a single responsibility. Each defines clear input/output contracts.

```
wild-session-telemetry     (collection)
    |
    v  structured events
wild-transcript-pipeline   (normalization + redaction)
    |
    +-----> wild-gap-miner (analysis + recommendations)
    |            ^
    +------------+
```

### Repository 1: wild-session-telemetry (325 tests)

**Mission:** Collect and export privacy-aware telemetry from agent sessions.

When agents invoke tools through wild-admin-tools-mcp or wild-rails-safe-introspection-mcp, events fire to the telemetry layer. Those events describe:

- The tool that was called (action name)
- The outcome (success, denied, error, rate_limited, preview)
- How long it took (latency in milliseconds)
- When it happened (ISO 8601 timestamp)
- Who called it (service account identifier)

The telemetry layer **never** receives:
- Raw parameter values (which job ID was retried, which cache key was invalidated)
- Before/after state snapshots
- Confirmation nonces
- Stack traces
- Adapter-specific identifiers

These exclusions are hardcoded. Not configurable. The forbidden field list is enforced at the privacy layer, before any event touches storage.

**Why fire-and-forget?** Telemetry failures must never break the upstream pipeline. If the telemetry collector is slow, out of disk space, or completely down, agents continue operating. A failure is logged to stderr, swallowed, and operations proceed. This is the opposite of how logging usually works, and it is intentional.

**Configuration is frozen at startup.** Storage backends, output paths, privacy rules -- all locked. No runtime reconfiguration. This prevents configuration drift from weakening privacy guarantees mid-session.

Pure Ruby with zero runtime dependencies beyond stdlib.

### Repository 2: wild-transcript-pipeline (200+ tests)

**Mission:** Ingest, normalize, and process conversation transcripts at scale.

This repository handles the raw conversation context -- turns, tool invocations, intent signals. It does three things:

1. **Ingestion with multiple adapters.** Three sources: Claude Code session JSONL, MCP protocol logs, and generic conversation JSON. Each adapter converts its format into a common normalized schema.

2. **Privacy redaction at the turn level.** Transcripts contain freeform conversation that may include secrets and PII. The pipeline strips:
   - API keys and tokens (AWS, GitHub, bearer tokens)
   - Email addresses and IP addresses
   - Absolute filesystem paths
   - Embedded file contents
   - Custom patterns (via configuration)

3. **Export in multiple formats.** Normalized and redacted transcripts export as clean JSON Lines or Markdown.

This gem does not communicate with a network. It does not execute code. It does not persist state. It is a pure data transformation layer: ingest, normalize, redact, export.

Zero runtime dependencies.

### Repository 3: wild-gap-miner (276 tests)

**Mission:** Analyze telemetry and transcript data to surface capability gaps.

This is where the pipeline becomes intelligence. The gap-miner consumes structured data from both telemetry and transcripts and runs six analyzers:

1. **Denial analyzer** -- High denial rates signal policy mismatches or gaps in the capability gate's allowlist.
2. **Failure analyzer** -- High tool failure rates suggest fragile implementations or unhandled edge cases.
3. **Latency analyzer** -- High p95 latency suggests resource contention, blocking I/O, or algorithmic inefficiency.
4. **Utilization analyzer** -- Low capability coverage means tools are undiscoverable, poorly designed, or genuinely unneeded.
5. **Coverage analyzer** -- Gaps between what agents attempt and what tools provide are feature request signals.
6. **Pattern analyzer** -- Unusual sequences of tool calls, unexpected outcome distributions, or behavioral anomalies.

Each analyzer scores findings on a 0.0-1.0 scale. Gaps are ranked by severity. Recommendations are auto-generated.

Pure Ruby stdlib. Zero runtime dependencies.

---

## Privacy-First Telemetry: How Exclusions Are Enforced

The session-telemetry library enforces privacy through three mechanisms:

### 1. Hardcoded Forbidden Field List

22+ field patterns that must never be stored. This list is code, not configuration. It is not optional.

Examples: `params`, `parameters`, `before_state`, `after_state`, `nonce`, `confirmation_nonce`, `stack_trace`, `backtrace`, `jid`, `execution_id`.

If an incoming event contains any of these fields, they are stripped before storage.

### 2. Per-Event-Type Metadata Allowlists

Each event type has an explicit allowlist of metadata fields. Only those pass through. Everything else is dropped.

A job retry event might allow metadata fields like `category` and `job_type`. It does not allow `job_id`, `parameters`, `retry_count`, or anything that could leak operational specifics.

### 3. Fire-and-Forget with Zero Propagation

Telemetry errors -- ingestion failures, storage failures, export failures -- are logged to stderr and swallowed. They never propagate to the upstream caller.

This is a safety feature disguised as a failure mode. If the telemetry layer is broken, agents continue operating. The downstream gap-miner may see no data, but the operational pipeline is unaffected.

Telemetry gaps will not wake you at 3am. You will discover them during analysis, when gap-miner reports no recent data. That is a reasonable trade-off.

---

## What the Gap Miner Finds

Here is a concrete example of what gap analysis produces:

**Input:** 30 days of telemetry + transcripts from a Rails development workflow.

**Gap Report Output:**

```
Gaps Discovered (ranked by severity):

1. [DENIAL RATE]
   Severity: 0.92
   Tool: introspection.list_models
   Evidence: Hit 47% denial rate; policy mismatch or under-privileged caller
   Recommendation: Review capability gate policy for service-account-ci

2. [COVERAGE GAP]
   Severity: 0.78
   Signal: Agents asked for job retry API 18 times; current tool not exposed
   Recommendation: Add job_retry action to admin-tools-mcp

3. [LATENCY SPIKE]
   Severity: 0.65
   Tool: introspection.schema_query
   Evidence: p95 latency 2400ms; p50 is 140ms
   Recommendation: Check N+1 queries in schema introspection; consider caching

4. [PATTERN ANOMALY]
   Severity: 0.42
   Signal: Agents are calling introspection.list_models in tight loops
   Recommendation: Add discovery tool that lists available models once
```

Each gap is scored, ranked, and actionable. Operators prioritize work. Product teams make feature decisions. Infrastructure teams investigate performance regressions.

---

## Zero Runtime Dependencies

Both the transcript-pipeline and gap-miner use pure Ruby stdlib. No ActiveRecord, no HTTP client, no JSON parser beyond stdlib.

Why this matters:

1. **Production safety.** No dependency tree to audit. No transitive security issues. No version conflicts with the host application.
2. **Deployment simplicity.** These gems embed in any Ruby environment without adding operational overhead.
3. **Composability.** The pipeline can run offline, in batch, or integrated into diverse infrastructure without coordinating dependency versions.
4. **Auditability.** The source code is the complete system. No hidden behaviors in third-party libraries.

---

## Claude Code's Role in Building the Loop

Key decisions Claude Code made during implementation:

1. **Fire-and-forget semantics for telemetry failures.** Not "fail fast," but "never fail the upstream caller." This required careful error handling design.
2. **Forbidden field enforcement as hardcoded strings, not regexes.** Prevents subtle bugs where matching logic evolves over time and becomes less strict.
3. **Per-event-type metadata allowlists.** Not a global allowlist, but per-event-type. Fine-grained control while preventing operator mistakes.
4. **Three independent transcript adapters.** Not a monolithic parser, but separate adapters with a common output schema. Adding new sources is straightforward.
5. **Gap scoring on a normalized 0.0-1.0 scale.** Allows gaps to be ranked across different analysis types (denial, latency, coverage) on a common severity axis.
6. **Zero runtime dependencies as a hard constraint.** Not a goal -- a requirement. The implementation had to use only stdlib.

---

## Building Your Own Loop

The pattern is generalizable to any AI tool ecosystem:

**Layer 1: Collection (fire-and-forget).** Build a subscriber that receives events from operational tools. Apply strict privacy filtering. Make failures invisible to upstream. Freeze configuration after startup.

**Layer 2: Normalization (multiple sources, one schema).** Accept raw transcripts from multiple sources. Normalize via adapters. Apply privacy redaction at the content level. Export in multiple formats.

**Layer 3: Analysis (scoring and ranking).** Build analyzers that consume normalized data and surface gaps. Score on a normalized scale. Rank by severity. Generate actionable recommendations.

**Cross-cutting concerns:**
- Document input/output schemas for each layer. Make them immutable.
- Make privacy defaults restrictive. Force operators to expand, not shrink.
- Every privacy claim must have a corresponding adversarial test.
- File technical decisions in durable documents for future implementers.

---

## The Feedback Loop in Action

1. Agents interact with tools through wild-rails-safe-introspection-mcp and wild-admin-tools-mcp.
2. Those interactions emit telemetry events to wild-session-telemetry.
3. Sessions also produce transcript logs.
4. Both streams feed into wild-transcript-pipeline for normalization and redaction.
5. The gap-miner consumes both normalized telemetry and transcripts.
6. Gap reports surface actionable feedback: missing tools, policy mismatches, performance regressions, usage patterns.
7. That feedback drives tool development, policy tuning, and infrastructure improvements.

Without this loop, tools stagnate. With it, they improve iteratively based on actual usage patterns and agent struggles.

The wild ecosystem is not a static set of tools. It is a learning system that gets better because it has feedback.

---

## What Comes Next

- **Part 1**: [The Safety Architecture](/posts/wild-deep-dive-1-safety-architecture/) -- Defense in depth, adversarial testing, hard safety ceilings
- **Part 2**: [CLAUDE.md — Human-AI Collaboration Pattern](/posts/wild-deep-dive-2-claude-md/) -- Per-repo contracts that prevent scope creep and enforce safety
- **Part 4**: [Claude Code as Tech Lead](/posts/wild-deep-dive-4-tech-lead/) -- What happens when the AI makes the architectural decisions

This is the opposite of "build and hope." This is "build, observe, improve."

---

*Part of the [Wild Ecosystem](/wild-ecosystem/) -- 10 Ruby gems for governed AI agent operations in production Rails. Built with [Claude Code](https://claude.ai/code).*
