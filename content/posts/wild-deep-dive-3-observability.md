+++
title = 'Deep Dive Part 3: The Observability Loop — Teaching AI Tools to Improve Themselves'
slug = 'wild-deep-dive-3-observability'
date = 2026-03-26T15:00:00-05:00
draft = false
tags = ["wild-ecosystem", "ruby", "observability", "telemetry", "privacy", "claude-code", "ai-agents"]
categories = ["Wild Ecosystem Deep Dive"]
description = "How the wild ecosystem's three-repo pipeline — telemetry, transcript normalization, and gap mining — creates a feedback loop that teaches AI tools what they are struggling with. Read against Dapper, fire-and-forget supervision, and the privacy-engineering literature."
toc = true
bibliography = "citations/wild-citations.bib"
+++

Most AI-tool ecosystems follow the same operational pattern: build the tools, ship them, hope they work. Updates happen when someone reports a problem or a human reviewer notices something is broken. For agents that hold tool access to production Rails systems, with real stakes and real blast radius, hoping is not a strategy.

The [wild ecosystem](/wild-ecosystem/) was built with a different assumption: **agents operating with access need external feedback about what they struggle with.** Not compliance logging. Not dashboards for human consumption. Structured signals about denial rates, failure patterns, latency outliers, and capability gaps, designed for downstream automated analysis.

Three repositories make this work. They share no code. They have independent test suites, independent release cycles, and clear data contracts. Together, they answer a question most AI-in-production deployments never ask: *what is this system actually struggling with?* The architectural pattern — instrument cheaply, normalise centrally, analyse asynchronously — is the same one Sigelman and colleagues described in Google's Dapper paper[^sigelman2010dapper], adapted for a domain where the *production system* is an agent that calls tools rather than a microservice that serves requests.

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

**Mission:** collect and export privacy-aware telemetry from agent sessions.

When agents invoke tools through `wild-admin-tools-mcp` or `wild-rails-safe-introspection-mcp`, events fire to the telemetry layer. Those events describe:

- the tool that was called (action name)
- the outcome (success, denied, error, rate-limited, preview)
- how long it took (latency in milliseconds)
- when it happened (ISO 8601 timestamp)
- who called it (service-account identifier)

The telemetry layer **never** receives:

- raw parameter values (which job ID was retried, which cache key was invalidated)
- before/after state snapshots
- confirmation nonces
- stack traces
- adapter-specific identifiers

These exclusions are hardcoded. Not configurable. The forbidden-field list is enforced at the privacy layer, before any event touches storage — closer in spirit to the *data-minimisation* discipline of Sweeney's k-anonymity work[^sweeney2002kanonymity] than to the more permissive "log everything, scrub later" pattern common in operational telemetry.

**Why fire-and-forget?** Telemetry failures must never break the upstream pipeline. If the telemetry collector is slow, out of disk space, or completely down, agents continue operating. A failure is logged to stderr, swallowed, and operations proceed. This is the opposite of how logging usually works, and it is intentional. The pattern is a direct descendant of Armstrong's *let-it-crash* discipline from the Erlang OTP tradition[^armstrong2003reliable]: the unreliable subsystem must be quarantined from the reliable one, and the supervisor — not the worker — owns the decision about how failures propagate.

**Configuration is frozen at startup.** Storage backends, output paths, privacy rules — all locked. No runtime reconfiguration. This prevents configuration drift from weakening privacy guarantees mid-session.

Pure Ruby with zero runtime dependencies beyond stdlib.

### Repository 2: wild-transcript-pipeline (200+ tests)

**Mission:** ingest, normalise, and process conversation transcripts at scale.

This repository handles the raw conversation context — turns, tool invocations, intent signals. It does three things:

1. **Ingestion with multiple adapters.** Three sources: Claude Code session JSONL, MCP protocol logs, and generic conversation JSON. Each adapter converts its format into a common normalised schema.

2. **Privacy redaction at the turn level.** Transcripts contain freeform conversation that may include secrets and personally identifiable information. The pipeline strips:
   - API keys and tokens (AWS, GitHub, bearer tokens)
   - email addresses and IP addresses
   - absolute filesystem paths
   - embedded file contents
   - custom patterns (via configuration)

3. **Export in multiple formats.** Normalised and redacted transcripts export as clean JSON Lines or Markdown.

This gem does not communicate with a network. It does not execute code. It does not persist state. It is a pure data-transformation layer: ingest, normalise, redact, export.

Zero runtime dependencies.

### Repository 3: wild-gap-miner (276 tests)

**Mission:** analyse telemetry and transcript data to surface capability gaps.

This is where the pipeline becomes intelligence. The gap-miner consumes structured data from both telemetry and transcripts and runs six analysers:

