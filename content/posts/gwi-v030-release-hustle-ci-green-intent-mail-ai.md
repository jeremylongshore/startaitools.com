+++
title = 'GWI v0.3.0, Hustle CI Goes Green, and Intent Mail Gets an AI Brain'
slug = 'gwi-v030-release-hustle-ci-green-intent-mail-ai'
date = 2025-12-27T10:00:00-06:00
draft = false
tags = ["release-engineering", "ci-cd", "e2e-testing", "ai-email", "multi-project", "git-with-intent", "hustlestats", "intent-mail"]
categories = ["Development Journey"]
description = "Three projects, one day: git-with-intent ships v0.3.0 with monitoring and forecasting epics, Hustle's E2E tests finally pass in CI, and Intent Mail scaffolds a multi-provider AI router."
+++

December 27th was a convergence day. Three projects that had been grinding through separate backlogs all hit release-worthy milestones at the same time. Thirty-eight commits across git-with-intent, Hustle, and Intent Mail.

## git-with-intent v0.3.0

The v0.3.0 release closed four epics: F1 feature hardening, monitoring infrastructure, forecasting pipeline, and infra upgrades. Twenty-three commits landed across the board.

**F1 feature hardening** cleaned up rough edges that accumulated during the v0.2.x cycle. Approval gate edge cases — empty diff handling, multi-commit squash detection, and branch protection rule conflicts — all got explicit handling instead of falling through to a generic error path. The kind of polish that doesn't show up in a changelog but prevents support tickets.

**Monitoring** wired observability into the approval pipeline. Every approval gate decision now emits structured logs with:

- The rule that fired (which policy blocked or approved the PR)
- The commit context (author, branch, file paths touched)
- The resolution (approved, blocked, or escalated to human review)
- Timing data (how long the evaluation took)

Before this, debugging a blocked PR meant reading the git log and guessing which rule caught it. Now there's a queryable trail. The log format is JSON-structured, so you can pipe it through `jq` or ship it to any log aggregator without parsing.

**Forecasting** is the more interesting addition. It analyzes commit velocity, approval latency, and merge frequency across time windows to project bottleneck formation. If your Monday morning approval queue has been growing 15% week-over-week for a month, the system surfaces that before you're drowning in stale PRs on a Tuesday. The forecasting module reads from the same structured logs the monitoring epic produces — one system feeds the other. This is why the monitoring epic shipped first. Without structured log data to analyze, the forecasting module would have needed its own data collection layer. Sequencing the epics correctly meant the second epic was cheaper to build.

**Infra upgrades** covered dependency bumps and CI workflow improvements. GitHub Actions workflow pinning, test matrix expansion for Python 3.11 and 3.12, and a Dockerfile base image bump. Nothing exciting. Everything necessary. The kind of maintenance that ages badly if you skip it.

Doc Filing v4.2 also landed in this release. The document organization system got chronological sequencing improvements and better category detection for mixed-format files. Category detection now handles files where the title doesn't match the content type — a markdown file named `api-spec` that contains meeting notes gets filed as meeting notes, not API documentation. Small quality-of-life upgrade, but it removes friction from daily use.

## Hustle CI Finally Goes Green

Nine commits, all focused on one goal: make the E2E test suite pass in CI without flaking. The tests had been passing locally for weeks. CI was a different story — every run was a coin flip between green and red, with different tests failing each time.

The core problem was authentication. E2E tests need a logged-in session to test anything behind the login wall — which is the entire app. In local development, you spin up a test user and log in through the UI. Fast enough, reliable enough. In CI, that same flow hits Firebase Auth rate limits after a handful of concurrent test workers, fails on headless browser cookie handling because Playwright's cookie jar doesn't behave identically to Chrome's, and adds 30 seconds of latency per test from the auth round-trips.

The symptoms were maddening. Tests passed individually. Tests passed in sequence. Tests failed when run in parallel — but different tests each time. Classic sign that the tests aren't failing because of test logic. They're failing because of shared mutable state, and in this case the shared mutable state was the authentication session.

