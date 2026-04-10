+++
title = 'STCI Zero to v0.1.0: A Token Cost Index in One Day'
slug = 'stci-zero-to-v010-token-cost-index'
date = 2026-01-02T10:00:00-06:00
draft = false
tags = ["go", "data-pipeline", "cloud-run", "ci-cd", "docker", "gcp"]
categories = ["Development Journey"]
description = "From empty repo to production release in one day: OpenRouter collector, indexer, API, Docker, Cloud Run with Workload Identity Federation, CI/CD, and a daily cron."
+++

Yesterday's ADR said what STCI would be. Today it exists.

Eleven commits. One repo. Full pipeline from data collection to production API, released as v0.1.0 by end of day.

## The Pipeline

STCI — the token cost index — tracks LLM API pricing across providers and models over time. The problem it solves: model pricing changes silently. OpenAI adjusts rates. Anthropic launches new tiers. Google reprices Gemini. If you're running production workloads across multiple providers, you need a ledger of what things actually cost, not what the pricing page said last time you checked.

The pipeline has three stages:

**Collector** — pulls current pricing data from OpenRouter's model listing API. OpenRouter aggregates pricing from multiple providers, which means one API call gets you Anthropic, OpenAI, Google, Mistral, and dozens of others. The collector normalizes the response into a standard schema: model ID, provider, input price per token, output price per token, timestamp.

**Indexer** — processes collected data into a time-series index. Each run compares current prices against the previous snapshot. Changes get flagged. New models get added. Discontinued models get marked. The index is append-only — you never lose historical pricing data.

**API** — serves the index over HTTP. Query by model, by provider, by date range. Get the current price, the price history, or a diff between two dates. Simple REST. No GraphQL complexity for what amounts to a time-series lookup.

## The Infrastructure

Docker containerized the whole thing. One Dockerfile, multi-stage build. The Go binary compiles to a ~12MB static binary. The container image is under 20MB. Cloud Run doesn't charge for idle, so a small container that spins up on request and dies after serving is basically free.

Workload Identity Federation handles auth. No service account keys sitting in environment variables. The Cloud Run service identity authenticates to GCP services directly. This is the right way to do GCP auth in 2026 — if you're still downloading JSON key files, stop.

CI/CD runs on GitHub Actions. Push to main triggers: build, test, container build, push to Artifact Registry, deploy to Cloud Run. The whole pipeline takes about 90 seconds. Tag a release and goreleaser produces the binary artifacts.

The daily cron is a Cloud Scheduler job that hits the collector endpoint once per day. Pricing doesn't change hourly. Daily granularity captures every meaningful change without burning API quota.

## Tests

The test suite covers the three critical paths: collector parsing (does it handle malformed API responses?), indexer diffing (does it correctly identify price changes?), and API response formatting (does the JSON match the documented schema?).

Edge cases tested: provider returning null pricing fields, models that exist in one snapshot but not the next, timestamp parsing across timezone boundaries. The kind of stuff that breaks at 2am on a Saturday if you don't test it explicitly.

## What v0.1.0 Means

This is a first cut. The collector only talks to OpenRouter. Direct API integrations with Anthropic, OpenAI, and Google would give more granular data — things like per-tier pricing, volume discounts, and batch API rates that OpenRouter doesn't surface.

The index format is SQLite. That's fine for a single-node deployment. If this needs to scale to multiple collectors writing concurrently, it'll need a proper database. But premature scaling is how side projects die. SQLite works today.

v0.1.0 ships. It collects data. It serves queries. It runs on a cron. Tomorrow's problems are tomorrow's problems.

## The Velocity

Eleven commits in one day for a complete data pipeline is fast. It's fast because yesterday's ADR eliminated decision-making during implementation. Every schema choice, every API endpoint, every infrastructure decision was already made. Today was pure execution.

That's the argument for ADRs on greenfield projects. The ADR doesn't slow you down. It moves the slow work — design decisions, tradeoff analysis, scope negotiation — to a day when you're not also trying to write code. Implementation day becomes a sprint because the maze is already solved.

Zero to production in a day. Not because the work was trivial, but because the decisions were already made.

---

## Related Posts

- [Deploying Next.js 15 to Google Cloud Run with Custom Domain + SSL](/posts/deploying-nextjs-15-google-cloud-run-custom-domain-ssl/) — Another Cloud Run deployment with WIF auth patterns
- [SSE, Cloud Run, and Every Platform Lie](/posts/sse-cloud-run-every-platform-lie/) — The hard lessons about running stateful services on Cloud Run
- [git-with-intent v0.9.0-v0.10.0: Docker Upgrades](/posts/git-with-intent-v090-v0100-docker-upgrades/) — Docker and CI/CD patterns for Go projects in the same ecosystem
