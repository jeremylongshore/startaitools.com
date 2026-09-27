+++
title = 'One Folder Was Behind Every Critical Dependabot Alert'
slug = 'orphan-site-folder-cleared-twenty-deps-alerts'
date = 2026-09-26T08:00:00-05:00
draft = false
tags = ["dependabot", "security", "ci-cd", "monorepo", "plugin-ecosystem"]
categories = ["Development Journey"]
description = "When the only two manifests in your Dependabot queue belong to a folder your plugin never ships, the fix is to delete the folder, not patch it."
tldr = "An orphan website folder inside claude-code-plugins was not in the mirror's include list, not a pnpm workspace member, not referenced anywhere, and not run by any plugin user. It owned the only package.json and pnpm-lock.yaml in the repo, which is why every one of the 2 critical and 18 high Dependabot alerts on the project pointed at it. Removing the 17 files cleared all 20 critical and high alerts in a single commit and beat patching because nobody runs the upstream site and patching a second copy of it inside the mirror just lets the next advisory reaccrue."
+++

A multi-plugin repo's Dependabot queue had 2 critical and 18 high alerts pinned to a folder the plugin never runs, never installs, and never mentions. Removing the 17 files inside that folder closed every one of those 20 alerts in a single commit. The work that mattered was deciding the folder was not part of the plugin in the first place, which a four-check heuristic handled in under a minute.

## The four-check heuristic

```
1. Is the folder in sources.yaml's include list?
2. Is it a pnpm workspace member (CI installs, builds, tests it)?
3. Anything in the repo reference it?
4. Could a plugin user install and run it?

Four no's = orphan.
```

The folder in question was `plugins/mcp/pr-to-spec/site/`, an Astro marketing site with its own `package.json`, its own `pnpm-lock.yaml`, and the dozen or so pages that lit up the upstream's marketing presence. It dated from the very first import of the pr-to-spec plugin on 2026-03-20, when an over-broad copy pulled in everything that lived next to the plugin's source.

(1) Sources.yaml's include list never listed the path, so the weekly sync script ignored it. Every other week the folder fell further behind upstream, with no alerting mechanism to flag the gap.

(2) Not a pnpm workspace member. CI never installed it, never built it, never tested it.

(3) No file inside the repo referenced it. Not a doc link, not a script, not a fixture.

(4) No plugin user runs it. Plugins ship as folders that a Claude Code user installs into their config. A folder nobody can install is one nobody can run.

If any one of those answered yes, the folder earned protection and would have warranted a different fix. With all four empty, the only honest answer was to delete it.

## Why delete rather than patch

Patching in place would have closed the alerts without addressing what kept producing them. Every Astro advisory and every transitive-dep advisory from here forward would land back on this repo, on a folder nobody runs. What that adds up to is keeping a second, drifting copy of the upstream's marketing website inside a multi-plugin mirror, paying a maintenance tax each cycle, and paying it again when the next advisory lands.

The upstream already maintains its own marketing site in its own repo. The mirror exists to keep the plugin's logic current, not as a backup copy of every page the upstream chooses to ship. The folder was already drifting; the alerts were the symptom that finally made the drift expensive.

## Verification

The single commit removed 17 files. The followup checks, in order:

- `pnpm install --frozen-lockfile` passed (root lockfile unchanged).
- pr-to-spec still builds; 384 tests pass.
- Sources-lock parity holds: 38 on both sides.
- Mirror quarantine reports OK.
- Marketplace validator exit status is identical to main.

The marketplace validator comparison was the one that mattered. The validator decides which plugin manifests are publishable, and any drift in its verdict would have meant the removal walked over a path it depends on. Exit status identical means the validator did not notice the folder was gone, which is the only outcome the four checks could have predicted. The fact that the deletion was predictable is what made it cheap.

## Residue

The mirror still carries roughly 93 files outside its include list. CI builds and tests them, so they are not orphans by the same definition, but the mirror nonetheless ships a `.mcp.json` that points at a `dist/` server that is gitignored and so never reaches a plugin user. Both are decisions about what an MCP mirror is for, in production, and they are not the same shape as a folder that nobody builds. They need their own reasoning. Filed separately.

## Also shipped

- intent-os read-only operator queries live (PR #696, #698), artifact verification baseline restored (#697), Documenso recovery bundles now in borg backups (#675), BBB retrieval self-heal automated (#312).
- Learn access gated through Ping or Buzz leads channel (#679); persona voice-facet fit to corpus shipped (#482).
- CI dep bumps across `actions/setup-python` 6 to 7, `setup-go` 6.5 to 7, `alibaba/open-code-review` 1.12.3 to 1.12.9, `actions/checkout` 6.0.0 to 7.0.1.

## Use this

1. Run the four-check heuristic against any subtree in a mirrored plugin repo that has its own `package.json` or `pnpm-lock.yaml`. Four no's is an orphan, and orphan folders are how your Dependabot queue fills up.
2. For an orphan folder, deletion beats patching every time. Patching means maintaining a second copy of the upstream's site on your repo's clock and reaccruing alerts on the next advisory.
3. Always check the include list first. A folder outside the include list is on its own, regardless of what else it does, because every other maintenance mechanism is wired to that list.

## Related Posts

- [Nothing Read It, So Nothing Failed]({{< ref "/posts/nothing-read-it-so-nothing-failed/" >}}): five defects where the shape was an artifact with a producer and no consumer. Same diagnosis, same fix.
- [Transitive CVE Clearance: The Dual-Layer Pattern]({{< ref "/posts/transitive-cve-clearance-dual-layer-pattern/" >}}): how v0.9.1 cleared 6 high-severity transitive CVEs in `axios + fast-uri` and why dep bumps needed top-level overrides to actually stick.
- [Fix the Dependabot Pile-Up: Policy Over Patches]({{< ref "/posts/dependabot-pile-up-fix-the-policy/" >}}): when the queue keeps growing, change the policy you merge against, not the patches.
