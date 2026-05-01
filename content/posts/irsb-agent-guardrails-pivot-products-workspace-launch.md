+++
title = 'IRSB Agent Guardrails Pivot, Products Workspace Launch, and the Pitch Deck Sprint'
slug = 'irsb-agent-guardrails-pivot-products-workspace-launch'
date = 2026-02-09T10:00:00-06:00
draft = false
tags = ["irsb", "strategy", "ai-agents", "pitch-deck", "eip-7702", "products", "marketplace", "bounties"]
categories = ["Development Journey"]
description = "IRSB pivots from generic intent receipts to AI agent guardrails with a pitch doc, framework target map, and delegation contracts. A new products repo launches with marketplace integration and anti-chargeback tooling. Bounties gets a README rewrite."
+++

Thirteen commits across three repos. The biggest shift wasn't code — it was strategic positioning. IRSB went from "intent receipts and solver bonds" to "on-chain guardrails for AI agents" in a single day.

## The Guardrails Pivot

IRSB had been positioned as a general-purpose intent settlement protocol. The contracts worked. The tests passed. But the pitch was abstract — "receipts for solver execution" doesn't make anyone's eyes light up.

The pivot reframed everything around a concrete problem: AI agents with wallet access and no spending controls. Every major agent framework (AgentKit, ElizaOS, Olas, Virtuals) gives agents the ability to sign transactions. None of them answer the question: what happens when the agent overspends?

The pitch doc structured the argument in three layers:

1. **Policy enforcement** — EIP-7702 delegation contracts with five enforcers (spend limits, nonce ordering, recipient allowlists, time windows, value caps)
2. **Execution receipts** — Cryptographic proof of what the agent actually did, stored on-chain and queryable
3. **Automated monitoring** — A watchtower service that detects policy violations in real-time and can freeze the agent's delegation

The framework target map identified six integration opportunities. Each framework has a different plugin/extension model, and the map documented the specific hook points where IRSB's policy layer would slot in:

| Framework | Hook Point | Integration Complexity |
|-----------|-----------|----------------------|
| AgentKit | Tool execution callback | Low — single wrapper function |
| ElizaOS | Action handler middleware | Medium — requires plugin registration |
| Olas | Service component interface | Medium — new component type |
| Virtuals | Transaction interceptor | High — custom EVM module |
| Brian AI | Intent resolver plugin | Low — standard plugin API |
| Safe | Guard module | Low — well-documented module pattern |

The map also scored each framework by market presence (number of deployed agents, monthly active developers) and technical fit (EVM-native vs. abstracted, custody model, existing policy capabilities). AgentKit and Safe ranked highest on both axes — AgentKit because of Coinbase's distribution, Safe because every Safe account already has a module system that IRSB can slot into directly.

### EIP-7702 Deprecation Decision

The delegation contracts were originally built on EIP-7702 (account delegation). The pitch doc included a note deprecating the EIP-7702 integration path in favor of a simpler proxy pattern. EIP-7702 requires the delegating account to sign a specific authorization, which means the agent needs the user's signature before it can act. The proxy pattern inverts this — the user deploys a proxy once, and the agent operates within the proxy's policy constraints without needing per-transaction authorization.

This was a pragmatic decision, not a philosophical one. EIP-7702 is elegant but adds a UX step that makes integration harder. The proxy pattern is less pure but ships faster. And in the context of a pitch to agent framework teams, "deploy once, agents operate within constraints" is a much easier story to tell than "agents request authorization for each new delegation scope."

### Public Positioning

Two public artifacts came out of the pivot. A Twitter thread walking through the gap analysis — "every framework gives agents wallets, none give agents guardrails" — got the core message out in 280-character chunks. The thread structured the argument as: problem (agents overspend), why existing solutions fail (multisig adds latency, spending limits are static), and how IRSB differs (dynamic policy enforcement with on-chain receipts).

