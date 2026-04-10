+++
title = 'Nixtla Repo: Zero to v0.2.0 with a Working Search-to-Slack Plugin'
slug = 'nixtla-repo-init-through-v020-search-slack-plugin'
date = 2025-11-23T10:00:00-06:00
draft = false
tags = ["nixtla", "claude-code-plugins", "slack", "search", "gemini", "groq", "ci-cd", "github-pages"]
categories = ["Development Journey"]
description = "Initializing the Nixtla Claude Code plugins repo from scratch to v0.2.0: full CI/CD, a working search-to-Slack pipeline with free provider options, and marketplace structure."
+++

New repo. Empty directory. By end of day: v0.2.0 tagged, a working plugin shipping, and a GitHub Pages site live.

## Repository Initialization

The Nixtla Claude Code plugins workspace needed proper infrastructure from commit one. Not a README and a prayer -- actual CI/CD, documentation filing, and GitHub Actions workflows.

First commit: project scaffolding with GitHub Actions for CI, automated doc filing using the standard 000-docs numbering scheme, and a base configuration for the plugin workspace. GitHub Pages site deployed from the repo's docs output.

This is a pattern I've repeated enough times that the muscle memory is automatic. New repo gets CI on the first commit, not the tenth. Every commit after that runs through the pipeline. No "we'll add tests later" debt.

## v0.1.0: Three Plugin Concepts

The first release documented three plugin concepts for the Nixtla ecosystem:

1. **nixtla-search-to-slack** -- search the web and GitHub, summarize with AI, publish to Slack channels
2. **nixtla-baseline-lab** -- run statistical forecasting baselines using Nixtla's open-source libraries
3. **nixtla-data-connector** -- bridge between Nixtla's time series tools and common data sources

All three were documented with architecture diagrams, API contracts, and dependency lists. No code yet. The release was a design checkpoint -- commit to the interfaces before writing the implementations.

## v0.2.0: Search-to-Slack MVP

The search-to-slack plugin went from concept to working code. Seven modules, 16,700 lines:

**Web search module.** Queries Brave Search, Google Custom Search, Bing, or DuckDuckGo. The provider is configurable -- all four have free tiers sufficient for development and light production use.

**GitHub search module.** Searches repositories, issues, code, and discussions using the GitHub API. Filters by language, stars, and activity recency.

**AI summary module.** Takes raw search results and produces structured summaries. Supports Gemini (Google's free tier) and Groq (free tier with generous rate limits) as LLM providers. The summary prompt is tuned for technical content -- it extracts key findings, identifies consensus vs. disagreement across sources, and flags recency of information.

**Slack publisher module.** Formats summaries as Slack Block Kit messages and posts to configured channels. Handles rate limiting, retry logic, and message threading for follow-up queries.

**Configuration module.** YAML-based config for provider selection, API keys, Slack channels, and search parameters. Validates on startup with clear error messages for missing or invalid configuration.

**CLI module.** Command-line interface for running searches, previewing Slack messages without sending, and testing individual pipeline stages in isolation.

**Plugin manifest module.** Standard `plugin.json` with metadata, dependencies, permissions, and Claude Code integration hooks.

## Free Provider Stack

The entire plugin runs at $0/month for development:

| Component | Provider | Free Tier |
|-----------|----------|-----------|
| Web search | Brave Search API | 2,000 queries/month |
| LLM summaries | Gemini 1.5 Flash | 1,500 requests/day |
| LLM fallback | Groq | 14,400 requests/day |
| Code search | GitHub API | 5,000 requests/hour |
| Publishing | Slack API | Unlimited for installed apps |

For production at scale, swap Brave for Google Custom Search ($5/1000 queries) and Gemini Flash for Gemini Pro. The provider abstraction makes this a config change, not a code change.

## Marketplace Structure

The plugin follows the marketplace validation spec: `plugin.json` with required fields, a validation script that checks schema compliance, and three Claude Skills that register the plugin's capabilities with Claude Code.

The validation script runs in CI. Every PR against the plugin gets schema-checked before merge. This catches breaking changes to the plugin manifest before they reach users.

## Baseline Lab Scaffold

Also scaffolded the Baseline Lab plugin structure -- directory layout, dependency list, and a stub MCP server configuration. No implementation yet. That's tomorrow's work.

## PipelinePilot Maintenance

Two minor commits on PipelinePilot: dependency bumps and a typo fix in the deployment docs. Nothing worth discussing. Maintenance happens.

---

**Related Posts:**

- [Claude Code Plugin Marketplace Launch](/posts/claude-code-plugin-marketplace-launch/) -- The marketplace these plugins publish to
- [Marketplace CI Hardening, Sync Guard, and Plugin Scaffold](/posts/marketplace-ci-hardening-sync-guard-plugin-scaffold/) -- CI/CD governance patterns reused in this repo
- [PipelinePilot: Building a Multi-Agent SDR Orchestrator on Vertex AI](/posts/pipelinepilot-multi-agent-sdr-orchestrator-vertex-ai/) -- The project that got the minor maintenance commits today
