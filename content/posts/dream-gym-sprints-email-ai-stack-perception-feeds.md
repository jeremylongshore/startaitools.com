+++
title = 'Dream Gym Sprints, Email AI Stack, and 128 RSS Feeds'
slug = 'dream-gym-sprints-email-ai-stack-perception-feeds'
date = 2025-12-29T10:00:00-06:00
draft = false
tags = ["full-stack", "ai-email", "rss", "tui", "hustlestats", "intent-mail", "perception", "git-with-intent"]
categories = ["Development Journey"]
description = "Hustle ships Dream Gym sprints 1-3 with workout logging and analytics. Intent Mail builds AI email intelligence with PII sanitization. Perception hits 128 feeds and a cyberpunk TUI. GWI patches webhook Dockerfiles."
+++

Four projects. Thirty-eight commits. Two of them are building real product features, one is growing into an intelligence platform, and one just needed a Dockerfile fix.

## Dream Gym: Sprints 1 Through 3

Hustle's Dream Gym module went from concept to working product in three sprints and fourteen commits.

**Sprint 1: Workout Logging.** The core data model is straightforward — exercises, sets, reps, weight, duration. But the UX question was whether to optimize for speed or detail. Speed won.

A workout entry is: pick exercise from favorites, enter weight and reps, tap done. Three taps for a working set. The full detail view (tempo, RPE, rest intervals) is there but collapsed by default. Nobody wants to fill out a form between sets. The exercise favorites list learns from usage — exercises you log frequently float to the top.

**Sprint 2: Journal.** Workout data captures what you did. The journal captures how it felt. Free-text entries tagged to specific workout sessions. Each entry links to a workout session ID, so the analytics layer can later correlate subjective state ("felt strong, slept 8 hours") with objective performance numbers. For now, it's structured text with timestamps and workout references. The journal also accepts mood tags — a simple 1-5 scale — for users who don't want to write paragraphs but still want to track how they felt.

**Sprint 3: Analytics and Charts.** Volume over time, PR tracking, muscle group distribution, session frequency. Chart.js handles the rendering. The interesting part isn't the charts — it's the data pipeline feeding them. Workout entries are denormalized into a `workout_stats` collection at write time. Every time a set is logged, a Cloud Function updates the aggregate document for that exercise, that muscle group, and that week. The charts read from pre-computed aggregates instead of running queries against raw workout data. This means the analytics page loads in under 200ms regardless of how many workouts are in the database.

The PR tracking deserved its own mention. Personal records get stored as a separate subcollection keyed by exercise. When a new set exceeds the previous max for that exercise, the PR document updates and the UI shows a celebration animation. Small touch, but it's the kind of feedback loop that makes people log workouts consistently.

Auth hardening also landed in this sprint batch. Firebase Auth rules tightened so users can only read and write their own workout data. Sounds obvious, but the initial Firestore rules were permissive during development — `allow read, write: if true` is a fast way to prototype and a fast way to leak data.

Locking them down before anyone else touches the app is non-negotiable. Workout data is personal data.

## Intent Mail: AI Email Intelligence

Fourteen commits pushed Intent Mail from "AI provider abstraction" to "AI email intelligence."

**Summarization** condenses long email threads into key points. Not a generic summary — structured extraction of action items, decisions made, questions asked, and deadlines mentioned. The output is JSON, not prose. Each extracted item has a type, the relevant quote from the thread, and the sender who said it.

The prompt engineering took more iteration than expected. Generic "summarize this" prompts produce generic summaries. The structured extraction prompt specifies exactly what to pull and in what format. It took four prompt revisions to get the action item extraction right — early versions would invent action items from conversational phrasing. "We should grab coffee sometime" is not an action item. "Please review the PR by Friday" is.

**Inbox triage** scores messages on urgency and relevance. The scoring model considers sender history (have you replied to this person before?), content signals (contains "deadline," "urgent," "by EOD"), and thread position (new thread vs. deep reply). Messages get bucketed into Act Now, Review Today, Read Later, and Archive. The goal is reducing a 50-message inbox scan to a 5-message priority list.

**Smart compose** suggests replies based on thread context and your writing patterns. This is the feature that needs the most caution. Suggesting a reply that sounds like you but says something you wouldn't is worse than no suggestion at all. The initial implementation is conservative — it suggests reply structures (acknowledge, answer, ask follow-up) rather than full text.

