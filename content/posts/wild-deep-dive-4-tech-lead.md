+++
title = 'Deep Dive Part 4: Building 10 Production Gems with Claude Code as Tech Lead'
slug = 'wild-deep-dive-4-tech-lead'
date = 2026-03-26T16:00:00-05:00
draft = false
tags = ["wild-ecosystem", "ruby", "claude-code", "ai-collaboration", "software-architecture", "ai-agents"]
categories = ["Wild Ecosystem Deep Dive"]
description = "What it means when the AI makes the architectural decisions. How Claude Code served as tech lead across 10 Ruby gems with approximately 2,924 tests and 60+ canonical docs — read against the LLM-agent and software-engineering-automation literature."
toc = true
bibliography = "citations/wild-citations.bib"
+++

The wild ecosystem set out to build a family of production-grade Ruby gems forming a governed operational-intelligence layer for AI agents. That ecosystem is now complete: ten repositories, approximately 2,924 tests, zero RuboCop offenses, sixty-plus canonical documents, all v1 implementations shipped.

This article is about how that was built, and what a collaboration between a human architect and an AI in the tech-lead seat actually looks like in practice. The relevant literature is moving quickly. Yao and colleagues' ReAct paper[^yao2023react] established the reason-then-act loop as the dominant abstraction for tool-using agents; Schick and colleagues' Toolformer work[^schick2023toolformer] and Wei and colleagues' chain-of-thought work[^wei2022chainofthought] are the immediate predecessors; Park and colleagues' generative-agents study[^park2023generative] demonstrated agent populations sustaining coherent multi-day behaviour; Li's recent survey of LLM-based agent paradigms[^li2024agentparadigms] catalogues the design space; and the SWE-smith line of work on agent-driven software engineering[^yang2025swesmith] documents how rapidly the benchmarks are moving. The wild ecosystem sits inside that trend, not outside it — but it makes deliberate choices about *which* parts of the agent are load-bearing and which parts the infrastructure absorbs.

This is Part 4 of the [Wild Ecosystem Deep Dive](/wild-ecosystem/) series.

---

## The Collaboration Model

The wild ecosystem was not built with Claude Code as a copilot — autocompleting code fragments, implementing features described in natural language, staying within preset guardrails.

Instead, Claude Code served as tech lead: making architecture decisions, choosing implementation patterns, catching its own bugs, testing its own code adversarially, and maintaining cross-repository consistency.

**Jeremy Longshore** operated as product owner and architect. He defined:

- the mission of each repository
- the boundaries (what each repo does and does not do)
- the ten-epic structure for each repo
- the key architectural decisions that needed to be made
- the non-negotiable safety rules for each context

**Claude Code** operated as implementer and technical decision-maker within those constraints. It:

- made sound implementation choices (e.g., should this authorisation check be a constant or a hash?)
- wrote adversarial tests against its own code
- identified and fixed bugs
- maintained patterns across repositories to prevent divergence
- surfaced architectural questions when the constraints left room for multiple valid approaches

This model flips the typical AI-in-development relationship. Jeremy was not directing Claude Code line by line. Claude Code was not waiting for approval on every design choice. They were collaborating as peers with clear ownership. The pattern is consistent with the *agent-as-tool-using-reasoner* abstraction Yao and colleagues introduced[^yao2023react] but extended to a higher unit of work: the agent reasons about *architecture* rather than only about the next tool call. Li's survey notes that this kind of long-horizon decision-making is where current agent stacks struggle most[^li2024agentparadigms]; the wild approach addresses it by constraining the architectural surface to the bounded design space the contract (the `CLAUDE.md` file) declares.

---

## The Numbers: What Actually Got Built

| Gem | Tests | Purpose |
|-----|-------|---------|
| wild-capability-gate | 224 | Cross-cutting access control |
| wild-rails-safe-introspection-mcp | 468 | Safe, read-only Rails introspection via MCP |
| wild-admin-tools-mcp | 439 | Governed admin operations via MCP |
| wild-session-telemetry | 325 | Privacy-first telemetry collection |
| wild-transcript-pipeline | 200+ | Transcript normalisation with PII redaction |
| wild-gap-miner | 276 | Gap analysis from telemetry data |
| wild-hook-ops | 247 | Hook lifecycle management |
| wild-permission-analyzer | 217 | Static permission auditing |
| wild-test-flake-forensics | 277 | Flake detection + root-cause analysis |
| wild-skillops-registry | 251 | Skills registry + coordination |
| **Total** | **~2,924** | **10 repos, 10 epics each, 60+ canonical docs** |

