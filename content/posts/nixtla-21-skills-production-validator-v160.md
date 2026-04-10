+++
title = '21 Skills and a Production Validator: Nixtla v1.6.0'
slug = 'nixtla-21-skills-production-validator-v160'
date = 2025-12-08T10:00:00-06:00
draft = false
tags = ["python", "claude-code-plugins", "architecture", "automation", "code-quality", "testing"]
categories = ["Technical Deep-Dive"]
description = "66 commits in one day: extracted embedded Python from 8+ skills, built a production SKILL.md validator with 14 critical fixes, audited skills through 3 spec versions, and shipped the TimeGPT lab phases 03-06."
+++

66 commits. The biggest single-day push the Nixtla repo has seen. Three major workstreams running in parallel: skill extraction, validator construction, and TimeGPT lab expansion. Each one would have been a reasonable day on its own.

The commit rate was sustainable because yesterday's CI optimization eliminated the feedback loop bottleneck. Every push validated in under a minute. That changes behavior — you commit smaller, more frequently, with higher confidence. The 66 commits aren't 66 features. They're 66 incremental steps where each one was tested before the next began.

The three workstreams interleaved rather than ran sequentially. Extract a skill, validate it with the in-progress validator, fix the validator based on what the extraction revealed, then extract the next skill. The validator improved because it had real test subjects. The extractions went faster because the validator caught mistakes immediately. Parallel workstreams with shared feedback loops outperform serial execution when the workstreams inform each other.

## Embedded Python Extraction

Eight skills had Python code embedded directly in their SKILL.md files. Fenced code blocks with executable logic — argument parsing, API calls, file I/O — sitting inside markdown documentation. It worked because Claude Code can extract and run fenced blocks, but it was wrong for every other reason.

The problems with embedded code were both obvious and ignored until the tooling forced the issue:

1. **No linting.** Black, flake8, and isort can't see code inside markdown fences. The formatting enforcement from yesterday? It only applied to `.py` files. Embedded code was a formatting free zone.
2. **No testing.** You can't import a function from a markdown file. Every embedded script was untested by definition. The only validation was "run it and see."
3. **No IDE support.** Jump-to-definition doesn't work. Autocomplete doesn't work. Syntax highlighting works but nothing else does. Developing inside a markdown code fence is writing Python with the tools turned off.
4. **No type checking.** mypy and pyright skip markdown files entirely. Type errors that would be caught instantly in a `.py` file hide indefinitely inside fenced blocks.
5. **Merge conflicts.** Markdown diffs are terrible. A one-line Python change inside a 200-line SKILL.md creates a diff that's nearly impossible to review.

The extraction followed the same process for each of the 8 skills: pull the Python out into a standalone `.py` file, replace the fenced block with a reference to the file, update the SKILL.md invocation section, add a `script:` field to the frontmatter pointing to the new file, and verify the skill still works through the plugin runtime.

The standalone files followed a naming convention: `main.py` for the primary entry point, `utils.py` for shared helpers, `config.py` for configuration parsing. Every extracted skill got the same directory structure regardless of complexity. A simple skill with 20 lines of Python gets the same layout as a complex skill with 200 lines. The consistency matters more than the optimization — when you open any skill directory, the file structure is predictable.

The tricky part was invocation paths. When Python lived inside the SKILL.md, the runtime extracted it to a temp directory and ran it from there. Standalone scripts live in the skill's own directory. Every file path reference — config files, output directories, log locations — needed updating. Three of the eight skills had hardcoded `/tmp/` paths that assumed the temp directory structure. Those became relative paths resolved against the skill's root.

One skill had a particularly nasty path issue. It used `__file__` to resolve a sibling config file — a common Python pattern. Inside a fenced code block extracted to a temp file, `__file__` points to `/tmp/extracted_abc123.py`. In its permanent home, `__file__` points to `skills/07-data-validator/main.py`. The config file resolution worked in both locations because the skill happened to copy the config to the same relative path in both cases. Pure luck. The fix was explicit config path injection via the skill's parameter schema instead of relying on `__file__` resolution.

