+++
title = 'Nixtla Baseline Lab: Real statsforecast Baselines via MCP Server'
slug = 'nixtla-baseline-lab-real-statsforecast-mcp-server'
date = 2025-11-24T10:00:00-06:00
draft = false
tags = ["nixtla", "mcp", "statsforecast", "time-series", "forecasting", "vertex-ai", "claude-code-plugins"]
categories = ["Development Journey"]
description = "The Nixtla Baseline Lab gets a working MCP server running SeasonalNaive, AutoETS, and AutoTheta baselines on M4 data with sMAPE and MASE evaluation metrics."
+++

Yesterday was plugin scaffolding. Today the Baseline Lab gets real models running real data through a real MCP server.

## Phase 2: Plugin Manifest and MCP Config

The Baseline Lab plugin needed two pieces of infrastructure before any forecasting code could run.

**Plugin manifest.** Standard `plugin.json` declaring the plugin's name, version, dependencies, and MCP server configuration. The MCP config tells Claude Code how to start the server, what tools it exposes, and what permissions it needs (filesystem read for data files, network for optional Nixtla cloud API calls).

**MCP server configuration.** The server exposes three tools: `run_baseline`, `compare_models`, and `get_metrics`. Each tool has a typed input schema and returns structured JSON. Claude Code discovers these tools at startup and can call them directly during conversations.

## Phase 3: Real Baselines

The toy data and stub implementations from the scaffold got replaced with actual Nixtla open-source libraries.

**Data source: datasetsforecast M4.** The M4 competition dataset is the standard benchmark for time series forecasting. The `datasetsforecast` package provides it as a single function call -- no manual download, no CSV parsing, no schema guessing. 100,000 time series across yearly, quarterly, monthly, weekly, daily, and hourly frequencies.

**Models: statsforecast.**

Three baseline models, all from Nixtla's `statsforecast` library:

- **SeasonalNaive** -- repeats the last observed seasonal pattern. The absolute floor for any forecasting system. If your model can't beat SeasonalNaive, your model is broken.
- **AutoETS** -- exponential smoothing with automatic model selection. Picks the best ETS variant (additive/multiplicative, with/without trend, with/without seasonality) based on information criteria.
- **AutoTheta** -- automatic Theta method selection. Decomposes the series and optimizes the theta parameter. Robust to outliers and level shifts.

These aren't toy implementations. `statsforecast` is Nixtla's production-grade library, optimized in Cython, capable of fitting thousands of series per second on a single core.

**Evaluation metrics: sMAPE and MASE.**

- **sMAPE** (Symmetric Mean Absolute Percentage Error) -- scale-independent, bounded between 0% and 200%. The standard M4 competition metric.
- **MASE** (Mean Absolute Scaled Error) -- compares forecast error to naive forecast error. MASE > 1 means the model is worse than naive. MASE < 1 means it adds value.

Both metrics computed per-series and aggregated. The MCP server returns individual series metrics and summary statistics (mean, median, P90) across the evaluation set.

## The MCP Server

300+ lines of Python. The server handles:

- Dataset loading and caching (M4 data loads once, stays in memory)
- Model fitting with configurable forecast horizons
- Cross-validation with expanding windows
- Metric computation and formatting
- Error handling for degenerate series (constant values, too-short histories)

A typical interaction through Claude Code:

```
User: Run baselines on M4 monthly data with a 12-step horizon

Claude: [calls run_baseline tool]

Results:
  SeasonalNaive  - sMAPE: 13.2%, MASE: 1.00 (by definition)
  AutoETS        - sMAPE: 11.8%, MASE: 0.87
  AutoTheta      - sMAPE: 11.5%, MASE: 0.84
```

The baseline results establish the floor. Any ML model, neural forecaster, or foundation model that claims to forecast M4 monthly data needs to beat sMAPE 11.5% or it's not adding value over a classical method that fits in milliseconds.

## CTO Audit Cleanup

Separate from the Baseline Lab work: a documentation cleanup pass across the Nixtla repo. Deleted duplicate doc files that had accumulated during rapid development, renumbered the remaining docs from 001 through 015 in the standard sequential scheme.

Also repositioned the repo README. The original README described a generic Claude Code plugin workspace. Rewrote it to position Nixtla as "Bob for Nixtla" -- an agentic workspace where Claude Code acts as a Nixtla power user, running baselines, comparing models, and generating reports through MCP tools rather than manual Python scripts.

## Vertex AI Agent Engine Foundation

Added the initial configuration for a Vertex AI Agent Engine deployment target. No agents deployed yet -- just the project setup, service account permissions, and deployment configuration. The plan: wrap the MCP server's forecasting capabilities in an ADK agent that can be deployed to Agent Engine for always-on availability outside of Claude Code sessions.

---

**Related Posts:**

- [Nixtla Repo: Zero to v0.2.0 with a Working Search-to-Slack Plugin](/posts/nixtla-repo-init-through-v020-search-slack-plugin/) -- Yesterday's repo initialization that set up the infrastructure this plugin builds on
- [PipelinePilot: Building a Multi-Agent SDR Orchestrator on Vertex AI](/posts/pipelinepilot-multi-agent-sdr-orchestrator-vertex-ai/) -- The Vertex AI Agent Engine deployment patterns this project will reuse
- [Claude Code Plugin Marketplace Launch](/posts/claude-code-plugin-marketplace-launch/) -- The marketplace ecosystem these plugins target
