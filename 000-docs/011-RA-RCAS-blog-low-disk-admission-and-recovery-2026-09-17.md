# 011-RA-RCAS — Daily producer could not create its isolated run on low disk; no post for 2026-09-17 until a same-day recovery

**Type:** Root-cause analysis + recovery record, written after the fact from retained evidence
**Incident window:** 2026-09-18 04:00:02 -06:00 (run creation failed) → 2026-09-18 23:19:05 -06:00 (recovered posts packeted)
**Impact:** The 2026-09-17 post did not land at 04:00, and the 05:00 posting-packet sweeps on 2026-09-16, 09-17 and 09-18 sent no packet (gap alerts only), because the 2026-09-15 and 2026-09-16 drafts had also been quarantined by the earlier contract incident (RCA 219 in the operations repository). No partial publish, no duplicate, no packet was sent for an unpublished post. All three missed dates were recovered the same evening and packeted at 23:19 -06:00.
**Authored:** 2026-10-05 from the logs, run registry, ledger and tracking notes listed in section 8. Evidence paths are on the dev box. Two capacity receipts recorded at the time under `/tmp` were purged with `/tmp` and are cited only by the numbers the tracking notes preserved.

## 1. Timeline (all times -06:00, the box's fixed zone)

| When | What | Evidence |
|---|---|---|
| 2026-09-16 04:16 / 09-17 04:17 | Producer runs for 09-15 and 09-16 exit after quarantine (`LAND-RESULT: QUARANTINED`, rc=10). Their completion contract failures are the earlier incident, not this one. | `run-2026-09-15.log`, `run-2026-09-16.log` |
| 2026-09-16, 09-17, 09-18 05:00 | Packet sweep: `GAP: no ledger entry for <yesterday>`, gap alert sent, `0 packets`. | `packet-2026-09-16.log` … `packet-2026-09-18.log` |
| **2026-09-18 04:00:02** | Daily run for 09-17 starts. `WARN: 1036MiB free on / is under the 2048MiB early-warning line (hard floor 500MiB)`. | `run-2026-09-17.log` lines 1-2 |
| 04:00:06 | Run registry writes a manifest for run `0438e537` (`created baseline=3aa5662f`). | run `0438e537` `run.log` |
| **04:00:41** | `FATAL: isolated run creation failed; owner work preserved`; fail-loud alert sent; rc=1. No worktree was created. | `run-2026-09-17.log` line 3-4 |
| 17:39:11 | When the first recovery run starts, run `0438e537` is marked `abandoned before worktree creation; manifest and logs retained`; its registry status is now `quarantined`, so no orphan active run remains. | run `0438e537` `run.log` (23:39:11 UTC) |
| 17:39–17:50 | Recovery attempts on release v1.17.39 (`3aa5662f`). Run `5dceed8d`: the MiniMax-transport producer stops at Claude Code's `unrecognized_model` guard with no artifacts. Run `18df819b` (shell fallback) is quarantined by the lander. | `run-2026-09-17.log` lines 5-1746 |
| 17:56–18:04 | Run `14b55cf8` (source `7b673a8a`) is interrupted; run `80123858` on v1.17.40 (`aefb70c4`) with the Grok fallback declines the governed producer contract and is stopped. | lines 1747-1787 |
| **18:10:24** | Admission now refuses with an actionable message: `workspace admission refused: available_bytes=2263351296 required_free_bytes=3389947904 registry_bytes=8763478016 protected_bytes=8763158528`. | line 1789-1790 |
| ~18:12 | Six quarantined run checkouts (8.66 GB) removed with `git worktree remove --force`; manifests, quarantines, logs and branches retained; 10.5 GB free. | tracking note on the incident bead |
| 18:12–18:48 | Runs `36cbdb62` and `679b62a4` (v1.17.41, `624f80fd`) fail the run write-set integrity check before landing; nothing published. | lines 1799-1902 |
| 20:44–22:27 | Recovery chain (`rerun-chain-20260918*.sh`). Skill instructions fast-forwarded to `63a5aa2` at 20:44:25. 09-15 run `619cb2d6` commits `c8891fa4`; 09-16 run `b2eff4c0` commits `5fc3eae0`. Both landers report `FAILED (source published; public article unavailable; delivery pending)` because the deploy had not caught up within the liveness window. | `rerun-chain-20260918.log` |
| 21:42 | MiniMax five-hour window exhausted (HTTP 429); remaining dates use the explicit `BLOG_PRODUCER=claude` mode, same gates. | `rerun-chain-20260918b.sh` header |
| **22:54–23:15** | 09-17 run `25e9c640` (source `ee3864ce`, v1.17.45): `PRODUCER-CONTRACT: complete`, committed `6f801cf3`, `Liveness OK`, `LAND-RESULT: OK`, `Overall STATUS: OK`; ledger entry recorded. | `run-2026-09-17.log` lines 1935-2010 |
| **23:16–23:19** | Manual run of the established packet sweep: three posts packeted, `marked packet_sent` for 09-15, 09-16 and 09-17. | `packet-2026-09-18.log` |
| 2026-09-19 04:00 | First scheduled run after recovery: 09-18 run `55a0462a` `LAND-RESULT: OK`; 05:02 sweep sends its packet. | `run-2026-09-18.log`, `packet-2026-09-19.log` |

