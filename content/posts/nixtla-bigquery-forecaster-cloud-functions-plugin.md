+++
title = 'Nixtla BigQuery Forecaster: Cloud Functions on 200 Million Rows'
slug = 'nixtla-bigquery-forecaster-cloud-functions-plugin'
date = 2025-11-29T10:00:00-06:00
draft = false
tags = ["python", "gcp", "bigquery", "data-engineering", "cloud-functions"]
categories = ["Development Journey"]
description = "Plugin #2 for the Nixtla workspace: a Cloud Function running AutoETS and AutoTheta on BigQuery public data — 200M+ Chicago taxi trip rows with keyless WIF deployment."
+++

Plugin #2. The Baseline Lab proved statsforecast works on curated datasets. The BigQuery Forecaster proves it works on real data at real scale.

## The Plugin

A Cloud Function (Python 3.12) that queries BigQuery public datasets, runs AutoETS and AutoTheta forecasts, and returns structured results. The target dataset: Chicago taxi trips — 200 million+ rows of timestamped ride data with fare amounts, trip durations, and pickup locations.

2,691 lines across 16 files. That's a complete plugin: source code, tests, deployment config, CI workflow, and documentation. The file count breaks down as: 4 Python source files, 3 test files, 2 deployment configs (Cloud Functions + GitHub Actions), 1 requirements file, and 6 documentation files including the README, architecture doc, and usage examples.

## Why BigQuery

The Baseline Lab runs on M4 competition data. Clean. Small. Pre-processed. That's fine for benchmarking but it doesn't answer the question a potential customer asks: "Does this work on my data?"

BigQuery public datasets are the closest thing to "your data" without actually touching proprietary information. The Chicago taxi dataset has every property that makes real-world forecasting hard: irregular time intervals, missing values, seasonal patterns at multiple frequencies (daily, weekly, annual), and enough volume that naive approaches fall over.

200 million rows also tests whether the statsforecast library handles BigQuery's data transfer patterns gracefully. Spoiler: it does, but you have to be careful about memory. The Cloud Function pulls aggregated data — daily fare totals, not individual trips — so the actual working set is manageable.

The aggregation query runs in BigQuery, not in Python. This matters. Pulling 200M raw rows into a Cloud Function would blow the memory limit instantly. The SQL aggregation reduces the dataset to ~2,500 daily data points before the data ever leaves BigQuery. The Cloud Function's job is forecasting, not data warehousing.

## Deployment Architecture

GitHub Actions deploys the Cloud Function using Workload Identity Federation. No service account keys stored in GitHub Secrets. No JSON key files checked into repos. WIF exchanges a GitHub OIDC token for short-lived GCP credentials at deploy time.

The CI workflow:

1. Authenticate via WIF
2. Run unit tests
3. Deploy to Cloud Functions (gen2)
4. Run a smoke test against the deployed function
5. Report results

The smoke test hits the live function with a small date range query. If the response includes a valid forecast array with the correct shape, the deploy succeeded. If not, the workflow fails and the previous version stays active.

## AutoETS vs. AutoTheta

Both models ship in the plugin. AutoETS (Exponential Smoothing) is the workhorse — fast, stable, good defaults. AutoTheta adds a decomposition step that handles multiple seasonal patterns better than ETS alone.

On the Chicago taxi data, AutoTheta edges out AutoETS on weekly aggregations where the day-of-week pattern is strong. AutoETS wins on monthly aggregations where the simpler trend-plus-season model is sufficient. The plugin runs both and returns results for each, letting the consumer pick.

No ensemble. No stacking. Just two models, two results, pick your favorite. Simplicity beats cleverness when the goal is demonstrating the library's capabilities to a potential customer.

The response format is a JSON object with forecast arrays for each model, metadata about the query (date range, aggregation level, BigQuery job ID), and timing information. The timing matters because Cloud Functions have a 540-second timeout. AutoETS runs in under 5 seconds on the aggregated data. AutoTheta takes 8-12 seconds. Plenty of headroom, but the timing data proves it.

## GitHub Profile Badges

Three commits to the GitHub profile repo the same day. Visual tech stack badges from skill-icons.dev replaced the text-based skill list. Stats card enhancements. Rank display fixes for the profile card.

Minor work. The kind of thing you do while waiting for a Cloud Function deployment to propagate. Cloud Functions gen2 deployments take 2-4 minutes. Enough time to push a badge update but not enough time to start anything meaningful.

## The Scorecard

| Component | Detail |
|-----------|--------|
| Plugin | BigQuery Forecaster (Plugin #2) |
| Runtime | Cloud Functions gen2, Python 3.12 |
| Data | Chicago taxi trips, 200M+ rows |
| Models | AutoETS, AutoTheta |
| Auth | WIF keyless deployment |
| Size | 2,691 lines, 16 files |

The Baseline Lab is a benchmark tool. The BigQuery Forecaster is a demo. Different purposes, same statsforecast foundation. Together they answer both questions a technical evaluator asks: "How accurate is it?" (Baseline Lab) and "Does it scale?" (BigQuery Forecaster).

Plugin #2 took one day to build because Plugin #1 established all the patterns. The directory structure, the test layout, the CI workflow, the README template — all of it carried over with minimal modification. The only new code was the BigQuery client and the Cloud Function entry point. Everything else was copy, adapt, verify. That's the payoff of building infrastructure before building features.

---

### Related Posts

- [Nixtla Baseline Lab: Phases 4 Through 8 in a Single Day](/posts/nixtla-baseline-lab-phases-four-through-eight/) — Plugin #1 and the golden task harness that benchmarks accuracy
- [Building a 254-Table BigQuery Schema in 72 Hours](/posts/building-254-table-bigquery-schema-72-hours/) — BigQuery at enterprise scale with a different dataset
- [Deploying Next.js 15 on Google Cloud Run with Custom Domain and SSL](/posts/deploying-nextjs-15-google-cloud-run-custom-domain-ssl/) — GCP deployment patterns with Cloud Run instead of Cloud Functions
