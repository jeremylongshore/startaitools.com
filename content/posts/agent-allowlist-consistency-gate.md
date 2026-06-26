+++
title = 'An Agent Allowlist Is a Comment Until a Gate Checks the Body'
slug = 'agent-allowlist-consistency-gate'
date = 2026-06-18T08:00:00-05:00
draft = false
tags = ["claude-code", "agents", "validation", "quality-gates", "ci"]
categories = ["AI Engineering"]
description = "A Claude Code agent's tools list is a runtime gate, not a comment. A body-vs-allowlist consistency check in CI took 317 agents to A-grade in one sweep."
+++

A Claude Code agent declares the tools it is allowed to use in its frontmatter. That `tools` line looks like documentation — a courteous note about what the agent touches.

It is not documentation. It is a runtime allowlist: tools not listed are *blocked at runtime*. The agent can write all the instructions it wants in its body about calling some MCP tool; if that tool isn't in the allowlist, the call never happens.

Which means a Claude Code agent has two surfaces that can disagree. The frontmatter declares a capability. The body exercises a behavior. Nothing in between proves they match. And because the allowlist is enforced at runtime, a mismatch isn't a cosmetic doc-drift bug — it's a latent failure. An agent that invokes a tool it forgot to declare doesn't error loudly. It silently can't do its job.

At one agent, you catch that by reading the file. This repo ships **317** of them. This post is about the gate that made all 317 declare the truth about themselves in one automated sweep, instead of someone hand-auditing 317 files and hoping.

## The problem: a runtime gate that nobody checked against behavior

Every agent file is two parts. Frontmatter — `name`, `description`, `tools`, `model`, and the rest — and a body, which is the prose that actually instructs the agent what to do and which tools to call. The `tools` field is the allowlist, and the allowlist is load-bearing in a way a comment never is: the runtime reads it and blocks anything not on it.

So there are exactly two ways for the frontmatter and the body to fall out of sync, and both are silent:

- **The body uses a tool the allowlist doesn't grant.** The agent's prose says "collect the analytics with the umami tools," but `tools` lists only `Read`. At runtime every umami call is blocked. The agent is shipped, looks fine, validates against a frontmatter-only schema, and cannot perform its one job.
- **The allowlist grants a tool the body never uses.** Over-declaration. The agent claims privilege it doesn't exercise. The allowlist is now lying in the other direction — it overstates the blast radius of the agent, which is exactly the wrong thing for an allowlist to do.

Neither of these shows up in a frontmatter-only validator. You can check that `tools` is a well-formed list of real tool names and still have an allowlist that has nothing to do with what the agent does. The schema was green and the agents were wrong, and the only thing that would have caught it was a human reading each body against each allowlist — which does not scale to 317.

The fix is the same move I keep coming back to: a declared property is only worth what the check that compares it to behavior is worth. Without that check, the allowlist is a comment that also happens to block your runtime calls — the worst of both, because being wrong is invisible until the agent fails quietly in front of a user.

## The approach: a kernel-strict gate that lands with the fleet

The check didn't arrive in one commit. It arrived as a schema-versioned progression — `3.9` to `3.10` to `3.11` — where each step tightened what "a valid agent" means, and the fleet was dragged up to meet each new bar in the same branch that raised it.

The version number isn't decoration either. Every change to what the validator accepts bumps `SCHEMA_VERSION` and lands a changelog entry, so "the day the agent contract got stricter" is a diff with a number, not a vibe. When an agent that passed last month fails today, the version delta tells you which rule moved and where it was signed off. A quality gate that changes silently is its own kind of drift; versioning the gate is how the gate stays auditable while it tightens.

**Schema 3.10.0 — flip the gate from lenient to kernel-strict.** The agent validator used to require almost nothing: `name`, `description`, and a warning if you used a banned field. That's a gate in name only. 3.10.0 flipped it to a two-layer required set, all of it *errors* at every tier (agents aren't tier-gated the way skills are):

