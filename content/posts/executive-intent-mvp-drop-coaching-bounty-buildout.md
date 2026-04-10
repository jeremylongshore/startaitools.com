+++
title = 'Executive Intent MVP Scaffold, Drop Coaching Curriculum, and Bounty Tracker Buildout'
slug = 'executive-intent-mvp-drop-coaching-bounty-buildout'
date = 2026-01-11T10:00:00-06:00
draft = false
tags = ["architecture", "gcp", "firebase", "testing", "ci-cd"]
categories = ["Development Journey"]
description = "Fifteen commits across four repos. Executive Intent gets its GCP/Firebase scaffold with CI and Gemini review. Drop gets a coaching curriculum for Shelly. Bounty tracker adds PR tracking."
+++

Four repos, fifteen commits, three distinct workstreams. January 11th split between greenfield scaffolding, curriculum design, and feature buildout. The unifying theme is preparation — each workstream is setting up the conditions for fast iteration rather than iterating fast on shaky foundations.

## Executive Intent MVP Scaffold

Executive Intent is a new platform for AI-assisted executive decision support. The premise: executives make decisions based on incomplete data scattered across a dozen tools. The platform aggregates evidence, surfaces relevant context, and presents recommendations with provenance chains so the decision-maker can trust the input.

Today was day one — no application code, all infrastructure.

The scaffold covered the full GCP/Firebase stack:

- **Firebase project initialization.** Firestore rules, storage rules, hosting config. Emulator suite configured for local development so nothing touches production during early iteration. The emulator config mirrors production exactly — same security rules, same indexes, same field validation. The gap between "works locally" and "works in production" should be zero.
- **CI pipeline.** GitHub Actions with lint, type-check, test, and build stages. Runs on every push and PR. The pipeline is strict from day one — no "we'll add CI later" that turns into "we'll add CI never." The pipeline also runs the Firebase emulator during tests, so integration tests hit a real Firestore instance (just a local one).
- **Gemini PR review.** Automated code review on every pull request using the Gemini API. The review focuses on security issues, type safety, and adherence to the project's architecture decisions. Not a replacement for human review — a first pass that catches the obvious stuff before a human spends time on it. The Gemini review workflow is templated from the one running on five other repos — tested patterns, not experiments.
- **Test suite foundation.** Vitest configured with coverage thresholds. Three placeholder tests that verify the project structure, imports, and config loading. The threshold starts at 80% and can only go up. The placeholder tests exist to ensure the test runner itself works — importing the config module, verifying environment variable loading, and checking that the project's TypeScript paths resolve correctly. These aren't testing business logic. They're testing that the test infrastructure works before there's business logic to test.
- **Next.js CVE patch.** The `create-next-app` scaffold shipped with a vulnerability in `next@14.x`. Patched to `14.2.29` before writing any application code. Starting a project with a known CVE is starting a project with technical debt on day zero. The CVE was in the middleware layer — a path traversal that could leak environment variables. Not exploitable in local development, but not the kind of thing you want in a production scaffold.

The whole scaffold is ten commits. That's a lot for "no application code," but every one of those commits is something that would be harder to retrofit later. CI is trivial to add to an empty repo. It's painful to add to a repo with 50 files and no test conventions. Gemini review is trivial to configure when there are no existing patterns to contradict. Coverage thresholds are trivial to enforce when coverage is 100% of zero lines.

This is the third project I've scaffolded with this exact pattern: Firebase + GitHub Actions + Gemini review + Vitest + strict TypeScript. The scaffold itself is becoming a template. Each new project starts from the same foundation and customizes from there. The consistency means moving between projects doesn't require relearning the CI pipeline or the test framework.

## Drop Coaching Curriculum for Shelly

The Drop project added a coaching curriculum — a structured learning path for the Shelly AI assistant. Shelly handles reporting and status updates. The curriculum defines what Shelly should know, how it should respond to different query types, and what level of detail is appropriate for different audiences.

