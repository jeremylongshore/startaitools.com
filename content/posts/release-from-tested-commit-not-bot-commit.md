+++
title = 'Tag a Tested SHA, Not a Bot Commit'
slug = 'release-from-tested-commit-not-bot-commit'
date = 2026-10-18T10:00:00-06:00
draft = false
tags = ["github-actions", "release-workflow", "semver", "branch-protection", "ci-cd", "bot-commits", "devops"]
categories = ["Technical Deep-Dive"]
description = "A bot push on a protected branch wedges a CI release in a tag-already-exists loop. Move the version bump into a PR and tag an already-CI-green SHA on main."
tldr = "A CI release that commits a version bump, pushes to main, and then tags its own commit defeats branch protection and traps every subsequent run in a tag-already-exists loop. Move the version bump into a normal pull request, gate the publish on a small release_check.py script that verifies the SHA is on main and the tag is not already present, and let the release workflow tag an already-CI-green SHA with gh release create --target <SHA>. The bot never writes to main and the release never tags a commit the protected branch did not accept."
+++

## The bot push on a protected branch is the bug

A conventional CI release job, meaning a workflow that commits a version bump, pushes to main, then tags its own commit, hits a wall on a protected branch with required checks. The branch refuses the unreviewed bot push before any tag step runs. The next run starts over, sees the previous reachable tag, recomputes the next version, and finds it already exists in the remote tag namespace. Every push after that exits 128 with `tag already exists`, and the release pipeline wedges in a loop no rerun can clear without manual surgery. After reading this you will have a release workflow that does not commit or push, a 29-test gate that refuses to publish on a stale SHA, and a recipe that any team can adopt tomorrow.

The conventional fix is `git describe` and a bot push. That is the wrong direction. `git describe` is itself fragile: it walks ancestry from HEAD, so any bot commit, manual revert, or rebased branch will either pick the wrong base or fail outright. The lookup has no opinion about what main actually accepted, only about what HEAD can reach. The shape of the bug is the bot push. Fixing the lookup without removing the push only papers over the wedge.

The right place to start is what the workflow is allowed to do, which is to point at a commit main has already accepted and create a GitHub release against that SHA. The release workflow is not a committer. The protected branch is the committer, and the protected branch is the only thing allowed to commit. Everything else is downstream.

## The design constraint

The release workflow must not write to main, must not create a client-side `git tag`, and must publish a release whose artifacts are the artifacts the protected branch already accepted. The only thing the workflow is allowed to do is point at a commit main has already green-lit. That single rule shapes the design, and every piece below is a guardrail enforcing it.

The bot push goes. The bot tag goes. The version bump moves into a normal pull request. The release workflow becomes a thin wrapper around three checks and a `gh release create --target <SHA>`. Everything else falls out of that.

## The fix, in three pieces

### The version PR

The version change goes through a normal pull request, alongside the change it ships. `version.txt`, `pyproject.toml`, and the new `CHANGELOG.md` entry all move together, get reviewed together, and land on main by the same path every other change lands. The protected branch treats the version bump the same way it treats any other code: required checks, reviewer, merge button. The bot never touches main.

This is the smallest change with the largest effect. The release workflow no longer needs to commit, push, or set up authentication for a push. It only needs to read a SHA, validate it, and call `gh release create` against it. Every push failure, every merge conflict on a version bump, every secret rotation the bot push was depending on, disappears from the release path.

### `release_check.py`

Before the workflow does anything, a script named `release_check.py` runs three preconditions:

1. `version.txt`, `pyproject.toml`, and the new `CHANGELOG.md` entry all agree on the version.
2. The commit SHA the workflow was triggered on is reachable from `origin/main`.
3. No tag at the computed version already exists.

If any precondition fails, the workflow exits non-zero. The check is the gate, and the workflow has nothing else to fall back to: a separate retry path does not exist, an override switch does not exist, and a parallel publish path does not exist. The script is plain Python with no dependencies beyond the standard library.

The companion fix in the same change distinguishes three outcomes from `git ls-remote --exit-code --tags origin v$VERSION`: tag found (refuse to release), tag absent (proceed), and any other non-zero exit (hard fail, do not publish). The shape of the check is a small dispatch on the exit code rather than a single boolean. The mapping that comes out of the man page, verified empirically against a real `git ls-remote --exit-code` run, is exit 0 for tag found, exit 2 for ref not found (the recipe's proceed case), and exit 128 (or 1) for transport, DNS, or auth errors (the recipe's hard-fail case):

```python
result = subprocess.run(
    ["git", "ls-remote", "--exit-code", "--tags", "origin", f"v{version}"],
    capture_output=True,
)
if result.returncode == 0:
    die(f"v{version} already exists on origin; refusing to release")
if result.returncode == 2:
    # exit 2 from --exit-code means the ref was not found in the remote namespace
    pass  # tag absent, proceed to publish
else:
    # any other non-zero exit is a transport, DNS, or auth error
    die(f"could not reach origin to verify v{version}: rc={result.returncode} {result.stderr.decode()!r}")
```

