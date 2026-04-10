+++
title = 'CAD Agent Perf Audit and git-with-intent SPIFFE Identity Analysis'
slug = 'cad-dxf-perf-planning-gwi-spiffe-identity-analysis'
date = 2026-02-23T10:00:00-06:00
draft = false
tags = ["performance", "architecture", "security", "spiffe", "ai-agents", "cad", "git-with-intent"]
categories = ["Development Journey"]
description = "A performance gap audit for the CAD agent and a SPIFFE/A2A identity analysis for git-with-intent — two planning sessions, no shipping."
+++

Not every day produces a release. February 23rd was two planning sessions across two projects — the kind of work that feels unproductive until you realize the next sprint runs 3x faster because of it.

## CAD Agent: Performance Plan Audit

The cad-dxf-agent hit v0.1.0 a few days ago. It works. It's also slow.

Loading a moderately complex DXF file (a structural floor plan with ~2,000 entities) takes 4-5 seconds on a decent machine. The edit engine processes changesets in under 100ms, but the initial parse and the viewer render are bottlenecks. For a desktop tool where Tony opens the same file 20 times a day, 5 seconds per open is noticeable. And that's a 2,000-entity drawing. Real structural detail sheets with schedules, notes, and dimension chains can hit 15,000+ entities. At the current rate, those would take 30+ seconds to load. Unacceptable.

The performance audit was systematic. Profile the full pipeline, identify the gaps, create tasks for each one.

**Parser hot spots.** The DXF parser reads the entire file into memory, builds a string-indexed entity map, then converts to the internal schema. Two problems: the string-indexed map uses linear scan for entity lookups (should be hash-based), and the schema conversion allocates intermediate objects that get immediately discarded. Both are fixable without changing the public API. The linear scan is the bigger offender — a 2,000-entity drawing means 2,000 string comparisons per lookup, and the edit engine does dozens of lookups per changeset operation. Switching to a dictionary keyed by entity handle should cut parse-to-edit time by 40-60%.

**Viewer render budget.** The Electron viewer redraws the entire canvas on every interaction — pan, zoom, entity selection. For 2,000 entities that's fine. For 10,000+ entities (a real structural drawing with details and schedules), it'll stutter. The fix is a dirty-region tracking system that only redraws entities affected by the current interaction. Standard 2D rendering optimization, but it needs to be designed before it's implemented. The canvas API supports clipping regions natively — the work is in determining which entities fall within the dirty region without scanning all of them. That's where the spatial index from the P3 list becomes a P1 dependency.

**Memory profiling gaps.** No memory profiling exists at all. The parser might be holding references to discarded intermediate objects. The revision history might be growing unbounded. Without profiling, these are guesses. The first task is to add memory snapshots at parse, edit, and save boundaries.

The audit produced 8 gap tasks, prioritized by user impact:

| Priority | Task | Expected Impact |
|----------|------|----------------|
| P1 | Parser hash-based lookups | 40-60% parse speedup |
| P1 | Viewer dirty-region tracking | Smooth 10K+ entity pan/zoom |
| P2 | Memory profiling at boundaries | Identify hidden leaks |
| P2 | Revision history size cap | Prevent unbounded growth |
| P3 | Lazy loading for large blocks | Defer unused block parsing |
| P3 | Incremental DXF writing | Avoid full-file rewrite on save |
| P3 | Entity spatial indexing | Fast area-based queries |
| P3 | Background thread for parse | Non-blocking UI during load |

No code shipped. Just a clear plan for what v0.2.0 needs to be fast.

## git-with-intent: SPIFFE/A2A Identity Gap Analysis

git-with-intent runs AI agents that interact with git repositories, LLM providers, and external APIs on behalf of tenants. Every agent action needs to be attributable to a specific tenant, a specific agent, and a specific run.

