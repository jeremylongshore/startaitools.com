+++
title = 'Deep Dive Part 3: A 12-Package Nested Monorepo That Watches AI Agents for You'
slug = 'irsb-deep-dive-3-watchtower-architecture'
date = 2026-03-27T15:00:00-05:00
draft = false
tags = ["irsb", "typescript", "monitoring", "architecture", "monorepo", "ai-agents", "claude-code", "devops"]
categories = ["IRSB Deep Dive"]
description = "Inside the IRSB Watchtower: a 12-package pnpm monorepo with evidence verification, behavior signal derivation, risk scoring, and auto-dispute — ~500 tests of deterministic monitoring."
toc = true
+++

Posting an on-chain receipt for a completed AI agent job is not the same as monitoring the receipt. Receipts are inert data. They do not check themselves for hash mismatches, verify that artifact files actually exist, or notice when an agent's behavioral profile starts drifting toward anomalous territory. They certainly do not file a dispute within the 1-hour challenge window when something looks wrong.

That gap -- between "we have on-chain evidence" and "we are actively verifying it and acting on it" -- is exactly the space the IRSB Watchtower occupies. It is a fully autonomous monitoring system that watches agent activity, verifies evidence integrity, derives behavioral signals, computes risk scores, and triggers disputes without human intervention. At v0.5.0 it has approximately 500 tests covering its deterministic logic. The chain integration uses mock data while real IRSB client wiring is completed, but all the monitoring logic itself is production-grade.

This is Part 3 of the [IRSB Ecosystem Deep Dive](/irsb-ecosystem/) series. [Part 1](/posts/irsb-deep-dive-1-on-chain-enforcement/) covered on-chain enforcement and the contract architecture. [Part 2](/posts/irsb-deep-dive-2-evidence-pipeline/) covered the evidence pipeline from submission to verification.

---

## Why a Watchtower

The protocol layer handles enforcement mechanically: bonds are locked, receipts are posted, disputes can be opened. But the protocol does not know whether a receipt is fraudulent. It cannot tell whether an artifact hash was fabricated, whether a manifest was tampered with, or whether an agent has been exhibiting a slow pattern of small violations that individually fall below alert thresholds.

Someone needs to know. And that someone needs to act within time constraints. The IRSB challenge window is one hour. If a fraudulent receipt goes unchallenged in that window, it is accepted and the bond is unlocked. A human operator watching a dashboard is not a reliable system. Sleep, context switching, alert fatigue -- any of these can cause a missed challenge.

The Watchtower runs a continuous scan cycle. It fetches the current block, creates a chain context, runs every registered rule against that context, collects findings, and either simulates or executes the resulting actions. When a CRITICAL risk signal is detected, the score is automatically set to 100 and the dispute path is triggered. The operator is notified via webhook. The challenge is filed on-chain.

The key design constraint is that all of this must be deterministic and auditable. Every finding, every action, every ledger entry is persisted in JSONL format so the reasoning behind any dispute can be reconstructed from first principles.

---

## 12-Package Architecture

The Watchtower lives in a nested pnpm monorepo with nine packages and three application entrypoints. The dependency graph is intentional: application layers only depend downward into the infrastructure packages, never sideways.

```
apps/worker → core, config, chain, irsb-adapter, evidence-store, metrics, webhook
apps/api    → core, config, chain, irsb-adapter, metrics, signers
apps/cli    → config, chain, irsb-adapter
irsb-adapter → config, resilience
```

The three apps are thin orchestration layers. The real logic lives in the packages. This separation means the rule engine, evidence verification, and risk scoring are all independently testable without spinning up a node connection or a Fastify server.

The nine packages break down by responsibility:

- **core** -- The rule engine, Finding schema, and ActionExecutor. Zero cloud dependencies. This package runs identically in test and production.
- **config** -- Zod schemas for all configuration. Nothing touches environment variables without going through here first.
- **chain** -- A viem abstraction layer. All block fetching, transaction submission, and event reading is isolated here. Mock implementations swap in for tests.
- **irsb-adapter** -- The contract client for the IRSB protocol. Currently wraps mock chain data while real IRSB client integration is pending.
- **evidence-store** -- JSONL persistence for findings and action ledger entries. Append-only, deterministic, readable with any text tool.
- **metrics** -- Prometheus instrumentation. Scan cycle duration, finding counts by severity, action outcomes.
- **webhook** -- HMAC-signed delivery of findings and alerts to operator endpoints.
- **resilience** -- Retry logic with exponential backoff and a circuit breaker for chain RPC calls.
- **signers** -- Pluggable signing backends. `LocalPrivateKey` for development and testing. `CloudKMSSigner` is scaffolded but cloud integration is pending -- all current deployments use the local key path.

