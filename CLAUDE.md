# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Read this file first every session before touching code or content. It holds the rules and the map. The history and per-job detail behind them live in `000-docs/019-DR-REFF-blog-pipeline-reference.md`.

## What This Repo Is

Hugo static blog at **https://startaitools.com**: 430+ posts in `content/posts/`, plus monthly retrospectives, research, multi-chapter "features," citation corpora and ecosystem hub pages. Most of the code here is the automated blog pipeline (`scripts/blog/`) that writes, lands and syndicates one post a day from host cron.

Production is the Intent Solutions VPS behind Caddy. A push to `master` runs Release, which publishes a tag and calls Deploy. Netlify is retired (no config, not a rollback target).

Parent workspace: `/home/jeremy/000-projects/blog/CLAUDE.md`.

## Critical Rules

1. **Never edit `public/`** (generated) or anything inside `themes/archie/` (submodule; override in `layouts/`).
2. **Deploy branch is `master`.** There is no `main`.
3. **Always build with `--buildFuture`.** Without it, same-day posts with a later timestamp silently drop.
4. **Always set `slug`** in post front matter, matching the filename, or the URL drifts from the title.
5. **This checkout is the cron execution surface.** Host cron runs `scripts/blog/*.sh` straight from it. Keep it on `master`; do feature work on a branch built elsewhere (a worktree, or a commit built on `origin/master`). Nothing fast-forwards it on a schedule, so a merged script change does not take effect for cron until someone runs `git pull --ff-only` here. Merged is not deployed.
6. **`decisions.jsonl` and `feedback.jsonl` are append-only history.** Never rewrite or compact them. `index.db` is derived and gitignored.
7. **Skill instructions and skill data live in two places.** Instructions (`SKILL.md`, `references/`, `agents/` for `blog-backfill`, `blog-feedback`, `blog-calibrate`) are global at `~/.claude/skills/blog-*/`. Data and enforcement (`.claude/skills/blog-backfill/{methodology,scripts,references}/`) and all of `scripts/blog/` are tracked here. Edit instructions in the global copy, data and enforcement here. This box is the only one that runs the pipeline.
8. **Code decides, prose points.** Before changing any pipeline rule (dates, paths, tiers, gates, contracts, schedule), read `000-docs/014-AT-ADEC-blog-pipeline-authority-map.md`. Do not restate a rule the code owns; point at it.
9. **Finish by pushing.** Per `AGENTS.md`, work is not complete until `git push` and `bd dolt push` succeed.

## Task Tracking (Beads / bd)

`bd` is mandatory. Run `bd prime` for the full workflow.

```bash
bd ready                                # Find available work
bd show <id>                            # Read issue context
bd update <id> --claim                  # Claim work atomically
bd create "Title" -p 1 --description "Context" --acceptance "Done when..."
bd close <id> --reason "Done"
bd dolt pull && bd dolt push            # Sync issue history (start and end of session)
```

The embedded Dolt database is authoritative; `.beads/issues.jsonl` is an ignored passive export.

## Commands

```bash
hugo server -D                                          # Local server with drafts
hugo --buildFuture --gc --minify --cleanDestinationDir  # Build exactly as production does
hugo new posts/my-post.md                               # New post from archetypes/default.md
git submodule update --init --recursive                 # Only if themes/archie/ is empty after clone
python3 check-links.py                                  # HTTP-test every markdown URL (manual; not in CI)
```

Hugo is pinned to **0.150.0 extended** in CI and on the VPS. The pinned CI build is authoritative; a feature that needs a newer Hugo is not ready.

## Lint and Test

`scripts-lint.yml` is the CI gate; `lint-all.sh` runs the same checks locally.

```bash
scripts/blog/lint-all.sh                    # Everything CI runs: shellcheck, ruff, pipeline invariants, pytest
scripts/blog/lint-all.sh --check-drift      # Assert the script's file globs still match scripts-lint.yml

pytest tests/test_host_drift.py -q                                  # One test module
pytest tests/test_blog_pipeline.py -q -k "utm"                      # Tests matching a keyword
pytest "tests/test_host_drift.py::test_no_drift_when_host_matches" -q   # One test

bash scripts/blog/test-pipeline-invariants.sh                       # Bash invariants (idempotency, cross-post, packet)
python3 .claude/skills/blog-backfill/scripts/lint-post-voice.py content/posts/<slug>.md   # Voice lint on one post
python3 scripts/blog/host-drift-check.py                            # Host crontab + deployed reviewer agents vs the repo (read-only)
```

