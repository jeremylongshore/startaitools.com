+++
title = 'Deep Dive Part 2: Cryptographic Receipts and the Evidence Pipeline That Proves What AI Agents Actually Did'
slug = 'irsb-deep-dive-2-evidence-pipeline'
date = 2026-03-27T14:00:00-05:00
draft = false
tags = ["irsb", "typescript", "solidity", "cryptography", "ai-agents", "claude-code", "cloud-kms"]
categories = ["IRSB Ecosystem Deep Dive"]
description = "How the IRSB Solver creates SHA-256 evidence bundles, signs them with Cloud KMS, and posts cryptographic receipts on-chain — creating an unforgeable audit trail for AI agent work."
toc = true
+++

"Trust me, the AI did good work." That is the state of most AI agent frameworks today. The agent completes a task, your logs say it finished, and you are left reconstructing what actually happened from console output and hope. There is no cryptographic commitment. There is no unforgeable record. There is nothing to challenge.

The [IRSB Ecosystem](/irsb-ecosystem/) is built on the premise that claimed work and proved work are not the same thing. The evidence pipeline is the mechanism that closes that gap. It does not ask you to trust the solver. It asks you to verify the hash.

This is Part 2 of the [IRSB Ecosystem Deep Dive](/irsb-ecosystem/) series. [Part 1](/posts/irsb-deep-dive-1-on-chain-enforcement/) covered the on-chain enforcement layer -- the five enforcers, the solver registry, and the bond mechanics that make violations expensive. This part covers what happens between intent arrival and the receipt that lands on-chain: the policy gate, the evidence bundle, the Cloud KMS signature, and the replay-protected receipt posting.

The Solver is code-complete at v0.3.0 with 139 tests. It is not yet deployed to production infrastructure.

---

## From Intent to Receipt

Every piece of work in IRSB starts as an intent: a normalized structure describing what needs to happen, who requested it, when it expires, and what inputs to operate on. The solver receives that intent and processes it through a linear pipeline before anything reaches the chain.

The pipeline has five stages:

1. **Policy gate** -- Four deterministic checks decide whether the intent is allowed to execute at all.
2. **Execution** -- The solver performs the actual work.
3. **Evidence bundle creation** -- Every output artifact is SHA-256 hashed. A canonical manifest is assembled and hashed.
4. **Cloud KMS signing** -- The manifest hash is signed using a hardware-backed key that never leaves Google's infrastructure.
5. **On-chain receipt posting** -- The signature and hashes are posted to `IntentReceiptHub` with replay protection.

The key insight is that the evidence bundle is created before the signature. The solver cannot sign a favorable summary of what happened. It signs a hash of the actual artifacts -- every file, every output -- as they exist on disk. If the artifacts are altered after signing, the hash mismatch is immediately detectable by anyone who re-hashes the outputs.

---

## The Policy Gate: Four Checks

Before any work begins, the solver runs `evaluatePolicy()`. The function is deliberately simple: four independent checks, all reasons accumulated, no early returns. If any check fails, the intent is rejected with the full list of failure reasons -- not just the first one found.

```typescript
export function evaluatePolicy(
  intent: NormalizedIntent,
  config: ResolvedConfig
): PolicyResult {
  const reasons: string[] = [];

  // Check 1: jobType allowlisted
  if (!config.POLICY_JOBTYPE_ALLOWLIST.includes(intent.jobType)) {
    reasons.push(`jobType '${intent.jobType}' not in allowlist`);
  }

  // Check 2: expiresAt not in the past
  if (intent.expiresAt) {
    const expiresAt = new Date(intent.expiresAt);
    if (expiresAt.getTime() < Date.now()) {
      reasons.push(`intent expired at ${intent.expiresAt}`);
    }
  }

  // Check 3: requester allowlist (if configured)
  if (config.POLICY_REQUESTER_ALLOWLIST) {
    if (!config.POLICY_REQUESTER_ALLOWLIST.includes(intent.requester)) {
      reasons.push(`requester '${intent.requester}' not in allowlist`);
    }
  }

  // Check 4: size guard
  const inputsJson = canonicalJson(intent.inputs);
  const maxBytes = config.POLICY_MAX_ARTIFACT_MB * 1024 * 1024;
  if (inputsJson.length > maxBytes) {
    reasons.push(`inputs size ${inputsJson.length} exceeds max ${maxBytes}`);
  }

  return { allowed: reasons.length === 0, reasons };
}
```

The four checks cover the most common failure modes in agent work:

- **jobType allowlist** -- The solver only processes work it explicitly knows how to do. An unknown job type is rejected, not attempted and failed.
- **expiry check** -- Stale intents are rejected at the gate. A solver should not act on instructions that were issued for a time window that has already passed.
- **requester allowlist** -- Optional, but when configured, it prevents intents from unauthorized sources from entering the execution pipeline at all.
- **size guard** -- A ceiling on serialized input size prevents resource exhaustion and makes inputs auditable. If inputs are too large to hash in bounded time, the pipeline should not accept them.

Accumulating all failure reasons rather than short-circuiting is a deliberate design choice. Callers get a complete diagnostic in one pass, which matters when debugging why an intent was rejected in a production pipeline.

---

## Evidence Bundle Creation

Once the solver completes work, `createEvidenceBundle()` scans the output directory, hashes every artifact, assembles a manifest, and hashes the manifest itself. The manifest is the single source of truth for what the solver produced.

```typescript
export async function createEvidenceBundle(
  params: CreateEvidenceBundleParams
): Promise<EvidenceBundleResult> {
  const { runDir, intentId, runId, jobType, policyDecision, executionSummary, gitCommit } = params;

  const artifacts = await scanArtifacts(runDir);

  const manifest: EvidenceManifestV0 = {
    manifestVersion: MANIFEST_VERSION,
    intentId, runId, jobType,
    createdAt: new Date().toISOString(),
    artifacts,
    policyDecision,
    executionSummary,
    solver: { service: "irsb-solver", serviceVersion: SERVICE_VERSION, gitCommit },
  };

  const manifestSha256 = computeManifestHash(manifest);

  const evidenceDir = join(runDir, "evidence");
  ensureDir(evidenceDir);
  atomicWrite(join(evidenceDir, "manifest.json"), canonicalJson(manifest) + "\n");
  atomicWrite(join(evidenceDir, "manifest.sha256"), manifestSha256 + "\n");

  return { manifest, manifestPath: join(evidenceDir, "manifest.json"), manifestSha256 };
}
```

Three implementation details matter here:

**Canonical JSON.** Standard `JSON.stringify()` does not guarantee key ordering across environments or runtimes. `canonicalJson()` produces a deterministically ordered serialization. The same manifest data always produces the same bytes, which always produces the same SHA-256 hash. Without this, a manifest serialized on one machine might hash differently on another -- breaking verification.

**Path-sorted artifact entries.** The `scanArtifacts()` function returns entries sorted by file path. This ensures that adding or removing files changes the manifest hash in a detectable way, and that the artifact list is stable regardless of filesystem enumeration order.

**Atomic writes.** The manifest and its hash file are written atomically. An observer cannot read a partially written manifest and compute a hash that does not match the final file.

The `policyDecision` field is included in the manifest. This means the policy gate outcome -- every rejection reason, or the explicit allowed signal -- is part of the signed artifact. A receipt therefore commits not just to what work was done, but to the fact that the policy gate was passed.

---

## Cloud KMS Signing

The manifest hash is signed using Google Cloud KMS rather than a local private key. This choice is not arbitrary.

Local private keys are files on disk. They can be copied, stolen, or leaked. A solver operator who wants to forge a receipt can do so if they control the signing key. Cloud KMS stores keys in hardware security modules. The private key material never leaves Google's infrastructure. The operator can request a signature, but cannot extract the key.

The practical consequence: a signature produced by Cloud KMS proves that the signing request was made by an authorized IAM principal at a specific point in time, and that the key was not compromised. GCP audit logs record every signing operation. The signing authority is traceable.

The signing flow works as follows: the manifest hash is passed to the KMS `asymmetricSign` API, which returns a DER-encoded signature. DER is the standard encoding for ECDSA signatures from hardware systems, but Ethereum expects `r`, `s`, and `v` components. The solver parses the DER, normalizes `s` to its low form, and computes the recovery parameter.

```typescript
function parseDerSignature(der: Buffer): { r: bigint; s: bigint } {
  if (der[0] !== 0x30) throw new Error(`Invalid DER: expected 0x30`);
  let offset = 2;

  if (der[offset] !== 0x02) throw new Error('Invalid DER: expected 0x02 for r');
  offset++;
  const rLen = der[offset]!; offset++;
  const rBytes = der.subarray(offset, offset + rLen); offset += rLen;

  if (der[offset] !== 0x02) throw new Error('Invalid DER: expected 0x02 for s');
  offset++;
  const sLen = der[offset]!; offset++;
  const sBytes = der.subarray(offset, offset + sLen);

  return {
    r: BigInt(`0x${Buffer.from(rBytes).toString('hex')}`),
    s: BigInt(`0x${Buffer.from(sBytes).toString('hex')}`),
  };
}
```