The three application packages are `watchtower-api` (a Fastify REST API for querying findings and agent risk reports), `watchtower-cli` (utilities for inspecting the evidence store and triggering manual scans), and `watchtower-core` (the worker process that drives the scan loop).

This architecture pays for itself in testability. The ~500 tests can exercise `verifyEvidence()`, `scoreAgent()`, and `RuleEngine.execute()` without any network calls because chain and contract dependencies are injected interfaces with mock implementations.

---

## Evidence Verification

When the Watchtower processes a receipt, it does not take the claimed hash values at face value. It re-derives them. The `verifyEvidence()` function is a sequential pipeline of six checks, each with a specific failure code. The first failure short-circuits the pipeline to avoid misleading downstream results.

```typescript
export function verifyEvidence(
  receipt: NormalizedReceipt,
  runDir: string,
  options?: VerifyOptions,
): VerificationResult {
  const failures: VerificationFailure[] = [];
  const evidenceLinks: EvidenceLink[] = [
    { type: 'receiptId', ref: receipt.receiptId },
    { type: 'manifestSha256', ref: receipt.manifestSha256 },
  ];

  // 1. Path safety — block traversal, null bytes, absolute paths
  const pathCheck = validateRelativePath(receipt.manifestPath);
  if (!pathCheck.valid) {
    failures.push({ code: 'UNSAFE_PATH', message: `Manifest path unsafe: ${pathCheck.reason}` });
    return buildResult(failures, evidenceLinks);
  }

  // 2. Manifest exists and within size limit
  // 3. SHA-256 hash matches receipt claim
  // 4. JSON parse + Zod schema validation
  // 5. delivered[] matches manifest artifacts
  // 6. Each artifact: path safe, exists, size matches, hash matches

  return buildResult(failures, evidenceLinks);
}
```

The path safety check deserves emphasis. Before any file is read, the path is validated against three attack patterns: directory traversal sequences (`../` and encoded variants), null bytes, and absolute paths. A receipt that claims its manifest lives at `../../../../etc/passwd` should not trigger a filesystem read. It should produce an `UNSAFE_PATH` failure immediately.

The twelve failure codes map precisely to where in the pipeline the verification broke down:

| Code | Stage |
|------|-------|
| `UNSAFE_PATH` | Path safety validation |
| `MANIFEST_NOT_FOUND` | File existence check |
| `MANIFEST_TOO_LARGE` | Size limit enforcement |
| `MANIFEST_READ_ERROR` | Filesystem I/O |
| `MANIFEST_PARSE_FAIL` | JSON deserialization |
| `MANIFEST_SCHEMA_INVALID` | Zod schema validation |
| `MANIFEST_HASH_MISMATCH` | SHA-256 re-derivation |
| `DELIVERED_MISMATCH` | Artifact list reconciliation |
| `ARTIFACT_NOT_FOUND` | Artifact file existence |
| `ARTIFACT_TOO_LARGE` | Artifact size limit |
| `ARTIFACT_SIZE_MISMATCH` | Declared vs actual size |
| `ARTIFACT_HASH_MISMATCH` | Artifact SHA-256 re-derivation |

A `MANIFEST_HASH_MISMATCH` means the manifest file exists and is valid JSON but the content no longer matches what the solver claimed when posting the receipt. This is either tampering or a re-run that overwrote the evidence directory. Either way, the Watchtower opens a finding.

---

## Behavior Signal Derivation

Evidence verification catches integrity failures on individual receipts. Behavior signal derivation operates at a higher level: it watches the pattern of an agent's activity over time and flags anomalies that would not be visible in any single receipt.

The system derives ten signals from the combination of receipts, evidence verification results, and chain events. Each signal carries a severity level and a weight. The severity levels drive automated response thresholds:

```typescript
const SEVERITY_POINTS: Record<string, number> = {
  LOW: 5,
  MEDIUM: 15,
  HIGH: 30,
  CRITICAL: 60,
};
```