**The full pytest suite is heavy; prefer a single module.** One full run writes about 4.2 GiB of fixture repos and takes 15 to 22 minutes (measurements: runbook `000-docs/004`, "Capacity limits"). `tests/conftest.py` refuses to start when another session holds the suite lock, when `-n` asks for more than 2 xdist workers (`-n auto` is refused), or when free disk is below the suite peak plus the daily producer's admission line (`tests/suite_capacity.py`). A refusal is a capacity fact, not a flake; do not work around it.

On this box pytest and ruff are uv tools in `~/.local/bin`; the system Python has no pytest module, so use `pytest`, not `python3 -m pytest`. CI installs `pytest==9.1.1` and `ruff==0.16.9` with pip.

**Tests pin parts of this file.** After editing CLAUDE.md run these three: `tests/test_host_drift.py` (the schedule table below must match `scripts/blog/host/blog-cron.manifest` row for row), `tests/test_one_authority_per_concern.py` (the `-06:00` offset sentence and the tier-creep thresholds in the schedule row), and `tests/test_blog_role_manifest.py` (no per-tier reviewer list may appear in CLAUDE.md, AGENTS.md or README.md).

**CI shape:** `ruff` and the pytest suite run on `ubuntu-24.04`, pinned to match this host. A push to `master` that touches only `content/posts/*.md`, `static/images/posts/` and the two methodology JSONL files skips the pytest suite, so a daily post is not held before deploy; any other path runs it. The Hugo build, `tests/test_site_events.py` against the built HTML, and the two-day offline contract replay run on pull requests only. Voice lint runs on changed posts in pull requests.

## Release and Deploy

- `release.yml` runs on every push to `master`: `BREAKING CHANGE` bumps major, a `feat:` prefix bumps minor, anything else patch. It publishes master plus an annotated tag, verifies the GitHub Release, then calls `deploy.yml`. `version.txt` is the version's source of truth; `CHANGELOG.md` is written by the workflow.
- `deploy.yml` builds with Hugo 0.150.0 and deploys to `/srv/startaitools/dist` through the command-restricted VPS path, then smokes `https://startaitools.com/healthz`. The VPS always rebuilds from `origin/master`.
- **Rollback:** revert on `master` and let the next Release deploy it.
- Caddy owns the legacy redirects, the `/api/forms/*` proxy to forms-api, cache headers, `/healthz` and 404s. Source of truth: intent-os `ops/deploy/startaitools/Caddyfile.fragment`. Change redirects there, not here.
- The former RSS sync workflow was removed after it overwrote full posts with excerpts. Do not recreate it.

## Front Matter

Both TOML and YAML exist. **Prefer TOML** for new posts:

```toml
+++
title = 'Post Title'
slug = 'post-title'                      # REQUIRED, matches filename
date = 2026-04-16T08:00:00-06:00
draft = false
tags = ["ai", "deployment"]
categories = ["Technical Deep-Dive"]     # Must be from the allowed list
description = "SEO description"
tldr = "Summary text"                    # Renders a tl;dr box; the writer brief requires it
toc = true                               # Optional TOC sidebar
+++
```

**Allowed `categories`**: `Technical Deep-Dive`, `Development Journey`, `AI Engineering`, `DevOps`, `Architecture`, `Weekly Recap`, `Monthly Retrospective`.

**Dates:**
- New posts use the `-06:00` offset, all year. The automation host is fixed at UTC-06:00 with no daylight saving shift, `resolve_target_date` in `scripts/blog/lib-cron-common.sh` picks the target day on that clock, and the producer contract checks the front-matter date against it. `lint-post-voice.py` flags any other offset on a new post. Older posts with `-05:00` stay as published.
- Use morning timestamps and stagger a multi-post day by an hour.

## Architecture

