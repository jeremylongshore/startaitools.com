# 004-OP-RUNB — Blog pipeline: low disk, missed day, quarantine, and syndication recovery

**Owner:** Jeremy (pipeline) · capacity of the dev box `/` filesystem: the backup fabric owner (intent-os `ops/backup/README.md`)
**Applies to:** `scripts/blog/blog-backfill-daily.sh` (04:00), `scripts/blog/blog-land.sh`, `scripts/blog/blog-posting-packet.sh --sweep` (05:00)
**Incident that produced this runbook:** `003-RA-RCAS-blog-backfill-disk-exhaustion-2026-09-04.md`

## 1. What the alerts look like and where the logs are

| Signal | Where | Meaning |
|---|---|---|
| `WARNING (not a failure) blog-backfill-daily: N MiB free ...` | Buzz `sys-automation` (severity `high`) | Free space on `/` is under the 10240 MiB early-warning line. The run went ahead. Free space **today**; under the 4084 MiB admission line the next run refuses. |
| Summary email subject starting `⚠️ DISK N MiB:` | Jeremy's inbox | Same warning, attached to the day's normal summary. |
| `cron job blog-backfill-daily failed: DATE: NO POST — early exit rc=1; reason: disk guard refused ...` | Buzz `sys-automation` (`high`) | The admission line fired. The message carries the date, the reason, free vs admission (floor + run reserve) vs warn, the log path, and the recovery command verbatim. |
| Email `🚨 blog-backfill aborted early: DATE (rc=1) — disk guard refused` | Jeremy's inbox | Same content plus the last 30 log lines. |
| `disk-cleanup` alert `root filesystem still N% full after weekly cleanup` | Buzz `sys-automation` (`high`) | The weekly cleanup could not get `/` under 90%. Capacity work is needed regardless of the blog. |
| Estate dead-man (`automation-liveness-sweep`) | Buzz | `blog-backfill-daily.beat` fresh but `.ok` stale = the job runs and fails. |

Logs: `~/.local/state/blog-backfill-daily/run-YYYY-MM-DD.log` (one per **target** day; the file name is the day that has or lacks a post, not the day the cron fired). Kept 180 days by `prune_run_logs`; nothing else in that directory is ever removed by the pipeline. Lander log: `~/.local/state/blog-land/`. Packet log: `~/.local/state/blog-posting-packet/`.

## 2. First question: can the producer run right now?

```bash
scripts/blog/blog-backfill-daily.sh --disk-check
# free=61731MiB mount=/ admission=4084MiB (floor=500MiB + reserve=3584MiB) warn=10240MiB state=ok   (exit 0)
# ... state=warn (runs, but free space soon)                    (exit 0)
# ... state=BELOW-FLOOR (producer will refuse)                  (exit 1)
```

It reads `df -Pm` on the repo path. No lock, no log, no beat, no alert. The lines it compares against:

| Line | Default | Env override | Behavior |
|---|---|---|---|
| Residual floor | 500 MiB | `BLOG_BACKFILL_DISK_MIN_MB` (producer; values under 500 are raised to 500), `BLOG_LAND_DISK_MIN_MB` (lander) | What must still be free after a run. **Do not lower it to make a run go through.** A `git commit`, a `hugo` build, or an atomic ledger write on a wedged disk fails half-way and leaves a corrupted tree or a torn ledger, which then costs a quarantine and a manual clean-up. The floor is why a full disk costs one day, not the pipeline. |
| Run reserve | 3584 MiB | `BLOG_BACKFILL_RUN_RESERVE_MB` | What one run consumes (measured 2830 MiB, see "Capacity limits"). |
| Admission line | floor + reserve = 4084 MiB | (derived) | The producer refuses below it. Each failover or catch-up child re-checks it. |
| Early warning | 10240 MiB | `BLOG_BACKFILL_DISK_WARN_MB` | Run, warn via Buzz and the email subject. Room for the admission line plus two more runs, so a stalled workspace retirement is seen days before a refusal. |

Units are MiB everywhere (`df -Pm`); `df -h` rounds and must not be used for comparisons.

## 3. Disk-capacity and retention policy for this pipeline

**September 18 correction:** isolated runs introduced full source/Hugo checkouts.
The September 5 small-state measurement below describes the earlier design, not
current capacity. Two native quarantined runs alone occupied about 5.90 GB on
September 18. Completed-checkout retention is verified and journaled; quarantine
and incomplete delivery remain protected. See
`010-OP-RUNB-daily-producer-contract-recovery.md` for admission, census and recovery.

What it writes and how long it lives:

