+++
title = 'AI Code Review Blind Test: Where 5 Bots Shine'
slug = 'ai-code-review-without-context-blind-test'
date = 2026-04-16T08:00:00-05:00
draft = false
tags = ["ai-agents", "automation", "claude-code", "open-source", "ci-cd"]
categories = ["AI Engineering"]
description = "Five AI bots reviewed 74 PRs blind. No Slack, no roadmap. Matched maintainer decisions 63.5%. The breakdown is the finding."
toc = true
tldr = "A multi-bot review pipeline (CodeRabbit, Gemini, Greptile, CodeQL, Qodo, with Claude Code synthesizing) judged 74 real Kilo-Org/kilocode PRs with zero strategic context and matched actual maintainer decisions 63.5% of the time. The breakdown is where it gets useful: 76.5% on REQUEST_CHANGES, 78.8% on COMMENT, 33.3% on APPROVE. A tier curve runs 28% on simple docs PRs but 100% on major refactors. Context-free AI review is strongest exactly where maintainer review is most expensive."
+++

## The result, up front

Five AI review bots running blind against 74 real open-source PRs hit **63.5% agreement** with what the project's maintainers actually did. No Slack, no roadmap, no release-timing context. Just the diff, the bot consensus, the test suite, and Claude Code synthesizing the verdict. Every review artifact was written by the pipeline; the human role was a final approval gate before anything would have been submitted upstream, which never happened.

That number gets more interesting when you break it down. The pipeline is strong where it needs to be strong, weak where it *should* be weak, and counter-intuitively best on exactly the kind of PRs that cost maintainers the most time. The asymmetry is a deployment blueprint for AI code review.

## Setup

