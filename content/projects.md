+++
title = "Projects"
description = "Recent and active projects from Jeremy Longshore at Intent Solutions — what's been shipping in the last few weeks, with star counts and live links."
+++

What's been shipping lately. Star counts and pushed dates pulled live from GitHub; pages on this site link out to the canonical repo or live URL.

## Flagship — open source

### claude-code-plugins-plus-skills · 2,100+★

The marketplace and ecosystem hub. **425 plugins, 2,810 skills, 200 agents** for Claude Code — installable via the `ccpi` CLI package manager. Public marketplace at [tonsofskills.com](https://tonsofskills.com); source at [github.com/jeremylongshore/claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills).

This is the through-line for most of the other work — every plugin and skill listed below ends up in this hub. The `ccpi` package manager handles install, validation, and upgrade.

### @intentsolutions/audit-harness

Deterministic test-quality gates published as a single dev dependency. Hash-pinning, escape-scan, CRAP, architecture, bias, and Gherkin lint — runnable as `pnpm exec audit-harness <cmd>` in any repo. Companion to the `/audit-tests` and `/implement-tests` skills (the canonical Intent Solutions testing SOP).

[npm](https://www.npmjs.com/package/@intentsolutions/audit-harness) · [GitHub](https://github.com/jeremylongshore/audit-harness)

## Recently shipped

### guidewire-mcp-for-claude

Carrier-native MCP servers + governance harness for Guidewire estates (PolicyCenter, ClaimCenter, BillingCenter). v0.1.0 shipped in May 2026 — six foundation packages, five carrier-vocabulary tools, full blueprint published the same day. Anthropic-first; will publish to the claude-code-plugins-plus marketplace.

[GitHub](https://github.com/jeremylongshore/guidewire-mcp-for-claude) · [v0.1.0 case study](/posts/guidewire-mcp-v0-1-0-foundation-ship/)

### plugins-nixtla · 6★

Nixtla time-series forecasting plugins — StatsForecast, MLForecast, NeuralForecast — exposed as Claude Code skills with proper agent affordances. Built for an active Nixtla engagement. [GitHub](https://github.com/jeremylongshore/plugins-nixtla)

### claude-code-slack-channel · 17★

Two-way Slack bridge for Claude Code via Socket Mode + MCP stdio. Hash-chained tamper-evident audit journal, per-thread session isolation, policy-gated MCP tools, permission relay with Block Kit buttons, five-layer prompt-injection defense. Three runtimes (Bun / Node.js / Docker), TypeScript strict. [GitHub](https://github.com/jeremylongshore/claude-code-slack-channel)

### j-rig-skill-binary-eval

Release-quality evaluation harness and rollout gate for Claude Skills. Pushed daily; the eval framework that shipped 10 epics in a single day during March 2026. [GitHub](https://github.com/jeremylongshore/j-rig-skill-binary-eval)

### intent-blueprint-docs · 27★

Enterprise AI documentation generator — 22 templates covering PRD, architecture, tasks, risk management. Works in Claude Code and Cursor, zero-setup. [GitHub](https://github.com/intent-solutions-io/intent-blueprint-docs)

### iam-bobs-brain · 21★

General-purpose enterprise orchestrator on Google ADK + Vertex AI Agent Engine. Multi-agent system with risk tiers (R0–R4), policy gates, evidence bundles, and Mission Spec v1 workflows. [GitHub](https://github.com/intent-solutions-io/iam-bobs-brain)

### gastown-viewer-intent · 29★

Real-time agent observability dashboard. Beads task graph, agent activity stream, and system health rendered as either TUI or React web interface. Go + React. [GitHub](https://github.com/intent-solutions-io/gastown-viewer-intent)

## Production hosting

### Braves Booth Intelligence

Real-time broadcast operations dashboard for Atlanta Braves radio. Microservices, LLM narrative generation with a 4-tier fallback chain, live probability gauges. v1.0.0 currently live at [scorecardecho.com](https://scorecardecho.com).

### Intent Solutions VPS

A single Contabo VDS hosts five containerized stacks behind one Caddy ingress: Plane (project management), Twenty (CRM), Umami (analytics), ntfy (notifications), and the Braves Booth stack. Watchtower auto-updates the off-the-shelf services; per-repo CI/CD handles the bespoke ones. The migration runbook is open: [intentsolutions-vps-runbook](https://github.com/jeremylongshore/intentsolutions-vps-runbook).

### Partner deliverable portal

Single Hugo site at `partners.intentsolutions.io` with sections per partner engagement, deployed via Tailscale OIDC + force-command SSH from a GitHub Actions workflow. ~22 seconds end-to-end including smoke checks.

## Tooling and skills

### excel-analyst-pro · 26★

Financial modeling toolkit for Claude Code with auto-invoked skills. Build DCF, LBO, variance, and pivot tables from natural language. [GitHub](https://github.com/jeremylongshore/excel-analyst-pro-skill-md)

### iam-git-with-intent · 10★

AI-powered git workflow automation — smart commit messages, changelogs, PR descriptions, and release notes generated from diff analysis. [GitHub](https://github.com/intent-solutions-io/iam-git-with-intent)

### contributing-clanker

The `/contribute` Claude Code skill plus the OSS contribution workspace it operates on. Keeps AI-assisted upstream contributions honest before they reach maintainers — runs deterministic gates against any AI-proposed PR. [GitHub](https://github.com/jeremylongshore/contributing-clanker)

### qmd-team-intent-kb · 10★

Governed team memory platform for Claude Code, powered by QMD. Teams build, query, and maintain shared knowledge bases with access controls and audit trails. [GitHub](https://github.com/jeremylongshore/qmd-team-intent-kb)

## Research and exploration

### irsb · 1★

On-chain guardrails for AI agents — EIP-7702 spend limits, cryptographic execution receipts, automated dispute resolution. The principle: no AI agent should hold unguarded keys. [GitHub](https://github.com/jeremylongshore/irsb) · [hub on this site](/irsb-ecosystem/)

### moat · 1★

Verified Agent Capabilities Marketplace — MCP-first trust, policy, and execution layer for agent-to-agent interactions. [GitHub](https://github.com/jeremylongshore/moat)

### intentional-cognition-os

Local-first, remote-capable knowledge OS. "Compile knowledge for the machine. Distill understanding for the human." Active exploration. [GitHub](https://github.com/jeremylongshore/intentional-cognition-os)

### cad-ai-agent · 3★

Drawing intelligence platform for AEC professionals. Upload a DXF, PDF, or DWG; describe what you need in plain English; get structured edits, compliance reports, quantity takeoffs, RFIs, and drawing summaries — all without the AI ever touching the original file. [GitHub](https://github.com/jeremylongshore/cad-ai-agent)

## This site

[Start AI Tools](/) is the daily journal — built on Hugo, deployed via Netlify, rendered through the Dispatch design system, and published into automatically by a 7 AM cron that classifies each day's work into a tier and writes the post end-to-end. **241 posts** published as of this writing, growing daily without manual intervention. Source: [github.com/jeremylongshore/startaitools.com](https://github.com/jeremylongshore/startaitools.com).

---

Most repos are MIT or Intent Solutions Proprietary. Need help implementing any of these? [Let's talk.](https://intentsolutions.io/)
