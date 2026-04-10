+++
title = 'IRSB Multi-Release Prep and Hustle E2E Strict Mode Fixes'
slug = 'irsb-multi-release-prep-hustle-e2e-strict-mode'
date = 2026-02-11T10:00:00-06:00
draft = false
tags = ["irsb", "release-engineering", "solidity", "security-audit", "hustle", "e2e-testing", "debugging"]
categories = ["Development Journey"]
description = "Release prep for four IRSB versions including the SolidityGuard v1.2.0 audit report, plus three Hustle E2E test fixes targeting strict mode violations, URL matching, and false positive error detection."
+++

Eight commits across two repos. IRSB stacked up release prep for four versions. Hustle's E2E suite got three targeted fixes for failures that had been intermittent long enough to become background noise.

## IRSB Release Prep: Four Versions

Release prep is the unglamorous work between "code works" and "version ships." Four IRSB packages needed version bumps: v0.3.0 for the solver, v0.5.0 for the watchtower, v1.0.1 for the SDK, and v1.3.1 for the protocol contracts.

Each version bump required the same checklist: update `package.json` version, regenerate the lockfile, update cross-package workspace references, write the CHANGELOG entry, and verify the build passes with the new version constraints. With four packages in the same monorepo sharing workspace dependencies, the order matters — the SDK bump had to land before the solver and watchtower bumps, because both depend on `@irsb/types` from the SDK.

The dependency graph for the release:

```
@irsb/types (v1.0.1) ← @irsb/solver (v0.3.0)
                      ← @irsb/watchtower (v0.5.0)
@irsb/sdk (v1.0.1)   ← @irsb/protocol (v1.3.1)
```

Getting this wrong means one package publishes with a dependency that doesn't exist yet. The workspace protocol (`workspace:*`) handles this in development, but published packages need exact version ranges.

### SolidityGuard v1.2.0 Audit Report

The SolidityGuard audit report shipped alongside the protocol release. SolidityGuard is the static analysis component that runs Slither checks against the contract suite. The v1.2.0 report covered 37 contracts with findings categorized by severity:

- **2 HIGH** — Both related to reentrancy guards on cross-contract calls. Fixed with `nonReentrant` modifiers and checks-effects-interactions ordering.
- **5 MEDIUM** — Mostly gas optimization opportunities and one unchecked return value from a low-level call.
- **11 LOW/INFORMATIONAL** — Naming conventions, missing NatSpec comments, unused imports.

The HIGH findings were already patched in previous commits. The audit report documented the fixes with before/after code snippets and links to the specific commits. This is the artifact that an external auditor would review first — it shows you found the problems and fixed them, not just that you ran a tool.

## Hustle E2E Fixes: Three Specific Problems

### Strict Mode Violation

The test helper module imported `@/lib/firebase/admin`, which has a top-level initialization that calls `process.exit(1)` if the Firebase service account is missing. In the test environment, the service account isn't configured — tests use the Firebase emulator. Vitest's strict mode flagged the import because the module wasn't mocked, and the `process.exit` call would terminate the test runner.

The fix: mock the admin module at the test file level before any imports that trigger it.

```typescript
vi.mock('@/lib/firebase/admin', () => ({
  adminAuth: { verifySessionCookie: vi.fn() },
  adminDb: { collection: vi.fn() },
}));
```

### URL Matching

The dashboard navigation assertion used a regex without an end anchor:

```typescript
// Matched /dashboard, /dashboard/settings, /dashboard/add-athlete
await page.waitForURL(/\/dashboard/);
```

Adding the `$` anchor and optional trailing slash made the assertion precise. Without it, the test proceeded as soon as any dashboard sub-route loaded, which meant subsequent assertions ran against the wrong page.

### False Positive Detection

The error detection logic looked for any `[role="alert"]` element on the page. Next.js dev tools inject alert-role elements for hot module replacement notifications. The test was catching framework noise and throwing assertion errors.

The fix scoped the selector to application error banners (`.bg-red-50[role="alert"]`) and added a content check — only flag it as an error if the element has non-empty text content.

## What I Learned

**Version ordering in monorepos is a dependency graph problem.** Publish packages in topological order of their dependency graph, not alphabetical order. Get it wrong and consumers pull a version that references a dependency that hasn't been published yet.

**Mock before import, not after.** Vitest evaluates module-level code at import time. If a module calls `process.exit()` during initialization, mocking it after import is too late. The mock declaration has to come first.

**Related Posts:**
- [IRSB Four Releases in One Day, Perception Topic Watchlist, and Hustle Session Cookies](/posts/irsb-four-releases-one-day-perception-watchlist-hustle-cookies/)
- [Hustle E2E Stabilization Sprint and Bounty Tracker Init](/posts/hustle-e2e-stabilization-sprint-bounty-tracker-init/)
- [IRSB Security Audit Fixes, git-with-intent v0.6.0, and GitHub Profile Overhaul](/posts/irsb-security-audit-fixes-gwi-v060-github-profile-overhaul/)