- **The kernel floor — 8 fields:** `name`, `description`, `tools`, `model`, `color`, `version`, `author`, `tags`. This is the `@intentsolutions/core` agent-definition required set, consumed from the kernel with an inline fallback mirror so the validator and the spec can't drift apart.
- **The enterprise live set on top:** `disallowedTools` / `skills` / `background` on every agent, plus `hooks` / `mcpServers` / `permissionMode` on standalone agents (those three are plugin-level and ignored at runtime on a plugin agent, so they're only required where they mean something).

It also promoted the banned fields — `capabilities`, `expertise_level`, `activation_priority`, `type`, `category`, `when_to_use` and friends — from WARN to ERROR, and added `fable` to the model enum.

The discipline that makes this real is in the commit note: **CI goes red until the in-repo agents are remediated in the same branch.** The gate and the fleet land together. A gate you merge *before* the fleet conforms is just a broken `main` with a TODO. A gate you merge *with* a deterministic remediation of all 317 agents is enforcement from the first commit — the bar and everything held to it move in one motion.

The two-pass order matters and is worth slowing down on. The remediation that turned CI green could not also be the remediation that got things *right*, because "green" and "correct" are different bars and conflating them is how a big migration goes sideways.

So the green pass was deliberately dumb and deterministic: every agent missing a `tools` field got the full canonical tool set (a faithful default that preserved the inherit-everything behavior those agents already had), `tags` scaffolded from plugin category plus name, `version` set to `1.0.0`, a stable `color`, and empty `disallowedTools` / `skills` / `background false`. Nothing clever, nothing that required judgment per agent — just enough to satisfy the new required set so the gate could go live with a green fleet under it.

**The A-grade pass — narrow to least privilege.** *Then* a second pass took the allowlists from "technically valid" to "actually minimal." It did three things to every agent: rewrote `description` into capability plus an explicit "Use when…" plus trigger phrases; replaced the scaffolded category `tags` with at least two real lowercase topic tags; and narrowed `tools` from full-canonical to least-privilege. The result: median allowlist around five tools, and **zero** agents retaining the full ten-tool set, down from 311 inheriting all of it.

The edits were surgical — only `description`, `tools`, and `tags` changed; every body and all other frontmatter byte-identical across all 317. Splitting it this way meant the risky, judgment-heavy narrowing happened against an already-green baseline, so any regression had a single obvious cause instead of being buried in the same diff that introduced the gate.

And here's the gap that remained. After the A-grade pass, every allowlist was structurally valid *and* least-privilege — and still nothing proved any of them matched the body. Least privilege you assert by hand is just a tighter comment. A smaller allowlist that the body contradicts is, if anything, *more* dangerous than an over-broad one: the tighter you draw the grant, the more likely an honest behavior in the body falls outside it and gets blocked.

## The check: body-vs-allowlist consistency (schema 3.11.0)

3.11.0 is the step that closes the gap. `validate_agent()` stopped reading only the frontmatter and started reading the body too, then cross-checking what the body *does* against what the allowlist *grants*. The structure, paraphrased:

```python
# Illustrative — the shape of the body-vs-allowlist consistency check.
def check_agent_body_vs_allowlist(frontmatter, body):
    # Example code isn't behavior. Strip fenced ``` … ``` blocks first
    # so a tool shown in a usage snippet doesn't read as a tool call.
    body = strip_fenced_code(body)

    declared   = mcp_tools_in(frontmatter["tools"])     # mcp__server__tool entries
    fq_in_body = find_fully_qualified_mcp_refs(body)     # mcp__server__tool used in prose

    errors, warnings = [], []

    # CHECK 3 (ERROR): zero MCP tools declared, but the body calls them.
    if not declared and fq_in_body:
        errors.append("body references MCP tools but the allowlist declares "
                      "none — every call would be runtime-blocked")

    # CHECK 1 (ERROR): a specific tool the body invokes isn't on the allowlist.
    for ref in fq_in_body:
        if ref not in declared:
            errors.append(f"body invokes '{ref}' but it is not in the allowlist")

    # CHECK 2 (WARN): heuristic short-name mention, only on MCP-oriented agents.
    for name in backtick_verb_camelcase(body):
        if not matches_any_declared(name, declared):
            warnings.append(f"body mentions `{name}` (tool-call-shaped) "
                            "but no declared tool matches")

    # WARN: declared but never used — over-declared privilege / drift.
    for tool in declared:
        if tool not in fq_in_body:
            warnings.append(f"declares '{tool}' but the body never uses it")

    return errors, warnings
```

The severities are sized to the confidence, and that's the part that makes it a usable gate rather than a noise machine:

- **A fully-qualified `mcp__server__tool` reference in the body that isn't on the allowlist is an ERROR.** That string is unambiguous — it's the exact runtime name, it doesn't appear by accident, and if it's in the body and not the allowlist, the runtime *will* block it. High confidence, hard failure.
- **An allowlist with zero MCP tools whose body still calls them is an ERROR.** Same reasoning, whole-agent scale: every MCP call the agent makes is dead on arrival.
- **A backtick short-name that looks tool-call-shaped is a WARN, and only on MCP-oriented agents.** This is the heuristic, and it's deliberately timid. An earlier, broader version of this check would have flagged `getStaticProps` and every other `verbCamelCase` token in a body as a phantom tool. So the short-name heuristic is gated to agents that actually deal in MCP tools, and it only warns — because a check that cries wolf gets switched off, and a switched-off check protects nothing.

Two engineering details earn their place. **Fenced code is stripped before any matching** — a tool shown inside a triple-backtick usage example is documentation of how to call it, not the agent calling it, so it shouldn't trip the gate. And the strong signal (exact `mcp__` strings) carries the errors while the weak signal (short names) carries only warnings. Both choices come from the same instinct: a precise gate that fails hard on certainty and merely whispers on a guess is one people leave on.

## The result: one real defect, found by machine

The check ran against all 317 agents and surfaced a genuine pre-existing defect that had been sitting in the repo, green, the whole time. `data-collector.md` invoked six `mcp__umami__*` tools in its body and declared only `Read` in its allowlist.

Read that again in runtime terms: the agent whose entire purpose is collecting analytics data could not make a single analytics call. Every one would have been blocked. It wasn't doc-drift — it was a latent outage the frontmatter-only schema had no way to see. The fix was to declare the six tools, because the agent genuinely needed them.

That single catch is the whole argument for the check. One agent, wrong in a way that looked fine, in a fleet too large to read by hand, found deterministically the moment the validator was taught to compare declaration against behavior. And notice it was an *under*-declaration — the body asked for more than the allowlist granted. A privilege auditor that only worried about agents asking for too much would have walked right past it. The check has to run both directions because the silent runtime failure lives in the direction most reviewers don't think to look. Nine new unit tests pin the check's behavior; all 317 agents validate to zero agent-level errors.

| Surface | What it claims | What enforces it |
|---|---|---|
| `tools` frontmatter | the agent's allowed capability | the runtime — undeclared tools are blocked |
| agent body | the agent's actual behavior | the model, following the prose |
| **consistency gate (3.11.0)** | **declaration and behavior agree** | **CI — ERROR on a fully-qualified mismatch** |

## The principle: declared capability must be machine-checked against behavior

Strip away the specifics and this is the same boundary lesson as [an MCP server's write gate](/posts/the-api-is-the-real-boundary/). There, the client-side tool gate was UX and the server-side gate was the boundary, and the mistake was confusing the two. Here, the allowlist is a declaration and the body is the behavior, and the mistake is assuming they agree because you wrote them in the same file.

They don't agree until a check makes them. A declaration nobody verifies decays into a comment — and a comment that's also a runtime gate is a latent failure waiting for the worst moment to surface.

The move generalizes past Claude Code agents. Any place a system declares a capability separately from where it exercises it — an RBAC scope versus the endpoints it guards, a capability manifest versus the syscalls a process makes, a type annotation versus what a dynamically-typed function actually returns, an OpenAPI contract versus the handler — has this same fault line. The declaration is cheap to write and ages into a liability the day it stops matching the behavior, because nobody was checking.

The fix is never "be more careful when you write the declaration." Care doesn't survive contact with 317 files and a year of edits. The fix is a deterministic check that reads both sides and fails when they diverge — and it has to live in CI, not in a reviewer's discipline, because the whole problem is that the discipline doesn't scale. Once the check exists, the property it guards stops being a thing you hope is true and becomes a thing that can't merge while false.

Scale is what turns this from nice-to-have into non-negotiable. At one agent, the author is the auditor and the body fits on a screen. At 317, the only auditor that scales is a check in CI that reads every body against every allowlist on every push — and that's the difference between asserting your agents are correct and proving it.

## Tradeoffs

The body check is heuristic, not an AST. It matches text patterns — fully-qualified `mcp__server__tool` strings and backtick `verbCamelCase` mentions — so it cannot catch a tool invoked through a dynamically constructed string in the body, and it scopes the short-name heuristic narrowly on purpose.

That's a deliberate trade of recall for precision: a gate that throws false ERRORs gets disabled, so the certain signal fails hard and the uncertain signal only warns. Strong over complete.

Stripping fenced code means a tool that appears *only* inside an example block is invisible to the check. Acceptable, because an example isn't behavior — but worth naming, because it's the one place a real call could hide.

And the check bites hardest on MCP tools specifically, because their fully-qualified namespace makes them matchable with confidence. A plain `Bash`-vs-`Read` mismatch isn't gated the same way, since those canonical tools don't carry an unambiguous call signature in prose. That's fine by design: the MCP surface is the privileged, high-blast-radius one, and that's exactly where you want the allowlist to be provably honest.

## Also shipped

The same day, the team knowledge-base work continued on a parallel track: the qmd adapter got a native FTS5/BM25 keyword backend with no external binary, a retrieval eval harness reporting Recall@10 and nDCG@10, and SHA-256 pinning of the retrieval-model weights that fails closed if the hash doesn't match. Plus a round of CI cleanup across the plugins repo. Each is its own thread; here they're the backdrop to a day whose lead story was making 317 agents' declared tools provably match what they actually do.

---

**Related posts:**

- [MCP Server Auth: The API Is the Real Boundary](/posts/the-api-is-the-real-boundary/) — the same lesson on a different surface: the declared gate and the enforced gate are not the same thing, and confusing them is how security theater ships.
- [A Second Brain You Can Audit Beats One You Must Trust](/posts/governed-second-brain-local-first-mcp/) — replace every promise with a command that checks it, applied to a governed knowledge store.
- [Green CI Proves Nothing: Why Your Tests Gate Zero Calls](/posts/when-green-ci-proves-nothing/) — the same instinct turned on tests: a green check that verifies nothing is worse than no check at all.
