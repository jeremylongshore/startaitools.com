+++
title = 'A Reply Your Bot Loses to a Crash Is One Your User Never Got'
slug = 'crash-durable-replies-loss-proof'
date = 2026-06-24T08:00:00-05:00
draft = false
tags = ["reliability", "durability", "bots", "crash-safety"]
categories = ["DevOps"]
description = "Making every bot reply path — streaming and file-upload — crash-durable. The unglamorous reliability work that separates a demo bot from one people depend on."
+++

A demo bot answers when nothing goes wrong. A bot people depend on answers when something does.

The gap between those two is mostly invisible. It lives in the moment your bot has composed a reply, started sending it, and then the process dies — a deploy, an OOM kill, a host reboot. The user is sitting in the channel. The work happened. The answer existed. And it's gone, because it lived only in the memory of a process that no longer exists.

On June 24, 2026, the throughline of an otherwise scattered hardening day in **claude-code-slack-channel** was closing that gap for every reply path the bot has. The epic name was honest about the goal: crash-safety. The README true-up called the user-facing property by its plain name — **loss-proof replies**.

## The Thesis

Durability is a feature users only notice when it's missing. Nobody opens a channel and thinks "what a relief, my answer survived a restart." They only ever notice the silence where an answer should have been. That asymmetry is exactly why durability gets skipped: it earns no applause when it works and all the blame when it doesn't, so it loses every prioritization argument to the next shiny feature — right up until the first lost reply in front of a customer.

The fix isn't clever. It's the unglamorous discipline of making sure no reply lives *only* in volatile memory between "composed" and "confirmed delivered."

That window — composed but not yet confirmed — is where every lost reply lives. Shrinking it to zero is the entire job.

## What "Crash-Durable" Actually Means Here

The standard is at-least-once delivery across a process restart. Concretely:

1. The bot decides what to send.
2. That intent gets written to durable storage *before* the send is attempted.
3. The send runs.
4. On success, the durable record is marked delivered.

If the process dies between steps 2 and 4, a restart finds the unfinished reply and redelivers it. The user gets the answer late rather than never. The naive version — compose, send, done, with nothing written down — has no step 2, so a crash anywhere in the send is silent and permanent data loss the user experiences as the bot just not answering.

That's the whole contract. But the contract has to hold for *every* kind of reply, not just the easy one.

A bot that's durable for plain text and lossy for everything else isn't durable; it's durable-ish. In production "durable-ish" reads as "loses replies sometimes," and an intermittent loss erodes trust about as fast as a constant one — arguably faster, because the user can't predict it and stops believing any answer is final.

## Two Reply Paths, Both Made Durable

The work split along the two rich paths a reply can take.

**Streaming replies** — the token-by-token answer that updates in place as the model generates. Shipped crash-durable in [PR #254](https://github.com/jeremylongshore/claude-code-slack-channel/pull/254) (`feat(reply): make streaming replies crash-durable`).

The hard part of a stream: it has no single send moment to protect. It's a sequence of edits to a message, any one of which can be the one that dies. Durability has to cover the *resumption point* — where the stream was when the process fell over — not just the final flush. Protecting only the last write would leave a half-written answer frozen on screen with no way to know it was abandoned.

**File-upload replies** — when the answer is an artifact, not text. This landed in two deliberate parts:

- A durable building block plus design in [PR #255](https://github.com/jeremylongshore/claude-code-slack-channel/pull/255) (`durable file-upload building block + design`).
- Wiring it live in [PR #256](https://github.com/jeremylongshore/claude-code-slack-channel/pull/256) (`wire durable file-upload replies live`).

Splitting "build the primitive" from "make it the live path" is the move that keeps a risky change reviewable. The building block ships and gets tested before any user traffic crosses it, so the live-wiring PR is a small, focused diff instead of a big-bang switch nobody can fully reason about.

When both merged, the crash-safety epic closed with a one-line claim worth earning: *all rich paths durable*.

## The Details That Make It Honest

Two design findings recorded mid-flight show this wasn't a copy-paste of someone's outbox tutorial.

**A `findUploaded` contract.** Redelivering a file-upload reply naively means re-uploading the file — so a crash between "uploaded" and "confirmed" would double-post the artifact. The user gets the same file twice and learns the bot is flaky in a new direction.

The contract is the part that checks whether the upload already happened before retrying, turning at-least-once *attempts* into effectively-once *artifacts*. At-least-once delivery is only safe when redelivery is idempotent; this is where that safety gets built. Skip it and you've traded a lost-reply bug for a duplicate-reply bug, which is not progress.

**An exfil-guard on redelivery.** Redelivery replays a reply the bot decided to send earlier. If the bot's security posture changed in between — a channel locked down, a principal revoked — a naive replay would happily ship data the *current* policy forbids.

Guarding the redelivery path means a recovered reply still has to pass the gate, not ride a grandfather clause from before the crash. Durability that bypasses your security boundary isn't a feature; it's a backdoor with good intentions. The recovered reply is treated as a new send subject to today's rules, not a sealed envelope from a more permissive yesterday.

The README true-up after the epic closed put numbers on the surface area now under test: **1237 tests** and **7 acceptance primitives** backing the crash-safety and multi-agent hardening claims. The acceptance primitives matter more than the raw count — they're the named behaviors a reply must satisfy to count as durable, which is what keeps "loss-proof" from drifting back into a marketing word.

## The Rest of the Day, Briefly

This was the cleanest thread, not the only one. The same day, **agent-governance-plane** landed its Topology C egress-allowlist core — a preflight verdict plus egress policy ([PR #114](https://github.com/jeremylongshore/agent-governance-plane/pull/114)) — and reserved an `on_behalf_of` principal field for the multi-tenant authority model ([PR #116](https://github.com/jeremylongshore/agent-governance-plane/pull/116)). **claude-code-plugins** closed the remaining 8 audited bugs in its external-plugin sync pipeline. And **governed-second-brain** brought a second off-host backup live on Cloudflare R2 — the same durability instinct, one layer down: a brain with one backup is a brain with a single point of loss.

One honest aside on tooling: claude-code-plugins adopted Greptile as its AI PR reviewer in the morning and reverted to Gemini by afternoon when Greptile hit a quota pause. Adopt a tool, hit a wall, revert the same day. Not every hardening decision sticks — and the discipline is reverting cleanly rather than waiting on a paused dependency in the merge path.

## The Takeaway

A reply your bot composes but loses to a crash mid-send is, from the user's seat, identical to a reply it never composed at all. The work doesn't count until it's delivered, and "delivered" has to survive the process that produced it.

Making every reply path crash-durable — streaming *and* file-upload, with idempotent redelivery and a guarded replay — is the kind of work that shows up nowhere in a feature list and everywhere in whether people trust the thing.

It's also the work that's easiest to defer forever, because it has no demo. You can't screenshot a reply that *would* have been lost. The only evidence durability ever produces is the absence of a complaint — which is exactly why it has to be a deliberate engineering goal with named acceptance behaviors, not a thing you hope the happy path gives you for free.

Durability is a feature users only notice when it's missing. The goal is for them to never notice it at all.

## Related Posts

- [Honor the Gate When the Verdict Is Inconvenient](/posts/honor-the-gate-when-the-verdict-is-inconvenient/)
- [Stop Crying Wolf: A 3-Strike Uptime Monitor Gate](/posts/stop-crying-wolf-3-strike-uptime-monitor-gate/)
