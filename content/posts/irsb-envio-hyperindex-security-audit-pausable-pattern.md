+++
title = 'IRSB Security Audit: Pausable Patterns, Invariant Tests, and an Envio Indexer That Fought PostgreSQL'
slug = 'irsb-envio-hyperindex-security-audit-pausable-pattern'
date = 2026-02-18T10:00:00-06:00
draft = false
tags = ["blockchain", "security", "testing", "solidity", "ci-cd", "envio", "irsb"]
categories = ["Development Journey"]
description = "Three new invariant test suites, a Pausable guard on DisputeModule, dead code removal, and the Envio HyperIndex port conflict that wasted an hour."
+++

Security audits are unglamorous. You read every function, ask "what if this is called when it shouldn't be," and write tests for the answers. February 18th was 14 commits of that for the IRSB monorepo.

## The Pausable Pattern on DisputeModule

The DisputeModule handles arbitration in the IRSB protocol. If a solver disputes a receipt, this contract manages the lifecycle: filing, evidence submission, resolution, and timeout-based auto-resolution.

The problem: there was no way to pause it. If a critical vulnerability surfaces in production, you need an emergency brake. Every other state-changing contract in IRSB had OpenZeppelin's `Pausable` mixin. DisputeModule didn't.

The fix was surgical. Add `Pausable` to the inheritance chain, then put `whenNotPaused` guards on the two functions that change state:

- `resolve()` — arbitrator settles a dispute
- `resolveByTimeout()` — auto-resolves when the dispute window expires

View-only functions and the dispute filing itself stay unguarded. You want users to still be able to file disputes and read state even during an emergency pause. Only resolution — the irreversible part — gets the brake.

## Three Invariant Test Suites

Invariant tests are different from unit tests. A unit test checks a specific input-output pair. An invariant test defines a property that must hold across all possible state transitions, then throws randomized inputs at the contract until it either proves the property or finds a violation.

Three new suites went in:

**Receipt integrity invariants** — every receipt that enters `IntentReceiptHub` must have a non-zero solver address, a valid chain ID, and an amount within the solver's registered bond limit. The invariant fuzzer generates random receipt payloads and checks that the hub rejects anything violating these constraints.

**Bond balance invariants** — the sum of all solver bonds in escrow must equal the contract's actual token balance. This catches accounting bugs where bonds get credited without a corresponding transfer, or withdrawals happen without debiting the bond ledger.

**Dispute lifecycle invariants** — a dispute that reaches `RESOLVED` status can never transition to any other state. A dispute that reaches `TIMED_OUT` can never be resolved by an arbitrator. These state machine invariants catch reentrancy bugs and ordering violations.

The bond balance invariant found a rounding edge case on the first run. Not exploitable in practice — sub-wei precision — but it was still a gap in the accounting logic that a formal audit would flag.

## Dead Code and Formatting

`Events.sol` was a standalone file that duplicated events already defined in their respective contracts. It existed because early development declared events in a central file, then individual contracts grew their own event definitions. The central file became dead code that would confuse any auditor.

Deleted it. No references broke.

`forge fmt` ran across the entire Solidity codebase. Three contracts had inconsistent brace style from different contributors. Not a security issue, but auditors notice formatting inconsistencies and it costs review time.

The Moloch test signatures were out of sync with the actual function signatures. When someone renamed parameters in the contracts, the test helpers kept the old names. Forge doesn't catch this — it resolves by selector, not by parameter name. But it makes the test suite misleading to read.

## CI: Split Tests, Parallelize Coverage

The monorepo CI was running all tests sequentially. Solidity unit tests, invariant tests, TypeScript watchtower tests, Python agent tests — all in one job. A single Solidity invariant test failure would block the TypeScript test results for 8+ minutes.

Split into four parallel jobs:
1. Solidity unit tests
2. Solidity invariant tests (with higher gas limits)
3. TypeScript service tests
4. Python agent tests

Coverage now runs in parallel too. Each job generates its own coverage artifact, and a final job merges them. Total CI time dropped from ~12 minutes to ~5 minutes for the common case where most jobs pass.

## Envio HyperIndex: Port Conflicts

Envio HyperIndex is an indexer for blockchain events. It watches contract events on-chain and populates a local PostgreSQL database with structured data for the frontend.

Getting the local dev environment running should have been trivial. It wasn't.

The Envio dev server defaults to PostgreSQL on port 5432. My dev server already runs system PostgreSQL on 5432. Envio's local Caddy proxy defaults to ports 80 and 443. Caddy was already bound to those ports for other projects.

Two port conflicts, neither surfaced as a clear error message. The Envio process just silently failed to start, or started and couldn't write to the database. The fix: override the ports in the Envio config and point it at a dedicated PostgreSQL instance on 5433. Simple once you know the problem. Annoying to diagnose from "it doesn't work."

The indexer itself is straightforward once running. Define the contract events you care about, write handlers that transform event data into your schema, and Envio manages the ingestion pipeline. The local dev experience — once the port conflicts are resolved — is fast. Events appear in the database within seconds of being emitted on a local Anvil chain.

## The Day in Numbers

| Area | What Shipped |
|------|-------------|
| Security | Pausable on DisputeModule, `whenNotPaused` on 2 functions |
| Testing | 3 invariant test suites, Moloch signature fixes |
| Cleanup | Dead `Events.sol` removed, `forge fmt` across codebase |
| CI | 4 parallel jobs, merged coverage |
| Indexer | Envio HyperIndex local dev running (after port fight) |

Fourteen commits, no new features. Just making the existing code harder to break and easier to audit. That's the job some days.

---

## Related Posts

- [IRSB Monorepo v1.0.0: Extracting Shared Packages](/posts/irsb-monorepo-v1-extracting-shared-packages/) — The monorepo migration these tests now protect
- [Building Moat: Auth, On-Chain Receipts, and 117 Tests](/posts/building-moat-auth-persistence-onchain-receipts-117-tests/) — Moat's testing approach for the IRSB trust layer
- [Session Cookie Auth, Forgot-Password Timeouts, and Killing Flaky E2E Tests](/posts/session-cookies-forgot-password-flaky-e2e-tests/) — Another security hardening sprint with a testing focus