After extraction, every skill's Python code was visible to the linting pipeline. Black immediately flagged 23 formatting issues across the 8 files. isort reordered imports in 6 of them. flake8 found 4 unused imports and 2 bare `except` clauses. None of these were bugs — the code worked fine — but they were invisible technical debt that accumulated because the code lived outside the toolchain's reach.

The bare `except` clauses were the most concerning. A skill that catches every exception silently — including `KeyboardInterrupt` and `SystemExit` — can hang indefinitely if something goes wrong. Both were narrowed to catch specific exceptions: `requests.RequestException` for network failures, `json.JSONDecodeError` for malformed API responses. The skill should handle expected failures and let unexpected ones propagate to the runtime.

## Four Skills Refactored for Compliance

Beyond extraction, four skills needed structural refactoring to meet the current spec. The spec had evolved through three versions (v2.1, v2.2, v2.3) while these skills were frozen at v2.0 conventions.

The changes per skill varied but the pattern was consistent:

- **Frontmatter fields**: v2.2 added `min_claude_version` and `requires_network`. Both were missing from all four skills.
- **Parameter schemas**: v2.3 tightened the JSON Schema for skill parameters. Three skills used `additionalProperties: true` where the spec now requires explicit property definitions.
- **Error handling section**: v2.2 made the error handling section mandatory. Two skills had error handling in their Python code but didn't document it in the SKILL.md. The validator flags this as a compliance failure — documented error handling is a contract with the user, not just an implementation detail.
- **Output format section**: v2.3 requires skills to declare their output format — JSON, plain text, file path, or structured data. This section was entirely absent from all four skills because it didn't exist in v2.0.

Each refactored skill got a full manual test: invoke, pass valid parameters, pass invalid parameters, verify error messages match the documented behavior. Automated testing catches schema mismatches. Manual testing catches the cases where the schema is technically correct but the user experience is broken.

The manual testing surfaced one genuine bug: a skill's error handling section documented a `ParameterValidationError` exception, but the Python code raised `ValueError`. The error class name in the docs was aspirational — someone wrote the docs first and never updated the implementation. The fix was renaming the exception class to match the docs, not the other way around. The docs represented the intended contract. The code was the one that drifted.

This is a design principle worth stating explicitly: when docs and code disagree, fix the code unless you can articulate why the docs were wrong. Docs represent the user-facing promise. Code represents the current implementation. Promises outrank implementations. The custom exception class also provides better error messages — `ParameterValidationError("'horizon' must be a positive integer, got -3")` tells the user exactly what to fix, while `ValueError("-3")` does not.

## The SKILL.md Production Validator

This is the piece that will outlive the Nixtla project.

The validator started as a linting script and ended as a 14-check production-grade tool. The initial version just checked frontmatter fields against a schema. By commit 40-something, it was catching problems I didn't know existed.

The architecture is deliberately simple: a Python script with 14 functions, each returning a pass/fail result with an error message. No plugin system, no configuration file, no extensibility hooks. Adding a check means adding a function and registering it in a list. Removing a check means deleting a function. The entire validator is a single file under 400 lines. It stays readable because it stays flat.

### The 14 Checks

1. **Frontmatter presence** — SKILL.md must start with a valid TOML or YAML frontmatter block
2. **Required fields** — name, version, description, author, min_claude_version, requires_network
3. **Field types** — version must be semver, requires_network must be boolean
4. **Character limits** — name under 50 chars, description under 200 chars
5. **Name format** — kebab-case, no underscores, no spaces, no uppercase
6. **Version format** — strict semver (MAJOR.MINOR.PATCH, no v-prefix)
7. **Description quality** — third-person detection (flags "I" and "my" in descriptions)
8. **Section presence** — required sections: Description, Parameters, Usage, Error Handling
9. **Section ordering** — sections must appear in spec-defined order
10. **Parameter schema** — JSON Schema block must parse and validate against meta-schema
11. **Code block language tags** — every fenced code block must have a language identifier
12. **Internal link validity** — section references within the SKILL.md must resolve
13. **Trailing whitespace** — no trailing whitespace in any line (the YAML parsing lesson from yesterday)
14. **File size** — SKILL.md must be under 50KB (Claude Code has context window constraints)

