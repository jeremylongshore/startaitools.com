+++
title = 'GWI IDP Specification Suite, Bounties EV Scoring, and IRSB Resilience Patterns'
slug = 'gwi-idp-spec-suite-bounties-ev-scoring-irsb-resilience'
date = 2026-02-03T10:00:00-06:00
draft = false
tags = ["git-with-intent", "idp", "bounties", "irsb", "intentvision", "intent-mail", "specifications", "resilience"]
categories = ["Development Journey"]
description = "Fifty-five commits across six repos. git-with-intent produces 20+ IDP specification documents and removes 2,735 lines of dead code. Bounties ships EV scoring. IRSB adds resilience patterns and a webhook sink."
+++

Fifty-five commits across six repos. The highest single-day commit count of the month, though the commit count overstates the architectural significance. Most of these were specification documents, not code.

## git-with-intent: The IDP Specification Sprint

Twenty-nine commits, and the bulk of them were specification documents for an Internal Developer Platform.

The IDP spec suite covers the standards a platform team needs to evaluate and enforce:

- RAG pipeline specifications (chunking strategy, embedding model requirements, retrieval evaluation thresholds)
- DORA metrics tracking (deployment frequency, lead time, change failure rate, MTTR)
- SOC2 compliance requirements (access control logging, data retention policies, incident response)
- SAST integration standards (which tools, which severity levels block merge, false positive handling)
- Feature flag governance (TTL requirements, flag cleanup automation, percentage rollout gates)
- Incident response procedures (severity classification, escalation paths, post-mortem templates)

Twenty-plus documents in total, each following the same template — purpose, scope, requirements, validation criteria, and integration points with git-with-intent's analysis engine.

The template matters. Every spec document has a "Validation Criteria" section that describes exactly how git-with-intent can verify compliance. The feature flag spec says flags must have a TTL field. The validation criterion says "scan for flag declarations matching pattern X and assert TTL field is present and non-zero." That's machine-executable. The spec isn't just a policy document — it's an input to the analysis engine.

These specs position git-with-intent as an IDP component rather than a standalone tool. An IDP that can enforce its own specifications through automated analysis is more valuable than one that just publishes standards and hopes people follow them.

The other significant git-with-intent work: 2,735 lines of dead code removal. Modules that were scaffolded during the early phases but never connected to anything. Test fixtures for features that were redesigned. Configuration schemas for abandoned approaches. The dead code wasn't hurting anything at runtime, but it was confusing anyone trying to understand the codebase. Less code, less confusion.

The version went from v0.7.0 to v0.7.1 — minor bump because the specs are additive and the dead code removal doesn't change behavior. Twenty-nine commits sounds impressive until you realize most of them are `git add specs/soc2-compliance.md && git commit`. The spec documents are the intellectual work. The commits are just filing.

## Bounties: EV Scoring and Competition Monitoring

Eight commits pushing bounties to v0.2.0. The headline feature is expected value scoring.

EV scoring assigns each bounty a score based on four factors:

- **Payout** — the bounty amount in dollars
- **Estimated effort** — hours based on historical data for similar bounties (not the poster's estimate, which is consistently too low)
- **Competition level** — number and strength of existing claims
- **Maintainer responsiveness** — average review turnaround time from the maintainer profile

The formula: `EV = (payout / estimated_hours) * (1 / competition_factor) * maintainer_speed_bonus`. The maintainer speed bonus is a 2x multiplier for maintainers averaging under 24 hours, 1x for under a week, 0.5x for over a week.

Competition monitoring is the data layer for the competition factor. It tracks how many claims each bounty has, how many are from known strong submitters (based on past resolution rate), and whether the bounty is trending on aggregator sites. A bounty that just appeared on a popular aggregator is about to get flooded with claims — the competition factor should spike preemptively.

## IRSB Monorepo: Resilience and Webhook Sink

Six commits spanning v0.2.0 to v0.3.0.

The resilience work adds circuit breakers and retry policies to the external service calls. When the blockchain RPC provider is slow or down, the circuit breaker trips after three consecutive failures and returns cached data for 30 seconds before trying again. The retry policy uses exponential backoff with jitter — base delay 100ms, max delay 5s, jitter factor 0.3. The jitter prevents thundering herd problems when the circuit breaker resets and all pending requests retry simultaneously.

The webhook sink is a development tool — a local HTTP server that captures webhook payloads and displays them in a terminal UI. When you're testing the bounty settlement flow, you need to see what payloads the event system is sending. The sink captures them, pretty-prints the JSON, shows timing between events, and highlights payload differences between consecutive webhooks. It replaces the previous approach of tailing log files and grepping for webhook entries.

## IntentVision: Terraform Drift and Secret Manager

Six commits. Terraform drift detection catches when manual changes have been made to infrastructure that should be managed declaratively. The drift detector runs `terraform plan` on a schedule and opens a GitHub issue when it finds resources that don't match the Terraform state. The issue includes the full plan output so you can see exactly what drifted and who needs to either update the Terraform config or revert the manual change.

Secret Manager integration replaces hardcoded API keys and database credentials with references to GCP Secret Manager. The application reads secrets at startup, with a fallback to environment variables for local development. This means `docker-compose up` still works without GCP credentials — the env vars take precedence over Secret Manager lookups when both exist.

## intent-mail: Gmail Push Notifications and Sync Daemon

Five commits. Gmail push notifications use Google's Pub/Sub API to receive real-time notifications when new emails arrive, instead of polling the IMAP server every 60 seconds. The latency improvement is significant — from up to 60 seconds for new email detection to under 2 seconds.

The sync daemon maintains the Pub/Sub subscription, renews the Gmail watch registration (which expires every 7 days), and processes incoming notifications. When a push notification arrives, it fetches the new message headers (not the full body until requested), indexes them by sender, subject, and timestamp, and makes them available to the intent-mail search and rules engine.

The daemon uses SQLite for the local index — fast, single-file, no server process needed. A full re-index of 10,000 messages takes about 4 seconds. Incremental updates from push notifications take under 100ms.

Fifty-five commits. The git-with-intent spec suite is the largest deliverable by document count. The bounties EV scoring is the most algorithmically interesting. The IRSB resilience work is the most operationally important. The intent-mail sync daemon will save the most time daily. A wide day, not a deep one.

---

## Related Posts

- [Bounty Scoring Algorithm and GWI Compliance Reports](/posts/bounty-scoring-algorithm-gwi-compliance-reports/) — Earlier bounty scoring work and the compliance reports that git-with-intent generates
- [Intent Mail: Full Platform Build with Gmail, Outlook, and a Rules Engine](/posts/intent-mail-full-platform-gmail-outlook-rules-engine/) — The intent-mail platform before push notifications
- [IRSB Security Audit Fixes, git-with-intent v0.6.0, and GitHub Profile Overhaul](/posts/irsb-security-audit-fixes-gwi-v060-github-profile-overhaul/) — The IRSB security hardening that preceded resilience work
