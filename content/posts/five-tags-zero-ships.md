+++
title = "Five Tags, Zero Ships: How an Auto-Release Workflow Lied for a Whole Day"
slug = 'five-tags-zero-ships'
date = 2026-05-19T10:00:00-05:00
draft = false
tags = ["release-engineering", "ci-cd", "monorepo", "debugging", "typescript"]
categories = ["Technical Deep-Dive"]
description = "Five GitHub release tags created. npm registry unchanged. Three discrete bugs: tests silenced with || true, monorepo version drift, missing npm publish step."
+++

Five GitHub tags. v1.0.4 through v1.1.0. Five green checkmarks on the workflow. Five formatted release notes. The npm registry stayed at v1.0.5 the entire time.

This is what it looks like when a release workflow ships tags without shipping code. Every observable surface said "done" except the one that mattered — the registry. The bug wasn't in one place; it was three independent failures that combined to make the lie convincing.

## What the Checkmarks Promised

`gh release list` showed all five tags with formatted changelogs. The workflow run logs were entirely green. If you ran `npm install -g intentional-cognition-os`, you got v1.0.5. No error. No warning. Silently wrong for anyone relying on v1.0.5+, silently right for everyone else.

The pattern repeated across the morning: commit → auto-release fires → tag appears → npm registry unchanged. The workflow was perfectly honest about tagging. It just wasn't releasing anything.

## Bug 1: Tests That Passed by Lying

The "Verify readiness" step was:

```yaml
- name: Verify readiness
  run: pnpm test || true
```

The `|| true` is the tell. Every test failed. `Failed to resolve entry for package @ico/types` — the workspace packages hadn't been built yet, so `pnpm test` resolved nothing, threw hard errors, and the `|| true` swallowed them all. The workflow saw exit code 0 and kept going.

In a monorepo, the build step is not optional ceremony. The test runner needs the workspace packages to be built first. The fix:

```yaml
- name: Verify readiness
  run: |
    set -e
    pnpm build
    pnpm test
    pnpm lint
    pnpm typecheck
```

`set -e` means any non-zero exit stops the workflow. If tests fail after the build, you find out. If the build fails, you stop. Lint and typecheck went into the same step because they were already in the local pre-push hook; the only reason to keep them out of the release gate is laziness or speed, and a release gate is the wrong place to optimize either.

## Bug 2: Nine Version Sources, Six Ignored

Nine surfaces emit a version string in this repo: root `package.json`, `version.txt`, `CHANGELOG.md`, the five workspace `package.json` files (`packages/cli`, `packages/kernel`, `packages/compiler`, `packages/types`, `packages/benchmarks`), and the runtime constant at `packages/kernel/src/version.ts`. The workflow bumped three of them — root, `version.txt`, `CHANGELOG.md` — and silently left the other six behind.

Result: root said 1.0.4, workspace packages said 1.0.3. Root said 1.0.5, workspace said 1.0.4. Drift every run. `ico --version` told users the workspace's number, not the tag's.

Lock-step monorepos need single-source-of-truth version sync. A helper that picks up the six the workflow was missing:

```bash
bump_pkg_json() {
  local file=$1
  local version=$2
  node -e "
    const fs = require('fs');
    const pkg = JSON.parse(fs.readFileSync('$file', 'utf8'));
    pkg.version = '$version';
    fs.writeFileSync('$file', JSON.stringify(pkg, null, 2) + '\n');
  "
}

bump_pkg_json package.json "$VERSION"
for pkg in packages/*/package.json; do
  bump_pkg_json "$pkg" "$VERSION"
done
sed -i "s/export const VERSION = '.*';/export const VERSION = '$VERSION';/" \
  packages/kernel/src/version.ts
```

All nine sources now move together. `ico --version` reports the truth.

## Bug 3: The Step That Wasn't There

The workflow tagged releases. It never published to npm. There was no `npm publish` step. That's not a typo — the workflow was complete without it. Every release ran. Every release skipped the one thing that makes it a release.

Here's what belongs after "Create GitHub Release":

```yaml
- name: Publish to npm
  env:
    NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
  run: |
    set -e
    if [ -z "$NPM_TOKEN" ]; then
      echo "NPM_TOKEN not set — skipping publish"
      exit 0
    fi
    if npm view "intentional-cognition-os@$VERSION" version 2>/dev/null; then
      echo "intentional-cognition-os@$VERSION already on npm — skipping"
      exit 0
    fi
    echo "//registry.npmjs.org/:_authToken=$NPM_TOKEN" > ~/.npmrc
    pnpm --filter intentional-cognition-os publish --no-git-checks
    sleep 5
    npm view "intentional-cognition-os@$VERSION" version
```

Three guards, all in the script — not in the step's `if:` condition. (Step-level `env:` isn't available to that step's own `if:` in GitHub Actions, so `if: env.NPM_TOKEN != ''` would always evaluate false. The check belongs inside `run:`, where the env is real.) Token presence fails safe if it's missing. Idempotency skips if already published (covers manual publishes). Post-publish verification re-queries the registry to confirm it landed.

A release workflow that doesn't end with a verifiable artifact in the registry isn't a release workflow. It's a tagging workflow with extra steps.

## The State Behind the Process

Fixing the workflow forward didn't fix the present. When the workflow was corrected (commit `7681dd5`), `main` was drifted: root at 1.1.0, workspace at 1.0.5. Users running `ico --version` got `1.0.5`. One-time backfill in commit `c651de8` aligned all nine version sources to 1.1.0. Then verified: `pnpm build` succeeded, `pnpm test` 1,210/1,210 passing, `ico --version` → `1.1.0`.

Process bugs leave state behind. Fixing the process doesn't heal the damage. You clean it up separately.

## The Three-Bug Pattern

Every CI/CD pipeline that ships has these three failure modes available:

1. Quality gates that pass on failure (`|| true`, swallowed errors). Fix: `set -e` and explicit step order.
2. Monorepo workspaces with distributed version state. Fix: single-source-of-truth version sync in the workflow.
3. A release workflow that doesn't end with verification the artifact reached the registry. Fix: final step that queries the registry and confirms.

The icos release workflow had all three. The checkmarks lied because the workflow wasn't designed to catch itself lying.

## Also Shipped 2026-05-19

Daily-log convention — the rest of the day, in one paragraph each. Not connected to the release-workflow thread; logged here because they happened on the same git day.

- **claude-code-slack-channel v2 cluster** — 4 PRs merged with enterprise governance substrate framing. RFC 8785 JCS interop vectors (#175), cross-tier shadow detection (#176), journal v2 Ed25519 signing (#177), strip denied tool-call detail (#178).
- **kobiton R3 close-out** — deliverable final review, Blog 3 rewrite, 5 close-out PRs merged.
- **claude-code-plugins partner portal** — Kobiton and Nixtla brand integration, Killer Skill of the Week refresh.
- **intentional-cognition-os test infra** — Intent Solutions Testing SOP layers L0-L7 installed (`.husky/`, dependency-cruiser, stryker, RTM/PERSONAS/JOURNEYS docs). 3,447 insertions in commit `e0efdee`.

## Related Posts

- [v1.0.0: Conditional GO Through a Release Gate](/posts/v1-release-gate-conditional-go/) — The gate that flagged this path.
- [Honest Performance Benchmarks for a Paid-API Compiler](/posts/honest-perf-benchmarks-paid-api-compiler/) — Earlier icos work from this release cycle; same repo, different failure mode.