A `CRITICAL` signal does not feed into the score calculation. It overrides it. Any CRITICAL signal in a snapshot window sets the overall risk to 100 regardless of math. This is a deliberate choice: certain behaviors (fabricated hashes, challenge window violations, bond manipulation) are not "high risk" -- they are categorical failures that require immediate action.

`LOW` signals are informational. An agent that occasionally runs close to its time budget or posts receipts slightly late in a window accumulates LOW signals. These do not trigger automated disputes but they do appear in the risk report and contribute to the composite score. A pattern of consistent LOW signals can push a score into the range that triggers an alert even without any individual HIGH or CRITICAL finding.

The weight field on each signal handles the case where multiple signals of the same type fire in a short window. Rather than counting each occurrence as a fresh independent data point, the weighting system allows the scoring function to treat correlated signals with appropriate skepticism about their independence.

---

## Risk Scoring

The `scoreAgent()` function takes an agent record, a set of behavioral snapshots, and a timestamp. It produces a `RiskReport` and any new `Alert` objects that should be delivered to the operator.

```typescript
export function scoreAgent(
  agent: Agent, snapshots: Snapshot[], generatedAt: number,
): { report: RiskReport; newAlerts: Alert[] } {
  const allSignals = snapshots.flatMap((snap) => snap.signals);

  let rawScore = 0;
  let hasCritical = false;
  for (const signal of allSignals) {
    const points = SEVERITY_POINTS[signal.severity] ?? 0;
    rawScore += points * signal.weight;
    if (signal.severity === 'CRITICAL') hasCritical = true;
  }

  const overallRisk = hasCritical ? 100 : Math.min(100, Math.round(rawScore));

  // Confidence: HIGH if 5+ signals from 2+ snapshots
  // Alerts: CRITICAL_SIGNAL_DETECTED or HIGH_RISK_SCORE
  // Report ID: SHA-256 of canonical JSON payload
  // ...
}
```

The confidence calculation addresses a different problem: how much should the operator trust a risk score derived from limited data? A score of 75 computed from 12 signals across 4 scan windows is more reliable than the same score computed from 2 signals in a single window. The confidence level -- `LOW`, `MEDIUM`, or `HIGH` -- is surfaced in the report so operators can contextualize the score without digging into raw signal data.

Two alert types exist. `CRITICAL_SIGNAL_DETECTED` fires on any snapshot containing a CRITICAL severity signal. `HIGH_RISK_SCORE` fires when the numeric score reaches 80 or above, even if no individual signal is CRITICAL. The alert path triggers the webhook sink, which signs the payload with HMAC and delivers it to the configured operator endpoint.

The report ID is a SHA-256 hash of the canonical JSON payload (deterministic key ordering, no whitespace). This means if the same agent produces the same signals with the same weights, it produces the same report ID. Idempotency is enforced at the action ledger level using this ID.

---

## The IRSBHook: EIP-8183 Bridge

The contracts layer exposes `IRSBHook`, which bridges the EIP-8183 Agentic Commerce Protocol job lifecycle into the IRSB accountability pipeline. Every significant job event -- acceptance, result submission, completion, rejection -- triggers a corresponding IRSB operation automatically.

```solidity
contract IRSBHook is IACPHook {
    function afterAction(uint256 jobId, TypesACP.Action action, address caller) external override {
        if (action == TypesACP.Action.AcceptJob) _afterAcceptJob(jobId, caller);
        else if (action == TypesACP.Action.SubmitResult) _afterSubmitResult(jobId, caller);
        else if (action == TypesACP.Action.CompleteJob) _afterCompleteJob(jobId);
        else if (action == TypesACP.Action.RejectJob) _afterRejectJob(jobId);
    }
}
```

The hook enforces accountability at each stage. On `AcceptJob`, it verifies the solver is registered in the IRSB registry and locks a proportional bond. The bond size is computed from the job value -- larger jobs require larger bonds, creating an economic incentive for accuracy that scales with stakes.

On `SubmitResult`, the hook auto-posts a V1 receipt through the trusted hook path. This is distinct from a solver manually posting a receipt: the hook path has elevated trust because the contract itself is attesting to the submission, not an external call that could be spoofed.

