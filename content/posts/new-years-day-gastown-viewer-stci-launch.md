+++
title = "New Year's Day: Gastown Viewer, STCI Launch, and Four Repos Deep"
slug = 'new-years-day-gastown-viewer-stci-launch'
date = 2026-01-01T10:00:00-06:00
draft = false
tags = ["go", "tui", "api-design", "ci-cd", "testing"]
categories = ["Development Journey"]
description = "Four repos, 26 commits. Gastown Viewer goes from scaffold to full MVP, STCI gets its ADR, create-agent-skill hits test coverage, and git-with-intent reaches Phase 35."
+++

Most people start the new year with resolutions. I started it with goreleaser configs and daemon HTTP APIs.

January 1st hit 26 commits across 4 repos. Not a typo. Here's what shipped.

## Gastown Viewer: Scaffold to MVP

Gastown Viewer went from an empty directory to a working product in a single day. The concept: a TUI and web interface for viewing and navigating structured intent data, backed by a daemon HTTP API.

The architecture has three layers:

1. **TUI client** — a terminal interface built in Go using Bubble Tea. Keyboard-driven navigation, tree rendering, detail panels. The kind of tool you can ssh into a server and use without a browser.
2. **Web client** — the same data, rendered in a browser. For people who don't live in terminals.
3. **Daemon HTTP API** — the shared backend. Both clients talk to the same API. No duplicated logic. No state drift between interfaces.

The Beads adapter was the piece that made this work cleanly. Instead of hardcoding a data source, the viewer plugs into any Beads-compatible store through an adapter interface. Swap the adapter, swap the data source. The viewer doesn't care where the intent data lives.

Goreleaser handles distribution. One `goreleaser.yaml` produces binaries for Linux, macOS, and Windows. Checksums, archives, changelog generation. Push a tag, get release artifacts. No manual build steps.

The daemon pattern deserves a note. Running the API as a background daemon means the TUI can start instantly — it doesn't need to load, parse, and index data on every launch. The daemon stays warm. Cold start is a one-time cost.

## STCI: The ADR Before the Code

STCI — the token cost index — got its foundation on January 1st. Not code. An Architecture Decision Record.

This might seem backwards. Why write an ADR for a project that doesn't exist yet? Because STCI is a data pipeline, and data pipelines built without schema decisions up front become data swamps within a month.

The ADR locked down: data collection strategy (which providers, which models, what granularity), storage format, indexing approach, and API surface. Tomorrow's code would follow today's decisions. That's the point of ADRs — they're not documentation for documentation's sake. They're constraints that prevent scope creep during implementation.

## create-agent-skill: Test Coverage Sprint

Six commits landed on create-agent-skill, all focused on testing. The scaffolding tool generates agent skill definitions, and the test suite needed to verify that generated output matched the expected structure across edge cases.

This is the unglamorous work. No new features. No architecture changes. Just making sure the thing that generates other things generates them correctly. The kind of work that prevents 3am debugging sessions two months from now.

## git-with-intent Phase 35

Phase 35 brought automation triggers and context graph updates to git-with-intent.

Automation triggers let you define rules that fire on specific intent events. Commit lands with a particular tag? Trigger a build. Intent graph edge crosses a threshold? Notify a channel. The trigger system is event-driven — it watches the intent stream and matches patterns against a rule set.

The context graph got denser. New edge types, better traversal queries, and performance work on the graph database layer. The graph is the core data structure of the whole system — every intent, every relationship, every dependency lives there. Making traversal fast is not optional.

Phase 35 is deep in the project timeline. At this point, git-with-intent is past the exciting early phases and into the grind of making a complex system robust. Automation triggers are the kind of feature that makes the system useful for real workflows instead of just interesting as a concept.

## The Pattern

Four repos. Twenty-six commits. One day.

The interesting thing isn't the volume. It's the mix. A greenfield MVP (Gastown Viewer), a design-before-code exercise (STCI ADR), a pure testing sprint (create-agent-skill), and deep iteration on a mature system (git-with-intent Phase 35).

New Year's Day code hits different when you're building tools you actually want to use. Gastown Viewer exists because I needed a better way to browse intent data. STCI exists because I wanted to track what LLM API calls actually cost over time. The best side projects are the ones that scratch your own itch.

Twenty-six commits is how you start a year.

---

## Related Posts

- [Building Post-Compaction Recovery: Beads](/posts/building-post-compaction-recovery-beads/) — The system Gastown Viewer's Beads adapter connects to
- [git-with-intent v0.9.0-v0.10.0: Docker Upgrades](/posts/git-with-intent-v090-v0100-docker-upgrades/) — Earlier phases of the git-with-intent evolution
- [GWI Feature Marathon: Phases 9-30](/posts/gwi-feature-marathon-phases-nine-through-thirty/) — The marathon that brought git-with-intent to this point