## 2. Direct cause (inferred; no stderr retained)

At 04:00 the root filesystem had 1036 MiB free. The disk guard correctly let the run proceed (above the 500 MiB floor, below the 2048 MiB warning). The isolated-run creator wrote its manifest at 04:00:06 and failed at 04:00:41 with only `isolated run creation failed`. No stderr from that step was kept, and the release that ran (v1.17.39, `3aa5662f`) had no admission check. Reproducing the failure would mean filling the production disk again, so it was not attempted. The cause is therefore inferred: the timing fits a failed `git worktree add` on a nearly full disk, but the 04:00 run does not prove it. The byte-count refusal at 18:10 came from a later release that added admission. That release required 3.39 GB free (twice the tracked checkout plus a reserve) when 2.26 GB was available.

## 3. Underlying cause

Isolated per-run checkouts, introduced by the 2026-09-17 contract work, keep failed and quarantined runs on disk as evidence. Each retained checkout with its generated `public/` tree costs roughly 1.4 GB. Two days of quarantined failures, plus retained recovery attempts, consumed the headroom the 2026-09-04 disk cleanup had restored (see RCA 003). The 500 MiB floor was sized for the old in-place producer, not for a producer that needs a multi-gigabyte workspace before it starts.

## 4. Contributing factors

- The 04:00 failure message did not say how many bytes were needed or available. The admission refusal at 18:10 does.
- The registry left a `creating` manifest for the failed 04:00 run until the next run marked it abandoned at 17:39 (23:39 UTC).
- Recovery attempts on older releases exposed separate defects (MiniMax model-catalog guard, a fallback that cannot honour the producer contract, the transcript-based role-completion check). Each was contained by quarantine or the write-set check; none published.
- The MiniMax usage window ran out mid-recovery.

## 5. What was and was not wrong

The disk floor, quarantine, lander gates and gap alerts all behaved as designed: no incomplete draft was published and each missed morning raised an alert. The packet sweep never sent a packet for a post that had not landed. What was wrong was capacity planning for retained run evidence, and a run-creation error that did not carry its numbers.

## 6. Resolution

