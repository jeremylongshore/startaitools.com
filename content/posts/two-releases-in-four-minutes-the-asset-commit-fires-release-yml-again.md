+++
title = 'Two releases in four minutes: why release.yml fires twice'
slug = 'two-releases-in-four-minutes-the-asset-commit-fires-release-yml-again'
date = 2026-10-20T08:00:00-06:00
draft = false
tags = ["github-actions", "release-workflow", "semver", "hugo", "startaitools", "patch-bumps", "asset-commits", "devops"]
categories = ["DevOps"]
description = "Why startaitools saw v1.33.31 and v1.33.32 land four minutes apart: the post+assets cadence is two pushes to master, so release.yml stamps each one."
tldr = "Two releases that landed four minutes apart on the same day are not a bot double-bumping a failure: they are the post+assets cadence producing a second push to master, and release.yml triggers on every push."
+++

## Two releases in four minutes, again

Two releases landing four minutes apart on the same host day look like a bot double-bumping a busted tag on the Releases page, until you read origin (the canonical, GitHub-hosted copy of the git remote) master and see the assets-trailing-post shape. release.yml, the GitHub Actions workflow that stamps a semver tag on every push to master, fires on every push. On this repo the post commit and the social-card assets commit are always two events.

You can see it in the version.txt history on origin master. A patch bump lands at 04:34 -0600 host time. The second lands at 04:38. Four minutes and twenty-four seconds between the two version stamp commits. The Releases page shows two tags the same host day: v1.33.31 and v1.33.32. Nothing rolled back between them.

This note is by-design confirmation that the dual release is normal cadence for this pipeline. Anyone glancing at version.txt or the Releases page can check the commit log between the two tags, see the assets-trailing-post shape, and stop chasing a phantom bot bug. If the dual release still bugs you, gate `[skip ci]` on the raw assets-trailing commit and the second release collapses into the first.

## The four events on 2026-10-20

Order is timestamp, what landed, why it lands.

1. 04:32:43 -0600 host, the published post. The day's markdown, on the 2>/dev/null exit-code bug, lands on master. The producer backfill cron wrote the file and pushed.
2. 04:37:06 -0600 host, the social-card assets. The make-post-image and make-social-card scripts ran after the post landed, writing the 1200x630 social card image and the 1080x1080 square, plus the API-side media variants. That is a separate commit on master.
3. 04:34:20 -0600 host, chore: release v1.33.31. GitHub Actions saw the post commit at the master tip, ran release.yml against that head, did not see a BREAKING CHANGE or `feat:` prefix, applied a +0.0.1 patch bump to version.txt, pushed the tag.
4. 04:38:44 -0600 host, chore: release v1.33.32. The intervening assets commit at 04:37:06 pushed a new HEAD to master, release.yml re-ran against that head, again no BREAKING CHANGE or `feat:` prefix detected, another +0.0.1 patch bump, stamped v1.33.32.

Each release.yml invocation independently bumps version.txt by 0.0.1. Both tags pushed cleanly; the chain has no rollback or bot retry between them. Two commits on master that qualify as release events are what produces two tags the same day.

## Why the cadence produces two pushes

The image script is a separate step that runs in its own commit because a flaky model call cannot be allowed to break the publish path. The blog-land step publishes the markdown only. The image step runs after, in its own commit, with a deterministic PIL fallback if the model call fails.

The producer's contract treats the post and the image as one logical deliverable, but they hit master as two git events. From GitHub's view, two pushes to master means two workflow runs. release.yml has no opinion about whether a push is the post or the assets. The semver detection is purely prefix-based on the commit message: BREAKING CHANGE goes to major, `feat:` prefix goes to minor, everything else is a patch. The version bump is computed against the post-push HEAD and applied atomically. Two pushes in a row from this workflow produce two patches when neither carries a special prefix.

## Prior art on this repo

The same shape showed up on 2026-10-19 (v1.33.29 and v1.33.30 with one assets commit between them) and on 2026-10-17 (v1.33.22, v1.33.23, v1.33.24). On 2026-10-17 three release commits in one host day came from interleaved assets-and-fixes commits. The pattern is consistent: each separate push to master that does not carry a `feat:` or BREAKING CHANGE marker triggers its own patch bump.

A September 14 prior precedent in "The Pipeline Landed Its Own Output Today" ran the same shape: four commits at 04:19 -0600, the post, its social card, the dual-publish to tonsofskills, and the v1.17.35 release tag. Today's four commits are the same sequence on a faster release roll.

## How to verify on your own repo

If a repo's CI release workflow fires on every push to its default branch, and any pipeline produces more than one commit per logical deliverable, expect a tag-stamp per commit. The fix when the dual stamp matters is gating the assets-only or chore-only commits out of the trigger: prefix the assets commit with a `[skip ci]` trailer, or send it on a branch the workflow does not watch. Either keeps the post commit as the only release-firing event on that day.

## Use this

- Glance at the version.txt diff between two adjacent same-day tags before assuming a bot double-stamped a busted release. A diff of +0.0.1 with no rollback in between is the natural cadence, not a defect.
- Check the commit log between the tags. Two commits in the post+assets cadence (one post, one assets) explain two tags within minutes, every time.
- Gate raw assets-trailing commits behind `[skip ci]` if the dual stamp bugs you. The release still fires once for the post itself.

## Related posts

- "Tag a Tested SHA, Not a Bot Commit" - the cousin case for the same release.yml pathology, this time on the protected-branch side.
- "When git describe Traps Your CI Semver Bump, Look Up the Highest Existing Tag Instead" - the semver-monotonicity pattern that makes today's dual-release observation coherent.
- "The Pipeline Landed Its Own Output Today" - the September 14 prior precedent, four commits at 04:19 -0600 (the post, its social card, the dual-publish, the release tag).

The v1.33.32 release note lives at https://github.com/jeremylongshore/startaitools.com/releases/tag/v1.33.32.
