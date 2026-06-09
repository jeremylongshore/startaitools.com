+++
title = 'Agent-Native Mobile Testing'
slug = 'agent-native-mobile-testing'
description = "A three-chapter series on plugin authoring, agent reliability on real-device clouds, and AI triage for agent-orchestrated mobile cloud testing — worked through kobiton/automate as the running case study."
date = 2026-05-11T07:00:00-04:00
featured = true
status = 'in-progress'
+++

Agentic CLIs are converging on a single substrate for mobile testing — MCP servers expose vendor capabilities, AGENTS.md briefs cross-runtime behavior, hooks enforce deterministic invariants, OpenTelemetry observes the result. The vendors building real-device clouds for AI-driven testing are the first ones who have to solve this in production.

This feature works through what plugin authoring looks like in that world, using Kobiton's published [`kobiton/automate`](https://github.com/kobiton/automate) plugin as the running case study. Three chapters, expanding as the series ships:

- **[Chapter 1 — AGENTS.md as a Cross-Tool Plugin Brief](/features/agent-native-mobile-testing/01-agents-md-cross-tool-plugin-brief/)** (May 11): a 5-device parity sweep, the gaps it exposed, and the operational facts a good `AGENTS.md` would close.
- **[Chapter 2 — Making Agents Reliable on Real-Device Clouds](/features/agent-native-mobile-testing/02-making-agents-reliable-on-real-device-clouds/)** (Jun 9): the partial-failure seams between MCP tool calls, and the agents + hooks + documented limitations that close the Chapter 1 gaps. Published on [Kobiton's engineering blog](https://kobiton.com/blog/make-agents-reliable-on-real-cloud-devices/).
- **Chapter 3:** Text-first AI triage on session logs. *(in progress)*

Each chapter cites and links back to where it was first published; the chapter form here adds connective tissue that didn't fit the original post format.
