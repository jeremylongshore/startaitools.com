+++
title = 'IRSB Four Releases in One Day, Perception Topic Watchlist, and Hustle Session Cookies'
slug = 'irsb-four-releases-one-day-perception-watchlist-hustle-cookies'
date = 2026-02-08T10:00:00-06:00
draft = false
tags = ["irsb", "release-engineering", "typescript", "firebase", "perception", "hustle", "e2e-testing", "session-management"]
categories = ["Development Journey"]
description = "Ten IRSB commits pushing four version bumps from v0.2.0 to v1.2.0, Perception's interactive Topic Watchlist and ingestion button, and Hustle's Firebase session cookie fix with E2E stabilization."
+++

Three repos, seventeen commits. The IRSB monorepo pushed through four releases in a single day — clearing a backlog of fixes that had been accumulating across the solver, dashboard, SDK, and protocol packages. Perception moved from static topic display to interactive CRUD with real Firestore persistence. Hustle fixed the auth flow that had been silently expiring users after one hour and stabilized two more flaky E2E tests.

## IRSB: v0.2.0 Through v1.2.0

Ten commits, four releases. The IRSB monorepo had accumulated fixes across multiple packages — TypeScript strict mode violations, ERC-8004 adapter badge rendering, and a Lit network key derivation bug that only surfaced on Sepolia. Instead of batching these into a single large release, I cut four separate versions to keep the changelog readable and bisectable.

The release cadence was deliberate. Each version targets a single package or concern, which means downstream consumers can upgrade incrementally. A user who only depends on `@irsb/solver` can take v0.2.0 without pulling in the dashboard changes from v0.4.0. Monorepo versioning gets complicated when packages have cross-dependencies, but keeping the release scope narrow reduces the blast radius of any individual upgrade.

**v0.2.0** fixed TypeScript strict mode across the solver package. The `noUncheckedIndexedAccess` flag caught twelve places where array access assumed a value existed without checking. These were all runtime-safe (the arrays were always populated by the time they were accessed) but TypeScript couldn't prove it statically. Each fix was a simple nullish coalescing operator or explicit length check.

The twelve fixes broke down into three patterns: five array index accesses that needed optional chaining (`arr[i]?.field`), four `Map.get()` calls that needed nullish coalescing (`map.get(key) ?? defaultValue`), and three `Object.entries()` destructures where the value type was widened to `T | undefined`. The last category was the most annoying — the entries were guaranteed to exist because the object was constructed in the same function, but TypeScript's type narrowing doesn't track across `Object.entries()`.

**v0.4.0** updated ERC-8004 adapter badge rendering in the dashboard. ERC-8004 is a credibility publishing standard — adapters register their verification results on-chain, and the dashboard displays badges based on those results. The credibility badges were pulling from a hardcoded enum instead of the on-chain registry. When new adapters got registered, the badges wouldn't reflect them until a code deploy. The fix: read adapter metadata directly from the `CredibilityPublisher` contract at render time, with a 60-second cache to avoid hammering the RPC.

The cache uses a simple in-memory map keyed by adapter address. On first render, it fetches adapter metadata from the contract and stores it with a timestamp. Subsequent renders within 60 seconds return the cached value. The cache invalidates on page navigation, which is acceptable — badge data doesn't change within a single page view.

**v1.0.0** was the major bump. This was primarily documentation and packaging — the README rewrite, the updated contributor guide, and the consolidated CHANGELOG that covered everything from the initial protocol design through the go-to-market sprint. No breaking API changes, but the maturity signal mattered for the pitch deck.

The CHANGELOG consolidation was the most time-consuming piece. Six months of commits across four packages, collapsed into a single narrative. Each entry links to the specific commit and includes the package scope: `[protocol]`, `[solver]`, `[watchtower]`, `[sdk]`. The format makes it possible to filter by package when reviewing what changed.

The contributor guide covered the monorepo setup (pnpm workspaces, turborepo for build orchestration), the testing requirements (forge for Solidity, vitest for TypeScript, pytest for Python), and the release process (which packages can be released independently vs. which must be released together). The guide is aimed at someone joining the project cold — it assumes familiarity with TypeScript and basic Solidity but doesn't assume knowledge of the IRSB architecture.

**v1.2.0** fixed a Lit Protocol key derivation issue. The `derivedKeyId` was being generated with the wrong chain parameter on Sepolia, causing signature verification to fail silently. The key would derive, the signature would generate, but `ecrecover` on-chain returned `address(0)` instead of the expected signer. The fix was a one-line chain ID parameter correction, but finding it took three hours of tracing through the Lit SDK internals.

The debugging process: first I checked the signature bytes (valid format, correct length). Then the message hash (matched the expected digest). Then the recovery ID (within range). Everything looked correct at the TypeScript level. The problem only became visible when I compared the `derivedKeyId` against what the Lit relay node actually computed — the chain parameter was `1` (mainnet) instead of `11155111` (Sepolia), so the derived key was for a completely different network.

This is the kind of bug that unit tests don't catch because the mock Lit node and the real Lit node behave differently. The mock doesn't validate chain parameters — it just returns a key. The real relay node uses the chain parameter as an input to the key derivation function, which means different chains produce different keys. The lesson: integration tests against the real relay, not just the mock, for anything involving key derivation.

After the fix, I added a post-derivation assertion that compares the local chain ID against the one embedded in the `derivedKeyId`. If they don't match, it throws immediately with a descriptive error instead of silently producing a wrong-chain key. This turns a three-hour debugging session into a one-line error message.

## Perception: Interactive Topic Watchlist

Perception's Topic Watchlist moved from read-only display to full CRUD. The dashboard previously showed a static list of monitored topics pulled from a YAML config. Now topics are managed through Firestore with real-time sync.

