+++
title = 'Deep Dive Part 4: Z3 Formal Verification, the Three-Layer Stack, and Claude Code as Architect'
slug = 'irsb-deep-dive-4-ai-agent-pivot'
date = 2026-03-27T16:00:00-05:00
draft = false
tags = ["irsb", "python", "z3", "formal-verification", "ai-agents", "claude-code", "ai-collaboration", "architecture"]
categories = ["IRSB Deep Dive"]
description = "How Z3 SMT solver replaces LLM-as-a-judge with mathematical proofs, the three-layer IRSB+Moat+Scout stack, and the story of Claude Code as the lead architect across 285 commits."
toc = true
+++

Every AI governance product running today uses some version of LLM-as-a-judge: feed the agent's output to a second model and ask it whether the first model behaved. It is probabilistic reasoning about probabilistic reasoning. The result is a confidence score, not a proof. The IRSB ecosystem took a different path — formal verification using Z3, an SMT solver from Microsoft Research, which can mathematically prove the absence of a constraint violation rather than estimate its likelihood. That distinction matters when an autonomous agent has wallet access and real-world consequences attached to its decisions.

This post is about how that system works, the three-layer stack it sits inside, and the story of building it with Claude Code as architect. Visit the [IRSB Ecosystem](/irsb-ecosystem/) hub for the full series context.

This is Part 4 of the [IRSB Ecosystem Deep Dive](/irsb-ecosystem/) series. [Part 1](/posts/irsb-deep-dive-1-on-chain-enforcement/) covered on-chain enforcement, [Part 2](/posts/irsb-deep-dive-2-evidence-pipeline/) the evidence pipeline, [Part 3](/posts/irsb-deep-dive-3-watchtower-architecture/) the Watchtower architecture.

---

## Z3 Formal Verification: Replacing LLM-as-a-Judge

The `FormalAgentVerifier` is the centrepiece of Moat's trust plane. It receives a `ToolCall` — the agent's intent to do something — and returns a `VerificationReport` with one of three outcomes: `PROVEN_SAFE`, `PROVEN_UNSAFE`, or `UNKNOWN`.

Nine constraints span six categories: `FILE_ACCESS`, `NETWORK`, `COMMAND_EXEC`, `DATA_EXFIL`, `RESOURCE_LIMIT`, and `PERMISSION`. Each constraint is a logical proposition that Z3 either satisfies or refutes. The system is fail-closed: `UNKNOWN` is treated as unsafe. If the solver times out, the call is blocked.

```python
class FormalAgentVerifier:
    def verify(self, tool_call: ToolCall) -> VerificationReport:
        if not self.config.enabled:
            return VerificationReport(tool_call=tool_call, result=VerificationResult.PROVEN_SAFE)

        applicable = self._get_applicable_constraints(tool_call.tool_name)
        violations, proofs, checked = [], [], []

        for constraint in applicable:
            checked.append(constraint.name)
            try:
                is_safe, detail = self._verify_single_constraint(constraint, tool_call)
                if is_safe:
                    proofs.append(f"{constraint.name}: {detail}")
                else:
                    violations.append(f"{constraint.name}: {detail}")
            except Exception as exc:
                violations.append(f"{constraint.name}: verification error — {exc}")

        if violations:
            return VerificationReport(result=VerificationResult.PROVEN_UNSAFE, ...)
        return VerificationReport(result=VerificationResult.PROVEN_SAFE, ...)
```

The loop is deliberately simple. Complexity lives in the per-constraint verifiers, which use Z3's theory of strings, integers, and bit-vectors to construct proofs rather than heuristics.

---

## Path Traversal via Z3 String Theory

The path traversal check is the clearest illustration of what formal verification adds. The question is not "does this path look suspicious?" — it is "can Z3 prove that the strings `..` and `//` do not exist anywhere in this path value?"

```python
def _check_path_traversal_z3(self, params: dict[str, Any]) -> tuple[bool, str]:
    z3 = _get_z3()
    path = str(params.get("path", params.get("file_path", "")))

    solver = z3.Solver()
    solver.set("timeout", self.config.solver_timeout_ms)

    path_var = z3.String("path")
    has_traversal = z3.Or(
        z3.Contains(path_var, z3.StringVal("..")),
        z3.Contains(path_var, z3.StringVal("//")),
    )

    solver.add(path_var == z3.StringVal(path))
    solver.add(has_traversal)

    result = solver.check()
    if result == z3.unsat:
        return True, f"Z3 proved no traversal sequences in '{path}'"
    elif result == z3.sat:
        return False, f"Z3 found traversal sequence in '{path}'"
    else:
        return False, f"Z3 solver returned {result} (fail-closed)"
```

The solver adds two assertions: the path variable equals the actual path, and the path contains a traversal sequence. If Z3 returns `unsat` — meaning no assignment satisfies both constraints simultaneously — the absence of traversal is proven. A regex could be bypassed by encoding tricks. A Z3 proof cannot.

