+++
title = 'Christmas Eve Cleanup: GWI SDK Types and Intent Mail Audit Log'
slug = 'christmas-eve-cleanup-gwi-sdk-intent-mail-audit'
date = 2025-12-24T10:00:00-06:00
draft = false
tags = ["typescript", "docker", "audit-logging", "release-engineering", "git-with-intent"]
categories = ["Development Journey"]
description = "Six commits across two repos on Christmas Eve: git-with-intent SDK types update and E2E docs, plus intent-mail Docker deployment, Gemini review fixes, and an audit log with rollback."
+++

Christmas Eve. Six commits. The kind of day where you polish what shipped yesterday instead of building something new.

## git-with-intent: SDK Types

Two commits on git-with-intent. The SDK types needed an update — TypeScript definitions for the client library had drifted from the actual API surface.

New endpoints added in v0.10.0 (budget, quota, provider health) didn't have corresponding type definitions. Any TypeScript consumer of the SDK was either using `any` or maintaining their own type stubs.

The type update added interfaces for every public endpoint response:

- `BudgetStatus` — remaining balance, alert thresholds, current spend
- `QuotaLimits` — current usage, reset timestamps, tier limits
- `CircuitBreakerState` — provider name, failure count, recovery ETA
- `StepPagination` — page size, total count, cursor tokens

```typescript
// Before: consumers used 'any' or hand-rolled types
const budget = await client.getBudget(tenantId) as any;

// After: full type safety from the SDK
const budget: BudgetStatus = await client.getBudget(tenantId);
// budget.remainingBalance, budget.alertThreshold — all autocomplete
```

The barrel file also re-exports the error types — `QuotaExceededError`, `ProviderUnavailableError`, `TenantNotFoundError` — so consumers can catch specific errors instead of parsing message strings.

## E2E Documentation Rewrite

The E2E documentation got a rewrite focused on the test-to-deployment workflow. The original docs assumed familiarity with the codebase.

The new version assumes someone is running the suite for the first time — it starts with "clone the repo, install dependencies, copy `.env.example`" and walks through the first green test run.

The docs also cover the test data lifecycle. E2E tests create real tenants, real agent definitions, and real run records. All of that test data needs cleanup after the suite finishes.

The previous approach was manual — developers had to remember to run a cleanup script. The new docs explain the automatic teardown in the `afterAll` hook, and how to recover if a test crashes before teardown completes.

## intent-mail: Docker Deployment

Four commits on intent-mail. The first was Docker deployment — a multi-stage Dockerfile and docker-compose configuration.

SQLite storage lives on a mounted volume so data persists between container restarts. The compose file includes an optional Adminer service for inspecting the database during development.

The Dockerfile uses a Python 3.12 slim base with a two-stage build: the first stage installs build dependencies for the cryptography library (gcc, libffi-dev), the second stage copies only the compiled wheel and application code. Production image: 89MB.

## Gemini Review Fixes

The Gemini review from December 23rd flagged more issues beyond the rules engine parser.

Error messages in the Gmail connector leaked raw API response bodies, including potentially sensitive headers. The fix wraps API errors in a sanitized exception. A `401 Unauthorized` now says "Gmail authentication failed — token may be expired" instead of dumping the entire Google API error object.

Another catch: the attachment download endpoint didn't validate file size before streaming. A corrupted attachment reference could trigger an unbounded download. The fix adds a configurable size limit (default 25MB, matching Gmail's limit) and aborts if Content-Length exceeds it.

## The Audit Log

The audit log was the real addition. Every action the rules engine takes gets an immutable entry:

```sql
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    rule_name TEXT NOT NULL,
    message_id TEXT NOT NULL,
    action_type TEXT NOT NULL,
    action_detail TEXT,
    reversible BOOLEAN DEFAULT 1,
    reversed_at DATETIME
);
```

The `reversible` flag matters. Labeling is reversible — remove the label. Archiving is reversible — move it back. Deleting is not.

The rollback system checks this flag before undoing an action. Call `rollback(rule_name="auto-label-deploys", since="2025-12-23")` and every reversible action since that timestamp gets undone. Irreversible actions get logged as skipped.

This is the safety net for the rules engine. Deploy a new rule, watch it run for a day, realize it's too aggressive, roll it back. No manual cleanup of hundreds of mislabeled messages.

The audit table also serves as a debugging tool. When a user asks "why is this message in my deployments folder?" the audit log shows exactly which rule moved it, when, and what condition matched. One query instead of mentally simulating rule evaluation.

---

Six commits. SDK types that should've shipped with v0.10.0. Audit infrastructure that should've shipped with the rules engine. Christmas Eve is for the things you forgot to include the first time.

### Related Posts

- [Intent Mail: Full Email Platform in a Day — Gmail, Outlook, and a Rules Engine](/posts/intent-mail-full-platform-gmail-outlook-rules-engine/)
- [git-with-intent v0.9 to v0.10: Docker Upgrades, README Rewrites, and Strategic Research](/posts/git-with-intent-v090-v0100-docker-upgrades/)
- [Building Post-Compaction Recovery with Beads](/posts/building-post-compaction-recovery-beads/)
