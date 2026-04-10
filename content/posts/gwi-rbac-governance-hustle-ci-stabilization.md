+++
title = 'GWI RBAC Governance and Hustle CI Stabilization'
slug = 'gwi-rbac-governance-hustle-ci-stabilization'
date = 2025-12-26T10:00:00-06:00
draft = false
tags = ["rbac", "governance", "ci-cd", "git-with-intent", "hustle", "e2e-testing"]
categories = ["Development Journey"]
description = "git-with-intent adds RBAC governance: tenant management, quotas, secrets, and audit trail, plus marketplace E2E tests. Hustle stabilizes after merge conflicts and Gemini review fixes."
+++

December 26th. Three commits on git-with-intent, three on hustle. The GWI work was about governance. The hustle work was about not breaking things.

## git-with-intent: RBAC and Governance

The RBAC system adds the multi-tenant access layer that git-with-intent needed before any real organization could use it. Three commits covering the full governance surface.

### Tenant Management

Each tenant gets an isolated namespace with its own configuration, agent definitions, and run history.

Tenant creation provisions the namespace, sets default quotas, and generates an API key scoped to that tenant. Tenant deletion is soft — the namespace gets marked inactive, data is retained for the audit retention period, and the API key is revoked immediately.

Reactivation is supported with a new API key, preserving the historical data.

### Quotas

Per-tenant rate limits on API calls, agent runs, and storage consumption. The quota system is configurable per tier:

- **Free tier:** 100 agent runs per month
- **Paid tier:** 10,000 agent runs per month
- **Enterprise tier:** unlimited with spend alerts

Quota checks happen at the API gateway level, before the request reaches the application layer. An over-quota request gets a 429 with a `Retry-After` header.

The implementation stores current usage in an in-memory counter with periodic flush to the database. This avoids a database read on every API call. The flush interval defaults to 60 seconds, and a flush happens on process shutdown.

### Secrets Management

Tenants can store secrets (API keys for LLM providers, webhook URLs, authentication tokens) that agents access at runtime.

Secrets are encrypted at rest using AES-256-GCM. Agent code never sees raw secrets — it calls `get_secret(name)` which decrypts and returns the value in memory without persisting it to logs or step history.

Secret rotation works without downtime. Store a new version and the old version remains valid for a configurable grace period (default 1 hour). In-flight agent runs that cached the old secret still work. After the grace period, only the new version authenticates.

### Audit Trail

Every governance action gets an immutable audit entry: who made the change, when, what the old value was, what the new value is.

The log is append-only with a cryptographic chain — each entry includes a hash of the previous entry, so tampering with historical records breaks the chain.

This isn't application logging. It's the compliance artifact that an auditor asks for when they want to verify access controls are enforced.

## Marketplace E2E Tests

git-with-intent has a marketplace where tenants publish and install agent definitions. The E2E tests cover the full lifecycle:

1. Create a tenant
2. Publish an agent definition
3. Search the marketplace
4. Install the agent
5. Run it and verify output
6. Uninstall it

These tests run against a real (local) instance of the platform, not mocks. The test fixture spins up the API server, provisions a test tenant, and tears everything down after the suite finishes.

The E2E tests also validate the RBAC layer. A tenant with "viewer" permissions can search and install but can't publish. A "publisher" can publish but can't modify other tenants' agents. An "admin" can do everything.

## Hustle: Merge Conflicts and Review Fixes

Three commits on hustle, and none of them were features.

### Auth Middleware Merge

A merge conflict from concurrent Dream Gym and HustleStats development needed manual resolution. The conflict was in shared auth middleware — both products added Firebase Auth checks with slightly different configurations.

The resolution unified the auth middleware with product-specific config injected at startup. Both products use the same middleware with different session durations and role mappings.

The merge also cleaned up dead code — both products had independently created a `validateSession` helper with identical implementations. The unified middleware replaced both copies with a single shared function.

### Gemini Review Fixes

The Gemini reviewer caught two issues from earlier PRs.

First: Dream Gym registration created Firebase users with `emailVerified: true` before the user actually verified. The fix sets it to `false` and relies on the verification email flow.

Second: a test fixture hardcoded port 3847 for the dev server. Passed locally, failed in CI where the port was already in use. The fix uses port 0 (OS-assigned) and reads the actual port from startup output.

Port collisions are inevitable in shared CI environments. Port 0 should be the default in every test fixture that starts a server.

---

Six commits. GWI has governance. Hustle has stability. The day after Christmas is for the infrastructure that makes other days productive.

### Related Posts

- [git-with-intent v0.9 to v0.10: Docker Upgrades, README Rewrites, and Strategic Research](/posts/git-with-intent-v090-v0100-docker-upgrades/)
- [Christmas Day: Dream Gym MVP and Intent Mail IMAP Connector](/posts/christmas-day-dream-gym-mvp-intent-mail-imap/)
- [Marketplace Security Framework: Building Scanner, Battling False Positives](/posts/marketplace-security-framework-scanner-false-positives/)