Adding a topic requires a keyword, a category selection from 16 options, and optional source assignment from the 128-feed catalog. The source picker uses autocomplete with a 10-result cap to keep the dropdown usable. Each topic document stores the keyword, category, assigned source IDs, creation timestamp, and the user ID that created it. Deleting a topic uses a hover-reveal button pattern — the delete icon only appears on mouse hover, preventing accidental deletions on touch-heavy workflows. The Firestore listener on the `topics_to_monitor` collection provides real-time updates — add a topic on one browser tab, it appears instantly in another.

The "Run Ingestion" button landed in the same session. Previously, ingestion ran only on a cron schedule — if you wanted fresh data, you waited. The button fires a `POST /trigger/ingestion` request and polls for progress every 3 seconds, showing phase updates: loading sources, fetching feeds, storing articles, done. The button disables itself while a run is active and shows elapsed time. If a run is already in progress (detected by the `ingestion_runs` document), the button shows the existing run's progress instead of starting a duplicate.

The pipeline processes 128 RSS feeds with a 10-feed concurrency semaphore. Without the semaphore, firing 128 HTTP requests simultaneously overwhelmed the Cloud Run instance's connection pool and triggered ECONNRESET errors on about 15% of feeds. The semaphore limits concurrent fetches to 10, which completes the full pipeline in about 45 seconds on a warm instance. On a cold start, the first run takes closer to 90 seconds because the FastAPI service needs to initialize the Firestore client and load the source catalog from YAML.

The button's polling mechanism uses a simple `setInterval` that clears itself when the run completes or when the component unmounts. The unmount cleanup was the part I almost forgot — without it, navigating away from the dashboard while an ingestion was running would leave an orphaned interval polling a Firestore document forever.

The dashboard's Firestore data structure also got a fix. Article documents were storing `published_at` as a string timestamp instead of a Firestore `Timestamp` type, which broke date-range queries. Firestore can only run inequality filters on `Timestamp` fields, not on strings that happen to look like timestamps. The migration script converted existing documents in batches of 500, reading the string value, parsing it into a JavaScript `Date`, and writing it back as a `Timestamp`.

## Hustle: Session Cookies and E2E Fixes

Hustle's auth had a subtle bug. Users were getting logged out after one hour despite the cookie having a 14-day `maxAge`. The root cause: the cookie stored a raw Firebase ID token, which expires in one hour regardless of cookie settings. The fix was switching to `createSessionCookie()`, which issues a server-side session token with the actual requested lifetime.

The distinction matters: `createSessionCookie()` takes the ID token and issues a new, server-side token with an independent expiration. The cookie stores this session token instead of the raw ID token. Server-side verification switches from `verifyIdToken()` to `verifySessionCookie()` — different method, different token type, different code path in the Admin SDK. The session token actually respects the `maxAge` you set.

The migration path was also important. Existing users with the old raw ID token cookie would hit `verifySessionCookie()` and fail. The middleware needed a fallback: try `verifySessionCookie()` first, and if it throws with a specific error code indicating the token isn't a session cookie, fall through to `verifyIdToken()` as a legacy path.

This lets existing sessions degrade gracefully — they'll expire within the hour and re-authenticate with the new flow. No forced logout, no "please log in again" banner, no support tickets. Users on the old flow see zero disruption; they just silently migrate on their next login.

The E2E test suite got two fixes. A strict mode violation in the test helpers was importing a module that triggered a side effect at import time — `process.exit(1)` in an error handler. Vitest's strict mode flagged it because the module wasn't mocked. The mock needed to cover the entire module surface — `adminAuth` and `adminDb` — so the side-effecting initialization code never runs.

The second fix was a URL matching regex that was too loose, causing navigation assertions to pass prematurely when the browser was still on a sub-route. The regex `/\/dashboard/` matched `/dashboard`, `/dashboard/settings`, `/dashboard/add-athlete`, and anything else starting with that path. Adding `\/?$` to the regex anchored it to the dashboard root instead of matching any dashboard sub-path. A small regex change, but it eliminated three intermittent test failures that had been dismissed as "flaky."

## What I Learned

**Cut small releases often.** Four versions in one day sounds excessive, but each release had a clean changelog entry and a clear scope. When the Lit key derivation bug surfaced later, `git bisect` pointed directly at v1.2.0 instead of a monster release with thirty unrelated changes. The overhead of cutting a release (version bump, changelog entry, tag) is about 10 minutes. The overhead of debugging a regression in a 30-change release is hours. The math favors small releases every time.

**Silent signature failures are the worst kind.** The Lit key derivation bug didn't throw errors. It returned a valid-looking signature that failed on-chain verification. The only signal was `address(0)` from `ecrecover`. If you're working with any key derivation system, always verify the round-trip: derive, sign, recover, and compare addresses.

**Firestore type mismatches are silent until query time.** Storing a date as a string works fine for reads — you get the string back, parse it, and render it. The problem only surfaces when you try to run a range query (`where published_at > someTimestamp`), because Firestore's inequality operators don't cross type boundaries. If the field is a string, you can only compare against strings. If you need time-range queries, store native `Timestamp` from the start.

**Related Posts:**
- [IRSB v1.0.0 Release Prep: Security Audit Scaffold and Mobile UX](/posts/irsb-v100-release-security-audit-mobile-ux/)
- [Perception Dashboard: Wiring Real Triggers, Topic Watchlists, and the BSL-1.1 Decision](/posts/perception-dashboard-real-triggers-topic-watchlists/)
- [Session Cookie Auth, Forgot-Password Timeouts, and Killing Flaky E2E Tests](/posts/session-cookies-forgot-password-flaky-e2e-tests/)