All written to pass zero RuboCop offenses. All with explicit safety rules documented and tested. All with clear data contracts and cross-repo dependencies mapped.

---

## What "AI as Tech Lead" Actually Means

This model is not about code generation. It is about technical decision-making under constraints.

Consider the capability gate — the access-control layer that guards privileged tool access across the ecosystem. When Jeremy defined the mission ("answer whether this agent can call this tool in this context"), Claude Code had to decide:

- what is the shape of a capability ID? Is it a string like `"admin.job.retry"`, or is there a structured format?
- how are policies stored? In memory, in YAML, in a DSL?
- what is the runtime interface? Do calls check a constant hash, call a method on a gate object, or something else?

Jeremy provided the safety rules: authorisation must be logged, denials must never propagate as exceptions, configuration must freeze after startup. Within those constraints, Claude Code made implementation choices.

These choices had downstream effects. When `wild-admin-tools-mcp` needed to integrate the capability gate, the decisions Claude Code made in the gate repo directly shaped the integration pattern. When `wild-rails-safe-introspection-mcp` followed, it inherited those patterns. The cross-repo consistency property is exactly what Bernstein and colleagues' Orleans virtual-actor work argues for in a distributed-systems setting[^bernstein2014orleans]: when the *state machine* is consistent across instances, downstream complexity drops sharply.

That consistency across ten independent repositories did not happen by accident. It happened because Claude Code maintained internal coherence — asking itself *am I following the pattern established in the capability gate?* and *will future implementers understand why I chose this way?*

---

## The CLAUDE.md Coordination Mechanism

Each repository has its own `CLAUDE.md` file. These files are not documentation — they are contracts.

Example from `wild-admin-tools-mcp`:

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

The `CLAUDE.md` file is the binding contract between Jeremy (as architect) and Claude Code (as implementer). It prevents scope creep. It enforces consistency. It makes the constraints explicit so they can be tested. Part 2 of this series treats the contract pattern in detail; in short, the contract is positioned at the start of the prompt so that the long-context attention curve Liu and colleagues characterised[^liu2024lostmiddle] does not degrade it over a long session.

---

## Cross-Repo Dependency Management

Ten independent repositories need consistent patterns. The wild ecosystem used three mechanisms.

### 1. Beads (task tracking)

Each repository uses Beads for task tracking. All ten repositories follow the same structure:

- ten epics per repo (named for outcomes, not technical nouns)
- child tasks under each epic with clear acceptance criteria
- explicit dependency blocks between tasks and across repositories
- annotations that read like operator progress notes, not machine scraps

Moving from one repo to another felt natural. The task structure was familiar. The acceptance-criteria patterns were consistent.

### 2. Canonical Documentation in `000-docs/`

Every repo has a `000-docs/` directory with filed documents following `/doc-filing` conventions:

- `001-PP-PLAN-repo-blueprint.md` (mission, boundaries, architecture)
- `002-PP-PLAN-epic-build-plan.md` (ten-epic breakdown)
- `003-TQ-STND-privacy-model.md` (privacy guarantees)
- `004-AT-ADEC-architecture-decisions.md` (why things are shaped this way)

Understanding a new repo required reading predictable documents in a predictable order. The cognitive load for moving between repositories was minimal.

### 3. Shared Notes

When a pattern emerged that applied across multiple repos, it was documented once and linked from affected repos. When multiple repos needed to validate configuration, a shared note on *Configuration Freezing Patterns* was filed. Each repo referenced it, preventing copy-paste divergence. The pattern parallels the Orleans *grain* abstraction Bernstein and colleagues described for distributed systems[^bernstein2014orleans]: the canonical definition lives in one place, and every consumer holds a reference, not a copy.

---

## Quality Metrics: What a Human Reviewer Would Find

Zero RuboCop offenses across all ten repositories is notable but expected. More interesting are the quality choices.

### Adversarial Testing

Every safety rule gets tested by code that tries to break it. The methodology follows the *language-model red-teaming* pattern Perez and colleagues introduced at EMNLP 2022[^perez2022redteam]: the system under test is also a participant in the test design, and the tests deliberately target the rules the system is supposed to enforce.

