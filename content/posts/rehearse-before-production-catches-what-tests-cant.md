+++
title = 'Rehearse the deploy, not the test suite'
slug = 'rehearse-before-production-catches-what-tests-cant'
date = 2026-10-01T08:00:00-06:00
draft = false
tags = ['deployment', 'release-engineering', 'devops', 'production', 'rehearsal']
categories = ['DevOps']
description = 'A production deploy rehearsal runs the deploy as the deploy user. It caught a folder-permission bug in catalyst-onboarding the test suite could not.'
tldr = 'Rehearsing the catalog one step at a time before production caught a folder-permission bug that no test could have caught. The discipline is rehearsing what the deploy actually does, not what the test suite says it does, and the rehearsal script should cover rollback, sending-switch-on, hashed-data restore, and every other pre-deploy switch that the deploy script itself touches.'
+++

## The finding

A ten-scenario rehearsal on the dev box caught a real production-breaking bug before it left the staging network. The bug was a folder-permission mistake in the deploy script: the directory the database process needed to write to was created with the wrong owner, and the database would not have started on the VPS. The test suite had nothing to say about it. The rehearsal said it on attempt two.

The rest of this post is the discipline behind that rehearsal: what to script, what to run, and what to refuse to merge until the rehearsal passes.

## What the rehearsal actually was

A production deploy package for `catalyst-onboarding` had shipped a full self-hosted runner: a deploy check, a staging test, a restore drill. The CI was green. Two independent reviewers still stopped the PR with two blockers and three should-fix items:

- Rollback after migration. The readiness probe would refuse to come up unless the schema matched the migration head baked into the image. Roll back a migrating deploy and the app is half-switched, reading a new schema from an old binary.
- Backup step with no time limit. The new database backup command had no timeout, so a wedged backup could hang the nightly server backup, which would also hang, which would also fail the morning check.

The three should-fix items: a backdoor that could turn email sending on without a recorded approval, a failed redeploy that would roll back onto the same broken version, and image versioning hygiene (no tag that pinned the version, so the runner could drift).

The builder fixed all five. CI was green again. Then the real test: the deploy package ran, in full, on the dev box, with the real encrypted secrets, against a clean staging instance. The cases:

1. Deploy. Upgrade with a database change. Roll back. Verify the older image accepts the new schema exactly one revision forward, and the new image refuses the old one.
2. Sending switch. Try to turn email sending on without the recorded approval. The deploy script refused.
3. Failed redeploy. Cut the network mid-deploy. The runner stopped safely. The previous version stayed up.
4. Bad version. Push a tag that does not exist. The deploy rolled itself back inside the time budget.
5. Backup under a locked database. The backup step gave up in 3 seconds. The nightly backup continued.
6. Restore drill from the encrypted dump. Rebuilt the database from the backup, verified row counts, swapped it in, and rolled the change back cleanly.

And case seven is the one I remember. The deploy script, on a clean target directory, created the data folder, the journal folder, the temp folder, and the upload folder. The data folder had the wrong owner. The deploy script wrote the right thing, then the systemd unit started, and the database process died on the first write with permission denied, on a path the test suite had never touched. The test suite ran as the test user, which owned everything.

No test would have caught it. All four layers ran as one identity. The unit tests, the integration tests, and the CI runner all used the same test-user. The deploy script runs as a different user, on a fresh directory, with permissions the test environment never reproduced. The rehearsal reproduces them, because the rehearsal runs the deploy script the way production will.

That is the lesson. Tests check what the code does. The rehearsal checks what the deploy does. Those are not the same question.

## Why the discipline exists

A deploy is not a single command. It is a sequence of side effects: a directory created, a service file installed, a port opened, a database migration applied, a health check called, the old version stopped, the new version started, the load balancer re-pointed, the old version left running for a window in case the new one is bad. Every one of those steps has a small chance of failing in a way no test layer exercises. A unit test cannot simulate a half-applied schema migration because it sees a single schema, applied once, never rolled back. An integration test cannot simulate a deploy that creates a directory owned by a different user because the integration test assumes the same identity throughout. The rehearsal is the only place where the deploy runs the way it will run, with the permissions it will have, against the filesystem state it will have to create.

