+++
title = 'IRSB Ecosystem'
date = 2026-03-27T12:00:00-05:00
menu = 'main'
weight = 16
+++

# The IRSB Ecosystem

**3 layers. 37 contracts. ~1,200 tests. One mission: make AI agent transactions cryptographically accountable.**

The IRSB ecosystem is a three-layer stack — protocol, policy, and brokering — that together form the first on-chain accountability layer for AI agent work. Every transaction produces an immutable receipt. Every solver posts a bond. Every violation triggers automated enforcement.

Built collaboratively with [Claude Code](https://claude.ai/code).

---

## The Problem

AI agents are getting wallet access. Every major framework — AgentKit, ElizaOS, Olas, Virtuals, Brian AI, Safe — gives agents the ability to sign transactions. None of them answer the question: **what happens when the agent does something wrong?**

| Framework | Spend Limits | Execution Receipts | Monitoring | Dispute Resolution |
|-----------|:---:|:---:|:---:|:---:|
| Coinbase AgentKit | — | — | — | — |
| ElizaOS | — | — | — | — |
| Olas | — | — | — | — |
| Virtuals Protocol | — | — | — | — |
| Brian AI | — | — | — | — |
| Safe + Modules | — | — | — | — |
| **IRSB + Moat** | **On-chain** | **On-chain** | **Watchtower** | **Automated** |

Soft reputation systems require trusting someone. IRSB replaces trust with math and economics.

---

## Architecture

Three layers, clear separation of concerns.

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: Scout — Intelligent Brokering                     │
│  Discovers bounties (Algora/Gitcoin/Polar/GitHub)           │
│  Matches agents · Routes through Moat · Collects receipts   │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: Moat — Policy-Enforced Execution                  │
│  Scope policies · Budget policies · Domain allowlists       │
│  Default-deny gateway · Z3 formal verification              │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: IRSB Protocol — Cryptographic Accountability      │
│  Receipts · Bonds · Disputes · Delegation · Enforcers       │
│  11 contracts deployed on Sepolia                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Layer 1: IRSB Protocol

**Cryptographic accountability for AI agent transactions.** [GitHub](https://github.com/jeremylongshore/irsb) | [Dashboard](https://irsb-protocol.web.app)

**Status:** 11 contracts deployed on Sepolia testnet (v1.4.0). 552 protocol tests.

### Core Contracts

- **SolverRegistry** — Solver lifecycle, bond staking (0.1 ETH minimum), slashing, 3-strikes jail, reputation decay (30-day half-life)
- **IntentReceiptHub** — Receipt posting with ECDSA signature verification, 1-hour challenge window, dispute resolution, batch posting
- **DisputeModule** — Arbitration for complex disputes, escalation from deterministic to human resolution

### Delegation & Enforcers (EIP-7702)

- **WalletDelegate** — EIP-7702 delegation with ERC-7710 redemption and caveat enforcement. beforeHook/execute/afterHook pipeline.
- **SpendLimitEnforcer** — Daily + per-transaction spend caps with ERC-20 calldata parsing
- **TimeWindowEnforcer** — Session time bounds
- **AllowedTargetsEnforcer** — Contract address whitelist
- **AllowedMethodsEnforcer** — Function selector whitelist
- **NonceEnforcer** — Replay prevention

### Supporting Contracts

- **EscrowVault** — ETH + ERC20 escrow
- **X402Facilitator** — x402 payment settlement (direct + delegated)
- **AgenticCommerce** — EIP-8183 agentic commerce protocol
- **CredibilityRegistry** — On-chain credibility tracking
- **ERC8004Adapter** — Validation signal publishing
- **IRSBHook** — Bridges EIP-8183 jobs into the IRSB accountability pipeline

---

## Layer 2: Moat

**Policy-enforced execution layer.** [GitHub](https://github.com/jeremylongshore/moat)

**Status:** Code-complete. Z3 formal verifier (42 tests). Gateway, control-plane, trust-plane, and MCP server implemented.

Every agent call passes through the Moat Gateway, which enforces:
- **Scope policies** — which capabilities the agent can access
- **Budget policies** — spending limits per tenant/time period
- **Domain allowlists** — no open proxy, only declared outbound domains
- **Default-deny** — if not explicitly allowed, it's blocked

The **FormalAgentVerifier** uses Z3 SMT solver to provide mathematical proofs of constraint satisfaction — 9 constraints across file access, network, command execution, data exfiltration, resource limits, and permissions. Fail-closed: UNKNOWN is treated as unsafe.

---

## Layer 3: Scout

**Intelligent brokering agent.** Lives inside the Moat repo.

**Status:** 8 MCP tools implemented. Broker scope defined.

Scout discovers available work (bounties on Algora, Gitcoin, Polar, GitHub), matches it to the right solver/agent, and routes it through Moat. Eight MCP tools:

- `capabilities.list` / `capabilities.search` / `capabilities.execute` / `capabilities.stats`
- `bounty.discover` / `bounty.triage` / `bounty.execute` / `bounty.status`

Scout doesn't execute work — it finds the right worker and ensures the work flows through policy enforcement.

---

## Off-Chain Services

### Solver (v0.3.0) — 139 tests

Policy gate (4 checks: jobType allowlist, expiry, requester allowlist, size guard), evidence bundle creation with SHA-256 artifact hashing, canonical JSON for deterministic hashing, Cloud KMS signing with DER parsing and EIP-2 low-S normalization.

**Status:** Code-complete. Not yet deployed to production infrastructure.

### Watchtower (v0.5.0) — ~500 tests

12-package nested pnpm monorepo. Evidence verification, behavior signal derivation (10 signals with severity weighting), risk scoring with critical override, auto-dispute pipeline, circuit breaker + retry resilience patterns.

**Status:** Code-complete. Chain context currently uses mock data — real IRSB client integration pending.

### Agents (v0.2.0) — 42 tests

Z3 FormalAgentVerifier, RAG pipeline with 12 prompt injection patterns, ledger tracking.

### Indexer (v0.1.0)

Envio HyperIndex for IRSB contract events → GraphQL API.

---

## Deployed Contracts (Sepolia)

| Contract | Address | Etherscan |
|----------|---------|-----------|
| SolverRegistry | `0xB6ab964832808E49635fF82D1996D6a888ecB745` | [View](https://sepolia.etherscan.io/address/0xB6ab964832808E49635fF82D1996D6a888ecB745) |
| IntentReceiptHub | `0xD66A1e880AA3939CA066a9EA1dD37ad3d01D977c` | [View](https://sepolia.etherscan.io/address/0xD66A1e880AA3939CA066a9EA1dD37ad3d01D977c) |
| DisputeModule | `0x144DfEcB57B08471e2A75E78fc0d2A74A89DB79D` | [View](https://sepolia.etherscan.io/address/0x144DfEcB57B08471e2A75E78fc0d2A74A89DB79D) |
| ERC-8004 IdentityRegistry | `0x8004A818BFB912233c491871b3d84c89A494BD9e` | [View](https://sepolia.etherscan.io/address/0x8004A818BFB912233c491871b3d84c89A494BD9e) |
| **IRSB Agent ID** | **#967** | [8004scan.io](https://8004scan.io) |

**Operational Accounts:**

| Account | Address |
|---------|---------|
| Deployer/Operator | `0x83A5F432f02B1503765bB61a9B358942d87c9dc0` |
| Safe (Owner) | `0xBcA0c8d0B5ce874a9E3D84d49f3614bb79189959` |

---

## Standards Referenced

| Standard | Role in IRSB |
|----------|-------------|
| ERC-7683 | Cross-chain intent format |
| EIP-7702 | EOA delegation to smart contracts |
| ERC-7710 | Delegation redemption framework |
| ERC-7715 | Permission request protocol |
| ERC-8004 | Agent identity and validation signals |
| x402 | HTTP payment protocol integration |

---

## Quick Stats

| | |
|---|---|
| **Protocol contracts** | 37 Solidity files |
| **Deployed on Sepolia** | 11 contracts (v1.4.0) |
| **Protocol tests** | 552 (Foundry) |
| **Solver tests** | 139 (Vitest) |
| **Watchtower tests** | ~500 (Vitest) |
| **Agent tests** | 42 (Pytest) |
| **Total tests** | ~1,200 |
| **Languages** | Solidity, TypeScript, Python |
| **EIPs implemented** | 6 |
| **Dashboard** | [irsb-protocol.web.app](https://irsb-protocol.web.app) |
| **Monorepo** | [github.com/jeremylongshore/irsb](https://github.com/jeremylongshore/irsb) |
| **Moat** | [github.com/jeremylongshore/moat](https://github.com/jeremylongshore/moat) |
| **License** | BUSL-1.1 → MIT on 2029-02-17 |
| **CI** | 5 GitHub Actions workflows |

---

## Deep Dive Series

- [Part 1: Five On-Chain Enforcers That Make AI Agent Wallets Structurally Safe](/posts/irsb-deep-dive-1-on-chain-enforcement/)
- [Part 2: Cryptographic Receipts and the Evidence Pipeline](/posts/irsb-deep-dive-2-evidence-pipeline/)
- [Part 3: A 12-Package Nested Monorepo That Watches AI Agents for You](/posts/irsb-deep-dive-3-watchtower-architecture/)
- [Part 4: Z3 Formal Verification, the Three-Layer Stack, and Claude Code as Architect](/posts/irsb-deep-dive-4-ai-agent-pivot/)

---

*Don't own a chain. Own the standard.*
