+++
title = 'IRSB On-Chain Solver Registration: Agent ID 967'
slug = 'irsb-on-chain-solver-registration-agent-id-967'
date = 2026-02-07T10:00:00-06:00
draft = false
tags = ["irsb", "solidity", "erc-8004", "on-chain", "identity", "hustle"]
categories = ["Development Journey"]
description = "IRSB registers a solver on the ERC-8004 IdentityRegistry and receives Agent ID 967. AI-CONTEXT cross-references document the integration points. Hustle adds issue templates."
+++

A thin commit day by February standards — four commits across two repos. But one of those commits put an agent identity on-chain, which is worth writing up.

## IRSB: Solver Registration on ERC-8004

Three commits. The first registered a solver identity on the ERC-8004 IdentityRegistry contract. The second added AI-CONTEXT cross-reference documentation. The third cleaned up the deployment scripts.

### ERC-8004 IdentityRegistry

ERC-8004 is the identity standard for autonomous agents operating on-chain. The registry maps agent addresses to verifiable identity records: what the agent does, who operates it, what capabilities it claims, and what reputation it's accumulated. Think of it as DNS for AI agents — a public, verifiable lookup from address to identity.

The registry stores identity records as packed structs in two storage slots:

- **Slot 1:** Operator address (20 bytes) + capability bitmap (12 bytes)
- **Slot 2:** Metadata URI pointing to the full identity document (an IPFS hash)

The packing keeps storage costs low — the entire identity record costs the same gas as storing two `uint256` values.

### Agent ID 967

The IRSB solver registered as Agent ID 967. The identity record declares:

- **Capabilities:** Bounty resolution for software engineering tasks
- **Operator:** Intent Solutions
- **Verification method:** Passkey-based authentication (built two days ago) linked to this on-chain identity
- **Capability bitmap:** Bits set for `SOLVER`, `SOFTWARE_ENGINEERING`, and `AUTOMATED` — three of the 96 possible capability flags defined by ERC-8004

The registration transaction cost roughly $0.12 in gas on Sepolia testnet. On mainnet the cost would be comparable — the IdentityRegistry contract is optimized for minimal storage, and registration is a single `SSTORE` for each of the two slots plus the mapping update.

### Why This Matters

When the IRSB protocol's bounty system is live, anyone can submit a bounty resolution. The question is trust: how do you evaluate a solver you've never worked with?

Reputation APIs exist, but they're centralized — the API provider can modify or delete reputation data. The ERC-8004 identity gives you a starting point that nobody controls. Agent ID 967 has an on-chain history — every bounty it's claimed, resolved, or failed is recorded as events on the IdentityRegistry. That history is verifiable by anyone with an Ethereum node and immutable once written. You can't fake a track record when it's on a public ledger. You can't selectively delete failed bounties. The good and the bad accumulate equally.

The passkey integration from yesterday feeds directly into this. When Agent ID 967 authenticates to the IRSB gateway, the gateway verifies the passkey signature and then checks the on-chain identity record to confirm the agent's declared capabilities match what it's trying to do. A solver registered for software engineering tasks can't claim a design bounty — the capability bitmap doesn't include the `DESIGN` flag.

### AI-CONTEXT Cross-References

The IRSB monorepo has grown complex enough that navigating between related components isn't obvious from the directory structure alone. The AI-CONTEXT files are machine-readable cross-reference maps that tell Claude Code (or any AI assistant) how the components relate.

The cross-references added today document three relationships:

- The passkey service authenticates agents (references `packages/agent-passkey/`)
- The IdentityRegistry provides on-chain identity verification (references `contracts/IdentityRegistry.sol`)
- The bounty contracts use the IdentityRegistry for solver capability checks (references `contracts/BountyMarket.sol` and the `verifyCapability` internal function)

These relationships were implicit in the code — function calls, import paths, contract interfaces. Now they're explicit in files that an AI can read without tracing the full call graph.

## Hustle: Issue Templates

One commit adding GitHub issue templates for bug reports and feature requests. The templates use GitHub's YAML-based issue form syntax rather than Markdown templates. YAML forms give you dropdowns, checkboxes, and required fields — the submitter can't skip the reproduction steps.

The bug report template has structured fields: steps to reproduce, expected behavior, actual behavior, affected components (dropdown with the main modules), and environment details. The feature request template has: problem description, proposed solution, acceptance criteria, and affected components.

The templates use required field validation — you can't submit a bug report without reproduction steps. This prevents the "it doesn't work" issues that provide no actionable information and require a round-trip of questions before anyone can investigate.

## The Thin Day Question

Four commits is light. Some days are like this. The solver registration was a 90-minute task that required careful transaction construction, verification on the block explorer, and testing the capability check flow end-to-end. The AI-CONTEXT work was another hour of reading through the codebase and documenting relationships that exist but aren't obvious. The issue templates were 15 minutes. The deployment script cleanup was 10 minutes.

Not every day produces 30+ commits. The solver registration is a single transaction that took less than a second to execute, but it's the transaction that gives the IRSB agent a permanent, verifiable identity on a public chain. Agent ID 967 will accumulate reputation over months and years of bounty resolution. Today just created it.

The three IRSB commits and one Hustle commit won't impress anyone looking at commit counts. But Agent ID 967 on the IdentityRegistry is more consequential than most 30-commit days. It's the difference between "we have an agent that can solve bounties" and "we have an agent with a verifiable on-chain identity that can accumulate trust." The identity is the foundation that everything else builds on.

---

## Related Posts

- [IRSB Deep Dive: On-Chain Enforcement and How the Protocol Actually Works](/posts/irsb-deep-dive-1-on-chain-enforcement/) — The on-chain enforcement architecture that Agent ID 967 participates in
- [Building Moat: Auth, Persistence, On-Chain Receipts, and 117 Tests](/posts/building-moat-auth-persistence-onchain-receipts-117-tests/) — The auth and on-chain receipt infrastructure underlying agent identity
- [IRSB SDK, CLI, and x402 Payment Protocol v1.1.0](/posts/irsb-sdk-cli-x402-payment-protocol-v110/) — The SDK that interacts with the IdentityRegistry