```
content/
├── posts/                    # Flat, no subdirectories
├── monthly-recaps/           # One retrospective per month (no September 2026, see 000-docs/012)
├── features/                 # Curated multi-chapter long-reads; one directory per feature
├── citations/                # .bib + .jsonl corpora for the deep-dive series; noindex
├── mcp-for-beginners/        # Bundled third-party mini-repo with its own .github and translations. Avoid bulk edits
├── agentic-design-patterns/, tiny-recursive-models/   # Book-theme sections
├── research/                 # Standalone articles
└── *.md                      # about, contact, projects, research, deployment-thesis, irsb-ecosystem and wild-ecosystem hubs (not in the nav)

layouts/                      # Overrides of the archie theme. The site's whole look lives here, not in the theme
├── index.html, 404.html
├── _default/{single,list}.html
├── features/{single,list}.html
└── partials/                 # head (CSS/JS bundle, Umami tag), header, footer (subscribe form), schema (JSON-LD), social-meta, post-card, contact-cta, claude-partner-badge

assets/css/                   # tokens.css (design tokens), custom.css (layout), syntax.css (GENERATED by scripts/blog/gen-syntax-css.py)
assets/js/                    # main.js (forms fetch) + measure.js (Umami events), bundled by head.html
themes/archie/                # Submodule. themes/book/ is a manual copy. PaperMod and hugo-bearblog in .gitmodules are dead entries; do not check them out
config/_default/config.toml   # The only config file
drafts/                       # Manual WIP staging, outside content/, ignored by Hugo

scripts/blog/                 # The pipeline (see next section)
├── lib-cron-common.sh        # Shared cron plumbing: target date, locks, disk guard, liveness, atomic JSON, publish_file_to_repo
├── blog-backfill-daily.sh    # Daily wrapper: isolated workspace, producer launch, then the lander
├── blog-land.sh              # Deterministic lander: verify, commit, push, publish, or quarantine
├── blogpipe/                 # The gate set as one typed package: roles, contract, records, publication, evidence, writer
│                             #   blog-producer-contract.py and blog_publication_state.py are thin shims over it. Edit the package
├── writer-context/           # Versioned, hash-pinned writer brief
└── host/                     # blog-cron.manifest (the versioned schedule) + the two gate reviewer agents with SHA256SUMS

.claude/skills/blog-backfill/ # In-repo skill DATA and ENFORCEMENT (no SKILL.md here)
├── scripts/                  # lint-post-voice.py, apply-patterns.py, feedback-sweep.py, tier-creep-guard.py, post-to-*.sh, deny-lists
├── methodology/              # decisions.jsonl, feedback.jsonl, patterns.jsonl, calibration reports
└── references/               # seo-grounding.md

tests/                        # ~60 pytest modules; conftest.py + suite_capacity.py are the session preflight
000-docs/                     # Runbooks, incident reviews, decision records (NNN-CC-ABCD naming)
```

**Config facts worth knowing:** menu is Posts, Features, Recaps, Research, About, Contact. Goldmark runs with `unsafe = true`. Highlighting uses classes, not inline colours, so code colours come from the generated `syntax.css` per light and dark theme. Permalinks are `/posts/:slug/` and `/monthly-recaps/:slug/`.

**`list.html` is dual-mode.** If a section's `_index.md` has body content, the section renders as a single page; with front matter only it renders the article list. Adding body text to an `_index.md` flips the view. Hubs, research and book sections rely on this.

**Forms and measurement.** The footer subscribe form is POSTed by `assets/js/main.js` to `/api/forms/signup` and never navigates, so `/subscribe-success/` is not in the live flow. `*_click` events are attempts; `subscribe_accepted` and `contact_accepted` mean forms-api answered 2xx, not a confirmed subscriber. Event catalogue: `docs/analytics-events.md`.

**Design.** `DESIGN.md` and `docs/design-system.md` are the brand source of truth (charcoal and ember; Syne, Inter, Source Serif 4). Read them before changing `layouts/` or `assets/css/`.

## Content Pipeline

A **produce, land, illustrate, syndicate** chain, split so an LLM is never in the git-commit path.

