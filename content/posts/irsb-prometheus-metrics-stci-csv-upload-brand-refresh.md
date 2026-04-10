+++
title = 'IRSB Prometheus Metrics, STCI CSV Upload, and Brand Refresh'
slug = 'irsb-prometheus-metrics-stci-csv-upload-brand-refresh'
date = 2026-02-02T10:00:00-06:00
draft = false
tags = ["irsb", "prometheus", "stci", "git-with-intent", "jeremylongshore", "github-profile", "observability"]
categories = ["Development Journey"]
description = "IRSB monorepo completes Epic 1 with a shared Prometheus metrics package. STCI drops API keys for CSV upload. git-with-intent consolidates its logger. GitHub profile and jeremylongshore.com get cleanups."
+++

Five repos touched, none of them deeply. February 2nd was a polish day — finishing things started earlier in the week and cleaning up loose ends across the portfolio. Sixteen commits total, none individually dramatic but collectively moving four projects forward.

## IRSB Monorepo: Epic 1 Complete

Five commits closing out Epic 1. The headline is a shared Prometheus metrics package extracted from the monorepo's services.

Each IRSB service was instrumenting its own metrics with slightly different label names, histogram buckets, and counter naming conventions. The inconsistencies were small but compounding:

- The gateway used labels `{method, path, status}` for `http_requests_total`
- The solver service used `{http_method, route, status_code}` for the same counter
- Histogram buckets ranged from the gateway's conservative set (100ms, 500ms, 1s, 5s) to the solver's aggressive set (1ms, 5ms, 10ms, 50ms, 100ms, 500ms, 1s)

Grafana dashboards had to account for both naming schemes, with query aliases mapping one to the other. Every new dashboard panel required checking which naming convention the target service used.

The shared package standardizes everything. One import, consistent labels, preconfigured histogram buckets for HTTP latency (5ms, 10ms, 25ms, 50ms, 100ms, 250ms, 500ms, 1s, 2.5s, 5s). Each service calls `metrics.NewHTTPHandler()` and gets a middleware that instruments all the standard HTTP metrics automatically.

Custom metrics still use service-specific names, but the base instrumentation is identical everywhere. The Grafana dashboards can now use one query template across all services instead of per-service overrides.

The package also standardizes the `/metrics` endpoint configuration — port 9090 on all services, path `/metrics`, no authentication (the metrics port is only accessible within the VPC). Before this, the gateway exposed metrics on 8081 and the solver on 3001. Prometheus scrape configs had per-service port overrides. Now it's one config for all services.

Epic 1 completion means the IRSB monorepo has its foundational infrastructure: CI pipeline, shared packages, deployment configuration, and now observability. The Epic 1 checklist had 14 items. The last three to close were the metrics package, a shared error handling module, and updating the CLAUDE.md to reflect the new package structure.

Epics 2 and onward are feature work. The difference between building on a solid foundation versus building without one shows up in velocity. Every future service starts with shared metrics, shared error handling, and shared config — 10 minutes of imports instead of a day of setup. The upfront cost of Epic 1 pays for itself starting with the second service.

## STCI: CSV Upload Replaces API Keys

Three commits on STCI. The big one: replacing the API key integration with direct CSV upload.

STCI (Solana Token Cost Index) originally pulled token price data from a third-party API. The API required keys, had rate limits, and cost money above the free tier. For a side project tracking Solana token costs, that's unnecessary overhead. Every month the API key rotated, the cron job broke silently, and the dashboard showed stale data until someone noticed.

The replacement is simple. Download the CSV export from the data provider (free, no auth required), upload it through the STCI dashboard, and the parser handles the rest. The parser validates column headers, handles both comma and tab delimiters, and rejects files with fewer than 7 days of data (not enough for meaningful trend calculation).

No API keys to manage, no rate limit errors at 3am, no monthly bill.