### Third-Person Detection

Check #7 was the most interesting to build. Skill descriptions should read as documentation, not personal narrative. "Analyzes time series data" not "I analyze time series data." The detector scans the description field for first-person pronouns at sentence boundaries. Simple regex, high impact — it caught 6 of the 21 skills using first-person voice.

The false positive rate was initially terrible. "Mississippi" contains "I" in the middle. The fix was anchoring the pattern to word boundaries and sentence starts: `\b[Ii]\b` at the start of a sentence, `\b[Mm]y\b` anywhere. Still not perfect — "my" in "pymysql" triggers it — so there's a small allowlist for known compound words.

The six rewritten descriptions all followed the same pattern: swap the subject from first person to the skill name or an impersonal construction. "I fetch search results and summarize them" became "Fetches search results and generates AI-powered summaries." The rewrite isn't just cosmetic — it forces the description to be about the skill's capability, not the author's intent. That distinction matters when 21 skills are listed in a catalog and the user is scanning descriptions to find the right one.

### The Audit Trail

Every skill got audited against all three spec versions sequentially. v2.1 first (the most permissive), then v2.2, then v2.3. This wasn't about passing — it was about understanding what changed. A skill that passes v2.1 but fails v2.3 tells you exactly which spec evolution broke it. Running all three versions produces a diff that reads like a changelog for each skill's compliance status.

The audit covered all 21 skills. Results: 14 passed v2.3 after the day's fixes. 7 needed the extraction + refactoring work described above. Zero skills were left in a failing state by end of day.

The validator outputs a JSON report per skill with pass/fail per check, the specific error message for failures, and a compliance score (0-14). The aggregate report across all skills is a single table: skill name, compliance score, failing checks. This table gets committed to `reports/skill-compliance.json` on every CI run. The historical record shows compliance trajectory over time — useful for proving to a reviewer that quality is trending up, not just claiming it.

The validator itself has tests. 14 checks means 14 positive test cases and 28 negative test cases (each check has at least a "missing" and a "malformed" failure mode). The test suite for the validator is larger than the validator. This is correct — a validation tool that isn't exhaustively tested is worse than no validation tool because it creates false confidence.

The negative test cases were built from real failures encountered during the day's audit. Each time a skill failed a check, the specific failure became a test fixture. By end of day, the test suite was a catalog of every way a SKILL.md can be wrong. That catalog is the validator's most valuable artifact — more valuable than the validator code itself, because the catalog defines what "wrong" means for this ecosystem.

## TimeGPT Lab: Phases 03-06

While the validator and extraction work dominated the commit count, the TimeGPT lab advanced through four phases:

**Phase 03:** API client wrapper with retry logic and rate limiting. TimeGPT's API has aggressive rate limits for free-tier keys. The wrapper implements exponential backoff with jitter, capped at 3 retries. After the third failure, it falls back to the local statsforecast baseline and logs a warning. The fallback is the key design decision — a benchmark that fails when the paid API is unavailable is useless for development. The local baseline is always available, always free, and provides the comparison denominator regardless of API status.

**Phase 04:** Benchmark harness comparing TimeGPT forecasts against local baselines. Same M4 Monthly dataset from the Baseline Lab. The harness runs both models on identical data splits and produces a comparison table: sMAPE, MASE, and RMSSE for each model at each horizon. The split strategy matters: 80/20 temporal split with no shuffling, because time series data has temporal dependencies that random shuffling destroys. The last 20% of each series is the test set. Always.

**Phase 05:** Visualization layer. Forecast comparison charts as PNG output using matplotlib. Nothing fancy — line plots with confidence intervals, actual vs. predicted overlays, and a residual plot. The point is quick visual sanity checking, not publication-quality graphics. Each chart includes the model name, the sMAPE score, and the forecast horizon in the title. A CEO looking at the chart can tell which model won without reading the code or the comparison table.

**Phase 06:** Documentation and integration testing. Every phase got a test. The test for Phase 03 mocks the API client to avoid hitting the real endpoint. Phase 04 tests use the mocked client and verify the comparison table structure. Phase 06 is the integration test that runs the full pipeline end-to-end with a real API call (skipped in CI, run manually before release).

