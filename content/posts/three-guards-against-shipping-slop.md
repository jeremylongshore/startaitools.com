+++
title = 'Three Guards Against Shipping Slop'
slug = 'three-guards-against-shipping-slop'
date = 2026-05-12T08:00:00-05:00
draft = false
tags = ["partner-engineering", "code-review", "quality-gates", "engineering-discipline", "slop-defense", "mcp"]
categories = ["Technical Deep-Dive"]
description = "How three review guards — adversarial pre-flight, empirical verification, post-delivery sweep — catch slop shipping to partners. Seven PRs, one day, zero embarrassment."
+++

Seven pull requests landed on a single partner fork in one day, alongside half a dozen upstream issue filings and the closeout of a prior audit round. That is a velocity that produces slop by default. The slop did not ship — not because the work was careful, but because three distinct guards were standing between the work and the partner, each catching a different class of failure the other two would have missed.

This post is about those three guards. Not about the velocity. The velocity is the symptom. The guards are the system.

The engagement is Kobiton, a mobile device cloud partner running an MCP server at `api.kobiton.com/mcp`. The day's output included a hooks bundle, an agents addition, a server-side audit slate, and a consistency cleanup — PRs #39 through #45 on the fork. Any one of those, shipped wrong, would have cost partner credibility. None shipped wrong. Three guards caught the slop at three different moments in the workflow.

## Guard 1: Adversarial pre-flight on the hooks bundle

Before the hooks bundle PR went up, three specialist subagents ran in parallel against the raw artifact:

- `code-reviewer`
- `security-auditor`
- `test-automator`

The output was not gentle. Six BLOCKERs and eight HIGHs surfaced between the three reviewers. The PreToolUse envelope shape was wrong. The credential-handling strategy was unsafe — hooks were going to make authenticated API calls from inside a Claude Code session, with a credential surface that nobody had thought through. The `appId` parameter was an SSRF vector. Error responses echoed PII. There was a ReDoS in input parsing. `CLAUDE_PROJECT_DIR` vs `CLAUDE_PLUGIN_ROOT` was confused throughout. The shell-vs-exec form choice was wrong for several handlers. TLS and timeout defaults were missing entirely.

The bundle was BLOCKED from submission. Not "submit with caveats" — blocked, with a re-review date of 2026-05-21.

The hooks PR that actually landed — #44 — was a redesigned advisory-only bundle. No API calls from hooks at all. The credential surface that produced half the BLOCKERs was eliminated by design, not patched. 28 new tests passed. The artifact that shipped was a different artifact than the one that was queued to ship.

The transferable insight is about reviewer parallelism. A security reviewer reading after a code reviewer reads a different file than the one the code reviewer read. The code reviewer has already mentally cleared the surface; the security reviewer inherits that clearance silently. Running the three reviewers in parallel against the raw artifact — each one seeing the actual code, none of them inheriting another reviewer's frame — is what surfaced the BLOCKERs.

Serial review with the same three personas would likely have caught fewer issues — this is a structural inference from how reviewer framing inherits, not a measured comparison. The parallelism is load-bearing. It is also adversarial by construction: each reviewer is graded on what they find, not on consensus with the others.

## Guard 2: Empirical verification over inference on the server-side audit

The R3 server-side audit slate for Kobiton — the set of findings about what the MCP server does and does not implement — started as a documentation review. Read the public docs, reason about the MCP protocol, file findings about apparent gaps.

Several DRAFT findings carried inference-grade language. "Likely missing." "Probably not declared." "Appears to omit." That language is a tell. Inference-grade findings filed to a partner are slop with a hedge attached. The hedge does not protect anyone — the partner still has to spend cycles refuting wrong claims.

The work shifted from inference to probe. Using the `getCredential` MCP tool to obtain a real Kobiton API key, the audit executed raw authenticated probes against `api.kobiton.com/mcp`:

- `initialize`
- `resources/list`
- `prompts/list`
- `resources/templates/list`

The verbatim server response to `initialize`:

```
protocolVersion: 2025-03-26
capabilities: {"tools": {}}
serverInfo: {"name":"kobiton","version":"1.0.0"}
```

Resources, prompts, and templates list each returned JSON-RPC error `-32601` (method not found).

Six findings flipped from "likely missing" to verified against a server response: F36 (instructions field absent), F37 (resources capability absent), F38 (prompts capability absent), F42a (tools.listChanged not declared), F42b (resource subscriptions not declared), plus a newly-discovered protocol version lag — the server declares `2025-03-26` against a current spec of `2025-11-25`, two releases behind.

The OAuth retraction is the load-bearing example for this guard, and it is worth describing in detail because the retraction is more valuable than the original finding would have been.

Bundle 3 DRAFT claimed Kobiton was missing three things: RFC 9728 (Protected Resource Metadata), RFC 8414 (Authorization Server Metadata), and `WWW-Authenticate` response headers entirely. Those claims were built from doc review. They were wrong.

The empirical probe showed all three were already implemented. Kobiton's MCP server has OAuth 2.1 with PKCE S256 and dynamic client registration. The well-known metadata endpoints respond. `WWW-Authenticate` is emitted. The original Bundle 3 finding — filed as a serious gap — was wrong on its central claims.

The Bundle 3 issue body got rewritten. The wrong claims were withdrawn. The bundle was narrowed to two real, verified gaps: F41d (the `resource_indicators_supported` field is undeclared) and F41e (the `WWW-Authenticate` header is inconsistent on bad-token 401 responses). The issue body included an explicit sourcing-discipline paragraph: here is what was wrong, here is why it was wrong, here is the corrected scope.

