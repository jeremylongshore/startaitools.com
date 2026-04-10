+++
title = 'IRSB Go-to-Market Sprint: Sepolia Deployment, TypeScript SDK, and Subgraph'
slug = 'irsb-go-to-market-sprint-sepolia-sdk-subgraph'
date = 2026-01-25T10:00:00-06:00
draft = false
tags = ["irsb", "blockchain", "typescript", "sdk", "the-graph", "sepolia", "firebase", "security", "ci-cd"]
categories = ["Technical Deep-Dive"]
description = "29 commits across 4 repos in a full go-to-market sprint: investor report, Sepolia deployment with solver reputation dashboard, TypeScript SDK with CI/CD, The Graph subgraph, Across Protocol adapter, Firebase deployment, and security hardening."
+++

## The Go-to-Market Push

IRSB had been a protocol with working contracts and passing tests. What it didn't have was the surrounding infrastructure that makes a protocol investable and usable by external developers. January 25th was the day that changed — 25 commits on IRSB alone across every layer of the go-to-market stack.

This wasn't a technical exploration day. It was a business-driven sprint with a clear goal: produce the artifacts that a potential investor or integration partner would need to evaluate the protocol. That meant documentation (investor report + feasibility study), tooling (SDK + subgraph), deployment (Sepolia + dashboard), and credibility signals (security hardening + auditor outreach).

## Investor Report and Feasibility Study

Twenty-five thousand words across two documents. The investor report covers market positioning, competitive landscape, technical architecture, and financial projections. The feasibility report digs into the implementation details — gas costs per operation, transaction throughput under load, and the economic model that makes solver bonds work.

These aren't blog posts. They're structured business documents with data tables, architecture diagrams, and specific claims backed by on-chain metrics. Writing them forced a level of rigor that casual documentation doesn't: every performance claim had to be verifiable on Sepolia, every competitive comparison had to reference specific features in competing protocols.

The process of writing the reports surfaced two gaps in the protocol that hadn't been apparent from the test suite alone. The gas cost section revealed that the `DisputeModule`'s evidence submission was 40% more expensive than necessary due to redundant storage writes. The throughput section showed that the solver registration flow had an unnecessary second transaction that could be batched with the bond deposit.

Both were fixed before the reports were finalized. Documentation as debugging.

## Sepolia Deployment with Solver Reputation Dashboard

The protocol was deployed to Sepolia with all contracts verified on Etherscan. Contract verification matters for external evaluation — investors and auditors want to read the deployed bytecode's source, not just trust that the local source matches.

The solver reputation dashboard is a Firebase-hosted React app that reads on-chain data and displays:

- **Solver registration status** — bonded, active, slashed, withdrawn
- **Reputation scores** — calculated from receipt accuracy, dispute history, and time in good standing
- **Historical performance** — charts of solver activity over time

The dashboard pulls data through two channels: direct RPC calls for current state, and The Graph subgraph for historical data. This dual approach keeps the dashboard responsive (current state is fast via RPC) while supporting historical queries (subgraph handles the indexing).

## TypeScript SDK: @intentsolutionsio/irsb-sdk

The SDK went from nothing to published with examples and CI/CD in a single push. The package exposes typed wrappers around every contract interaction:

```typescript
import { IrsbClient } from '@intentsolutionsio/irsb-sdk';

const client = new IrsbClient({
  rpcUrl: 'https://sepolia.infura.io/v3/YOUR_KEY',
  privateKey: process.env.PRIVATE_KEY,
});

// Register as a solver with 0.1 ETH bond
const tx = await client.solver.register({ bondAmount: '0.1' });

// Submit an intent receipt
const receipt = await client.receipts.submit({
  intentHash: '0x...',
  solver: '0x...',
  result: { success: true, gasUsed: 45000 },
});
```

The naming went through a rename during this sprint. It started as a generic package name and landed on `@intentsolutionsio/irsb-sdk` — scoped to the organization, explicit about what it wraps.

The CI/CD pipeline runs on every push to the SDK directory:

1. **TypeScript compilation** — `tsc --noEmit` for type checking
2. **Unit tests** — `vitest` with contract mocks
3. **Integration tests** — Against a local Hardhat fork of Sepolia
4. **Build** — Produces both ESM and CJS outputs
5. **Publish gate** — Version bump detection triggers npm publish on merge to main

The examples directory includes complete scripts for common operations: registering a solver, submitting receipts, querying dispute status, and monitoring solver reputation. Each example is runnable with `npx tsx examples/register-solver.ts` after setting environment variables.

## The Graph Subgraph

The subgraph indexes all IRSB contract events into a queryable GraphQL API. Deploying it was not smooth.

**Entity fixes** — The initial schema defined entities that didn't match the actual event signatures. The `Receipt` entity expected a `solver` field from the event, but the event emits `solverAddress`. Schema had to match event ABI exactly or the indexer silently drops events.

