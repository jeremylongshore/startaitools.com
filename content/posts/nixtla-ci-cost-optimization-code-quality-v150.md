+++
title = 'CI Cost Optimization and Code Quality Enforcement: Nixtla v1.5.0'
slug = 'nixtla-ci-cost-optimization-code-quality-v150'
date = 2025-12-07T10:00:00-06:00
draft = false
tags = ["ci-cd", "python", "devops", "code-quality", "cost-optimization"]
categories = ["Development Journey"]
description = "Tiered CI approach cutting costs 90%, Black/isort/flake8 enforcement, secrets scanning fixes, YAML parsing bugfix, and Doc-Filing v3 restructure — Nixtla v1.5.0."
+++

22 commits. Most of them were about spending less money on things that don't need to be expensive.

The Nixtla workspace hit v1.5.0 today. Not a feature release — a governance release. Every commit was about making the existing codebase cheaper to run, safer to maintain, and easier to read. The kind of release where the changelog is boring and the impact is permanent.

## The CI Cost Problem

The Nixtla workspace had been running every check on every push. Full test suite, linting, type checking, documentation validation, secrets scanning — all of it, every time, regardless of what changed. A typo fix in a README triggered the same 8-minute pipeline as a core forecasting algorithm change.

GitHub Actions minutes aren't free after a certain threshold, and the burn rate was climbing. More plugins meant more tests meant more minutes. The math was heading in the wrong direction.

At the current trajectory — adding roughly one plugin per week and 5-8 skills per plugin — the CI bill would triple within two months. Fixing this after the cost hits is reactive. Fixing it now, with three plugins in the workspace, is a 22-commit afternoon. The best time to optimize CI costs is before the cost becomes a problem.

Three plugins also means the tiered approach is testable with real data — enough diversity to exercise path filtering but few enough that a full Tier 3 run completes in reasonable time.

## Tiered CI

The fix was a three-tier approach:

**Tier 1 (every push):** Linting, formatting, secrets scanning. Fast checks that catch the most common problems. Under 30 seconds.

**Tier 2 (changed paths):** Unit tests scoped to modified plugins. If you only touched the BigQuery Forecaster, only BigQuery Forecaster tests run. Path filtering in GitHub Actions using `paths` triggers on the workflow and `dorny/paths-filter` for the job matrix.

**Tier 3 (release branches + manual):** Full integration suite. Every plugin, every test, every validation. The expensive stuff runs when it matters — before releases and when you explicitly ask for it.

Result: ~90% reduction in CI minutes on feature branch pushes. The pipeline that took 8 minutes now takes 40 seconds for a typical commit. The full suite still runs before anything ships.

The implementation uses a composite workflow. A single `.github/workflows/ci.yml` file with three jobs instead of three separate workflow files. The jobs share a checkout step (cached) and diverge at the check layer. This matters because GitHub Actions charges per-job for the runner startup. Three separate workflows mean three runner boots. One composite workflow with three jobs means one boot with parallel job execution.

The path filter configuration was the fiddly part. `dorny/paths-filter` outputs a JSON object mapping filter names to booleans. The downstream job matrix reads these outputs and conditionally includes or excludes test suites. Getting the YAML right took four commits — the output variable syntax for cross-job references in GitHub Actions is one of those things that looks simple in the docs and breaks in practice because of quoting rules.

## Code Quality Enforcement

Black, isort, and flake8 got added as pre-commit hooks and CI gates simultaneously. Not sequentially — both at once. If you add the CI check first, you spend a week reformatting old code to pass. If you add pre-commit first, people bypass it. Both at the same time means the first PR after merge either passes or fails immediately. No ambiguity about whether formatting is optional.

Black with default settings. isort with Black-compatible profile. flake8 with a short ignore list (E501 for line length since Black handles that, W503 for line breaks before binary operators). The ignore list is documented in `setup.cfg` with a comment explaining why each rule is suppressed.

Every existing Python file got reformatted in a single commit. One commit, one diff, done. Mixing formatting changes with logic changes makes git blame useless. Separate commit means you can always `git blame --ignore-rev` the formatting commit.

