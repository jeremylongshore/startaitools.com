+++
title = 'Making Agents Reliable on Real-Device Clouds'
slug = 'making-agents-reliable-on-real-device-clouds'
date = 2026-06-09T08:00:00-05:00
draft = false
canonicalURL = "https://kobiton.com/blog/make-agents-reliable-on-real-cloud-devices/"
tags = ["claude-code", "mcp", "agents", "hooks", "mobile-testing", "kobiton", "reliability", "devops", "appium"]
categories = ["Technical Deep-Dive"]
description = "Reliability on a real-device cloud isn't in the API calls — it's in the partial-failure seams between MCP tool calls. Three task-specific agents, four advisory hooks, and a documented-limitations list make those seams legible so an agent routes instead of guessing."
+++

> **Canonical home:** This post first appeared on Kobiton's blog at [kobiton.com/blog/make-agents-reliable-on-real-cloud-devices](https://kobiton.com/blog/make-agents-reliable-on-real-cloud-devices/). This page mirrors it; SEO authority consolidates to the Kobiton URL via `rel="canonical"`.

# Making Agents Reliable on Real-Device Clouds

**TL;DR** — Every MCP tool a real-device cloud exposes is individually well-behaved; the reliability problem lives in the *seams between calls* — the reservation that succeeds before the device is session-ready, the upload that succeeds before the parser finishes, the termination that succeeds before a ~5-minute cooldown clears. The reference implementation makes those seams legible with three task-specific agents (device picker, capability reconciler, session triage), four hooks around the MCP calls (three advisory, one guard), and a Known Limitations section tied to public issues. The hooks make **zero authenticated API calls** — they emit advisories into the agent's context and let the agent's already-authenticated MCP tools do the real work, which collapsed a six-blocker security review down to almost nothing. Reliability in this category is the legibility of the seams.

---

## The partial-failure problem

Real-device clouds expose tools that are individually well-behaved: reserveDevice, uploadAppToStore, confirmAppUpload, getApp, terminateSession. Each call presents a discrete success or failure boundary. The reliability issue isn't in any single call; it's in the seams between calls.

A reservation returns success, but the device enters a brief readiness window before sessions can actually start.

An app upload returns success, but a server-side parser is still asynchronously processing the APK in the background, and downstream calls that assume "uploaded means usable" fail in ways that don't make root cause obvious.

A session termination returns success, but the device enters an observed cleanup cooldown of roughly five minutes during which the same device's reservation will fail under a generic `device_unavailable`.

For a human operator using a web portal, these gaps are usually manageable: wait briefly and retry. For an agent composing 8–10 tool calls into a single orchestrated run, each invisible gap is a routing decision the agent can't make without the right signals.

The reference implementation makes those signals legible. Three layers, in order of where they sit in the call stack: agents at the top, deciding what to do; hooks in the middle, annotating *what just happened*; documented limitations underneath, telling the agent *what the platform doesn't do*.

## A worked sequence

To make this concrete, consider a typical orchestrated run. The agent calls reserveDevice and gets success. It calls uploadAppToStore and gets success. It calls confirmAppUpload, also success. Without help, the natural next step is to start a session. But the platform parser is still asynchronously processing the binary in the background; downstream calls before the parse completes can fail in ways that don't make root cause obvious. With the May 12 changes in place, a PostToolUse hook on confirmAppUpload injects an advisory into the agent's context recommending it poll `getApp(appId)` until the state field reads `READY`. The agent waits, polls, sees `READY`, and only then issues the next call. Same number of tool calls; lower probability of triggering the failure window.

## Three agents, three routed decisions

The reference implementation now includes three task-specific agent definitions under `agents/`. Each maps to a specific orchestration moment where a senior engineer would carry tacit knowledge and an agent, without help, would not.

**device-picker.md.** When the user describes a target device in natural language ("Pixel 7", "any modern Android", "latest iPhone with iOS 17"), the picker resolves the description into a `listDevices` filter, ranks candidates by live availability and match strength, surfaces the top 1–3 to the user for confirmation, and excludes-on-retry if a reservation fails with `device_unavailable`. The conservative behavior (always confirm before reserving, exclude failed candidates, fall back to manual selection after two failures) is the routing rule that keeps an agent out of reservation thrash. A device fleet under contention can chew through retries silently; a picker that knows when to stop is the difference between a retry spiral and a clean fallback.

**appium-capability-reconciler.md.** When a user's local Appium test script has capabilities that diverge from the selected device and app, the reconciler applies a three-policy rule: must-match fields (`platformName`, `udid`, `app`) auto-edit to match; suggested-default fields (`automationName`, `sessionName`) ask the user before overwriting; user-controlled fields stay untouched. The contract is designed to reduce silent capability mismatches where a test executes against an unintended device profile and the mismatch only surfaces during downstream debugging.

