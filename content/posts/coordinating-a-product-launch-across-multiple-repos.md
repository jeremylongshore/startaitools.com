+++
title = 'Coordinating a Product Launch Across Multiple Repos'
slug = 'coordinating-a-product-launch-across-multiple-repos'
date = 2026-10-13T08:00:00-06:00
draft = false
tags = ["release-engineering", "devops", "monorepo", "multi-repo", "automation", "ci-cd"]
categories = ["DevOps"]
description = "The order of operations for a product launch across three repos and three releases: what each step prevents and what to check after the merge."
tldr = "A coordinated launch is a pipeline pattern, not luck. On a recent launch, three cross-repo pull requests landed in 71 seconds (one per repo, in a deliberate order), two same-repo additions spaced around the burst, and three releases fired from the existing release workflow over the next four hours. The order is the work, and the merge window is the proof that the order held."
+++

Multi-repo launches drift by default. A demo site keeps showing the old name while the canonical route (the one URL the product should be reachable at) finally exists, the homepage never surfaces the launch, a partner badge (a small image signalling a third-party endorsement) misses one surface, and the PRs merge in the wrong order. The fixes are predictable, the failure modes too.

After reading this you have the order of operations for shipping a coordinated launch across three repos, plus the post-merge checks (verifications run after each merge, before users see the change) that catch the drift before it ships publicly.

## What drift looks like

The easy mistake is treating each surface as its own launch. The product repo flips the canonical route. The demos repo (a separate site listing the company's running examples) still shows the old card. The landing page mentions the old name. The partner badge sits on a sidebar but not the homepage. Every individual change looks correct in isolation. Together they tell two contradictory stories on the live site for hours or days.

In a single-repo world this is one PR. In a multi-repo estate (the whole collection of repos, servers and services a company runs), a coordinated launch is three cross-repo PRs (one per repo) plus the same-repo additions and releases that support them. The coordination is the work, not the code.

## The three-repo burst

The shape that worked on a recent launch: three pull requests, one per repo, landed in 71 seconds in deliberate order.

First, the product repo gets the canonical route. The new demo address is live. Old bookmarks 301 to it. Form source attribution uses the product name, not the legacy project name. This is the smallest, most reversible change, and it has to land first so the demos catalog and the homepage can link to a real address.

Second, the demos repo gets the searchable catalog entry. The product card collapses its duplicates into one entry at the canonical route. The catalog still leads with the engineering evidence, but the entry is now findable from the hero and from a search for the product name.

Third, the landing page gets a real homepage slot for the launch. Not a footer link, not a feature subsection. A direct entry that describes the workflow, links to the canonical demo, and stays within the visitor vocabulary the demos catalog uses.

The three merges took 71 seconds. The order held across three repositories, three CI lanes, and three review queues. Merge in any other order and at least one surface breaks during the publish window. Merge in this order and the three changes read like one narrative when published.

## The same-repo additions

Two more pull requests landed on the landing page repo, hours before and after the burst.

The partner badge (a small image signalling a third-party endorsement) went in first, on its own release. The homepage is the surface most people see first, and a badge that reads "we are a real partner" anywhere else ships a less believable site. Pairing it with the canonical-route PR would have coupled two unrelated changes; pairing it on the same landing repo made it land on a different release, then converge with the homepage slot in production.

The mobile contact layout fix went in last, hours after the burst. A footer that compresses against the badge or a contact layout that overflows is the kind of regression that escapes desktop review and lands in the first wave of complaints. Shipping it on its own release, after the homepage feature was live, kept the change easy to revert.

## The three-release timing

The three cross-repo PRs alone do not publish anything. Each repo ships a release that the deploy workflow picks up. Three releases landed on this launch, on the landing page repo: a patch bump for the partner badge fix, another patch bump for the mobile contact fix, then a minor bump for the new homepage slot.

The releases are not separate launches. They fire from the existing release workflow on the landing page repo. They were spaced across four hours because the partner badge shipped first, the mobile fix landed after the burst, and the homepage feature (the one tied to the cross-repo coordination) shipped last.

The trap is treating the releases as background. They are the publish event. The PRs are the rehearsal.

## Post-merge checks

Three post-merge checks catch the drift while it still lives in a deploy window and can be reverted.

Check the canonical route from the product repo directly, not through the demos catalog. If the canonical address returns a stub or the old project still wins on ranking, the migration leaked.

Check the catalog from a clean browser, signed out, no cache. The new product entry should be findable from the hero and from a search for the product name. If only the engineering evidence shows it, the catalog landed but the entry did not.

Check the homepage on mobile width. A footer that compresses against the badge or a contact layout that overflows is the kind of regression that escapes desktop review and lands in the first wave of complaints.

## Why this matters

The pattern is not about shipping faster. It is about making drift impossible by construction. A reader hitting any one of the three surfaces lands on a coherent story. A scraper indexing the canonical route, the demos catalog, and the homepage finds one set of names and one partner signal. A new visitor clicking through from any surface ends at the same demo.

The demo itself sits at https://www.intentoutreach.com/, the canonical address the rest of the surfaces point to. Get that address right, and the rest of the launch is a publish event instead of a recovery exercise.

## Also shipped

- catalyst-onboarding-v2: a 21-hour autonomous Claude Opus 5 session closed the P2 correspondence gate, with 11 in-line test and syntax fixes and zero course corrections.

## Use this

- Ship the canonical product route before the catalog entry. If the catalog links to the old address for even ten minutes, search engines index the wrong canonical and the migration keeps dragging.
- Couple the partner badge to its own release, not the cross-repo burst. A partner signal that lands with the rest of the launch reads as marketing, not as evidence.
- Treat the release as the publish event, not the merge. The PRs are the rehearsal.

## Related posts

- [Coordinating 22 repos under one governance pattern](/posts/beads-rollout-twenty-two-repos-org-governance/): the same shape as coordinating three repos in 71 seconds, with atomic branches and a shared contract spelled out.
- [Estate-wide triage in one pass](/posts/backlog-zero-estate-triage-machine/): the inverse shape, one sweep across many repos, where the order-of-operations lesson still applies.
- [Coordinated cross-system work where the order of merges decides whether the system goes live or stays broken](/posts/ship-dormant-wire-later-multi-agent-slack/).