The reformatting touched 47 files. Most changes were trivial — trailing whitespace, single vs. double quotes, import ordering. A few files had Black make more aggressive changes: splitting long function signatures across multiple lines, reformatting nested dictionary literals, and adding trailing commas to function call arguments. Every one of these is a valid Black decision, but reviewing a 47-file diff where most changes are whitespace and a few are structural requires patience.

The `.git-blame-ignore-revs` file now has exactly one entry. It will probably stay that way — the point of enforcing formatting from now on is that you never need another mass-reformat commit.

## Secrets Scanning

The existing secrets scanner was throwing false positives on base64-encoded test fixtures. A test that validates JWT parsing had a hardcoded expired token — technically a secret pattern, practically worthless. The scanner flagged it on every run.

Fixed by adding a `.secret-scan-baseline` file that whitelists known false positives with inline justification. Each entry includes the file path, the matched pattern, and a one-line reason it's safe. The scanner still runs, but it diffs against the baseline instead of the full codebase. New secrets get caught. Old false positives stay quiet.

The baseline file is itself scanned — you can't hide a real secret in the allowlist by claiming it's a false positive. The scanner checks that every baselined pattern matches the declared file path and that the declared file path still exists. If someone deletes the test file containing the JWT fixture but leaves the baseline entry, the scanner flags it as a stale exemption. Stale exemptions are treated as warnings, not errors, but they show up in the CI summary.

Beyond the false positive fix, the scanner got a new rule: no `.env` files in the repository, period. Not `.env.example`, not `.env.test`, not `.env.local`. Environment configuration goes in `setup.cfg` or in CI secrets. The `.env` convention is too easy to accidentally populate with real values and commit. Two of the three plugins had `.env.example` files. Both got converted to a `[tool:env]` section in their respective `setup.cfg` files with comments documenting each required variable.

## YAML Parsing Fix

A subtle bug in the skill manifest loader: YAML files with trailing whitespace on empty lines were parsed differently by PyYAML vs. the GitHub Actions YAML parser. A manifest that validated locally failed in CI. The root cause was `yaml.safe_load` treating `key: \n` (with trailing space) differently than `key:\n` (without). The fix was normalizing whitespace before parsing. Three lines of code, two hours of debugging.

The frustrating part: the CI log said "invalid YAML" with no line number. PyYAML's error messages for whitespace issues are famously unhelpful. The debugging technique that worked was binary-search diffing: copy the YAML from the CI runner's debug output, paste it locally, compare byte-for-byte against the source file. `diff <(xxd file1.yml) <(xxd file2.yml)` revealed the trailing `0x20` on line 14 instantly. Hex dump diff is the nuclear option for "these files look identical but behave differently."

## Doc-Filing v3 Restructure

Documentation got renumbered and recategorized under the v3 convention. Architecture docs (001-series), plugin docs (100-series), operational docs (200-series). The numbering creates a natural sort order that matches how you'd browse the docs: understand the system first, then the plugins, then how to operate them.

The migration script handled renumbering but cross-references required manual updates. 11 documents referenced other documents by number. Changing document 037 to document 103 means finding every `037-` reference in every other document and updating it. A `sed` one-liner handled the substitution but verifying correctness required reading each reference in context. Automation does the replacement. Humans verify the replacement makes sense.

v1.5.0 is the version where the Nixtla repo became maintainable. Not feature-complete, not production-ready — maintainable. CI costs are controlled. Code formatting is enforced. Secrets are scanned with a sane baseline. Documentation has a navigable structure. Everything from here builds on solid ground.

## Related Posts

- [Three Releases in One Day: Nixtla Goes Enterprise](/posts/nixtla-enterprise-docs-restructure-v100-release/)
- [Nixtla Baseline Lab: Phases 4 Through 8 in a Single Day](/posts/nixtla-baseline-lab-phases-four-through-eight/)
- [Building Production CI/CD: Documentation to Deployment](/posts/building-production-ci-cd-documentation-to-deployment/)
