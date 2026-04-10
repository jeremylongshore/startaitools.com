+++
title = 'Eleven-Repo Sprint: ADK Deployment Battle, STCI Redesign, and Scattered Fixes'
slug = 'eleven-repo-sprint-adk-deployment-battle-stci-redesign'
date = 2026-01-04T10:00:00-06:00
draft = false
tags = ["gcp", "adk", "agent-engine", "next-js", "e2e-testing", "ci-cd", "go"]
categories = ["Development Journey"]
description = "87 commits across 11 repos. Perception ADK Agent Engine deployment burns 22 commits on fix iterations, intent-mail gets AI compose, and STCI pivots to premium subscriptions."
+++

Eighty-seven commits. Eleven repos. Most of them fixes.

January 4th was the kind of day where the commit count looks impressive and the actual progress is modest. High volume, scattered focus. Here's the honest breakdown.

## The Perception ADK Deployment Battle

Twenty-two commits on Perception. Almost all of them deployment fixes.

The Perception agent runs on Google's ADK (Agent Development Kit) with Agent Engine as the hosting layer. Agent Engine is Google's managed runtime for ADK agents — you deploy your agent definition and it handles scaling, versioning, and endpoint management.

In theory.

In practice, deploying to Agent Engine on January 4th meant hitting a wall of configuration issues. The agent definition would validate locally, pass unit tests, and then fail on deploy with cryptic error messages about resource specifications. Fix one, hit another. Fix that, hit a third.

The commit log tells the story:

- `fix: agent engine resource spec format`
- `fix: agent engine deployment config`
- `fix: correct service account permissions`
- `fix: agent engine timeout configuration`
- `fix: deployment retry logic`

And so on. Twenty-two times. Each commit a small adjustment, a redeploy, a wait, a new error. This is what deploying to a relatively new managed service looks like. The documentation covers the happy path. The error messages cover nothing useful. You iterate.

By end of day, the agent was running on Agent Engine. But 22 commits to get there is not a victory lap. It's a battle of attrition.

## intent-mail: AI Compose and Security

The email platform picked up two features: AI-assisted compose and security hardening.

AI compose uses the LLM to draft email responses based on the thread context. Select a thread, hit compose, and the model generates a draft that matches the conversation tone and addresses the open questions. You edit before sending — it's a draft tool, not an auto-responder.

Security work included rate limiting on the API endpoints and input sanitization on the rules engine. The rules engine accepts user-defined conditions, which means it accepts user-defined strings that get evaluated. Without sanitization, that's an injection vector. Standard OWASP stuff, but the kind of thing you patch before it becomes a headline.

## STCI Premium Redesign

Two days after v0.1.0, STCI got a scope expansion. The original design was a free API serving token pricing data. The redesign adds a premium tier with subscription management and analytics dashboards.

Subscription handling uses Stripe. Analytics track query patterns — which models get looked up most, which providers get compared, what date ranges are popular. The analytics aren't just for billing. They tell you what the users actually care about, which informs what data to collect next.

This is a significant pivot from "free tool" to "freemium product." Whether it's the right call depends on whether anyone actually uses the free tier. Ship the premium infrastructure now, validate demand later.

## The Rest of the Scatter

**Hustle** — Next.js 15 E2E test fixes. The E2E suite was failing intermittently on CI. Root cause: race conditions in the test setup where the dev server wasn't fully ready when Playwright started hitting endpoints. Added health check polling before test execution.

**Intent Blueprint Docs** — Phase 1 of a documentation generation system. Scaffolding, templates, initial content structure. Foundation work for a bigger build coming soon.

**Go project CI polish** — Linting configuration, build matrix updates, and dependency pinning across multiple Go repos. The kind of maintenance work that prevents future CI failures but doesn't produce anything visible.

## Why 87 Commits Doesn't Mean 87 Units of Progress

The Perception deployment alone was 22 commits of fix-iterate-fix. That's not 22 features. That's one feature with 21 false starts. The intent-mail AI compose was real progress. The STCI redesign was real progress. The rest was maintenance.

Days like this are important to log honestly. The commit count makes it look like a productive day. The reality: one deployment battle consumed most of the energy, and everything else got scraps of attention.

Scatter days happen. The discipline is recognizing them for what they are instead of inflating the narrative.

---

## Related Posts

- [Perception Agent System: Zero to MCP Dashboard](/posts/perception-agent-system-zero-to-mcp-dashboard/) — The Perception system before the ADK deployment battle
- [How to Get an ADK Agent into the Google Community Showcase](/posts/how-to-get-adk-agent-into-google-community-showcase/) — ADK patterns and Google's agent ecosystem
- [GWI v0.3.0 Release, Hustle CI Green, Intent-Mail AI](/posts/gwi-v030-release-hustle-ci-green-intent-mail-ai/) — Earlier intent-mail and Hustle CI work