- Workspace admission (added after v1.17.39) reports `available_bytes`, `required_free_bytes`, `registry_bytes` and `protected_bytes` on refusal (in place by 18:10 on 2026-09-18).
- Bounded retention of completed isolated checkouts (keep two eligible checkouts for at least 24 hours; quarantined, unfinished and changed checkouts stay protected), shipped in the 2026-09-18 release series; see the CHANGELOG section "September 18 production recovery boundary corrections".
- Run diagnostics moved outside the publication checkout (issue #84, PR #80) with the paired skill-instruction change (claude-skills-private #10/#11, merge `c7c47a47`).
- Role completion decided from staged role outputs and a hash-bound roles receipt (#86, paired with claude-skills-private #12).
- One-off capacity recovery: generated `public/` trees pruned from three quarantined workspaces (4,347,653,651 bytes) and six quarantined checkouts removed; manifests, quarantines, logs and branches retained.

## 7. Recovery evidence

| Content date | Recovered by run | Post commit | Ledger | Packet |
|---|---|---|---|---|
| 2026-09-15 | `619cb2d6-1ea7-48fb-97b4-ebb5f56b59f9` | `c8891fa4` | published_at 2026-09-19T03:27:25Z | sent 2026-09-18 23:19:05 |
| 2026-09-16 | `b2eff4c0-000a-4ae7-866e-35547cd7e6d5` | `5fc3eae0` | published_at 2026-09-19T04:21:19Z | sent 2026-09-18 23:19:05 |
| 2026-09-17 | `25e9c640-621d-4ea6-8620-bcdde7100be7` | `6f801cf3` | published_at 2026-09-19T05:11:22Z | sent 2026-09-18 23:19:05 |

No date was given up. The nightly catch-up planner later listed all three as `published` (first seen in the 2026-09-21 run: `"published": ["2026-09-17", "2026-09-18", "2026-09-19"]`, `"gave_up": []`).

Later scheduled runs: 2026-10-02 run `05fc7cd4` and 2026-10-03 run `94c4389b` both reached `PRODUCER-CONTRACT: complete`, `LAND-RESULT: OK` and `Overall STATUS: OK`, and their 05:00 sweeps marked the packets sent. On 2026-10-04 the read-only disk check reported `state=ok` with tens of GiB free (43863 MiB at 20:12 -06:00).

## 8. Evidence

- `~/.local/state/blog-backfill-daily/run-2026-09-15.log`, `run-2026-09-16.log`, `run-2026-09-17.log`, `run-2026-09-18.log`, `rerun-chain-20260918.log`
- `~/.local/state/blog-posting-packet/packet-2026-09-16.log` through `packet-2026-09-19.log`
- `~/.local/state/blog-run-workspaces/f3a63e261675b536b391/runs/2026-09-17/0438e537-ed0e-43e5-be62-49f066384adf/{manifest.json,run.log}`
- `.blog-syndication-ledger.json` rows for 2026-09-15, 09-16 and 09-17
- `~/.claude/skills` reflog: fast-forward to `63a5aa2` at 2026-09-18 20:44:25 -06:00

## 9. Remaining risks and follow-ups

- Retained quarantine still accumulates; the run census warns `QUARANTINE OVER LINE` daily. Retention protects evidence by design, so the operator must review and retire quarantines through the runbook (004, 010), not by deleting checkouts.
- `blog-posting-packet.sh --sweep --dry-run` still sends the "pipeline healthy" heartbeat email when nothing is queued: the heartbeat branch does not check `DRY_RUN`. Use date mode for dry runs until that is fixed. In dry-run mode the log line `Packet emailed to …` is also printed even though nothing was sent.
- The `[claude-code:unrecognized_model]` warning still appears in every MiniMax-transport run. It no longer stops the producer, but it is noise that can hide a real failure.

## Rollback

Code rollback is a reviewed revert through the normal release path, paired with the matching skill-instruction revert. A rehearsal on disposable clones (2026-10-04) showed both reverts (the #80 diagnostics commit `09ab7b25` here and `c7c47a47` in the skill repository) touch only the expected files and conflict only in `CHANGELOG.md`. The rehearsal was mechanical: conflicts were not resolved and no tests were run on the reverted trees. Never roll back by deleting quarantine, manifests or ledger rows.
