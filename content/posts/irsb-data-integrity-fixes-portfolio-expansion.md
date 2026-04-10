+++
title = 'IRSB Data Integrity Fixes and Portfolio Expansion'
slug = 'irsb-data-integrity-fixes-portfolio-expansion'
date = 2026-01-27T10:00:00-06:00
draft = false
tags = ["irsb", "bug-fixes", "graphql", "firebase", "git-with-intent", "jeremylongshore", "portfolio"]
categories = ["Development Journey"]
description = "IRSB gets real: fake demo data removed, testnet preview banner added, subgraph GraphQL types fixed, solver IDs converted to bytes32. git-with-intent README update and jeremylongshore.com grows to 25 projects with a new Open Source section."
+++

Eight commits across three repos. Most of the day was bug fixes in the IRSB monorepo — the kind of work that doesn't produce features but produces trust. Every item on today's list existed because the testnet deployment exposed gaps between what the code assumed and what the chain actually returned.

## IRSB: Removing the Lies

### Demo Data Purge

The IRSB dashboard had hardcoded demo data seeded for screenshots and investor demos. Fake operators, fake bounties, fake resolution events. The problem: some of that demo data leaked into the testnet deployment. A testnet user could see "Operator Alpha" with a fake track record and think it was real activity.

The fix removed all hardcoded seed data and replaced it with a testnet banner that says exactly what it is. The seeder script still exists for local development, but it's gated behind a `SEED_DEMO=true` environment variable that the deployment pipeline never sets.

The purge also removed the "demo mode" toggle that was accessible from the footer. That toggle switched between live subgraph data and the hardcoded fixtures. In theory it let evaluators see a populated dashboard without testnet data. In practice it confused everyone who found it accidentally.

### Testnet Preview Banner

A persistent amber banner at the top of every page when running against testnet. Not dismissible. The text: "Testnet Preview — Data may be reset without notice." This eliminates the ambiguity that the demo data created.

The banner reads the `NEXT_PUBLIC_NETWORK` environment variable. On mainnet it renders nothing. On testnet it renders the warning. On localhost it renders a blue "Local Development" banner instead.

The three-state banner is a pattern worth standardizing. Any protocol with a testnet should make the environment visually unambiguous. Users shouldn't have to check the URL or inspect network requests to know which network they're interacting with.

### Subgraph GraphQL Types

The Graph Protocol subgraph had type mismatches between the schema and the event handlers. The `BountyCreated` event emits a `uint256` for the bounty ID, but the schema defined it as `ID` (a string). The subgraph compiled and deployed, but queries returned null for any bounty ID above 2^53 because JavaScript's number precision truncated the value.

The fix changed the schema to use `BigInt` for all numeric chain values and `Bytes` for addresses and hashes. Every handler got updated to use `BigInt.fromI32()` and `Address.fromBytes()` constructors instead of raw casts.

This is a trap that every Graph Protocol subgraph hits eventually. The AssemblyScript runtime that subgraphs compile to doesn't have JavaScript's number type — it has distinct integer and byte types. Using `ID` (which maps to a string) for numeric values works until the numbers get large enough to expose the precision loss.

### Solver ID bytes32 Conversion

Solver IDs were stored as `string` in the contract and `String` in the subgraph. The protocol spec says they should be `bytes32` — a fixed-size identifier derived from the solver's address and registration timestamp. The string representation worked for small testnet deployments but would collide at scale.

The contract migration was straightforward: change the mapping key type and add a conversion function. The harder part was updating every frontend call site that passed solver IDs as strings. Sixteen call sites across four components.

The conversion function uses `keccak256(abi.encodePacked(solverAddress, registrationTimestamp))`. This produces a deterministic, collision-resistant identifier that can be computed off-chain for lookups. The frontend now computes the bytes32 ID client-side before making subgraph queries, which also eliminates a class of bugs where string-based IDs had inconsistent casing.

### Operator Page and Firebase Fixes

The operator detail page crashed when a solver had no resolution history. A missing null check on the `resolutions` array. The fix: default to an empty array when the subgraph returns null. This is the kind of bug that only surfaces with real data — every test operator had at least one resolution, so the null path was never exercised.

The Firebase rewrite rule for the SPA wasn't catching deep links to operator pages. Requests to `/operators/0x1234` hit a 404 because the rewrite only matched single-segment paths. Updated the rule to `**` glob matching.

Firebase hosting rewrites are deceptively simple until you have nested routes. The original rule was `"source": "/operators"` which matches `/operators` but not `/operators/0x1234`. The fix: `"source": "/operators/**"`. Same issue existed for `/bounties/**` and `/solvers/**` — all three got updated. The catch-all `"source": "**"` rewrite at the bottom of the rules list handles everything else, but specific routes need their own entries to take priority over static file serving.

## git-with-intent: README Refresh

The README still described v0.3.0 features. Updated to reflect v0.5.0: added the `gwi gate` command documentation, the ReviewerAgent configuration section, and the interactive approval screenshots. Removed the "coming soon" section that listed features now shipped.

The new README structure follows the same three-audience pattern used for IRSB: evaluators get a one-paragraph description and a feature list, users get installation and quickstart, contributors get architecture and development setup. The old README tried to be all three at once and ended up serving none of them well.

Also added a "What's New in v0.5.0" section at the top for returning visitors who just want the delta. This section gets replaced with each release — it's not a changelog, it's a spotlight on the current version's headline features.

## jeremylongshore.com: 25 Projects and Open Source

The portfolio grew from 18 to 25 listed projects. The new entries: IRSB protocol, git-with-intent, lumera-emanuel, bounties platform, perception dashboard, intentCAD, and the blog infrastructure.

The bigger change was the new Open Source section. A dedicated page listing every MIT-licensed project with links to GitHub, documentation status, and contribution guidelines. git-with-intent is the flagship entry. The section pulls project metadata from a JSON file so adding new projects is a data change, not a template change.

Each project card shows: name, one-line description, license badge, last commit date, and a link to the contributing guide. The cards are sorted by last commit date so the most active projects appear first. This avoids the stale-project problem where abandoned repos sit at the top of a manually ordered list.

Seven projects made the initial list. The bar: MIT license, a README that passes a basic quality check, and at least one tagged release.

---

Eight commits. IRSB tells the truth now. The portfolio reflects what actually exists. None of this work is glamorous — no new features, no architecture diagrams, no release announcements. But a protocol that lies about its data is worse than a protocol that doesn't exist yet. Quiet, necessary work.

### Related Posts

- [IRSB Public Site Redesign and git-with-intent v0.5.0 Release](/posts/irsb-public-site-redesign-gwi-v050-release/)
- [Building Moat: Auth, On-Chain Receipts, and 117 Integration Tests in One Week](/posts/building-moat-auth-persistence-onchain-receipts-117-tests/)
- [GitHub Profile Refresh and Nixtla Review Readiness](/posts/github-profile-refresh-nixtla-review-readiness/)