Example from `wild-admin-tools-mcp`: the safety rule is *never bypass the capability gate*. The test creates a scenario where an action is configured as allowed, but the capability gate denies it for a specific caller. The test verifies that even though the action is configured, the gate denial is respected.

### Privacy Invariant Tests

The `wild-session-telemetry` library claims "twenty-two field patterns must never be stored." The test creates an event with all twenty-two forbidden fields, feeds it to the ingestion layer, and verifies that after storage, none of those fields exist in the stored record.

### Data Contract Tests

Each repo that exports data has tests verifying the output contract. Example from `wild-gap-miner`: the export schema specifies that gap severity is always in `[0.0, 1.0]`. The test creates gaps with invalid severity (e.g., 1.5, -0.1) and verifies that the export layer rejects them.

### Cross-Repo Integration Tests

When `wild-gap-miner` depends on output from `wild-session-telemetry` and `wild-transcript-pipeline`, integration tests create realistic exports from both upstream repos, feed them to the gap-miner, and verify that analysis runs correctly. These tests prevent contract drift — the same failure mode the SWE-smith authors observed in agent-driven software-engineering benchmarks, where contract changes upstream silently invalidate downstream agent behaviour[^yang2025swesmith].

---

## What This Changes

The developer becomes architect. The AI handles implementation depth.

In a traditional model, the architect specifies features, and the developer implements them. In this model, Jeremy specified constraints and outcomes, and Claude Code made the technical decisions that transformed those constraints into working, tested, documented code.

The implications:

1. **Architectural leverage increases.** One architect can oversee ten repositories with thousands of tests because the AI is making sound decisions within specified constraints — not asking for permission on every detail. Brooks' 1987 *No Silver Bullet* argument cautioned against expecting any single tool to deliver an order-of-magnitude productivity improvement[^brooks1987nosilverbullet]; the more interesting question is whether a *collaboration model* can. The evidence here suggests yes, but the gain is in the architect's leverage rather than in raw code-writing speed.

2. **Code review focus shifts.** Instead of reviewing line-by-line implementations, review focuses on whether constraints were honoured, whether safety rules were tested, whether documentation is clear.

3. **Consistency improves.** Because the AI makes decisions within constraints, patterns emerge naturally. Divergence has to be intentional, not accidental.

4. **Knowledge transfer becomes feasible.** Documentation-first execution means future implementers (human or AI) can read the decisions and understand the reasoning.

---

## Practical Takeaways: How to Replicate This

### 1. Define the CLAUDE.md template

Create a standard `CLAUDE.md` structure that every repo follows. Include mission, scope, non-goals, directory layout, build commands, safety rules (numbered, binding, tested), canonical-doc index, and task-tracking rules. Make it a contract, not guidance.

### 2. Use the 10-epic structure

Every repository starts with the same epic breakdown:

- Epic 1: Foundations (schema, configuration, core interfaces)
- Epics 2–9: Feature areas (each focused and complete)
- Epic 10: Quality (adversarial testing, documentation, release)

This forces completeness. A repo that skips Epic 10 cannot ship.

### 3. Track tasks with explicit dependencies

Use Beads or an equivalent that enforces dependency blocks between tasks, cross-repo dependency visibility, narrative annotations, and no task closure without evidence.

### 4. Document decisions as you build

When a question arises ("should we store denied capabilities in the gate log?"), answer it in a filed document, not just in code comments. Use numbered documents with category and type codes. Maintain an INDEX.

### 5. Establish clear data contracts

When a repository exports data, the output schema is a living document: filed, typed, versioned, and validated by integration tests.

### 6. Test safety rules adversarially

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

These tests are the safety ratchet. They prevent regressions. The methodology — *adversarial tests as a first-class verification artefact* — follows directly from Perez and colleagues' language-model red-teaming work[^perez2022redteam] and from Park and colleagues' demonstration that agent populations require explicit behavioural constraints to remain coherent over long horizons[^park2023generative].

---

## The Reality Check

Building ten production repositories with this model required:

- clear architectural vision upfront (the master blueprint)
- detailed per-repo planning before any code (the `CLAUDE.md` files)
- disciplined task tracking (Beads, with explicit dependencies)
- aggressive testing (~300 tests per repo on average)
- extensive documentation (sixty-plus filed documents)

This is not a lightweight approach. It is intentional, documented, and exhaustive. The literature on long-horizon agent behaviour is consistent on this point: without explicit structural anchors, agent behaviour drifts[^liu2024lostmiddle][^sharma2023sycophancy]; with them, it composes[^park2023generative].