The same approach applies to network constraints (port range verification via integer arithmetic), command execution checks (allowlist membership via set theory), and data exfiltration detection (payload size bounds via bit-vector arithmetic). The choice of theory depends on the domain of the constraint.

---

## The Three-Layer Stack

The full vision is three independently useful layers that together form a complete accountability stack for AI agent transactions.

**Layer 1 — IRSB Protocol.** Cryptographic accountability at the protocol level. Receipts, bonds, disputes, delegation chains, and enforcers. 552 protocol tests. Deployed on Sepolia testnet. Mainnet deployment is planned for Q3 2026. The protocol contracts provide economic security: agents post bonds, violators get slashed, bad actors enter jail. Nothing in Layer 2 or 3 replaces this — they build on top of it.

**Layer 2 — Moat.** Policy-enforced execution. An agent cannot make a network call, write a file, or spend funds without passing through Moat's gateway. Scope policies (which tools an agent may use), budget policies (how much it may spend), and domain policies (which hosts it may contact) are evaluated before execution. The Z3 verifier sits in the trust plane alongside the Cedar policy engine (planned, not yet created), providing formal proof of constraint satisfaction for each tool call.

**Layer 3 — Scout.** Intelligent work brokering. Scout discovers bounties, matches them to capable agents, and routes execution through Moat. It does not execute work — it finds the right worker and ensures the work flows through the accountability stack below.

Each layer can be adopted without the others. A team that wants policy-enforced execution without on-chain receipts can run Moat standalone. A team that wants formal verification without brokering can use the verifier directly. The stack design is composable by intent.

---

## Scout: The Brokering Brain

Scout lives inside the Moat repository (`github.com/jeremylongshore/moat`) as a separate service. Its interface is eight MCP tools, split evenly between capability management and bounty workflow.

```python
TOOL_SCHEMAS = [
    # Core capability tools
    {"name": "capabilities.list",    "description": "List registered capabilities with filters"},
    {"name": "capabilities.search",  "description": "Search capabilities by name/description/tags"},
    {"name": "capabilities.execute", "description": "Execute through policy-enforced gateway"},
    {"name": "capabilities.stats",   "description": "7-day reliability stats and trust signals"},
    # Scout-workflow tools
    {"name": "bounty.discover",      "description": "Search Algora/Gitcoin/Polar/GitHub for bounties"},
    {"name": "bounty.triage",        "description": "Assess bounty feasibility and match to agents"},
    {"name": "bounty.execute",       "description": "Route matched work through Moat gateway"},
    {"name": "bounty.status",        "description": "Track bounty execution and receipt collection"},
]
```

The `bounty.discover` tool aggregates across four platforms: Algora, Gitcoin, Polar, and GitHub Sponsors. `bounty.triage` scores feasibility against registered agent capabilities and returns a match score. `bounty.execute` does not run the work — it packages the matched bounty and agent, routes it through Moat's gateway with appropriate scope and budget policies attached, and returns a gateway receipt.

The Money Agent, which handles payment flows after successful execution, is currently a stub. The trust signal system in `capabilities.stats` tracks 7-day reliability metrics per registered capability, feeding into the triage scoring and eventually into IRSB bond sizing.

---

## The Competitive Moat

The governance landscape for AI agents splits into two camps: Web2 MCP governance tools (Runlayer, Natoma, Acuvity, Lasso) and Web3 intent protocols (CoW Protocol, Across/UMA, AgentKit). Neither has the full picture.

| Dimension | Web2 MCP Governance | Web3 Intent Protocols | IRSB + Moat + Scout |
|---|---|---|---|
| Policy enforcement | Dashboard rules | Smart contract limits | Both + Z3 formal proofs |
| Audit trail | Database logs | On-chain events | Both + evidence bundles |
| Economic security | None | Bonds (some) | Bonds + slashing + jail |
| Agent monitoring | Dashboard alerts | None | Watchtower (automated) |
| Dispute resolution | Manual review | None | Automated + escalation |
| Bounty discovery | None | None | 4 platforms via Scout |

Web2 tools have flexible policy surfaces but no economic stakes and no formal verification. Web3 protocols have economic stakes but no behavioral governance for agents operating above the transaction layer. IRSB closes both gaps simultaneously.

The framework integration roadmap targets six ecosystems across three priority tiers.

| Tier | Framework | Integration Point | Priority |
|---|---|---|---|
| 1 | ElizaOS | Plugin for receipt + bond | High |
| 1 | Safe + Modules | Module for IRSB enforcers | High |
| 2 | AgentKit | CDP integration | Medium |
| 2 | Olas | Service component | Medium |
| 3 | Brian AI | Transaction receipts | Lower |
| 3 | Virtuals | Agent monitoring | Lower |

