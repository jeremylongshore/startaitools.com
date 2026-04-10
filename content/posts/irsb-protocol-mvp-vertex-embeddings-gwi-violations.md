+++
title = 'IRSB Protocol MVP, Vertex AI Embeddings, and GWI Violation Pipeline'
slug = 'irsb-protocol-mvp-vertex-embeddings-gwi-violations'
date = 2026-01-14T10:00:00-06:00
draft = false
tags = ["irsb", "git-with-intent", "vertex-ai", "embeddings", "monorepo", "dispute-resolution"]
categories = ["Development Journey"]
description = "Bootstrapping the IRSB monorepo from zero to MVP with DisputeModule timeout resolution, building the GWI violation pipeline from detection to dashboard, and migrating Executive Intent to Vertex AI embeddings."
+++

Thirteen commits across three repos. The day split between three distinct workstreams: getting IRSB from bootstrap to an actual MVP, standing up the git-with-intent violation pipeline, and migrating Executive Intent's embedding layer to Vertex AI.

## IRSB: Zero to MVP

The IRSB monorepo got its first real functionality today. Previous work had set up the repo structure and contract scaffolding, but nothing ran end-to-end. Today changed that.

### DisputeModule Timeout Resolution

The DisputeModule handles what happens when an AI agent exceeds a spending bond. The original design required manual intervention -- a human reviews the dispute and releases or slashes the bond. That works for high-value disputes but creates an unbounded queue for small ones.

The timeout resolution mechanism adds automatic settlement. If a dispute goes unresolved for a configurable period (default: 72 hours for disputes under 0.1 ETH), the system auto-settles based on the agent's historical compliance score. High-compliance agents get their bond returned minus a small fee. Low-compliance agents get slashed.

The implementation required changes to three contracts:

- `DisputeModule.sol` -- new `resolveByTimeout` function with compliance oracle integration
- `BondManager.sol` -- conditional release logic based on settlement outcome
- `ComplianceOracle.sol` -- on-chain score aggregation from watchtower reports

The integration test suite covers the full lifecycle: bond deposit, agent action, dispute filing, timeout expiry, and automatic settlement. Twenty-three test cases covering edge cases around concurrent disputes, mid-dispute bond top-ups, and oracle staleness checks.

## GWI Violation Pipeline (D5.2-D5.5)

git-with-intent already had violation detection from earlier work. Today's sprint built the infrastructure that makes detection actionable.

### D5.2: Detector Improvements

The violation detector gained pattern matching for three new categories:

- **Scope creep violations** -- agent modifies files outside its declared scope
- **Budget overruns** -- cumulative token spend exceeds the declared intent budget
- **Cadence violations** -- agent commits outside the approved time windows

Each category produces a structured violation record with severity (info/warn/critical), affected files, and a machine-readable remediation hint.

### D5.3: Alert Routing

Alerts route based on severity. Critical violations page the on-call via PagerDuty webhook. Warnings aggregate into a daily digest. Info-level events log to the event store and show up on the dashboard.

### D5.4: Remediation Suggestions

Each violation type now generates a specific remediation suggestion. Scope creep violations suggest updating the intent manifest. Budget overruns recommend splitting the task into smaller intents. Cadence violations offer schedule adjustment templates.

### D5.5: Violation Dashboard

A basic React dashboard that queries the violation event store and renders violations by severity, category, and agent. The initial version is read-only -- remediation actions come in a later phase.

## Executive Intent: Vertex AI Embeddings Migration

The Executive Intent service was using OpenAI's `text-embedding-ada-002` for semantic search over intent documents. The migration to Vertex AI embeddings (`text-embedding-004`) cut costs and kept everything on GCP.

The migration required updating the embedding dimension from 1536 to 768, re-indexing all existing documents, and swapping the client library from `openai` to `@google-cloud/aiplatform`. The similarity thresholds needed recalibration -- Vertex embeddings produce different distance distributions, so the "relevant match" threshold moved from 0.82 to 0.74.

A backfill script re-embedded all 847 existing intent documents. Total migration time including backfill: about 40 minutes. Inference cost dropped from ~$0.03/1K queries to effectively zero under Vertex AI's free tier allocation.

The only behavioral change: the Vertex embeddings cluster related intents slightly differently. Intents about "budget management" and "spending limits" that were previously distant neighbors now cluster together, which actually improved search relevance for the IRSB use case where those concepts overlap heavily.

## Numbers

| Metric | Value |
|--------|-------|
| Commits | 13 |
| Repos touched | 3 (irsb, git-with-intent, executive-intent) |
| New test cases | 23 (DisputeModule) |
| Documents re-embedded | 847 |
| Embedding cost reduction | ~100% (free tier) |

## Related Posts

- [IRSB Monorepo v1.0.0: Extracting Shared Packages](/posts/irsb-monorepo-v1-extracting-shared-packages/) -- the later monorepo restructuring that unified IRSB's packages
- [git-with-intent v0.9 to v0.10: Docker Upgrades and Strategic Research](/posts/git-with-intent-v090-v0100-docker-upgrades/) -- subsequent GWI releases that built on this violation pipeline
- [GWI RBAC Governance and Hustle CI Stabilization](/posts/gwi-rbac-governance-hustle-ci-stabilization/) -- the governance layer that complemented this violation work
