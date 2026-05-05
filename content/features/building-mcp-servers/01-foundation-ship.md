+++
title = 'Foundation Ship — Guidewire MCP v0.1.0'
weight = 10
date = 2026-05-05T08:00:00-05:00
description = 'The first chapter of the Building MCP Servers feature: what shipping a foundation v0.1.0 means in practice, and why "foundation" beats "minimum viable" as the framing.'
+++

**Source post:** [Guidewire MCP v0.1.0 — foundation ship](/posts/guidewire-mcp-v0-1-0-foundation-ship/)

The phrase "minimum viable product" is a trap when you're building infrastructure. MVP frames the conversation around what you can take *out* and still ship — which is exactly the wrong question for a server that other systems are about to depend on. **Foundation** is the better word: not the smallest thing that works, but the smallest thing that won't have to be torn out and rebuilt when chapter two arrives.

## What v0.1.0 actually means

A foundation release answers three questions before it ships:

1. **What schemas are public, and what are private?** Anything public is a contract. Once you've got users, you can't take it back without versioning.
2. **What's the auth boundary?** A v0.1 with no auth is fine for an internal MCP server. A v0.1 with hand-rolled auth is a disaster waiting on a refactor.
3. **What's the test surface?** Not "do the tests pass" — what's *covered*. The v0.1 tests are the ones you'll keep iterating against.

If those three are clear, the v0.1 ships and the v0.2 has somewhere to land. If any of them are fuzzy, you don't have a foundation — you have a prototype that someone is about to build on top of.

## The Guidewire ship

The Guidewire MCP v0.1.0 case study (linked above) walks through the actual decisions: tool surface, resource surface, prompt surface, and the deliberate non-decision to leave streaming for v0.2. Each of those decisions cost about an hour of thinking and saved about a week of regret.

The chapter ahead picks up from there: the integration test loop that caught three bugs the unit tests missed.
