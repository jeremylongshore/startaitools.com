+++
title = 'BigQuery Integration, 23 Skills at L4 Quality: Nixtla v1.8.0'
slug = 'nixtla-bigquery-integration-23-skills-l4-quality'
date = 2025-12-10T10:00:00-06:00
draft = false
tags = ["python", "bigquery", "gcp", "claude-code-plugins", "testing", "architecture"]
categories = ["Development Journey"]
description = "3-plugin workflow integration with E2E testing, 23 skills at 100% L4 quality, Anthropic API swap, SerpAPI removal, and doc archival — Nixtla reaches production parity."
+++

26 commits. The day the three plugins stopped being independent projects and started being a pipeline.

Four days of infrastructure, quality enforcement, and security hardening led to this: the moment where separate components become a system. v1.8.0 isn't the biggest release by commit count. It's the most important by what it proves — three independently developed plugins can compose into a reliable workflow with tested failure handling.

## 3-Plugin Workflow Integration

Each plugin had been built and tested in isolation. Search-to-slack finds information. Baseline Lab runs forecasts. BigQuery Forecaster queries production data. All three worked. None of them talked to each other.

The integration defines a workflow: BigQuery Forecaster queries raw data and produces a structured dataset. Baseline Lab consumes that dataset and generates forecasts with accuracy metrics. Search-to-slack takes the forecast results and posts a summary to a Slack channel. Input of one is the output of the previous.

The glue is a workflow manifest — a YAML file that declares the pipeline stages, maps outputs to inputs, and defines failure behavior. If BigQuery returns no data (empty query result), the pipeline stops and posts a "no data" message to Slack instead of feeding an empty dataset to the forecaster. If the forecast fails (statsforecast throws on pathological data), the pipeline posts the raw data summary without forecasts.

The failure modes were the hard part. Three plugins means three categories of failure, and the combinations multiply. BigQuery timeout + forecast success + Slack rate limit is a different recovery path than BigQuery success + forecast failure + Slack success. The workflow manifest handles 6 explicit failure combinations. Anything outside those 6 falls through to a generic error handler that dumps context to a log file and posts a terse error to Slack.

The quickstart for each plugin got rewritten to reflect the workflow context. Previously: "here's how to run the BigQuery Forecaster standalone." Now: "here's how to run it standalone, and here's how it fits into the 3-plugin pipeline." The standalone instructions stayed — plugins should still work independently — but the workflow section shows what upstream data looks like and what the downstream consumer expects.

## End-to-End Testing

Unit tests existed for each plugin. Integration tests for the workflow didn't. Writing them revealed three assumptions that were true in isolation and false in combination:

1. The BigQuery Forecaster returned timestamps as strings. The Baseline Lab expected datetime objects. A `pd.to_datetime()` call in the workflow glue fixed it.
2. The Baseline Lab output used column name `forecast_value`. Search-to-slack expected `predicted`. A rename in the output mapping.
3. The BigQuery Forecaster's error response was a dict with a `message` key. The workflow error handler expected an `error` key. Both conventions existed in the codebase because each plugin was written months apart.

Three bugs. All trivial. All invisible until the plugins ran in sequence. This is why integration tests exist — not to catch logic errors but to catch interface mismatches.

The E2E test runs the full pipeline against a small BigQuery dataset (1,000 rows, not 200 million) and validates that a Slack message appears in the test channel with the expected structure. The test takes 45 seconds — mostly waiting for BigQuery to process and Slack to acknowledge. It runs in Tier 3 CI only, not on every push. The cost of one E2E run is roughly equivalent to 20 unit test runs, so gating it behind the release tier keeps the cost optimization from yesterday intact.

## 23 Skills at 100% L4 Quality

L4 is the highest quality tier in the SKILL.md validation framework. L1 is "parseable frontmatter." L2 adds required fields and section structure. L3 adds parameter schemas and error handling. L4 adds everything from yesterday's validator: character limits, third-person descriptions, code block language tags, internal link validity, output constraints.

