+++
title = 'Deterministic First, LLM Second: An Advisory CI Pre-Screen'
slug = 'deterministic-first-llm-advisory-ci'
date = 2026-05-15T08:00:00-05:00
draft = false
tags = ["ci-cd", "github-actions", "llm", "deterministic-systems", "groq", "pull-request-automation"]
categories = ["DevOps"]
description = "Wire an LLM into CI without veto power: the deterministic classifier is the product, the LLM is advisory polish, and the never-block contract retires the old system the same day."
+++

The old PR review system ran Gemini on every submission to the `claude-code-plugins` repo. It broke every time — quota errors, timeout, malformed JSON, the works. On 2026-05-15 I shipped a replacement and deleted the original on the same day.

The replacement is structured around two contracts. A deterministic classifier scores each submission against 12 rules and emits one of three verdicts. A Groq LLM bolted on top writes a 5-line summary as advisory polish. The deterministic layer is the product. The LLM never blocks.

The first live invocation immediately caught two bugs in the new system. That's not failure. That's the design working exactly as intended.

Five PRs in one day: [#719](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/pull/719), [#723](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/pull/723), [#721](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/pull/721), [#724](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/pull/724), [#725](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/pull/725). Together they close the epic and demonstrate why the deterministic-first pattern lets you replace a live system without a transition period.

> **The never-block contract:** LLM outputs are advisory only. They never block the primary CI decision. If the LLM crashes, times out, or hallucinates, the deterministic verdict posts unchanged and the rest of the pipeline runs as if the LLM step never existed.

## The two contracts that matter

The pre-screen workflow lives on two non-negotiable contracts that separate the product from the polish.

The first: **the deterministic classifier is the product.** It ingests validator JSON output, applies 12 rules to the changeset, and emits a verdict — `PASS`, `CHANGES_REQUESTED`, or `HARD_BLOCK`. Three outcomes. No gray. No ambiguity.

The classifier is a pure function. No I/O. No dependencies beyond the Python stdlib. Every test case maps to a rule. Every rule maps to observable, repeatable behavior. You can trace it from input to output without waiting for an API to respond or hoping an LLM doesn't hallucinate.

PR [#719](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/pull/719) closed this layer in 579 new lines: `.github/workflows/pr-prescreen.yml` (~270 lines of workflow), `scripts/pr-prescreen/classify.py` (the classifier), and 12 unit tests covering every rule and edge case.

The workflow pattern is fork-safe: `pull_request_target`, SHA-pinned checkout, `persist-credentials: false`, never executes PR-controlled code. I copied the security pattern verbatim from the broken Gemini workflow (lines 23-79 — those were the load-bearing security). The security model didn't change. The signal source did.

The second contract: **the LLM is advisory, never blocks.** When the deterministic layer says `PASS`, the Groq LLM generates a 5-line human-readable summary. The summary is rendered as a GitHub comment. It carries zero veto power.

If Groq times out, crashes, the API key leaks, or the model hallucinates — `continue-on-error: true` on the workflow step ensures the pre-screen verdict still posts. The comment just doesn't appear. Slack doesn't ping a summary. The rest of the CI runs unchanged. The primary signal is independent of the advisory layer.

The verdict table:

| Verdict | Deterministic rule | Slack | Comment | Retry |
|---------|------------------|-------|---------|-------|
| `PASS` | All skills ≥ C, no fatal errors | Ping | LLM summary (Groq) | No |
| `CHANGES_REQUESTED` | Missing fields or D/F grade | Silent | Deterministic details | No |
| `HARD_BLOCK` | Fatal validator error or missing impl | Ping | Deterministic details | No |

Groq runs only on `PASS` verdicts. If Groq fails, the verdict still posts — just without the summary. The deterministic layer is the contract. The LLM is the enhancement that runs *inside* the bounds of the contract.

PR [#723](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/pull/723) added the Groq integration: 388 new lines, `scripts/pr-prescreen/summarize.py`. It calls Groq directly via stdlib `urllib` — no SDK, no dependency overhead, no transitive vulnerability surface. Model: `llama-3.3-70b-versatile`. Wall-clock budget: 5 seconds. Single attempt. No retries.

The function is dead simple: POST the verdict JSON plus the changeset summary to Groq, parse the response, format it, return. 11 unit tests including fixes from PR #720's review:

- broad `except Exception` for the never-block contract — catch literally everything
- `OSError` instead of `TimeoutError` for broader I/O coverage (`socket.timeout`, connection resets, the rest of the network failure surface)
- `json.JSONDecodeError` guard for malformed responses

One tested invariant matters most: **user-controlled PR content cannot override the fixed system prompt.** The system prompt is a string literal in the source. The PR body is data. They never meet in the same code path. The classifier output goes into the user-role message; the system role is hard-coded and unreachable from outside.

## What "never block" buys you

The old Gemini system gave an LLM veto power over 3,000+ shipped artifacts. Every time it broke, you couldn't delete it — too much workflow depended on it staying alive. The downstream blast radius made retiring it a multi-week migration.

You're stuck in maintenance mode: tuning prompts, chasing API changes, hoping the next model version handles the job the same way the last one did. You can't turn it off. You can't replace it. The veto power is a cage.

The never-block contract changes the trade-off entirely. The LLM is an enhancement layered on top of a deterministic core, not the core itself. If it malfunctions, the workflow degrades gracefully to the deterministic verdict — which you already trust to be correct.

You can replace the old system on the same day you deploy the new one. You're not hedging bets. You're not running both in parallel. You're not waiting for three weeks of production data to prove the new system is safe. You measure trust against the deterministic layer; the LLM is polish that can't revoke the decision.

PR [#719](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/pull/719) merged. The next day PR [#721](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/pull/721) deleted `gemini-code-review.yml` (179 lines of perpetually broken YAML) as a single breaking change.

That PR removed:

- the workflow file itself
- the orphaned `ENABLE_GEMINI_REVIEW` repo variable (operator deletes after merge)
- the `--thorough` flag on the validator (advertised in the README but with broken plumbing)

It also added two new surfaces:

- `scripts/pr-prescreen/audit.py` — appends one row per pre-screen run to `freshie/inventory.sqlite`, tracking the decision history for post-mortems and operator review. Inline `CREATE TABLE IF NOT EXISTS` schema. `continue-on-error: true` so DB failures don't mask the primary signal.
- a 265-line operator runbook at `000-docs/265-DR-GUID-pr-prescreen-system.md` documenting the workflow, the verdicts, the audit schema, and the operator's playbook.

No transition period. No parallel runs. No "let's keep both for safety." The new system had been live for exactly one `workflow_dispatch` manual invocation. That was enough to trust it — because the deterministic layer is the contract and it's testable end-to-end without the LLM in the loop.

## First live invocation found two bugs

The first production run was PR [#722](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/pull/722) — a hyperflow submission from an external contributor with 8 new skills. The run immediately surfaced two design flaws the test suite didn't catch, because the test suite ran against toy data and missed the production edge cases.

**Bug 1: empty-changeset explosion.** PR #722 touched `sources.yaml` only — no `plugins/` paths. The changeset filter triggered a fallback I'd written without thinking: "no plugin paths matched" → pass through *all* results → generate comment body for ~400 skills.

GitHub's comment API caps bodies at 65,536 characters. The post failed silently. The deterministic verdict was correct, but the comment never landed and the Slack ping fired with an incomplete reference. Confusing signal to the operator. Real production bug caught by the first real-world input.

**Bug 2: pointless comments.** Even after fixing Bug 1, every infrastructure or documentation PR would still get a "PASS: no plugin paths matched" comment. That's accurate — nothing happened. But it's signal without value: visible noise on every non-plugin PR. Noise erodes signal over time. After a week, the operator stops reading the comments.

PR [#724](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/pull/724) fixed both in 50 lines net (+50/-163 after deleting the dead fallback). Three changes:

- Empty changeset → emit empty filtered list (the classifier reports "no plugin paths," doesn't dump everything).
- Skip the Post Comment and Slack Notify steps entirely when `steps.diff.outputs.count == '0'`.
- Cap the per-skill table at 100 rows and truncate the body to 65,000 characters with a clear marker.

Empty changeset → no comment, no ping. The deterministic signal has preconditions. When those preconditions aren't met, the system stays silent. No noise. No confusion.

The system found its own design flaws on first contact with reality. That's not a weakness of the never-block contract — that's the whole point. The deterministic classifier is safe enough to trust on its first invocation. The advisor runs under safe conditions. When reality violated the conditions, the system degraded gracefully and the operator fixed the precondition. Not the core logic. The core logic was never wrong. The assumptions feeding it were.

## The spec was invisible — fix the surface

PR #722 was thoughtful. The contributor read CONTRIBUTING.md, followed the issue template, and wrote skills that made technical sense. All 8 were structurally sound. And all 8 were missing every one of the 6 marketplace-required frontmatter fields plus every one of the 7 body sections.

The expectations were buried in `000-docs/6767-b-SPEC-DR-STND-claude-skills-standard.md` — the Global Master Standard for Claude Skills, v3.6.0, with the 100-point rubric and source citations against Anthropic + AgentSkills.io. Authoritative. Comprehensive. Invisible to contributors.

No link from the PR template. No mention in CONTRIBUTING.md. No signpost in the plugin-submission issue template. The deterministic classifier caught it all as D and F grades and reported each one. That's correct — the validator is working. But the feedback loop was broken: the spec was invisible to contributors. Invisible requirements produce work that looks wrong until you read the fine print. By then you've already written it.

PR [#725](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/pull/725) surfaced the spec on three contributor surfaces:

- **CONTRIBUTING.md** — new "Read the spec before you start" callout above "Before You Submit," with the distilled requirements and direct links.
- **`.github/PULL_REQUEST_TEMPLATE.md`** — top-of-template now points to CONTRIBUTING and to the spec. Also replaces stale "auto-review bot" phrasing that referred to the deleted Gemini workflow.
- **`.github/ISSUE_TEMPLATE/plugin-submission.yml`** — adds a markdown description block with the spec callout and replaces 5 generic checkboxes with 7 spec-aware ones covering the real validator gates.

Also corrected two stale strings while I was there: "Gemini 2.5 Pro will post a review" → "the PR Pre-screen workflow," and the example switched from the deprecated `--enterprise` flag to the current `--marketplace` flag.

The validator still grades the same way. The standard didn't move. But now the spec isn't a surprise buried 8 directories deep; it's the first thing you see when you open a pull request. The expected drop in D/F submissions isn't a change to the validator. It's a change to the surface contributors actually touch.

The five-PR arc — [#719](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/pull/719), [#723](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/pull/723), [#721](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/pull/721), [#724](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/pull/724), [#725](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/pull/725) — is a case study in what never-block lets you do: ship something small, watch it collide with reality, and fix the collisions without unwinding the core. The deterministic classifier didn't change between Phase 1 and the hot-fix. The Groq advisory didn't change either. The preconditions and the surface visibility did, because reality demanded it.

Deterministic first, LLM second, never-block contract always. That's the formula that lets you retire the old system on the same day and trust the replacement.
