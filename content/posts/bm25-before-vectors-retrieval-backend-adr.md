+++
title = 'BM25 Before Vectors: An Eval-Gated Retrieval ADR'
slug = 'bm25-before-vectors-retrieval-backend-adr'
date = 2026-06-17T08:00:00-05:00
draft = false
tags = ["retrieval", "search", "testing", "adr"]
categories = ["Development Journey"]
description = "Why ship BM25 search now and gate vectors behind an eval set? An ADR naming the trigger before a 333MB embedding model creeps into a local-first plugin."
+++

The day after you ship a thing, there's a pull toward the next feature. June 17 was the day after the Governed Second Brain plugin went public, and almost none of the work was new features. It was test coverage for gates that had none, a license finally pinned to a name, a `main` branch dragged back to green after a sync, and one decision written down before it could evaporate.

That last one is the highlight: a retrieval-backend ADR that says *don't add a vector database yet.*

It's the least flashy item on the list and the most valuable one, because it's the only artifact that will still be doing work three weeks from now when someone hits a search that doesn't return what they wanted.

## The Thesis

The day after a ship isn't for building forward. It's for backfilling the things that ship-day pressure skipped — the test coverage, the license metadata, and especially the decisions you made in your head but never wrote down. A decision that lives only in your memory is a decision you'll relitigate in three weeks, badly, having forgotten why you chose what you chose. The cheapest insurance against that is an ADR with the reasoning and the trigger condition baked in.

## The Decision: BM25 Now, Vectors Behind an Eval Gate

The Governed Second Brain stores memories and answers questions over them. Today, search runs on BM25 — keyword ranking, the same family of algorithm that powered search engines in the 1990s. It is boring, fast, has zero model dependency, and it works for most lookups.

It does not work for everything. A natural-language question phrased as a sentence — "does the brain run in-process without a daemon" — returned zero hits from the BM25 keyword path. The same question run through the hybrid query path (query expansion + vector similarity + a reranker) returned exactly one hit: the right one. So the upgrade path is real and proven, not theoretical.