The pipeline ran against 75 real PRs on a fork of [Kilo-Org/kilocode](https://github.com/Kilo-Org/kilocode), a TypeScript monorepo. Workflow: cherry-pick the PR onto the fork, let five AI review bots auto-review it, run the test suite in a fresh GitHub Codespace, synthesize the findings, and record a verdict (APPROVE, COMMENT, or REQUEST_CHANGES) in a private journal under [`/.reviews/`](https://github.com/jeremylongshore/kilocode/tree/main/.reviews) on the fork. The verdicts never left the fork. Once the real Kilo-Org maintainers made their own calls on those PRs over time, the private corpus became a blind-prediction set.

One PR was marked do-not-merge by its own author and excluded. That leaves **74 blind verdicts** to compare against actual maintainer behavior.

## The bench

Full pipeline documented in [`.reviews/METHODOLOGY.md`](https://github.com/jeremylongshore/kilocode/blob/main/.reviews/METHODOLOGY.md):

| Layer | Tool | Role |
|-------|------|------|
| Bot | CodeRabbit | Line-by-line review, summaries |
| Bot | Gemini Code Assist | Second-model perspective |
| Bot | Greptile | Codebase-graph-aware review |
| Bot | CodeQL | SAST security scanning |
| Bot | Qodo PR-Agent | Open-source auto-describe/review |
| Search | Sourcegraph | Blast-radius queries |
| Primary | Claude Code | Synthesis, verdict composition, journal |
| Gate | Human | Approval gate only (never triggered upstream submit) |

Eleven-step workflow: pick a PR, read every existing upstream comment, mirror to fork so bots auto-review, fetch metadata and diff, synthesize bot findings, run a tiered verification (CI, local tests, manual UI spot-checks), Claude Code composes the review and journal, lint for tone and links, gate approves (step 10), submit upstream (step 11). Step 11 was never executed. That's what made the corpus a blind set.

Of the 75 PRs reviewed, 54 were fork-mirrored with the full five-bot treatment. The other 21 got local review only, typically because fork cherry-pick would have produced misleading bot diffs on stale or conflict-heavy branches. Both groups contribute to the 74-PR comparable set. Everything (per-PR `status.json`, full journals, fork-PR bot threads, aggregated test logs) browses from [`/.reviews/`](https://github.com/jeremylongshore/kilocode/tree/main/.reviews).

**What the pipeline deliberately did not see:** the Kilo-Org maintainer Slack, the current release branch strategy, ongoing architectural refactors, downstream dependency timing, superseded-PR lineage, or any conversation not linked in the PR itself. Every verdict was formed from the diff, the existing upstream comment thread, the bot consensus, the CI signals, and the codebase at HEAD.

Test runs were real. The [aggregated `.reviews/logs/` run](https://github.com/jeremylongshore/kilocode/tree/main/.reviews/logs) shows 7,938 passing tests in 142.52 seconds for the `kilo-code` package against the cherry-picked branches, running on Codespace `premiumLinux` (8-core, 32GB RAM), the tier recorded verbatim in eight per-PR status files.

## The scorecard

| Verdict | N | Matched maintainer | Accuracy |
|---------|---|---------------------|----------|
| REQUEST_CHANGES | 17 | 13 | **76.5%** |
| COMMENT (neutral) | 33 | 26 | **78.8%** |
| APPROVE | 24 | 8 | **33.3%** |
| **Overall** | **74** | **47** | **63.5%** |

Three things to take away from this table.

**Rejection and triage are strong.** REQUEST_CHANGES hit 76.5% and COMMENT hit 78.8%. When the pipeline said "this shouldn't merge as-is" or "this needs more discussion," the real maintainers agreed roughly four times out of five. Those calls lean on signals that live inside the diff and the CI output: missing tests, unresolved feedback, merge conflicts, type unsafety, stale branches. Context-free AI review handles them well because the context *is* the diff.

**APPROVE is honest about its limits.** Two-thirds of PRs the pipeline would have merged went differently: closed, superseded, merged only after revision. That's not a failure mode, it's the right answer. Approving a PR for merge is the decision most entangled with strategic context: release timing, competing PRs, user prioritization, roadmap. The pipeline didn't have any of it. A 33% APPROVE accuracy is exactly the signal you want. It tells you where the maintainer has to stay in the loop.

**The tier curve is the best news in the corpus:**

| Tier | Description | Match rate |
|------|-------------|-----------|
| 1 | Docs-only | **28%** |
| 2 | Small code fix (<50 lines) | 54% |
| 3 | Scoped feature | 67% |
| 4-5 | Multi-file feature | 82% |
| 6 | Major refactor | **100%** |

**The curve is inverted from difficulty.** Complex multi-file refactors (the PRs that cost maintainers the most review time) are exactly where the pipeline is most accurate. Docs-only PRs, the "easy" ones, are where it struggles. The explanation is structural: complex PRs broadcast their issues in the diff (new abstractions, interface changes, test coverage patterns, cross-file ripple). Simple PRs are often gated by context that never makes it into the code: a Slack thread, a verbal agreement, a coordinator's preference.

This is the deployment blueprint. An AI review pipeline earns the most trust exactly where maintainer review is the most expensive.

## Three cases the context gap explained

Full journal and (where fork-mirrored) bot thread for each lives under `.reviews/PR-<number>/` on the fork.

**[PR #5267](https://github.com/Kilo-Org/kilocode/pull/5267), release-timing context.** A Gemini 3 `extra_content` plumbing fix. The pipeline flagged REQUEST_CHANGES: the OpenRouter provider listed in the PR description wasn't in the actual diff, there were no tests, and the branch had merge conflicts. The journal's observation: *"The entire downstream plumbing is useless if the originating provider doesn't emit the field."* Technically correct. The maintainers merged it anyway. Unblocking a downstream integration inside a specific release window beat holding for completeness. The pipeline scored the code. The maintainers scored the code *and* the release cycle.

**[PR #4631](https://github.com/Kilo-Org/kilocode/pull/4631), roadmap context.** A clean fix for Anthropic "thinking block" filtering when users switch models mid-conversation. The pipeline called APPROVE. The journal praised "the right level of abstraction" and separately noted the tests were "thorough." The maintainers closed it, not for technical reasons, but because a different architectural choice landed in parallel. The pipeline was reviewing the code. The maintainers were reviewing the code against a roadmap the pipeline couldn't see.

**[PR #5568](https://github.com/Kilo-Org/kilocode/pull/5568), hygiene gate vs. pragmatism gate.** A six-line override for MiniMax and Kimi context windows. The pipeline left a COMMENT flagging a missing changeset and un-run upstream CI. It merged without either. The pipeline's hygiene checklist exceeded what the maintainers actually gated on. Correctness was enough; paperwork was optional.

Three clean categories of off-diff context: release timing, roadmap lineage, organizational pragmatism. None of these were the pipeline being wrong about the code. All of them were the pipeline being wrong about the *frame* the code lived inside. That's a recoverable failure mode. You add the context back by posting the review and letting the maintainer respond. It's not a structural flaw.

## What this teaches us about AI code review

Three patterns stack cleanly out of the data.

**Context-free review is a rejection-and-triage engine.** The combined 77% accuracy on REQUEST_CHANGES + COMMENT means a well-tuned multi-bot pipeline can reliably route PRs away from a maintainer's critical-path queue. That's a real productivity win at any team scale. If a bot army catches four-out-of-five PRs that shouldn't merge as-is, maintainer attention gets spent on the ones that actually need human judgment.

**Diff-broadcast signals are learnable at scale. Off-diff signals aren't.** The tier inversion proves it. Major refactors have their design tension written into the structural code (new modules, interface changes, coverage patterns), and multi-bot consensus reads them fluently. Docs PRs often depend on context that lives in a Slack thread or a coordinator's memory. No amount of additional bots recovers information that was never in the input.

**The accuracy curve is a deployment blueprint, not a limitation.** Point AI review at complex PRs with high trust. Keep humans in the loop on approval decisions and on the simple-but-context-heavy PRs. That mapping matches where maintainer time is actually scarce, and it matches what the data shows AI can and can't do. An honest AI review product ships this asymmetry as a feature.

## Reproducibility

The pipeline is reproducible on any active open-source TypeScript monorepo. Fork it, set up five review-bot integrations, provision GitHub Codespaces (free tier covers ~60 PRs/month on premium Linux), cherry-pick PRs onto the fork, let the bots auto-review, run the tests, synthesize. The [METHODOLOGY.md](https://github.com/jeremylongshore/kilocode/blob/main/.reviews/METHODOLOGY.md) is checked in, and every per-PR verdict, journal, bot thread, and test log is browsable under [`/.reviews/`](https://github.com/jeremylongshore/kilocode/tree/main/.reviews).

The methodology matters as much as the number. A blind-prediction setup is how you honestly measure any AI review tool: record the pipeline's call before the maintainer decision happens, then compare. Without that discipline, any self-reported accuracy figure is suspect.

## Related

- [`.reviews/`](https://github.com/jeremylongshore/kilocode/tree/main/.reviews): full corpus, methodology, per-PR journals, test logs
- [METHODOLOGY.md](https://github.com/jeremylongshore/kilocode/blob/main/.reviews/METHODOLOGY.md): workflow + stack
- [DASHBOARD.md](https://github.com/jeremylongshore/kilocode/blob/main/.reviews/DASHBOARD.md): every PR, verdict, tier, confidence

---

*Separately, one upstream contribution to Kilo-Org/kilocode during this window was merged: [PR #5880](https://github.com/Kilo-Org/kilocode/pull/5880).*
