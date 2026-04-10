+++
title = 'Global Skill Schema and a Prediction Markets Vertical'
slug = 'nixtla-global-skill-schema-prediction-markets-vertical'
date = 2025-12-05T10:00:00-06:00
draft = false
tags = ["nixtla", "skills", "schema", "prediction-markets", "polymarket", "ci-cd", "architecture"]
categories = ["Development Journey"]
description = "Defining the Global Standard Skill Schema, a HOW-TO guide for perfect skills, ARD/PRD templates, a Polymarket Analyst skill, CI workflow, and a demo forecasting project. 106 files, 11,951 lines."
+++

106 files. 11,951 lines. The day split into two halves: standardizing how skills get built, then proving the standard works by building a new vertical from it. Standards that exist without implementations are aspirational. Standards that ship with a working example are real.

## Global Standard Skill Schema

The 8 skills from Dec 1 followed a structure. But that structure lived in tribal knowledge and copy-paste. Today it became a formal specification.

The Global Standard Skill Schema defines every field a SKILL.md can contain, which fields are required vs. optional, the validation rules for each field, and the versioning contract (how the schema itself evolves without breaking existing skills).

Key decisions:

- **Inputs and outputs use JSON Schema draft 2020-12.** Not a custom format. Not a subset. The full spec, so any JSON Schema validator works.
- **Permissions are declarative, not prescriptive.** A skill declares "I need read access to BigQuery" -- not "I need the `bigquery.tables.getData` IAM role." The installer maps declarations to specific permissions for each platform.
- **Version field is semver.** Breaking changes to a skill's interface require a major version bump. This is enforced by CI, not honor system.

## HOW-TO-MAKE-A-PERFECT-SKILL

A 400-line guide that walks through building a skill from blank file to 100% compliance. Not a reference doc -- a tutorial with a running example.

The example skill is a weather data fetcher. Simple enough to follow, complex enough to exercise every schema field. The guide walks through each section of the SKILL.md, explains why the field exists, shows the correct format, and lists the common mistakes the compliance checker will catch.

The guide ends with a "common pitfalls" section drawn directly from the Dec 4 compliance remediation. Every mistake that showed up across all 8 skills is documented with the wrong way, the right way, and the reason the checker flags it. Learning from someone else's mistakes is faster than making your own.

This exists because the Dec 4 compliance push showed that poorly scaffolded skills create remediation work. Better to teach the standard upfront than fix violations after the fact.

## ARD/PRD Templates

Two document templates: Architecture Requirements Document and Product Requirements Document. Both follow the Nixtla conventions but are generic enough to reuse across any plugin or skill.

The ARD template covers: system context, component boundaries, data flow, infrastructure requirements, security model, and scaling considerations. The PRD template covers: problem statement, personas, requirements (functional/non-functional), acceptance criteria, and success metrics.

These templates existed informally in people's heads and previous documents. Now they're versioned files with placeholder guidance, examples, and validation rules. New verticals start from the templates instead of from memory. The difference matters when the third person tries to write a PRD and the first two people aren't available to answer questions.

## Polymarket Analyst Skill

The prediction markets vertical. Polymarket is a prediction market platform where users trade on the outcomes of real-world events. The Polymarket Analyst skill applies Nixtla's time series forecasting to market data -- specifically, predicting price movements and identifying mispriced contracts.

The skill pulls data from Polymarket's public API, runs statistical models against historical price series, and outputs forecasts with confidence intervals. The interesting part is the data shape: prediction market prices are bounded (0-100), mean-reverting near expiry, and subject to information shocks that break stationarity assumptions.

StatsForecast handles bounded data and regime changes reasonably well, but the default model selection heuristics don't account for the near-expiry compression pattern. The skill includes a custom preprocessing step that segments the time series by time-to-expiry and selects models accordingly.

## CI Workflow

A GitHub Actions workflow that runs on every push and PR:

1. Validates all SKILL.md files against the Global Standard Skill Schema
2. Runs the demo forecasting project end-to-end
3. Checks that new files follow naming conventions
4. Verifies that version bumps are consistent across affected files

The workflow uses the compliance checker from Dec 1 but wraps it in CI-native reporting -- annotations on PR diffs showing exactly which lines fail validation.

## Demo Forecasting Project

A standalone project that installs the Polymarket Analyst skill and runs it against included sample data. The sample data is real (anonymized) Polymarket price history for 5 resolved markets, so the forecasts can be scored against actual outcomes.

The demo produces a report comparing forecast accuracy across models, with a final recommendation for which model configuration to use in production. It's both a demonstration and a benchmark.

## Baseline Lab Archive

Archived the baseline-lab plugin scaffold. The functionality it was meant to provide has been absorbed into the skills framework. Rather than maintain two parallel implementations, the scaffold got moved to `archived/` with a note pointing to its replacement.

Archiving instead of deleting preserves the git history and makes it possible to reference the original design decisions if questions come up later. Delete is permanent. Archive is reversible. When you're not sure which one to pick, archive wins.

---

**Related Posts:**

- [Skills Infrastructure from Scratch: 8 SKILL.md Files, an Installer, and a Compliance Framework](/posts/nixtla-skills-pack-phase-zero-compliance/) -- the infrastructure this schema standardizes
- [v1.2.0: Every Skill to 100% Compliance](/posts/nixtla-v120-skills-hundred-percent-compliance/) -- the compliance push that revealed the need for better upfront guidance
- [Verified Plugins Program: Quality Signal for the Marketplace](/posts/verified-plugins-program-quality-signal-for-the-marketplace/) -- marketplace-level quality standards that align with this schema