**Multi-surface architecture** means these AI features work in both the CLI and TUI. The intelligence layer doesn't know which surface is calling it. Same API whether you're running `intent-mail triage` in a pipeline or interacting through the TUI dashboard.

**PII sanitization** strips personally identifiable information before any content hits an LLM provider. Email addresses, phone numbers, and names get replaced with tokens. The LLM sees `[PERSON_1] asked [PERSON_2] to call [PHONE_1]` instead of real data. Tokens get rehydrated in the response. The token map is held in memory for the duration of the request and discarded — it never persists to disk or gets logged.

This isn't optional — sending someone else's email content to a third-party API without sanitization is a liability. The sanitizer runs as middleware in the provider router, so every AI feature gets PII protection regardless of whether the feature developer remembered to add it.

## Perception: 128 Feeds and a Cyberpunk TUI

Perception crossed 128 RSS feed sources and shipped v0.4.0.

The feed count matters because it's the threshold where naive polling breaks. At 128 feeds with a 15-minute refresh interval, you're making 512 HTTP requests per hour. Some feeds are slow. Some return 500s intermittently. Some return 403s during peak traffic because the publisher's CDN rate-limits feed readers.

The ingestion pipeline now uses a priority queue with exponential backoff per feed. Healthy feeds poll on schedule. Flaky feeds back off automatically and recover when they stabilize. The backoff caps at 2 hours — beyond that, the feed is marked degraded and an alert fires.

The cyberpunk TUI dashboard is pure indulgence. Green-on-black terminal interface with box-drawing characters, scrolling feed tickers, and color-coded alert levels. It's a monitoring dashboard that looks like it belongs in a 90s hacker movie. Functionally identical to a plain text status page. Aesthetically, much more fun to leave running on a second monitor.

The eight feeds panel shows real-time ingestion status per source category — tech, security, AI, business, policy, research, open-source, and general news. Each category aggregates its feed health into a single status indicator. Green means all feeds in the category polled successfully in the last cycle. Yellow means degraded (some feeds backing off). Red means the category is stale.

v0.4.0 bundles the feed scaling improvements, the TUI, and a batch of reliability fixes for the article deduplication pipeline. The dedup fixes addressed a content-hash collision problem where feeds that republish slightly edited versions of the same article (updated timestamp, minor wording change) were creating duplicate entries. The hash now covers title + first 500 characters of content + source URL, which catches cosmetic edits while still deduplicating genuine reposts.

## GWI: Webhook Dockerfile Fixes

Two commits. The webhook receiver's Dockerfile had a build stage that copied the wrong directory structure, causing the production image to miss its config files. Straightforward fix — update the `COPY` paths to match the monorepo layout after a recent directory restructure.

Small commits. Big consequences if they'd shipped broken. Webhook receivers that can't read their config silently drop events. No error, no crash, no alert. Just events that vanish into nothing. The worst kind of production bug is the one where everything looks healthy.

## The Throughput Question

Four projects in a single day raises the obvious question: is this sustainable? The answer is that these aren't four parallel deep-focus sessions. Dream Gym sprints were planned and executed sequentially. Intent Mail's AI features built on the provider abstraction from two days ago. Perception's feed scaling was a known backlog item. The Dockerfile fix took 10 minutes.

The trick isn't working on four projects simultaneously. It's having four projects at different stages where the next step on each one is clear enough to execute without re-reading the entire codebase. Dream Gym had a sprint plan. Intent Mail had an architecture doc. Perception had a backlog ticket. The Dockerfile had a failing health check. Context-switching cost is proportional to the ambiguity of what you're switching to.

---

**Related Posts:**

- [Perception Agent System: Zero to MCP Server and Dashboard in One Day](/posts/perception-agent-system-zero-to-mcp-dashboard/) — Perception's origin story and the agent architecture these feeds power
- [Building a Multi-Brand RSS Validation System: 97 Feeds Tested](/posts/building-multi-brand-rss-validation-system-97-feeds-tested/) — RSS feed validation patterns at scale
- [HustleStats Launch Sprint: From Firebase Auth to Production SaaS with Stripe Billing in One Day](/posts/hustlestats-launch-sprint-stripe-billing-paywall/) — The Hustle billing infrastructure Dream Gym runs on
