# 018-RA-RCAS — One rejected push stranded the 2026-11-03 post and the admission gate refused every run for nine days

**Type:** Root-cause analysis + recovery record, written from retained evidence on the dev box
**Incident window:** 2026-11-04 05:06:07 -06:00 (push rejected) → 2026-11-13 00:35 -06:00 (gate cleared); catch-up of the nine missed dates followed
**Impact:** No post landed for 2026-11-03 through 2026-11-12 (ten calendar days). The 2026-11-03 post was produced, sealed and committed but never published; 2026-11-04..12 were never produced. Two emails went out every night; none named the cause or an actionable command.
**Authored:** 2026-11-13 from `~/.local/state/blog-backfill-daily/run-*.log`, `~/.local/state/blog-land/`, the run registry under `~/.local/state/blog-run-workspaces/`, and GitHub run annotations. Times are the box's fixed -06:00.
**Related:** `011-RA-RCAS-blog-low-disk-admission-and-recovery-2026-09-17.md` (same gate, different trigger); `004-OP-RUNB-blog-low-disk-recovery.md` §4b (the recovery procedure this incident added).

## 1. Timeline

| When | What | Evidence |
|---|---|---|
| 11-04 04:00–05:05 | Run for 2026-11-03: the producer timed out once on the MiniMax transport (45 min), self-repaired in round 2; post sealed Tier 1, all gates pass. | `run-2026-11-03.log` |
| 11-04 05:06:03 | `blog-land.sh` committed `b766d0f6` on the run branch (post + 2 decision lines). | same |
| **11-04 05:06:07** | **Bare `git push origin HEAD:refs/heads/master` rejected: `[remote rejected] HEAD -> master (Internal Server Error)`**. One attempt, no retry. `LAND-RESULT: FAILED (orphaned local commit)`, rc 11, alert "manual push needed". | `~/.local/state/blog-land/*2026-11-03*` line 37 |
| 11-05 → 11-12, 04:00 nightly | `blog-run-workspace.py create` finds the 11-03 manifest ACTIVE, `recover_abandoned` sees the commit is not on remote master, sets `pending_publication`, and **refuses the new run**: `previous committed run needs publication reconciliation`. The wrapper's abnormal-exit alert reads "isolated run creation/admission failed; inspect logged validation and capacity evidence". Catch-up children are refused by the same gate. | `run-2026-11-0{4..11}.log`, run `6fb27c2e` `run.log` |
| 11-06, 11-08, 11-09 | Separately, GitHub hosted jobs on the personal account did not start: *"The job was not started because your account is locked due to a billing issue"* (startaitools Release on 11-08, comehomealabama deploys on 11-06/09). Lint and tests were green locally; nothing on master deployed between 11-04 and 11-13. Hosted jobs started again on 11-11. The 11-04 push rejection is plausibly the same lock beginning. | `gh api .../check-runs/<id>/annotations` |
| 11-13 00:30 | Hand push of the stranded commit (rebased onto `09ed607b`, pushed as `58ce6ab8`); Release green; post live (HTTP 200). | this session |
| 11-13 00:36 | `--date 2026-11-04` still refused: after the rebase, `validate(committed=True)` measured the run's write set as `baseline_sha..HEAD`, which now also contained the 11-08 feedback-sweep commit — `feedback append belongs to another slug or run`. | run `6fb27c2e` manifest `recovery_error` |
| 11-13 00:35 | The 11-03 run record quarantined (its post was already live); gate clear; sequential catch-up queue for 11-04..12 started on the Claude producer. | `~/.local/state/blog-run-workspaces/.../2026-11-03/.../manifest.json` |

## 2. Root cause

A single push attempt decided the day, and a stranded commit stopped the pipeline until a human intervened.

1. **No retry on the post push.** `blog-land.sh` pushed once; a transient remote rejection (here a GitHub 500) became "orphaned local commit". The image push already used `push_with_rebase` after the 2026-08-18 race; the post push, which decides the day, did not.
2. **The admission gate refused instead of reconciling.** `recover_abandoned` verified a committed, sealed run and, finding it not on remote master, retained it as `pending_publication` and refused every later `create` — by design "refusing to discard committed run", but with no attempt to publish what the lander was about to publish.
3. **Rebase was impossible without breaking the run's own checks.** `validate()` measures the write set as `baseline_sha..HEAD`, and the quality seal binds `baseline_sha`, so even the "manual push" the alert asked for left the run unreconcilable and the gate still closed.
4. **The alert hid the reason and never escalated.** The abnormal-exit path used the wrapper's stage label; the helper's JSON error (naming the stranded run and its manifest) only reached the log. Nine identical emails, two per night, with a printed recovery command the gate would refuse. The consecutive-failure escalation lived only on the normal summary path.
5. **Catch-up could not help.** Its window was 3 days and it ran behind the same gate.

This is the third incident of the class: 2026-08-18 (image push race, fixed with `push_with_rebase`), 2026-10-31 (post push raced the release bot, pushed by hand 2026-11-01), 2026-11-04 (this one). Each earlier fix addressed one push path; none changed the two structural facts above.

## 3. Recovery performed

1. Pushed the stranded commit by hand from the run workspace (rebase onto `origin/master`, push); verified Release/deploy green and the article live.
2. Quarantined the 11-03 run record with the reason recorded (its content was already published; the record could not be reconciled under the old `validate()`); its delivery rows (ledger/packet/cross-post) did not run automatically, as for 2026-10-31.
3. Ran the nine missing dates as a sequential queue (`blog-backfill-daily.sh --date D`, oldest first, waiting for the release bot to settle between dates, Claude producer), then `blog-posting-packet.sh --sweep`.

## 4. Changes (bead `startaitools-5p0`)

| # | Change | Where |
|---|---|---|
| 1 | The post push retries: `push_post_with_retry` (fetch; rebase through the workspace helper when the remote moved; backoff on a transient rejection; exhaustion is the only stranded outcome). | `lib-cron-common.sh`, `blog-land.sh` |
| 2 | `recover_abandoned` reconciles a committed, sealed, pushable run (rebase, re-baseline, push, verify) before refusing; `reconcile --manifest` does the same by hand and is the command the refusal names; `rebase-onto-remote --manifest` is the lander's retry step. The manifest records `sealed_baseline_sha` and every `rebases[]` entry; the seal verifier matches the baseline it was produced on. | `blog-run-workspace.py`, `blogpipe/publication.py` |
| 3 | The abnormal-exit alert carries the helper's real reason in the subject and body, names the matching recovery command, and escalates after two consecutive failed runs. | `blog-backfill-daily.sh` |
| 4 | Catch-up window 3 → 14 days. | `blog-backfill-daily.sh` |
| 5 | Release: a content-only push releases even when `verify` is red (fail-safe `scope` job). | `.github/workflows/release.yml` |
| 6 | Tests: sandbox proof of the retry (rejected first push lands on attempt 2; dead remote gives up), reconcile of a sealed unpushed run (and refusal of an unsealed one / dead remote), the abnormal-exit alert text and escalation. | `test-pipeline-invariants.sh`, `tests/` |

Not changed here: the outside-in "days since the last post landed" liveness row lives in intent-os (dev-box sweep), tracked there; the GitHub billing lock is an owner account matter.

## 5. What would have caught it earlier

- A second night with the same refusal is an outage, not a second incident: the escalation now fires on the abnormal-exit path.
- The subject line now carries the helper's error, so "needs publication reconciliation; evidence: …manifest.json" is readable from a phone.
- With change 2 the 2026-11-05 run would have reconciled the 11-03 commit itself and produced its own post; the outage would have been one night.
