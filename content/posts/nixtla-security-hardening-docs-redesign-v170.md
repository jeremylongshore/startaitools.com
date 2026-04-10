+++
title = 'Security Hardening and Docs Redesign: Nixtla v1.7.0'
slug = 'nixtla-security-hardening-docs-redesign-v170'
date = 2025-12-09T10:00:00-06:00
draft = false
tags = ["security", "documentation", "devops", "python", "developer-experience"]
categories = ["Development Journey"]
description = "Skills security hardening, 16 broken links fixed from directory reorg, plugin guides for all 3 production plugins, PLUGIN_TREE.md, and a 'no hype, facts only' README redesign — Nixtla v1.7.0."
+++

20 commits. The theme was trust: can someone clone this repo, understand what it does, and trust that it won't do anything unexpected?

After four days of building infrastructure, features, and quality tooling, v1.7.0 is the release that makes the repo presentable to someone outside the development team. Security boundaries, comprehensive guides, a navigable tree, and a README that respects the reader's time.

## Security Hardening for Skills

Skills execute code. That's the point. But executing code from a SKILL.md file that was last audited three spec versions ago is a different kind of trust than running a pinned dependency from PyPI.

The hardening work focused on three areas:

**Permission boundaries.** Every skill now declares its required permissions in frontmatter: `requires_network`, `requires_filesystem`, `requires_env_vars`. The plugin runtime validates these declarations against what the skill actually does at load time. A skill that claims `requires_network: false` but imports `requests` fails validation before execution.

**Input sanitization.** Skills that accept user parameters now validate inputs against their declared JSON Schema before processing. Previously, the schema was documentation — the runtime passed raw parameters through and let the skill handle validation. Now the runtime rejects malformed inputs at the boundary. The skill never sees bad data.

**Output constraints.** Skills that write files are restricted to their own output directory. No `../../` escapes, no writes to `/tmp/` or home directories. The path canonicalization runs before the skill's write function, not after. This was already the convention but it wasn't enforced programmatically.

The permission boundary check is static analysis, not runtime sandboxing. The loader reads the skill's Python AST and looks for `import requests`, `import urllib`, `open()` calls with write mode, and `os.environ` access. If any of these appear in the code but aren't declared in the frontmatter, the skill fails to load. It's not perfect — dynamic imports and `eval()` bypass the check — but it catches the common case of a skill that grew new capabilities without updating its permission declarations.

The env var check was the most controversial. Many skills read `HOME` or `PATH` implicitly through standard library calls. Requiring `requires_env_vars: true` for every skill that calls `os.path.expanduser()` would be pedantic. The compromise: a list of exempt env vars (PATH, HOME, USER, SHELL, TERM) that don't trigger the flag. Everything else — API keys, database URLs, custom config vars — requires the declaration.

## 16 Broken Links

Yesterday's numbered directory restructure moved files. Today's build revealed 16 broken internal links. Every documentation file that referenced a plugin by its old path — `plugins/search-to-slack/` instead of `plugins/01-search-to-slack/` — was now pointing at nothing.

The fix was tedious but straightforward. `grep -r` for the old paths, replace with new paths, verify each one resolves. No script — at 16 occurrences it's faster to fix by hand than to write and validate a migration script. The rule of thumb: automate at 50, manual at 15.

One link was genuinely broken before the restructure. A reference in the architecture doc pointed to a design document that had been renamed during the Doc-Filing v3 migration two days ago. It had been broken for two days and nobody noticed because nobody reads architecture docs during a feature sprint.

The fix batch got its own commit with a descriptive message listing all 16 paths changed. This is the kind of commit that looks ridiculous in a log — "fix 16 broken links" with a diff that's nothing but path string replacements — but it's essential for future debugging. When someone does `git log --follow` on a documentation file and sees it moved, they need to find the commit that updated all references. A single commit with a clear message makes that traceable.