The fix was an auth bypass specifically for test environments. A test middleware intercepts auth checks when `NODE_ENV=test` and injects a pre-authenticated session. No login flow, no Firebase round-trips, no rate limits.

The bypass only activates when a `TEST_AUTH_TOKEN` environment variable is present — missing in production, present in CI. If the variable is absent, the middleware is a no-op. Defense in depth against accidentally shipping a test backdoor to production.

Session cookies for localhost needed their own fix. Secure cookies with `SameSite=Strict` don't survive cross-origin redirects on `localhost`. The browser silently drops the cookie on the redirect, so the session appears to work (login succeeds) but the next navigation loses the session (dashboard redirects back to login). The test configuration relaxes cookie security to `SameSite=Lax` and drops the `Secure` flag. Again, only in test environments. The symptom — "tests pass individually but fail in sequence" — is a classic cookie-handling tell.

The CI checker itself got bounded. Previous runs would spin up the full test suite and let it run unbounded. Now there's a timeout per test file and a maximum total runtime. If the suite exceeds the bound, it fails fast instead of hanging the CI runner for 20 minutes while a single test waits for a network timeout that will never resolve.

All E2E tests now pass in CI. That sentence took nine commits and two days of debugging to earn.

## Intent Mail: AI Provider Abstraction

Six commits laid the foundation for Intent Mail's AI capabilities. The project is a terminal email client with intelligence built in — not bolted on after the fact as a "smart reply" button.

The key architectural piece is a multi-provider router. Email summarization, inbox triage, and smart compose all need LLM calls. Hardcoding a single provider means you're locked in when prices change or a provider degrades.

The router abstracts the provider behind an interface: send a prompt, get a response. The router decides which provider handles it based on task type, latency requirements, and cost budget. Summarization can use a cheaper, faster model. Smart compose needs a higher-quality model because the user sees the output directly. The router makes that decision transparent instead of burying it in a config constant.

Provider failover is built into the router from the start. If the primary provider returns a 5xx or times out, the router retries with the next provider in the fallback chain. The user doesn't see the failover — the response just takes slightly longer.

The CLI and TUI foundation went in alongside the AI layer. Intent Mail runs in the terminal — no Electron, no web UI. The CLI handles single commands (`intent-mail summarize inbox`) for scripting and pipelines. The TUI provides an interactive interface for triage workflows where you're making rapid decisions across dozens of messages. Both surfaces share the same command layer underneath. Building a feature once means it works in both contexts.

Documentation got reorganized from a flat collection of notes into a structured docs directory. Architecture decisions, API contracts, and provider configuration all have dedicated files now. The provider configuration docs are especially important because adding a new LLM provider means editing a config file, not writing adapter code — but only if you can find the config documentation. Not glamorous work, but finding the right doc in 2 seconds instead of 20 compounds across a project's lifetime.

## The Common Thread

All three projects hit the same pattern today: the infrastructure that makes the real features work. Monitoring makes approval gates debuggable. Auth bypass makes E2E tests viable in CI, not just on a developer laptop. Provider abstraction makes AI features portable across LLM backends.

None of these are the features users see. All of them are the reason those features will be reliable when users do see them. Infrastructure days don't make good demo videos. They make good software.

The v0.3.0 release was the most satisfying checkpoint of the three. Four epics closing simultaneously means the roadmap planning was correct — the work items were scoped right and the dependencies resolved in the right order. When epics close together instead of one at a time, it usually means the estimation was honest rather than optimistic.

---

**Related Posts:**

- [git-with-intent v0.9 to v0.10: Docker Upgrades, README Rewrites, and Strategic Research](/posts/git-with-intent-v090-v0100-docker-upgrades/) — Later GWI releases building on this foundation
- [Session Cookie Auth, Forgot-Password Timeouts, and Killing Flaky E2E Tests](/posts/session-cookies-forgot-password-flaky-e2e-tests/) — The auth and cookie patterns Hustle's CI fix builds on
- [Building Production CI/CD: From Documentation to Deployment](/posts/building-production-ci-cd-documentation-to-deployment/) — CI pipeline patterns used across all three projects