**kobiton-session-triage.md.** When a session terminates in a non-success state, the triage agent pulls the artifact bundle and applies a documented detector ladder (parser race, cooldown collision, log-endpoint mismatch, capability mismatch, reservation conflict, then script-level error), presenting the diagnosis with specific evidence pointers and a recommended fix. The detector ladder is ordered by specificity, not by frequency: a more-specific pattern matches first, so the agent's diagnosis improves diagnostic specificity instead of defaulting to the most common failure category. The agent avoids asserting a root cause without artifact-level evidence. If the bundle is inconclusive, it says so and surfaces the raw artifacts for the user.

What ties the three together is that each turns a fuzzy orchestration moment (which device should I pick? do these capabilities match? why did this fail?) into a routed decision with named conservatism rules. An agent calling these doesn't have to invent the rules at runtime.

## Four hooks, four legible signals

The `hooks/` directory includes four scripts that fire around the plugin's MCP tool calls. Three of them are advisory; one is a guard.

| Hook | Event | What it does |
|------|-------|-------------|
| `validate-userintent` | PreToolUse, every tool | Validates a userIntent argument against a bounded regex (110–145 chars, partner + experiment phase + verb phrase + contact email). Denies the call if malformed. |
| `advise-pre-terminate-cooldown` | PreToolUse, `terminateSession` | Allows the call; injects a notice that the device enters a ~5-minute cooldown immediately on success. |
| `advise-app-upload-poll` | PostToolUse, `confirmAppUpload` | Injects an advisory recommending the agent poll `getApp(appId)` until state reads `READY` or `FAILURE_PARSING` before issuing downstream calls. |
| `advise-post-terminate-cooldown` | PostToolUse, `terminateSession` | Confirms the cooldown window with `sessionId` echoed for traceability. |

The key architectural decision here is that **the hook scripts make zero authenticated API calls**. An earlier version of this bundle had the hook scripts themselves poll `getApp` to drive the parser-readiness wait. A multi-reviewer review of that design flagged the credential strategy, SSRF surface, and PII echo into agent context as significant concerns: six blocker-level findings and eight high-severity concerns across the credential, network, and prompt-injection axes. In the reference implementation, the current hook design eliminates the need for authenticated API calls within the hook layer itself. Hooks emit text advisories into the agent's context window; the agent uses its already-authenticated MCP tools to do any real polling. Same outcome, substantially smaller security blast radius, and reduced risk that a compromised or misconfigured hook script could expose credentials or session content.

That advisory-only posture is also why the hooks compose cleanly with the rest of the stack. A hook never owns state; it annotates state the tool just returned. The agent stays the decision-maker. The hook just makes sure the agent isn't deciding blind.

Same shape as the agents, one layer lower: invisible platform state becomes legible advisory; the agent's next decision is informed instead of speculative.

## Known limitations as partnership

The third leg is harder to point at than the agents or the hooks, because it's a documentation pattern rather than a code path. The `skills/run-automation-suite/SKILL.md` now includes a Known Limitations section listing the documented platform-state issues (`confirmAppUpload` async race, `deleteSession` cooldown, W3C-strict log-endpoint behavior, `listDevices` token-cap pagination), each tied to a public `kobiton/automate` issue tracking the upstream fix.

This matters because the alternative — a SKILL.md that reads "the plugin handles app upload, session lifecycle, and log retrieval seamlessly" — is the marketing voice that fails first contact with an agent. Agents do not infer intent from marketing language. They route from explicit constraints, caveats, and documented behavior. A skill that names its limits in line gives the agent the same calibration a senior engineer would carry into the work.

The cross-tool brief at `AGENTS.md` extends the same pattern to non-Claude harnesses. Same caveats, same upstream issue references, same documented constraints, just reachable by Gemini CLI, Codex CLI, and Copilot CLI without requiring those clients to read Claude-specific docs. One source of truth, four runtimes.

Transparency becomes part of the reliability model itself.

An agent that knows what the platform does not guarantee can route around uncertainty. An agent that does not know will retry blindly, misclassify failures, and compound orchestration drift.

## The takeaway

A real-device cloud's reliability story used to live in two places: fleet availability and Appium driver fidelity. Both still matter. But for an agent-orchestrated workflow, a third dimension shows up: *the legibility of the seams* — the partial-failure windows between successful tool calls where invisible platform state lives. Reservations that succeed before sessions can start. Uploads that succeed before parsers finish. Terminations that succeed before cooldowns clear.

The May 12 fork revision makes those seams legible. Three agents route the decisions the partial-failure moments demand. Four hooks turn invisible state into advisories the agent can act on. A Known Limitations section keeps the calibration honest as the platform evolves.

If you author a plugin against a real-device cloud: agents for the orchestration moments, hooks for the seams between them, a documented limitations list for the partnership. None of those replaces the underlying platform. Together they make an agent better equipped to interact with it reliably. And reliability, in this category, is the feature that compounds.

---

*This is Chapter 2 of the [Agent-Native Mobile Testing](/features/agent-native-mobile-testing/) series. [Chapter 1 — AGENTS.md as a Cross-Tool Plugin Brief](/posts/agents-md-cross-tool-plugin-brief/) ran the parity sweep that surfaced these seams; this chapter is the reference implementation that closes them.*