The tradeoff is obvious: automated real-time data becomes manual periodic uploads. For STCI's use case — weekly cost index calculations — that's fine. The data doesn't need to be real-time. It needs to be correct. And the CSV export from the data provider is more reliable than the API endpoint, which occasionally returned stale cached data that the API team took days to fix.

The other two STCI commits were unrelated to the CSV migration:

A mobile responsive fix for the dashboard tables — horizontal scroll with a visible scrollbar indicator instead of hiding columns on small screens. The previous approach hid the last two columns on mobile, which happened to be the trend indicators. Users on phones saw the data but couldn't see whether costs were going up or down.

A Gemini code review integration for the PR workflow. The Gemini integration runs on every PR and posts inline comments. It catches obvious issues — unused imports, missing error handling, inconsistent naming — that shouldn't wait for human review.

## git-with-intent: Logger Consolidation

Two commits. The codebase had three different logging approaches: `console.log` in early modules written during the prototype phase, Winston in the API layer added when structured logging became necessary, and Pino in the agent framework because it was the fastest option for high-throughput log streams.

Logger consolidation picked Pino for three reasons: it's the fastest Node.js logger in benchmarks, it outputs structured JSON by default (which Cloud Logging ingests natively), and it has built-in serializers for HTTP requests and errors that redact sensitive fields.

The migration touched 34 files. Most replacements were mechanical — swap the import, update the log level calls. The `console.log` replacements required adding log levels where none existed. Everything that was `console.log` became `logger.info` or `logger.debug` depending on whether it was operational output or debugging noise. The Winston removal also dropped two transitive dependencies from the bundle.

The second commit documented the MCP Server architecture — how git-with-intent exposes its analysis capabilities as an MCP (Model Context Protocol) server that Claude Code and other AI tools can consume directly. The documentation covers the available tools (commit analysis, intent classification, pattern detection), expected input schemas, and the authentication flow for remote MCP connections.

The MCP documentation is forward-looking. Most git-with-intent users interact through the CLI. But the MCP server allows AI assistants to call git-with-intent's analysis programmatically — ask "what changed in the last week?" and get structured data back, not terminal output. The docs ensure that someone integrating the MCP server doesn't have to read the source code to understand the tool surface.

## GitHub Profile and jeremylongshore.com

Cleanup commits across both. The GitHub profile README got updated project counts (22 active repos, up from 18 last month) and refreshed descriptions for the three flagship projects. jeremylongshore.com got minor copy adjustments following yesterday's brand repositioning — tightening the case study summaries, fixing a broken project link that pointed to an old repo name, and updating the footer copyright year.

These are the kinds of commits that don't warrant their own section but add up. A portfolio with outdated project counts and broken links undermines the repositioning work from yesterday. The profile README changes were 4 lines. The jeremylongshore.com fixes were 3 commits touching 5 files. Small, but each one prevents a credibility gap when someone actually clicks through from the newly repositioned about page to the GitHub profile.

Five repos in a day, none of them getting more than five commits. That's the rhythm of a polish day — breadth over depth, finishing over starting.

The IRSB metrics package and the STCI CSV migration are the two changes with lasting impact. The metrics package eliminates a class of consistency bugs across every future IRSB service. The CSV migration eliminates a recurring operational failure. The rest is maintenance that keeps the portfolio coherent — necessary work that doesn't make for exciting commit messages but prevents entropy from accumulating.

---

## Related Posts

- [IRSB Security Audit Fixes, git-with-intent v0.6.0, and GitHub Profile Overhaul](/posts/irsb-security-audit-fixes-gwi-v060-github-profile-overhaul/) — The IRSB security work that preceded Epic 1 completion
- [STCI: Zero to v0.1.0 Token Cost Index](/posts/stci-zero-to-v010-token-cost-index/) — STCI's initial build, before the CSV migration
- [git-with-intent v0.9 to v0.10: Docker Upgrades, README Rewrites, and Strategic Research](/posts/git-with-intent-v090-v0100-docker-upgrades/) — Where git-with-intent's architecture landed later
