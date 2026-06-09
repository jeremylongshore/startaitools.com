+++
title = 'Chapter 2 — Making Agents Reliable on Real-Device Clouds'
slug = '02-making-agents-reliable-on-real-device-clouds'
date = 2026-06-09T07:00:00-05:00
draft = false
weight = 2
+++

> **Chapter 2 of 3** in [Agent-Native Mobile Testing](/features/agent-native-mobile-testing/). The canonical version of this chapter was published on Kobiton's engineering blog: **[Making Agents Reliable on Real-Device Clouds](https://kobiton.com/blog/make-agents-reliable-on-real-cloud-devices/)**. This page adds the series connective tissue and points you there for the full write-up.

**TL;DR** — Chapter 1 found the gaps an `AGENTS.md` should close: lifecycle invisibility, endpoint compatibility, the cooldown window where a device reports `is_online=true` but can't take a session yet. Chapter 2 builds the reference implementation that closes them. The reliability problem on a real-device cloud isn't the API calls — it's the **partial-failure moments that emerge between** MCP tool calls. The fix is making those seams legible: three task-specific agent definitions, four advisory hooks, and platform limitations documented as a contract rather than discovered the expensive way.

---

Chapter 1 ran a 5-device parity sweep through [`kobiton/automate`](https://github.com/kobiton/automate) and came away with a list of operational facts that an agent would otherwise learn by getting burned — which Appium log endpoints work, what "online" actually means, how long a device sulks after `deleteSession`. The conclusion was that those gaps are documentation, not code.

Chapter 2 is what happens when you take that seriously and build the layer that carries the documentation into the agent's actual decision loop.

## The seam, not the call

Every individual MCP tool call against the cloud succeeds or fails cleanly. `reserveDevice` returns. `getSession` returns. `getSessionArtifacts` returns. The reliability problem lives in the gaps **between** those calls — the device that reports ready but isn't, the upload that half-completes, the log endpoint that returns empty instead of erroring. An orchestrating agent that treats each call as atomic and the transitions as free will queue its next action into a state that hasn't settled.

The Kobiton write-up walks a worked sequence through one of those transitions and shows where a naive scheduler skids. The point isn't that the cloud is flaky — it's that the seams are invisible unless something makes them legible.

## What makes the seams legible

The reference implementation has three moving parts, each mapping back to a Chapter 1 gap:

- **Three task-specific agent definitions** — each one owns a routed decision (which device pool, when a session is actually ready, when to fall back to the artifact API instead of trusting a log call). Narrow agents with a single judgment to make beat one omniscient agent guessing across all of them.
- **Four advisory hooks** — deterministic signals fired at the dangerous transitions, so a probabilistic agent gets a hard fact at exactly the moment it would otherwise guess. Advisory, not blocking: they inform routing, they don't seize control.
- **Known limitations documented as partnership** — the cooldown window, the endpoint compatibility boundaries, the lifecycle states between `online` and `session-ready` — written down as a contract the agent can read, which is precisely the `AGENTS.md` surface Chapter 1 argued for.

That's the through-line for the series: Chapter 1 named the operational facts; Chapter 2 turns them into agents, hooks, and a documented contract so an agent **routes** instead of guesses.

## Read the full chapter

The complete write-up — the worked partial-failure sequence, the three routed decisions, the four hook signals, and "known limitations as partnership" — lives on Kobiton's blog:

**→ [Making Agents Reliable on Real-Device Clouds](https://kobiton.com/blog/make-agents-reliable-on-real-cloud-devices/)**

Chapter 3 closes the series with text-first AI triage on session logs — turning the artifacts these sessions produce into a signal an agent can act on.