1. **Denial analyser** — high denial rates signal policy mismatches or gaps in the capability gate's allowlist.
2. **Failure analyser** — high tool-failure rates suggest fragile implementations or unhandled edge cases.
3. **Latency analyser** — high p95 latency suggests resource contention, blocking I/O, or algorithmic inefficiency.
4. **Utilisation analyser** — low capability coverage means tools are undiscoverable, poorly designed, or genuinely unneeded.
5. **Coverage analyser** — gaps between what agents attempt and what tools provide are feature-request signals.
6. **Pattern analyser** — unusual sequences of tool calls, unexpected outcome distributions, or behavioural anomalies.

Each analyser scores findings on a 0.0–1.0 scale. Gaps are ranked by severity. Recommendations are auto-generated. The architectural pattern — *cheap collection plus deferred deep analysis* — is the design Sigelman and colleagues recommended in the Dapper paper based on operational experience at Google scale[^sigelman2010dapper]; the move Beyer and colleagues codified for SRE practice generally is the same one[^beyer2016sre].

Pure Ruby stdlib. Zero runtime dependencies.

---

## Privacy-First Telemetry: How Exclusions Are Enforced

The session-telemetry library enforces privacy through three mechanisms.

### 1. Hardcoded Forbidden-Field List

Twenty-two-plus field patterns that must never be stored. This list is code, not configuration. It is not optional.

Examples: `params`, `parameters`, `before_state`, `after_state`, `nonce`, `confirmation_nonce`, `stack_trace`, `backtrace`, `jid`, `execution_id`.

If an incoming event contains any of these fields, they are stripped before storage. The design choice to keep the list in code rather than in configuration is deliberate: configuration is mutable at deploy time and prone to silent erosion; code is part of the artefact under review. The audit-log-integrity literature, going back to Schneier and Kelsey's 1999 work[^schneier1999audit] and Haber and Stornetta's earlier digital-time-stamp scheme[^haber1991timestamp], converges on the same posture — the rule that protects sensitive data must itself be tamper-evident.

### 2. Per-Event-Type Metadata Allowlists

Each event type has an explicit allowlist of metadata fields. Only those pass through. Everything else is dropped.

A job-retry event might allow metadata fields like `category` and `job_type`. It does not allow `job_id`, `parameters`, `retry_count`, or anything that could leak operational specifics.

### 3. Fire-and-Forget with Zero Propagation

Telemetry errors — ingestion failures, storage failures, export failures — are logged to stderr and swallowed. They never propagate to the upstream caller.

This is a safety feature disguised as a failure mode. If the telemetry layer is broken, agents continue operating. The downstream gap-miner may see no data, but the operational pipeline is unaffected. The discipline is the Armstrong *isolate-failures-at-the-supervisor* pattern from the Erlang OTP tradition[^armstrong2003reliable]: the worker does not get to decide whether its own failure should hurt the system. Telemetry gaps will not page anyone at 03:00; they will be discovered during analysis, when the gap-miner reports no recent data. That is a reasonable trade-off.

---

## What the Gap Miner Finds

Here is a concrete example of what gap analysis produces.

**Input:** thirty days of telemetry plus transcripts from a Rails development workflow.

**Gap report output:**

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

Each gap is scored, ranked, and actionable. Operators prioritise work. Product teams make feature decisions. Infrastructure teams investigate performance regressions. The format follows the *p99 latency plus categorical outcome* idiom Beyer and colleagues established as the operational standard for SRE-grade observability[^beyer2016sre].

---

## Zero Runtime Dependencies

Both the transcript-pipeline and gap-miner use pure Ruby stdlib. No ActiveRecord, no HTTP client, no JSON parser beyond stdlib.

The reasons are operational. First, *production safety*: no dependency tree to audit, no transitive security issues, no version conflicts with the host application. Second, *deployment simplicity*: these gems embed in any Ruby environment without adding operational overhead. Third, *composability*: the pipeline can run offline, in batch, or integrated into diverse infrastructure without coordinating dependency versions. Fourth, *auditability*: the source code is the complete system. There are no hidden behaviours in third-party libraries — a property Schneier and Kelsey identified as essential for any audit subsystem[^schneier1999audit].

---

## Claude Code's Role in Building the Loop

Several decisions Claude Code made during implementation are worth naming explicitly.

1. **Fire-and-forget semantics for telemetry failures.** Not *fail fast*, but *never fail the upstream caller*. The error-containment design follows Armstrong's supervision-tree discipline directly[^armstrong2003reliable].
2. **Forbidden-field enforcement as hardcoded strings, not regexes.** Prevents subtle bugs where matching logic evolves over time and becomes less strict.
3. **Per-event-type metadata allowlists.** Not a global allowlist, but per-event-type. Fine-grained control while preventing operator mistakes — the *least common mechanism* posture Saltzer and Schroeder argued for[^saltzer1975protection] adapted to telemetry instead of access control.
4. **Three independent transcript adapters.** Not a monolithic parser, but separate adapters with a common output schema. Adding new sources is straightforward.
5. **Gap scoring on a normalised 0.0–1.0 scale.** Allows gaps to be ranked across different analysis types (denial, latency, coverage) on a common severity axis.
6. **Zero runtime dependencies as a hard constraint.** Not a goal — a requirement. The implementation had to use only stdlib.

