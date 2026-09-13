# Daily blog producer authentication and incomplete fallback, September 13

## Impact and evidence

The September 12 post did not land. At September 13 10:00:02 UTC the producer measured 538MiB free, above its 500MiB refusal floor and below its 2048MiB warning. That warning correctly surfaced a separate capacity risk. No ENOSPC marker was found in this run, and Hugo and voice lint passed; disk pressure is not the demonstrated cause of this missed post.

At 10:00:12 UTC Claude started; at 10:00:19 it failed because its OAuth session had expired and could not refresh. The MiniMax shell-agent fallback then used all 120 turns in 596 seconds. At 10:10:15 it returned turn-exhaustion status. At 10:10:56 the deterministic lander refused missing readiness sentinel, classification, agent audit and pattern-engine receipt, preserving the draft in quarantine. This was correct containment. The posting sweep reported no landed post at 11:00 UTC.

Private source evidence: `~/.local/state/blog-backfill-daily/run-2026-09-12.log`, `~/.local/state/blog-land/land-2026-09-12.log`, and the timestamped quarantine folder. Existing unrelated draft and layout edits were preserved.

## Earlier repairs and recurrence

The July producer/lander inversion prevented incomplete drafts from being published. The July static MiniMax shell fallback and later cron PATH fix restored provider access when interactive credentials expired. The September 5 disk warning, log retention and exact-date recovery work (PR67, RCA003) improved detection and recovery; it did not remove expiring authentication from the producer or provide the fallback with the full Agent toolchain. The September 5 backup exclusions remain installed, but retained archives do not immediately shrink when new-source exclusions change. The complete September 13 census measured the local Borg repository at 100,366,032,896 bytes (93.47GiB). The initial version of this report incorrectly repeated a partial 40GiB measurement; it did not prove reclamation. Borg independently hit ENOSPC at 08:07 UTC and failed at 08:08 UTC; that earlier backup failure does not replace the demonstrated authentication/toolchain cause of the 10:00 blog failure.

The old wrapper read `$?` after the completed `if` statement, so failures from all three producers were recorded as `exit 0`. This hid the actual distinction between authentication failure, timeout and turn exhaustion.

## Correction

The automatic producer uses the already reviewed MiniMax Anthropic-compatible Claude transport (compiler fb96c06/#180), preserving the complete Skill/Agent toolchain. A small Python launcher loads the existing static key into only the child environment, overrides the provider and model aliases there, and leaves OAuth files and global settings untouched. Automatic failure stays visible; it does not retry through the shell-only harness that lacks mandatory agent tools. Explicit OAuth and legacy modes remain available, with the latter still subject to every publication gate. No turn limit or publication gate is relaxed. The original deadline, pipeline lock, read-only Git shim, classification/audit requirements and final lander are unchanged.

All producer functions capture the exit status in their `else` branch. MiniMax status2 is turn exhaustion; status3 and outer timeout124 are deadlines.

## Verification and operational limits

Six executable function regressions reproduce the old exit-zero bug and pass after the change. Credential tests prove parent environment isolation, key-free command arguments and refusal without a configured key. A seventh wrapper regression prevents automatic fallback to the tool-incomplete legacy producer. The full Python suite passes 175 tests with one existing opt-in live-image smoke skipped; the shell pipeline invariant suite passes. ShellCheck and Ruff pass with the repository's actual configuration. Initial CI caught two line-length errors hidden by the sparse checkout's missing `pyproject.toml`; restoring that tracked configuration and correcting the lines made the same gate pass locally. Live harmless probes authenticate as MiniMax-M3; a real subagent invocation is recorded in `/tmp/blog-minimax-task-probe-20260913.jsonl`.

The repair merged as PR70 (`7c243826`) at 20:03:57 UTC. Hosted Python/lint/Hugo/preview checks passed. The canonical cron checkout fast-forwarded to the repaired source, preserving the hashes of all 12 pre-existing user files. A full local Hugo build in memory passed with 2185 pages and 797 processed images, without another 1.4GiB output copy.

`scripts/blog/blog-backfill-daily.sh --date 2026-09-12` ran the configured producer from 20:04:49 to 20:15:21 UTC (632 seconds). The real session invoked independent Agent tools. The lander verified the readiness sentinel, classifier, audit addendum, pattern-engine receipt, voice lint and Hugo build. Its structural length gate reduced the classifier's Tier 2 to Tier 1; no gate was waived. It committed the post as `608b7bae`, pushed image assets as `4956abbb`, and dual-published to tonsofskills as `2ac44bc77`. The lander returned zero and the daily run ended OK at 20:17:51 UTC.

At 20:18:02 UTC the [public September 12 post](https://startaitools.com/posts/sealing-a-168-bead-planning-graph-took-three-reviews-and-a-seven-seat-council/) returned HTTP200 with the exact title, date and slug and `Cache-Control: no-cache, no-store, must-revalidate`. Its VPS deployment workflow34780212367 succeeded. The repeat exact-date run at 20:18:59 UTC recognized the existing post and performed no generation. The established posting-packet job sent the one recovered post at 20:20:17 UTC, marked `packet_sent`, and created its existing workflow card at 20:20:23 UTC. Private receipts are under `~/.local/state/intent-os/alert-review/20260913T193100Z/blog/`; the original failed draft remains in quarantine.

This proves one real missed-day recovery and repeat-run idempotency. It does not prove that a future unattended cron run has completed; the existing fail-loud and no-post checks remain responsible for detecting recurrence.

## Rollback and remaining risk

Revert the source commit or explicitly select `BLOG_PRODUCER=claude` to restore OAuth behavior, understanding that the observed expired session remains unusable until separately refreshed. No database/schema migration or credential mutation is required. Preserve quarantine, logs and append-only methodology. Do not forge a readiness sentinel, lower the disk floor, or publish an incomplete draft to obtain a green job.

Host headroom is tracked separately by existing P1 capacity work. Provider or content-review failure remains possible; the lock, finite deadline, quarantine, failure notifications and independent no-post sweep must remain active.
