+++
title = 'Deep Dive Part 1: Five On-Chain Enforcers That Make AI Agent Wallets Structurally Safe'
slug = 'irsb-deep-dive-1-on-chain-enforcement'
date = 2026-03-27T13:00:00-05:00
draft = false
tags = ["irsb", "solidity", "ethereum", "eip-7702", "security", "ai-agents", "claude-code", "smart-contracts"]
categories = ["IRSB Deep Dive"]
description = "How EIP-7702 delegation, five caveat enforcers, and bond staking create defense-in-depth guardrails for AI agent wallets — with 11 contracts live on Sepolia."
toc = true
+++

Every framework that lets an AI agent control a wallet eventually faces the same uncomfortable question: what stops it from doing something you did not intend? Current answers range from "we wrote a policy document" to "we trust the model." Neither is an answer an engineer should accept when real money is involved. The field has been shipping capability without shipping safety infrastructure, and the gap is widening.

The [IRSB Ecosystem](/irsb-ecosystem/) is a protocol-level attempt to close that gap — not by adding more agent memory or better prompting, but by encoding limits in Solidity and putting them on-chain before a transaction ever executes.

This is Part 1 of the [IRSB Ecosystem Deep Dive](/irsb-ecosystem/) series. It covers the on-chain enforcement layer: how EIP-7702 delegation works, what the five caveat enforcers do, how calldata parsing catches ERC-20 transfers, and what the SolverRegistry's bond-and-slash model adds on top. Eleven contracts are deployed on Sepolia testnet today.

---

## The Wallet Delegation Problem

Giving an AI agent raw private key access to a wallet is the worst version of the problem. The agent can do anything, at any time, with no audit trail, and no recovery path if it goes wrong. A key can be extracted from a compromised environment. A model can be manipulated into transferring funds through a carefully crafted prompt. There is no circuit breaker.

EIP-7702 changes the delegation model. Instead of giving an agent a key, an EOA (externally owned account) delegates execution authority to a smart contract — the WalletDelegate. The EOA remains the owner; the contract becomes the gatekeeper. Every call the agent wants to make goes through the WalletDelegate, which enforces a set of caveats before the transaction touches the target.

The caveats are not optional hints. They are Solidity. If a caveat reverts, the call reverts. The agent cannot override them with a longer explanation or a different framing. This is the structural distinction that matters: policy-as-code enforced at the EVM level, not policy-as-prompt enforced at the model level.

---

## The beforeHook/execute/afterHook Pipeline

The WalletDelegate's `executeDelegated()` function implements a three-phase pipeline. Before the actual call executes, every registered caveat enforcer runs its `beforeHook()`. After the call succeeds, every enforcer runs its `afterHook()`. If any hook reverts at any point, the entire transaction fails and state is not changed.

```solidity
function executeDelegated(bytes32 delegationHash, address target, bytes calldata callData, uint256 value)
    external payable whenNotPaused nonReentrant returns (bytes memory result)
{
    TypesDelegation.StoredDelegation storage stored = _delegations[delegationHash];
    if (stored.delegator == address(0)) revert DelegationNotFound();
    if (!stored.active) revert DelegationNotActive();

    address delegator = stored.delegator;
    TypesDelegation.Caveat[] storage caveats = _caveats[delegationHash];

    // WD-2: Run all beforeHooks
    for (uint256 i = 0; i < caveats.length; i++) {
        ICaveatEnforcer(caveats[i].enforcer)
            .beforeHook(caveats[i].terms, delegationHash, delegator, target, callData, value);
    }

    bool success;
    (success, result) = target.call{ value: value }(callData);
    if (!success) revert ExecutionFailed();

    // WD-2: Run all afterHooks
    for (uint256 i = 0; i < caveats.length; i++) {
        ICaveatEnforcer(caveats[i].enforcer)
            .afterHook(caveats[i].terms, delegationHash, delegator, target, callData, value);
    }

    emit DelegatedExecution(delegationHash, delegator, target, value);
}
```

Each enforcer receives the same inputs: the encoded terms for that caveat, the delegation hash, the delegator's address, the target contract, the raw calldata, and the ETH value. Enforcers are stateful — they can track cumulative spend, call counts, or any other metric across the lifetime of a delegation. The terms are ABI-encoded at delegation creation time and cannot be modified without creating a new delegation.

The `nonReentrant` guard and `whenNotPaused` checks wrap the whole function. The contract owner can pause the system in an emergency without touching individual delegations.

---

## SpendLimitEnforcer: Daily and Per-Transaction Caps

The spend limit enforcer is the most critical piece of the system. It addresses two distinct attack vectors: a single large drain and a slow bleed of many small transactions that collectively exceed what the user intended.

The solution is two independent caps. The per-transaction cap prevents any single call from moving more than a threshold amount. The daily cap resets each epoch (defined as `block.timestamp / 1 days`) and prevents cumulative daily spend from exceeding the limit even if every individual transaction is below the per-tx threshold.

