+++
title = 'CAD Agent Zero to v0.1.0, Intent Scout Economics, and Perception Auto-Ingestion'
slug = 'cad-dxf-agent-zero-to-v010-intent-scout-economics'
date = 2026-02-20T10:00:00-06:00
draft = false
tags = ["ai-agents", "cad", "dxf", "python", "architecture", "typescript", "full-stack"]
categories = ["Development Journey"]
description = "A full greenfield CAD agent from DXF parser to desktop UI shell in 17 commits, plus an economics layer for Intent Scout and stale-feed filtering for Perception."
+++

February 20th was a three-project day, but one project dominated. The cad-dxf-agent went from empty directory to tagged v0.1.0 release in 17 commits.

## CAD Agent: The Full Greenfield

The idea is simple. A structural engineer types "move the column east by 2 feet" and the software edits the DXF file. Local-first, no cloud dependency for the core workflow, never modifies the original file.

Seventeen commits built the full pipeline:

**DXF schema, parser, and writer.** The schema defines the internal representation — entities, layers, blocks, attributes. The parser reads industry-standard DXF files into that schema. The writer serializes edited drawings back to valid DXF. Round-trip fidelity matters here. If you parse a DXF, make no changes, and write it back, the output should be byte-for-byte identical to the input. Any drift means the tool is silently corrupting drawings. The parser handles the main entity types a structural engineer encounters: LINE, LWPOLYLINE, CIRCLE, ARC, TEXT, MTEXT, INSERT (block references), and DIMENSION. Anything exotic gets preserved as raw DXF data — passed through without interpretation.