The four phases represent a shift in the Baseline Lab's purpose. Phases 01-02 (from earlier in the week) established that statsforecast's open-source models produce reliable baselines. Phases 03-06 establish how those baselines compare to TimeGPT's commercial offering. The benchmark harness isn't just testing — it's building the evidence base for a conversation with Nixtla's team about where the value boundary lies between free and paid offerings. The numbers matter because they'll be shown to the CEO.

## Numbered Directory Restructure

The workspace directory layout got rationalized. Plugins moved to a `plugins/` directory with numbered prefixes (01-search-to-slack, 02-baseline-lab, 03-bigquery-forecaster). Skills moved to `skills/` with their own numbering. The numbering isn't just aesthetics — it defines load order for the plugin runtime. Plugin 01 initializes first, which matters when plugins have cross-dependencies.

The restructure was a single commit with 47 file moves. Every import path, every relative reference, every CI workflow path filter — all updated atomically. This is the advantage of doing the CI path-filter work yesterday: the paths were already parameterized in the workflow, so updating them was a config change, not a workflow rewrite. If the path filters had been hardcoded, this restructure would have broken CI and required a separate fix commit.

Skills got a parallel numbering scheme: 01 through 21, grouped by plugin. Skills 01-07 belong to search-to-slack, 08-14 to baseline-lab, 15-21 to bigquery-forecaster. The grouping is conventional, not enforced — a skill's plugin assignment is declared in its frontmatter, not implied by its directory number. But the numbering makes `ls` output readable at a glance.

## Workspaces Layer

A new `workspaces.json` configuration defines named workspace contexts. Each workspace specifies which plugins and skills are active, which environment variables are required, and which CI tier to apply.

Three workspaces ship with v1.6.0:

- **default** — loads all plugins and skills, runs full CI. For release preparation and comprehensive testing.
- **bigquery** — loads only the BigQuery Forecaster plugin and its dependencies. For focused development on the data pipeline.
- **dev** — loads all plugins but skips integration tests and disables the secrets scanner. For rapid iteration when you're making changes you know are safe.

This is the foundation for multi-user support. Different team members can activate different workspace configurations without stomping on each other's environment variables or CI settings.

The workspace concept also solves a CI cost problem. The tiered CI from yesterday scopes tests by changed paths. Workspaces scope tests by intent. A developer working on the BigQuery Forecaster doesn't need search-to-slack tests even if they modify a shared utility function. The workspace config tells CI "this change is in the bigquery context" and the test matrix adjusts accordingly.

The workspace configuration is validated by the same CI pipeline it configures. A workspace that references a nonexistent plugin or an invalid environment variable name fails the Tier 1 lint check. This prevents the "config works on my machine" problem where someone adds a workspace locally, never pushes it, and the CI config drifts from what's actually available.

66 commits is too many for one day. It's evidence that the previous days' foundational work — CI tiers, formatting enforcement, doc structure — removed enough friction that the actual feature work could flow without interruption. The infrastructure investment paid off within 48 hours. The validator alone will save more time in the next month than the entire day cost to build — every future skill gets validated automatically instead of manually reviewed against a spec document.

v1.6.0 is the release where the Nixtla workspace became a product with quality guarantees. Not "probably works." Not "works if you follow the setup instructions exactly." 21 skills, all passing 14 automated checks, all tested, all documented, all linted. The compliance report is committed to the repo as proof.

Tomorrow's work — security hardening and documentation redesign — builds on this foundation. The hard part is done.

## Related Posts

- [CI Cost Optimization and Code Quality Enforcement: Nixtla v1.5.0](/posts/nixtla-ci-cost-optimization-code-quality-v150/)
- [Nuclear Option Day: Validator Rewrite, 63 New Packs, 414 Plugins](/posts/nuclear-option-day-validator-rewrite-414-plugins/)
- [Nixtla Baseline Lab: Real statsforecast Baselines via MCP Server](/posts/nixtla-baseline-lab-real-statsforecast-mcp-server/)
