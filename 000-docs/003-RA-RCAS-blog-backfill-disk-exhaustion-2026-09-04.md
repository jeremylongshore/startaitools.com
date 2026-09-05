# 003-RA-RCAS — Daily blog producer refused on a full disk; no post for 2026-09-04

**Type:** Root-cause analysis + recovery record
**Incident window:** 2026-09-05 04:00:02 -06:00 (producer refusal) → recovery the same morning
**Impact:** startaitools.com had no post for 2026-09-04 and no syndication packet for that day. No corruption, no partial publish, no duplicate. TeamKB compile for the same window was healthy and is not part of this incident.
**Authored by:** Jeremy's Claude session, 2026-09-05. Evidence paths are on the dev box (`team-server`).

## 1. Timeline (all times -06:00, the box's fixed zone)

| When | What | Evidence |
|---|---|---|
| 2026-07-26 → 2026-08-30 | Weekly `disk-cleanup` logs `/` at 90% → 97% → 99% → 89% → 100% → 97% → 100%. It trims docker/journal/apt/snap only and never alerts. | `~/.local/state/disk-cleanup/cleanup.log` |
| 2026-08-04 → 2026-09-03 | Nightly borg backup exits non-zero on 8 of 31 nights (exit 1/2), including 08-30, 08-31, 09-01, 09-03. The 09-02 line is even truncated mid-write. | `~/.backups/backup.log` (root) |
| 2026-09-05 02:00–02:12 | borg create/prune runs (adds 1.32 GB unique). | `journalctl -u borg-backup.service` |
| 02:45–02:48 | devbox borg push: source size **90 G** (documented as 40 G). | `~/.local/state/devbox-borg-push/push.log` |
| 03:30–03:32 | VPS replica pull OK, replica **22 G** (documented as 10 G). | `~/.local/state/borg-replica/pull.log` |
| 03:30–03:44 | TeamKB compile: 27 candidates, 26 promoted, audit chain ok. Its scratch is 68 MiB under `/tmp/teamkb-compile`; its backup at 04:34 stages 271 MB in `/tmp` and removes it. **Not a contributor.** | `~/.local/state/teamkb-compile-daily/run-2026-09-04.log` |
| **04:00:02** | `blog-backfill-daily.sh` starts, target 2026-09-04. `disk_guard` reads **217 MiB** free on `/` against the 500 MiB floor and refuses. Fail-loud trap fires (Buzz + email). rc=1. | `~/.local/state/blog-backfill-daily/run-2026-09-04.log` |
| 04:00–04:02 | B2 offsite push runs normally. | `~/.local/state/borg-offsite/push.log` |
| 05:00 | Packet sweep runs normally; nothing to send for 09-04 (no ledger entry). | packet log |
| 08:50 | First measurement of this investigation: `/` 87% used, **52 GB free**. | `df` |

## 2. Direct cause

The producer's hard floor did its job. `disk_guard` (`scripts/blog/lib-cron-common.sh`) reads `df -Pm` (MiB), saw 217 < 500, logged `FATAL: only 217MiB free on / (need 500MiB) — refusing to run`, and exited 1 before the lock-protected generation, commit, build, or ledger write could start. The units, the comparison, and the exit path are correct; the regression tests added with this record pin all three.

## 3. Underlying cause

The root filesystem of the dev box (387 GB) has been operating within roughly 1 GB of full since mid-August. Nothing single-handedly filled it; four growth sources with no cap and no early warning did:

| Consumer | Documented | Measured 2026-09-05 | Growth |
|---|---|---|---|
| `/backup/borg-repository` (this box's own borg repo) | 40 G | **92 G** | 74 G on 07-31 → 90 G on 09-05 (≈0.45 GB/day of new unique data; per-archive original set grew 97 G in April → 140 G in August) |
| `~/backups/vps-borg-replica` (the VPS repo, pulled nightly) | 10 G | **22 G** | 10 G on 08-05 → 22 G on 09-04 (≈0.4 GB/day; the VPS repo itself is doubling monthly) |
| `/tmp` | transient | **34 G** | 38 review clones/copies of intent-os (≈10 G) written by one session on 2026-09-03 evening and abandoned; 3.5 G of session scratchpads; 232 `tmp.*` leftovers (2.7 G); 1.6 G cad-dxf clones |
| `/var/lib/docker` | — | 10.6 G | 4 orphaned 1 GB Postgres volumes from test stacks, 388 MB dangling images |

Backup material alone (114 G, 30% of the disk) plus temp debris (34 G) left the daily writers fighting over the last gigabyte. The weekly cleanup could not touch any of it and reported `100% -> 100%` without alerting.

**What changed, to answer "we never had this before":** early August. The dev-box borg repo crossed 74 G on 07-31 and the VPS replica started growing 1 G every 2–3 days from 08-05. The weekly log goes 90% (07-26) → 97% (08-02) → 100% (08-16). Backup growth is the dominant new load; the `/tmp` review-clone burst on 09-03 is what pushed the last gigabyte over the edge for the 09-05 04:00 run.

## 4. The unexplained part, stated plainly

Between 04:00 (217 MiB free) and 08:50 (52 GB free) roughly 50 GB became free, and this investigation did **not** find the process that released it. Checked and excluded: journal vacuum, tmpfiles-clean, apt autoremove (removed one small package at 06:06), docker events, the TeamKB backup (271 MB staged and removed), the Dolt reaper (one idle server), the self-hosted runners (no jobs), deleted-but-open files (only memfd), every Claude/Codex session log between 04:00 and 08:50 (none ran a reclaim), and shell history (empty for the window). The best-supported inference, not a proven fact: a transient consumer between the 02:00 borg run and 04:00 (the replica pull's rsync of a 22 G repo, or the borg create itself, can double-hold segments mid-copy) plus a manual or session cleanup after 08:30 that left no log. This is recorded as a follow-up, and the new early warning at 2 GiB exists precisely so the next approach to the floor is observed rather than reconstructed.

## 5. Contributing factors

- **No warning tier anywhere.** The producer only spoke at the floor; the weekly cleanup logged and stayed silent; the liveness sweep watches beats, not headroom.
- **Retention was documented in numbers that were no longer true** (`/backup` 40 G, `~/backups` 10 G in the global CLAUDE.md and the intent-os backup README). Nobody re-measured because nothing alerted.
- **Review clones in `/tmp` have no owner and no retention**, and `/tmp` is on `/`.
- **Borg failures were not surfaced.** Eight non-zero nights in a month is exactly the signal a full disk gives first.
- **The fail-loud alert was terse:** "early exit rc=1 — NO POST. Check log" gave the date and rc but not the reason, the capacity, or the recovery command.

## 6. What was and was not wrong in the pipeline

- 500 MiB floor: correct value, correct units, correct behavior. Not changed.
- Target date: `date -d yesterday` is calendar-day arithmetic; the box is `Etc/GMT+6` (fixed offset, no DST). The `-06:00` in the log is intentional. Now formalized in `resolve_target_date` with an injectable clock and DST-boundary tests.
- Idempotency: `published_post_for_date` only accepts a tracked, unchanged post; untracked debris is refused. Unchanged, now covered by recovery tests.
- Retry: the producer cannot self-recover a missed day (no auto-catchup, by design). Recovery is a manual, idempotent rerun of the same wrapper for the exact date.

## 7. Resolution

**Capacity (2026-09-05 morning).** 38 abandoned review clones/copies in `/tmp` (owner: a finished partner-network session; git clones with zero unpushed commits or plain tree copies; 2 days old; rebuildable) were removed from an allowlisted manifest, plus two dangling docker images from 2025. `/` went from 52,724 MiB free (87%) to 62,001 MiB free (85%); inodes 44.8 M → 46.1 M free. Manifest preserved at `~/.local/state/blog-backfill-daily/reclaim-2026-09-05-manifest.txt`. Nothing under `/backup`, `~/backups`, docker volumes, scratchpads of possibly-live sessions, or `tmp.*` of unknown owners was touched.

**Prevention (this change).**
- `disk_guard` gains an early-warning tier (default 2048 MiB) and exports the reading for alerts; floor semantics unchanged and documented as non-negotiable in code.
- Producer: `--date YYYY-MM-DD` (idempotent exact-day recovery through the same guards), `--disk-check`, warning via Buzz `high` and the email subject, fail-loud alert now carries target date, reason, capacity, log path, and the recovery command.
- Bounded footprint: run logs pruned after 180 days by exact filename only (`prune_run_logs`, refuses anything outside `~/.local/state`, refuses windows under 30 days); quarantine counted and warned at 12 entries, never deleted.
- Weekly `disk-cleanup` (deployed at `~/bin/disk-cleanup.sh`, root cron.weekly) now raises a Buzz `high` alert when `/` is still ≥ 90% after cleanup.
- Regression coverage: `scripts/blog/test-pipeline-invariants.sh` gains disk-headroom (below/at/above floor and warning line, message content, legacy caller, alert helper, and a negative mutant test), target-date (DST boundaries, strict `--date`), retention (allowlist, refusals, idempotency, quarantine census), and recovery (exact date, rerun, partial state, ledger count) groups.

**Recovery of 2026-09-04.** See §8; the runbook is `004-OP-RUNB-blog-low-disk-recovery.md`.

## 8. Recovery evidence

Filled in by the recovery run on 2026-09-05; see the run log `~/.local/state/blog-backfill-daily/run-2026-09-04.log` (the refusal lines at the top are preserved as the incident trail, the recovery appends below them).

Prevention merged first (PR #67 → v1.17.9, CI: shellcheck, ruff, voice-lint, invariants, hugo build all green), then the real checkout was fast-forwarded so the wrapper's own preflight pull was a no-op (bash must never read a script that changes underneath it), then the documented one-day recovery ran from the real checkout.

| Step | Command / check | Result |
|---|---|---|
| Headroom | `blog-backfill-daily.sh --disk-check` | `free=56775MiB ... state=ok` |
| Pre-state | post / sentinel / quarantine / ledger / queue for 2026-09-04 | none / none / none / 0 / 0; lock free; `claude -p` answered |
| Dry run | `blog-land.sh 2026-09-04 --dry-run` | `LAND-RESULT: NO-POST` (expected before the producer) |
| Recovery | `blog-backfill-daily.sh --date 2026-09-04` | rc=0 after 1117 s; producer `claude -p /blog-backfill 2026-09-04 2026-09-04` exited cleanly after 960 s; `LAND-RESULT: OK`; `Overall STATUS: OK`; summary email sent |
| Post | `content/posts/project-subagents-load-at-session-start.md`, `date = 2026-09-04T08:00:00-05:00`, Tier 1, 1046 words | exactly **1** file for the date |
| Commits | `08415245 post(2026-09-04): Claude Code Subagents Load at Session Start, Not at Commit (Tier 1)` then `31cece54 assets(2026-09-04): social image and cards ...` | one post commit, one assets commit, `HEAD == origin/master`; release automation cut v1.17.10 and v1.17.11 |
| Live | `https://startaitools.com/posts/project-subagents-load-at-session-start/` | HTTP 200 after 60 s liveness probe; title served |
| Sentinel / quarantine | `.blog-staging/2026-09-04.intent.json` / `.blog-quarantine/` | consumed / still 4 entries, no new entry |
| Ledger after land | `jq '[.[]|select(.date=="2026-09-04")]|length'` | **1** (`packet_sent: false`) |
| Sweep | `blog-posting-packet.sh --sweep` | rc=0, 68 s: `Packet emailed to ezekiel@intentsolutions.io (1 post(s))`, `marked packet_sent`, Plane card HTTP 201, `end (1 packet(s))` |
| Ledger after sweep | same query | **1**, `packet_sent: true` |
| Idempotent rerun | `blog-backfill-daily.sh --date 2026-09-04` again | rc=0 in 10 s: `Published post already covers 2026-09-04 ... generation is a no-op`; no new commit |
| Idempotent sweep | `--sweep` again | `No unpacketed posts ... end (0 packets)`; heartbeat only |
| Final state | posts=1, ledger=1, quarantine=4, tree clean apart from pre-existing untracked drafts | no duplicate post, ledger entry, or packet |

The 05:00 sweep that morning had already logged `GAP: no ledger entry for 2026-09-04 — the 04:00 producer likely failed; alerting.`, so the syndication side detected the miss on its own; that gap alert is the intended dead-man for the producer.

Disk during recovery: 56,775 MiB free at start, 61,239 MiB after (other sessions' churn dominates the difference; the pipeline's own delta is the post, its image assets, and one 8 KB log).

## 9. Remaining risks and follow-ups

1. **Backup growth is the load-bearing problem and is out of this repo's hands.** `/backup` (92 G) and `~/backups` (22 G) need a decision from the backup owner: re-measure the intent-os backup README numbers, explain why the VPS repo doubled since August, and set a size budget. Re-homing the B2 origin to the home server is already decided (intent-os decision-log/043) and would move the replica off this disk.
2. **Borg exit codes are not alerted.** Eight failures in a month were only visible in a root-owned log.
3. **`/tmp` review clones need an owner and a retention rule** at the estate level; this incident removed one session's debris by hand with a manifest. 3.5 G of scratchpads and 232 `tmp.*` files remain because their owners could not be established safely.
4. **The 50 GB release is unexplained** (§4).
5. Docker: 4 orphaned Postgres volumes (≈4 G) from longbox test stacks; left in place pending owner confirmation.
6. `.blog-staging/` still holds two stale sentinels (2026-07-15, 2026-07-27) and `content/posts/` an untracked 2026-07-27 post; pre-existing, outside the pipeline's write-set at run time, left untouched.
