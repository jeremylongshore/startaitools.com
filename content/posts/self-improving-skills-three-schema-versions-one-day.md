+++
title = 'Self-Improving Skills: Three Schema Versions in One Day'
slug = 'self-improving-skills-three-schema-versions-one-day'
date = 2026-05-14T08:00:00-05:00
draft = false
tags = ["claude-code-plugins", "skills", "schema-design", "marketplace", "backward-compatibility", "release-engineering"]
categories = ["Technical Deep-Dive"]
description = "Backward-compatible schema upgrades for Claude skills: L0 metadata indexing, conditional visibility, and config prompts eliminate mid-task environment errors. 2783 skills."
+++

A skill that throws `UnknownEnvVar` mid-task is a UX disaster. By the time the error surfaces, skill selection has already happened, the user is mid-thought, and recovery is "go set the env var and start over." The whole point of skill metadata is to prevent that *before* the skill is ever shown. Three schema versions shipped to the claude-code-plugins marketplace on 2026-05-14 — 3.4.0, 3.5.0, 3.6.0 — are three layers of the same defense. Catalogs get cheap to interrogate. Skills hide themselves when their deps are absent. And on install, skills tell the installer exactly what to prompt for.

All three shipped same-day. None broke a single one of the 2783 existing skills. The discipline that made that possible is older than the patches.

## Layer 1 — Progressive Disclosure (3.4.0)

The catalog problem is mechanical. At 2783 skills, the full skills-catalog.json is 23 MB raw, 5.5 MB gzipped. Every consumer pays for `body` HTML — full SKILL.md content rendered to HTML and inlined per skill — even when the consumer only needs name, description, and trigger tags for routing. The "trigger match" path is paying for the "render the full skill body" path.

PR #714 added a second build artifact: an L0 metadata index at `marketplace/src/data/skills-index.json`, emitted alongside the existing L1 catalog at `skills-catalog.json`.

| Artifact | Raw | Gzipped |
|---|---|---|
| L0 index (new) | 817 KB | **97 KB** |
| L1 catalog (existing) | 23 MB | 5.5 MB |

**56× reduction gzipped.** L0 carries name, description, tags, allowed-tools, visibility flags — everything a router or browser needs to decide whether to surface a skill. L1 keeps the rendered body for consumers that need to display it.

The CLI surface on `discover-skills.mjs` reflects the two consumer shapes:

- `--level=full` (default) — emits both L0 and L1
- `--level=metadata` — L0 only, skips `mdToHtml(body)` per skill, ~3× build speedup (0.54s vs 1.58s)
- `--level=file` — errors with guidance (file-level is a runtime concept, not a build artifact)

The skip-`mdToHtml` shortcut is where the speedup lives. HTML rendering is per-skill work proportional to body size; cutting it out for metadata-only builds collapses the slowest stage.

Backward compatibility is trivial here because the artifact is consumer-protocol, not authoring-protocol. SKILL.md frontmatter didn't change. Existing `skills-catalog.json` consumers see two new top-level fields (`schemaVersion`, `level`) and nothing else moved. The build produces a superset.

## Layer 2 — Conditional Visibility (3.5.0)

Cheap catalogs don't help if the user still has to scroll past skills they can't run. A `/gemini-pr-review` skill that needs `GCP_PROJECT` shouldn't appear in selection on a machine without GCP auth. PR #715 added four optional frontmatter fields so skills declare their environmental preconditions.

| Field | Behavior |
|---|---|
| `requires_env` | Hidden unless every listed env var is set |
| `requires_tools` | Hidden unless every listed tool is available |
| `fallback_for_env` | Shown ONLY when listed env vars are NOT set |
| `fallback_for_tools` | Shown ONLY when listed tools are NOT available |

Two scopes (env, tools), two directions (require, fallback). The shape covers the common cases without proliferating fields. All four accept three input forms — block-list, inline-array `[a, b]`, CSV string — and the parser normalizes them.

The non-obvious part is the contradiction check. The same identifier MUST NOT appear in both `requires_{scope}` and `fallback_for_{scope}` per scope. A skill cannot simultaneously *require* X to be set AND be the *fallback* for X being absent — that skill would be unreachable in either state.

The validator catches this. Given:

```yaml
requires_env: [GITHUB_TOKEN, SHARED_VAR]
fallback_for_env: [SHARED_VAR, OTHER_VAR]
requires_tools: [docker, kubectl]
fallback_for_tools: [kubectl]
```

The output is:

```
ERROR: contradictory visibility rule on requires_env + fallback_for_env: ['SHARED_VAR'] appears in both
ERROR: contradictory visibility rule on requires_tools + fallback_for_tools: ['kubectl'] appears in both
```

The catalog has plenty of skills that would set these. `/gemini-pr-review` would set `requires_env: [GCP_PROJECT]`. `/whop-deployment-specialist` would set `requires_env: [WHOP_API_KEY]`. A generic web-search skill would set `fallback_for_env: [FIRECRAWL_API_KEY]` so it surfaces only on machines without the premium crawler. Migration isn't auto-populated — it's per-skill judgment about what the skill actually depends on.