The DER structure is straightforward: a `0x30` sequence header, followed by two ASN.1 integers for `r` and `s`. Each integer is prefixed with `0x02` and a length byte. The parser reads these fields sequentially, handling the variable-length encoding correctly.

---

## EIP-2 Low-S Normalization

After parsing `r` and `s` from the DER signature, the solver normalizes `s` to its low form. This step is required for Ethereum compatibility.

The secp256k1 curve has a symmetry property: for any signature `(r, s)`, the value `(r, curve_order - s)` is also a valid signature for the same message and key. This means every signature has two valid representations. Without normalization, the same signing operation produces different bytes depending on which representation the signing hardware returns. Applications that index or deduplicate by signature bytes would treat them as different signatures.

More importantly, transaction malleability exploits rely on this property. A malicious relay can mutate a signature from its high-S form to its low-S form (or vice versa) without invalidating it, changing the transaction ID without changing what the transaction does. EIP-2 (and Bitcoin's BIP-62) eliminate this by requiring `s <= curve_order / 2`.

```typescript
const SECP256K1_N = BigInt('0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141');
const SECP256K1_HALF_N = SECP256K1_N / 2n;

// In signHashComponents():
const { r, s: rawS } = parseDerSignature(sigBytes);
const sNormalized = rawS > SECP256K1_HALF_N;
const s = sNormalized ? SECP256K1_N - rawS : rawS;
const v = await this.computeRecoveryV(digestBuffer, r, s, sNormalized);
```

If `rawS` is greater than half the curve order, the solver flips it: `s = curve_order - rawS`. The boolean `sNormalized` records whether the flip occurred, which is needed to compute the correct recovery parameter `v`. The recovery parameter tells the verifier which of the two possible public keys corresponds to the private key that produced this signature -- it is the tiebreaker that makes `ecrecover` deterministic.

---

## On-Chain Receipt Posting

With a valid signature in hand, the solver posts a receipt to `IntentReceiptHub`. A receipt is not a log entry -- it is a permanent, challengeable record that commits the solver to specific claims about what work was done.

```solidity
function postReceipt(Types.IntentReceipt calldata receipt, uint256 declaredVolume)
    external whenNotPaused nonReentrant returns (bytes32 receiptId)
{
    // Validate solver is active and has sufficient bond
    Types.Solver memory solver = solverRegistry.getSolver(receipt.solverId);
    if (solver.status != Types.SolverStatus.Active) revert InvalidSolver();

    // PM-EC-001: Bond must cover declared volume
    uint256 requiredBond = solverRegistry.requiredBondForVolume(declaredVolume);
    if (solver.bondBalance < requiredBond) revert InsufficientBondForVolume();

    receiptId = computeReceiptId(receipt);
    if (_receipts[receiptId].exists) revert ReceiptAlreadyExists();

    // IRSB-SEC-006: Replay protection with chainId + contract address + nonce
    bytes32 messageHash = keccak256(abi.encode(
        block.chainid, address(this), currentNonce,
        receipt.intentHash, receipt.constraintsHash, receipt.routeHash,
        receipt.outcomeHash, receipt.evidenceHash,
        receipt.createdAt, receipt.expiry, receipt.solverId
    ));
    address signer = messageHash.toEthSignedMessageHash().recover(receipt.solverSig);
    if (signer != solver.operator) revert InvalidReceiptSignature();

    _receipts[receiptId] = receipt;
    _receiptStatus[receiptId] = Types.ReceiptStatus.Pending;
    // ... indexing, nonce increment, event emission
}
```

Several security properties are encoded in the message hash:

**Chain ID (IRSB-SEC-001).** Including `block.chainid` in the signed message means a signature produced for Sepolia cannot be replayed on mainnet. This is elementary but critical -- without it, a valid testnet receipt becomes a valid mainnet receipt.

**Contract address.** Including `address(this)` means a signature for one deployment of `IntentReceiptHub` cannot be replayed against a different deployment. Upgrading the contract address invalidates all prior signatures.

**Nonce (IRSB-SEC-006).** Including `currentNonce` means each receipt posting is unique even if the same intent hash, evidence hash, and outcome hash appear again. The nonce is incremented after each successful posting.

The bond check enforces a key invariant: the solver must have posted a bond sufficient to cover the declared work volume before the receipt is accepted. If a solver's bond balance has been slashed below the required threshold, they cannot post new receipts until they re-stake. This is the economic coupling that makes receipts meaningful -- posting a receipt is an assertion backed by locked capital.

The `IntentReceiptHub` is deployed on Sepolia testnet at `0xD66A1e880AA3939CA066a9EA1dD37ad3d01D977c`.

---

## Challenge, Dispute, and Finalization

A receipt does not become final the moment it is posted. It enters a one-hour challenge window during which anyone can dispute it. This is the mechanism that makes receipts more than self-reported claims.

The lifecycle has four states:

- **Pending** -- Receipt posted, challenge window open (default: 1 hour).
- **Disputed** -- A challenger has posted a bond and raised a dispute.
- **Finalized** -- Challenge window elapsed with no dispute, or a dispute was resolved in the solver's favor. The solver's reputation score increases.
- **Slashed** -- A dispute was resolved against the solver. The solver's bond is slashed in proportion to the violation; the challenger receives a bounty.

The `DisputeModule` handles two resolution paths: deterministic and arbitrated. Deterministic resolution covers cases where the outcome can be computed from on-chain data alone -- a timeout (the challenge window elapsed), an invalid signature (the evidence hash does not match the submitted artifacts), or a replay (the same receipt hash appears twice). These cases resolve without human involvement.

For disputes that cannot be resolved deterministically -- a challenger claims the work was wrong but the hash is valid -- the dispute escalates to an arbitration pool. The arbitrators review the evidence bundle off-chain, post their determination on-chain, and the smart contract enforces the outcome.

This architecture separates two concerns that most systems conflate: verifying that the work was committed to (cryptographic) and verifying that the committed work was correct (judgment). The evidence pipeline handles the first problem completely. The dispute module handles the second.

---

## Why This Matters

Any AI agent framework can log "task completed." The log entry says the work happened. It does not prove what work happened, what outputs were produced, or that the agent reporting completion is the same agent that performed the work.

The IRSB evidence pipeline addresses a different question: not whether work was done, but what exactly was done and who can be held accountable if it was wrong.

When a solver posts a receipt, it is not logging a claim. It is cryptographically committing to a SHA-256 hash of every artifact it produced. That commitment is signed by a Cloud KMS key whose usage is audit-logged by Google. That signature is posted on-chain with replay protection, bonded capital as a stake, and a challenge window. Anyone can re-hash the artifacts and verify that the on-chain hash matches. Anyone can check the Sepolia transaction. No permissions required.

The provenance chain is complete: intent arrives, policy gate passes, work executes, artifacts are hashed, manifest is signed with a hardware-backed key, receipt goes on-chain. At each step, the prior step is committed to. Altering any part of the chain -- the artifacts, the manifest, the signature -- breaks the next link.

The ecosystem is code-complete and not yet in production. The contracts are on Sepolia. The Solver has 139 passing tests. The Watchtower (Part 3) uses mock chain data while real IRSB client integration is pending. The infrastructure is not yet live, but the cryptographic design is fully specified and tested.

---

## What Comes Next

This series has four parts:

- [Part 1: Five On-Chain Enforcers That Make AI Agent Wallets Structurally Safe](/posts/irsb-deep-dive-1-on-chain-enforcement/) -- the enforcement contracts, the bond mechanics, and the three-strikes jail.
- **Part 2: Cryptographic Receipts and the Evidence Pipeline** (this post) -- the solver's policy gate, SHA-256 evidence bundles, Cloud KMS signing, and on-chain receipt posting.
- [Part 3: A 12-Package Nested Monorepo That Watches AI Agents for You](/posts/irsb-deep-dive-3-watchtower-architecture/) -- the Watchtower's architecture, its ten behavior signals, the risk scoring engine, and the auto-dispute pipeline.
- [Part 4: Z3 Formal Verification, the Three-Layer Stack, and Claude Code as Architect](/posts/irsb-deep-dive-4-ai-agent-pivot/) -- the FormalAgentVerifier, Scout's brokering layer, and what it looks like to build a protocol-layer system collaboratively with an AI.

The underlying thesis is that AI agents with economic agency require economic accountability. Claimed work is worthless at protocol scale. Proved work -- hashed, signed, bonded, and challengeable -- is the foundation that makes agentic commerce viable.

---

*Part of the [IRSB Ecosystem](/irsb-ecosystem/) deep dive series. Built with [Claude Code](https://claude.ai/code).*
