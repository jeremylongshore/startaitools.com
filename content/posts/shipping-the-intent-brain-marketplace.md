+++
title = 'Shipping Is Not Building: A Sunday of Merges'
slug = 'shipping-the-intent-brain-marketplace'
date = 2026-06-15T08:00:00-05:00
draft = false
tags = ["development", "shipping", "git"]
categories = ["Development Journey"]
description = "A quiet Sunday with no new code—just four PR merges that landed the intent-brain marketplace and cited search built across the prior week."
+++

Sunday, June 15, 2026. No features were built. Four pull requests merged. That was the entire day.

It's tempting to read a day like this as nothing happened. The opposite is true. The merge is the moment work built across several days actually reaches the people it was built for. Building and shipping are two separate events, and they almost never happen on the same day.

## The Thesis

A commit is a promise to yourself. A merge is the work arriving for everyone else.

Across the prior week, two repos accumulated branches—an intent-brain marketplace, a cited-search feature, a plugin, a brain build. None of that was usable by a teammate until it was on `main`. On Sunday it landed. The whole job of the day was to close loops that had been open since Friday.

## What Actually Merged

Two repos, four merges. Nothing dramatic in any single one. Together they finished a feature that had been spread across the week.

**qmd-team-intent-kb** took two PRs:

- PR #185, `feat/intent-brain-marketplace`—the marketplace itself.
- PR #184, `feat/brain-cited-search-and-plugin`—cited search plus the plugin that exposes it.

Those two branches are the substance. The "intent brain" is a knowledge base; the marketplace makes brains discoverable, and cited search makes their answers traceable back to a source. Both were built earlier. Sunday is when they stopped being branches and became the product.

**intent-os** took the other two:

- PR #1, `track/brain-build-2026-06-13`—merging the brain-build track from two days earlier into the main line.
- PR #3, a changelog commit logging a Plane email fix and a partner onboarding (Max).

The changelog entry is the smallest thing on the list and the most honest about what shipping day looks like: you record what changed, including the boring operational fixes, so the next person reading the log knows the state of the world.

## Why Branch Names Carry Dates

`track/brain-build-2026-06-13` merged on `2026-06-15`. The branch name carries the day the work was *built*; the merge carries the day it *shipped*. Two days apart, and that gap is the entire point.

If you only look at `main`, the brain build looks like a Sunday event. It wasn't. The dated branch is the receipt that says: this was assembled Friday, it merged Sunday, and the time in between was review, conflict resolution, and waiting for the right moment to land it. The git history preserves both timestamps because both matter.

## Shipping Is Its Own Skill

The reason this deserves a note at all: a lot of effort goes into building, and almost none into respecting the merge as a distinct act. The branch sitting locally, passing every test, helps no one. It's potential, not delivery.

What a merge day actually requires:

- Resolving whatever drifted while the branch sat open.
- Confirming the PR still does what the branch name claims.
- Writing the changelog line so the state is legible to the next reader.
- Onboarding the person who now depends on the thing that just landed (the partner onboarding in the same changelog is not a coincidence—you ship to someone).

None of that is glamorous. All of it is the difference between code that exists and code that's in use.

## A Small Day That Closes a Loop

There's no metric to report here. No benchmark, no test count, no before-and-after. The honest shape of June 15 is four merges and a changelog entry. The intent-brain marketplace and cited search, built across the prior week, reached the main line. A Plane email bug got logged as fixed. A new partner got onboarded into a system that was, as of that morning, finally complete enough to onboard them to.

That's a full day's work even though no new code was written. Building is where the idea takes shape. Shipping is where it becomes real for someone other than the author. Sunday was a shipping day, and shipping days are worth naming.

## Related Posts

- [Honor the Gate When the Verdict Is Inconvenient](/posts/honor-the-gate-when-the-verdict-is-inconvenient/)
- [Green CI Proves Nothing: Why Your Tests Gate Zero Calls](/posts/green-ci-proves-nothing-why-your-tests-gate-zero-calls/)

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Shipping Is Not Building: A Sunday of Merges",
  "description": "A quiet Sunday with no new code—just four PR merges that landed the intent-brain marketplace and cited search built across the prior week.",
  "datePublished": "2026-06-15T08:00:00-05:00",
  "dateModified": "2026-06-15T08:00:00-05:00",
  "author": {
    "@type": "Person",
    "name": "Jeremy Longshore"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Start AI Tools"
  },
  "url": "https://startaitools.com/posts/shipping-the-intent-brain-marketplace/",
  "keywords": "shipping, merging, git workflow, pull requests, development journey, intent brain, cited search"
}
</script>