Backward compatibility holds because the fields are optional. All 2783 existing skills validate cleanly. Standard-tier validator output is unchanged (236 pre-existing errors, no new ones). L0/L1 catalog consumers see the new fields as empty arrays for unmigrated skills. The parser change is strictly additive.

## Layer 3 — Self-Declared Config (3.6.0)

Layer 2 hides skills that can't run. That solves the "skill in selection that fails on first use" problem. But it leaves a second problem: the user wants to *enable* the gemini-pr-review skill on this machine. How does the installer know what to prompt for? Reading the SKILL.md body for env var mentions is parsing-by-regex; that path is not defensible.

PR #716 added two optional frontmatter blocks. Skills self-describe the secrets they read from the environment and the per-skill config keys they consume.

| Block | Location | Purpose |
|---|---|---|
| `required_environment_variables` | Top-level, list of objects | Secrets the skill reads from env |
| `metadata.intent-solutions.config` | Nested, list of objects | Non-secret per-skill config keys |

Each entry self-describes. Env entries need `name` + `prompt`. Config entries need `key` + `description` + `default`. The installer renders the prompt, captures the value, writes it to disk before the skill ever runs.

The cross-field check ties 3.6.0 back to 3.5.0. If a skill declares `requires_env: [GCP_PROJECT]` but doesn't include `GCP_PROJECT` in `required_environment_variables`, the validator warns: the visibility gate names a var the installer can't prompt for. The skill will hide itself correctly, but the user has no path to make it visible.

A targeted test with intentional violations:

```yaml
requires_env: [GITHUB_TOKEN, UNDECLARED_VAR]
required_environment_variables:
  - name: GITHUB_TOKEN
    prompt: "Personal access token"
  - name: BROKEN_ENTRY        # missing prompt → ERROR
metadata:
  intent-solutions:
    config:
      - key: default_branch
        description: "Target branch for PRs"
        default: main
      - key: broken_entry     # missing description + default → ERROR
```

Validator output:

```
ERROR: required_environment_variables[1] (name=BROKEN_ENTRY) missing required key 'prompt'
ERROR: metadata.intent-solutions.config[1] (key=broken_entry) missing required key 'description'
ERROR: metadata.intent-solutions.config[1] (key=broken_entry) missing required key 'default'
WARNING: requires_env declares ['UNDECLARED_VAR'] but they have no matching entry in required_environment_variables
```

Storage is deliberately boring. Resolved user values land in `~/.claude/skill-config/<skill-name>.yaml`, mode 600, plain YAML. The marketplace doesn't enforce a loader. Python skills read it with PyYAML, bash skills shell out to `yq`, Node skills use `js-yaml` — whatever the skill is already using. No new runtime dependency.

Backward compat held again. 2783 existing skills validate cleanly, same 236 pre-existing errors as main, zero new errors. Full `npm run build` in `marketplace/` is green.

## The Discipline That Made This Safe

Three schema versions in one day is the kind of velocity that breaks downstream consumers in shops without a forcing function. The `SCHEMA_CHANGELOG.md` in the claude-code-plugins repo has one, established 2026-04-28 after a different one-day schema debacle:

> `ALWAYS_REQUIRED` is the IS enterprise 8-field set: `{name, description, allowed-tools, version, author, license, compatibility, tags}`. Do not reduce it. Do not reframe as "marketplace polish." Tracking metadata (version, author, license) is REQUIRED at marketplace tier, not optional polish.

The rule is simple. The required-fields set does not move. Every new field added in 3.4.0, 3.5.0, and 3.6.0 is **optional**. Every existing consumer that ignores the new fields keeps working. Every existing skill that doesn't declare visibility or config keeps validating.

That is why 2783 skills migrated cleanly with zero new validator errors. The discipline isn't ceremony — it's the constraint that lets three minor versions ship in one day without breaking a single downstream consumer.

## The Stack Composes

The three layers stack:

- **3.4** makes the catalog cheap to interrogate. Routers and browsers pull 97 KB gzipped instead of 5.5 MB.
- **3.5** hides skills that can't run on this machine. The user never sees a skill they don't have the deps for.
- **3.6** prompts for what's missing on install. Skills tell the installer the shape of their config surface; the installer captures it before the skill executes.

End-to-end, the failure mode from the opening paragraph — skill throws `UnknownEnvVar` mid-task — has nowhere to land. The catalog is too cheap to skip metadata fetches. The visibility gate hides skills without their preconditions. The install-time prompt populates the preconditions before the skill ever runs. That's the self-improving-skills surface: not a metaphor about smart skills, but a mechanism where the metadata carries the contract.

## Related Posts

- [Three Guards Against Shipping Slop](/posts/three-guards-against-shipping-slop/) — the prior week's release-engineering post on the same repo: gate, evidence, audit trail.
- [Monitoring Assumptions Silently Break Under Load](/posts/monitoring-assumptions-silently-break-under-load/) — adjacent theme: what happens when the contract you assumed isn't the contract the system signed.
- [Transitive CVE Clearance: The Dual-Layer Pattern](/posts/transitive-cve-clearance-dual-layer-pattern/) — same week, different repo. Two-move discipline applied to security patches; analogous to the additive-only discipline applied to schema changes here.