Before the change, a transient DNS blip or a credentials hiccup looked like `no tag`, and the workflow went on to publish a duplicate release. The check is now fail-closed. An independent QA pass in the build session caught this exact behavior while reviewing the recipe; the fix landed in the same pull request.

### The rewritten `release.yml`

The only steps the release workflow runs are:

1. Checkout the commit SHA the pull request merged.
2. Run the existing green-CI gate against that SHA.
3. Create the GitHub release with `gh release create --target <SHA>`.

No version commit. No push. No client-side `git tag`. The release tags a SHA the protected branch accepted and the required checks already passed on. v1.33.20 shipped this way on 2026-10-15: two commits on master, the workflow tagged one of them, and the other carries the `[skip ci]` marker that kept the recursive trigger from re-firing the workflow on the version-bump commit itself.

## The second-order tests

Twenty-nine new tests landed in `tests/test_release_gate.py`, organized by which precondition they cover:

- **Version agreement (8 tests).** The three files all carry the same version, and the version parses as semver. Drift between any two files fails the test. A version with a `+` build metadata suffix is rejected because `gh release create` does not accept it.
- **SHA reachability (6 tests).** The trigger SHA is on `origin/main`. A SHA from a feature branch is rejected. A SHA from a force-pushed branch that is no longer reachable is rejected. The check uses `git merge-base --is-ancestor`, not a string match.
- **Tag absence (9 tests).** No tag at the computed version exists. A tag on a different ref is ignored. A tag at the same version on a different name (`v1.2.3-backup`) is still caught. The test pins both the `git ls-remote` exit-code branch and the local `git tag --list` branch.
- **Network failure (4 tests).** A timeout, a DNS error, and an auth error from the tag lookup are all treated as failure, not as `no tag`. The test uses a mock transport, not the real network.
- **CI gate coupling (2 tests).** The release workflow refuses to publish if the green-CI gate has not run for the trigger SHA. The check reads the workflow run for the SHA from the GitHub API and verifies the conclusion is `success`.

If any one of them regresses, the suite fails before the workflow runs.

The other second-order win came from the test suite itself. Profiling found a 1.5s teardown hidden in four fixture servers running `serve_forever` polling. Replacing the polling with a 0.02s explicit `POLL` cut `test_agreements.py` from 84s to 56s, and pulled the full test-suite job from 15m 51s to 9m 20s. The release path is faster because the test suite it depends on is faster, and the recipe's safety property depends on that suite running on every protected-branch commit.

## The recorded contract

The recipe is now section 5.5 of the developer-workflow contract: `GitHub Actions rules`. Version changes go through a normal pull request. The release workflow validates the SHA is on main, runs the existing green-CI gate, and tags exactly that SHA with `gh release create --target <SHA>`. No workflow writes to main. No workflow creates a client-side tag. Verified on 2026-10-18: 29 new tests landed in `test_release_gate.py` covering the three preconditions, plus 3 pre-existing tests in the same file that the recipe inherited, for 32 release-gate tests passing in total and actionlint clean.

The companion half of the same contract lives at the highest-existing-tag lookup in `startaitools.com`'s own release workflow (lines 84 to 96). The lookup replaced `git describe` with `git tag --list 'v*' --sort=-v:refname | head -n1`. The same bot-commit wedge this recipe prevents is the wedge that traps `git describe`. Tag the tested SHA, look up the highest existing tag, the version stays monotonic regardless of what the bot has been doing. The protected branch and the workflow each own exactly one thing, and neither owns the other's.

## Use this

- Move every version change into a normal pull request that updates `version.txt`, `pyproject.toml`, and `CHANGELOG.md` together. The protected branch treats the bump the same way it treats code, and the release workflow no longer needs commit or push credentials.
- Replace the bot commit and push with a `release_check.py` that verifies the three files agree, that the SHA is on main, and that the tag is not already present. Treat a network error from the tag lookup as a hard failure, not as `no tag`.
- Rewrite the release workflow to do only three things: checkout the SHA, run the existing green-CI gate, and `gh release create --target <SHA>`. The release tags a SHA the protected branch accepted.

## Related Posts

- /posts/highest-existing-tag-beats-git-describe/. Replacing git describe with the highest-existing-tag lookup stops the [skip ci] tag-already-exists loop that this recipe also prevents at the workflow level.
- /posts/when-the-tailnet-trial-ends-move-the-runner-onto-the-network/. Same release-path family: yesterday's fix moved the deploy runner onto the tailnet so the workflow never has to mint a paid-tier token; today the version bump moves into a PR so the workflow never has to push to main.
- /posts/when-green-ci-proves-nothing/. The CI gate checks the run, not the artifact's relationship to the protected branch. Tagging a tested SHA closes that gap.
