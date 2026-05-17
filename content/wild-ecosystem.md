+++
title = 'Wild Ecosystem'
date = 2026-03-26T12:00:00-05:00
menu = 'main'
weight = 15
bibliography = "citations/wild-citations.bib"
+++

# The Wild Ecosystem

**Ten Ruby gems. Approximately 2,924 tests. One mission: make AI agents structurally safe in production Rails.**

The wild ecosystem is a family of open-source Ruby gems that together implement a governed operational-intelligence layer for AI-assisted development workflows. Every gem treats safety as a structural property of the infrastructure rather than a behavioural property of the agent: read-only where mutation is unnecessary, audited everywhere, bounded by hard ceilings that configuration cannot override.

**Paperback edition (PDF, 42 pages):** [/research-papers/wild-ecosystem-paperback.pdf](/research-papers/wild-ecosystem-paperback.pdf) — hub + four deep dives concatenated, unified bibliography, print-ready.

Built collaboratively with [Claude Code](https://claude.ai/code).

---

## The Problem

Large language model agents are increasingly granted tool access to production systems. The function-calling pattern that Schick and colleagues demonstrated with Toolformer[^schick2023toolformer] and that Yao and colleagues generalised into the reason-then-act loop of ReAct[^yao2023react] is now mediated by the Model Context Protocol[^anthropic2024mcp], an open specification for connecting language models to external tools and data sources. Li's recent survey of LLM-based agent paradigms[^li2024agentparadigms] documents how rapidly that surface has expanded: tool invocation, planning, retrieval, and feedback learning are now standard components of production agent stacks.

Most production implementations of this pattern grant agents unrestricted access — raw consoles, arbitrary queries, no audit trail. The failure modes are well documented. A single mis-issued tool call mutates data the operator did not intend to touch. An expensive query saturates a replica. Worse, Greshake and colleagues showed that adversarial content reachable through ordinary tool use can hijack the agent's decision loop entirely[^greshake2023indirect].

Wild takes a different position: **governed, audited, bounded access with hard safety ceilings that cannot be overridden.** The safety argument does not depend on the agent being well-behaved. It depends on the infrastructure foreclosing the unsafe paths in the first place — the deny-by-default posture that Saltzer and Schroeder named *fail-safe defaults* in their 1975 design-principles paper[^saltzer1975protection], expressed through the modern vocabulary of attribute-based access control[^hu2014abac].

---

## Architecture

Five layers, ten gems, with clear boundaries between each.

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

Governed admin operations via MCP. Nineteen actions across background jobs, cache, and feature flags. Every mutation requires two-phase nonce confirmation (SHA-256 bound to action, parameters, and caller identity) — a structural analogue of the two-phase commit protocol Gray formalised in 1978[^gray1978notes]. Dry-run previews carry zero side effects. Blast-radius caps enforce hard ceilings.

</div>
</div>

### Layer 2 — Governed Access

**[wild-capability-gate](https://github.com/jeremylongshore/wild-capability-gate)** | 224 tests

Cross-cutting access control. Defines what capabilities exist, who can use them, and which prerequisites must be met. Fail-closed semantics (errors produce denial, never accidental permission, following Saltzer and Schroeder's *fail-safe defaults*[^saltzer1975protection]). No implicit grants. Configuration is frozen after startup. Complete audit trail of every evaluation. The data model mirrors the ABAC vocabulary in NIST SP 800-162[^hu2014abac] rather than the role-based pattern of Sandhu and colleagues[^sandhu1996rbac], because attribute-keyed policies compose more cleanly across the ten-gem ecosystem than role-keyed ones would.

### Layer 3 — Observability & Learning Loop

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1.5rem; margin-bottom: 2rem;">
<div>

**[wild-session-telemetry](https://github.com/jeremylongshore/wild-session-telemetry)** | 325 tests

Privacy-first telemetry collection. Twenty-two hardcoded forbidden fields. Per-event-type metadata allowlists. Fire-and-forget semantics — telemetry failures never break upstream tools, following Armstrong's *let-it-crash* fault-containment discipline from the Erlang OTP tradition[^armstrong2003reliable]. Aggregation engine with pattern detection.

</div>
<div>

**[wild-transcript-pipeline](https://github.com/jeremylongshore/wild-transcript-pipeline)** | 200+ tests

Transcript normalisation with PII redaction. Three format adapters (Claude Code JSONL, MCP protocol logs, generic JSON). Strips emails, IP addresses, API keys, AWS credentials, GitHub tokens, and absolute paths. Privacy posture aligns with the *minimum information* principle Sweeney articulated in her k-anonymity work[^sweeney2002kanonymity]: collect what is needed for analysis and discard the rest before storage. Zero runtime dependencies.

</div>
<div>

**[wild-gap-miner](https://github.com/jeremylongshore/wild-gap-miner)** | 276 tests

Gap analysis from telemetry and transcript data. Six analyzers: denial rate, failure rate, latency outliers, low utilisation, poor coverage, recurring patterns. Severity scoring with actionable recommendations. The pipeline pattern (collect → normalise → analyse) mirrors the trace-then-aggregate architecture Sigelman and colleagues described in Google's Dapper paper[^sigelman2010dapper]. Pure Ruby stdlib.

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

Static analysis of capability-gate configurations before deployment. Six analyzers: consistency, risk, prerequisites, coverage, orphans, shadows. Catches permission-model mistakes before they reach production — addressing the comprehension gap Felt and colleagues documented in their work on Android permission systems[^felt2012android].

</div>
<div>

**[wild-test-flake-forensics](https://github.com/jeremylongshore/wild-test-flake-forensics)** | 277 tests

Flaky-test detection with confidence-scored root-cause hypotheses. Supports RSpec JSON, JUnit XML, minitest. History tracking with trend detection (worsening, stable, improving). Triage reports with severity scoring.

</div>
</div>

### Layer 5 — Skill Governance

**[wild-skillops-registry](https://github.com/jeremylongshore/wild-skillops-registry)** | 251 tests

Skills registry and coordination control plane. Lifecycle management (draft → active → deprecated → retired), health tracking with staleness detection, full-text search with relevance scoring, version management with changelogs. The coordination layer that ties the ecosystem together.

---

## Safety Innovations

**Allowlist-first access.** Models must be explicitly permitted. Unknown models and blocked models produce identical denial responses, foreclosing the enumeration oracles described in the security-engineering literature on covert side channels[^saltzer1975protection].

**Read-only by design.** No write paths exist in the introspection tools. No `eval`, no `constantize`, no dynamic method dispatch on user input. Enforced at adapter, guard, and audit layers independently — the defence-in-depth posture that the Saltzer–Schroeder principles call *complete mediation*[^saltzer1975protection].

**Two-phase nonce confirmation.** Admin mutations bind a SHA-256 nonce to the specific action, parameters, and caller identity. Single-use. Time-limited. Opaque failure reasons prevent oracle attacks. The two-phase shape mirrors Gray's commit protocol[^gray1978notes]; the cryptographic binding follows the integrity-token construction Haber and Stornetta proposed for time-stamped documents[^haber1991timestamp].

**Hard ceilings.** Row caps (default 50, ceiling 1,000) and query timeouts (default 5 s, ceiling 30 s) that cannot be overridden by configuration. Exceeding the cap raises an error rather than silently truncating — a deliberate departure from defaults that fail open.

**Adversarial testing.** SQL injection payloads, Ruby code-execution attempts, null-byte injection, prompt injection via model names — all verified as inert data. Database state snapshots before and after each test prove zero mutations. The methodology follows the language-model-vs-language-model red-teaming pattern Perez and colleagues introduced at EMNLP 2022[^perez2022redteam] and the indirect-prompt-injection threat model Greshake and colleagues catalogued at AISec 2023[^greshake2023indirect].

**Privacy-first telemetry.** Hardcoded forbidden field lists (not configurable). Per-event-type metadata allowlists. PII is never collected, not merely *redacted after the fact* — consistent with the audit-log integrity model Schneier and Kelsey described for forensic settings[^schneier1999audit].

---

## Built with Claude Code

The wild ecosystem was designed and implemented collaboratively with [Claude Code](https://claude.ai/code), Anthropic's AI coding agent. Claude Code served as technical lead — making architectural decisions, implementing all ten gems, writing adversarial test suites, and maintaining cross-repo consistency.

The coordination mechanism is `CLAUDE.md`, a per-repo file that acts as a binding contract between human architect and AI implementer. Safety rules, scope boundaries, and non-negotiable constraints are enforced through this pattern. The design responds to the *lost in the middle* effect Liu and colleagues documented in long-context language models[^liu2024lostmiddle]: when the implementer's effective attention degrades over long sessions, the contract has to be load-bearing at the beginning of every interaction.

**Deep dive series:**
- [Part 1: The Safety Architecture](/posts/wild-deep-dive-1-safety-architecture/)
- [Part 2: CLAUDE.md — Human-AI Collaboration Pattern](/posts/wild-deep-dive-2-claude-md/)
- [Part 3: The Observability Loop](/posts/wild-deep-dive-3-observability/)
- [Part 4: Claude Code as Tech Lead](/posts/wild-deep-dive-4-tech-lead/)

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

## Further reading

A consolidated bibliography for the wild ecosystem — covering capability-based access control, audit-log integrity, language-model agent architectures, indirect prompt injection, fault containment, and privacy engineering — is maintained at [/citations/](/citations/) (BibTeX + per-source verification metadata).

---

*Built with [Claude Code](https://claude.ai/code). Governed by design.*

---

## References

[^anthropic2024mcp]: Anthropic (2024). *Model Context Protocol Specification.* <https://modelcontextprotocol.io/>
[^armstrong2003reliable]: Armstrong, J. (2003). *Making Reliable Distributed Systems in the Presence of Software Errors.* PhD thesis, Royal Institute of Technology (KTH), Stockholm.
[^felt2012android]: Felt, A. P., Ha, E., Egelman, S., Haney, A., Chin, E., & Wagner, D. (2012). Android Permissions: User Attention, Comprehension, and Behavior. *Symposium on Usable Privacy and Security (SOUPS).* <https://doi.org/10.1145/2335356.2335360>
[^gray1978notes]: Gray, J. (1978). Notes on Database Operating Systems. In Bayer, R., Graham, R. M., & Seegmüller, G. (Eds.), *Operating Systems: An Advanced Course* (LNCS 60, pp. 393–481). Springer.
[^greshake2023indirect]: Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. (2023). Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection. *AISec '23.* <https://doi.org/10.1145/3605764.3623985>
[^haber1991timestamp]: Haber, S., & Stornetta, W. S. (1991). How to Time-Stamp a Digital Document. *Journal of Cryptology*, 3(2), 99–111. <https://doi.org/10.1007/BF00196791>
[^hu2014abac]: Hu, V. C., Ferraiolo, D. F., Kuhn, D. R., Schnitzer, A., Sandlin, K., Miller, R., & Scarfone, K. (2014). *Guide to Attribute Based Access Control (ABAC) Definition and Considerations.* NIST Special Publication 800-162. <https://doi.org/10.6028/NIST.SP.800-162>
[^li2024agentparadigms]: Li, X. (2024). A Review of Prominent Paradigms for LLM-Based Agents: Tool Use, Planning (Including RAG), and Feedback Learning. *COLING.* arXiv:2406.05804.
[^liu2024lostmiddle]: Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2023). Lost in the Middle: How Language Models Use Long Contexts. *Transactions of the Association for Computational Linguistics*, 12, 157–173. <https://doi.org/10.1162/tacl_a_00638>
[^perez2022redteam]: Perez, E., Huang, S., Song, F., Cai, T., Ring, R., Aslanides, J., Glaese, A., McAleese, N., & Irving, G. (2022). Red Teaming Language Models with Language Models. *EMNLP.* <https://doi.org/10.18653/v1/2022.emnlp-main.225>
[^saltzer1975protection]: Saltzer, J. H., & Schroeder, M. D. (1975). The Protection of Information in Computer Systems. *Proceedings of the IEEE*, 63(9), 1278–1308. <https://doi.org/10.1109/PROC.1975.9939>
[^sandhu1996rbac]: Sandhu, R. S., Coyne, E. J., Feinstein, H. L., & Youman, C. E. (1996). Role-Based Access Control Models. *IEEE Computer*, 29(2), 38–47. <https://doi.org/10.1109/2.485845>
[^schick2023toolformer]: Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). Toolformer: Language Models Can Teach Themselves to Use Tools. *NeurIPS.* arXiv:2302.04761.
[^schneier1999audit]: Schneier, B., & Kelsey, J. (1999). Secure Audit Logs to Support Computer Forensics. *ACM Transactions on Information and System Security*, 2(2), 159–176. <https://doi.org/10.1145/317087.317089>
[^sigelman2010dapper]: Sigelman, B. H., Barroso, L. A., Burrows, M., Stephenson, P., Plakal, M., Beaver, D., Jaspan, S., & Shanbhag, C. (2010). *Dapper, a Large-Scale Distributed Systems Tracing Infrastructure.* Google Technical Report dapper-2010-1.
[^sweeney2002kanonymity]: Sweeney, L. (2002). k-Anonymity: A Model for Protecting Privacy. *International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems*, 10(5), 557–570. <https://doi.org/10.1142/S0218488502001648>
[^yao2023react]: Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. *ICLR.* arXiv:2210.03629.
