+++
title = 'Skills Infrastructure from Scratch: 8 SKILL.md Files, an Installer, and a Compliance Framework'
slug = 'nixtla-skills-pack-phase-zero-compliance'
date = 2025-12-01T10:00:00-06:00
draft = false
tags = ["nixtla", "claude-code-plugins", "skills", "compliance", "architecture"]
categories = ["Development Journey"]
description = "Building the entire skills infrastructure for the Nixtla workspace from zero: 8 skill definitions, an installer package, demo project, compliance audits, and strategy documentation."
+++

53 files. 13,445 lines. One goal: give the Nixtla workspace a skills layer that doesn't exist yet.

## What Needed Building

The Nixtla workspace had plugins. It had documentation. It had release discipline. What it didn't have was a way for external tools to discover and invoke its capabilities through a standardized interface.

Skills are that interface. A SKILL.md file declares what a skill does, what inputs it needs, what outputs it produces, and what permissions it requires. An installer package reads those declarations and wires them into Claude Code. A demo project proves the whole chain works end-to-end.

None of this existed before today.

## 8 SKILL.md Files

Each skill covers one capability in the Nixtla forecasting ecosystem:

1. **Baseline Forecast** -- run StatsForecast models against time series data
2. **BigQuery Ingest** -- pull data from BigQuery into the forecasting pipeline
3. **Data Validation** -- check time series for gaps, outliers, and format issues
4. **Model Comparison** -- benchmark multiple models against each other
5. **Forecast Export** -- push results to Slack, BigQuery, or flat files
6. **TimeGPT Evaluation** -- compare Nixtla's TimeGPT against statistical baselines
7. **Anomaly Detection** -- flag unusual patterns in time series data
8. **Pipeline Orchestration** -- chain multiple skills into end-to-end workflows

Every file follows the same structure: purpose, inputs schema, outputs schema, prerequisites, usage examples. The structure matters more than any individual skill because it's the contract that every future skill will follow.

## The Installer Package

Two components: a CLI tool and a core library.

The CLI handles `install`, `uninstall`, `list`, and `validate` commands. It reads SKILL.md files, parses the metadata, and registers skills with Claude Code's skill registry. Uninstall is clean -- removes the registration without touching the underlying plugin code.

The core library handles parsing, validation, and registration logic. Separated from the CLI so other tools can programmatically manage skills without shelling out to the command line.

## Demo Project with Sample Data

A self-contained demo that installs two skills (Baseline Forecast and Data Validation), runs them against included sample time series data, and verifies the outputs match expected results.

The sample data is synthetic but realistic -- daily retail sales with trend, seasonality, and a few injected anomalies. Small enough to run in seconds, complex enough to exercise the full skill interface.

## Compliance Audits

Every SKILL.md ran through a compliance checker that validates:

- Required sections present and non-empty
- Input/output schemas parseable as valid JSON Schema
- Prerequisites list doesn't reference nonexistent packages
- Usage examples are syntactically valid
- Permissions declarations match what the underlying plugin actually needs

All 8 skills passed. The compliance checker itself became a reusable script for future skill additions.

## Strategy Documentation

The last piece: a rollout strategy document covering phases 0 through 3. Phase 0 (today) is infrastructure. Phase 1 is internal testing with real Nixtla data. Phase 2 is external beta with selected users. Phase 3 is marketplace publication.

Each phase has entry criteria, exit criteria, and a definition of done. The strategy doc exists so Phase 1 doesn't start until Phase 0 is actually finished -- not "mostly finished" or "finished except for that one thing."

## The Shape of the Day

This was pure linear execution. No debugging crises. No architectural pivots. The requirements were clear, the patterns were established from other projects, and the work was laying track. Thirteen thousand lines sounds like a lot until you realize most of it is structured metadata and schema definitions.

The interesting part wasn't any individual file. It was the decision to build all the infrastructure before writing a single line of skill implementation. The installer, the compliance checker, the demo project -- all of that exists to make Phase 1 implementation go faster, not to ship features today.

---

**Related Posts:**

- [Three Releases in One Day: Nixtla Goes Enterprise](/posts/nixtla-enterprise-docs-restructure-v100-release/) -- the enterprise documentation standard this skills layer builds on
- [Nixtla Baseline Lab: Phases 4 Through 8 in a Single Day](/posts/nixtla-baseline-lab-phases-four-through-eight/) -- the Baseline Lab plugin that the Baseline Forecast skill wraps
- [Ninety Skills, Three Packs, One Day](/posts/ninety-skills-three-packs-one-day/) -- skills infrastructure patterns at larger scale