**Edit engine.** The core module that applies structured changesets to an in-memory drawing. Move an entity, update a text label, add a block reference — each operation type has its own handler. The engine validates every operation before applying it. Invalid operations (moving an entity that doesn't exist, setting a property to an out-of-range value) get rejected with specific error messages, not silent failures.

**Revision notes.** Every edit session generates a revision log: what changed, which entities were affected, what the before/after values were. This is a compliance requirement for structural engineering — you need to know who changed what and when. The revision log is structured data, not just text. Each entry records the operation type, the entity handle, the old value, the new value, and a timestamp. This means you can diff two revision logs to see exactly what changed between two edit sessions — useful for peer review of drawing modifications.

**Planner provider interface and mock.** The LLM sits behind an abstract `PlannerProvider` interface. The `MockProvider` matches keywords to canned changesets — "move" triggers a move operation, "add" triggers an insert. No API key needed. Tests and CI run entirely against the mock. The interface contract means swapping in a real LLM provider later requires zero changes to the edit engine, validation, or UI layers.

**Desktop UI shell.** An Electron-based application that renders DXF drawings in a 2D viewer, accepts natural language prompts in a chat panel, and displays revision history. The viewer handles pan, zoom, and entity selection. Nothing fancy — functional enough to demo the pipeline end-to-end. The architecture keeps the UI completely decoupled from the backend: the viewer talks to the edit engine over IPC, which means swapping the Electron shell for a web UI later is a wiring change, not a rewrite.

**CI, tests, and docs.** GitHub Actions running pytest and linting on every push. The test suite covers three layers: parser round-trips (does a parsed-and-rewritten DXF match the original?), edit engine operations (does each operation type produce the expected state change?), and mock planner responses (does the mock return valid changesets for known prompts?). README with architecture diagram and setup instructions. CHANGELOG tracking every release. The usual governance files — LICENSE, CONTRIBUTING, code of conduct.

**Beads and doc-filing.** Task tracking from day one. Every feature got a bead, every bead got closed with evidence. Documentation filed into the standard numbering scheme.

The v0.1.0 tag landed at the end of the day. A real release with a changelog entry, not just a git tag. The full pipeline works: open a DXF, type a prompt, see the changeset, apply it, save the modified drawing. Every step covered by tests.

What doesn't work yet: real LLM integration (mock only), performance on large drawings, and the UI is rough. All known. All scoped for v0.2.0.

## Intent Scout: Economics Layer and Landscape Scanner

Intent Scout is a tool for scanning the AI agent landscape — who's building what, where the funding is going, what patterns are emerging.

Two commits landed:

**Economics layer.** A module that tracks funding rounds, valuations, revenue signals, and pricing models across the companies in the scanner's database. The data model handles the messiness of real fundraising data — some companies announce rounds without amounts, some have multiple rounds in the same quarter, some have convertible notes that don't map cleanly to equity rounds.

**Landscape scanner with ABI parse fix.** The scanner ingests structured data from on-chain sources, which means parsing contract ABIs. A bug in the ABI parser was silently dropping event definitions that used tuple types. The symptom: events with complex parameter types simply didn't appear in the scanner output. No error, no warning — they were filtered out during signature computation. The fix was in the type resolver — tuples need recursive expansion before the top-level event signature can be computed. A tuple parameter `(address,uint256)` needs to be expanded to its component types in the signature hash, not treated as a single opaque type.

Small commits, but the economics layer is foundational. Every analysis that says "this sector is heating up" needs funding data behind it. Without structured economics data, the scanner is just a list of companies. With it, you can track capital velocity — which sectors are accelerating, which are cooling, and where the smart money is concentrating.

## Perception: Auto-Ingestion and Stale Filtering

One commit on Perception, the media intelligence dashboard. Two features:

**Auto-ingestion on login.** Previously, the dashboard showed whatever data was in Firestore from the last manual ingestion run. If you didn't manually trigger an ingestion, you were looking at yesterday's news. Now it triggers a fresh ingestion when a user logs in, but only if the last ingestion was more than 6 hours ago. A timestamp check in a Firestore metadata document prevents hammering the RSS feeds on every page refresh or rapid tab switching.

**Stale feed filtering.** RSS feeds go stale. Publishers change URLs, sites go offline, feeds stop updating without warning.

The filtering rules are simple:

- A feed with no new articles in 30 days gets flagged as stale.
- A feed returning errors on 3 consecutive fetches gets disabled automatically.
- The dashboard shows a "feed health" indicator so you can see at a glance when your intelligence pipeline has blind spots.

Both features are infrastructure that the user never notices when it works. They only notice when it doesn't — stale dashboards and dead feeds are the kind of rot that kills trust in a tool.

## The Day in Numbers

| Project | Commits | Key Outcome |
|---------|---------|-------------|
| cad-dxf-agent | 17 | v0.1.0 release — full pipeline from parser to UI |
| intent-scout | 2 | Economics layer + ABI parse fix |
| perception | 1 | Auto-ingestion + stale feed filtering |

Twenty commits across three projects. The CAD agent was the headline — greenfield to tagged release in a day. The Intent Scout economics layer and Perception stale filtering are the kind of invisible work that compounds over weeks. Nobody tweets about a stale feed filter. But when the dashboard shows fresh data every morning without manual intervention, that's the filter doing its job.

Greenfield days are the most satisfying days in software. Every commit makes visible progress. No legacy code fighting you. No backwards compatibility constraints. Enjoy it while it lasts — by v0.2.0, the codebase has opinions and you're negotiating with your own past decisions.

---

## Related Posts

- [Shipping a CAD Agent from Zero: DXF Parsing, Edit Engines, and LLM Planner Interfaces](/posts/building-cad-dxf-agent-from-zero-to-v010/) — Deeper technical dive into the CAD agent architecture
- [Perception Dashboard: Wiring Real Triggers, Topic Watchlists, and the BSL-1.1 Decision](/posts/perception-dashboard-real-triggers-topic-watchlists/) — Earlier Perception infrastructure work
- [IRSB Monorepo v1.0.0: Extracting Shared Packages](/posts/irsb-monorepo-v1-extracting-shared-packages/) — Another greenfield architecture from this same week