Most AI assistants in developer tools are configured with a single system prompt and a prayer. The curriculum approach is different: instead of one monolithic prompt, you build a library of situational responses that the assistant selects from based on context. It's the difference between "here's everything you need to know" and "here's how to behave in this specific situation."

This isn't prompt engineering in the "tweak the system prompt until it works" sense. It's curriculum design — a structured body of knowledge with explicit learning objectives. The curriculum has modules:

1. **Context gathering.** How to pull relevant data from git, beads, and PR metadata without overwhelming the output.
2. **Audience awareness.** A technical lead wants commit-level detail. A product manager wants feature-level summaries. An executive wants three bullet points and a risk assessment.
3. **Escalation patterns.** When to flag something as needing human attention rather than generating a summary that papers over a problem.

Each module has example inputs, expected outputs, and failure modes. The curriculum is versioned alongside the codebase so it evolves with the tool.

The audience awareness module is the most important. The same git history can produce a five-paragraph technical summary or a three-line executive brief. Getting this wrong is worse than not having the tool — a PM who receives engineer-level detail stops reading reports, and an engineer who receives executive-level summaries can't act on them.

The escalation patterns module addresses the AI's biggest weakness: not knowing when to say "I don't know." A reporting tool that generates confident summaries about a failing pipeline is actively dangerous. The curriculum trains Shelly to flag anomalies — unusually low commit counts, broken CI, missing beads entries — instead of smoothing them into a narrative.

## Bounty Tracker PR Tracking

The bounty tracker (initialized yesterday) got its first real feature: PR tracking.

When a bounty is claimed and a PR is submitted, the tracker links them. It monitors PR status — open, review requested, changes requested, merged, closed — and updates the bounty status accordingly.

The implementation polls the GitHub API on a cron schedule. Not event-driven yet — webhooks are the obvious next step, but polling is simpler to debug and good enough for the current scale of maybe ten active bounties at any time.

Why not webhooks from the start? Because webhooks require a public endpoint, SSL, payload verification, and retry handling. Polling requires a cron job and an API token. For ten bounties, polling wins on simplicity.

Added basic filtering: filter bounties by status, by repository, by claimant. The data model is intentionally flat — a bounty has a title, a value, a status, and an optional PR URL. No premature normalization.

The polling approach has an obvious limitation: GitHub API rate limits. The tracker makes one API call per tracked PR per cron cycle. At ten bounties, that's ten calls every fifteen minutes — well within the 5,000/hour authenticated limit. At a hundred bounties, it would need batching or webhooks. Building for the current scale and noting the upgrade path.

The status transitions are simple: `open` -> `claimed` -> `pr_submitted` -> `pr_merged` -> `paid`. Each transition is logged with a timestamp. The tracker doesn't handle payment — it just records when a bounty moves to `paid` based on manual confirmation. Keeping the financial side manual is intentional. Automating payment requires tax reporting, compliance, and legal review. The tracker handles the engineering workflow; payment is a business process that stays separate.

---

Fifteen commits, four repos. Executive Intent has a scaffold that's stricter than most production projects. Shelly has a curriculum instead of a prompt. The bounty tracker tracks PRs.

The common thread: each workstream invested in structure before building features. CI before code. Curriculum before prompts. Data model before UI.

These investments feel slow on day one and pay dividends every day after.

Each workstream moved meaningfully forward without getting in the others' way.

The day produced no user-facing features and no production deployments. Every commit was preparation. Scaffolds, curricula, data models, CI pipelines. The kind of work that makes the next week productive instead of the next hour.

### Related Posts

- [Governance Day: Proprietary Licenses, Portfolio Refresh, and STCI Dashboard v0.5.0](/posts/governance-day-licenses-portfolio-stci-dashboard/)
- [HustleStats Launch Sprint: Stripe Billing and Paywall Enforcement](/posts/hustlestats-launch-sprint-stripe-billing-paywall/)
- [Building Production CI/CD: Documentation to Deployment](/posts/building-production-ci-cd-documentation-to-deployment/)
