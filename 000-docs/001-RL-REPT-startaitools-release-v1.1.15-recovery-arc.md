# Release Report: startaitools.com v1.1.15 (recovery arc v1.1.9 – v1.1.15)

## Executive Summary

- **Version span**: v1.1.9 → v1.1.15 (auto-tagged by `release.yml`; this ceremony cut no manual tag by design, to avoid colliding with the repo's push-triggered release automation)
- **Release date**: 2026-08-04
- **Type**: patch series (fixes + content + docs)
- **Ceremony**: /repo-sweep + /release run after a full pipeline-outage recovery
- **Approved by**: Jeremy (interactive gates, this session)

## What This Arc Contains

### The outage and its three root causes
1. **2026-08-01 missed post**: local `pull.rebase=true` routed the preflight's `git pull --ff-only` through the rebase path, which refuses the deliberately carried dirty `.beads/interactions.jsonl`. Fixed in code: `-c pull.rebase=false` (f5a6358c).
2. **2026-08-02/03 missed posts**: an uncommitted 12-file refactor of `scripts/blog/` (the estate Buzz alert-floor cutover) tripped the dirty-tree guard. Completed and committed (aef7b908).
3. **Deploys failing since 2026-08-01**: no Tailscale WIF credentials on the repo because the estate Tailscale API token had expired (90-day TTL) with re-mint pending as an owner action. Restored: fresh credential in sops, per-repo federated trust (subject `repo:jeremylongshore/startaitools.com:*`), secrets set, push-triggered deploys verified green (run 30883438310 and every push since). Also fixed 124 root-owned `.git` objects + root-owned `dist/` dirs on the VPS that broke even manual deploys.

### Recovered content
- 2026-08-01 · "The Version Number That Only Existed on the Client" (Tier 2)
- 2026-08-02 · "When Live Numbers Argue Back" (Tier 1)
- 2026-08-03 · "The Check That Only Confirmed a Name" (Tier 2, produced by the cron-identical pipeline run)

All three landed with classifier records, tier-appropriate quality gates, audit addenda, dual-publish to tonsofskills, ledger + crosspost-queue entries.

### Proof of unblocked pipeline
Cron-identical run (2026-08-04 ~00:25) passed preflight, produced, landed, auto-deployed, and went live end-to-end. One defect surfaced: the producer violated the producer/lander boundary by invoking the lander itself around the git-guard shim; the wrapper's HEAD-moved check caught it (tracked: bead `startaitools-18b`, P1).

## Sweep Results (Phase 0)
- Merged: #56 (actions/checkout 7.0.1), #57 (actions/setup-python 7.0.0) — CI green, squash.
- Pruned: 21 dead local branches. Left: `ops/web-analytics-minimax-deterministic-email` (unmerged WIP), `minimax-test2` stash, other sessions' untracked drafts.
- Scaffolding: all standard files present. Secrets scan: clean.

## Documentation Currency (Phase 2)
- README: dead Netlify placeholder badge → live Actions deploy badge; hosting/deployment rewritten to the VPS contract; post count 290+ → 325+ (actual 329).
- CLAUDE.md: automation table synced to the live crontab (backfill 07:00→04:00, packet 08:30→05:00); post counts refreshed; stale README gotcha retired.
- CHANGELOG: curated Keep-a-Changelog consolidated entry added above the auto-generated sections (0000e315).

## Quality Gates

| Gate | Status |
|------|--------|
| Hugo build (local + CI gate) | ✓ |
| Voice lint (all new posts) | ✓ |
| Secrets scan | ✓ |
| Version consistency (version.txt = tag = changelog) | ✓ v1.1.15 |
| Deploy smoke (`/healthz` + title verification) | ✓ |
| Gist currency | deferred by owner decision (no gist exists; daytime pass) |

## Known Conformance Gap
`release.yml`'s auto-changelog writes one-line commit dumps, not Keep-a-Changelog sections; a strict §2.6 gate would block manual releases. Mitigated this cycle with the curated consolidated entry. Upgrading the generator is an optional follow-up (not filed; low value while the automation is the tag owner).

## Rollback

Content/docs commits are individually revertable (`git revert <sha>` + push → auto-deploy). Deploy rollback: Netlify remains DNS-flippable during the soak per the cutover runbook; VPS serves from `origin/master` so a revert push is the primary path.

## Timeline (America/Chicago)
- 22:0x 08-03 · outage diagnosed; Buzz cutover committed; Aug 1+2 posts produced/landed via manual pipeline
- 23:5x 08-03 · VPS ownership rot fixed; manual deploy; posts live
- 00:1x 08-04 · Tailscale credential refreshed (owner) → WIF trust minted → auto-deploy restored
- 00:25 08-04 · cron-identical pipeline run → Aug 3 post live end-to-end
- 01:0x-08:2x 08-04 · sweep, docs currency, curated changelog, v1.1.14/v1.1.15 auto-releases verified