On `CompleteJob`, the bond is unlocked. On `RejectJob`, the dispute path opens automatically. The Watchtower monitors chain events from the hook and uses them as inputs to the behavioral signal derivation pipeline.

All of this is deployed on Sepolia testnet. The contracts are not on mainnet. The hook path is under active development and the Watchtower's IRSB client integration is the next milestone before any mainnet consideration.

---

## Resilience Patterns

A monitoring system that goes down when the thing it monitors is under stress is not useful. The resilience package addresses three failure modes.

The circuit breaker wraps all chain RPC calls. If the chain node returns errors above a threshold rate, the circuit opens and the Watchtower stops attempting calls for a configured backoff window. This prevents the scan loop from hammering a degraded RPC endpoint and producing a backlog of failed requests that would overwhelm the system when connectivity recovers. When the circuit is open, the worker emits a metric and continues its loop -- it does not crash.

Retry logic with exponential backoff handles transient failures: network blips, rate limits, momentary RPC unavailability. The retry policy is configurable per operation type. Evidence store writes use aggressive retry because data loss is worse than latency. Webhook delivery uses moderate retry because the operator endpoint may legitimately be down during planned maintenance.

`DRY_RUN` mode is mandatory for new deployments. When `DRY_RUN=true`, the ActionExecutor simulates every action -- dispute filings, bond operations, webhook deliveries -- without submitting transactions or making external calls. All findings are logged. The action ledger records what would have happened. Operators can run the Watchtower against a real chain context for as long as they need to validate that the rules are producing sensible findings before enabling live execution.

This is not optional. `DRY_RUN=false` requires an explicit configuration change. The design treats production execution as an opt-in after validation, not the default.

---

## The Data Flow

A complete Watchtower scan cycle, from trigger to persisted output:

1. **Worker** initiates a scan on the configured block interval.
2. **IrsbClient** calls `getBlockNumber()` to establish the current chain position (mock data in v0.5.0).
3. **createChainContext()** assembles the block number, recent receipts, and agent registry snapshot into a context object.
4. **RuleEngine.execute(context)** runs every registered rule against the context. Each rule returns zero or more `Finding` objects.
5. **ActionExecutor** receives the findings. In `DRY_RUN` mode, it logs planned actions. In live mode, it submits transactions and calls external APIs.
6. **ActionLedger** records each action with its report ID. Idempotency check here: if the same report ID has already been acted on, the action is skipped.
7. **EvidenceStore** appends findings to JSONL. This is the permanent audit record.
8. **WebhookSink** fires for CRITICAL signals and HIGH_RISK_SCORE alerts. Payload is HMAC-signed with the operator's configured secret.
9. **Metrics** records scan duration, finding counts by severity, and action outcomes to Prometheus.

The JSONL persistence format is intentional. It is readable without tooling, appendable without locking, and trivially importable into any data pipeline. If a dispute is ever challenged on-chain and the operator needs to reconstruct the evidence trail, the answer is `cat evidence-store.jsonl | grep <receiptId>`.

---

## What Comes Next

The IRSB Ecosystem Deep Dive is a four-part series:

- [Part 1](/posts/irsb-deep-dive-1-on-chain-enforcement/) -- 37 Solidity contracts, bond mechanics, and the receipt format
- [Part 2](/posts/irsb-deep-dive-2-evidence-pipeline/) -- Submission, normalization, and the evidence store
- **Part 3 (this post)** -- Watchtower architecture, evidence verification, and risk scoring
- Part 4 (coming soon) -- Z3 formal verification, the three-layer stack, and the pivot story

The Watchtower at v0.5.0 is code-complete for the monitoring logic with approximately 500 tests across the package suite. The next milestone is wiring the real IRSB client so the chain context uses live Sepolia data instead of mocks, followed by promoting the Cloud KMS signer from scaffolding to integration-tested status. After that, the path to a testnet production deployment is short.

The broader thesis behind this work is that AI agent accountability cannot rely on trust-and-verify with humans in the loop. The challenge windows are too short, the agent volume is too high, and the failure modes are too varied. Automated monitoring with deterministic, auditable logic and mandatory dry-run validation before live execution is the only architecture that scales. The Watchtower is what that looks like in practice.

---

*Part of the [IRSB Ecosystem](/irsb-ecosystem/) deep dive series. Built with [Claude Code](https://claude.ai/code).*
