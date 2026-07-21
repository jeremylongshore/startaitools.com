+++
title = 'IRSB Ecosystem'
date = 2026-03-27T12:00:00-05:00
bibliography = "citations/irsb-citations.bib"
+++

# The IRSB Ecosystem

**Three layers. Thirty-seven contracts. Approximately 1,200 tests. One mission: make AI-agent transactions cryptographically accountable.**

The IRSB ecosystem is a three-layer stack — protocol, policy, and brokering — that together form the first on-chain accountability layer for AI-agent work. Every transaction produces an immutable receipt. Every solver posts a bond. Every violation triggers automated enforcement.

**Paperback edition (PDF, 59 pages):** [/research-papers/irsb-ecosystem-paperback.pdf](/research-papers/irsb-ecosystem-paperback.pdf) — hub + four deep dives + Guidewire MCP foundation-ship post concatenated, unified bibliography, print-ready.

Built collaboratively with [Claude Code](https://claude.ai/code).

---

## The Problem

AI agents are getting wallet access. The tool-using paradigm Schick and colleagues introduced with Toolformer[^schick2023toolformer] and Yao and colleagues generalised into the ReAct loop[^yao2023react] now extends to financial action: every major framework — AgentKit, ElizaOS, Olas, Virtuals, Brian AI, Safe — gives agents the ability to sign transactions. None of them answer the question: **what happens when the agent does something wrong?** Li's survey of LLM-based agent paradigms[^li2024agentparadigms] documents the rapid expansion of the agent surface and the corresponding gap in accountability infrastructure.

| Framework | Spend Limits | Execution Receipts | Monitoring | Dispute Resolution |
|-----------|:---:|:---:|:---:|:---:|
| Coinbase AgentKit | — | — | — | — |
| ElizaOS | — | — | — | — |
| Olas | — | — | — | — |
| Virtuals Protocol | — | — | — | — |
| Brian AI | — | — | — | — |
| Safe + Modules | — | — | — | — |
| **IRSB + Moat** | **On-chain** | **On-chain** | **Watchtower** | **Automated** |

Soft reputation systems require trusting someone. IRSB replaces trust with math and economics — the same posture Schneier and Kelsey articulated for forensic audit logs[^schneier1999audit] and Haber and Stornetta proposed for time-stamped documents[^haber1991timestamp]: integrity that is verifiable without depending on the trustworthiness of any single party. Greshake and colleagues' work on indirect prompt injection[^greshake2023indirect] makes the case acute: an agent's instructions can be compromised through ordinary tool use, so the safety property must live outside the agent.

---

## Architecture

Three layers, clear separation of concerns. The decomposition follows the *information-distribution* discipline Parnas articulated in 1971[^parnas1971information]: each layer hides decisions the other layers do not need to know.

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

**Cryptographic accountability for AI-agent transactions.** [GitHub](https://github.com/jeremylongshore/irsb) | [Dashboard](https://irsb-protocol.web.app)

**Status:** 11 contracts deployed on Sepolia testnet (v1.4.0). 552 protocol tests.

### Core Contracts

- **SolverRegistry** — solver lifecycle, bond staking (0.1 ETH minimum), slashing, three-strikes jail, reputation decay (30-day half-life). The bond-and-slash economic shape inherits from the staking-and-finality literature, most directly Buterin and Griffith's Casper FFG design[^buterin2017casper].
- **IntentReceiptHub** — receipt posting with ECDSA signature verification, 1-hour challenge window, dispute resolution, batch posting.
- **DisputeModule** — arbitration for complex disputes, escalation from deterministic to human resolution.

### Delegation & Enforcers (EIP-7702)

- **WalletDelegate** — EIP-7702 delegation[^eip7702] with ERC-7710 redemption[^erc7710] and caveat enforcement. `beforeHook` / `execute` / `afterHook` pipeline.
- **SpendLimitEnforcer** — daily plus per-transaction spend caps with ERC-20 calldata parsing.
- **TimeWindowEnforcer** — session time bounds.
- **AllowedTargetsEnforcer** — contract address whitelist.
- **AllowedMethodsEnforcer** — function selector whitelist.
- **NonceEnforcer** — replay prevention.

### Supporting Contracts

- **EscrowVault** — ETH + ERC-20 escrow.
- **X402Facilitator** — x402 payment settlement[^x402spec] (direct + delegated).
- **AgenticCommerce** — EIP-8183 agentic commerce protocol.
- **CredibilityRegistry** — on-chain credibility tracking.
- **ERC8004Adapter** — validation signal publishing[^erc8004].
- **IRSBHook** — bridges EIP-8183 jobs into the IRSB accountability pipeline.

---

## Layer 2: Moat

**Policy-enforced execution layer.** [GitHub](https://github.com/jeremylongshore/moat)

**Status:** code-complete. Z3 formal verifier (42 tests). Gateway, control-plane, trust-plane, and MCP server[^anthropic2024mcp] implemented.

Every agent call passes through the Moat Gateway, which enforces:
- **Scope policies** — which capabilities the agent can access
- **Budget policies** — spending limits per tenant/time period
- **Domain allowlists** — no open proxy, only declared outbound domains
- **Default-deny** — if not explicitly allowed, it is blocked. The posture is Saltzer and Schroeder's *fail-safe defaults* principle applied at the transaction layer[^saltzer1975protection].

The **FormalAgentVerifier** uses the Z3 SMT solver[^demoura2008z3] to provide mathematical proofs of constraint satisfaction — nine constraints across file access, network, command execution, data exfiltration, resource limits, and permissions. Fail-closed: `UNKNOWN` is treated as unsafe. The smart-contract verification literature is consistent on this point: symbolic-execution approaches (Luu and colleagues' Oyente[^luu2016oyente], Kalra and colleagues' ZEUS[^kalra2018zeus]) all use the same closed-world discipline.

---

## Layer 3: Scout

**Intelligent brokering agent.** Lives inside the Moat repo.

**Status:** 8 MCP tools implemented. Broker scope defined.

Scout discovers available work (bounties on Algora, Gitcoin, Polar, GitHub), matches it to the right solver/agent, and routes it through Moat. Eight MCP tools:

- `capabilities.list` / `capabilities.search` / `capabilities.execute` / `capabilities.stats`
- `bounty.discover` / `bounty.triage` / `bounty.execute` / `bounty.status`

Scout does not execute work — it finds the right worker and ensures the work flows through policy enforcement.

---

## Off-Chain Services

### Solver (v0.3.0) — 139 tests

Policy gate (4 checks: jobType allowlist, expiry, requester allowlist, size guard), evidence-bundle creation with SHA-256 artifact hashing, canonical JSON for deterministic hashing, Cloud KMS signing with DER parsing and EIP-2 low-S normalisation[^eip2]. The off-chain compute pattern follows Eberhardt and Tai's design rationale for off-chaining computation while keeping commitments on-chain[^eberhardt2017offchain].

**Status:** code-complete. Not yet deployed to production infrastructure.

### Watchtower (v0.5.0) — ~500 tests

12-package nested pnpm monorepo. Evidence verification, behaviour-signal derivation (10 signals with severity weighting), risk scoring with critical override, auto-dispute pipeline, circuit-breaker + retry resilience patterns. The architecture follows the watchtower literature for off-chain dispute monitoring: McCorry and colleagues' Pisa[^mccorry2019pisa], Avarikioti and colleagues' Cerberus Channels[^avarikioti2020cerberus], and Khabbazian and colleagues' Outpost[^khabbazian2019outpost] all argue that watchtowers must operate without blocking the on-chain happy path.

**Status:** code-complete. Chain context currently uses mock data — real IRSB client integration pending.

### Agents (v0.2.0) — 42 tests

Z3 FormalAgentVerifier[^demoura2008z3], RAG pipeline with 12 prompt-injection patterns (drawn from the Greshake and colleagues taxonomy[^greshake2023indirect] and the broader jailbreak survey literature[^yi2024jailbreak]), ledger tracking.

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
| [ERC-7683](https://eips.ethereum.org/EIPS/eip-7683) | Cross-chain intent format[^erc7683] |
| [EIP-7702](https://eips.ethereum.org/EIPS/eip-7702) | EOA delegation to smart contracts[^eip7702] |
| [ERC-7710](https://eips.ethereum.org/EIPS/eip-7710) | Delegation redemption framework[^erc7710] |
| [ERC-7715](https://eips.ethereum.org/EIPS/eip-7715) | Permission-request protocol[^erc7715] |
| [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004) | Agent identity and validation signals[^erc8004] |
| [x402](https://www.x402.org/) | HTTP payment-protocol integration[^x402spec] |

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

## Further reading

A consolidated bibliography for the IRSB ecosystem — covering Ethereum consensus and finality, payment-channel watchtowers, smart-contract formal verification, MEV, agent paradigms, and cryptographic audit-log integrity — is maintained at [/citations/](/citations/) (BibTeX + per-source verification metadata).

---

*Don't own a chain. Own the standard.*

---

## References

[^anthropic2024mcp]: Anthropic (2024). *Model Context Protocol Specification.* <https://modelcontextprotocol.io/>
[^avarikioti2020cerberus]: Avarikioti, G., Litos, O. S. T., & Wattenhofer, R. (2020). Cerberus Channels: Incentivizing Watchtowers for Bitcoin. *Financial Cryptography and Data Security (FC).* <https://doi.org/10.1007/978-3-030-51280-4_19>
[^buterin2017casper]: Buterin, V., & Griffith, V. (2017). *Casper the Friendly Finality Gadget.* arXiv:1710.09437.
[^demoura2008z3]: de Moura, L., & Bjørner, N. (2008). Z3: An Efficient SMT Solver. *TACAS.* <https://doi.org/10.1007/978-3-540-78800-3_24>
[^eberhardt2017offchain]: Eberhardt, J., & Tai, S. (2017). On or Off the Blockchain? Insights on Off-Chaining Computation and Data. *ESOCC.* <https://doi.org/10.1007/978-3-319-67262-5_1>
[^eip2]: Wood, G., & Reitwiessner, C. (2015). *EIP-2: Homestead Hard-fork Changes.* <https://eips.ethereum.org/EIPS/eip-2>
[^eip7702]: Buterin, V., Hancock, S., Akhunov, A., Beiko, T., & St. Pierre, T. (2024). *EIP-7702: Set EOA Account Code.* <https://eips.ethereum.org/EIPS/eip-7702>
[^erc7683]: Across Protocol and Uniswap Labs (2024). *ERC-7683: Cross-Chain Intents Standard.* <https://eips.ethereum.org/EIPS/eip-7683>
[^erc7710]: ERC-7710 contributors (2024). *ERC-7710: Smart Contract Delegation Redemption.* <https://eips.ethereum.org/EIPS/eip-7710>
[^erc7715]: ERC-7715 contributors (2024). *ERC-7715: Request Permissions for Transactions.* <https://eips.ethereum.org/EIPS/eip-7715>
[^erc8004]: ERC-8004 contributors (2024). *ERC-8004: Agent Identity and Validation Signals.* <https://eips.ethereum.org/EIPS/eip-8004>
[^greshake2023indirect]: Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. (2023). Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection. *AISec '23.* <https://doi.org/10.1145/3605764.3623985>
[^haber1991timestamp]: Haber, S., & Stornetta, W. S. (1991). How to Time-Stamp a Digital Document. *Journal of Cryptology*, 3(2), 99–111. <https://doi.org/10.1007/BF00196791>
[^kalra2018zeus]: Kalra, S., Goel, S., Dhawan, M., & Sharma, S. (2018). ZEUS: Analyzing Safety of Smart Contracts. *NDSS.*
[^khabbazian2019outpost]: Khabbazian, M., Nadahalli, T., & Wattenhofer, R. (2019). Outpost: A Responsive Lightweight Watchtower. *AFT.* <https://doi.org/10.1145/3318041.3355464>
[^li2024agentparadigms]: Li, X. (2024). A Review of Prominent Paradigms for LLM-Based Agents: Tool Use, Planning (Including RAG), and Feedback Learning. *COLING.* arXiv:2406.05804.
[^luu2016oyente]: Luu, L., Chu, D.-H., Olickel, H., Saxena, P., & Hobor, A. (2016). Making Smart Contracts Smarter. *CCS.* <https://doi.org/10.1145/2976749.2978309>
[^mccorry2019pisa]: McCorry, P., Bakshi, S., Bentov, I., Miller, A., & Meiklejohn, S. (2019). Pisa: Arbitration Outsourcing for State Channels. *AFT.* <https://doi.org/10.1145/3318041.3355461>
[^parnas1971information]: Parnas, D. L. (1971). Information Distribution Aspects of Design Methodology. *Proceedings of the IFIP Congress.* <https://doi.org/10.1184/R1/6606470.V1>
[^saltzer1975protection]: Saltzer, J. H., & Schroeder, M. D. (1975). The Protection of Information in Computer Systems. *Proceedings of the IEEE*, 63(9), 1278–1308. <https://doi.org/10.1109/PROC.1975.9939>
[^schick2023toolformer]: Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). Toolformer: Language Models Can Teach Themselves to Use Tools. *NeurIPS.* arXiv:2302.04761.
[^schneier1999audit]: Schneier, B., & Kelsey, J. (1999). Secure Audit Logs to Support Computer Forensics. *ACM TISSEC*, 2(2), 159–176. <https://doi.org/10.1145/317087.317089>
[^x402spec]: x402 Working Group (2024). *x402: HTTP 402 Payment Required Protocol.* <https://www.x402.org/>
[^yao2023react]: Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. *ICLR.* arXiv:2210.03629.
[^yi2024jailbreak]: Yi, S., Liu, Y., Sun, Z., Cong, T., He, X., Song, J., Xu, K., & Li, Q. (2024). Jailbreak Attacks and Defenses Against Large Language Models: A Survey. arXiv:2407.04295.
