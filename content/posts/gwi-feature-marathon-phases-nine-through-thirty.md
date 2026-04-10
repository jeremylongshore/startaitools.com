+++
title = 'Feature Marathon: git-with-intent Phases 9 Through 30'
slug = 'gwi-feature-marathon-phases-nine-through-thirty'
date = 2025-12-17T10:00:00-06:00
draft = false
tags = ["git-with-intent", "saas", "redis", "stripe", "marketplace", "reliability"]
categories = ["Development Journey"]
description = "38 commits across 22 phases: remote registry, SaaS control plane, tenant admin, workflow scheduler, PatchPlan forensics, metering, marketplace, and reliability infrastructure."
+++

Thirty-eight commits. Twenty-two phases. One day. This is what feature velocity looks like when the architecture is right and you're not fighting your own abstractions.

December 17th was a marathon day for git-with-intent. The connector framework from the previous day gave me a stable foundation. Now it was time to build everything that sits on top of it.

## The Phase Map

Here's what shipped, grouped by capability:

### Remote Registry (Phases 9-10)

The connector registry from phase 4 was local — connectors registered at startup and lived in memory. Phases 9-10 moved the registry to a remote service with API endpoints for registration, discovery, and health monitoring.

This matters because connectors can now be deployed independently. A GitLab connector running in one process registers itself with the remote registry. The core engine in another process discovers it. No shared memory, no monolith coupling.

Phase 10 added versioned connector metadata. When a connector registers, it declares its capabilities and version. The engine can select the newest compatible version if multiple connectors handle the same URL pattern.

### SaaS Control Plane (Phases 11-13)

Three phases building the multi-tenant management layer:

- **Phase 11**: Tenant provisioning. Create a tenant, allocate resources, generate API keys.
- **Phase 12**: Usage tracking. Every connector call, every analysis run, every output generation gets metered per tenant.
- **Phase 13**: Admin dashboard. View tenant usage, manage API keys, monitor system health.

The control plane is where the product becomes a business. Without it, git-with-intent is a tool. With it, git-with-intent is a service that can bill customers.

### Tenant Admin (Phase 14)

Self-service tenant administration. Tenants can manage their own API keys, view usage history, configure notification preferences, and set up team member access. This offloads the work that would otherwise go to a support inbox.

### Workflow Scheduler (Phases 15-16)

Automated analysis runs on a schedule. Tenants configure a cron expression and a list of repositories. The scheduler triggers analysis runs at the specified intervals and delivers results via webhook or email.

Phase 16 added retry logic for failed scheduled runs. If a scheduled analysis fails (connector timeout, rate limit exhaustion, transient error), the scheduler retries with backoff instead of silently dropping the run.

### Planner Service with PatchPlan (Phases 17-19)

The planner service is the intelligence layer. Given a repository's commit history and intent analysis, it generates a PatchPlan — a structured recommendation for what the team should work on next.

PatchPlans include:

- **Technical debt score** based on the ratio of refactor/fix commits to feature commits
- **Velocity trends** showing whether the team is accelerating or decelerating
- **Risk zones** identifying areas of the codebase with high churn and low test coverage
- **Recommended patches** with estimated effort and priority

This is where git-with-intent stops being a reporting tool and starts being an advisory tool. The commit history tells you what happened. The PatchPlan tells you what to do about it.

### Forensics: Replay and Collector (Phases 20-22)

Three phases building audit and forensics capabilities:

- **Phase 20**: Event collector. Every significant operation (connector call, analysis run, PatchPlan generation) emits an event to a durable log.
- **Phase 21**: Replay engine. Given a time range and a tenant, reconstruct exactly what the system did. Which connectors were called, what data was returned, what analysis was performed.
- **Phase 22**: Forensic queries. Search the event log by event type, tenant, connector, time range, or error code.

Forensics isn't a feature users ask for. It's a feature you need when something goes wrong and the user asks "what happened?" The replay engine lets you answer that question precisely instead of guessing.

### Metering and Billing (Phases 23-25)

The Stripe billing bridge. Phase 23 wired usage tracking to Stripe metering. Phase 24 added plan limits — free tier gets 5 repos/month, pro tier gets 100, enterprise gets unlimited. Phase 25 built the billing enforcement middleware that rejects API calls when a tenant exceeds their plan.

The billing bridge is deliberately simple. Usage events flow from the control plane to Stripe's metered billing API. Stripe handles invoicing, payment processing, and dunning. I don't want to be in the billing business. I want to sell a git analysis tool.

### Marketplace (Phases 26-28)

The connector marketplace. Phase 26 built the registry API — list available connectors, view details, read reviews. Phase 27 added publish flows — connector developers can submit their connectors for review and listing. Phase 28 built install flows — tenants can install marketplace connectors into their workspace with one click.

The marketplace closes the loop on the connector SDK from December 16th. Build a connector → publish to marketplace → users install it → usage gets metered → developer gets a revenue share. That's the ecosystem play.

### Reliability (Phases 29-30)

The final two phases hardened everything built above:

- **Redis rate limiting** across all API endpoints. Token bucket algorithm with per-tenant quotas. Redis handles the distributed state so rate limits work correctly across multiple API server instances.
- **Circuit breaker** on the marketplace registry. If the registry goes down, the system falls back to cached connector metadata instead of failing open.
- **Load tests** using k6 scripts. Simulated 100 concurrent tenants running analysis jobs to find bottlenecks. The scheduler was the first thing to choke — its job queue wasn't partitioned by tenant, so one tenant's burst could delay another tenant's scheduled runs.

## The Volume Question

Thirty-eight commits in one day for 22 phases. That's less than 2 commits per phase. Some phases were a single commit.

This isn't depth. It's breadth. Each phase established the foundation for a capability without polishing it to production quality. The billing bridge works but doesn't handle edge cases like mid-cycle plan changes. The marketplace works but doesn't have a review moderation workflow. The forensics replay works but doesn't have a UI.

That's the right tradeoff for this stage. Get the surface area covered, then deepen each capability based on what users actually need. Building a perfect billing system before a single customer has signed up is a waste.

The risk is that breadth without depth creates technical debt. Every unfinished edge case is a future bug report. The mitigation is documentation — each phase's commit message describes what was built AND what was deferred. When I come back to deepen billing, the commit message from phase 24 tells me exactly what's missing.

Twenty-two phases. One day. The architecture held.

---

## Related Posts

- [Architecture Reboot: git-with-intent Connector Framework](/posts/gwi-architecture-reboot-connector-framework/) — The connector SDK that made this marathon possible
- [Building Idempotent Stripe Billing Enforcement with Firestore](/posts/building-idempotent-stripe-billing-enforcement-firestore/) — A deeper dive into billing enforcement patterns
- [git-with-intent v0.9 to v0.10: Docker Upgrades and Strategic Research](/posts/git-with-intent-v090-v0100-docker-upgrades/) — Where the reliability work from phases 29-30 evolved