1. **Produce.** The `/blog-backfill` skill writes the post, a `decisions.jsonl` record and a readiness sentinel in `.blog-staging/`, inside an isolated run workspace, and does no git. It stages each mandatory agent's result plus a hash-bound `roles.json` receipt; that receipt is what proves the required agents ran.
2. **Land.** `blog-land.sh` verifies the sentinel, the contract, the receipts, voice lint and a Hugo build. Only then does it commit and push, dual-publish to tonsofskills, and queue API cross-posts. On any failed precondition it **quarantines** the post and alerts. `.blog-quarantine/` is evidence; never auto-delete it.
3. **Illustrate.** After the push, `make-post-image.py` generates one image and commits it separately, falling back to the deterministic `make-social-card.py`. A vendor failure can never turn a good publish into a quarantine. `BLOG_IMAGE_GEN=0` disables generation.
4. **Syndicate.** `blog-posting-packet.sh` builds an HTML posting packet (three voices, UTM-tagged links, image URLs, approved disclaimers) and emails it to the social poster, who posts by hand. Dev.to and Hashnode are cross-posted by API from `.crosspost-queue.json`.

**Tiers.** 1 Field Note, 2 Technical Deep-Dive, 3 Case Study, 4 Distinguished Paper (manual, `/blog-research-article`). The only binding length rule is the lander's cap (`LAND_TIER1_MAX_LINES=145`, `LAND_TIER2_MAX_LINES=260` in `blog-land.sh`), which caps the shipped tier; `feedback-sweep.py` and `blogpipe/publication.py` mirror it under a parity test. Line counts in writer instructions are targets, not limits.

**Which agents must run and which must leave a PASS receipt:** one table only, "Mandatory roles" in the skill's `SKILL.md`, rendered from `python3 -B -m blogpipe required-roles`. Do not restate it here or anywhere else.

**Writer brief:** `scripts/blog/writer-context/writer-context-vN.md`, rendered by `python3 -B -m blogpipe writer-context render`. Released versions are hash-pinned, so an edit is a new version (`000-docs/015`).

**Two registers that must not converge.** The article is a work journal: what got built, what broke, what it cost, with no engineered hook and no call to action. Marketing voice applies only to syndication copy, generated after publish from the finished article. Marketing tone in an article is a defect. Third-party marketing skills may shape syndication mechanics, but their text never enters this repo; a CI test fails the build if it does.

**Syndication ledger, three facts never conflated** (`.blog-syndication-ledger.json`): `packet_sent` and `packet_status` mean the packet email was delivered and what it told the poster. `syndication.<surface>.status` is belief (`assumed_posted` is never rewritten to `posted`). `publication_evidence` is proof, written only from a post-shaped URL on the claimed platform (`blogpipe/evidence.py`).

**SEO phase.** BlogPosting JSON-LD comes from `layouts/partials/schema.html` on every dated page; the SEO phase may add FAQPage only, and touches title, description, schema, `tldr` and FAQ, never the body voice. The global `seo-*` agents are wrong for a Hugo site; ground them from `.claude/skills/blog-backfill/references/seo-grounding.md`, and skip the phase if that file is missing.

**Unattended runs use MiniMax.** `BLOG_PRODUCER=auto` runs the Claude toolchain on a static SOPS-held MiniMax key, because the `claude -p` OAuth sign-in expires and only an interactive session can renew it. Jobs that still call `claude -p` directly fail when that sign-in lapses.

## Autonomous Daily Automation

Host cron drives the pipeline. **The versioned schedule is `scripts/blog/host/blog-cron.manifest`**; `python3 scripts/blog/host-drift-check.py` compares it with `crontab -l`. This table must match the manifest (`tests/test_host_drift.py`). Change the crontab, the manifest and this table in the same reviewed change. What each job does in detail: `000-docs/019`, section 3.