A link-checking script got added to the Tier 1 CI checks. `grep -rn` for internal markdown links, resolve each one against the repo's file tree, fail if any are dead. Runs in under 2 seconds. The 16 broken links from today are the last batch that will go undetected — from now on, CI catches them before merge.

## Plugin Guides for All Three Production Plugins

Each of the three production plugins — search-to-slack, baseline-lab, and BigQuery Forecaster — got a dedicated guide. Not a README, which already existed. A guide. The difference: READMEs answer "what is this?" Guides answer "how do I use this from zero?"

Each guide follows the same structure: prerequisites, installation, configuration, first run, common operations, troubleshooting. The prerequisite section is specific — not "Python 3.x" but "Python 3.12+ with pip 23.0+, a GCP project with BigQuery API enabled, and a service account key with `bigquery.jobs.create` permission."

The troubleshooting sections came from real problems encountered during development. The BigQuery Forecaster guide has a section on WIF (Workload Identity Federation) token refresh failures that took an afternoon to debug. The search-to-slack guide documents the Slack API rate limit behavior that differs between free and paid workspace tiers. These aren't hypothetical — every troubleshooting entry has a git commit SHA where the problem was first encountered and fixed.

Writing these guides surfaced a gap in the Baseline Lab's setup process. The guide's "first run" section required a step that wasn't automated: downloading the M4 dataset. The setup script installed dependencies but assumed the data was already present. Added a `--with-data` flag to the setup script that downloads and validates the M4 Monthly CSV. Small fix, big difference for someone following the guide for the first time.

## PLUGIN_TREE.md

A new file at the repo root: `PLUGIN_TREE.md`. An annotated directory tree showing every plugin, every skill, their status (production/beta/experimental), and their dependency relationships.

The tree is manually maintained, not generated. Generated trees are accurate but unreadable — they include every `__pycache__` directory and `.pyc` file. The manual tree includes only the files that matter for understanding the plugin architecture. Each entry has a one-line annotation explaining what it does.

Dependency relationships are marked with arrows: `03-bigquery-forecaster → 02-baseline-lab (forecast models)`. This makes it possible to understand the plugin graph without reading import statements. It also makes breaking changes visible — if you're modifying the Baseline Lab's output format, the tree tells you BigQuery Forecaster depends on it.

The tree also marks each skill's quality level (L1-L4) as of the latest CI run. At the time of writing: all 21 skills at L4. The tree is the single document that answers "what's in this repo and what shape is it in?" without requiring any other context.

## README Redesign: No Hype, Facts Only

The repo README got rewritten from scratch. The old version had the usual open-source project structure: badges at the top, a marketing paragraph, feature bullet points, installation instructions. Fine for a public library. Wrong for this repo.

The new README leads with what the repo contains: 3 production plugins, 21 skills at v2.3 compliance, CI with tiered cost optimization. No adjectives. No "powerful" or "flexible" or "enterprise-grade." Just counts and version numbers.

The installation section got replaced with a quickstart that's one command. The architecture section links to the architecture doc instead of duplicating it. The contribution section was removed entirely — this is an internal repo, not a community project.

The README is 87 lines. The old one was 210. Shorter by 59%. Every line in the new version earns its place by answering a question someone would actually ask within the first 5 minutes of looking at the repo.

The hardest line to cut was the feature comparison table against competing approaches. It was well-researched and genuinely useful. But a README comparison table says "we're insecure enough to need competitive positioning." The comparison lives in the architecture doc now, where it belongs — context for design decisions, not sales material at the front door.

v1.7.0 shipped at end of day. The repo that a reviewer would clone tomorrow is materially different from the one that existed yesterday morning — not in what it does, but in how clearly it communicates what it does and how safely it does it.

## Related Posts

- [21 Skills and a Production Validator: Nixtla v1.6.0](/posts/nixtla-21-skills-production-validator-v160/)
- [Three Releases in One Day: Nixtla Goes Enterprise](/posts/nixtla-enterprise-docs-restructure-v100-release/)
- [Marketplace Security Framework and Scanner False Positives](/posts/marketplace-security-framework-scanner-false-positives/)
