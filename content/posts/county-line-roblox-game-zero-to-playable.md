+++
title = 'County Line: Roblox Game from Template to Feature-Complete in One Day'
slug = 'county-line-roblox-game-zero-to-playable'
date = 2026-01-22T10:00:00-06:00
draft = false
tags = ["roblox", "game-development", "lua", "rojo", "ci-cd"]
categories = ["Development Journey"]
description = "Building the County Line UTV mud racing Roblox game from a blank template to feature-complete in 14 commits across 3 repos: vehicle controls, retention systems, monetization, VFX, audio, and leaderboards."
+++

## From Template to Playable

County Line is a UTV mud racing game for Roblox. On January 22nd it went from a blank `roblox-game-template` initial commit to a feature-complete game across six development phases in 14 commits. Three repos were touched: the game itself, the template it was scaffolded from, and supporting agent infrastructure.

The velocity came from having a structured phase plan before writing any code. Each phase had clear exit criteria, and no phase started until the previous one was done. Six phases, one day, zero rework.

## Phase 2: Vehicle Controls

The template provided a bare Roblox place file. Phase 2 turned it into something driveable. UTV vehicle chassis, steering, throttle, suspension tuning — the fundamentals that make the game feel like a game instead of a tech demo.

Roblox vehicle physics are constraint-based. You define a `VehicleSeat`, attach `HingeConstraint` objects for wheels, and tune `AngularVelocity`, `MaxTorque`, and `Damping` values until the vehicle handles the way you want. Mud racing vehicles need heavy suspension travel and lower top speeds compared to road vehicles. The tuning took more iteration than the implementation.

## Phase 3: Retention Systems

Daily login rewards, streak tracking, and a progression system. The goal is simple: give players a reason to come back tomorrow.

The retention system tracks login timestamps in a `DataStore` and calculates streak length. Streaks multiply the daily reward up to a cap. Missing a day resets the streak but preserves total progress. Standard mobile game retention pattern adapted for Roblox's `DataStoreService`.

## Phase 4: Monetization

Roblox monetization runs on Developer Products (one-time purchases) and Game Passes (permanent unlocks). County Line uses both:

- **Game Passes**: Premium vehicle skins, exclusive trail area access
- **Developer Products**: Currency bundles, boost items

The receipt processing handles Roblox's `MarketplaceService:ProcessReceipt` callback pattern — you must return `Enum.ProductPurchaseDecision.PurchaseGranted` only after successfully granting the item, or the player gets charged without receiving anything. Edge case handling here matters more than in most game systems because real money is involved.

The receipt handler persists granted purchases to `DataStore` before returning `PurchaseGranted`. This protects against the case where the grant succeeds, the return value is sent, but the server crashes before the `DataStore` write. On next join, the player's inventory gets reconciled against purchase records.

## Phase 5: Vehicle Variety and Trails

One UTV isn't a game. Phase 5 added multiple vehicle options with different handling characteristics and a trail/leaderboard system. Each trail has a start gate, checkpoints, and a finish trigger. Completion times get stored in an `OrderedDataStore` for the leaderboard.

The leaderboard UI pulls the top 50 times from the `OrderedDataStore` sorted ascending. Roblox's `OrderedDataStore:GetSortedAsync` handles the sorting server-side, which keeps the client code simple.

## Phase 6: VFX and Audio

Mud particles, engine sounds, tire spray effects, and ambient audio. The visual polish phase that makes the game feel finished rather than functional.

Roblox particle emitters attached to wheel positions generate mud spray proportional to vehicle speed. Engine audio uses a `Sound` object with `PlaybackSpeed` modulated by RPM. Not physically accurate, but perceptually convincing.

## Supporting Infrastructure

Beyond the game itself, two other pieces shipped:

**Rojo Map Sync** — Rojo is the tool that lets you develop Roblox games in a real editor (VS Code) instead of Roblox Studio's built-in script editor. The `default.project.json` maps the filesystem directory structure to Roblox's instance tree. Setting this up correctly on day one means every subsequent commit works with standard Git tooling.

**CI/CD Pipeline** — GitHub Actions workflow that runs Selene (Lua linter) on every push. Catches common Lua mistakes — unused variables, shadowed locals, wrong `self` usage — before they make it into the game. Not a build pipeline (Roblox compilation happens in Studio), but a quality gate.

**Agent Infrastructure** — Strategic tooling for agentic development workflows. The template repo got its initial commit during this sprint, establishing the scaffold that County Line and future Roblox projects would share.

## Session Stats

| Metric | Value |
|--------|-------|
| **Commits** | 14 |
| **Repos** | 3 (county-line, roblox-game-template, agent infra) |
| **Phases completed** | 2 through 6 |
| **Key systems** | Vehicle physics, retention, monetization, trails, VFX, CI/CD |

## The Template Approach

Starting from a template instead of a blank repo saved roughly two hours of boilerplate: place file setup, Rojo configuration, basic project structure, `.gitignore` for Roblox artifacts. The template is now available for future Roblox projects, which means the next game starts at Phase 2 instead of Phase 1.

The lesson from this sprint: structured phases with clear exit criteria are the difference between "I built a game in a day" and "I made progress on a game for a day." Every phase had a definition of done. Every phase shipped.

## Related Posts

- [X Bug Triage Plugin: Zero to v0.4.3 in One Day](/posts/x-bug-triage-plugin-zero-to-v043-one-day/) — Another zero-to-complete sprint with similar velocity
- [Building Production CI/CD: Documentation to Deployment](/posts/building-production-ci-cd-documentation-to-deployment/) — CI/CD pipeline patterns applied in a different context
- [Marketplace CI Hardening](/posts/marketplace-ci-hardening-sync-guard-plugin-scaffold/) — CI governance patterns for a different ecosystem
