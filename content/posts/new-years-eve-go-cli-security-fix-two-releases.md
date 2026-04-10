+++
title = "New Year's Eve: A Go CLI From Scratch, a Security Fix, and Two Releases"
slug = 'new-years-eve-go-cli-security-fix-two-releases'
date = 2025-12-31T10:00:00-06:00
draft = false
tags = ["go", "cli", "security", "release-engineering", "testing", "create-agent-skill", "git-with-intent", "hustlestats", "intent-mail", "perception"]
categories = ["Development Journey"]
description = "New Year's Eve across five projects: a brand new Go CLI validator and skill wizard, a critical eval injection fix in GWI, Dream Gym AI strategy, and two point releases for Intent Mail and Perception."
+++

Last day of 2025. Five projects touched. Twenty-five commits. One project built from nothing, one patched a security hole that should never have existed, and two shipped point releases to close out the year clean.

## create-agent-skill: New Go CLI

Nine commits. Brand new project. A Go CLI tool for validating and scaffolding Claude Code agent skills. The problem it solves: skill definitions are YAML files with a specific schema, and getting the schema wrong means the skill silently fails to load or behaves unexpectedly at runtime.

The validator checks skill definitions against the spec: required fields present, types correct, tool declarations match available tools, prompt templates reference valid variables. It's the kind of validation that catches errors at authoring time instead of at runtime when a user tries to invoke the skill and gets an opaque failure. The error messages are specific — not "invalid skill definition" but "field 'trigger_phrases' is required and missing" or "tool 'web_search' is declared but not in the available tools registry."

The skill wizard is the interactive counterpart. Walk through a series of prompts — name, description, tools needed, trigger phrases — and it generates a complete skill definition file. The wizard enforces the same validation rules inline, so you can't accidentally create an invalid skill. If you select a tool that requires specific permissions, the wizard prompts for those permissions before continuing. The generated file includes comments explaining each field.

Go was the deliberate choice here. The tool needs to be a single binary that drops into any developer's PATH. No runtime dependencies, no virtual environments, no `npm install`. Go compiles to a static binary. Ship the binary, it works. The entire project compiles in under 3 seconds. That fast feedback loop matters when you're iterating on CLI flag parsing and output formatting.

CI/CD went in on commit 4 of 9. GitHub Actions runs `go vet`, `go test ./...`, and `golangci-lint` on every push. The test suite covers both the validator logic (does it catch missing required fields? does it reject unknown tool references?) and the wizard output (does the generated file pass validation?). Circular validation — the tool validates what the tool generates. If the wizard produces something the validator rejects, both are wrong.

The release workflow cross-compiles for Linux, macOS (ARM and Intel), and Windows. Four binaries per release, uploaded as GitHub release assets. `goreleaser` handles the matrix build, checksums, and release note generation. A developer downloads their platform binary and they're running.

## git-with-intent: The Eval Fix

Five commits. One of them was critical. The rest were important. But the critical one is why this section exists.

The expression evaluator in the approval gate system was using `eval()`. Python's `eval()` with user-influenced input. In a CI/CD tool that processes commit messages and PR descriptions.

The attack surface: craft a commit message with a Python expression in the right field, and the approval gate evaluator would execute it. Not theoretical — any string that reached the expression evaluator was one `__import__('os').system('rm -rf /')` away from arbitrary code execution. In a CI/CD tool. Running with CI runner permissions. The blast radius of this vulnerability was everything the CI runner could touch.

The fix replaced `eval()` with a safe expression evaluator. The new evaluator parses expressions into an AST and walks the tree, supporting only comparison operators, boolean logic, and string operations. No function calls. No imports. No attribute access. The expression `commits > 5 and author != "bot"` works. The expression `__import__('os').system('whoami')` throws a `SafeExpressionError`.

This is the kind of fix where the diff is small and the risk it eliminates is enormous. Five lines of `eval()` replaced by a 200-line safe evaluator. The safe evaluator has its own test file with 40+ test cases covering every operator, every edge case in type coercion, and every known bypass technique for Python expression evaluators. Worth every line.

The other commits in this batch: approval gate logic fixes surfaced during Gemini code review, and test coverage for the new evaluator. The Gemini review feedback was genuinely useful here — it flagged edge cases in boolean short-circuiting that the initial test suite missed.

