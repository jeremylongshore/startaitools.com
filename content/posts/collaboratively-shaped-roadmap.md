+++
title = 'Four Primitives, Three Reviews: How a Contributor PR Reshaped a Roadmap'
slug = 'collaboratively-shaped-roadmap'
date = 2026-04-18T08:00:00-05:00
draft = false
tags = ["architecture", "slack", "mcp", "claude-code", "roadmap", "open-source"]
categories = ["Architecture"]
description = "claude-code-slack-channel v0.4.0 shipped a contributor PR that forced a scoping conversation. Four roadmap primitives emerged. Three parallel reviews — architect, sitrep, devils-advocate — converged on a narrower v0.5.0 than the original issues proposed. This is a case study in how collaborative review reshapes plans."
+++

## TL;DR

`claude-code-slack-channel` v0.4.0 shipped Casey Margell's `allowBotIds` PR on 2026-04-18. The merge forced a direction question the roadmap hadn't yet answered: with peer bots now able to deliver into the channel, what is the project *becoming*? Four issues were filed in response — thread-scoped sessions (#32), a declarative policy engine (#29), a threaded action journal (#30), and a bot-manifest protocol (#31). Before writing a single line of code, the project ran the four proposals through prior-art research and three independent review passes. The reviews converged on a narrower v0.5.0 than the issues proposed: ship #32 first, then #29, defer #30 with a reframed scope, push #31 to a later release conditional on external signals. This post is a case study in that process — not the roadmap itself, but how the roadmap got reshaped.

## The catalyst: a merged PR, not a committed plan

`claude-code-slack-channel` is a Slack bridge for Claude Code — one TypeScript file plus a small library, MIT-licensed, running an MCP server that lets a Slack thread stand in for the terminal. The v0.3.x line ran a single session per channel, gated outbound messages on `channel`, and keyed permission replies on an opaque `requestId`. Four keys, four scopes, no shared identifier. That was fine for a solo-maintainer tool.

On 2026-04-18 Casey Margell's PR #33 merged: `feat(gate): per-channel allowBotIds for opt-in cross-bot delivery`. The feature itself is modest — a config knob that allows specific peer bots to deliver messages into a channel. The implication is not. Once a second bot can deliver into the same channel, the following assumptions break:

- **Session identity is no longer implicit.** "The conversation" is not a property of the channel anymore; it is a property of the thread inside the channel where a specific work item is being handled.
- **The outbound gate is a confused deputy.** Hardy (1988) named this failure mode forty years ago: a process that holds ambient authority granted by multiple callers eventually forgets which caller authorised what. A channel-wide outbound gate fires the same way whether the tool call was authorised by thread A or thread B.
- **Audit is no longer monotone.** With one bot per channel, "who did what" is answerable from the stderr log. With two, the ordering of deliveries matters and the stderr log is the wrong place to store it.

Four GitHub issues went up in the hours after the merge, filed by the maintainer as a first draft of where v0.5.0 should go — not by Casey, whose contribution was the merged implementation, PR #33. None of the four had implementation PRs attached. None had been reviewed outside the maintainer's own head.

That was the moment to stop coding and do the work of thinking out loud.

## The four proposals, in one paragraph each

**#32 thread-scoped sessions.** Replace the single channel-wide session with one session per `(channel, thread_ts)` tuple. File-based state under `~/.claude/channels/slack/sessions/<channel_id>/<thread_ts>.json`. Widen the outbound gate from `channel` to the tuple. Widen the pairing key from `requestId` to `(thread_ts, requestId)`. Add an idle-timeout reaper. Security-flavoured but framed as a concurrency feature.

**#29 declarative policy engine.** Replace the hard-coded self-echo filter and permission-reply-shaped-text drop with an `access.json` policy array. Three decision types: `auto_approve`, `deny`, `require` (with N-of-M approvers). First-match-wins evaluation. Described as a UX fix for notification fatigue.

**#30 threaded action journal.** Post every tool call, every permission decision, and every delivery as a threaded Slack reply. Three verbosity tiers: `off`, `compact`, `full`. Pitched as the compliance-grade audit artifact for SOC 2 / CISO review.

**#31 bot-manifest protocol.** A pinned Slack message in a standard format that advertises a bot's capabilities to peer bots — "here is what I do, here is what requires approval." Two new MCP tools, `read_peer_manifests` and `update_my_manifest`. Pitched as the standards-definition play: if someone is going to define a Slack agent manifest, let it be us.

Read at face value, the four feel like a coherent v0.5.0. They all touch the same code paths. They reference each other. They form a tidy four-quadrant picture: *who is working* (sessions), *what is allowed* (policy), *what happened* (journal), *who else is here* (manifest). Symmetric. Almost suspiciously so.

## Phase 0: preflight consistency audit

Before any research went out, a preflight pass audited what was already shipping against what the issues assumed. The result: **four critical drifts** between the in-flight roadmap and the code that merged the same day.

- **Version drift.** The Explore agent's earlier deep-dive notes were recorded against v0.3.1. The roadmap issues were still citing v0.3.1 internals. v0.4.0 had shipped hours earlier. Line counts, function locations, and one function *signature* (`assertSendable` now takes three arguments — `filePath`, `inboxDir`, `allowlistRoots` — and resolves symlinks with `realpathSync`) had changed.
- **"Casey's PR" was Casey's *issue*.** The roadmap mention of "Casey's PR #27" was wrong twice over: #27 is an issue, not a pull request, and the implementation (PR #33) was already merged. The thesis "Casey's PR forced a direction question we're still answering" needed reframing to "Casey's work *landed* and four follow-on proposals were filed that build on the merged foundation." Stronger story, not weaker.
- **Every line-number citation was stale.** `server.ts` was 1,092 lines at v0.4.0, not the 1,071 the earlier agent had noted. `lib.ts` was 546, not 504. Every `file.ts:N` reference had to be re-grepped.
- **Precursors already shipped.** Two of the four primitives had precursor behaviour already in v0.4.0: the triple-check self-echo guard plus the permission-reply-shaped-text drop is *hard-coded* policy (the #29 story), and the `[slack] bot message delivered` stderr line is a one-channel audit stream (the #30 story). The issues read as greenfield; they are not. That is a framing bug in the roadmap text, not a scope bug, but it matters for honest writing.

The preflight caught the things that would have embarrassed a published article. It also changed the thesis. The story isn't "four primitives need to exist." It's "two exist as ad-hoc code and want to be lifted into configuration; two are genuinely new."

## Phase 1: four research briefs against forty years of prior art

Each primitive got its own brief, scoped to two questions: what does the existing literature say about this class of system, and what failure modes has the literature catalogued that the issue doesn't mention? Semantic Scholar, DOI lookups, canonical project docs. Thirteen verified sources for sessions; eleven for policy; comparable for the other two. No citations on title alone — each paper verified against the Semantic Scholar record before it could appear in a brief.

The briefs do not rehearse novelty. They check whether the proposals inherit the right lessons from work that has already happened.

**Sessions (#32) inherits from:** Honda, Vasconcelos, and Kubo (1998) on session types as a linear-resource type discipline; Armstrong (2003) on let-it-crash supervision trees; Bernstein et al. (2014) on Orleans virtual actors and the activation/deactivation tradeoff; Liu et al. (2024) on "lost in the middle" context degradation; Hardy (1988) on the confused deputy; Saltzer and Schroeder (1975) on least privilege. The proposal's design choices — file-keyed identity, idle eviction, widened pairing key — map cleanly to these. The gap the issue doesn't address: what does the session reaper do with an *in-flight* tool call? Armstrong's answer (a quiescence protocol, defined termination semantics, a supervisor that decides restart/escalate/ignore) is forty years old and absent from the issue text.

**Policy (#29) inherits from:** OASIS XACML (2013) for combining algorithms; NIST SP 800-162 (Hu et al., 2014) for ABAC semantics; OPA (Open Policy Agent Project, 2024) for the decoupled-evaluator reference design; CWE-22 (MITRE, 2024) for path-prefix canonicalization; CNSSI 4009 / NIST (2024) on two-person integrity; Greshake et al. (2023) on indirect prompt injection bypassing rule layers entirely. The `first-applicable` combining algorithm the issue picks is order-sensitive — a broad `auto_approve` at line 3 silently preempts a narrow `deny` at line 20. XACML encountered that lesson fifteen years ago and named combining algorithms specifically to address it. The issue does not propose a load-time linter for rule shadowing.

**Journal (#30) inherits from:** Schneier and Kelsey (1999) on hash-chained audit logs for untrusted-machine forensics; Haber and Stornetta (1991) on trusted-anchor timestamping; Fowler (2005) on event sourcing as command + event stream + projection; Dapper (Sigelman et al., 2010) on adaptive sampling. The brief is the most honest of the four: Slack threads are *editable and deletable* by anyone with retention authority in the workspace. Calling the Slack thread "the audit trail" is a category error. A compliance-grade journal requires hash-chained append-only storage *outside* Slack. The Slack thread is a user-visible projection of that store. The issue's SOC 2 framing is overclaiming.

**Manifest (#31) inherits from:** Miller (2006) on object capabilities and the name-versus-reference distinction; Felt et al. (2011) on the Android over-permissioning pattern; Singh (2000) on why KQML and FIPA ACL failed (standards-definition without cryptographic binding); Google A2A (2025) on signed Agent Cards at `/.well-known/agent-card.json`. The brief is also honest: pinned Slack messages are mutable by any non-guest channel member. A2A solved the authenticity problem with signatures; a pinned message cannot carry one. And a manifest that is peer-controlled untrusted text must never feed into policy decisions — that reintroduces the grant-from-claim error Miller spent a career warning about.

Four briefs, each one both endorsing the direction and naming the specific gap the issue elides. The research phase's contribution wasn't ratification; it was calibration.

## Phase 2: three parallel reviews, each with a different posture

With the briefs in hand, three reviews ran against the same inputs. Each had a narrow remit. None saw the others' output until all three were done.

### The architect review: "does the set compose?"

Its thesis: three of the four primitives quietly converge on the same identifier — `(channel, thread_ts)`. #32 makes it the session key. #30's journal entries are threaded replies keyed off `thread_ts`. #29's multi-approver `require` bucket is per-request inside a thread. #31 does *not* live at that layer: a bot manifest is channel-scoped, advertises agent-wide capability, and must be severed from access control. "Advertisements are not grants" (Miller 2006) is the invariant that keeps #31 from corrupting the other three.

The architect's strongest call was on sequencing. The roadmap's implied order (#33 → #29 → #32) gets it backwards. **#32 should ship first.**

Three reasons. First: isolation before authorization. The v0.4.0 outbound gate is a pre-existing confused-deputy bug (Hardy 1988), not a missing feature. Shipping a policy engine on top of a channel-scoped gate layers ABAC on top of a known security hole. The policy rules would be correct per spec and still allow cross-thread leakage because the underlying authority is too broad. Second: schema-bump risk. If `(channel, thread_ts)` becomes the session key after #29 ships, every `match` predicate in every already-deployed policy will want to gain an optional thread-scope predicate. That is a schema migration forcing every deployment to edit its `access.json`. Doing #32 first means #29 is born thread-aware. Third: #32 unblocks the most downstream work. #30 attaches to threads; #29 gains value from thread-scoped policies; #31 is independent either way.

The architect also named **three missing companion primitives** the roadmap didn't declare:
- Verified-identity layer for approvers — NIST two-person-integrity requires *verified* identity, not just display-name dedup.
- Policy-evaluation observability surface — OPA's posture is that decision auditability is *co-primitive* with decision evaluation. #29 pushes that into #30; #30's verbosity tiers were designed for tool I/O, not decision traces.
- Session-reaper fault-containment protocol — Armstrong's supervision-tree quiescence is the exact primitive #32 needs and doesn't name.

### The sitrep review: "is this actually shippable?"

Its thesis, in one line: over-engineered for v0.5.0.

The bandwidth math: forty-five new tests across four primitives, each touching either the gate, the permission relay, or the session model. Five to seven weeks of evenings for a solo maintainer even if everything goes smoothly. It will not go smoothly — thread-scoped sessions (#32) require a rewrite of session identity that touches the permission relay, the outbound gate, and the pairing-key scheme simultaneously. Once #32 lands, #29 and #30 both need to be re-read against the new session boundary. Ordering matters and the sitrep agrees with the architect that #32 must lead.

Its scope call: **ship v0.5.0 with #32 + #29 only. Defer #30 to v0.5.1 with a narrower frame. Defer #31 to v0.6.0 conditional on A2A adoption or a Slack signed-message primitive.**

The sitrep's double-down was the interesting part. It argued that #32 is the primitive where *expansion* unlocks second-order capability — and that the expansion worth investing in is *supervised* thread sessions with explicit fault containment. The session reaper isn't a TODO; it's the load-bearing architectural primitive. Each thread session runs under a supervisor that owns the state file. Tool calls register with the supervisor as in-flight work before they start. Eviction is a two-step protocol — quiesce (refuse new work, wait for in-flight), then drop — not a fire-and-forget `rm`. The emergent capability is *session migration*: once sessions have explicit supervisors and the state file is the sole source of truth (Orleans grain pattern per Bernstein 2014), a session can be evicted from one process and resumed in another. That is the step from "Slack bot" to "Slack-fronted agent runtime."

The sitrep also flagged four project-level risks the research briefs couldn't have caught because they're about the *project*, not the primitives: bus-factor concentration (the integration layer is under-tested and lives in the maintainer's head), platform lock-in drift (every primitive's naming is Slack-specific), ecosystem-competition moat (the permission-relay idea is now public; others will ship equivalents in six to twelve months), and **roadmap-issue-as-spec drift** — each of #29–#32 is sixty to a hundred lines of specification and is being treated as both an RFC and a design doc without the budget for either. That last risk matters beyond this project; it's the one I come back to in the closing.

### The devils-advocate review: "what is the strongest attack on the framing?"

Its thesis: drop the word *category*. The four primitives are not a new architectural category; they are the generic MCP-host deployment checklist rendered on Slack. Every primitive maps one-to-one onto existing shipped work: MCP spec session semantics (#32), XACML/OPA ABAC (#29), Dapper/OpenTelemetry adaptive-sampled audit (#30), Google A2A signed Agent Cards (#31). An article that elevates "same four primitives, rendered on Slack" to "a category of its own" is claiming a medium as a category, like claiming "email-as-a-control-plane" was a category in 2008. Platforms are not categories.

The review walked a retreat sequence: if any attack lands, fall back rather than abandon the thesis. First fallback — "new category" → "unusual composition." Second — "unusual composition" → "coherent stance; primitives reinforce each other." Floor — "coherent stance" → "documented direction decision." It recommended planting the flag at the second fallback.

It also named the one defensible novelty if the category claim *had* to be defended: **co-location.** MCP sessions are invisible to end users. OPA decisions are invisible. Dapper spans live in a backend UI nobody opens. A2A Agent Cards are machine-readable. The four primitives in this project are co-located on the chat thread the humans are already reading. The distinguishing invariant isn't any primitive in isolation; it's that all four fold into one human-visible surface. Slack is an *existence proof* of the pattern, not the category name.

## Where the three reviews converged

Three reviewers, three different postures, substantial agreement:

| Question | Architect | Sitrep | Devils-advocate |
|---|---|---|---|
| Does the set compose? | Yes (3+1); #31 is orthogonal | Yes but too much for one release | Yes and unremarkably so |
| Ship order? | #32 first (security) | #32 first (bandwidth) | (out of scope) |
| Ship scope for v0.5.0? | #32 + #29 cleanly; #30 and #31 can wait | #32 + #29 only | Prospective until something ships |
| Weakest primitive? | #30 as compliance claim; #31 as peer | #31 (no cryptographic binding) | #31 (A2A already solved this with signed cards) |
| Biggest missing piece? | Session-reaper supervision protocol | Session supervisor + ARCHITECTURE.md | Concession of prior art |

Where they disagreed, the disagreements were useful. The architect wanted a verified-identity primitive added to the set. The sitrep wanted the set *cut*, not extended. The devils-advocate wanted the framing narrowed so whatever shipped didn't carry overreaching rhetoric. Three pressures pulling in different directions, all constraining the same design — that's the triangulation. One observation the table can't carry: both the architect and sitrep — the two reviews that engaged implementation primitives directly — independently landed on the session reaper and supervision protocol as the project's single genuine engineering-originality bet. Two independent signals with different postures is a stronger convergence than any one opinion.

## What the process produced

Two primitives for v0.5.0, one deferred, one held.

**v0.5.0 is #32 and #29.** Thread-scoped sessions ship first, with an explicit supervisor — file-keyed state, widened outbound gate and pairing key, and a quiescence protocol (activate, quiesce, deactivate) for the reaper so that eviction is not a race against in-flight tool calls. The policy engine ships second, born thread-aware: `access.json` carries optional thread-scope predicates from v1, path-prefix rules canonicalize before comparison, a load-time linter flags rule-shadowing, and multi-approver `require` ties to verified Slack `user_id` rather than display name. Two documents get written before any code — `ARCHITECTURE.md` naming the integration-layer invariants, and `SECURITY.md` naming the four-principal model (session owner, Claude process, human approver, peer agent) — so the privilege-confusion bug is headed off at the definitional layer rather than discovered later.

**v0.5.1 is #30 with the compliance claim dropped.** The journal is operator visibility, not audit forensics. If forensic weight is ever needed, hash-chained storage outside Slack is a separate feature and a different ticket. An `--audit-log-file` flag writing JSON-lines locally can ship as a v0.4.1 patch in the meantime as the precursor primitive.

**#31 is held, conditional.** It waits for A2A adoption to clarify or for Slack to expose a signed-message primitive that a manifest can actually bind to. Until then, peer bots communicate by @-mention and natural language, exactly as Casey's original issue #27 use case described. Nothing in #32 or #29 depends on #31.

In one sentence, what v0.5.0 pitches: *two engineers can run independent investigations in the same channel, and the operations during those investigations follow configurable rules instead of firing an undiscriminated approval prompt for every tool call.* Coherent. Narrower than four primitives. Stronger story.

## What this case study is actually about

The roadmap is not the interesting artifact. The *process* is.

Three things went right that are worth naming:

**The preflight ran before the research did.** An hour of consistency checking caught four drift errors — version, PR-vs-issue, line numbers, precursor acknowledgement — any of which would have discredited the later analysis if they'd surfaced mid-draft. Running preflight before research is cheap. Running it after is how published roadmaps age badly.

**Three reviews ran in parallel, with different postures.** One review is an opinion. Two is a debate. Three orthogonal reviews — one on architectural composition, one on delivery feasibility, one on rhetorical defensibility — produce a triangulated answer that any single reviewer misses. The architect cared about layering. The sitrep cared about bandwidth. The devils-advocate cared about the narrator's credibility. No single one of them, alone, would have arrived at "ship two, defer one, push one conditional." All three, together, made that the obvious call.

**The research phase graded against prior art, not novelty.** Forty years of session-types, supervision-tree, XACML, hash-chained-audit, and capability-system literature is the part of this space that is *done*. The project's contribution is not to rediscover any of it. It is to inherit the right lessons and to name the failure modes the literature has already catalogued. That is a narrower kind of work than "defining a category," and it is the honest kind.

One thing went wrong that is worth naming too: the roadmap issues as filed were being treated as both RFCs and design docs without the budget for either. Each issue was sixty to a hundred lines of specification. That is a lot of text to carry without a review pass. The fix is not to write fewer issues — it is to treat an issue as a prospectus and require a short design document (two hundred words per primitive is enough) *between* filing and coding. That design document is where the reaper's quiescence protocol gets named. That document does not exist yet for #32. It will, before any code lands.

The most useful thing you can do to a roadmap before writing code against it is attack it from three angles and see what survives.

## Acknowledgements

Casey Margell's PR #33 was the catalyst. @jinsung-kang has also contributed merged work to the project. The research briefs cite thirteen peer-reviewed sources for sessions, eleven for policy, and comparable counts for journal and manifest; full bibliographies live in the project's design-doc directory alongside the implementation when it ships. The three review postures — architect, sitrep, devils-advocate — are reusable; anyone writing a roadmap can run the same three passes on their own proposals. Do it before you publish. Do it before you code. The cost is a few evenings. The payoff is a v0.5.0 you can actually ship.
