+++
title = 'IRSB Agent Passkey Scaffold on Cloud Run and Perception v0.6.0 Trending'
slug = 'irsb-agent-passkey-cloud-run-perception-v060-trending'
date = 2026-02-06T10:00:00-06:00
draft = false
tags = ["irsb", "passkey", "cloud-run", "wif", "perception", "hacker-news", "trending", "e2e-tests"]
categories = ["Development Journey"]
description = "IRSB scaffolds an agent-passkey service with Cloud Run WIF deployment and an AgentPasskeyClient. Perception ships v0.6.0 with HN Popular Blogs, trending articles, auth redirect fixes, and E2E tests."
+++

Two projects, twelve commits total, and each shipped something tangible. IRSB got its first agent authentication scaffold. Perception tagged a release. Neither project had more than six commits, but both moved from "in progress" to "deployed."

## IRSB: Agent Passkey on Cloud Run

Six commits building the agent-passkey service from scratch and deploying it to Cloud Run.

### The Problem

IRSB's agents need to authenticate against the protocol. Traditional API keys don't work well for autonomous agents — keys get leaked in logs, rotated keys break running agents that cached the old key, and there's no way to scope permissions per agent instance without building a custom authorization layer on top.

Passkeys (WebAuthn/FIDO2) provide a cryptographic identity that doesn't require secret management. The private key never leaves the agent's environment. Authentication is a challenge-response proof, not a shared secret.

### AgentPasskeyClient

The client library that agents import to authenticate. It handles two ceremonies:

- **Registration:** Creating a new passkey bound to an agent identity. One-time operation that creates the on-chain identity record.
- **Authentication:** Proving identity on each request. Returns a signed token that the IRSB gateway validates.

The client stores the private key material in the agent's local keystore — on Linux, a file in `~/.irsb/keys/` with 0600 permissions. On Cloud Run, it uses the instance's metadata service to derive a deterministic key from the service identity.

The authentication token includes the agent's identity, capabilities, and a timestamp. It expires after 5 minutes — short enough that a stolen token is nearly useless, long enough that normal request latency doesn't cause expiration between token generation and validation. The 5-minute window was chosen empirically: the longest observed end-to-end request in the IRSB system takes about 30 seconds during complex bounty resolution queries.

The client also handles token refresh transparently. If a request fails with a 401, the client re-authenticates and retries once before surfacing the error. This handles the edge case where a token expires mid-flight.

### Cloud Run with Workload Identity Federation

The passkey verification service runs on Cloud Run. Instead of using a service account key file (which is itself a secret management problem — you need a secret to manage your secrets), the deployment uses Workload Identity Federation.

The WIF setup is three pieces:

- A Workload Identity Pool in GCP that defines a trust boundary
- A provider configured to trust GitHub's OIDC issuer for the specific repository
- An IAM binding that maps the GitHub repository identity to a GCP service account

The service account has only the permissions the Cloud Run service needs — Firestore read/write for passkey storage, Secret Manager read for configuration, and Cloud Run invoker for the health check endpoint. No service account keys exist anywhere — not in the repo, not in GitHub secrets, not on any developer's machine.

### Gateway Logger Fix

One of the six commits was a bug fix. The gateway service was logging request bodies at INFO level, including authentication payloads. In development this is convenient. In production this means auth tokens appear in Cloud Logging where anyone with log viewer access can see them.

The fix drops request body logging to DEBUG (disabled in production) and adds a redaction filter that replaces any field matching "key," "secret," "token," or "passkey" with `[REDACTED]`. The redaction runs before serialization, so even if someone changes the log level to DEBUG in production, the sensitive fields are still scrubbed.

## Perception: v0.6.0

Six commits pushing Perception to v0.6.0 with three features and a test suite.

**HN Popular Blogs integration.** The 92 feeds added yesterday are now fully indexed and appearing in the dashboard. Each article gets a source attribution badge showing whether it came from the curated feed list (blue badge) or the HN Popular Blogs collection (green badge).

The distinction helps users understand why an article is in their feed — curated sources were hand-picked for direct relevance, HN Popular sources are algorithmically selected for broad reach. Different editorial standards, clearly labeled.

**Trending articles.** An algorithm that surfaces articles gaining traction across multiple feeds. If three independent blogs link to or discuss the same topic within 48 hours, that topic gets flagged as trending. The algorithm uses URL normalization (strip tracking parameters, resolve redirects, canonicalize) and keyword extraction (TF-IDF against the corpus) rather than exact URL matching.

The trending algorithm runs every 30 minutes. Each run scores topics by the number of independent sources, recency of mentions, and authority score of the sources. A topic mentioned by three high-authority blogs in 6 hours scores higher than one mentioned by five low-authority blogs over 48 hours.

**Auth redirect fix.** After login, users were being redirected to the root URL instead of the page they were trying to access. The fix stores the intended destination in the session before redirecting to the auth provider, then reads it back after successful authentication. Standard pattern, but the bug had been there since launch. Nobody reported it because most users bookmarked the dashboard directly.

**E2E tests.** Playwright tests covering the critical paths: login flow, feed browsing, article detail view, trending topics page, feed category filtering, and source attribution badges. Six tests running against a local instance with seeded data — 50 articles across 10 feeds with predetermined trending topics. The test suite adds about 45 seconds to the CI pipeline on every PR.

Six tests isn't comprehensive coverage, but it's the right starting set. These are the flows that break most often (login redirect was literally broken until today) and the flows that users hit first. Adding tests for edge cases comes later. Getting the critical path covered comes first.

Twelve commits across two projects. The passkey service gives IRSB agents a cryptographic identity without secret management. Perception v0.6.0 gives users trending topics and better feed attribution. Both shipped. Both deployed.

---

## Related Posts

- [Perception Agent System: Zero to MCP Dashboard in One Day](/posts/perception-agent-system-zero-to-mcp-dashboard/) — Perception's initial build from zero
- [Deploying Next.js 15 to Google Cloud Run with Custom Domain and SSL](/posts/deploying-nextjs-15-google-cloud-run-custom-domain-ssl/) — The Cloud Run deployment patterns used in the IRSB passkey service
- [Building Moat: Auth, Persistence, On-Chain Receipts, and 117 Tests](/posts/building-moat-auth-persistence-onchain-receipts-117-tests/) — Earlier IRSB authentication and on-chain identity work