## Hustle: Dream Gym AI Strategy

Four commits. Sprint 7 of the Dream Gym module focused on AI-powered workout recommendations.

The strategy layer analyzes workout history to suggest programming adjustments. If your squat volume has been flat for three weeks while your deadlift keeps climbing, the system suggests squat-focused programming. If you've been training 6 days a week for a month with declining performance, it suggests a deload week. The suggestions are grounded in actual training principles — progressive overload, fatigue management, volume landmarks — not generic "try harder" advice.

The AI component calls the LLM with a structured prompt that includes the user's training history summary, current trends, and detected plateaus. The response is constrained to a specific schema: recommendation type, affected exercises, reasoning, and suggested duration. This keeps the AI output actionable instead of conversational.

E2E tests for the AI recommendations validate that the suggestion pipeline produces structurally correct output. They don't validate whether the suggestions are good — that's a human judgment call. But they do verify that the pipeline doesn't crash on edge cases: empty workout history, single workout, all rest days, exercises with no comparable history. The edge case tests matter more than the happy path tests here — users with sparse data are more common than users with complete training logs.

## Intent Mail v0.4.0

Four commits wrapped up the v0.4.0 release. The summarization, triage, and smart compose features from two days ago got their release packaging: changelog, version bump, migration notes for the config format change (provider configuration moved from a flat key-value to a structured router config).

The migration notes needed real care. The old config format was `ai_provider = "anthropic"` and `ai_api_key = "sk-..."`. The new format is a `[providers]` table with per-provider configuration, routing rules, and fallback chains. Anyone upgrading from v0.3.x to v0.4.0 needs to rewrite their config file. The migration notes include a before/after example and a validation command that checks the new config without sending any API calls.

The release is the first version of Intent Mail with real AI capabilities. Everything before v0.4.0 was plumbing — provider abstraction, CLI framework, TUI scaffold. v0.4.0 is where the product starts doing what the name promises: making email less painful through AI that runs locally, respects privacy, and works without a browser.

## Perception v0.5.0

Three commits. The v0.5.0 release crossed a testing milestone: 4,800+ tests passing. For a news intelligence platform, the test count reflects the combinatorial surface of feed parsing, deduplication rules, relevance scoring, and alert thresholds. Each feed format variation, each dedup edge case, each scoring boundary needs its own test.

v0.5.0 also bundles the 128-feed scaling work and TUI improvements from earlier in the week. The test milestone is worth pausing on. Perception's test suite grew from zero to 4,800 in about six weeks. The growth isn't from padding test counts — it's from the combinatorial nature of the domain. RSS feeds come in RSS 2.0, Atom 1.0, and various malformed hybrids. Each format has different date fields, content fields, and author fields. Multiply that by dedup strategies, scoring thresholds, and alert rules, and 4,800 tests is the natural result of testing the matrix properly.

## Closing Out the Year

Five projects in the last day of 2025. The Go CLI was the most satisfying — there's something about starting a project from `go mod init` and ending with cross-compiled release binaries in the same day. Go's compile times and single-binary deployment model make "zero to release in a day" feel achievable rather than reckless. No dependency hell. No build configuration nightmare. Just code, compile, ship.

The eval fix was the most important work of the day. Security bugs don't get less dangerous because it's a holiday. If anything, shipping a fix on December 31st means it doesn't sit on a "fix after break" list where it ages for two weeks while the vulnerability stays open.

The two releases (Intent Mail v0.4.0, Perception v0.5.0) are the kind of year-end cleanup that feels good. Ship what's ready. Tag it. Write the changelog while the context is fresh. Start 2026 with a clean slate instead of half-finished release branches collecting merge conflicts.

---

**Related Posts:**

- [Fixing Provider Registry Mutations and Sandbox Permissions](/posts/fixing-provider-registry-mutations-sandbox-permissions/) — Earlier GWI security hardening in the same vein as the eval fix
- [58 E2E Tests, a Slack Channel, and a Launch in One Day](/posts/58-e2e-tests-slack-channel-launch-one-day/) — E2E testing patterns used in the Dream Gym sprint
- [Perception Dashboard: Wiring Real Triggers, Topic Watchlists, and the BSL-1.1 Decision](/posts/perception-dashboard-real-triggers-topic-watchlists/) — The dashboard and alerting system Perception v0.5.0 extends