Two new skills brought the count from 21 to 23. Both were utility skills — one for workspace environment validation, one for plugin dependency checking. Small but necessary.

The remaining 21 skills from yesterday all held at L4 after the security hardening changes. The security work added new frontmatter fields (`requires_filesystem`, `requires_env_vars`) but the validator was updated in the same PR, so no skills regressed.

100% L4 across 23 skills. No waivers, no "L3 with a plan to reach L4." The validator runs in CI. If a skill drops below L4, the build fails.

Getting to 100% required a decision about the two new utility skills. They could have shipped at L3 — functional but without the full documentation suite — and been upgraded later. That's the pragmatic approach. But the validator was now in CI, and shipping L3 skills would mean either adding an exception or watching the build go red and ignoring it. Neither option was acceptable. The utility skills got full L4 treatment before merge. They took an extra hour each. That hour bought permanent CI green.

## Anthropic API Swap

Search-to-slack originally used OpenAI's API for search result summarization. The summarizer takes raw search results — HTML snippets, titles, URLs — and produces a readable Slack message. GPT-3.5-turbo was fast and cheap for this.

Swapped to Anthropic's Claude API. The motivation wasn't quality (both produce adequate summaries for Slack posts) — it was consistency. The rest of the Nixtla workspace is built around Claude Code. Having a single OpenAI dependency for one summarization call created a billing relationship, an API key, and a failure mode that nothing else in the system shared.

The swap was 14 lines of code. The prompt stayed the same. The response parsing changed because Anthropic's API returns content in a different structure. The Slack output is indistinguishable.

One unexpected benefit: Claude's response includes a `stop_reason` field that makes it easy to detect truncated output. The OpenAI integration had a silent truncation bug where long search result summaries got cut off without warning. The new integration checks `stop_reason == "end_turn"` and retries with a shorter input if the response was truncated. A quality improvement that came for free with the swap.

## SerpAPI Removal

Related to the API swap: SerpAPI was the search backend for search-to-slack. It worked but it cost money per query and the free tier was 100 queries/month. For a demo plugin, that's fine. For a plugin that might run in a workflow triggered by a cron job, 100 queries evaporates fast.

Replaced with direct Google Custom Search API calls. The free tier is 100 queries/day, not per month. The response format is different — SerpAPI normalizes across search engines while Custom Search returns Google's raw JSON — but the normalizer was already a separate function. Swapped the implementation, kept the interface.

The SerpAPI removal also eliminated an npm dependency. The SerpAPI Python client pulls in `serpapi`, which pulls in `google-search-results`, which has its own dependency tree. The Google Custom Search API is a single HTTP call to a REST endpoint — no client library needed, just `requests`. One fewer dependency, one fewer supply chain risk, one fewer thing to update when Dependabot files a PR.

## Doc Archival

Documents 001 through 096 moved to an `archive/` directory. These were design documents, meeting notes, early architecture proposals, and spec drafts from the first two months of the project. Useful as historical record, harmful as active documentation. Having 96 numbered docs in the same directory as current operational guides meant `ls` required scrolling and search required filtering.

The archive preserves numbering. Document 001 in the archive is still 001. New documents in the active directory start at 100. The gap between 096 and 100 is intentional — room for three more documents that might emerge from the archive review as still-relevant.

The archival process wasn't just `mv`. Each document got a 30-second read to confirm it was truly historical. Three documents that looked archival were actually still referenced by active skills. Those stayed in the active directory and got renumbered into the 100-series. The alternative — archiving them and watching skills break — would have been discovered by CI, but finding out from a build failure that you archived something still in use is a worse experience than spending an extra 10 minutes checking.

## Related Posts

- [Security Hardening and Docs Redesign: Nixtla v1.7.0](/posts/nixtla-security-hardening-docs-redesign-v170/)
- [Nixtla BigQuery Forecaster: Cloud Functions on 200 Million Rows](/posts/nixtla-bigquery-forecaster-cloud-functions-plugin/)
- [21 Skills and a Production Validator: Nixtla v1.6.0](/posts/nixtla-21-skills-production-validator-v160/)