The transferable insight is about retraction economics. The credibility cost of an unwithdrawn wrong claim compounds — every future finding from the same audit gets read through the lens of "they got OAuth wrong, what else did they get wrong?" The credibility cost of an explicit retraction is small and decays fast. The partner reads the retraction, registers that the audit corrects itself, and the next finding gets evaluated on its merits.

Inference-grade findings shipped to partners are not "drafts" or "starting points." They are slop with a hedge. If the system can produce a verbatim server response, the audit has to produce one before the finding ships.

## Guard 3: Post-delivery consistency sweep against fork main

After PRs #39 through #44 landed, the work ran `/validate-consistency` against the fork's `main` branch. Each PR had been internally consistent. The sweep returned seven findings anyway — all of them cross-PR drift.

Critical findings, two:

- `AGENTS.md` was missing from the fork root, but the agents and hooks PRs both referenced it as if it existed.
- `package.json` was still at version `1.0.0` while `plugin.json` had been bumped to `1.0.2`. The version bump happened on one surface but not the other.

Warning findings, four:

- The README had no section for the new `agents/` directory introduced by PR #41.
- The README had no section for the new `hooks/` directory introduced by PR #44.
- `SKILL.md` claimed Node `>=18` while CI was already pinned to Node `20`.
- A fork-side issue reference read just `#28` with no owner — ambiguous between upstream and fork.

Info finding, one:

- `package.json` and `marketplace.json` had divergent descriptions.

All seven resolved in PR #45, a single cleanup pass. `AGENTS.md` got created at the fork root, 72 lines, every claim sourced. `package.json` bumped to `1.0.2` to match `plugin.json`. README gained sections for both `agents/` and `hooks/`. `SKILL.md` Node compatibility was updated to match CI. The bare `#28` was disambiguated to `jeremylongshore/automate#28`. The two manifest descriptions were aligned.

None of those seven findings would have been caught by reviewing any individual PR. Each PR was internally consistent. The drift only existed in the relational space between the PRs — file A references file B that does not exist yet, version X on surface 1 lags version Y on surface 2, description in manifest M diverges from description in manifest N.

The transferable insight is about review topology. Pre-submission review operates on one artifact at a time. Cross-artifact drift is structurally invisible to that frame. Running a consistency sweep as the closing move of the day catches a class of slop that pre-submission review cannot catch by design.

The sweep is cheap. The cleanup PR is small. The slop it prevents is the kind partners notice quietly and never mention — the README that does not describe what the repo contains, the version numbers that disagree with themselves, the references to files that do not exist. Quiet slop is the most expensive kind because the partner does not file a bug; they just lower their estimate of the engagement.

## What three guards do not catch

These three guards target three specific failure classes. The pre-flight guard catches surface flaws in the artifact being shipped. The empirical verification guard catches inference-grade claims about external systems. The post-delivery consistency guard catches cross-artifact drift.

None of the three catches bad strategic choices. If the underlying decision to ship an advisory-only hooks bundle — rather than no hooks at all, or rather than blocking hooks with a serious credential design — was wrong, the guards would not flag it. They would clear a well-built version of the wrong thing.

None of the three catches architectural drift over weeks. All three operate on a single day's window. A long arc of individually-consistent decisions adding up to a wrong system needs a different mechanism — typically a periodic architecture review or a deliberate retro, neither of which fits inside a daily ship cycle.

None of the three catches bad communication with the partner. The guards catch wrong claims, not wrong tone, wrong cadence, or wrong escalation. A correctly-filed finding delivered with the wrong framing to the wrong person at the wrong moment is still a credibility hit. That problem lives outside the guards.

The guards are necessary, not sufficient. They eliminate a category of public embarrassment; they do not produce good engineering. Good engineering happens upstream of the guards, in the choices about what to build and what to file. The guards make sure that the choices, once made, ship in a defensible form.

## What the day actually demonstrated

Seven PRs in a day on a partner engagement — with upstream filings and a prior audit round closing out in parallel — is a velocity that produces slop by default. That is the baseline. Velocity without a system underneath it is the slop pattern.

The slop did not ship today because three different mechanisms caught three different classes of error at three different moments. The pre-flight guard caught the hooks bundle before submission and forced a redesign that eliminated the credential surface entirely. The empirical verification guard caught the inference-grade OAuth claims before they shipped and converted the bundle into a narrower, defensible scope with an explicit retraction. The post-delivery consistency guard caught seven instances of cross-PR drift after the PRs landed and resolved them in a single cleanup pass.

The retraction is worth a second mention. Withdrawing wrong claims with an explicit sourcing-discipline paragraph is the kind of artifact that builds long-term credibility with a partner more than a perfect first submission would. A perfect first submission demonstrates competence. A retraction demonstrates a working error-correction loop. Partners optimize for working error-correction loops because they assume errors will happen — what they care about is what happens after.

This is the system. Not the velocity, the system underneath the velocity. The velocity is downstream of the system, not the other way around. Seven PRs in a day is safe if the three guards are running. Seven PRs in a day without the guards is a slop event waiting to be discovered by the partner — usually quietly, usually without a bug report, usually as a downward revision of trust that nobody articulates.

The lesson is not "ship faster." The lesson is "build the guards first, then the velocity is allowed."
