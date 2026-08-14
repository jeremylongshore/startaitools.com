+++
title = 'Two Months, 598 Commits'
slug = 'two-months-598-commits'
description = 'What one operator and a fleet of agents produced between 2026-06-13 and 2026-08-13, counted from commands rather than memory: 191 registry records, 254 service entities, 35 schemas, 154 fixtures, 60 decision records, and the objective all of it serves.'
date = 2026-08-13T11:00:00-05:00
draft = false
weight = 40
tags = ["intent-os", "operations", "agents", "retrospective"]
categories = ["Development Journey"]
toc = true
+++

Intent OS was created on 2026-06-13. This chapter was written on 2026-08-13. Everything below was
re-derived from a command on that second date, because a number copied from an earlier draft is a
claim, not evidence.

## The count

```
$ git log --since=2026-06-13 --oneline | wc -l
598
```

Five hundred and ninety-eight commits in two months, of a repository that did not exist before
the first one.

| What | Count | Where it comes from |
|---|---|---|
| Commits | 598 | `git log --since=2026-06-13` |
| Dated CHANGELOG entries | 239 | across 44 distinct working days |
| Beads in this repository | 497 | 210 open, 3 in progress, 63 blocked, 280 closed |
| Beads estate-wide | 1,125 open | across 49 databases |
| Filed documents | 173 | `000-docs/` |
| Decision records | 60 | `decision-log/` |
| Evidence bundles | 36 | `evidence/` |
| JSON Schemas | 35 | with 154 fixtures, 80 of them negative |
| Repository records | 191 | schema-valid, 0 duplicate rejects |
| Service entities | 254 | 4 hosts, 4 environments, 246 services |
| Containers | 46 | all healthy on the 2026-08-12 snapshot |
| Declared capabilities | 16 | 8 healthy, 1 degraded, 6 unknown, 1 planned |

239 entries across 44 days works out to about 5.4 discrete pieces of recorded work per active
day. Not 44 days of steady output either: the entries cluster, because the work clusters.

## What the registry actually found

The repository registry is the one number that surprises people, so here is the breakdown from
`registry/INDEX.json`, projected 2026-08-11:

```json
{
  "canonical_count": 191,
  "classification_counts": { "archived": 44, "fork": 53, "unclassified": 94 },
  "duplicate_rejects": 0,
  "raw_unique_count": 191,
  "registry_record_count": 191,
  "schema_valid_count": 191,
  "scope_counts": { "intent-solutions-io": 37, "jeremylongshore": 154 },
  "invariant_ok": true
}
```

191 repositories, and 94 of them unclassified. That is not a governed portfolio, it is a
discovered one, and the difference is the entire B2 work stream. The registry's job at this stage
was to find everything and prove it found everything exactly once: `raw_unique_count`,
`registry_record_count` and `schema_valid_count` all equal 191, with zero duplicate rejects and
the invariant holding.

Counting things correctly turns out to be most of the work. 53 of those repositories are forks
and 44 are archived, and a system that quietly folds those into a headline number produces a
portfolio figure that is technically true and operationally useless.

## The entity projection

254 service entities, built from 250 inventory assets plus 4 synthesized environments. The split
that matters is the observed-state one:

- observed: 138
- intentionally excluded: 59
- known uncollected: 38
- access unavailable: 15

And separately: 112 of 254 are declared but unconfirmed, meaning the desired identity and the
observed state do not match yet.

Four categories of not-observed, each meaning something different. Intentionally excluded is a
decision. Known uncollected is a gap with a name. Access unavailable is a permissions problem.
Collapsing all three into "unknown" would hide which ones are anybody's job.

## The shape of the work

Reading the 60 decision records in order, the arc is not a feature roadmap. It is a slow move
from doing the work to making the work report itself.

The early records are about getting things running: notifications, the brain build, doc filing
conventions. The middle records are about identity and counting: canonical repository identity,
the registry staircase, the corpus census. The late records are about enforcement: the
operational-readiness seven, the capability matrix, the producer rule, drift clustering, and the
declaration store with a fail-closed gate.

One of them, D161, turned the whole philosophy into an admission test that new features have to
pass. Five questions, all of which should answer yes:

1. Does it automatically report into Mission Control?
2. Does it reduce human coordination?
3. Can an agent consume it?
4. Does it emit structured evidence?
5. Does it eliminate a manual checklist?

If not, question whether it belongs. The record is explicit that these are properties of the
output, not measures of effort or novelty, because a feature can be well built, well scoped, and
still fail every one. That is exactly the class the test exists to catch.

## What it is for

The objective is stated in D155, recorded 2026-08-05, and it is the sentence the entire estate
now organizes around:

> The objective is no longer "backup works". It is that the estate reports itself.

Every operational subsystem emits machine-readable health and state into the headquarters, so
executive status is generated automatically rather than assembled by hand. Mission Control
becomes a living headquarters rather than a documentation repository.

The record notes what that reframing does retroactively: it explains and unifies work already
shipped, the reconciler, the collector, the alert floor, the liveness fabric, the projections,
which had accumulated as separate capabilities without an organizing principle. And it converts a
large class of future questions from "go and find out" into "read the projection".

That is the difference between a company that is automated and a company that is legible. Plenty
of estates run automation. The rarer property is that at any moment you can ask what is true and
get an answer that was generated, timestamped, schema-checked, and honest about what it does not
know.

Six of sixteen capabilities cannot yet answer that question about themselves. They are listed by
name, with reasons and bead IDs, on the front page of the cockpit.

That is the number that will be different next time this is counted.