```solidity
function beforeHook(
    bytes calldata terms, bytes32 delegationHash,
    address, address, bytes calldata callData, uint256 value
) external override {
    (address token, uint256 dailyCap, uint256 perTxCap) = abi.decode(terms, (address, uint256, uint256));
    uint256 spendAmount = _extractSpendAmount(token, callData, value);

    if (spendAmount > perTxCap) revert CaveatViolation("Per-transaction spend limit exceeded");

    uint256 currentEpoch = block.timestamp / 1 days;
    SpendState storage state = spendState[delegationHash][token];
    if (state.epoch != currentEpoch) {
        state.totalSpent = 0;
        state.epoch = currentEpoch;
    }

    uint256 newTotal = state.totalSpent + spendAmount;
    if (newTotal > dailyCap) revert CaveatViolation("Daily spend limit exceeded");
    state.totalSpent = newTotal;
}
```

The epoch reset is lazy — it happens on the first transaction of a new day, not via a cron or keeper. This keeps gas costs low while guaranteeing that stale daily totals cannot carry forward.

The `token` parameter in the terms handles both native ETH (token address zero) and ERC-20 tokens. Each token tracked by a delegation gets its own independent `SpendState`. A delegation that covers both ETH and USDC has separate daily caps for each.

---

## The Other Four Enforcers

SpendLimitEnforcer handles the "how much" question. The other four enforcers handle "when," "where," "what," and "how many times."

**TimeWindowEnforcer** restricts execution to a specific time range, encoded as `(uint256 notBefore, uint256 notAfter)` in the terms. An agent session with a 9am-to-5pm window cannot be used at midnight, regardless of how the agent was prompted.

**AllowedTargetsEnforcer** maintains a whitelist of contract addresses the delegation is permitted to call. If the agent attempts to call a contract not in the whitelist, the `beforeHook` reverts. This prevents a compromised or confused agent from interacting with arbitrary protocols — only the contracts explicitly approved at delegation time are reachable.

**AllowedMethodsEnforcer** operates at the function selector level. Even if a target contract is whitelisted, the enforcer checks the first four bytes of calldata against an approved selector list. An agent granted permission to call `transfer()` on a token contract cannot call `approve()` or `transferOwnership()` on the same contract.

**NonceEnforcer** assigns a monotonically increasing nonce to each execution and rejects replays. This matters for signed delegation flows where the same delegation hash could theoretically be submitted multiple times.

These five enforcers compose independently. A delegation can use all five, three, or just one. Each enforcer is a separate deployed contract implementing the `ICaveatEnforcer` interface. Adding a new enforcer requires no changes to the WalletDelegate — it just needs a contract address and ABI-encoded terms. The system is fail-closed: an enforcer that does not recognize the calldata should revert rather than silently pass.

---

## ERC-20 Calldata Parsing

Tracking ETH spend is straightforward — it is the `value` parameter on the call. Tracking ERC-20 spend requires parsing calldata, because ERC-20 transfers pass the amount as an encoded function argument, not as ETH value.

The `_extractSpendAmount()` function handles the three common ERC-20 transfer patterns by inspecting the first four bytes of calldata (the function selector) and then ABI-decoding the relevant portion of the remaining arguments.

```solidity
function _extractSpendAmount(address token, bytes calldata callData, uint256 value)
    internal pure returns (uint256)
{
    if (token == address(0)) return value;

    if (callData.length >= 68) {
        bytes4 selector = bytes4(callData[:4]);
        if (selector == 0xa9059cbb || selector == 0x095ea7b3) { // transfer, approve
            (, uint256 amount) = abi.decode(callData[4:68], (address, uint256));
            return amount;
        }
        if (selector == 0x23b872dd && callData.length >= 100) { // transferFrom
            (,, uint256 amount) = abi.decode(callData[4:100], (address, address, uint256));
            return amount;
        }
    }
    return value;
}
```

`0xa9059cbb` is `transfer(address,uint256)`. `0x095ea7b3` is `approve(address,uint256)`. `0x23b872dd` is `transferFrom(address,address,uint256)`. The minimum calldata lengths (68 and 100 bytes) guard against malformed input that could cause a decode panic.

If the calldata does not match any recognized selector, the function returns the ETH value — which is zero for a pure ERC-20 call. This is a conservative fallback: an unrecognized ERC-20 call is not counted against the daily limit, which is a known limitation. The alternative — reverting on unrecognized selectors — would break legitimate interactions with non-standard tokens.

---

## SolverRegistry: Bond Staking and Slashing

The caveat enforcers handle what an agent can do. The SolverRegistry handles who is allowed to act as a solver in the first place, and what the economic consequences are for misbehavior.

Solvers post a bond before they can execute delegated transactions. The bond is not a fixed fee — it scales with volume, requiring 5% of cumulative transaction volume above the base minimum. This means a solver handling large transactions must post proportionally larger bonds, making attacks more expensive as the stakes increase.

```solidity
uint256 public constant MINIMUM_BOND = 0.1 ether;
uint64  public constant WITHDRAWAL_COOLDOWN = 7 days;
uint8   public constant MAX_JAILS = 3;
uint64  public constant DECAY_HALF_LIFE = 30 days;
uint16  public constant MIN_DECAY_MULTIPLIER_BPS = 1000; // 10% floor
```

