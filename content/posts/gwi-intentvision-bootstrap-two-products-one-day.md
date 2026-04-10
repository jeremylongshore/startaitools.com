+++
title = 'Two Products Bootstrapped from Zero to Release in One Day'
slug = 'gwi-intentvision-bootstrap-two-products-one-day'
date = 2025-12-15T10:00:00-06:00
draft = false
tags = ["git-with-intent", "intentvision", "nixtla", "release-engineering", "bootstrapping"]
categories = ["Development Journey"]
description = "git-with-intent v0.2.0 through 7 phases, IntentVision from init to v0.1.0 across 11 phases, plus project-template and nixtla commits. Two products shipped from empty repos."
+++

December 15th was a bootstrapping day. Two products went from empty directories to tagged releases. Not prototypes. Not "hello world" scaffolds. Actual versioned releases with real functionality.

## git-with-intent: 11 Commits Through 7 Phases

git-with-intent is the AI-assisted git workflow tool. On December 15th it went from concept to v0.2.0 across 11 commits.

The phases tell the story:

- **Phase 1**: Core commit analysis engine. Parse git history, extract semantic meaning from diffs.
- **Phase 2**: Intent classification. Map commits to intent categories (feature, fix, refactor, chore).
- **Phase 3**: Workflow templates. Predefined patterns for common git workflows.
- **Phase 4**: CLI scaffolding. Commander.js setup with subcommands for each operation.
- **Phase 5**: Configuration system. User-level and repo-level config with sensible defaults.
- **Phase 6**: Output formatting. Structured output for terminal, JSON, and markdown.
- **Phase 7**: Release prep. Version bump, changelog generation, LICENSE, README.

Each phase was a focused commit or two. No phase depended on a phase that hadn't been built yet. The ordering was deliberate — you can't build intent classification without a commit analysis engine, and you can't build a CLI without knowing what operations you're exposing.

v0.2.0 tagged at the end of phase 7. Not v0.1.0 — the version reflects that two minor iterations happened during the build. Phase 4 required rethinking the CLI surface area, which bumped the version.

## IntentVision: 18 Commits Through 11 Phases

IntentVision is the visual analytics companion. It reads git-with-intent output and renders dashboards, timelines, and contribution graphs.

Eighteen commits across 11 phases in a single day. That's aggressive. Here's how it breaks down:

- **Phases 1-3**: Data ingestion. Read git-with-intent JSON output, normalize the schema, build an in-memory model.
- **Phases 4-6**: Visualization primitives. Timeline rendering, contributor heatmaps, intent distribution charts.
- **Phases 7-9**: Dashboard composition. Combine primitives into configurable dashboard layouts.
- **Phase 10**: Export pipeline. Generate static HTML reports that work without a running server.
- **Phase 11**: Release. v0.1.0 tagged with a working end-to-end flow: git repo in, visual report out.

The interesting constraint was that IntentVision had to consume git-with-intent's output format. That format was being designed the same day. So phases 1-3 of IntentVision were built against a moving target. The solution was simple: define the JSON schema first as a shared contract, then build both products against it.

This is the upside of building two products in one day. You make the integration decision once, upfront, instead of discovering the impedance mismatch six months later.

## The Supporting Cast

Two other repos got commits on December 15th.

**project-template** received 6 commits. This is the scaffolding template used to initialize new projects. The commits added the standard governance files (LICENSE, CONTRIBUTING, SECURITY), CI/CD workflow templates, and the CLAUDE.md template that every project uses. Timing isn't coincidental — building two products from scratch in one day made it obvious which parts of project setup should be automated.

**nixtla** got 1 commit. A minor dependency update. Not every repo gets a dramatic day.

## The Shared Schema Decision

The most consequential decision of the day wasn't in any individual phase. It was defining the JSON schema contract between git-with-intent and IntentVision before either product had a line of code.

The schema defines what a "commit analysis result" looks like. Commit hash, author, timestamp, classified intent, confidence score, affected files with change categories. IntentVision consumes this. git-with-intent produces it. Both were built in parallel against the same contract.

If I'd built git-with-intent first and let the output format emerge organically, IntentVision would have had to adapt to whatever format evolved. That adaptation cost compounds over time. Every format change in the producer requires a corresponding change in the consumer. Define the contract first and both sides build to spec.

## The Pattern

Thirty-six commits across four repos. Two new products released. The execution was linear — no debugging sagas, no architecture pivots, no production fires. Phase 1, phase 2, phase 3, all the way through.

That linearity is the point. When you're bootstrapping from zero, the fastest path is sequential phases with clear boundaries. You don't parallelize day-one work. You don't build the dashboard before the data layer exists. You don't write tests for an API that hasn't been designed.

The hard part isn't any individual phase. It's maintaining velocity across 36 commits without losing coherence. Each commit has to advance the product. No "WIP" commits, no "fix typo" commits that should have been caught in review. When you're the only developer and you're shipping two products, every commit is a mini-release.

Two products. One day. Both still running.

The next day, I threw away most of the git-with-intent architecture and rebuilt it from scratch. But that's a different post.

---

## Related Posts

- [Nixtla Repo: Zero to v0.2.0 with a Working Search-to-Slack Plugin](/posts/nixtla-repo-init-through-v020-search-slack-plugin/) — Another zero-to-release bootstrapping day
- [git-with-intent v0.9 to v0.10: Docker Upgrades, README Rewrites, and Strategic Research](/posts/git-with-intent-v090-v0100-docker-upgrades/) — Where git-with-intent ended up months later
- [Building Production CI/CD: Documentation to Deployment](/posts/building-production-ci-cd-documentation-to-deployment/) — The CI/CD patterns that enable single-day product launches