The obvious move is to flip on vectors. The ADR ([qmd-team-intent-kb #189](https://github.com/jeremylongshore/qmd-team-intent-kb)) says: not yet.

The hybrid path isn't free. Turning it on pulls a ~333MB embedding model down on first run. For a local-first plugin whose whole pitch is "runs in-process, no daemon, no egress," a 333MB dependency is not a footnote — it's a different product. So the decision was written down as three clauses:

- **BM25 now.** It's the default backend. No model, no download, no egress.
- **Eval-gated, lean sqlite-vec next.** Vectors get added only when an eval set proves BM25 is leaving real questions unanswered — and when it does, the implementation is the leanest one that works (sqlite-vec, not a separate vector service).
- **Pin the weights.** When the embedding model does land, its weights are version-pinned. Retrieval quality that depends on a model is only reproducible if the model can't silently change underneath you.

Written down, the core of the ADR is three lines you can read in ten seconds:

```
Retrieval backend
  now:     BM25 (qmd search) — keyword, zero model, zero egress
  next:    sqlite-vec, ONLY when an eval set proves BM25 misses real questions
  always:  pin the embedding-model weights for reproducibility
```

The shape of that decision is the point. It's not "BM25 is good enough forever." It's "BM25 is the floor, and here is the exact condition under which we climb off it." The eval gate is the trigger. Without it, the upgrade is a vibe — someone notices a missed query, declares search broken, and bolts on a vector database the following Tuesday, dragging a 333MB model and a reproducibility problem in behind it. With it, the upgrade waits for evidence and arrives lean.

Note what the ADR does *not* do: it doesn't pick a winner on aesthetics. BM25 isn't there because keyword search is elegant; it's there because it's the cheapest backend that clears the bar today. The day it stops clearing the bar — measured, not felt — the gate opens. That's the difference between a default and a dogma.

This is the same discipline as a [pre-registered STOP](/posts/honor-the-gate-when-the-verdict-is-inconvenient/): write the gate before the number lands so the verdict is binding instead of motivated. Here the gate guards a dependency-weight decision rather than a research spend, but the mechanic is identical — name the condition in advance, in writing, so the future decision is bounded.

## The Unglamorous Half

The rest of the day was the kind of work that doesn't make a changelog headline but keeps the lights on.

None of it was glamorous. All of it was the same move as the ADR — take something fragile or implicit and make it solid and explicit — applied to tests, branches, installs, and licenses instead of to a search backend.

**Test coverage for all 51 gates.** [contributing-clanker](https://github.com/jeremylongshore) added bats coverage for every one of its 51 gates plus a shellcheck cleanup, closing a P1 from its own test audit (PR #54). Then it refreshed `TEST_AUDIT.md` and `TESTING.md` so the documented state matches the real state. A gate with no test is a gate you're trusting on faith; 51 of them on faith is a liability you only discover when one silently stops firing — and by then the thing it was supposed to catch is already in `main`. Backfilling the bats suite turns "we think these gates work" into "every gate has a test that proves it does."

**Getting `main` green again after a sync.** [claude-code-plugins](https://github.com/jeremylongshore/claude-code-plugins) pulled an external-plugin sync from upstream (#875), which knocked `main` over. Recovery took three surgical fixes — restore the branch after the sync (#877), then regenerate the README table of contents and fix a broken link (#879) — not a revert, not a force-push, just the minimum to get back to green. The same day it bumped patch versions for 43 plugins and listed governed-second-brain as a source. An external sync that turns `main` red is normal; leaving it red is not.

**Hardening the thing that just shipped.** The plugin itself got two point releases. 0.1.5 hardened the DB tools so they work for people who install the plugin directly, not just through the project's own installer — the failure mode you only see once a stranger runs your code. 0.1.6 declared the MCP server inline in `plugin.json` so it's self-contained. Day-two of a ship is when the assumptions baked in for *your* environment get found and removed.

**Settling the license.** The umbrella project ([intentional-cognition-os #138](https://github.com/jeremylongshore)) settled decision record DECR 035 to Apache-2.0 and canonicalized the umbrella's name, with the same change mirrored into qmd-team-intent-kb (#188). "What license is this and what is it actually called" is a question that's free to answer the day you write it down and expensive to answer the day a contributor asks in an issue. The umbrella's own guidance picked up the retrieval-backend decision too, and the plugin's status table got bumped to match the version that actually shipped — small diffs whose only job is to keep the documented world and the real world from drifting apart.

None of that ships a feature. All of it lowers the cost of the next feature.

## Why Write It Down At All

Every item above is the same move applied to a different artifact: take a state that currently lives in someone's head or in ship-day muscle memory and pin it to a file. The 51 gates get tests so coverage is a fact, not an assumption. The license gets a decision record so the answer is canonical, not folklore. And the retrieval backend gets an ADR so the next person who hits a missed search query reads "we chose BM25 on purpose, here's the eval gate that unlocks vectors" instead of reinventing the entire debate.

The new feature can wait a day. The decision you made today can't — it's already fading. Write it down while you still remember why.

## The Cost Asymmetry

An ADR costs about fifteen minutes: read the situation, name the trigger, commit the file. The thing it prevents costs days. A vector database added on a hunch is not a fifteen-minute mistake — it's a 333MB dependency, a model you now have to pin and ship, an egress story your users didn't sign up for, and a search stack two people will argue about in a future issue because nobody remembers it was supposed to be eval-gated. The ADR is the cheap artifact that stops the expensive one. Same with the 51 gate tests and the license record: minutes to write, days of confusion avoided.

That's the whole case for the day-after-ship day. It produces nothing you can demo. It produces the documents that make everything you demo next week cheaper and the decisions that made them defensible. Backfill the tests, settle the license, write down the ADR — then go build the next thing, on a foundation that won't make you relitigate the last one.

## Related Posts

- [Honor the Gate When the Verdict Is Inconvenient](/posts/honor-the-gate-when-the-verdict-is-inconvenient/)
- [Green CI Proves Nothing: Why Your Tests Gate Zero Calls](/posts/when-green-ci-proves-nothing/)
