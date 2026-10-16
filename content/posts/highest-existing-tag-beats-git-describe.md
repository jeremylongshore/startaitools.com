+++
title = 'When git describe Traps Your CI Semver Bump, Look Up the Highest Existing Tag Instead'
slug = 'highest-existing-tag-beats-git-describe'
date = 2026-10-15T08:00:00-06:00
draft = false
tags = ["git", "ci", "semver", "github-actions", "release-workflow", "bot-commits", "branch-protection"]
categories = ["DevOps"]
description = "A bot's [skip ci] version-bump commit that was rejected by branch protection creates an annotated tag outside the branch's ancestry. git describe keeps returning the older reachable tag, the bump recomputes a version that was already tagged, and the release job fails with `tag already exists` on every push. Use `git tag --list 'v*' --sort=-v:refname | head -n1` (highest existing tag, not git describe) and the version stays monotonic forever."
tldr = "CI semver bumps that fail with `tag already exists` on every push are usually not duplicate-tag bugs. They are `git describe` traps created by a bot's rejected `[skip ci]` version-bump commit. Replacing `git describe` with `git tag --list 'v*' --sort=-v:refname | head -n1` keeps the version monotonic regardless of tag ancestry."
+++

A CI-driven semver bump that reports `tag already exists` on every push looks like a duplicate-tag bug. It usually is not. The trap is `git describe` and a single bot commit that the protected branch refused.

I've debugged this loop enough times to know the duplicate-tag framing is misleading. The duplicate is real. It just is not the bug.

If your release workflow computes the next version with `git describe`, a bot's rejected version-bump commit can wedge the next release forever. The fix is a one-liner that ignores ancestry and trusts the highest existing tag in the repo.

What happens:

1. The release bot pushes a `chore: release v1.33.20 [skip ci]` commit.
2. Branch protection rejects the push. The bot is not on the bypass list, so the commit never lands. That is by design.
3. The bot's annotated tag `v1.33.20` was already created locally before the push attempt. It now points to a commit that is not on the branch's history.
4. Next push: `git describe` walks ancestry from HEAD, skips the dangling tag, and returns the last reachable tag, say `v1.33.19`.
5. The bump computes `v1.33.20`, tries to create the tag, fails with `tag already exists`, and the workflow exits 128.
6. Every subsequent push does the same thing.

The fix is one line:

```bash
PREV_TAG=$(git tag --list 'v*' --sort=-v:refname | head -n1)
```

That is the highest existing semver tag in the repo, sorted by refname descending, regardless of reachability. The version stays monotonic forever.

Then the bump step computes the next version from `$PREV_TAG` (a normal semver bump) instead of `$(git describe --tags --abbrev=0)`. The dangling tag from the bot no longer matters, because the lookup ignores it.

The comment in the workflow spells out the failure mode and why `git describe` is wrong here:

```yaml
# Use the HIGHEST EXISTING semver tag, NOT `git describe` (which only
# considers tags reachable from HEAD). A prior release tag can point to
# a "[skip ci]" version-bump commit that never landed on the branch
# (protected-branch push rejected the bot) and so dangles; `git describe`
# then keeps returning an older tag and the bump recomputes an
# already-existing tag → `git tag` fails "already exists" (exit 128) on
# every push. Highest-existing-tag makes the version monotonic
# regardless of ancestry and permanently breaks that loop.
          PREV_TAG=$(git tag --list 'v*' --sort=-v:refname | head -n1)
```

The `[skip ci]` commit on the bot side is intentional. It breaks the workflow-recursion loop so the bot's own version-bump does not re-trigger the release workflow that produced it. `version.txt` is the single source of truth for the new version.

The same workflow has a supersede and reconcile path that protects against a commit landing on master before its tag does. That keeps a held bot push from wedging the next release, but only if the highest-tag lookup is already in place. Otherwise the next run still recomputes a version that exists.

If you are debugging the symptom right now, the audit trail is:

- `git tag --list 'v*' --sort=-v:refname` shows the dangling tag at the top.
- `git cat-file -p v1.33.20^{commit}` shows the commit it points to. If that commit is not on master, the branch is in the trap.
- `git log v1.33.20..master` is empty, which is why `git describe` keeps skipping it.

## Use this

- Replace `git describe --tags --abbrev=0` with `git tag --list 'v*' --sort=-v:refname | head -n1` in your CI semver bump step. The version becomes monotonic regardless of tag ancestry.
- Confirm the bot identity on any `[skip ci]` gap. If the bot is not on the branch-protection bypass list, treat its commits as conditional on push acceptance, and read its tag as advisory until it lands.
- Add the supersede and reconcile path that publishes nothing when a newer commit has already reached the default branch. That keeps the next release from re-entering the same loop on the next bot push.

The full fix lives in [release.yml](https://github.com/jeremylongshore/startaitools.com/blob/master/.github/workflows/release.yml).

Related posts:

- [rank-only-reporting-keeps-the-eval-honest](/posts/rank-only-reporting-keeps-the-eval-honest/)
- [park-the-cutover-keep-the-work](/posts/park-the-cutover-keep-the-work/)
- [name-the-single-authority-in-a-daily-pipeline](/posts/name-the-single-authority-in-a-daily-pipeline/)