| Path | What | Retention | Who removes |
|---|---|---|---|
| `~/.local/state/blog-backfill-daily/run-*.log` | one run log per target day (≈8 KB) | 180 days | `prune_run_logs`, exact filename `run-YYYY-MM-DD.log` only, inside `~/.local/state` only, window never under 30 days |
| `.blog-quarantine/<stamp>-<slug>/` | the only copy of a post that failed its gates | forever | a human, after triage. Counted every run; WARN at 12 entries (`BLOG_QUARANTINE_MAX_ENTRIES`). Never auto-deleted. |
| `.blog-staging/DATE.intent.json` | readiness sentinel | consumed by the lander on success | lander |
| `/tmp/blog-pipeline.lock` | flock file (0 bytes) | n/a | harmless |
| producer git shim `mktemp -d` | 1 file | run | wrapper (EXIT trap) |
| lander `ASTRO_TMPD` | dual-publish scratch | run | lander |
| External `blog-run-workspaces/.../runs/DATE/UUID/workspace` | full isolated source and generated Hugo files | two eligible completed checkouts, minimum 24 hours since latest completion; protect unfinished/quarantined/dirty/active runs | verified journaled retirement during normal creation |
| External run manifest, logs, quality proof and checkout-evidence archive | durable ownership/audit/recovery evidence | retained after eligible checkout retirement | no automatic evidence pruning |

### Capacity limits (measured 2026-10-05, startaitools-9a8.4.2)

On 2026-10-03 the dev box reached 0 bytes free. Two things stacked: completed run
workspaces had not retired since 09-17 (registry ~45 GB; fixed by PR #118, and
the 10-04 run's `CHECKOUT-RETENTION` line shows a 6.1 GB registry holding only
the two retention-window runs), and several full runs of `tests/` ran at once.

| Workload | Measured peak | How measured | Limit now enforced |
|---|---|---|---|
| One daily producer run | 2830 MiB per run workspace: 1381 MiB checkout + 1449 MiB Hugo `public/` | `du` of a fresh worktree of `origin/master` before and after the lander's exact `hugo --buildFuture --gc --minify --cleanDestinationDir`, sampled each second (no transient overshoot; final = peak). Matches the registry's ~2.95 GB growth per day from 09-21 to 10-01 and the 2830-2833 MiB of each retained run. | Admission line 4084 MiB = 500 floor + 3584 reserve (~25% growth headroom). |
| One full `pytest tests/` run | 4252 MiB of temp trees; 21m56s wall, serial | `pytest tests/ --basetemp <dir>` on `origin/master` (1281 passed, 6 skipped), `du` of the basetemp sampled every 3 s. Pipeline fixtures build git repos and full run workspaces; pytest holds every tree until the session ends, so the peak is about the same at any worker count. | `tests/conftest.py`: needs 5120 MiB (peak + ~20%) free on the temp filesystem, plus the 4084 MiB daily admission line on a host that runs the pipeline (9204 MiB here). |
| Concurrent suites | n x one suite | 43 retained basetemps (11 GB) in `/tmp/pytest-of-jeremy` on 2026-10-05; two 10-04 sessions alone held 3.9 and 3.6 GB | One suite per user at a time (non-blocking `flock`); pytest-xdist capped at `-n 2`, `-n auto` refused. |
| Retained temp trees | was 3 sessions x every test | pytest default retention | `pyproject.toml`: keep only failed tests' trees, latest session only. |

Worst case for one scheduled night is the parent run plus one failover child plus
up to three catch-up dates, each with its own workspace: about 8 x 2830 MiB. That
is not reserved up front on purpose: every child invocation re-runs the guard, so
the night stops at the first child that would cross the admission line, and the
residual floor still holds. Retirement keeps two completed runs, so steady state
is about three workspaces (~8.5 GB).

The suite guards refuse; they never wait or delete. To run a targeted test while
a full suite holds the lock, wait for it. Never free space by deleting `/backup`,
`~/backups`, or another session's live scratch; reclaim from `~/.cache` and abandoned `/tmp` review clones first.

**Historical September 5 shared-disk baseline.** Measured 2026-09-05 on a 387 GB `/`: `/backup` 92 G (own borg repo), `~/backups` 22 G (VPS replica), `/tmp` 34 G (session review clones and scratch), `/var/lib/docker` 10.6 G, `~/.codex` 6.4 G, `~/.rustup` 8 G. The pipeline's whole state directory is 1.2 MB.

**What may be reclaimed, and what may not (from the global operating rules):**

- Safe: `~/.cache/<subdir>` last modified 90+ days ago; abandoned `/tmp` review clones **after** establishing the creating session has ended, the clone has no unpushed commits, and it is a copy of a repository that still exists (record a manifest first: path, size, owner, mtime, kind); dangling docker images; `docker builder prune`.
- Never: `/backup`, `~/backups` (backup stores; see the incident AAR intent-os `000-docs/150`), `~/.local/share/pnpm`, `~/.cache/borg`, any docker **volume** whose owner you have not confirmed, another session's live scratchpad under `/tmp/claude-1000`, `~/.teamkb`, credentials, and the only copy of any log.
- Capacity ownership: growth in `/backup` and `~/backups` belongs to the backup fabric owner; `/tmp` review clones belong to the session that created them (the estate rule "commit early / use worktrees" applies); docker test stacks belong to the repo whose compose file started them.

## 4. Recover a missed day (idempotent; safe to run twice)

Preconditions, in this order:

1. `scripts/blog/blog-backfill-daily.sh --disk-check` exits 0 with a comfortable margin (aim for gigabytes, not the floor).
2. No partial or duplicate artifact for the day:

   ```bash
   D=2026-09-04
   grep -rlE "^date = ['\"]?$D|^date: ['\"]?$D" content/posts/          # expect nothing
   ls .blog-staging/$D.intent.json 2>/dev/null                            # expect nothing
   ls -d .blog-quarantine/*-* | xargs -I{} sh -c 'grep -lE "^date = .?'$D'" {}/*.md 2>/dev/null' # expect nothing
   jq --arg d $D '[.[]|select(.date==$d)]|length' .blog-syndication-ledger.json   # expect 0
   ```

   A quarantined copy for the day means a previous attempt failed its gates: read `~/.local/state/blog-land/` for the reasons first; recovery will produce a fresh post, and the quarantined copy stays as evidence.
3. The lander's own dry run, if you want to see the checks without touching anything: `scripts/blog/blog-land.sh $D --dry-run` (reports `NO-POST` before the producer has run, which is the expected answer at this point).

Run (this is the documented backfill command for one day; it drives the same `claude -p '/blog-backfill D D'` producer, the same git guard, and the same deterministic lander as the 04:00 cron):

```bash
scripts/blog/blog-backfill-daily.sh --date 2026-09-04
scripts/blog/blog-posting-packet.sh --sweep
```

Then verify public publication, external manifest/seal/native proof and canonical delivery/index as described in `000-docs/010-OP-RUNB-daily-producer-contract-recovery.md`; do not trust the exit code or the unchanged owner HEAD:

```bash
D=2026-09-04
# The owner HEAD intentionally stays unchanged. Fetch/read authoritative Git
# publication and the external manifest/seal/proof as documented in runbook010.
git fetch origin master
git log --oneline origin/master -3
python3 scripts/blog/blog-run-workspace.py census \
  --repo "$PWD" --state-dir "$HOME/.local/state/blog-run-workspaces"
jq --arg d $D '[.[]|select(.date==$d)]|length' .blog-syndication-ledger.json   # 1
jq --arg d $D '.[]|select(.date==$d)|{slug,packet_sent,published_at}' .blog-syndication-ledger.json
curl -sfo /dev/null https://startaitools.com/posts/<slug>/ && echo live
tail -5 ~/.local/state/blog-posting-packet/*.log        # one packet email for D, or the heartbeat if it was already sent
```

Running `--date` again for a landed day is a no-op: `published_post_for_date` finds the tracked, unchanged post and the run exits0 only after public/delivery verification, the cross-post sweep and canonical-index reconciliation. Running the packet sweep again sends nothing for a day already marked `packet_sent`.

## 5. Inspect quarantine

```bash
ls -la .blog-quarantine/                    # <UTC-stamp>-<slug> directories
cat .blog-quarantine/<entry>/*.md | head    # the post as produced
grep -h "QUARANTINED\|Reasons" ~/.local/state/blog-land/run-*.log | tail
```

Quarantine is never pruned by automation. Original incident evidence and external quarantined workspaces remain protected; do not treat a later successful reproduction as authority to delete them. Record any separately authorized archival/retirement outcome in Beads with proof and retained evidence. The producer warns when combined original/external quarantine exceeds12 entries; runbook010 describes the external manifest and full-checkout census.

## 6. Scheduler, timezone, target date

- Cron (`crontab -l`): `0 4 * * *` producer, `0 5 * * *` packet sweep. The box's zone is `Etc/GMT+6`: a fixed `-06:00` with **no DST**, which is why every log stamp reads `-06:00` year-round. That is intentional.
- The target day is **yesterday by calendar day** (`resolve_target_date` → `date -d "<now> 1 day ago"`), never "now minus 24 hours". Even on a DST-observing zone the calendar form lands on the right date across the spring-forward and fall-back nights; the invariant tests pin both boundaries with an injected clock (`BLOG_CLOCK`).
- `--date` accepts strict `YYYY-MM-DD`, a real calendar date, not in the future.

## 7. Test the failure path safely

Never fill the real filesystem. The regression suite injects the reading:

```bash
bash scripts/blog/test-pipeline-invariants.sh      # includes the disk-headroom group
scripts/blog/lint-all.sh                            # everything CI runs
```

To watch the wrapper refuse without touching real state, override the floor **upward** for one manual run (this is the only direction the floor is ever moved, and only by hand):

```bash
BLOG_BACKFILL_DISK_MIN_MB=999999999 scripts/blog/blog-backfill-daily.sh --disk-check   # exit 1, state=BELOW-FLOOR
```

(Do not run the full wrapper with that override: it takes the lock, writes a run log for yesterday, and fires the real fail-loud alert.)

## 8. Ownership and follow-ups

- Pipeline behavior, thresholds, retention, this runbook: Jeremy.
- Dev-box capacity (`/backup`, `~/backups`, borg growth, VPS replica growth): backup fabric owner; the decided-not-executed re-home of the B2 origin (intent-os decision-log/043) would move 22 G off this disk.
- `/tmp` hygiene for review clones: the estate cross-session rules; a retention rule for abandoned clones is an open follow-up.
- Borg non-zero exits are not alerted today; open follow-up (see the incident record §9).
