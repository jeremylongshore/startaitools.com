+++
title = 'IRSB v1.1.0: CLI Verify, x402 Payment Protocol, and the SDK Rename'
slug = 'irsb-sdk-cli-x402-payment-protocol-v110'
date = 2026-01-30T10:00:00-06:00
draft = false
tags = ["irsb", "cli", "x402", "erc-8004", "npm", "release-engineering", "typescript", "blockchain"]
categories = ["Development Journey"]
description = "Nineteen commits across four repos: the irsb CLI gets a verify command, x402 payment protocol lands, ERC-8004 credibility publishing ships, and the SDK renames from intent-solutions to irsb."
+++

Nineteen commits across four repos. The biggest chunk — fifteen commits — went into IRSB itself, pushing through a CLI expansion, a payment protocol, a credibility standard, and a versioned release. The remaining four touched IntentVision, jeremylongshore.com, and PipelinePilot.

## The irsb CLI and Receipt Verification

The CLI got a `verify` command. Until now, verifying an on-chain receipt meant calling the `IntentReceiptHub` contract directly — either through Etherscan or a custom script. The verify command wraps the contract read into a single invocation:

```bash
irsb verify --receipt-id 0x7a3f... --chain sepolia
```

It pulls the receipt from the hub contract, validates the signature against the registered solver, checks the challenge window status, and returns a structured result. The receipt verification module handles the full validation pipeline: signature recovery, solver registration lookup, timestamp bounds, and dispute status cross-reference.

This was part of Epic 1's auto-challenge implementation, which went through eight phases. Phases 1-4 covered the challenge workflow scaffolding — detecting expired challenge windows, submitting challenge transactions, and tracking challenge state. Phases 5-8 wired in the watchtower, which monitors receipts in real-time and triggers challenges automatically when a receipt violates policy constraints.

The watchtower scaffold is exactly that — a scaffold. It watches for `ReceiptSubmitted` events, evaluates each receipt against a policy ruleset, and queues challenges. The actual challenge submission and dispute resolution flow exists but hasn't been battle-tested against adversarial receipts yet.

The eight-phase structure was deliberate. Each phase shipped independently — phases 1-4 could land without the watchtower existing. That meant the CLI verify command was useful from day one, even before auto-challenge was wired up. Incremental delivery on protocol features is harder than it sounds because smart contract interfaces can't change after deployment. Getting the phase boundaries right meant thinking about contract immutability upfront.

## x402 Payment Protocol

x402 brings HTTP-native payments to IRSB. The idea: an AI agent hits an API endpoint, gets a `402 Payment Required` response with a payment envelope, negotiates the payment through a facilitator contract, and retries the request with a payment proof header.

The facilitator contract handles escrow. The agent deposits funds, the service provider delivers the response, and the facilitator releases payment upon confirmation. If the service doesn't deliver, the agent can reclaim after a timeout. Standard escrow mechanics, but encoded in Solidity and integrated into the IRSB receipt pipeline — every x402 payment generates a verifiable receipt.

This matters because AI agents are going to spend money. They already do through tool calls that hit paid APIs. x402 puts that spending on-chain where it can be audited, bounded by spend limits, and disputed if the service was never rendered.

## ERC-8004 Credibility Publishing

ERC-8004 is a credibility standard for on-chain entities. A solver registers its credibility score — computed from receipt history, dispute outcomes, and bond amounts — and any consumer can read it before delegating work.

The publishing flow: the solver calls `publishCredibility()` with a signed attestation, the contract verifies the attestation against the solver's registered key, and stores the score with a timestamp. Consumers call `getCredibility(solverAddress)` and get back the score, timestamp, and attestation hash.

It's a reputation primitive. Not a full reputation system — there's no decay, no weighting, no aggregation across chains. Just a signed score that a solver publishes and anyone can read. The minimal version ships first; complexity gets added when there's evidence it's needed.

## SDK Rename and npm Provenance

The package formerly known as `@intent-solutions-io/irsb` is now just `irsb` on npm. The scope change reflects a branding decision — IRSB is the product name, not Intent Solutions. Every import path changed:

```typescript
// Before
import { ReceiptHub } from '@intent-solutions-io/irsb';

// After
import { ReceiptHub } from 'irsb';
```

npm provenance got enabled at the same time. Every published package now includes a Sigstore-signed provenance attestation linking the package contents to the specific GitHub Actions workflow run that built it. You can verify that the tarball on npm matches the source code on GitHub without trusting the publisher.

The v1.1.0 release bundles all of this: CLI verify, x402 facilitator, ERC-8004 publisher, SDK rename, and provenance. Tagged, changelog'd, and published.

## The Rest of the Day

**IntentVision** (1 commit): Repository rename and PR workflow update. Housekeeping that needed doing after the org restructure.

**jeremylongshore.com** (2 commits): Visibility updates to the personal site. Content changes, not architecture.

**PipelinePilot** (1 commit): `.env` security fix. Credentials were committed to the repo. They're now in `.env.example` with placeholder values and `.env` is in `.gitignore`. The kind of fix that takes five minutes and prevents a very bad day.

## What Stuck

**Ship the CLI verb early.** The verify command could have waited for the full auto-challenge pipeline. But having `irsb verify` available immediately changed how I tested everything else — x402 receipts, credibility attestations, challenge workflows. A CLI that reads on-chain state is the fastest feedback loop you can build.

**npm provenance is free insurance.** Enabling it took one line in the GitHub Actions workflow. The supply chain attack surface for npm packages is real, and provenance attestations close the gap between "I published this" and "this came from that commit." No reason not to do it on day one.

---

**Related Posts:**
- [IRSB Monorepo v1.0.0: Extracting Shared Packages](/posts/irsb-monorepo-v1-extracting-shared-packages/) — the monorepo migration and scoped npm rename that preceded this release
- [Deep Dive Part 1: Five On-Chain Enforcers](/posts/irsb-deep-dive-1-on-chain-enforcement/) — the enforcer architecture that x402 and auto-challenge build on
- [New Year's Eve: A Go CLI, a Security Fix, and Two Releases](/posts/new-years-eve-go-cli-security-fix-two-releases/) — similar multi-repo day with a security fix pattern
