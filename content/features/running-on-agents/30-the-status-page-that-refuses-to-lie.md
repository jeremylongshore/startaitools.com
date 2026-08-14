+++
title = 'The Status Page That Refuses to Lie'
slug = 'the-status-page-that-refuses-to-lie'
description = 'Green requires fresh provenance and a timestamp, unknown renders loudly with a reason, and a coverage percentage exists only over a non-zero population. Twenty-two schema conditionals and 80 negative fixtures enforce it, because a rule nobody can see the violations of is a preference.'
date = 2026-08-13T10:00:00-05:00
draft = false
weight = 30
tags = ["json-schema", "observability", "contracts", "intent-os"]
categories = ["Architecture"]
toc = true
+++

Most status pages are a rendering of what a collector last managed to fetch. When the collector
fails, the page shows the previous value, and the previous value was green. This is the default
behavior of nearly every dashboard, and it is the single most dangerous property a status page
can have, because the failure it hides best is its own.

The Intent OS projections are built so that cannot happen, and the enforcement is not a code
review convention. It is JSON Schema, with negative fixtures that prove each rule rejects the
specific lie it was written to catch.

## The rule that defines operational

The doctrine came first. Decision D169, recorded 2026-08-05:

> D164 (the operational-readiness seven) is permanent architecture, binding on every subsystem:
> backup, the GitHub receiver, the event fabric, Graphify, OpenGrok, Intent Eval, SigNoz, the
> agent gateway, and every future service. **If something cannot automatically report its own
> health, ownership, evidence, and state into Mission Control, it is not considered operational.**

That is a stricter bar than it first appears, and the record says so in the same breath: several
subsystems that work fine today would not pass it. Which is the point of the second half of the
pairing, and the best sentence in the repository:

> The two decisions are deliberately paired: a rule nobody can see the violations of is a
> preference.

A rule with no visible violations is indistinguishable from a rule nobody follows. So D169 sets
the bar, and the capability matrix is the surface that shows who is under it. On 2026-08-12 the
matrix reported 16 declared capabilities: 8 healthy, 1 degraded, 6 unknown, 1 planned. Half the
estate cannot yet prove itself to the cockpit, which is visible on the front page rather than
being a thing you find out during an incident.

Each unknown row carries the reason and the bead that will close it. The backup fabric, for
instance, renders unknown with the note that its liveness markers exist on the dev box but do not
report into the composition set. The backups work. The reporting does not, and the page will not
round that up.

## Seven conditionals in the health contract

The health projection schema carries seven `if`/`then` conditionals. Across the four operational
schemas there are 22. They encode the things a human reviewer would otherwise have to notice.

The negative fixtures name themselves, which is the fastest way to read the contract:

```
schemas/fixtures/health-projection.v0/invalid-stopped-shown-healthy.json
schemas/fixtures/health-projection.v0/invalid-running-with-alarm-shown-healthy.json
schemas/fixtures/health-projection.v0/invalid-unknown-without-reason.json
schemas/fixtures/ownership-coverage.v0/invalid-percentage-over-zero-governed.json
schemas/fixtures/ownership-coverage.v0/invalid-unknown-without-reason.json
```

Read them as prohibitions and you have the design:

- A stopped container can never render healthy.
- A running container with a mapped warning or critical alarm can never render healthy.
- An unknown state must carry a reason. Unknown without explanation is invalid, not merely unhelpful.
- A coverage percentage cannot exist over a governed population of zero.

There are 154 fixtures in total, 80 of them negative. More than half the test corpus exists to
prove the contracts reject bad data rather than to prove they accept good data, which is the
correct ratio for a system whose whole job is refusing to overstate.

## Green is not a color, it is a claim with provenance

Every row on every projection carries where it came from and when it was observed. The
deployment-state header from 2026-08-12 reads:

```
Observed 2026-08-12T08:05:38Z · registry repos 147 · API calls 220/500 · VPS fleet: ok (46 containers on intentsolutions)
```

Three separate provenance facts before a single row of status. The capability matrix goes
further and states its source freshness inline: at compose time, ci-release-status fresh,
deployment-state fresh, health-projection fresh, linkage fresh. A source older than 48 hours
cannot produce a healthy row. It produces unknown, with the staleness as the reason.

The composition rule is written on the page itself, which means it cannot drift from the code
without someone noticing:

> Capability health, never data greenness: planned becomes planned/empty; no bound source becomes
> unknown-loudly (D169); absent or stale (>48h) source becomes unknown-with-reason, never
> healthy; monitor down or bound container non-healthy becomes degraded; else healthy.

## Two populations, never collapsed

The ownership coverage page is the clearest example of the whole philosophy, because it is the
one where the tempting lie is most obviously convenient.

There are 191 discovered repositories in the registry. There are 0 governed ones, because the
declaration store is empty at this stage, which is legal. The page could report 0% coverage. It
refuses:

> **NOT YET GOVERNED, no ownership percentage exists.** 191 repositories are discovered and none
> is governed yet, the declaration store is absent, which is legal at B2 start. No ownership
> percentage exists to report: nothing has been evaluated.

Zero governed is not 0% and not 100%. It is not yet governed, and that is a third state with its
own rendering. The schema enforces it via the negative fixture named above. The distinction
matters because 0% invites someone to chart it and watch it improve, when the true statement is
that no measurement has been taken at all.

The two populations, discovered and governed, are stated separately and never combined into one
number. Combining them would produce a figure that looks like a metric and means nothing.

## The independence that is real, and the one that is not

It would be a better story if two independent observers counted the container fleet and the page
went red when they disagreed. That is not what happens, and it is worth being exact.

The health page reports 46 healthy containers. The deployment-state page reports 46 containers on
the same host. Both numbers come from the same fence-ratified fleet collector, so this is one
observer reported twice. Two views agreeing is not corroboration when they share a source.

The genuine independence is narrower and lives in the collector, where Netdata's `/info` and
`/alarms` endpoints are read as two endpoints with two separate failure states:

```python
def collect_netdata(base_url, stub=None):
    """Two independent endpoints, two independent failure states (hardening:
    an /info failure must not discard usable /alarms data ...)."""
```

That hardening exists because the first version treated a failure of either endpoint as a total
failure, and threw away alarm data it actually had. SigNoz is probed separately for its own
health only, never its query API, and the health page links to telemetry depth rather than
copying it. Three monitors, three failure states, no shared fate.

## What this buys

The projections are not alerting. Paging belongs to the alert floor, and the pages say so. What
the contracts buy is narrower and more valuable: when a page says healthy, that word has a
defined meaning backed by a schema and a fixture that proves the opposite case is rejected.

A green light you have to interpret is not a green light. It is a color.
