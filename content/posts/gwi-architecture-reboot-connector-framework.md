+++
title = 'Architecture Reboot: git-with-intent Connector Framework and GA Hardening'
slug = 'gwi-architecture-reboot-connector-framework'
date = 2025-12-16T10:00:00-06:00
draft = false
tags = ["git-with-intent", "architecture", "connector-sdk", "reliability", "intentvision", "saas"]
categories = ["Technical Deep-Dive"]
description = "41 commits rebooting git-with-intent from legacy phases to a connector SDK architecture, plus IntentVision's pivot to SaaS commercialization."
+++

One day after bootstrapping git-with-intent to v0.2.0, I threw most of it away.

Not literally. The core intent classification engine survived. But the architecture around it — the CLI structure, the plugin system, the way connectors talked to the core — all of it got rebooted. Forty-one commits in a single day, and the result was a product that looked nothing like what shipped 24 hours earlier.

## Why Reboot After One Day

The v0.2.0 architecture had a fundamental problem: every integration was hardcoded. Want to analyze GitHub PRs? Write a GitHub module. Want to analyze GitLab MRs? Write a GitLab module. Want to read from Bitbucket? Another module. Each one duplicated the same patterns — authentication, pagination, rate limiting, error handling — with slight variations.

This is fine for a prototype. It's death for a product that needs to support arbitrary git platforms.

The connector SDK was the answer. Instead of writing platform-specific modules, define a connector interface and let each platform implement it. The core engine doesn't know or care whether it's reading from GitHub, GitLab, or a local bare repo. It talks to a connector, and the connector handles the platform-specific details.

This isn't a novel pattern. It's the adapter pattern from the Gang of Four book, applied to git platform integration. The novelty is deciding to do it on day two instead of day two hundred.

## The New Architecture: 8 Phases

The reboot followed 8 phases across 41 commits.

### Phase 1: Connector Interface Definition

The core abstraction:

```typescript
interface GitConnector {
  // Discovery
  listRepositories(org: string): AsyncIterable<Repository>;
  
  // Read operations
  getCommits(repo: Repository, opts: CommitQuery): AsyncIterable<Commit>;
  getDiff(repo: Repository, ref: string): Promise<Diff>;
  getBranches(repo: Repository): AsyncIterable<Branch>;
  
  // Metadata
  getPullRequests(repo: Repository, opts: PRQuery): AsyncIterable<PullRequest>;
  getReviews(pr: PullRequest): AsyncIterable<Review>;
  
  // Lifecycle
  connect(config: ConnectorConfig): Promise<void>;
  disconnect(): Promise<void>;
  healthCheck(): Promise<HealthStatus>;
}
```

Every method that returns multiple items uses `AsyncIterable`. This is the key design decision. Connectors can paginate internally without the caller knowing or caring about page sizes. A GitHub connector paginates at 100 items per page. A local git connector reads from `git log` with no pagination. Same interface.

The `healthCheck()` method was added after I realized that connectors to remote platforms can fail silently. A GitHub token might expire mid-session. A GitLab instance might go down. The health check gives the core engine a way to verify connectivity before starting an expensive analysis run.

### Phase 2: Local Git Connector

The first connector implementation was the local git connector. It wraps `git` CLI commands — `git log`, `git diff`, `git branch` — and parses their output into the connector interface types.

This is the least exciting connector but the most important for testing. Every other connector gets validated by comparing its output against the local connector's output for the same repository. If the GitHub connector returns different commits than `git log` for the same repo, the GitHub connector has a bug.

### Phase 3: GitHub Connector

The GitHub connector uses Octokit with automatic pagination and token rotation. Rate limiting is handled at the connector level — if GitHub returns a 429, the connector backs off and retries without the core engine knowing.

Token rotation was the tricky part. GitHub's API rate limit is per-token. If you're analyzing a large organization with thousands of repos, a single token's 5,000 requests/hour limit isn't enough. The connector accepts multiple tokens and rotates through them, tracking rate limit headers to pick the token with the most remaining quota.

### Phase 4: Connector Registry

A central registry where connectors self-register. The core engine queries the registry for a connector that can handle a given repository URL. URL patterns determine which connector handles which repo:

- `https://github.com/*` → GitHub connector
- `https://gitlab.com/*` → GitLab connector  
- `/path/to/local/repo` → Local git connector
- `ssh://git@*` → SSH connector (delegates to local after clone)

The registry also handles connector lifecycle — initialization, health monitoring, and graceful shutdown.

### Phase 5: Reliability Layer

This phase added the infrastructure that separates a demo from a product:

**Circuit breakers** on every remote connector. If a connector fails 3 times in 60 seconds, the circuit opens and the connector reports itself unhealthy. The core engine can then fall back to a different connector or report the failure to the user.

**Retry with exponential backoff.** Not just for rate limiting — also for transient network failures, DNS resolution hiccups, and TLS handshake timeouts. Maximum 3 retries with jitter to prevent thundering herd.

