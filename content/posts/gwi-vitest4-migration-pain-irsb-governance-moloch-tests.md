+++
title = 'git-with-intent Vitest 4 Migration Pain and IRSB Governance with 104 Moloch Tests'
slug = 'gwi-vitest4-migration-pain-irsb-governance-moloch-tests'
date = 2026-02-12T10:00:00-06:00
draft = false
tags = ["git-with-intent", "vitest", "ci-cd", "migration", "irsb", "solidity", "governance", "testing", "security"]
categories = ["Development Journey"]
description = "Seven Vitest 4 migration CI fixes for git-with-intent v0.8.0 — mock patterns, process.exit at import, vi.hoisted — plus IRSB v1.4.0 with TimelockController, volume-proportional bonds, and 104 Moloch DAO-style governance tests."
+++

Eighteen commits across three repos. git-with-intent fought through a Vitest 4 migration that broke CI seven different ways. IRSB shipped v1.4.0 with governance contracts and a 104-test Moloch DAO suite. Perception got a dashboard fix.

## git-with-intent: Vitest 4 Migration

The v0.8.0 prep for git-with-intent included upgrading from Vitest 3.x to Vitest 4. The test suite passed locally. CI failed. Then it failed six more times in six different ways.

### Mock Pattern Changes

Vitest 4 changed how `vi.mock()` interacts with module resolution. In Vitest 3, mock declarations were hoisted above imports automatically. Vitest 4 introduced `vi.hoisted()` as an explicit mechanism and stopped auto-hoisting in several edge cases.

The git-with-intent codebase had 47 test files using `vi.mock()`. Twelve of them relied on the auto-hoisting behavior in ways that Vitest 4 no longer supported. Each one needed a slightly different fix depending on whether the mock needed access to test-scoped variables.

Pattern that broke:

```typescript
// Vitest 3: worked because vi.mock was hoisted above the import
import { analyzeCommit } from '../src/analyzer';
vi.mock('../src/git-client', () => ({ getCommitDiff: vi.fn() }));
```

Vitest 4 fix using `vi.hoisted()`:

```typescript
const mocks = vi.hoisted(() => ({
  getCommitDiff: vi.fn(),
}));
vi.mock('../src/git-client', () => mocks);
import { analyzeCommit } from '../src/analyzer';
```

The `vi.hoisted()` call explicitly marks the factory as safe to hoist. Without it, the mock factory executes after the import, and the import gets the real module instead of the mock.

### process.exit at Import Time

Three modules in git-with-intent call `process.exit(1)` in their top-level error handlers — the config loader, the git binary checker, and the telemetry initializer. In Vitest 3, these modules were mocked before their code ran. In Vitest 4, two of the three started executing before the mock took effect.

The fix was the same pattern each time: move the `vi.mock()` declaration to the top of the file and use `vi.hoisted()` for the mock factory. But the config loader was trickier — it imported other modules that also had side effects. That required mocking the entire dependency chain, not just the direct import.

### CI-Specific Failures

Two failures only reproduced in CI, not locally. Both were timing-related. The first was a test that verified commit analysis performance — it asserted completion within 500ms, which worked on a developer laptop but not on GitHub Actions' shared runners. The fix: remove the performance assertion from the unit test and move it to a dedicated benchmark suite.

The second was a race condition in the git binary version check. The test spawned `git --version` and parsed the output. On CI, the spawn occasionally returned an empty string because the process hadn't written to stdout yet when the test read it. The fix: `await` the stream close event instead of reading after spawn.

## IRSB v1.4.0: Governance Layer

IRSB's v1.4.0 introduced a governance layer inspired by Moloch DAO patterns, with three new contracts and one significant upgrade to the bonding system.

### TimelockController

Protocol parameter changes (bond amounts, challenge windows, slashing percentages) now go through a `TimelockController` with a 48-hour delay. The controller queues proposals, enforces the delay, and executes them atomically. During the delay window, a guardian address can cancel malicious proposals.

The timelock prevents a compromised admin key from immediately changing parameters to drain bonds. Forty-eight hours gives watchtower operators time to detect and respond.

### Volume-Proportional Bonds

The bond amount changed from a fixed value to a function of the solver's trailing 30-day settlement volume. Higher volume means higher bond. The formula:

```
bond = max(MIN_BOND, volume_30d * BOND_RATE)
```

`MIN_BOND` is 0.1 ETH. `BOND_RATE` is 1% — for every 1 ETH of settled intents in the past 30 days, the solver must bond an additional 0.01 ETH. This aligns incentives: solvers handling more value have more at stake.

### Nonce Enforcement and ECDSA Fix

Nonce enforcement prevents replay attacks on solver submissions. Each solver maintains an on-chain nonce that increments with each receipt. Submitting a receipt with a stale nonce reverts.

The ECDSA fix addressed an `address(0)` check. The `ecrecover` precompile returns `address(0)` for invalid signatures instead of reverting. The existing code compared the recovered address against the expected signer but didn't first check for the zero address. A carefully crafted invalid signature could pass verification by targeting a solver with address `0x0` (which doesn't exist in practice, but the check should be there defensively).

### 104 Moloch DAO-Style Tests

The governance test suite covers 104 scenarios across proposal lifecycle, voting mechanics, ragequit, and guild kick. These aren't unit tests — they're integration tests that deploy the full contract suite, register solvers, submit proposals, advance time, and verify state transitions end-to-end.

### Catastrophic Failure Pre-Mortem

The v1.4.0 release included a pre-mortem document covering five catastrophic failure scenarios: admin key compromise, bond drain through rapid parameter changes, oracle manipulation, governance capture, and cross-contract reentrancy. Each scenario has a detection method, response playbook, and the specific contract safeguard that mitigates it.

## Perception Dashboard Fix

One commit: the dashboard article count was showing stale data because the Firestore listener wasn't resetting when the category filter changed. The listener detach function wasn't being called in the `useEffect` cleanup, so each filter change stacked another listener. After switching categories five times, you had six listeners all updating the same state. The fix was the standard React pattern — return the unsubscribe function from the effect.

## What I Learned

**Major test framework upgrades break CI, not your IDE.** Local test runs have consistent timing, warm caches, and predictable process scheduling. CI has none of that. Always run the full suite in CI before declaring a framework upgrade complete.

**Pre-mortems are cheaper than post-mortems.** Writing down "what happens if the admin key leaks" before it happens forces you to build the safeguards. Writing it down after costs you the bonds.

**Related Posts:**
- [git-with-intent v0.9 to v0.10: Docker Upgrades, README Rewrites, and Strategic Research](/posts/git-with-intent-v090-v0100-docker-upgrades/)
- [IRSB Monorepo v1.0.0: Extracting Shared Packages and Unifying a Blockchain Platform](/posts/irsb-monorepo-v1-extracting-shared-packages/)
- [IRSB Agent Guardrails Pivot, Products Workspace Launch, and the Pitch Deck Sprint](/posts/irsb-agent-guardrails-pivot-products-workspace-launch/)
