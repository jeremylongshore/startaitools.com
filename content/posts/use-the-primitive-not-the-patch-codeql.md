+++
title = 'Use the Primitive, Not the Patch: Closing a CodeQL Backlog by Class'
slug = 'use-the-primitive-not-the-patch-codeql'
date = 2026-09-27T10:00:00-05:00
draft = false
tags = ["security", "static-analysis", "codeql", "ci-cd", "monorepo"]
categories = ["Development Journey"]
description = "When CodeQL keeps flagging js/file-system-race, the fix is one canonical primitive routed through one shared module. Eleven TOCTOU sites closed."
tldr = "When a static-analysis tool keeps flagging the same class of bug across a codebase, the right fix is to introduce the canonical primitive once and route every occurrence through it. Per-site patches close the alert and leave the class open. The day that crystallized this for one repo was a CodeQL backlog sweep that landed a single new module, scripts/safe-fs.mjs, and routed eleven TOCTOU sites through it."
+++

## The pattern that kept recurring

The CodeQL queue at the top of the week had twelve open alerts under the same rule name: `js/file-system-race`. The sites lived in CI tooling scripts, in the jrig boundary reader, in the validate input readers, in the proofs test, in the auto-bump driver, in the reconstruct-versions stub. Different files, one bug shape: a path gets checked (`existsSync`, `lstat`, or `stat`), then read or written by name in a separate call. The filesystem under the script is not quiescent between the two operations.

Twelve independent fixes would have closed the alerts. That is the patch-by-site answer, and it is wrong. The next advisory lands on a sibling site, the queue fills back up, and the ship has not moved.

The right answer is one new module, `scripts/safe-fs.mjs`, that captures the canonical primitive for "open a path safely and check it." It does the no-follow open, the regular-file check, and the same-inode stat before and after, in one call. Eleven sites get routed through it.

## Why a handle, not a reordering

Reordering calls looks appealing. The race becomes smaller when `existsSync(p)` moves above `readFile(p)` or disappears entirely. Both rearrangements shrink the window. Neither closes the race. A handle's `stat()` and `readFile()` resolve against the same open file descriptor, which is to say the same inode, regardless of what happens to the path afterward. That property is what the primitive captures.

The shipped helper looks like:

```
export function readTextSameInode(path) {
  // no-follow open, regular-file check, stat before and after via fd
}
```

The exact body is in the commit. The discipline is what matters: a single canonical call for "I want to read this path confidently," with the file descriptor pinning it.

## The TOCTOU sweep that landed

The hero commit introduced `safe-fs.mjs` and rewired eleven call sites:

- changelog coverage
- doc authority
- supersession template
- epic-1 scorecard
- jrig DB boundary default reader
- certification input
- plugin validator
- proofs test
- auto-bump
- reconstruct-versions
- `generate-missing-plugins.cjs`, which switched to the `'wx'` flag so a re-run can never overwrite a freshly written file

Each call was a check-then-read pair. Each was rewritten to use `readTextSameInode` (or the typed-file siblings for JSON, partial JSON, and binary). The pattern checker at land time confirms no tracked Markdown path fails the `safe-fs` rules.

Verification at the commit level: `node --test` passed 122/122 across the ten affected suites. Nothing downstream tripped from a swapped file descriptor.

## Sibling commits, same discipline

Twenty-one more commits shipped in the same sweep. Each one routes a class through a primitive rather than per-site patching the alert:

- Two passes against `py/path-injection` on the podium webchat ingest. The first pass restricted the character set on `phone_e164` and `location_uid` and required the resolved path to stay inside `PARTIAL_STATE_DIR` or raise `WebchatError` mapped to HTTP 400. CodeQL still flagged `Path.resolve` because the path gets queried against the filesystem before the containment check. The second pass moved to lexical normalize (the joined path through `os.path.normpath`) plus the containment form CodeQL recognizes. The lesson: when the first primitive still trips the scanner, find the form the scanner accepts. Two primitives, layered, applied at one site.
- The same handle-based stat+read pattern landed in `project-health-auditor/servers/code-metrics.ts` for alert 9. The MCP server audits an arbitrary caller-supplied repo path, so it cannot assume the filesystem underneath it is quiescent between calls. Same justification, different file.
- `conversational-api-debugger` had an `incomplete-sanitization` case for alert 7. The previous escape was `body.replace(/'/g, "\\'")` wrapped in single quotes. POSIX single-quoted shell ignores backslash, so the first embedded quote closed the string early and the rest of the body ran as shell syntax. The canonical primitive for shell escaping is the close/escape/reopen technique: replace each `'` with `'\''`. The shipped generator and the test that pinned the broken pattern were both rewritten to use it.
- `sync-lockfile` for alert 2833 had a `matchesPattern` that turned a `sources.yaml` glob into a regex by escaping only `.`. Every other regex metacharacter in a pattern (`(`, `+`, `[`, `\`, `$`) silently changed what the supply-chain lockfile matched. The canonical primitive is a small tokenizer that translates only the glob tokens (`**/`, `**`, `*`, `?`) and escapes everything else. Verified by a differential run over all 113 real patterns against every tracked path and suffix. About 11.4 million comparisons, zero differences.
- SBOM package URLs for alert 3032 got encoded per the purl npm type. Scope's `@` encodes to `%40`, which yields `pkg:npm/%40angular/animation@12.3.1`. Each segment encodes on its own, and a name with more than one slash or an empty segment is refused.
- Atomic temp-plus-rename (`writeFileAtomic`) landed for the marketplace catalog files in the CLI doctor command, covering alerts 2115-2117. The commit body names the reason: "The catalog is the file Claude Code reads to install plugins; a torn write breaks installs." A per-site patch would have left the catalog exposed. Temp-plus-rename collapses the class.
- `TRUSTED_MAIN_ANCHOR` for the gitleaksignore blueprint E4.5 gate is a pinned main-commit anchor. Two failure modes were tried and rejected during design: advancing the release tag forward, and trusting the moving main ref. A PR cannot make its own commit an ancestor of a commit already on main. Re-pinning to a PR commit fails the required check because that commit is not on main during the PR run. The primitive is the main commit, pinned.
- One false-positive got documented rather than fixed. `autoescape=False` in `generate-pack.py` is intentional because the templates render Markdown, never HTML. Enabling HTML escaping would corrupt Markdown syntax with the entities those characters render to. The fix is to pass `autoescape=False` explicitly with a comment. A documented false-positive with a code comment IS a primitive.
- Flask debug mode defaults off in the webhook handler template. Debug-on-by-default in a template that ships to users as the starting point for their own webhook server silently teaches an insecure pattern into production deployments.

## Verification across the sweep

The validate job's lattice check (`validate:saas-lattice`) regenerated clean. `pnpm --filter project-health-auditor test` passed 26/26. `pnpm --filter conversational-api-debugger test` passed 36/36. The dolt-sync and doltlite-sync tests passed 60/60. The scorecard suite passed. Ruff, eslint, prettier, and the audit-harness pin were clean.

The matcher that classifies future alerts against these primitives does the same. If a future advisory lands on a sibling shape, the comparator tells me which module owns it, which function to call, and where the unused import is hiding.

## Use this

- Run your SAST tool's category-grouped report. The categories with the most alerts are the categories where a primitive pays for itself. Per-site fixes are the wrong shape for top-heavy categories.
- Name the primitive for each category. TOCTOU resolves to open-then-stat-on-the-same-handle. Incomplete shell sanitization wants close-escape-reopen. Supply-chain globs go through "tokenize only glob tokens, escape everything else." Torn writes need temp-plus-rename. The gitleaks ignore gate uses a pinned main-commit anchor.
- Route every occurrence through one shared module. The next advisory lands on a sibling site, not on a novel bug. Documented false-positives belong in the same module, with the comment that justifies the bypass.

## Also shipped

- The 2026-09-27 tonsofskills.com security-warning incident record was filed at `000-docs/815`. Twelve VirusTotal engines flagged the domain as malicious or suspicious. No compromise evidence on the site or VPS. Dead-domain policy held at zero actionable occurrences.
- Two docs commits in intent-os on estate distribution research (73 venues, readiness findings).
- The 2026-09-26 post was dual-published to tonsofskills.com/blog.

## Related posts

- [reachability-is-not-freshness](https://startaitools.com/posts/reachability-is-not-freshness/): how the same access pattern can be true at one moment and false at the next.
- [orphan-site-folder-cleared-twenty-deps-alerts](https://startaitools.com/posts/orphan-site-folder-cleared-twenty-deps-alerts/): close twenty-odd alerts across a different security surface.
- [seven-merges-one-audit-zero-leaks](https://startaitools.com/posts/seven-merges-one-audit-zero-leaks/): what audit-discipline looks like after a security incident.