**Request deduplication.** If the core engine requests the same commit diff twice (which happens during multi-pass analysis), the connector returns the cached response instead of making a second API call. Cache lifetime is 5 minutes — long enough to cover a single analysis run, short enough to not serve stale data.

### Phase 6: Connector SDK

The SDK packages the connector interface, base classes, test fixtures, and validation tools into a publishable package. Third-party developers can build connectors without cloning the entire git-with-intent repo.

The test fixtures were the real value. The SDK includes a `ConnectorTestSuite` that validates any connector implementation against the interface contract. Implement the interface, run the test suite, and if it passes, your connector works with git-with-intent. No manual validation needed.

### Phase 7: GA Hardening

General availability prep. Error messages went from developer-friendly (`TypeError: Cannot read property 'sha' of undefined`) to user-friendly (`Repository 'org/repo' returned no commits. Check your access token permissions.`). Every error path got a human-readable message with a suggested fix.

Logging got structured. JSON log lines with correlation IDs so you can trace a single analysis run across connector calls, core engine processing, and output generation. The correlation ID propagates through `AsyncLocalStorage` — no manual threading required.

### Phase 8: Integration Tests

End-to-end tests that exercise the full path: URL in → connector selection → data fetch → intent analysis → output generation. These tests run against real GitHub repos (read-only, public repos) and validate that the connector framework actually works in production conditions, not just in mocked unit tests.

The integration test suite takes 45 seconds to run because it's making real HTTP calls. That's acceptable for a CI pipeline that runs on PR merge. It's not acceptable for local development, so the tests are gated behind a `--integration` flag.

## IntentVision: SaaS Pivot

While git-with-intent was getting its architecture reboot, IntentVision pivoted from a local tool to a SaaS product. Five commits, all focused on commercialization:

1. **Multi-tenant data isolation.** Each organization gets its own data partition. No shared tables, no tenant ID columns — actual schema-level isolation using PostgreSQL schemas.
2. **Stripe billing integration.** Usage-based pricing tied to the number of repositories analyzed per month.
3. **Authentication.** OAuth with GitHub (the primary identity provider for the target audience).
4. **Dashboard hosting.** Move from static HTML export to a hosted dashboard with live data.
5. **Landing page.** Product positioning, pricing tiers, CTA to sign up.

The SaaS pivot made sense because IntentVision's value proposition requires persistent data. A one-time static report is useful. A dashboard that shows trends over time is worth paying for.

## What the Reboot Preserved

Not everything from v0.2.0 was thrown away. The intent classification engine — the core algorithm that reads a diff and determines whether it's a feature, fix, refactor, or chore — survived unchanged. It was the one part of the architecture that had no coupling to the platform integration layer.

The classification engine takes a `Diff` object as input and returns an `IntentClassification`. It doesn't know where the diff came from. GitHub, GitLab, local git, a file on disk — the engine doesn't care. That abstraction boundary existed in v0.2.0 by accident (I wrote it that way because it was simpler, not because I planned for a connector framework). The reboot formalized what was already implicit.

The configuration system also survived. User preferences, repo-level overrides, and default values all carried over. Configuration is orthogonal to platform integration, so the connector reboot didn't touch it.

What got thrown away: the CLI command structure (rebuilt around connector discovery), the output pipeline (rebuilt to support multiple output targets per connector), and every line of code that mentioned "GitHub" by name outside the GitHub connector module. About 60% of v0.2.0's code was replaced.

## The Cost of Rebooting Early

Forty-one commits to reboot an architecture that was 24 hours old. That sounds wasteful. It wasn't.

The alternative was building 3 more hardcoded platform modules, then realizing the pattern was wrong, then refactoring while trying to maintain backward compatibility with users who had already integrated the hardcoded modules. That refactoring would have been 200+ commits and broken every existing integration.

Rebooting on day two cost 41 commits and broke nothing because nothing was in production yet. The connector SDK shipped as the first stable interface. No migration guides needed. No deprecation notices. No angry users.

The lesson isn't "always reboot your architecture on day two." The lesson is that the cost of architectural change is a function of how much depends on the current architecture. On day two, the answer is "nothing." On day two hundred, the answer might be "everything." If you're going to make a fundamental change, make it when the cost is lowest.

Forty-six commits across two products. One architecture rebooted. One product pivoted to SaaS.

The connector SDK became the stable foundation that everything else — phases 9 through 70 — would build on over the next two days.

---

## Related Posts

- [Two Products Bootstrapped from Zero to Release in One Day](/posts/gwi-intentvision-bootstrap-two-products-one-day/) — The day before this reboot
- [Fixing Provider Registry Mutations and Sandbox Permissions](/posts/fixing-provider-registry-mutations-sandbox-permissions/) — A later registry bug that the connector framework's design prevented from recurring
- [Vertex AI Agent Engine's Architecture Pivot](/posts/pipelinepilot-vertex-ai-migration-architecture-pivot/) — Another same-day architecture reboot forced by a platform limitation