**Sync tuning** — The subgraph was syncing slowly on Sepolia because the start block was set to 0. IRSB contracts were deployed after block 7,200,000. Setting the correct `startBlock` in `subgraph.yaml` for each data source cut initial sync time from hours to minutes.

**Enum handling** — Solidity enums arrive as `uint8` in events. The subgraph mapping needs explicit casting:

```typescript
// Bad: entity.status = event.params.status (type error)
// Good: entity.status = event.params.status == 0 ? "Pending" : "Active";
```

The mapping handlers required a manual lookup table from integer to string for every enum used in events. The Graph's AssemblyScript doesn't support TypeScript enums, so this is unavoidably manual.

## Across Protocol Adapter and Dashboard

The Across Protocol adapter enables cross-chain intent settlement. When a user submits an intent on one chain, the solver can fill it using Across's bridge infrastructure and submit the receipt on the origin chain. The adapter handles the bridge relay logic and receipt attestation.

The dashboard component for Across integration shows pending cross-chain intents, bridge relay status, and settlement confirmation. It's a tab within the main solver reputation dashboard, not a separate application.

## Firebase Dashboard Deployment

The dashboard deployment uses Firebase Hosting with GitHub Actions:

```yaml
- name: Deploy to Firebase
  uses: FirebaseExtended/action-hosting-deploy@v0
  with:
    repoToken: ${{ secrets.GITHUB_TOKEN }}
    firebaseServiceAccount: ${{ secrets.FIREBASE_SERVICE_ACCOUNT }}
    channelId: live
```

Preview deployments on PRs go to Firebase preview channels. Merges to main deploy to the live channel. The build step runs `vite build` with environment variables for the Sepolia RPC URL and subgraph endpoint.

## Security Hardening

Four categories of security improvements shipped in this sprint:

**SSRF Protection** — The dashboard's API proxy routes (used to bypass CORS for RPC calls) were vulnerable to server-side request forgery. The fix: an allowlist of permitted upstream URLs. Any request to a non-allowed URL returns 403. The allowlist includes only the Sepolia RPC endpoint and the subgraph API.

**CSP Headers** — Content Security Policy headers added to Firebase Hosting configuration. `script-src 'self'`, `connect-src` limited to known API endpoints, `frame-ancestors 'none'`. These prevent XSS attacks and clickjacking on the dashboard.

**Input Validation** — All user-supplied parameters (addresses, amounts, hashes) validated against regex patterns before being passed to contract calls. Ethereum addresses must match `^0x[a-fA-F0-9]{40}$`. Amounts must be valid decimal strings. Intent hashes must be 32-byte hex.

**Dependency Audit** — `npm audit` with `--audit-level=high` added to CI. Any high or critical vulnerability in the dependency tree blocks the build.

## Auditor Outreach Templates

Three email templates for security auditor outreach: initial inquiry, technical brief, and engagement proposal. Each template includes the protocol architecture summary, contract count, line count, and deployment addresses. The goal is to start audit conversations with the technical context already provided so the first call is productive, not introductory.

## County Line: Gulf Shores Edition and TestEZ

The remaining 4 commits went to County Line. The Gulf Shores Edition adds a beach/coastal terrain variant to the procedural generator. TestEZ integration brings Roblox's testing framework into the CI pipeline — `TestBootstrap` runs tests headlessly via Rojo and reports results to GitHub Actions.

## Session Stats

| Metric | Value |
|--------|-------|
| **Commits** | 29 |
| **Repos** | 4 (irsb, county-line, bounty-orchestrator, roblox-game-template) |
| **IRSB commits** | 25 |
| **Documents produced** | 2 (investor report, feasibility study — 25K words) |
| **SDK published** | @intentsolutionsio/irsb-sdk |
| **Contracts deployed** | All IRSB contracts on Sepolia |
| **Security fixes** | SSRF, CSP, input validation, dependency audit |

## What Made This Day Work

The go-to-market sprint covered seven distinct workstreams in a single day: documentation, deployment, SDK, subgraph, dashboard, security, and outreach. None of these were technically novel — TypeScript SDKs, Firebase deployments, and Graph subgraphs are established patterns.

What made the day productive was having the protocol itself already stable. The contracts were tested, the architecture was settled, and the API surface was frozen. The go-to-market layer is a function of protocol stability. If the contracts were still changing, every downstream artifact (SDK, subgraph, dashboard) would need rework with each protocol change.

Build the protocol first. Build the go-to-market second. Not in parallel.

## Related Posts

- [IRSB Monorepo v1.0.0: Extracting Shared Packages](/posts/irsb-monorepo-v1-extracting-shared-packages/) — Later monorepo consolidation of the packages created in this sprint
- [IRSB Deep Dive 1: On-Chain Enforcement](/posts/irsb-deep-dive-1-on-chain-enforcement/) — Technical deep dive into the enforcement layer deployed here
- [Christmas Eve Cleanup: GWI SDK and Intent Mail Audit](/posts/christmas-eve-cleanup-gwi-sdk-intent-mail-audit/) — Earlier SDK packaging work with similar CI/CD patterns
