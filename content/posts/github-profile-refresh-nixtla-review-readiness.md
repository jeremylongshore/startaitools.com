+++
title = 'GitHub Profile Refresh and Nixtla Review Readiness'
slug = 'github-profile-refresh-nixtla-review-readiness'
date = 2025-11-26T10:00:00-06:00
draft = false
tags = ["devops", "documentation", "python", "data-engineering", "developer-experience"]
categories = ["Development Journey"]
description = "Professional GitHub README rewrite, Nixtla Baseline Lab v0.7.0 review kit with mobile checklist, and a Perception dashboard README restructure."
+++

Polish day. Three repos, zero new features, all preparation. The kind of day that doesn't feel productive until someone actually reads what you wrote.

The work was split across github-profile (3 commits), nixtla (8 commits), and perception (1 commit). Twelve commits total. Every single one touched a markdown file or a shell script. Not a single Python function was modified.

## GitHub Profile: 305 Lines Down to 135

The GitHub profile README had accumulated cruft. 305 lines of badges, project lists, and metrics that hadn't been verified in months. Half the stats were wrong. Two project links were dead.

The rewrite cut it to 135 lines. Every metric verified against actual repo data. The focus shifted to Vertex AI multi-agent work — the most technically interesting thing happening across the portfolio. Professional badge icons replaced the homebrew SVG badges that looked fine on desktop and terrible on mobile. Contribution graph stays. Pin section reorganized to show the four most active repos.

The profile is a landing page. It should communicate "what this person builds" in 10 seconds. 305 lines communicates "this person doesn't edit."

The hardest part was killing darlings. Four projects that took weeks of work got cut because they weren't the current focus. A Python automation framework that was genuinely useful — gone. An n8n workflow collection with 12 production deployments — gone. The profile represents what you're building now, not everything you've ever built. Portfolio pages are for the archive. The profile is for the present tense.

## Nixtla v0.7.0: The Review Kit

The Baseline Lab was ready for external eyes. Specifically, Max Mergenthaler's eyes — Nixtla's CEO. Eight commits to get it presentation-ready.

The gap between "works on my machine" and "ready for review by someone who matters" is always larger than you expect. Code that runs correctly can still fail a review if the reviewer can't figure out what it does in the first 60 seconds. Every commit in this batch was about closing that gap.

### What Shipped

**Benchmark reporting tool.** Runs the full M4 Monthly benchmark suite and produces a formatted report: model name, dataset slice, sMAPE, MASE, runtime, and a pass/fail indicator against the golden thresholds. The report is both human-readable (Markdown table) and machine-parseable (JSON sidecar). The dual format matters — Markdown for the README, JSON for programmatic consumption by downstream tools that need to track accuracy trends over time.

**Reproducibility bundles.** A single command packages the entire experiment — code version, data hash, environment snapshot, forecast output, and the benchmark report — into a timestamped tarball. Anyone can unpack it, run the same code, and verify they get the same numbers. Reproducibility is the baseline for credibility in forecasting. Without it, benchmark numbers are just marketing claims.

**GitHub issue draft generator.** Converts findings from a benchmark run into pre-formatted GitHub issues. If AutoETS regresses on a specific dataset slice, the generator creates an issue with the slice ID, expected vs. actual sMAPE, the commit that introduced the regression, and a suggested investigation path. The template includes labels, assignee suggestions, and a reproduction command. Saves 10 minutes per issue and eliminates the "I found a regression but forgot to file it" failure mode.

**TimeGPT showdown mode** from Phase 8 got polish — cleaner output formatting, better error messages when the API key is missing, and a summary table at the end showing which model won on each metric. The summary table is the artifact Max cares about most. One table that says "on this dataset, AutoETS beats TimeGPT on sMAPE by X% and loses on MASE by Y%." That's the conversation starter for a CEO evaluating whether statistical baselines are competitive with foundation models.

### The Review Kit

v0.7.0 also shipped a set of review kit scripts. These aren't part of the product. They're for the reviewer.

- `review-quickstart.sh` — clones, sets up, runs one forecast, produces one chart. Under 2 minutes. Tested on a fresh Ubuntu 22.04 VM to make sure there are no hidden dependencies on my local machine.
- A README rewrite with a DevRel UX flow: problem statement, one-command demo, architecture diagram, then details. The old README started with installation instructions. Nobody cares about installation until they know why they should install it. The new flow answers "why" in the first paragraph and "how" in the second.
- A mobile checklist for Max. Bullet points, no code blocks, readable on a phone screen. The CEO is not going to SSH into a server to evaluate this. He's going to read it on his phone between meetings and decide if it's worth a deeper look.

The mobile checklist was the highest-leverage artifact of the day. Everything else supports the code. The checklist supports the decision-maker.

The checklist had five sections: what the project does, what shipped this week, one thing to try (a link to the hosted demo), the benchmark numbers, and a "what's next" section with three bullet points. No technical jargon. No architecture diagrams. No code snippets. Just answers to the questions a busy CEO will ask: what is it, does it work, and what's the plan.

## Perception: README Restructure

One commit. The Perception dashboard README got the same treatment as the GitHub profile — shorter, focused, verified. Removed stale feature descriptions for things that had been refactored out. Updated the architecture section to reflect the current trigger-based system.
Added a quick-start section that didn't exist before.
This was a 20-minute cleanup, not a project.

## The Numbers

| Repo | Commits | What Changed |
|------|---------|-------------|
| github-profile | 3 | README rewrite (305 to 135 lines), badge refresh, metric verification |
| nixtla | 8 | Benchmark reporter, reproducibility bundles, issue generator, review kit, v0.7.0 |
| perception | 1 | README restructure, stale feature descriptions removed |

## The Pattern

Three repos touched. All documentation. Zero functional changes. The temptation is to skip days like this in a dev log because "nothing happened." But the GitHub profile now accurately represents the portfolio. The Nixtla review kit means the CEO can evaluate the project without scheduling a demo. The Perception README won't confuse the next person who opens the repo.

The review kit is the most important output. Everything else on this day was incremental improvement to existing docs. The review kit is a new artifact type — a package designed to make someone else's decision easier. Not documentation for the developer. Documentation for the decision-maker.

Documentation is a product. Ship it like one.

---

### Related Posts

- [Nixtla Baseline Lab: Phases 4 Through 8 in a Single Day](/posts/nixtla-baseline-lab-phases-four-through-eight/) — the build sprint that created everything this review kit packages
- [GitHub Release Workflows, Uncommitted Changes, and Semantic Versioning](/posts/github-release-workflow-uncommitted-changes-semantic-versioning/) — release automation patterns for version bumps
- [Enterprise Documentation Transformation: Git-Native TaskWarrior Workflows](/posts/enterprise-documentation-transformation-git-native-taskwarrior-workflows/) — documentation-as-product philosophy applied to enterprise workflows
