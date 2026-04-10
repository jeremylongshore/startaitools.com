+++
title = 'Hustle E2E Stabilization Sprint and Bounty Tracker Init'
slug = 'hustle-e2e-stabilization-sprint-bounty-tracker-init'
date = 2026-01-10T10:00:00-06:00
draft = false
tags = ["testing", "debugging", "full-stack", "firebase"]
categories = ["Development Journey"]
description = "Fifteen commits across three repos. Thirteen of them are E2E test fixes — selectors, error handling, storage state, and Firestore field compatibility. The other two initialize a bounty tracker."
+++

Some days you ship features. Some days you make the tests stop lying to you. January 10th was the second kind.

Fifteen commits across three repos. Thirteen went into the Hustle E2E test suite. The tests weren't failing — they were flaking. Passing on one run, failing on the next, with no code changes in between. The kind of instability that erodes trust in CI until everyone ignores it.

A flaky test suite is worse than no test suite. No tests means you know you're flying blind. Flaky tests mean you think you have a safety net, but it has holes you can't see. Every "retry and it'll pass" is a small erosion of the habit of treating red CI as a real signal.

## The Flake Catalogue

The failures fell into four categories.

**Stale selectors.** The dashboard had been through a UI refresh in December. Component class names changed, data-testid attributes moved to different elements, and three tests were clicking on selectors that no longer existed. Playwright's default timeout hid the problem — the tests would wait 30 seconds, fail, and retry. On a good day, the element would load just in time. On a bad day, timeout.

Fixed by auditing every selector in the suite against the current DOM. Twelve selectors updated. Two tests were targeting elements that had been removed entirely — those got rewritten to test the replacement components.

The lesson: every UI change should touch the corresponding test file in the same PR. If you change a component's structure, the test that clicks on that component needs to change too. This sounds obvious written down. In practice, the UI changes and the tests are in different directories, reviewed by different people, and nobody catches the drift until CI goes red.

**Error handling gaps.** The billing tests assumed Stripe webhook delivery was synchronous. They'd create a subscription, then immediately check the user's plan status. In practice, the webhook takes 1-3 seconds to arrive and process. The test would pass when the webhook was fast and fail when it wasn't.

The fix wasn't adding sleep statements. It was adding polling with an explicit timeout:

```typescript
await expect(async () => {
  const plan = await getUserPlan(testUser.id);
  expect(plan.tier).toBe('pro');
}).toPass({ timeout: 10_000 });
```

Playwright's `toPass` retries the assertion block until it succeeds or times out. No arbitrary delays, no false confidence.

**Storage state corruption.** The test suite used a shared `storageState.json` for authenticated sessions. When tests ran in parallel, two workers would sometimes write to the same file simultaneously, corrupting the JSON. The next test that read it would parse garbage and fail with a cryptic Playwright error about invalid browser context.

Fixed by giving each parallel worker its own storage state file:

```typescript
const storageStatePath = `./test-results/storage-${test.info().parallelIndex}.json`;
```

**Firestore field compatibility.** The test assertions were checking for fields that existed in the old Prisma schema but had different names in Firestore. `createdAt` vs `created_at`. `planId` vs `plan_id`. The November Firebase migration changed the field naming convention from camelCase to snake_case, but the test assertions never caught up.

Eight assertions updated to match the Firestore schema. The kind of bug where the tests are "testing" something but actually validating nothing — the field they're checking doesn't exist, so the assertion sees `undefined` and the equality check against `undefined` passes silently.

This is arguably the most dangerous category. The other three produce visible failures — timeouts, file corruption, selector misses. Schema drift produces invisible passes. The test says green, the field doesn't exist, and you have zero coverage where you think you have full coverage.

## The Pattern

Every one of these failures was a test that passed for the wrong reason or failed for the wrong reason. None of them caught actual application bugs. They were testing their own infrastructure — selector stability, webhook timing, file I/O race conditions, schema drift.

This is the cost of not maintaining tests alongside the code they cover. The UI refresh, the Firebase migration, and the billing integration all shipped without updating the corresponding tests. Each left behind a small landmine. Thirteen landmines later, CI was useless.

The stabilization sprint took most of the day. Not because any individual fix was hard — most were one-line changes to a selector or an assertion. The hard part was diagnosing each flake. You can't fix a test you can't reproduce. Running the suite ten times to see which tests fail intermittently, then narrowing down whether the failure is timing, state, or selector-related, is the actual work.

## Bounty Tracker Init

Separate from the Hustle work: two commits initializing a bounty tracker project. Basic repo scaffolding — `package.json`, `tsconfig.json`, a `README.md` with the project scope, and an empty `src/` directory.

The bounty tracker will aggregate open bounties from GitHub, Algora, and CSV imports into a single prioritized view. The idea is simple: instead of checking three different platforms to see what's available and what's worth pursuing, check one dashboard that ranks everything by expected value.

Today was just the foundation. More on this as it develops.

After the stabilization sprint, the test suite runs clean ten times in a row. That's the bar. Not "passes most of the time." Not "passes if you retry." Passes every time, in parallel, on a cold start. Anything less and you're back to ignoring CI.

---

Fifteen commits. Thirteen test fixes that turned a flaky CI pipeline back into a reliable one. Two commits that planted a seed for a new project. Not flashy, but the Hustle test suite now means something again.

### Related Posts

- [Session Cookies, Forgot Password, and Flaky E2E Tests](/posts/session-cookies-forgot-password-flaky-e2e-tests/)
- [Building Production-Grade Testing Infrastructure: A Playwright Case Study](/posts/building-production-grade-testing-infrastructure-playwright-case-study/)
- [HustleStats Firebase Auth Cutover: Seven Pages](/posts/hustlestats-firebase-auth-cutover-seven-pages/)