ElizaOS and Safe are the highest-leverage entry points. ElizaOS has the largest active community building autonomous agents. Safe has the on-chain infrastructure — modules, guards, and multisig governance — that maps cleanly to IRSB's enforcer model.

---

## The Pivot Story

The February 2026 pivot was not gradual. Between February 5 and 10, the project shifted from a generic intent protocol design — competing with Across and UMA on bridging and settlement — to a focused AI agent accountability layer.

The pivot insight was specific: AI agents with wallet access are being deployed without adequate accountability infrastructure. The Across/UMA space already has credible solutions for cross-chain intent settlement. The AI agent space does not have a credible solution for what happens when an agent misbehaves, overspends, or makes a decision that a human stakeholder later disputes.

IRSB's receipt/bond/dispute infrastructure, already designed for on-chain settlement, mapped directly onto this problem. A receipt proves an agent took a specific action. A bond creates economic stakes. A dispute mechanism creates recourse. The protocol did not need to be redesigned — it needed to be aimed at a different target.

The other significant architectural change was the Lit Protocol migration. The original design used Lit Protocol for distributed key management — threshold signatures across Lit nodes for every signing operation. In practice this meant added latency, a hard dependency on Lit node availability, and meaningful operational complexity for every production deployment. Cloud KMS replaced it. Google manages the HSMs, the signing operations are synchronous, and the dependency graph is simpler. The architectural elegance of threshold cryptography was real, but the operational cost was not worth it for the current stage of the project.

---

## Claude Code as Architect

285 commits. 52 days. 6 EIPs implemented. Three repositories built to production standards on Sepolia testnet.

The collaboration model for IRSB followed the same pattern documented in the Wild ecosystem deep dive series: Jeremy Longshore as product owner and human architect, Claude Code as technical lead. The division of responsibilities:

**Jeremy defined:**
- Protocol semantics and economic design
- Integration targets and positioning
- The architectural pivot from generic intents to AI agent accountability
- Non-negotiable safety constraints

**Claude Code decided:**
- Data model specifics and type hierarchies
- Test architecture and adversarial test cases
- Implementation patterns within each service
- Cross-repository consistency and interface contracts

The CLAUDE.md pattern is the binding contract between these two roles. Every service has a CLAUDE.md that defines what the service does, what it does not do, its safety rules, and the scope boundaries the AI implementer must not cross. These files are not documentation — they are operational constraints for the AI. An instruction in CLAUDE.md that says "never execute tool calls without a valid verification report" is enforced across every session.

The adversarial test suite for the formal verifier is a good example of Claude Code operating as genuine technical lead. The test cases were not specified by Jeremy — they were generated by the AI reasoning about attack surfaces: encoding tricks that might bypass path checks, malformed parameter types that could trigger edge cases, timing sequences that could exploit the fail-open path before the verifier initializes. A copilot fills in the implementation. A tech lead thinks adversarially about what it just built.

---

## Regulatory Tailwind and Licensing

The EU AI Act compliance deadline for high-risk AI systems is August 2, 2026. Article 12 requires providers of high-risk AI systems to implement logging mechanisms sufficient to ensure traceability of outputs. IRSB receipts — immutable, on-chain, tied to cryptographic agent identifiers — satisfy this requirement natively. Organizations deploying AI agents in regulated verticals (financial services, healthcare, infrastructure) are looking for accountability infrastructure that does not require custom development. IRSB provides it at the protocol layer.

The licensing structure reflects a deliberate commercial strategy. IRSB is licensed under BUSL-1.1, which restricts commercial use by competing protocols until the change date. That change date is February 17, 2029, when the license converts to MIT. The protocol is commercially protective now, fully open-source later. This is the same pattern used by Uniswap v3 and several other DeFi protocols that needed first-mover protection during the growth phase.

---

## The Full Picture

Four posts, three repositories, one protocol.

- [Part 1: On-Chain Enforcement](/posts/irsb-deep-dive-1-on-chain-enforcement/) — 37 smart contracts, 552 tests, receipt/bond/dispute semantics on Sepolia
- [Part 2: The Evidence Pipeline](/posts/irsb-deep-dive-2-evidence-pipeline/) — evidence bundles, IPFS anchoring, dispute submission flow
- [Part 3: The Watchtower Architecture](/posts/irsb-deep-dive-3-watchtower-architecture/) — automated monitoring, anomaly detection, escalation chains
- Part 4: This post — Z3 formal verification, the three-layer stack, Claude Code as architect

The gap between "AI agents can transact" and "AI agents can transact safely" is the gap IRSB fills — not with promises, but with math, economics, and 37 smart contracts.

---

*Part of the [IRSB Ecosystem](/irsb-ecosystem/) deep dive series. Built with [Claude Code](https://claude.ai/code).*