The current identity model is simple: each agent run gets a JWT issued by the platform, scoped to a tenant. That works for single-agent runs where one agent talks to one LLM and one set of APIs. But as the platform adds agent-to-agent communication (Google's A2A protocol), the identity model breaks down. When Agent A calls Agent B, which identity does Agent B use? The caller's? Its own? A delegated token? And when the audit log shows "agent modified file X," which agent in a multi-agent chain gets the attribution?

The SPIFFE (Secure Production Identity Framework for Everyone) analysis was a gap assessment: what would it take to give every agent a SPIFFE identity, and how does that compose with A2A protocol's authentication model?

**SPIFFE gives you workload identity without secrets.** Instead of distributing API keys or JWTs to agents, each agent gets a SPIFFE Verifiable Identity Document (SVID) issued by a SPIRE server. The SVID is an X.509 certificate that encodes the agent's identity as a URI: `spiffe://git-with-intent/tenant/acme/agent/code-reviewer`. Short-lived, auto-rotated, no static secrets to leak.

**A2A protocol needs identity at the agent level, not just the service level.** When Agent A sends a task to Agent B, the A2A spec expects both agents to authenticate. SPIFFE can provide the transport-layer identity (mTLS between services), but A2A also needs application-layer identity (which specific agent initiated this task). The gap is in the mapping: how do you go from a SPIFFE SVID to an A2A agent card identity?

The analysis identified three gaps:

1. **No SPIRE server infrastructure.** Deploying SPIRE on GKE adds operational complexity. You need a SPIRE server per cluster, node attestation configured for each node pool, and registration entries for each agent type. That's not a weekend task.

2. **SVID-to-A2A mapping.** A2A agent cards use opaque agent IDs. SPIFFE SVIDs use structured URIs. A mapping layer needs to translate between the two without losing the hierarchical identity structure that makes SPIFFE useful in the first place.

3. **Delegation chains.** When Agent A delegates work to Agent B, the SVID chain needs to be preserved for audit. SPIFFE doesn't natively support delegation — you'd need a custom claims mechanism or a sidecar that tracks the call chain. Without delegation tracking, the audit log shows Agent B did the work but doesn't show Agent A requested it.

None of this blocks the current roadmap. The platform works fine with JWTs for single-agent runs. But multi-agent orchestration is coming, and bolting identity onto a running system is harder than designing it in. The decision was to document the gaps now and revisit when A2A integration hits the roadmap — probably Q2 2026. By then, SPIRE's GKE attestor should be more mature, and the A2A spec's authentication model might have settled enough to build against without chasing a moving target.

**Also landed:** a `.gitignore` update for Vite build artifacts that were leaking into the repo. Small but annoying — every `git status` showed 30 lines of noise from `.vite/` cache files. The pattern was `**/.vite/` to catch nested workspace directories. These files were showing up in PRs as unrelated changes, which muddies review diffs and makes actual code changes harder to spot.

## Why This Day Matters

Planning days feel like you accomplished nothing. No PRs merged, no versions tagged, no deploy triggers fired.

But here's the thing: the last three projects where I skipped the planning phase and went straight to implementation? Each one had a mid-sprint "wait, we need to rethink this" moment that cost 2-3 days. The CAD perf audit means v0.2.0 won't waste time profiling during implementation. The SPIFFE analysis means multi-agent identity won't be a panic project when A2A goes live.

The work that prevents work is still work. Two documents, zero PRs, and the next two weeks of implementation are scoped and prioritized before they start. That's the trade.

---

## Related Posts

- [Shipping a CAD Agent from Zero: DXF Parsing, Edit Engines, and LLM Planner Interfaces](/posts/building-cad-dxf-agent-from-zero-to-v010/) — The v0.1.0 this audit is evaluating
- [git-with-intent v0.9 to v0.10: Docker Upgrades, README Rewrites, and Strategic Research](/posts/git-with-intent-v090-v0100-docker-upgrades/) — The platform these identity decisions affect
- [Fixing Provider Registry Mutations and Sandbox Permissions](/posts/fixing-provider-registry-mutations-sandbox-permissions/) — Earlier git-with-intent security work
