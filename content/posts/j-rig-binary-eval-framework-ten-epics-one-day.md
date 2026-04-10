+++
title = 'j-rig Binary Eval Framework: Ten Epics, One Day'
slug = 'j-rig-binary-eval-framework-ten-epics-one-day'
date = 2026-03-29T10:00:00-05:00
draft = false
tags = ["typescript", "testing", "evaluation", "architecture", "monorepo", "ci-cd"]
categories = ["Technical Deep-Dive"]
description = "Building a full binary skill evaluation framework in a single day — ten epics from workspace scaffold to drift detection, with a calibration engine that measures whether your judges agree with themselves."
+++

Twenty-eight commits. Ten epics. A TypeScript monorepo that went from `pnpm init` to drift detection, eval packs, and a calibration engine in one calendar day. j-rig is a binary evaluation framework: given a skill definition and an execution trace, did the agent demonstrate the skill or not? Yes/no. Binary.

The "binary" part is the whole point. Eval frameworks love to produce scores — 0.73 out of 1.0, 4 out of 5 stars, "mostly correct." These numbers feel precise but they're not actionable. When your agent scores 0.73 on "can it parse a config file," what do you do? Is that good? Is that a regression? Binary evaluation strips away the false precision. The agent either parsed the config file or it didn't. Pass or fail. Now you can count, trend, and alert on real signals.

## The Architecture

The monorepo has a specific shape:

```
packages/
├── schemas/          # Zod schemas + YAML/SKILL.md parsers
├── registry/         # Deterministic skill registry
├── evidence/         # SQLite evidence layer
├── trigger/          # Roster, runner, metrics
├── execution/        # Harness + observation layer
├── judgment/         # Calibration engine + model matrix
├── reports/          # Regression, baseline, scoring, launch
├── optimizer/        # Failure clustering + experiment engine
└── drift/            # Drift detection + eval packs + reeval
```

Each package has a clear boundary. Schemas flow down. Evidence flows in from execution and out to reports. The judgment layer sits between execution and reports — it takes raw observations and produces binary verdicts. The optimizer sits beside reports, consuming the same evidence but producing recommendations instead of summaries.

The dependency graph is intentionally acyclic. Any package can be tested in isolation. Any package can be replaced without touching the others. This is what makes ten epics in one day possible — each epic is a vertical slice through one or two packages, not a horizontal change across all of them.

## Epic 1: Workspace Scaffold + CI

The boring but load-bearing work. pnpm workspace with `workspace:*` protocol references, strict TypeScript config with `noUncheckedIndexedAccess`, ESLint flat config, Vitest with coverage thresholds. CI runs on every push — lint, type-check, test, coverage gate. Nothing ships without green CI.

The scaffold is the most important commit. Every decision made here — dependency resolution strategy, TypeScript strictness level, test runner configuration — propagates through every subsequent epic. Get it wrong and you're fighting the toolchain for the rest of the day. Get it right and the toolchain disappears.

## Epic 2: Zod Schemas + Parsers

The type system is the contract. Every data structure in the system — skill definitions, execution traces, judgment records, calibration results — is defined as a Zod schema. The schemas serve triple duty: runtime validation, TypeScript type inference, and documentation.

Two parsers consume external formats. The YAML parser reads structured skill definitions:

```yaml
skill_id: config-file-parsing
version: 1
criteria:
  - id: reads-file
    description: Agent reads the target config file
    required: true
  - id: extracts-values
    description: Agent extracts all requested key-value pairs
    required: true
```

The SKILL.md parser handles a markdown format for human-authored skill definitions. Same information, different ergonomics. Authors who think in markdown write SKILL.md files. Authors who think in structured data write YAML. The registry accepts both.

Both parsers validate against Zod schemas at parse time. Malformed definitions fail fast with specific error messages — not "invalid YAML" but "criteria[1].description is required."

## Epic 3: Package Integrity + Deterministic Registry

The registry is a resolved, validated, content-addressed map of every skill in the system. "Deterministic" means the same inputs always produce the same registry state. No timestamps, no random IDs, no insertion-order dependencies. Two developers loading the same skill files get byte-identical registries.

The package integrity checker validates the registry itself. Duplicate skill IDs, dangling references between criteria, version conflicts — all caught before any evaluation runs. The integrity check runs as a CI gate. If you introduce a skill definition that conflicts with an existing one, CI fails before tests even start.

## Epic 4: SQLite Evidence Layer

Evidence is the foundation everything else reads from. Every execution, every observation, every judgment gets written to SQLite with a structured lifecycle: `created → running → completed | failed`. No evidence is ever updated in place — state transitions append new rows with timestamps.

SQLite is the right choice for a developer tool. No server process. No connection strings. No Docker dependency. Clone the repo, run the tests, and the evidence database is a file in `.j-rig/evidence.db`. You can query it with any SQLite client. You can copy it to another machine. You can check it into git if the data is small enough.

The run lifecycle is explicit. A run is created with a roster (which skills to evaluate), transitions to running when execution begins, and lands at completed or failed with a summary record. Partial failures are tracked — if 8 of 10 skills complete but 2 fail, the run is completed with a failure count, not marked as failed. Binary at the skill level, not at the run level.

## Epic 5: Trigger Harness

The trigger harness answers three questions: what to evaluate (roster), how to run it (runner), and what happened (metrics). The roster is a list of skill IDs pulled from the registry. The runner executes each skill evaluation in sequence, writing observations to the evidence layer. Metrics are computed after execution completes — pass rates, duration distributions, error categorization.

The roster supports filtering by tag, version range, and priority. You don't always want to run every eval. During development, you run the skills you changed. During CI, you run everything. During a release gate, you run the critical subset. The roster makes these different scopes explicit.

## Epic 6: Execution Harness + Observation Layer

