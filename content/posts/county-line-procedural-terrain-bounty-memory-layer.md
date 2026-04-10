+++
title = 'County Line Procedural Terrain, Bounty Memory Layer'
slug = 'county-line-procedural-terrain-bounty-memory-layer'
date = 2026-01-24T10:00:00-06:00
draft = false
tags = ["roblox", "procedural-generation", "langgraph", "firestore", "ci-cd", "lua"]
categories = ["Development Journey"]
description = "16 commits across 5 repos: County Line world generation with procedural terrain and Selene CI, bounty-orchestrator memory integration with LangGraph Store, and CLAUDE.md housekeeping across IRSB and intent-mail."
+++

## Procedural Terrain

County Line's static map was a placeholder. Handcrafted terrain works for small areas but mud racing needs variety — different trail layouts, varying elevation, terrain textures that change between runs. January 24th started the procedural generation system.

The terrain generation uses Roblox's `Terrain:FillBlock` and `Terrain:FillBall` APIs to place voxel-based terrain at runtime. A seed-based noise function (Perlin via `math.noise`) controls elevation. The generator runs on the server at place load, creating a unique layout each session while keeping the structural features consistent — hills are always where you expect hills, but the exact contours vary.

The interesting constraint is performance. Roblox terrain is voxel-based with a 4-stud resolution. Filling large areas with `FillBlock` calls in a loop will freeze the server if you do it naively. The generator yields (`task.wait()`) every N operations to keep the server responsive during generation. Not elegant, but Roblox doesn't give you background threads for terrain operations.

## Driveable Vehicles on Generated Terrain

Procedural terrain creates a problem: vehicle spawn points need to be on solid ground. The previous static map had hardcoded spawn locations. With generated terrain, those coordinates might be inside a hill or floating above a valley.

The fix is a raycast from above each spawn point downward, finding the terrain surface, and placing the spawn pad at that Y coordinate plus an offset. `workspace:Raycast()` with a `RaycastParams` that only hits terrain (not parts). Each spawn point adapts to whatever the generator produced.

## Leaderboard Wiring

The leaderboard system from Phase 5 needed updates to work with procedural trails. Since trail geometry changes each session, leaderboard times are now scoped by seed — same seed means comparable times. Different seeds get separate leaderboard entries. The `OrderedDataStore` key includes the seed hash, so players comparing times are always comparing runs on identical terrain.

## Selene CI Integration

The GitHub Actions pipeline got Selene linting for Lua code quality. Selene is a static analyzer for Lua that catches Roblox-specific issues: deprecated API usage, incorrect `Instance` method calls, type mismatches in Roblox APIs.

The CI configuration uses a `selene.toml` with Roblox standard library definitions:

```toml
[lints]
global_usage = "allow"
shadowing = "warn"
unused_variable = "warn"

[config]
std = "roblox"
```

The `std = "roblox"` setting tells Selene about Roblox globals like `game`, `workspace`, `Instance`, and `script`. Without it, every Roblox API call looks like an undefined global.

## Bounty Orchestrator: Memory Integration

The bounty orchestrator from yesterday's greenfield got its memory layer. LangGraph Store provides persistent key-value storage that agents can read and write across graph executions. Combined with a `MemoryManager` class, the orchestrator now remembers past bounty evaluations.

The memory architecture:

- **LangGraph Store** — Persistent state that survives across workflow runs
- **MemoryManager** — Application-level abstraction over the store, handling serialization, TTL expiration, and conflict resolution
- **Firestore backing** — The Store is backed by Firestore documents, so memory persists across container restarts

The practical benefit: when the orchestrator evaluates a bounty it has seen before, it can compare current conditions against its previous assessment. If the competition increased or the bounty value changed, the EV score updates accordingly. Without memory, every evaluation starts from zero.

## CLAUDE.md Housekeeping

IRSB and intent-mail both got CLAUDE.md updates — refreshed project descriptions, updated command references, and corrected architecture descriptions that had drifted from reality. Not exciting, but these files are the first thing any agent session reads. Stale CLAUDE.md files waste context and produce wrong assumptions.

## Hustle Admin Migration

A few commits migrating Hustle's admin panel. Routine work — moving admin routes, updating data access patterns, no architectural changes worth documenting.

## Session Stats

| Metric | Value |
|--------|-------|
| **Commits** | 16 |
| **Repos** | 5 (county-line, bounty-orchestrator, hustle, irsb, intent-mail) |
| **Key systems** | Procedural terrain, Selene CI, LangGraph memory |
| **New capabilities** | Seed-based terrain generation, persistent bounty memory |

## Related Posts

- [County Line Visual Sprint, Bounty Orchestrator Greenfield](/posts/county-line-visual-polish-bounty-orchestrator-gwi-v040/) — Previous day's work on both County Line and the bounty orchestrator
- [Intent Mail: Full Platform with Gmail, Outlook, and Rules Engine](/posts/intent-mail-full-platform-gmail-outlook-rules-engine/) — The intent-mail project that got CLAUDE.md updates today
- [IRSB Deep Dive 1: On-Chain Enforcement](/posts/irsb-deep-dive-1-on-chain-enforcement/) — The IRSB project that also got documentation updates