| When (host UTC-06:00; no DST shift) | Script | What it does |
|---|---|---|
| 04:00 daily | `scripts/blog/blog-backfill-daily.sh` | Produces yesterday's post in an isolated workspace, then runs the lander. `--date YYYY-MM-DD` recovers one missed day through the same guards. |
| 05:00 daily | `scripts/blog/blog-posting-packet.sh --sweep` | Builds and emails the posting packet for each unsent post; marks delivery in the ledger, never publication. |
| 05:30 daily | `scripts/blog/blog-crosspost-sweep.sh` | Sends due Dev.to and Hashnode cross-posts from the queue. |
| 06:15 daily | `scripts/blog/native-metrics-devto.py` | Read-only Dev.to metrics collector; records an explicit status row rather than a silent zero. |
| 06:30 daily | `scripts/blog/web-analytics-daily.sh` | Emails the daily portfolio analytics brief. |
| 07:30 daily | `scripts/blog/blog-syndication-ingest.sh` | Reads authenticated receipt emails and URL pastes, appends `publication_evidence`, then runs the unverified-post dead-man check. |
| 07:00 weekly (Sunday) | `scripts/blog/next-topics-refresh.sh` | Ranks next topics from Umami performance and a trend scan into `.next-topics.jsonl`. |
| 10:00 weekly (Sunday) | `scripts/blog/blog-feedback-sweep.sh` | Deterministic rubric grader; publishes feedback rows by record-level merge. Exit 75 means deferred, retried next run. |
| 11:00 weekly (Sunday) | `scripts/blog/blog-tier-creep-guard.sh` | Tier-mix tripwire on the rolling 30 posts. It alerts at T2 > 40, T1 < 52, T3 > 12, T1 > 85 (percent; `BANDS` in `tier-creep-guard.py` is the authority), on breach onset or worsening, and again after `ESCALATE_RUNS` quiet runs if the breach persists. A second metric alerts when the pattern engine has applied nothing across recent posts while an active rule still matches history. |
| 12:00 weekly (Sunday) | `scripts/blog/blog-recommendation-worker.sh` | Drains one `auto-ok` bead onto a feature branch, runs `lint-all.sh`, and opens a PR only if it is green. Never merges. |
| 08:00 weekly (Monday) | `scripts/blog/blog-team-rollup.sh` | Weekly growth rollup email to the team; metric values render from verified references only. |
| 09:00 monthly (1st) | `scripts/blog/blog-monthly-calibrate.sh [YYYY-MM]` | Calibration report for the previous complete month, built and pushed from a detached worktree. |
| 09:30 monthly (1st) | `scripts/blog/blog-monthly-retro.sh` | Previous month's retrospective into `content/monthly-recaps/`, from a detached worktree. |

**Gate reviewer agents.** `blogpipe/roles.py` requires the global `fact-checker` and `article-consistency-checker` reviewers, which load from `~/.claude/agents/`. Their reviewed copies and hashes are in `scripts/blog/host/agents/`. `host-drift-check.py` reports a missing or differing deployed copy and never overwrites it.

**Logs:** `~/.local/state/<job-name>/` (for example `blog-backfill-daily/run-YYYY-MM-DD.log`). Alerts go to Buzz `sys-automation` and email. Mail config is `~/000-projects/blog/.env`.

**When a day is missed** there is no automatic catch-up. Run `scripts/blog/blog-backfill-daily.sh --date YYYY-MM-DD`, then `scripts/blog/blog-posting-packet.sh --sweep`. Invoking the skill directly is not equivalent: the wrapper supplies the lock, the isolated workspace and the run contract (runbook `000-docs/010`).

**Disk.** The producer and lander refuse below a 500 MiB floor. That floor is not a tunable: the fix for a refusal is capacity, never the number (runbook `000-docs/004`).

## Orientation

- `000-docs/014` authority map, `000-docs/019` pipeline reference, `000-docs/004` and `000-docs/010` recovery runbooks, `000-docs/013` metric dictionary.
- `000-docs/002-REF-omarchy-plugin-promotion-reference.md`: read before drafting anything about the Omarchy work.
- `GEMINI.md`, `RELEASES.md` and `SETUP_GITHUB.md` describe jeremylongshore.com, not this repo. Ignore them.
- `README.md` post count drifts; refresh it against `ls content/posts/*.md | wc -l` when you touch it.
- `check_links.sh` and `verify_links.sh` are narrow legacy checkers; `check-links.py` is the complete one. None runs in CI.
- Skills: `/blog-backfill`, `/blog-feedback`, `/blog-calibrate`, `/blog-research-article`.
