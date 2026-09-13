# Daily blog producer authentication and incomplete fallback, September 13

## Impact and evidence

The September 12 post did not land. At September 13 10:00:02 UTC the producer measured 538MiB free, above its 500MiB refusal floor and below its 2048MiB warning. That warning correctly surfaced a separate capacity risk. No ENOSPC marker was found in this run, and Hugo and voice lint passed; disk pressure is not the demonstrated cause of this missed post.

At 10:00:12 UTC Claude started; at 10:00:19 it failed because its OAuth session had expired and could not refresh. The MiniMax shell-agent fallback then used all 120 turns in 596 seconds. At 10:10:15 it returned turn-exhaustion status. At 10:10:56 the deterministic lander refused missing readiness sentinel, classification, agent audit and pattern-engine receipt, preserving the draft in quarantine. This was correct containment. The posting sweep reported no landed post at 11:00 UTC.

Private source evidence: `~/.local/state/blog-backfill-daily/run-2026-09-12.log`, `~/.local/state/blog-land/land-2026-09-12.log`, and the timestamped quarantine folder. Existing unrelated draft and layout edits were preserved.

## Earlier repairs and recurrence

The July producer/lander inversion prevented incomplete drafts from being published. The July static MiniMax shell fallback and later cron PATH fix restored provider access when interactive credentials expired. The September 5 disk warning, log retention and exact-date recovery work (PR67, RCA003) improved detection and recovery; it did not remove expiring authentication from the producer or provide the fallback with the full Agent toolchain. The backup exclusions subsequently reduced the measured local borg repository from92GiB to40GiB; the filesystem remains under independent pressure from other consumers.

The old wrapper read `$?` after the completed `if` statement, so failures from all three producers were recorded as `exit 0`. This hid the actual distinction between authentication failure, timeout and turn exhaustion.

## Correction

The automatic producer uses the already reviewed MiniMax Anthropic-compatible Claude transport (compiler fb96c06/#180), preserving the complete Skill/Agent toolchain. A small Python launcher loads the existing static key into only the child environment, overrides the provider and model aliases there, and leaves OAuth files and global settings untouched. Automatic failure stays visible; it does not retry through the shell-only harness that lacks mandatory agent tools. Explicit OAuth and legacy modes remain available, with the latter still subject to every publication gate. No turn limit or publication gate is relaxed. The original deadline, pipeline lock, read-only Git shim, classification/audit requirements and final lander are unchanged.

All producer functions capture the exit status in their `else` branch. MiniMax status2 is turn exhaustion; status3 and outer timeout124 are deadlines.

## Verification and operational limits

Six executable function regressions reproduce the old exit-zero bug and pass after the change. Credential tests prove parent environment isolation, key-free command arguments and refusal without a configured key. A seventh wrapper regression prevents automatic fallback to the tool-incomplete legacy producer. The full Python suite passes 175 tests with one existing opt-in live-image smoke skipped; the shell pipeline invariant suite passes. ShellCheck and Ruff pass with the repository's actual configuration. Initial CI caught two line-length errors hidden by the sparse checkout's missing `pyproject.toml`; restoring that tracked configuration and correcting the lines made the same gate pass locally. Live harmless probes authenticate as MiniMax-M3; a real subagent invocation is recorded in `/tmp/blog-minimax-task-probe-20260913.jsonl`.

These probes verify provider/tool availability, not the recovered article. The exact-date recovery remains `scripts/blog/blog-backfill-daily.sh --date 2026-09-12`; the lander must independently verify the completed artifact and public URL. Recovery receipts and publication proof will be appended after execution.

## Rollback and remaining risk

Revert the source commit or explicitly select `BLOG_PRODUCER=claude` to restore OAuth behavior, understanding that the observed expired session remains unusable until separately refreshed. No database/schema migration or credential mutation is required. Preserve quarantine, logs and append-only methodology. Do not forge a readiness sentinel, lower the disk floor, or publish an incomplete draft to obtain a green job.

Host headroom is tracked separately by existing P1 capacity work. Provider or content-review failure remains possible; the lock, finite deadline, quarantine, failure notifications and independent no-post sweep must remain active.
