# Verified numbers ledger: running-on-agents

Every figure used in the four chapters, with the command that produced it and the date it was
run. Contract 116 rule: counts are evidence, never constants. Re-run before any edit that
restates a number.

All commands run from `~/000-projects/intent-os` unless noted. Derived **2026-08-13**.

## Volume

| Figure | Value | Command |
|---|---|---|
| Commits since intent-os was created | 598 | `git log --since=2026-06-13 --oneline \| wc -l` |
| Commits total | 605 | `git log --oneline \| wc -l` |
| Dated CHANGELOG entries | 239 | `grep -cE '^### 20[0-9]{2}-' CHANGELOG.md` |
| Distinct days with entries | 44 | `grep -oE '^### 20[0-9]{2}-[0-9]{2}-[0-9]{2}' CHANGELOG.md \| sort -u \| wc -l` |
| First / last entry | 2026-06-13 / 2026-08-13 | same, `sort \| head -1` and `tail -1` |
| Filed docs | 173 | `ls 000-docs/*.md \| wc -l` |
| Decision-log files | 60 (59 numbered 001-058, plus 006a) | `ls decision-log/ \| wc -l` |
| Evidence bundles | 36 | `ls evidence/ \| wc -l` |

Note: 239 entries over 44 active days is roughly 5.4 entries per working day. The plan's
"242 sessions" figure did not survive re-derivation; entries are not sessions, and the
CHANGELOG heading count includes non-dated headings.

## Beads

| Figure | Value | Command |
|---|---|---|
| intent-os beads total | 497 (210 open, 3 in progress, 63 blocked, 280 closed) | `bd stats` in intent-os |
| Estate open | 1,125 | `mission-control/open-work.md` totals line |
| Estate in progress / blocked / deferred | 42 / 4 / 148 | same |
| Databases | 49 | same |
| Active now | 46 | `mission-control/open-work.md` "Active now" heading |
| startaitools beads | 91 total, 14 open | `bd stats` in startaitools |

Snapshot date on open-work.md: 2026-08-12.

## Registry (B1)

From `registry/INDEX.json`, `projected_at` 2026-08-11T07:15:07Z:

- canonical_count 191, raw_unique_count 191, registry_record_count 191, schema_valid_count 191
- duplicate_rejects 0, invariant_ok true
- scopes: jeremylongshore 154, intent-solutions-io 37
- classification: archived 44, fork 53, unclassified 94
- `ls registry/repository-record.v0/ | wc -l` = 191

## Fleet and entities

| Figure | Value | Source |
|---|---|---|
| Service entities | 254 (4 host, 4 environment, 246 service) | `mission-control/service-entities.md` |
| Built from | 250 inventory assets + 4 synthesized environments | same |
| Declared but unconfirmed | 112 of 254 | same |
| Observed-state split | observed 138, intentionally_excluded 59, known_uncollected 38, access_unavailable 15 | same |
| Containers healthy | 46 (0 degraded, 0 unknown) | `mission-control/health.md`, observed 2026-08-12T07:36:55Z |
| Containers in deploy view | 46 on host intentsolutions | `mission-control/deployment-state.md`, observed 2026-08-12T08:05:38Z |
| Declared capabilities | 16 (8 healthy, 1 degraded, 6 unknown, 1 planned) | `mission-control/capability-matrix.md`, snapshot 2026-08-12T09:20:48Z |
| Ownership coverage | 191 discovered, 0 governed, 191 not yet declared | `mission-control/ownership-coverage.md` |

## Contracts

| Figure | Value | Command |
|---|---|---|
| JSON Schemas | 35 | `find schemas -name '*.schema.json' \| wc -l` |
| Fixtures total | 154 | `find schemas/fixtures -name '*.json' \| wc -l` |
| Negative fixtures | 80 | `find schemas/fixtures -name 'invalid*' \| wc -l` |
| if/then conditionals, 4 operational schemas | 22 | python walk of `schemas/operational/*.json` |
| health-projection.v0 conditionals | 7 | same |
| estate-capability-matrix.v0 conditionals | 7 | same |
| ci-release-status.v0 / deployment-state.v0 | 4 / 4 | same |

## Mission Control shape

- 9 pages regenerate under `pnpm mc` (README table rows)
- estate-graph.md regenerates under `pnpm estate-graph:mc`
- 4 cron sweeps feed them: work-sync-reconciler 05:20 CT, ci-release-status 05:40,
  deployment-state 05:50, health-projection 05:55 (all America/Chicago)
- write guard at `scripts/mission-control.sh:281-291`: scratch, gate, promote
- absent-state promote-guard at `scripts/mission-control.sh:202`

## Workstation, 2026-08-13

| Figure | Value | Command |
|---|---|---|
| Concurrent claude processes | 14 | `ps -eo comm= \| grep -c '^claude$'` |
| tmux sessions | 12 | `tmux ls \| wc -l` |
| iPad on tailnet | active, relay "nyc" | `tailscale status` |

## Blog

- 338 posts: `ls content/posts/*.md | wc -l` in startaitools

## CUT claims (did not survive verification)

1. **"Two independent observers count the container fleet and fail loudly if they disagree
   (46 and 46)."** No such reconciliation exists. Both the health page and the deployment-state
   page read the same fence-ratified fleet collector, so they are one observer reported twice.
   The real two-endpoint design is narrower and lives in
   `ops/health-projection/collect.py:63`: Netdata `/info` and `/alarms` are read as two
   independent endpoints with two independent failure states, so an `/info` failure cannot
   discard usable `/alarms` data. Chapter 3 uses that instead, accurately.
2. **"242 recorded sessions."** Re-derives to 239 dated CHANGELOG entries across 44 days.
3. **"497 beads in this repo alone"** (in a startaitools context). 497 is intent-os. The
   startaitools database holds 91.
4. **"61 decision records", "173 filed docs", "34 schemas", "141 fixtures".** Actual: 60
   decision-log files, 173 docs (this one held), 35 schemas, 154 fixtures.