The result is what most teams do not achieve: ten independent repositories that work together cohesively, with zero accidental divergence, clear contracts, testable safety rules, and documentation that future implementers can actually read and understand.

---

## Summary

Claude Code as tech lead works when:

1. the architect defines missions, boundaries, and non-negotiable rules
2. the implementer makes sound technical decisions within those constraints
3. the coordination layer (`CLAUDE.md`, Beads, canonical docs) makes decisions explicit and testable
4. safety is treated as a first-class concern, not an afterthought

The result is not faster development. It is *better* development: less divergence, more consistency, more testable, more documentable.

The wild ecosystem is an existence proof that this model scales to ten independent repositories, multiple layers of abstraction, cross-repo dependencies, and production-grade quality standards.

What changed is not raw AI capability. It is the collaboration model. Human architect, AI tech lead, structured constraints, explicit contracts, rigorous testing — together they produce something neither could build alone. Brooks' framing of the *essence* of software engineering as the irreducible difficulty of getting the design right[^brooks1987nosilverbullet] still applies; what has shifted is *who can hold which part of the essence*.

---

## The Full Series

- **Part 1**: [The Safety Architecture](/posts/wild-deep-dive-1-safety-architecture/) — defence in depth, adversarial testing, hard safety ceilings.
- **Part 2**: [CLAUDE.md — Human–AI Collaboration Pattern](/posts/wild-deep-dive-2-claude-md/) — per-repo contracts that prevent scope creep and enforce safety.
- **Part 3**: [The Observability Loop](/posts/wild-deep-dive-3-observability/) — telemetry, transcripts, and gap mining as a self-improving feedback loop.
- **Part 4**: This article — Claude Code as tech lead across ten production gems.

---

*Part of the [Wild Ecosystem](/wild-ecosystem/) — 10 Ruby gems for governed AI agent operations in production Rails. Built with [Claude Code](https://claude.ai/code).*

---

## References

[^bernstein2014orleans]: Bernstein, P. A., Bykov, S., Geller, A., Kliot, G., & Thelin, J. (2014). *Orleans: Distributed Virtual Actors for Programmability and Scalability.* Microsoft Research Technical Report MSR-TR-2014-41.
[^brooks1987nosilverbullet]: Brooks, F. P. (1987). No Silver Bullet — Essence and Accidents of Software Engineering. *IEEE Computer*, 20(4), 10–19. <https://doi.org/10.1109/MC.1987.1663532>
[^li2024agentparadigms]: Li, X. (2024). A Review of Prominent Paradigms for LLM-Based Agents: Tool Use, Planning (Including RAG), and Feedback Learning. *COLING.* arXiv:2406.05804.
[^liu2024lostmiddle]: Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2023). Lost in the Middle: How Language Models Use Long Contexts. *Transactions of the Association for Computational Linguistics*, 12, 157–173. <https://doi.org/10.1162/tacl_a_00638>
[^park2023generative]: Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative Agents: Interactive Simulacra of Human Behavior. *UIST.* <https://doi.org/10.1145/3586183.3606763>
[^perez2022redteam]: Perez, E., Huang, S., Song, F., Cai, T., Ring, R., Aslanides, J., Glaese, A., McAleese, N., & Irving, G. (2022). Red Teaming Language Models with Language Models. *EMNLP.* <https://doi.org/10.18653/v1/2022.emnlp-main.225>
[^schick2023toolformer]: Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). Toolformer: Language Models Can Teach Themselves to Use Tools. *NeurIPS.* arXiv:2302.04761.
[^sharma2023sycophancy]: Sharma, M., Tong, M., Korbak, T., Duvenaud, D., Askell, A., Bowman, S. R., et al. (2024). Towards Understanding Sycophancy in Language Models. *ICLR.* arXiv:2310.13548.
[^wei2022chainofthought]: Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q., & Zhou, D. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. *NeurIPS.* arXiv:2201.11903.
[^yang2025swesmith]: Yang, J., Lieret, K., Jimenez, C. E., Wettig, A., Khandpur, K., Zhang, Y., Hui, B., Press, O., Schmidt, L., & Yang, D. (2025). *SWE-smith: Scaling Data for Software Engineering Agents.* arXiv:2504.21798.
[^yao2023react]: Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. *ICLR.* arXiv:2210.03629.