## What the rehearsal script should cover

A rehearsal script for a production deploy should at minimum cover:

- The full deploy, including the pre-deploy switches (sending, feature flags, maintenance mode) and the post-deploy switches back on.
- A migration, a rollback, and a forward-fix on top of the rollback.
- A failed deploy at every external dependency (network, database, image registry, secrets backend) and the recovery path.
- The backup step under each of: a clean database, a locked database, a slow database, and a database the backup step cannot reach.
- A restore drill from the most recent backup, with a row count check, a hash check, and a swap-back.
- The alerting path. Kill a worker, confirm the alert reaches the on-call channel, restart, confirm the resolution note follows.

If the rehearsal cannot script one of those cases, the deploy is not ready.

## The cost

The full rehearsal took about an hour, on top of the time spent on the original PR. That is real time. The cost of not running the rehearsal, on a single production-breaking bug, was a 4 a.m. page, a manual restore, and an apology to whoever had to fix the database on the VPS at 4 a.m. The trade is not close.

## Use this

- Rehearse the deploy, not the test. The deploy script creates the production state. The test suite only checks the code. If they disagree, the deploy script wins, and the rehearsal is the only way to find that out before production.
- Script the cases the test suite cannot reach. New directories with the deploy user's permissions. Migrations applied and rolled back. Sending switches that need an approval record. The backup step under a locked database. Each of these is one bug the rehearsal catches and the test suite never will.
- Block the merge on the rehearsal, not on the test suite. Green CI is necessary, not sufficient. The deploy package is not done until it has run end to end, with the real encrypted secrets, against a clean staging instance, and every case in the script has a recorded outcome.

## Also shipped

- Marketplace mirror sync had failed three Mondays running, with 21 sources held in quarantine; four Sonnet drift reviewers landed the verdicts (`Re-baseline`: box-cloud-filesystem, dolt-mcp-vcs, skills-janitor, brand-forge, skyvern, kobiton-automate; `Re-baseline with notes`: hermes-tweet, x-bug-triage, governed-second-brain, slack-channel, pr-to-spec; `Hold`: hyperflow, x-twitter-scraper; plus the osv-scanner v2.6.0 flag held pending decision).
- PR #1594 resolved three lapsed CI deadlines on merit: changed-package audit flipped to blocking (only fails on deps PR changed, none in the a2a-client or pr-to-spec range tested); strict frontmatter errors fixed in 10 repo files (9 remain in external mirrors, deadline extended to 2026-10-31); whole-corpus `npm audit` extended to 2026-10-31.
- Bob's Big Brain bulk-import triage found 16,202 "imported" rows are ICO compile output in three waves, not a vault import. 6,443 already retired by title-Jaccard supersession, with some false matches. 5,100 rows to deprecate in three reversible waves.
- Registrar Nightly canary had failed five nights running: canary controls grew from 3 to 6, but the nightly fixture's seed text covered the original 3 only. PR #356 fixed it; manual `workflow_dispatch` confirmed green.
- `repo-sweep` and `release` skills v3 merged: branch-protection bypass gone (PRs merge through GitHub API pinned to exact commit, no `--admin`, protection never changed); estate mode scans 199 repos in roughly 34 seconds; 68+26 tests pass; both skills grade A (96 and 95) on the validator.

## Related posts

- [Linking the public surface to the deployment thesis]({{< ref "link-public-surface-to-deployment-thesis.md" >}}) (2026-09-30). The deploy thesis is the contract. This post is one rehearsal of one package against it.
- [Team page ordering is a release decision]({{< ref "team-page-ordering-is-a-release-decision.md" >}}) (2026-09-28). The release decision lives in the deploy script, and the deploy script is what the rehearsal exercises.
- [Use the primitive, not the patch, in CodeQL]({{< ref "use-the-primitive-not-the-patch-codeql.md" >}}) (2026-09-27). The same logic applies. Reach for the primitive the platform already maintains, then rehearse the rule the platform enforces.
