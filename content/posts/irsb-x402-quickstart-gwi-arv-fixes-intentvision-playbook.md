+++
title = 'x402 Quickstart, GWI ARV Fixes, and the IntentVision DevOps Playbook'
slug = 'irsb-x402-quickstart-gwi-arv-fixes-intentvision-playbook'
date = 2026-01-31T10:00:00-06:00
draft = false
tags = ["irsb", "x402", "git-with-intent", "intentvision", "devops", "documentation", "ci-cd", "solidity"]
categories = ["Development Journey"]
description = "Twenty-two commits across five repos: a 30-minute x402 quickstart, ARV gate fixes for git-with-intent, a react-router XSS patch, and an operator-grade execution plan for IntentVision."
+++

Twenty-two commits. Five repos. The kind of day where no single project gets a dramatic breakthrough but every project gets meaningfully better. IRSB led with thirteen commits of documentation and CI stabilization. git-with-intent got three targeted fixes. IntentVision got a real execution plan.

## x402: The 30-Minute Quickstart

The x402 payment protocol shipped yesterday. Today it got a quickstart guide designed to take a developer from zero to a working payment flow in 30 minutes.

The guide walks through four steps: deploy a local facilitator contract on Hardhat, configure an agent with x402 payment capability, hit a 402-protected endpoint, and verify the payment receipt on-chain. Each step has copy-pasteable code and expected output.

Writing quickstart guides forces you to confront your own API surface. Two things came out of the process: the facilitator deployment needed a helper script (three constructor arguments is two too many to remember), and the receipt verification step needed a human-readable output format instead of raw hex.

## Developer Tools Landing Page

IRSB's docs site got a developer tools landing page — a single entry point that routes to the quickstart, the adapter integration guide, the ERC-8004 publishing guide, and the CLI reference. Before this, developers had to know which doc they wanted. Now there's a table of contents with one-line descriptions.

The adapter integration guide covers how to wire IRSB receipts into an existing application. The pattern: implement the `ReceiptAdapter` interface, call `submitReceipt()` after your operation succeeds, and handle the three failure modes (no RPC, no signer, submission reverted). It's the same graceful degradation chain from Moat, extracted into a standalone guide.

The ERC-8004 publishing guide covers credibility score computation and on-chain attestation. A solver computes its score from three inputs: receipt count, dispute loss ratio, and current bond amount. The formula is deliberately simple — weighted average, no ML — because the score needs to be reproducible by any verifier.

## CI Fixes: Three Separate Problems

Three CI issues got fixed in the same afternoon. Each was independent, each was annoying.

**Stable Foundry pinning.** The Solidity CI was pulling `foundry-nightly`, which broke every few weeks when a nightly introduced a breaking change to `forge test` output formatting. Pinned to a specific stable release. CI should not depend on nightly toolchains.

**package-lock.json regeneration.** The TypeScript CI was failing because the lockfile was stale after the SDK rename. `npm ci` is strict about lockfile consistency — it won't auto-resolve mismatches like `npm install` does. Regenerated the lockfile from the updated `package.json` and committed it.

**Solidity formatting.** `forge fmt` was flagging formatting violations in test files that had been written before the formatter was configured. Ran the formatter across the full test directory and committed the result. Sixty files changed, zero logic changes.

## v2 Scope and Optimistic Dispute Docs

Two documentation-only commits captured forward-looking architecture decisions. The v2 scope document outlines what IRSB v2 looks like: multi-chain deployment (Base, Arbitrum, Polygon), a hosted indexer with GraphQL API, and a solver marketplace. None of this is committed code — it's a design doc that sets constraints for future work.

The optimistic dispute documentation explains the dispute resolution model. IRSB uses optimistic execution: receipts are assumed valid unless challenged within the challenge window. A challenger stakes a bond, provides evidence, and a resolver (currently a multisig, eventually a DAO) decides the outcome. The loser forfeits their bond. This is borrowed directly from Optimism's fault proof model, adapted for receipt disputes instead of state transitions.

## git-with-intent: ARV Gate and XSS Patch

Three commits, three distinct fixes.

**ARV gate fixes.** The Automated Review Verification gate was rejecting valid PRs because the score threshold was miscalibrated. Reviews with all checks passing but a "needs minor changes" comment were getting scored below the merge threshold. Adjusted the scoring weights so that informational comments don't tank the aggregate score.

**react-router XSS patch.** A dependency audit flagged a cross-site scripting vulnerability in react-router. The fix was a version bump — `react-router-dom` from 6.21.x to 6.22.x. The vulnerability required a specific URL pattern that the application didn't use, but unpatched dependencies in CI reports create noise that masks real issues.

**Dev tools docs.** Developer documentation for the GWI toolchain: how to set up a local development environment, run the test suite, and contribute. Standard contributor onboarding material that should have shipped with v0.3.0 but didn't.

## IntentVision: Operator-Grade Execution Plan

Three commits transformed IntentVision from "has a README" to "has a plan." The operator-grade execution plan breaks the product into six workstreams with dependencies, milestones, and staffing estimates. The DevOps playbook covers deployment topology (GKE Autopilot), observability stack (Cloud Monitoring + Loki), incident response runbooks, and on-call rotation.

This is the kind of work that doesn't produce features but makes future feature work predictable. Without an execution plan, every sprint starts with "what should we build next?" With one, sprints start with "here's what's next."

## The Rest

**Bounties** (1 commit): Tracker update. Active bounties refreshed with current status and payout amounts.

**jeremylongshore.com** (2 commits): Removed the No You Pick app. It was a side project that had been sitting on the personal site unused. Dead links to abandoned projects are worse than no links at all.

## What Stuck

**Write the quickstart before the reference docs.** The quickstart exposed two API ergonomics problems that would have gone unnoticed in reference documentation. Reference docs describe what exists. Quickstarts test whether what exists is usable.

**Pin your toolchains.** Foundry nightly, Node LTS, Solidity compiler — every dependency that can change under you will change under you, and it will happen on the day you need CI to be green for a release.

**Execution plans are cheaper than planning meetings.** Writing IntentVision's six-workstream plan took a few hours. It replaced dozens of future "what should we work on" conversations. The plan doesn't have to be right — it has to exist so deviations from it are conscious decisions instead of drift.

---

**Related Posts:**
- [IRSB v1.1.0: CLI Verify, x402 Payment Protocol, and the SDK Rename](/posts/irsb-sdk-cli-x402-payment-protocol-v110/) — the x402 protocol implementation that this quickstart documents
- [git-with-intent v0.9 to v0.10: Docker Upgrades and README Rewrites](/posts/git-with-intent-v090-v0100-docker-upgrades/) — previous GWI release cycle with similar security and docs work
- [Building Moat: Auth, On-Chain Receipts, and 117 Tests](/posts/building-moat-auth-persistence-onchain-receipts-117-tests/) — the graceful degradation chain referenced in the adapter integration guide
