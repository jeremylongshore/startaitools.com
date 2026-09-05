# 004-OP-RUNB — Blog pipeline: low disk, missed day, quarantine, and syndication recovery

**Owner:** Jeremy (pipeline) · capacity of the dev box `/` filesystem: the backup fabric owner (intent-os `ops/backup/README.md`)
**Applies to:** `scripts/blog/blog-backfill-daily.sh` (04:00), `scripts/blog/blog-land.sh`, `scripts/blog/blog-posting-packet.sh --sweep` (05:00)
**Incident that produced this runbook:** `003-RA-RCAS-blog-backfill-disk-exhaustion-2026-09-04.md`

## 1. What the alerts look like and where the logs are

| Signal | Where | Meaning |
|---|---|---|
| `WARNING (not a failure) blog-backfill-daily: N MiB free ...` | Buzz `sys-automation` (severity `high`) | Free space on `/` is under the 2048 MiB early-warning line. The run went ahead. Free space **today**; under 500 MiB the next run refuses. |
| Summary email subject starting `⚠️ DISK N MiB:` | Jeremy's inbox | Same warning, attached to the day's normal summary. |
| `cron job blog-backfill-daily failed: DATE: NO POST — early exit rc=1; reason: disk guard refused ...` | Buzz `sys-automation` (`high`) | The floor fired. The message carries the date, the reason, free vs floor vs warn, the log path, and the recovery command verbatim. |
| Email `🚨 blog-backfill aborted early: DATE (rc=1) — disk guard refused` | Jeremy's inbox | Same content plus the last 30 log lines. |
| `disk-cleanup` alert `root filesystem still N% full after weekly cleanup` | Buzz `sys-automation` (`high`) | The weekly cleanup could not get `/` under 90%. Capacity work is needed regardless of the blog. |
| Estate dead-man (`automation-liveness-sweep`) | Buzz | `blog-backfill-daily.beat` fresh but `.ok` stale = the job runs and fails. |

Logs: `~/.local/state/blog-backfill-daily/run-YYYY-MM-DD.log` (one per **target** day; the file name is the day that has or lacks a post, not the day the cron fired). Kept 180 days by `prune_run_logs`; nothing else in that directory is ever removed by the pipeline. Lander log: `~/.local/state/blog-land/`. Packet log: `~/.local/state/blog-posting-packet/`.

## 2. First question: can the producer run right now?

```bash
scripts/blog/blog-backfill-daily.sh --disk-check
# free=61731MiB mount=/ floor=500MiB warn=2048MiB state=ok      (exit 0)
# ... state=warn (runs, but free space soon)                    (exit 0)
# ... state=BELOW-FLOOR (producer will refuse)                  (exit 1)
```

It reads `df -Pm` on the repo path. No lock, no log, no beat, no alert. The two lines it compares against:

| Line | Default | Env override | Behavior |
|---|---|---|---|
| Hard floor | 500 MiB | `BLOG_BACKFILL_DISK_MIN_MB` (producer), `BLOG_LAND_DISK_MIN_MB` (lander) | Refuse. **Do not lower it to make a run go through.** A `git commit`, a `hugo` build, or an atomic ledger write on a wedged disk fails half-way and leaves a corrupted tree or a torn ledger, which then costs a quarantine and a manual clean-up. The floor is why a full disk costs one day, not the pipeline. |
| Early warning | 2048 MiB | `BLOG_BACKFILL_DISK_WARN_MB` | Run, warn via Buzz and the email subject. |

Units are MiB everywhere (`df -Pm`); `df -h` rounds and must not be used for comparisons.

## 3. Disk-capacity and retention policy for this pipeline

**The blog pipeline's own footprint is bounded and tiny.** What it writes and how long it lives:

| Path | What | Retention | Who removes |
|---|---|---|---|
| `~/.local/state/blog-backfill-daily/run-*.log` | one run log per target day (≈8 KB) | 180 days | `prune_run_logs`, exact filename `run-YYYY-MM-DD.log` only, inside `~/.local/state` only, window never under 30 days |
| `.blog-quarantine/<stamp>-<slug>/` | the only copy of a post that failed its gates | forever | a human, after triage. Counted every run; WARN at 12 entries (`BLOG_QUARANTINE_MAX_ENTRIES`). Never auto-deleted. |
| `.blog-staging/DATE.intent.json` | readiness sentinel | consumed by the lander on success | lander |
| `/tmp/blog-pipeline.lock` | flock file (0 bytes) | n/a | harmless |
| producer git shim `mktemp -d` | 1 file | run | wrapper (EXIT trap) |
| lander `ASTRO_TMPD` | dual-publish scratch | run | lander |

**The disk is shared, and the pipeline is the loudest victim, not the cause.** Measured 2026-09-05 on a 387 GB `/`: `/backup` 92 G (own borg repo), `~/backups` 22 G (VPS replica), `/tmp` 34 G (session review clones and scratch), `/var/lib/docker` 10.6 G, `~/.codex` 6.4 G, `~/.rustup` 8 G. The pipeline's whole state directory is 1.2 MB.

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

Then verify, do not trust the exit code:

```bash
D=2026-09-04
git log --oneline -3                                    # post(2026-09-04): ... commit present once
grep -rlE "^date = ['\"]?$D" content/posts/ | wc -l     # 1
ls .blog-quarantine/ | tail -3                          # no new entry for D
jq --arg d $D '[.[]|select(.date==$d)]|length' .blog-syndication-ledger.json   # 1
jq --arg d $D '.[]|select(.date==$d)|{slug,packet_sent,published_at}' .blog-syndication-ledger.json
curl -sfo /dev/null https://startaitools.com/posts/<slug>/ && echo live
tail -5 ~/.local/state/blog-posting-packet/*.log        # one packet email for D, or the heartbeat if it was already sent
```

Running `--date` again for a landed day is a no-op: `published_post_for_date` finds the tracked, unchanged post and the run exits 0 after the cross-post sweep. Running the packet sweep again sends nothing for a day already marked `packet_sent`.

## 5. Inspect quarantine

```bash
ls -la .blog-quarantine/                    # <UTC-stamp>-<slug> directories
cat .blog-quarantine/<entry>/*.md | head    # the post as produced
grep -h "QUARANTINED\|Reasons" ~/.local/state/blog-land/run-*.log | tail
```

Quarantine is never pruned by automation. When an entry has been triaged (re-produced, or judged not worth publishing), remove it by hand and say so in the day's bead or commit. The producer warns when the directory holds more than 12 entries.

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