This is where the agent under test actually runs. The execution harness sets up the environment, invokes the agent with a defined prompt, and captures everything that happens. The observation layer records what the agent did — tool calls, file operations, API requests, terminal output — as structured events.

Observations are raw. They contain no judgment. "Agent called `read_file('config.yaml')`" is an observation. "Agent successfully read the config file" is a judgment. This separation matters because the same observation can be judged differently depending on context, model, or calibration state.

The harness is intentionally dumb. It doesn't understand what the agent is doing. It doesn't try to be clever about what to record. It captures everything and lets the judgment layer decide what matters. This makes the harness reusable across different evaluation contexts without modification.

## Epic 7: Judgment Layer + Calibration Engine

The judgment layer takes observations and produces binary verdicts for each criterion in a skill definition. Did the agent read the file? Yes or no. Did it extract all values? Yes or no. The skill passes if all required criteria pass.

The calibration engine is the piece that makes this framework more than a test runner. It measures judge consistency. Run the same observations through the same judge model three times. Do you get the same verdicts? If a judge says "pass" on run 1 and "fail" on run 2 for identical observations, that judge is unreliable for that criterion.

The model matrix tracks calibration scores across judge models. GPT-4o might be 98% consistent on "did the agent read the file" but only 72% consistent on "did the agent handle the edge case gracefully." The matrix tells you which judges to trust for which criteria. Use the consistent judges. Retire or re-prompt the inconsistent ones.

```
Model Matrix (excerpt):
┌─────────────────┬──────────┬────────────────┬──────────────┐
│ Judge Model     │ reads-file│ extracts-values│ handles-edge │
├─────────────────┼──────────┼────────────────┼──────────────┤
│ gpt-4o          │    0.98  │      0.95      │    0.72      │
│ claude-3.5      │    0.99  │      0.97      │    0.89      │
│ gemini-2.5-flash│    0.96  │      0.91      │    0.68      │
└─────────────────┴──────────┴────────────────┴──────────────┘
```

This is the data that transforms "the eval said pass" into "the eval said pass, and this particular judge agrees with itself 97% of the time on this criterion." Confidence in your eval is now quantified, not assumed.

## Epic 8: Reports

Four report types, each serving a different audience:

**Regression reports** compare the current run against the previous run. What changed? Which skills flipped from pass to fail or vice versa? These are for developers checking whether their changes broke something.

**Baseline reports** compare the current run against a pinned baseline. The baseline is the last known-good state. Regressions against baseline are more significant than regressions against the previous run — the previous run might itself have been broken.

**Scoring reports** aggregate pass rates across skill categories, time ranges, and judge models. These are for managers and stakeholders who need a dashboard number.

**Launch reports** are go/no-go assessments. All critical skills must pass with calibrated judges. Any failure blocks launch. The launch report lists exactly what failed and why, with links to the evidence records.

## Epic 9: Optimizer

When skills fail, you want to know why and what to do about it. The optimizer has two components.

**Failure clustering** groups failures by common characteristics. If 12 skills fail and 10 of them involve file operations on Windows paths, that's one cluster with one root cause, not 10 independent failures. Clustering turns a wall of red into an actionable list of problems.

**The experiment engine** tests hypotheses. You think the file operation failures are caused by a missing path normalization step. Create an experiment: modify the agent prompt to include path normalization instructions, re-run the 10 clustered failures, compare results. The experiment engine tracks the hypothesis, the intervention, and the outcome. If the fix works, you have evidence. If it doesn't, you've eliminated a hypothesis and the record is preserved.

## Epic 10: Drift Detection + Eval Packs

Skills drift. The agent that scored 100% pass rate last month might score 85% this month — not because you changed anything, but because the underlying model was updated, or the test data shifted, or a dependency version bumped.

Drift detection runs the eval suite on a schedule and compares against the stored baseline. If pass rates change beyond a configured threshold, it alerts. The alert is specific: "skill `config-file-parsing` regressed from pass to fail on criterion `handles-edge`, judge `claude-3.5`, drift detected between runs 47 and 52."

Eval packs are portable evaluation bundles. A pack contains skill definitions, test fixtures, expected baselines, and judge configurations. You can share a pack across teams. You can version a pack alongside your agent. When the agent gets a major version bump, the eval pack gets updated to match. Packs make evaluation reproducible across machines and CI environments.

The reevaluation system triggers when a judge model is updated. Model updates can change judgment behavior. Reevaluation replays stored observations through the updated judge and compares new verdicts against the baseline. This catches silent model-update regressions — the kind where nothing in your code changed but your eval results shifted because the judge model got a bit more or less strict.

## CI: Gemini Code Review

Every epic followed the same commit pattern: feature commit, test commit, AAR (after-action review). The AAR records what worked, what didn't, and what to do differently. Not retrospective theater — these are one-paragraph notes written immediately after closing the epic.

Gemini AI code review runs in CI on every PR. Not as a replacement for human review — as a pre-filter. It catches the things humans skip when reviewing 28 commits in a day: unused imports, inconsistent naming, missing error handling on edge paths. The AI review runs in parallel with tests, so it adds zero time to the CI pipeline.

## Related Posts

- [IntentCAD v0.8.0 — Thirteen EPICs, One Day](/posts/intentcad-v080-thirteen-epics-one-day/) — same epic-per-day methodology applied to a different domain
- [Knowledge OS Bootstrap: Seven Epics, Marketplace Security, and Production AI Fixes](/posts/knowledge-os-bootstrap-seven-epics-marketplace-security/) — another TypeScript monorepo bootstrapped from scratch in a single day
- [Terminal-Bold Redesign and the 0% Recall Bug](/posts/terminal-bold-redesign-and-eval-recall-fix/) — evaluation recall debugging that motivated building a proper eval framework