The jail mechanism provides escalating consequences. A solver can be jailed up to three times for violations. After the third jail, they are permanently banned from the registry. This creates a three-strikes structure that allows for recovery from errors while enforcing a hard limit on repeated offenders.

When slashing occurs, the bond distribution is: 80% to the affected user, 15% to the challenger who surfaced the violation, and 5% to the protocol treasury. This alignment incentivizes external parties to monitor solver behavior and report violations — the system does not rely solely on protocol-owned monitoring.

The reputation decay uses a 30-day half-life with a 10% floor. A solver's reputation score decays over time if they are inactive, preventing indefinitely accumulated reputation from providing a permanent safety buffer. The 10% floor (`MIN_DECAY_MULTIPLIER_BPS = 1000`) means reputation never fully zeroes, preserving some history for long-term participants.

The 7-day withdrawal cooldown prevents a solver from draining their bond immediately after a violation is detected but before a slash transaction is confirmed.

---

## Deployed Contracts on Sepolia Testnet

All eleven protocol contracts are deployed on Sepolia. These are testnet deployments — no mainnet deployment exists yet.

| Contract | Address | Explorer |
|---|---|---|
| SolverRegistry | [0xB6ab964832808E49635fF82D1996D6a888ecB745](https://sepolia.etherscan.io/address/0xB6ab964832808E49635fF82D1996D6a888ecB745) | Sepolia Etherscan |
| IntentReceiptHub | [0xD66A1e880AA3939CA066a9EA1dD37ad3d01D977c](https://sepolia.etherscan.io/address/0xD66A1e880AA3939CA066a9EA1dD37ad3d01D977c) | Sepolia Etherscan |
| DisputeModule | [0x144DfEcB57B08471e2A75E78fc0d2A74A89DB79D](https://sepolia.etherscan.io/address/0x144DfEcB57B08471e2A75E78fc0d2A74A89DB79D) | Sepolia Etherscan |
| ERC-8004 Registry | [0x8004A818BFB912233c491871b3d84c89A494BD9e](https://sepolia.etherscan.io/address/0x8004A818BFB912233c491871b3d84c89A494BD9e) | Sepolia Etherscan |
| IRSB Agent ID | [#967](https://sepolia.etherscan.io/address/0x8004A818BFB912233c491871b3d84c89A494BD9e) | 8004scan |

The BUSL-1.1 license on the protocol contracts converts to MIT on 2029-02-17.

---

## The Competitive Gap

The AI agent wallet space has accumulated a number of frameworks over the past two years, but none of them have shipped on-chain enforcement. The comparison is not about capability — AgentKit, ElizaOS, Olas, Virtuals, Brian AI, and Safe are all competent systems in their respective lanes. The gap is about what happens when something goes wrong.

| Framework | On-Chain Spend Limits | Execution Receipts | Active Monitoring | Dispute Resolution |
|---|---|---|---|---|
| AgentKit (Coinbase) | No | No | No | No |
| ElizaOS | No | No | No | No |
| Olas | No | No | Partial | No |
| Virtuals Protocol | No | No | No | No |
| Brian AI | No | No | No | No |
| Safe (with modules) | Partial (manual) | No | No | No |
| IRSB | Yes (5 enforcers) | Yes (IntentReceiptHub) | Yes (Watchtower) | Yes (DisputeModule) |

Safe with custom modules can approximate some spend limiting, but it requires writing and deploying a module per use case and there is no standardized caveat interface. The other frameworks do not have on-chain enforcement at all — policy lives in the agent's system prompt or in off-chain configuration files that the model can read but cannot be forced to obey.

The structural difference is simple: IRSB limits are enforced by the EVM. The others rely on the model honoring a policy document it was given as context.

---

## What Comes Next

This post covered the enforcement layer — the contracts that run before and after every delegated call. The remaining parts of this series cover how the rest of the stack fits together:

- **Part 2: The Evidence Pipeline** — How IntentReceiptHub creates tamper-evident execution records, what the receipt schema captures, and how receipts feed the dispute resolution process.
- **Part 3: The Watchtower Architecture** — The off-chain monitoring system that watches on-chain events, scores solver behavior, and triggers alerts before slashing is warranted.
- **Part 4: Z3, the Three-Layer Stack, and Claude Code as Architect** — Formal verification of caveat logic using Z3, how the three layers (enforcement, evidence, monitoring) compose into a coherent safety system, and what it looks like to build protocol infrastructure with Claude Code as the primary development tool.

The core thesis across all four parts is the same: AI agents with wallet access need structural safety, not honor systems. Structural safety means the constraints exist independently of the model, are enforced before execution, and cannot be bypassed by prompt manipulation. Every other approach — system prompts, off-chain policies, trust-the-model — is an honor system. Honor systems fail when the stakes are high enough.

---

*Part of the [IRSB Ecosystem](/irsb-ecosystem/) deep dive series. Built with [Claude Code](https://claude.ai/code).*
