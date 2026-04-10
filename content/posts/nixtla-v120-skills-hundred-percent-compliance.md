+++
title = 'v1.2.0: Every Skill to 100% Compliance'
slug = 'nixtla-v120-skills-hundred-percent-compliance'
date = 2025-12-04T10:00:00-06:00
draft = false
tags = ["nixtla", "compliance", "skills", "documentation", "release-engineering"]
categories = ["Development Journey"]
description = "24 commits of systematic compliance remediation: every skill from ~38-40% to 100%, sales language stripped from the README, non-compliant doc names archived."
+++

24 commits. One release. The entire day was compliance remediation. Not the glamorous kind of engineering. The kind that makes everything else work correctly.

## The Starting Point

The skills infrastructure built on Dec 1 had the right structure but loose compliance. Each SKILL.md file scored between 38% and 40% against the compliance checker. Missing required fields, incomplete schemas, permissions that didn't match actual plugin requirements, usage examples that wouldn't parse.

100% was the target. Not 95%. Not "close enough." Every field filled, every schema valid, every example runnable. Partial compliance is worse than no compliance because it creates the illusion that the checker passed while leaving real problems hidden.

## The Grind

There's no trick to compliance work. You run the checker, read the failure list, fix each item, run the checker again. Repeat until green. The cycle time matters -- fast feedback loops make remediation tolerable. Slow feedback loops make it soul-crushing.

The compliance checker runs in under 2 seconds for all 8 skills. That's fast enough to run after every edit. If it took 30 seconds, the temptation to batch changes and check less frequently would win, and batching hides which change broke what.

The common failures across all 8 skills:

- **Input schemas** referenced types that didn't exist in the declared JSON Schema version
- **Output schemas** were missing `required` field declarations
- **Prerequisites** listed package names without version constraints
- **Usage examples** had placeholder values that wouldn't pass a syntax check
- **Permissions** requested broader access than the underlying plugin actually used

Each skill had roughly the same issues because they were all scaffolded from the same template. Fix the pattern once, apply it eight times. The first skill took 45 minutes. The eighth took 10.

The version constraint issue was the most insidious. Prerequisites listed `statsforecast` instead of `statsforecast>=0.7.0`. Without a version floor, the installer would happily pull in an ancient version missing the APIs the skill actually calls.

Every prerequisite got a minimum version pinned to the version tested against.

The permissions overreach was subtler. During scaffolding, skills got copy-pasted permission blocks from the most privileged skill. The Data Validation skill was requesting BigQuery write access when it only reads. The Forecast Export skill was requesting model training permissions when it only reads pre-computed results. Each skill's permissions got audited against its actual code paths.

## README Cleanup

The repo README had accumulated sales language over the past week. Phrases like "revolutionary forecasting capabilities" and "industry-leading precision" that crept in during the CEO-readiness push.

Stripped all of it. A technical README describes what the software does, how to install it, and how to use it. It doesn't sell. If the software is good, the description sells itself. If the software isn't good, marketing language in the README makes the gap between promise and reality worse. Nixtla's engineering team will read this README. They know what "revolutionary" actually costs.

## Non-Compliant Doc Names

Several documents from before the Doc-Filing v3.0 compliance push had names that didn't follow the `NNN-CAT-description.md` convention. Rather than rename them (which would break any existing links or references), they got archived to a `legacy-docs/` directory with a redirect note in each file pointing to its compliant replacement.

This is slower than bulk-renaming but doesn't break anyone's bookmarks or scripts that reference the old paths. Seven documents got archived this way. Each one took about 5 minutes -- rename, write the redirect note, verify the compliant replacement exists, update any cross-references in other documents that linked to the old name.

## v1.2.0

The release captures the state where every skill passes compliance at 100% and the README reads like technical documentation instead of a pitch deck.

No new features. No new skills. No new architecture. Just the existing codebase brought up to the standard it was supposed to meet from the beginning.

## What 100% Actually Means

100% compliance doesn't mean "perfect." It means every required field is present, every schema validates, and every example runs. The skills could still have bad descriptions, misleading examples, or permissions that are technically correct but unnecessarily broad.

Compliance is the floor, not the ceiling. The compliance checker catches structural problems -- missing fields, invalid syntax, type mismatches. It doesn't catch quality problems -- a description that says "does forecasting stuff" passes compliance but fails usefulness.

The next pass will address quality. Today was about getting the structure right so the quality pass has a stable foundation to work on.

## The 24-Commit Question

24 commits for compliance work looks like either poor planning or excessive granularity. It's the second one, deliberately. Each commit represents one logical change: "fix input schema for Baseline Forecast skill" or "remove sales language from section 3 of README."

The alternative -- one massive commit that touches 30 files -- makes it impossible to revert a single fix without reverting everything. Fine-grained commits cost more time during the day but pay it back the first time you need to `git revert` one specific change.

For compliance work specifically, the granularity also makes the review easier. A reviewer can approve "fix input schema types" without reading 30 unrelated changes. When the commit is small enough to hold in your head, the review takes 30 seconds instead of 15 minutes.

---

**Related Posts:**

- [Skills Infrastructure from Scratch: 8 SKILL.md Files, an Installer, and a Compliance Framework](/posts/nixtla-skills-pack-phase-zero-compliance/) -- the infrastructure this compliance push validates
- [Three Releases in One Day: Nixtla Goes Enterprise](/posts/nixtla-enterprise-docs-restructure-v100-release/) -- the enterprise standard that defined the compliance targets
- [Content Quality War: 7-Check Audit Across 340 Plugins](/posts/content-quality-war-7-check-audit-across-340-plugins/) -- compliance remediation at a larger scale
