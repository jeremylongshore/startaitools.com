+++
title = 'Nixtla Baseline Lab: Phases 4 Through 8 in a Single Day'
slug = 'nixtla-baseline-lab-phases-four-through-eight'
date = 2025-11-25T10:00:00-06:00
draft = false
tags = ["python", "ci-cd", "testing", "data-engineering", "visualization"]
categories = ["Development Journey"]
description = "Five phases of the Nixtla Baseline Lab shipped in one day — setup automation, CI with golden task harness, PNG visualization, CSV support, and a TimeGPT showdown mode."
+++

34 commits. Five phases. One day. The Nixtla Baseline Lab went from a test bed to a real product between breakfast and dinner.

## Phase 4: Testing and Skills Wiring

Phase 4 was plumbing. Test coverage for the existing baseline functions, skills wiring to expose them through the dev marketplace, and a marketplace entry so other tools could discover and invoke the lab. Nothing flashy. The kind of work that makes everything after it possible.

The dev marketplace integration meant writing a `marketplace.json` entry with the correct schema — skill name, description, invocation pattern, required parameters. This is the contract other tools use to call the Baseline Lab programmatically. Get the schema wrong and the marketplace silently ignores you.

Tests covered the core forecasting functions: model initialization, data preprocessing, forecast generation, and error metric calculation. Each test pinned expected output against the M4 Monthly reference data. If AutoETS changes its default hyperparameters in a future statsforecast release, these tests catch it before the change hits production.

## Phase 5: Automated Setup

`setup_nixtla_env.sh` — a single shell script that builds the entire environment from scratch. Python virtualenv, pip dependencies, statsforecast installation, validation smoke test.

The `/nixtla-baseline-setup` slash command wraps the script so you can run it from within Claude Code without dropping to a terminal. One command, working environment.

Validated on Ubuntu 22.04 with Python 3.12. AutoETS hit 0.77% sMAPE on the M4 Monthly dataset. That number became the acceptance threshold for everything that followed.

The validation step in the setup script is important. It doesn't just check that imports work. It runs a real forecast on a known dataset and compares the output to a pinned result. If the library installed correctly but the underlying BLAS configuration is wrong, the numbers drift. The validation catches that before you spend an hour debugging a "model regression" that's actually a numpy build issue.

## Phase 6: CI and the Golden Task Harness

This is the phase that matters most.

`run_baseline_m4_smoke.py` is a golden task harness — a reproducibility test that runs AutoETS against a known dataset slice and validates five things:

1. The forecast completes without error
2. The output shape matches expectations
3. sMAPE is below the acceptance threshold
4. No NaN values in the forecast
5. The entire run finishes within 120 seconds

Five checks. 120-second timeout. If any fail, CI fails. The GitHub Actions workflow runs this on every push.

The golden task pattern is stolen from compiler testing. You have a known input, a known acceptable output range, and a time budget. The forecast itself is the "compilation." If the compiler produces valid output in time, the code is good. If not, something regressed.

`marketplace.json` bumped to v0.4.0 with the CI integration metadata.

## Phase 7: Visualization and CSV

matplotlib-generated PNG charts for every forecast run. The chart shows historical data in blue, forecast horizon in red, and confidence intervals as a shaded band. Not pretty. Functional.

CSV support landed alongside. `example_timeseries.csv` ships with the repo as a reference dataset. argparse parametrization means you can point the forecaster at any CSV with a date column and a value column.

v0.5.0. The lab now reads arbitrary data, forecasts it, and produces both a CSV output and a PNG visualization. That's a usable tool, not just a test harness.

The argparse interface accepts `--horizon`, `--season-length`, and `--model` flags. Default horizon is 12 periods. Default season length auto-detects from the data frequency. Default model is AutoETS but you can swap in AutoTheta, AutoARIMA, or any other statsforecast model. The CLI is the demo interface — when someone asks "what does this tool do?", you hand them a CSV and a one-liner command.

## Phase 8: The TimeGPT Showdown

This is where it gets interesting.

`timegpt_client.py` wraps Nixtla's TimeGPT API — the foundation model that the Baseline Lab exists to benchmark against. The MCP server gained an `include_timegpt` flag that, when set, runs both AutoETS and TimeGPT on the same data and produces a side-by-side comparison.

The showdown mode is CI-safe. If the TimeGPT API key isn't present, the test gracefully skips the comparison and runs AutoETS only. No failed builds because someone forgot to set a secret. No conditional workflow files. Just a runtime check.

v0.6.0. 22 test cases across 6 categories: unit tests for the forecaster, integration tests for the CLI, golden task tests for CI, visualization tests for PNG output, CSV round-trip tests, and TimeGPT client tests (mocked when no API key is available).

## The Day's Shape

Five phases sounds ambitious. It wasn't. Each phase was a natural extension of the previous one. Phase 4 gave us tests. Phase 5 gave us setup. Phase 6 gave us CI. Phase 7 gave us output formats. Phase 8 gave us the comparison mode that justifies the project's existence.

The golden task harness is the piece I'll reuse. Forecast accuracy testing has the same structure as compiler testing: known input, bounded output, time budget. That pattern works for any deterministic-enough system.

---

### Related Posts

- [Golden Tests, Fuzz Testing, and the DXF Revision Corpus](/posts/golden-tests-fuzz-testing-dxf-revision-corpus/) — the same golden test pattern applied to CAD file parsing
- [Building Production CI/CD: Documentation to Deployment](/posts/building-production-ci-cd-documentation-to-deployment/) — CI pipeline patterns used across multiple projects
- [Python Class Identity Mismatch: A CI Debugging Guide](/posts/python-class-identity-mismatch-ci-debugging-guide/) — Python CI edge cases that bite you in automation