The EthResearch post went deeper with the technical specification for the three-layer architecture. It included Mermaid sequence diagrams showing the full transaction flow from agent intent through policy evaluation to on-chain execution, a comparison table against existing approaches (Safe modules, Gnosis spending limits, custom multisig patterns), and a section on the formal verification properties that the policy layer guarantees.

## Products Workspace Launch

A new `products` repo launched with marketplace integration tooling. The repo contains:

- **Product audit framework** — A checklist-based evaluation of each product in the Intent Solutions portfolio, scoring on documentation completeness, deployment readiness, and integration complexity
- **Anti-chargeback checklist** — Stripe-specific guidance for digital product sales: webhook verification, receipt generation, delivery confirmation, and dispute evidence templates
- **Agent-setup skill** — A Claude Code skill that scaffolds a new agent project with the standard Intent Solutions structure: FastAPI service, MCP tool definitions, Firestore persistence, and Cloud Run deployment config

The marketplace integration connects to the existing claude-code-plugins infrastructure. Products listed in the audit get a marketplace entry with pricing, demo links, and integration guides.

The agent-setup skill deserves a note. It generates a complete project scaffold in about 15 seconds: `pyproject.toml` with FastAPI and MCP dependencies, a `Dockerfile` with multi-stage build, a `cloudbuild.yaml` for Cloud Run deployment, a `tools.py` with three example MCP tool definitions, and a `README.md` with quickstart instructions. The scaffold is opinionated — it assumes Firestore for persistence, Cloud Run for hosting, and the MCP protocol for agent communication. These opinions are based on the stack that every other Intent Solutions project uses, which means debugging knowledge transfers across projects.

## Bounties README Rewrite

The contributions repo (renamed from `bounties` in April 2026) got a single commit: a complete README rewrite. The old README was a bullet list of tracker features. The new one positions the contribute-system as a competitive intelligence tool — not just "find paid issues" but "evaluate expected value, track competition, and optimize submission timing."

The rewrite structured the README around three user workflows: discovery (finding bounties across Algora, GitHub, and CSV imports), qualification (EV scoring based on prize, competition count, deadline proximity, and skill match), and execution (evidence gates, submission templates, and post-submission tracking). Each workflow has its own section with concrete examples rather than abstract feature descriptions.

The EV scoring formula is the part that makes the bounty system more than a tracker. Instead of listing bounties by prize amount (which is what every other tracker does), it ranks by expected value: `EV = prize * P(win) - estimated_hours * hourly_rate`. The `P(win)` estimate factors in competition count, deadline proximity (less competition near deadline), and historical win rate for similar bounty types. This turns bounty hunting from "grab the biggest prize" into "work on the highest-EV opportunity."

## What I Learned

**Strategic positioning is engineering work.** The guardrails pivot didn't change a single line of Solidity. But it changed every document, every pitch, and every integration conversation. The same contracts serve a different market when you reframe what problem they solve.

**Kill your elegant abstractions.** EIP-7702 was technically superior to the proxy pattern. It was also harder to integrate, harder to explain, and harder to demo. The proxy pattern shipped. Sometimes "less pure but works today" beats "more elegant but ships next quarter."

**Public artifacts force clarity.** Writing a Twitter thread about the guardrails gap required distilling the pitch to its essence. If you can't explain the problem in 280 characters, you don't understand the problem well enough. The EthResearch post required the opposite — enough technical depth that protocol researchers would engage rather than dismiss. Both exercises improved the pitch doc itself.

**Related Posts:**
- [IRSB v1.0.0 Release Prep: Security Audit Scaffold and Mobile UX](/posts/irsb-v100-release-security-audit-mobile-ux/)
- [IRSB Go-to-Market Sprint: Sepolia Deployment, TypeScript SDK, and Subgraph](/posts/irsb-go-to-market-sprint-sepolia-sdk-subgraph/)
- [IRSB Four Releases in One Day, Perception Topic Watchlist, and Hustle Session Cookies](/posts/irsb-four-releases-one-day-perception-watchlist-hustle-cookies/)