---

## Building Your Own Loop

The pattern generalises to any AI-tool ecosystem.

**Layer 1: collection (fire-and-forget).** Build a subscriber that receives events from operational tools. Apply strict privacy filtering. Make failures invisible to upstream callers. Freeze configuration after startup.

**Layer 2: normalisation (multiple sources, one schema).** Accept raw transcripts from multiple sources. Normalise via adapters. Apply privacy redaction at the content level. Export in multiple formats.

**Layer 3: analysis (scoring and ranking).** Build analysers that consume normalised data and surface gaps. Score on a normalised scale. Rank by severity. Generate actionable recommendations.

**Cross-cutting concerns:**

- Document input/output schemas for each layer. Make them immutable contracts.
- Make privacy defaults restrictive. Force operators to expand, not shrink.
- Every privacy claim should have a corresponding adversarial test.
- File technical decisions in durable documents for future implementers.

---

## The Feedback Loop in Action

1. Agents interact with tools through `wild-rails-safe-introspection-mcp` and `wild-admin-tools-mcp`.
2. Those interactions emit telemetry events to `wild-session-telemetry`.
3. Sessions also produce transcript logs.
4. Both streams feed into `wild-transcript-pipeline` for normalisation and redaction.
5. The gap-miner consumes both normalised telemetry and transcripts.
6. Gap reports surface actionable feedback: missing tools, policy mismatches, performance regressions, usage patterns.
7. That feedback drives tool development, policy tuning, and infrastructure improvements.

Without this loop, tools stagnate. With it, they improve iteratively based on actual usage patterns and observed agent struggles.

The wild ecosystem is not a static set of tools. It is a learning system that gets better because it has feedback — instrumented along the architectural lines that Dapper established for distributed tracing[^sigelman2010dapper], with the privacy posture k-anonymity-style data minimisation prescribes[^sweeney2002kanonymity], and the supervision discipline let-it-crash made operational for fault containment[^armstrong2003reliable].

---

## What Comes Next

- **Part 1**: [The Safety Architecture](/posts/wild-deep-dive-1-safety-architecture/) — defence in depth, adversarial testing, hard safety ceilings.
- **Part 2**: [CLAUDE.md — Human–AI Collaboration Pattern](/posts/wild-deep-dive-2-claude-md/) — per-repo contracts that prevent scope creep and enforce safety.
- **Part 4**: [Claude Code as Tech Lead](/posts/wild-deep-dive-4-tech-lead/) — what happens when the AI makes the architectural decisions.

This is the opposite of "build and hope." This is "build, observe, improve."

---

*Part of the [Wild Ecosystem](/wild-ecosystem/) — 10 Ruby gems for governed AI agent operations in production Rails. Built with [Claude Code](https://claude.ai/code).*

---

## References

[^armstrong2003reliable]: Armstrong, J. (2003). *Making Reliable Distributed Systems in the Presence of Software Errors.* PhD thesis, Royal Institute of Technology (KTH), Stockholm.
[^beyer2016sre]: Beyer, B., Jones, C., Petoff, J., & Murphy, N. R. (Eds.). (2016). *Site Reliability Engineering: How Google Runs Production Systems.* O'Reilly Media.
[^haber1991timestamp]: Haber, S., & Stornetta, W. S. (1991). How to Time-Stamp a Digital Document. *Journal of Cryptology*, 3(2), 99–111. <https://doi.org/10.1007/BF00196791>
[^saltzer1975protection]: Saltzer, J. H., & Schroeder, M. D. (1975). The Protection of Information in Computer Systems. *Proceedings of the IEEE*, 63(9), 1278–1308. <https://doi.org/10.1109/PROC.1975.9939>
[^schneier1999audit]: Schneier, B., & Kelsey, J. (1999). Secure Audit Logs to Support Computer Forensics. *ACM Transactions on Information and System Security*, 2(2), 159–176. <https://doi.org/10.1145/317087.317089>
[^sigelman2010dapper]: Sigelman, B. H., Barroso, L. A., Burrows, M., Stephenson, P., Plakal, M., Beaver, D., Jaspan, S., & Shanbhag, C. (2010). *Dapper, a Large-Scale Distributed Systems Tracing Infrastructure.* Google Technical Report dapper-2010-1.
[^sweeney2002kanonymity]: Sweeney, L. (2002). k-Anonymity: A Model for Protecting Privacy. *International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems*, 10(5), 557–570. <https://doi.org/10.1142/S0218488502001648>
