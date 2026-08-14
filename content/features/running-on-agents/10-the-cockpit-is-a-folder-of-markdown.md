+++
title = 'The Cockpit Is a Folder of Markdown'
slug = 'the-cockpit-is-a-folder-of-markdown'
description = 'Mission Control governs 191 repositories and 254 service entities with nine generated Markdown pages, four cron collectors, no server and no database. Here is why that shape was chosen and what keeps it honest.'
date = 2026-08-13T08:00:00-05:00
draft = false
weight = 10
tags = ["intent-os", "mission-control", "operations", "agents"]
categories = ["Architecture"]
toc = true
+++

Ask anyone to picture the control plane for 191 repositories, 46 running containers and 254
service entities, and they will describe a web application. Sidebar of services. Traffic lights.
A time-series chart nobody reads. Probably a login page.

Intent OS has none of that. Mission Control is a directory of Markdown files in a git repository.
Nine of them regenerate under a single command. There is no server, no database, no UI, and no
API. You read it with `cat`, or on GitHub, or by asking an agent to read it, which is the case
that actually matters.

The page says so about itself, in its own header:

> The estate cockpit. One screen that points at everything live: the generated status pages
> below, the session narrative, and the maps. This page asserts almost nothing itself, and a page
> that is mostly links can't drift much.

That last clause is the whole design.

## The nine pages

Each page is a projection of something real, generated and never hand-written. As of the
2026-08-12 snapshot:

| Page | What it projects |
|---|---|
| `open-work.md` | Every beads database's open, in-progress and blocked counts, estate-wide |
| `drift-report.md` | Drift findings, dossier freshness, the manual re-verify checklist |
| `eval-strip.md` | Nightly eval gate decisions from signed evidence manifests |
| `service-entities.md` | The service, host and environment projection from estate inventory |
| `deployment-state.md` | Per-repo deploy verdicts plus the VPS fleet's container state |
| `capability-matrix.md` | One row per declared capability, composed from the others |
| `health.md` | Per-service health from Netdata alarms plus container run state |
| `ownership-coverage.md` | Who owns what across the portfolio |
| `ci-release-status.md` | Per-repo CI and release status from direct GitHub reads |

A tenth, `estate-graph.md`, regenerates under its own command because a graph projector is not a
status sweep.

Four collectors feed them on cron, all America/Chicago: the work-sync reconciler at 05:20, CI and
release status at 05:40, deployment state at 05:50, health projection at 05:55. By the time
anyone is awake, the pages describe this morning.

## Why Markdown and not a dashboard

Three reasons, in the order they actually mattered.

**An agent can read it.** This is the load-bearing one. The estate is operated by agents at least
as often as by a human. A dashboard is a hostile interface to a language model: it is HTML
wrapped around an API you have to discover, authenticate to, and paginate. A Markdown table in a
git repo is one `Read` call. Every generated page also emits a schema-validated JSON twin for the
same reason, so an agent that wants structure does not have to parse a table.

**Git gives you history for free.** Every regeneration is a diff. What changed in the estate
between Tuesday and Wednesday is `git diff`, with no time-series database, no retention policy,
and no separate backup story. The pages are in the same repository as the decisions that produced
them.

**There is no server to keep alive.** A status page that goes down during an incident is worse
than no status page, because now you are debugging two things. A file cannot be down.

The capability matrix states the constraint plainly: it is a **truth table, not a dashboard**. It
composes the other projections and collects nothing itself.

## The part that makes it safe

A generator that fails is the obvious failure mode. If the collector cannot reach the VPS, the
renderer produces an honest page that says it has no runtime state. Committing that page would
replace a good projection with a blank one, and a blank status page reads as calm.

So the orchestrator refuses to promote it. The rule in `scripts/mission-control.sh` is that a
renderer's honest "no runtime state" placeholder must never replace a previously good committed
page. Absent state counts as a failed generation, so the previous page survives. The test is one
function:

```bash
page_live() {
  [ -s "$1" ] && ! grep -q 'No projection available\|No composed matrix available\|No coverage projection available' "$1"
}
```

The renderers stay honest, because a fresh checkout with no runtime state genuinely has no data
and should say so. The orchestrator is what decides whether that honest page is allowed to
overwrite yesterday's good one. It is not. The previous page survives, and the run prints which
generator failed.

The full flow is generate into a scratch directory, gate the scratch copies, then promote:

```bash
if ! bash ci/disclosure-gate.sh --paths "${gate_args[@]}"; then
  # (failure message elided: it reports that nothing was promoted, and that
  #  a flagged word means a real leak in some repo's tracked beads export)
  exit 1
fi
mkdir -p mission-control
for p in "${ok_pages[@]}"; do mv -f "$SCRATCH/$p" "mission-control/$p"; done
```

Nothing reaches the working tree until it has passed a disclosure scan. The scan runs on the
scratch copies, so a leak is caught before it is ever a tracked file, which is the only point at
which catching it is cheap.

Two more guards sit in front of that. The orchestrator refuses to write at all if the branch is
not one of the expected ones, and refuses if the working tree is dirty outside `mission-control/`.
In either case it degrades to printing the pages on stdout rather than writing them. You still
get your answer. You just do not get a surprise commit on top of work in progress.

There is one carve-out, and it is documented in the code rather than discovered later. The beads
telemetry log `.beads/interactions.jsonl` is written by every `bd` invocation, so counting it as
dirt would block regeneration after any bead work at all. It never feeds the generated pages, so
the dirty-tree check ignores it the same way it ignores `mission-control/` itself.

## What it looks like when it runs

The capability matrix on 2026-08-12 reported 16 declared capabilities: 8 healthy, 1 degraded, 6
unknown, 1 planned. That is not a great score, and it is not supposed to be. Six unknowns are six
subsystems that work fine but cannot yet prove it to the cockpit, each one carrying the bead ID
that will fix it. The planned row renders with empty cells rather than being hidden.

An unfillable row is evidence of a gap, which is the subject of chapter three.

## The honest cost

Regeneration is deliberate, never automatic. There is no hook, and the pages carry a snapshot
timestamp with a note to re-run if it is older than about three days. That means the cockpit can
be stale, and staleness is visible rather than prevented.

That was the trade. Automatic regeneration on a hook would mean the pages churn on every commit,
every conflict becomes a merge conflict in generated content, and the git history stops being
readable. The rule instead is that you never hand-merge a generated page: take either side and
re-run.

For a one-operator estate, a cockpit that is occasionally three days stale and always trustworthy
beats one that is always current and sometimes wrong. That preference is not universal. It is
just correct here, and knowing which one you are optimizing for is most of the decision.
