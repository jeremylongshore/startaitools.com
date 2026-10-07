# 014 — Blog pipeline authority map: one source of truth per concern

| Field | Value |
|---|---|
| Date | 2026-10-05 |
| Status | Decision record. Inventory complete; authorities chosen; removals filed as beads, **not yet made** |
| Scope | The daily blog pipeline: producer skill, references and agents, lander and helpers, cron wrappers, schedulers, release and deploy workflows |
| Bead | `startaitools-9a8.1.1` (epic `startaitools-9a8.1`, GitHub #121) |
| Owner roles | Pipeline maintainer (code, cron, lander); editorial lead (instructions, tiers, voice) |

## 1. Why this exists

The pipeline states the same rule in several places, and they disagree. A writer agent receives
prose that says one thing while the lander enforces another. This record lists every place that
states a rule for five concerns (dates, paths, tier rules, release gates, contracts) plus the
scheduler instructions, shows the conflicts with file and line evidence, and names **one
authority per concern**.

**Selection rule.** Deterministic code beats prose instructions. Versioned in-repo files beat live
copies under `~/.claude/`. Prose may restate a rule only as a pointer to its authority.

**Path notation.** `R:` is this repository (`startaitools.com`). `G:` is the live skill tree under
`~/.claude/skills/` (versioned in a separate private skills repository; the scheduled producer
reads it live, unpinned). The **primary checkout** is the owner's long-lived clone of this repo
that host cron executes from; the **run workspace** is the isolated per-run git worktree the
daily producer writes into.

## 2. Component inventory

| Component | Files | Owner role | What it decides |
|---|---|---|---|
| Producer skill | G:`blog-backfill/SKILL.md` | Editorial lead | Phase order, finding selection, writer choice, which reviewers to dispatch |
| Producer references | G:`blog-backfill/references/*.md` (17 files incl. `run-contract.md`, `write-post.md`, `writer-briefing-template.md`, `classify-day.md`, `content-tier-classification.md`, `final-verification.md`, `cadence-system.md`, `content-strategy.md`, `gather-material.md`) | Editorial lead | Writer brief, tier treatment, staging and receipt instructions |
| Skill-local agents | G:`blog-backfill/agents/{blog-classifier,blog-consistency-checker,blog-fact-checker}.md` | Editorial lead | Classification and review prompts |
| Global agents | `~/.claude/agents/{content-marketer,docs-architect,code-reviewer,seo-*,fact-checker,article-consistency-checker}.md` | Pipeline maintainer | Writer and reviewer prompts. `fact-checker.md` and `article-consistency-checker.md` are **untracked** files in a third-party agents clone |
| Writer context | R:`scripts/blog/writer-context/writer-context-vN.md` rendered by R:`scripts/blog/blogpipe/writer.py` (`python3 -B -m blogpipe writer-context render`); added 2026-10-06, see 015 | Editorial lead (text), pipeline maintainer (renderer) | Exactly what the writer agent receives; the run records the version |
| Instruction tests | G:`blog-backfill/tests/test_contract_instructions.py` | Editorial lead | Asserts contract phrases stay present in the prose |
| Related skills | G:`blog-calibrate/SKILL.md`, G:`blog-feedback/SKILL.md`, G:`blog-research-article/SKILL.md` | Editorial lead | Monthly calibration, feedback grading, manual long-form lane |
| In-repo skill scripts and data | R:`.claude/skills/blog-backfill/scripts/*` (`apply-patterns.py`, `lint-post-voice.py`, `feedback-sweep.py`, `tier-creep-guard.py`), R:`.claude/skills/blog-backfill/methodology/*.jsonl` | Pipeline maintainer | Pattern application, voice lint, length grading, tier-mix tripwire, decision and feedback records |
| Daily wrapper | R:`scripts/blog/blog-backfill-daily.sh`, R:`scripts/blog/lib-cron-common.sh`, R:`scripts/blog/blog-run-workspace.py`, R:`scripts/blog/claude-minimax-producer.py` | Pipeline maintainer | Target date, lock, isolated workspace, producer launch, git shim |
| Producer contract | R:`scripts/blog/blog-producer-contract.py` → R:`scripts/blog/blogpipe/{contract,roles,records,schema,brief,switch}.py` | Pipeline maintainer | Required agents per tier, receipt validity, record schema, dated enforcement switches |
| Lander | R:`scripts/blog/blog-land.sh`, R:`scripts/blog/blogpipe/publication.py`, R:`scripts/blog/pilot_release_gate.py` | Pipeline maintainer | Preconditions, quarantine, tier-length gate, pilot gate, commit and push, ledger and queue rows, liveness |
| Periodic wrappers | R:`scripts/blog/{blog-feedback-sweep,blog-tier-creep-guard,blog-monthly-calibrate,blog-monthly-retro,blog-posting-packet,blog-crosspost-sweep,blog-syndication-ingest,blog-team-rollup,next-topics-refresh,blog-recommendation-worker,web-analytics-daily}.sh`, `native-metrics-devto.py` | Pipeline maintainer | Weekly and monthly grading, distribution, reporting |
| Scheduler | Host `crontab` (not versioned); schedule table in R:`CLAUDE.md:294-304` | Pipeline maintainer | When each wrapper runs |
| Release and deploy | R:`.github/workflows/release.yml` (on push to `master`) → `scripts-lint.yml` (verify) → `deploy.yml` (build and deploy) | Pipeline maintainer | Whether a landed commit is released and served |

## 3. Chosen authority per concern

| Concern | Authority | Rationale |
|---|---|---|
| Dates | R:`lib-cron-common.sh:378-392` `resolve_target_date` (host-local yesterday; host clock fixed at UTC-06:00) plus R:`blogpipe/contract.py:76` (front-matter date must equal the target date); front-matter offset `-06:00` | Code decides the day and refuses a mismatched post; `-06:00` matches the host clock and the gather queries |
| Paths | The run workspace bound by R:`blog-run-workspace.py` and validated by the lander (R:`blog-land.sh:229`); G:`run-contract.md:6-9` is its prose mirror | Only the workspace write-set is validated; absolute primary-checkout paths are demoted to read-only examples already |
| Tier rules (classification) | R:`.claude/skills/blog-backfill/scripts/apply-patterns.py` with active rows in R:`methodology/patterns.jsonl`; tier domain 1-3 in R:`blogpipe/contract.py:101` | Deterministic pattern application and contract validation; prose cites pattern IDs that are retired |
| Tier rules (length) | R:`blog-land.sh:457-458` `LAND_TIER1_MAX_LINES=145`, `LAND_TIER2_MAX_LINES=260`, kept equal to R:`feedback-sweep.py:50-51` by R:`tests/test_blog_pipeline.py:1325-1328` | The only binding length rule; it sets the shipped tier |
| Release and publication gates | R:`blogpipe/roles.py:130-148,249-277` (required reviewers per tier) plus the lander precondition gate R:`blog-land.sh:226-428` (contract, sentinel, voice lint, Hugo, quarantine), R:`pilot_release_gate.py`, then `release.yml` → `scripts-lint.yml` → `deploy.yml` | What code requires is what actually blocks; prose tables cannot add or remove a gate |
| Contracts (receipts, schemas) | R:`blogpipe/contract.py`, `roles.py`, `records.py`, `schema.py` via R:`blog-producer-contract.py`; G:`run-contract.md` is the prose mirror held by G:`tests/test_contract_instructions.py` | Code validates every receipt and record; the mirror is tested |
| Schedule | Host crontab entries that invoke R:`scripts/blog/*.sh`; R:`CLAUDE.md` schedule table is the versioned mirror until a versioned crontab manifest exists | Cron is what runs; G:`SKILL.md:405-411` already forbids a parallel RemoteTrigger |

## 4. Conflicts, with evidence

Every row is a place that states a rule differently from its authority. Line numbers are as of
the date above.

### 4.1 Scheduler instructions that describe jobs that do not exist

| Where | Says | Reality |
|---|---|---|
| G:`references/cadence-system.md:11-13` | Daily 6:17, weekly Friday 5:42, monthly 8:23 CT, "RemoteTrigger cron" | Daily runs from host cron at 04:00; no RemoteTrigger exists; no weekly job |
| G:`references/cadence-system.md:149-205` | Full RemoteTrigger prompts, including "Commit, push to master, verify Netlify deploy" | Producer must not run git; Netlify is retired |
| G:`SKILL.md:12,38,115,353-355,384,434` | A "Phase 2W: Weekly Recap" and a `weekly` argument writing `week-NN-recap-YYYY.md` | No wrapper, no cron entry; zero weekly recaps have ever shipped |
| G:`SKILL.md:410-411` | "Weekly and monthly workflows have their own established wrappers" | True for monthly only |
| G:`references/content-strategy.md:13,31-32,61,100` | Weekly recaps as an aggregation layer | Not produced |
| R:`CLAUDE.md:294-304` | Cron table | Omits three live jobs (05:30 crosspost sweep, 06:15 native metrics, Sunday 12:00 recommendation worker) |

### 4.2 Four gate lists, none equal to the code

| Where | Tier 1 | Tier 3 |
|---|---|---|
| G:`SKILL.md:286-294` | Voice lint, Hugo, code-reviewer if code, `blog-consistency-checker` (unconditional tick) | Adds both fact-checkers; table omits `seo-content-auditor` (named only in prose at :282-283) |
| G:`references/write-post.md:396,411,429` | "Hugo build passes." only | "Hugo build + consistency audit + deeper code analysis" (no fact-check) |
| G:`references/content-tier-classification.md:13-16` | "Hugo build + consistency audit (one checker)" | "code analysis", no fact-check; adds a Tier 4 the code rejects |
| G:`references/final-verification.md:30-32` | Writer, code-reviewer, consistency checker, SEO meta, Hugo; no voice lint | Matches code |
| R:`methodology/publishing-gates.md` | A fifth, "non-negotiable" verifiability pass with no consumer and no records | — |
| **Code** R:`roles.py:142-147,261-262` | Tier 1 consistency checker required only from the dated switch (`brief.py:53`, 2026-10-14; observed before) | Both fact-checkers **and** `seo-content-auditor` |

### 4.3 Four length rules, one binding

| Where | Rule |
|---|---|
| G:`SKILL.md:258-260`, G:`write-post.md:381,398,413`, G:`writer-briefing-template.md:86-88`, G:`content-tier-classification.md:13-15` | Target bands 80-140 / 150-250 / 300-500 lines |
| G:`write-post.md:379`, G:`writer-briefing-template.md:154` | "about 1,500 words of prose" hard cap |
| G:`write-post.md:392` | No-finding notes "under 300 words" |
| G:`writer-briefing-template.md:91` | "The longest post this pipeline accepts is 500 lines" (nothing enforces a maximum) |
| **Binding** R:`blog-land.sh:457-458,469-475` | 145 / 260 body lines decide the shipped tier |
| R:`blogpipe/publication.py:146-147` | Re-states 145 / 260 as bare literals, outside the parity test |

Line counting between lander and grader is a separate open item (`startaitools-9a8.7.7`).

### 4.4 Primary-checkout paths

| Where | Kind | Evidence |
|---|---|---|
| G:`write-post.md:3,49` | Writer **write** path | "Write directly to `<primary checkout>/content/posts/SLUG.md`" |
| G:`writer-briefing-template.md:31,206` | Writer **write** path handed to the agent verbatim | "Write the file to `<primary checkout>/content/posts/{{SLUG}}.md`" |
| G:`final-verification.md:11,22,56` | Runs lint and index rebuild against the primary checkout | absolute script paths |
| G:`gather-material.md:12,80,86`; G:`classify-day.md:43` | Executes scripts and reads the 14-day decision window from the primary checkout | stale whenever the checkout lags origin |
| G:`blog-calibrate/SKILL.md:37-39,140` | Reads records and **writes** the calibration report in the primary checkout | — |
| R:`blog-monthly-calibrate.sh:43,72,140-141` | **Commits and pushes** in the primary checkout | `git -C "$BLOG_DIR" commit` then `push origin HEAD` |
| R:`blog-monthly-retro.sh:36,94,104` | Runs the producer skill headless **in** the primary checkout, which commits there | — |
| R:`tier-creep-guard.py:35-37` | Default data path is the primary checkout | read-only, can be stale |
| R:`CLAUDE.md:21,191` | "work is not complete until `git push` succeeds" | Loaded by the producer, which must not run git; only the git shim (`blog-backfill-daily.sh`) resolves it |

Resolved, kept for the record: the weekly feedback sweep no longer touches the primary checkout
(R:`blog-feedback-sweep.sh:36-49`). The ledger and queue files the lander writes beside the
primary checkout are git-ignored run state (`BLOG_STATE_DIR`), not source, and are out of scope.

### 4.5 Dates and timezone

| Where | Says |
|---|---|
| G:`write-post.md:57`, G:`gather-material.md:38` | `-06:00` |
| G:`writer-briefing-template.md:192` | `date = {{DATE}}T{{TIME}}-05:00` |
| R:`CLAUDE.md:86` | Either `-05:00` or `-06:00` is allowed |
| G:`cadence-system.md:11-13` | Schedule in "CT" (covered by 4.1) |
| R:`blog-land.sh:85` | Its own `date -d "yesterday"` default, which ignores the `BLOG_CLOCK` override that `resolve_target_date` honours (minor; the wrapper always passes the date) |

### 4.6 Tier classification and distribution prose

| Where | Says | Authority says |
|---|---|---|
| G:`agents/blog-classifier.md:59` | Pattern `auto-2026-06-001` | Retired (`patterns.jsonl`) |
| G:`classify-day.md:74` | Pattern `auto-2026-07-001` | Retired; only `auto-2026-08-001` is active |
| R:`tier-creep-guard.py:6,56` and R:`CLAUDE.md:303` | Bands 60-70 / 25-35 / 5-10 | Alerts fire at T2 > 40, T1 < 52, T3 > 12, T1 > 85 (`tier-creep-guard.py:60-63`) |
| G:`content-strategy.md:57` | Tier 1 gets an "Optional X post" | G:`SKILL.md:351` and the lander: X + LinkedIn packet |
| G:`content-tier-classification.md:16`, G:`blog-research-article/SKILL.md` | Tier 4 records into `decisions.jsonl` | R:`contract.py:101` accepts tiers 1-3 only (left to the editorial-lane design, `startaitools-bhn.8`) |

### 4.7 Contracts

| Where | Says | Authority says |
|---|---|---|
| G:`final-verification.md:36-50` | The `agent_audit` schema lives in `polish-seo.md`, nested `consistency.skill_local/global` | Record kinds and enums live in R:`blogpipe/records.py` and `schema.py` |
| R:`methodology/publishing-gates.md` | A record shape for a verifiability pass | No consumer; the contract would reject the shape |

## 5. Conflicts filed for change

Nothing in this record changes code or instructions. Each removal or alignment is a bead under
epic `startaitools-9a8.1`; the bead acceptance asks for a reviewed diff.

| Conflict (section) | Bead | Change |
|---|---|---|
| 4.1 weekly recap and RemoteTrigger | `startaitools-9a8.1.5` | Remove the weekly phase and the RemoteTrigger schedules |
| 4.2 gate lists, 4.7 contracts | `startaitools-9a8.1.6` | One gate table that matches `roles.py`, pointers elsewhere |
| 4.3 length rules | `startaitools-9a8.1.7` | One binding rule; prose bands labelled as targets; shared constants |
| 4.4 instruction paths | `startaitools-9a8.1.8` | Workspace-relative paths in writer and verification instructions |
| 4.4 periodic jobs in the primary checkout | `startaitools-9a8.1.9` | Monthly jobs and the tier-creep default path off the primary checkout |
| 4.5 timezone | `startaitools-9a8.1.10` | One front-matter offset everywhere |
| 4.6 tier prose | `startaitools-9a8.1.11` | Cite `apply-patterns.py`, drop retired IDs, print real thresholds |
| 2 unversioned reviewers | `startaitools-9a8.1.12` | Version the two global reviewer agents |
| 4.1 schedule mirror | `startaitools-9a8.1.13` | Version the cron schedule and check it against the host |

## 6. Acceptance status

- **Versioned authority map:** this document.
- **Duplicate or nonexistent scheduler instructions, four gate lists, four length rules and
  primary-checkout write paths removed in a reviewed diff:** **open.** The removals are the beads
  in section 5; this record only names the authority each removal must point at.
