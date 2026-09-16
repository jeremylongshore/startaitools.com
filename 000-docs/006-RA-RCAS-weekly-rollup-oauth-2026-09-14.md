# Weekly growth rollup missed, September 14, 2026

## Impact and UTC timeline

The Monday team growth report was not produced or sent. The wrapper ran at 2026-09-14 14:00:02 UTC and invoked `claude -p` at 14:00:03. At 14:00:11 the CLI returned `Failed to authenticate: OAuth session expired and could not be refreshed` with exit 1. The wrapper found no usable HTML, recorded a failed outcome, withheld its success heartbeat, and sent the established failure alert to Jeremy at 14:00:12. The syndication ledger reconciliation had already aged 25 rows to `assumed_posted`; those are beliefs with provenance, not posting receipts.

## Cause and earlier repairs

`scripts/blog/blog-team-rollup.sh` still depended on an interactive Claude OAuth access token for its unattended Monday job. That token expires while no interactive session refreshes it. The posting packet had already documented and removed the same headless OAuth dependency by using a static SOPS-backed MiniMax provider. The September 13 daily blog producer repair addressed its separate job; it did not change the weekly rollup. Disk pressure and the September 12 quarantined blog post were independent alert families, not causes of the September 14 rollup failure.

## Corrective action and verification

The weekly report generator now uses the estate's existing MiniMax Anthropic-compatible Claude toolchain by default. It resolves the key from the protected SOPS file in-process, never puts it in command arguments or logs, gives the generator a finite deadline, requires a substantive HTML file, and treats missing credentials as failure without silently falling back to interactive OAuth. An explicit `ROLLUP_PROVIDER=claude` remains available for attended use. `ROLLUP_DRY_RUN=1` skips ledger mutation, team mail, alerts and live success markers while retaining the generated HTML for review.

The offline regression replaces mail, ledger and alert destinations with disposable fixtures: the old generator fails when its simulated OAuth session is expired; the corrected generator receives the static key, creates HTML, and sends no mail. A missing key fails visibly. `test-pipeline-invariants.sh` runs this regression in CI. A real MiniMax no-mail dry run ended at 2026-09-16 02:00:17 UTC after 522 seconds, created a 23,800-byte HTML fragment with weekly comparison tables, visitors, UTM and a re-share nomination, and sent no team mail. A targeted no-mail replay for the missed September 14 window ended at 02:08:34 UTC after 342 seconds, produced 14,134 bytes with portfolio and all four site rows, weekly/monthly comparisons, UTM and a re-share nomination. This validates generator access and the HTML gate without pretending the missed Monday mail was delivered.

## Detection, recovery and rollback

The existing Monday cron and liveness/alert-floor signals remain active. If the rollup fails, inspect `~/.local/state/blog-team-rollup/run-YYYY-MM-DD.log` for the provider exit, credential and HTML gate; check the SOPS key reference without printing its value. Reproduce safely with `ROLLUP_DRY_RUN=1 ROLLUP_DATE=2026-09-14 ROLLUP_LOG_DIR=/tmp/weekly-rollup-check bash scripts/blog/blog-team-rollup.sh`; review `dryrun-YYYY-MM-DD.html`. Do not send a generated report to the team without reviewing it and the authorized mail workflow. Revert the corrective source commit to roll back; this changes no schema, persistent content, ledger format, or credential.

The no-mail dry run establishes provider access and HTML generation; the next scheduled Monday run is still a real-event verification point. Existing failure alerts must remain enabled until that receipt exists.
