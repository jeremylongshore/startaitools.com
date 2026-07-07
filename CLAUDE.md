# CLAUDE.md

Guidance for Claude Code working in this repository. Read this file first every session before touching code or content.

## What This Repo Is

Hugo static blog at **https://startaitools.com** documenting AI development, data engineering, and DevOps. ~291 posts in `content/posts/`, plus monthly retrospectives, research, curated multi-chapter "features," citation corpora, and ecosystem hub pages. Auto-deploys to Netlify on push to `master` (watched branches: `main`, `master`, `clean-main` — master is the active deploy target).

Parent repo context: `/home/jeremy/000-projects/blog/CLAUDE.md` (multi-blog workspace alongside `jeremylongshore/`).

## Task Tracking (Beads / bd)

`bd` is mandatory for this repo. `AGENTS.md` enforces a "Landing the Plane" workflow — work is not complete until `git push` succeeds.

```bash
bd ready                                # Find available work
bd update <id> --status in_progress     # Claim work
bd create "Title" -p 1 --description "Context"
bd close <id> --reason "Done"
bd sync                                 # Sync with git (end of session)
```

After upgrading bd: `bd info --whats-new`, then `bd hooks install` if warned.

## Commands

```bash
# Development
hugo server -D                                          # Local server with drafts
hugo server                                             # Production preview

# Build (matches Netlify exactly)
hugo --buildFuture --gc --minify --cleanDestinationDir

# New content
hugo new posts/my-post.md                               # Uses archetypes/default.md

# Theme setup (only if themes/archie/ is empty after clone)
git submodule update --init --recursive

# Link validation (manual, not in CI)
./verify_links.sh                                       # Post-build filesystem check
./check_links.sh                                        # Research page internal links
python3 check-links.py                                  # Concurrent HTTP test of all markdown URLs
```

## Git Branching and Deploy

- **Deploy branch**: `master` (Netlify watches `main`, `master`, `clean-main` — master is primary)
- `.github/workflows/release.yml` auto-tags semver on push to any of those three branches: detects `BREAKING CHANGE` → major, `feat:` prefix → minor, else patch. Writes `version.txt`, `CHANGELOG.md`, creates git tag + GitHub Release. `version.txt` is the source of truth for the version.
- `.github/workflows/sync-startaitools.yml` is **DISABLED** (cron commented out, `workflow_dispatch` only). The schedule previously overwrote comprehensive posts with RSS excerpts. Do not re-enable without a fix.

## Front Matter

Both TOML and YAML exist. **Prefer TOML** for new posts:

```toml
+++
title = 'Post Title'
slug = 'post-title'                      # REQUIRED — matches filename, prevents URL mismatches
date = 2026-04-16T08:00:00-05:00
draft = false
tags = ["ai", "deployment"]
categories = ["Technical Deep-Dive"]     # Must be from allowed list (see below)
description = "SEO description"
+++
```

Legacy posts use YAML (`---`). Both work.

**Allowed `categories`**: `Technical Deep-Dive`, `Development Journey`, `AI Engineering`, `DevOps`, `Architecture`, `Weekly Recap`, `Monthly Retrospective`.

**Date/time rules:**
- Use morning timestamps (e.g., `T08:00:00`) for same-day posts. Hugo excludes pages dated after build time unless `--buildFuture` is set. `--buildFuture` is in netlify.toml but not in local Hugo defaults.
- Stagger multi-post series by 1 hour (e.g., `T08:00:00`, `T09:00:00`, `T10:00:00`).
- Timezones: `-05:00` (CDT, summer) or `-06:00` (CST, winter). Repo TZ is `America/Chicago`.

**Optional front-matter params** (rendered by `layouts/_default/single.html`):
- `toc = true` — renders a TOC sidebar (float on desktop, stacks above body on mobile)
- `tldr = "Summary text"` — renders a tl;dr box above the body

## Architecture

```
content/
├── posts/                    # ~291 blog posts (flat — no subdirectories)
├── monthly-recaps/           # 10 retrospectives (Oct 2025 – Jun 2026) + _index.md stub
├── features/                 # Curated multi-chapter long-reads (books/series); _index.md + one dir per feature
├── citations/                # Shared citation corpora (.bib + .jsonl) for the deep-dive series; noindex; _index.md
├── agentic-design-patterns/  # Book-theme section (_index.md)
├── mcp-for-beginners/        # Bundled repo — ~100+ files, solutions in Python/TS/Java/Rust/C#/.NET, 6-language translations, its own .github + .devcontainer
├── research/                 # 3 standalone articles + _index.md
├── tiny-recursive-models/    # Book-theme section
├── _index.md                 # Homepage content
├── about.md, contact.md
├── projects.md, research.md
├── subscribe-success.md      # Netlify form confirmation page
├── irsb-ecosystem.md         # Ecosystem hub (menu = 'main', weight = 16)
└── wild-ecosystem.md         # Ecosystem hub (menu = 'main', weight = 15)

themes/
├── archie/                   # Primary theme — Git submodule (github.com/athul/archie)
└── book/                     # Docs sections — manually added, NOT a submodule

layouts/                      # Four theme overrides
├── index.html                # Homepage — minimal, delegates to theme partials
├── partials/footer.html      # Netlify subscribe form + RSS link + social icons + GA
└── _default/
    ├── single.html           # Post template, supports toc + tldr params
    └── list.html             # Dual-mode (see Layout Behavior below)

assets/css/custom.css         # Hugo asset pipeline — mobile grids, TOC stacking, table scroll, code word-break, header # removal
static/_redirects             # 6 Netlify redirect rules (legacy /en/blogs/*, /blogs/*, /projects/*, /skills, /resume, /startai/*)
static/images/                # Favicon, OG image, share image
archetypes/default.md         # TOML template used by `hugo new`

config/_default/config.toml   # Single config file (no environment splits)
netlify.toml                  # Build command, Hugo 0.150.0, TZ, aggressive no-cache headers
version.txt                   # Source of truth for semver (currently 0.12.0)

drafts/                       # WIP staging — NOT tracked by Hugo, manual pre-publish area
.crosspost-queue.json         # Syndication tracker: dev.to, hashnode, medium, substack, x

.github/workflows/
├── release.yml               # Auto semver on push to main/master/clean-main + manual dispatch
└── sync-startaitools.yml     # DISABLED (RSS sync overwrote posts; manual dispatch only)

scripts/
└── blog/                     # Cron-side glue for the in-repo blog pipeline (moved here 2026-05-16)
    ├── lib-cron-common.sh            # shared helpers: preflight, default_branch_of, post_exists_for_date, disk_guard, remote_live_check, validate_json/atomic_json_write, reconcile_repo, acquire_pipeline_lock, slack_fail
    ├── blog-backfill-daily.sh        # 7am — headless /blog-backfill (produces), then blog-land.sh (lands)
    ├── blog-land.sh                  # DETERMINISTIC land step: verify preconditions → commit/push/publish/queue, else QUARANTINE (WS1)
    ├── blog-posting-packet.sh        # 8:30am --sweep — builds + emails the Ezekiel posting packet (WS2)
    ├── blog-packet-html.cjs          # v3 HTML renderer for the packet
    ├── blog-team-rollup.sh           # Mon 8am — weekly team growth rollup (WS2b)
    ├── web-analytics-daily.sh        # 6:30am — daily portfolio analytics email to Jeremy (WS0)
    ├── blog-feedback-sweep.sh        # Sun 10am — deterministic rubric grader (no LLM)
    ├── blog-monthly-calibrate.sh     # 1st 9am — monthly /blog-calibrate report
    ├── blog-monthly-retro.sh         # 1st 9:30am — monthly retrospective post
    └── blog-tier-creep-guard.sh      # Sun 11am — deterministic tier-distribution tripwire (alerts only on breach)

.claude/skills/                # Project-scoped Claude Code skills (load only when working in this repo)
├── blog-backfill/             # Daily post generation + tier classification + crosspost queue
│   ├── SKILL.md
│   ├── agents/                # blog-classifier, blog-consistency-checker, blog-fact-checker
│   ├── references/            # classify-day, content-tier-classification, polish-seo, etc.
│   ├── scripts/               # feedback-sweep.py, tier-creep-guard.py, rebuild-methodology-index.sh, post-to-*.sh
│   └── methodology/           # decisions.jsonl, feedback.jsonl, calibration-YYYY-MM.md (tracked)
├── blog-feedback/             # Post-publication tier assessment (interactive + --auto-sweep)
└── blog-calibrate/            # Monthly tier-distribution + Brier-score report
```

## Hugo Version Gap (Critical)

- **Netlify**: 0.150.0 (locked in `netlify.toml`)
- **Local**: 0.163.3-extended (snap) — 13 minor versions ahead

Test builds locally but expect Netlify to use older behavior. If a feature works locally and not in production, check Hugo release notes between 0.150 and the local version.

## Critical Rules

1. **Never edit `public/`** — auto-generated by Hugo on every build.
2. **Never edit files inside `themes/archie/`** — it's a submodule. Override via `layouts/`.
3. **Never commit broken builds** — run `hugo --buildFuture --gc --minify --cleanDestinationDir` locally first.
4. **Always include `slug = 'filename'`** in post front matter. Hugo derives slug from title if omitted, producing URL drift.
5. **Always use `--buildFuture`** in build commands — without it, same-day posts with afternoon timestamps get silently excluded from the build.
6. **Deploy branch is `master`** (not `main`). `main` exists but master is the active target.
7. **Finish by pushing** — per `AGENTS.md`, work is not complete until `git push` succeeds and `git status` shows "up to date with origin".
8. **Never break the in-repo blog pipeline.** `.claude/skills/blog-*/` and `scripts/blog/*.sh` are tracked, executable, and wired into cron. Edits to `decisions.jsonl` are append-only (never modify existing records). Path references inside scripts use either `${CLAUDE_SKILL_DIR}` or repo-relative resolution (`SCRIPT_DIR = Path(__file__).resolve().parent`) — do not introduce `~/.claude/skills/blog-*` paths anywhere; they will break on fresh clones.
9. **decisions.jsonl + feedback.jsonl are append-only, version-controlled history.** Every classification + grading decision is a git diff. Do not rewrite or compact them. `index.db` is derived (gitignored) and regenerated by `scripts/rebuild-methodology-index.sh`.

## Netlify Build Details

From `netlify.toml`:
- `HUGO_VERSION = "0.150.0"`, `NODE_VERSION = "18"`, `TZ = "America/Chicago"`, `HUGO_ENABLEGITINFO = "true"`, `HUGO_ENV = "production"`
- Build command: `git submodule update --init --recursive && hugo --buildFuture --gc --minify --cleanDestinationDir`
- HTML served with aggressive no-cache headers (`Cache-Control: public, max-age=0, must-revalidate`) for `/*.html`, `/posts/*`, `/about/*`, `/projects/*`, `/research/*`. Plus `no-cache, no-store` for `/index.html`.
- HTTP → HTTPS force redirect (301).

## Config Summary

`config/_default/config.toml`:
- Theme: `archie`
- Menu (7 items by weight): Home (5), Posts (10), Monthly Recaps (15), About (20), Research & Curriculum (25), Projects (27), Contact (30)
- Goldmark renderer with `unsafe = true` (embedded HTML allowed)
- Highlight style: `friendly`, code fences enabled, line numbers off
- Permalinks: `blog = "/:slug/"`, `posts = "/posts/:slug/"`, `monthly-recaps = "/monthly-recaps/:slug/"`
- `params.customCSS = ["css/custom.css"]` — resolved via Hugo asset pipeline from `assets/css/custom.css`

## Layout Behavior Notes

`layouts/_default/list.html` has **dual behavior**: if a section's `_index.md` contains body content (not just front matter), the list template renders it as a single content page. If `_index.md` has only front matter, it renders the default article list. Adding body content to an `_index.md` therefore flips the section from a list view to a single-page view. This is how ecosystem hubs, research, and book sections work.

`layouts/partials/footer.html` contains a Netlify-powered subscribe form (`data-netlify="true"`, honeypot bot-field). The form POSTs to `/subscribe-success/`, which is a real content page (`content/subscribe-success.md`).

## Content Sections

- **`posts/`** — flat directory, no subdirectories. (The historical `posts/startai/` RSS-sync directory is gone; the `sync-startaitools.yml` workflow that fed it is disabled.)
- **`features/`** — curated multi-chapter long-reads (books/series). `_index.md` renders a landing page; each feature is its own subdirectory of ordered chapters. Slower cadence than `posts/`, denser per page.
- **`citations/`** — shared citation corpora (`.bib` + `.jsonl`) that the deep-dive series draws from. `noindex`; every source verified against Semantic Scholar (match ≥0.70) or a canonical DOI/URL. One corpus per ecosystem (wild, irsb).
- **`mcp-for-beginners/`** — a bundled mini-repo (~100+ files). Chapters `00-Introduction` through `11-MCPServerHandsOnLabs`, translations in 6 languages, own `.github/`, `.devcontainer/`. Be careful with bulk operations inside this directory.
- **`agentic-design-patterns/`, `tiny-recursive-models/`** — use the `book` theme via section `_index.md` with body content.
- **`research/`** — 3 standalone articles + `_index.md`. Not a book section.
- **`irsb-ecosystem.md`, `wild-ecosystem.md`** — top-level ecosystem hub pages (not in `posts/`). Both have `menu = 'main'` and `weight` for nav ordering. Deep-dive series posts live in `posts/` and link back to their hub; their sourcing lives in `citations/`.

## Content Pipeline (blog-backfill)

**End-to-end architecture (the big picture — inverted 2026-07-05).** The pipeline is a **produce → land → syndicate** chain, split so an LLM is never in the git-commit path:

1. **PRODUCE** — the `/blog-backfill` skill (LLM) writes the post + a `decisions.jsonl` record + a readiness sentinel (`.blog-staging/DATE.intent.json`) and does **no git**. It attests `ready:true` only if every quality gate passed.
2. **LAND** — `scripts/blog/blog-land.sh` (pure bash, deterministic) verifies preconditions — sentinel `ready:true` + classifier record + step-8 audit addendum + `hugo` build — and only then commits/pushes to startaitools.com, dual-publishes to tonsofskills, and queues API cross-posts. If any precondition fails it **quarantines** the post (moves it aside, restores a clean tree) and alerts — it never publishes something half-baked. This is why a timeout/blocked-gate can no longer brick the next day's run. Dual-publish/field-notes push via `lib-cron-common.sh:publish_file_to_repo` (git plumbing, working-tree-free, retry-on-race — see its header for why).
3. **SYNDICATE** — `scripts/blog/blog-posting-packet.sh` builds the per-post HTML "posting packet" (three voices, UTM links, approved disclaimers) and emails it to Ezekiel, who posts manually. State lives in `.blog-syndication-ledger.json`.

Shared cron plumbing lives in `scripts/blog/lib-cron-common.sh` (preflight, `default_branch_of`, `post_exists_for_date`, disk/lock/liveness/atomic-json guards, `publish_file_to_repo`). All wrappers are fail-loud (ntfy + email) and idempotent. Full cron schedule + who-does-what: § "Autonomous Daily Automation" below.

Daily posts are generated via the **project-scoped** `/blog-backfill` skill (lives in `.claude/skills/blog-backfill/` inside this repo, **not** in `~/.claude/skills/`). Same for `/blog-feedback` and `/blog-calibrate`. Moved in-repo 2026-05-16 so enforcement travels with the code — fresh clone reproduces the entire pipeline. It auto-classifies each day's work:

| Tier | Name | Length | Quality Gate |
|------|------|--------|-------------|
| 1 | Field Note | 80–140 lines | Hugo build |
| 2 | Technical Deep-Dive | 150–250 lines | Hugo build + consistency audit |
| 3 | Case Study | 300–500 lines | Hugo build + consistency + fact-check |
| 4 | Distinguished Paper | 1200–1800 words | Manual via `/blog-research-article` |

All classification decisions land in `.claude/skills/blog-backfill/methodology/decisions.jsonl` (append-only — never edit). Tier feedback at `.claude/skills/blog-backfill/methodology/feedback.jsonl`. Calibration reports at `.claude/skills/blog-backfill/methodology/calibration-YYYY-MM.md`. Monthly retrospectives go to `content/monthly-recaps/` (not `content/posts/`).

## Cross-Posting + Syndication (WS2/WS3, 2026-07-05)

Two separate lifecycles, two files (both gitignored):

- **`.crosspost-queue.json`** — the **API cross-post** work queue (Dev.to + Hashnode only; Medium retired to manual). Appended + processed by `blog-land.sh` after each verified publish (Tier ≥ 2 only), with atomic write + jq validation. Entry schema in `references/crosspost-queue.md`. The old `substack_emailed`/`x_thread_emailed` booleans are gone.
- **`.blog-syndication-ledger.json`** — the per-post **did-he-post record** (`syndication` sub-object: x / li_personal / li_company / substack / medium + `packet_sent`). Written by `blog-land.sh`; read/updated by the posting packet + weekly rollup.

**Social posting is handed to Ezekiel** (`ezekiel@intentsolutions.io`). `blog-posting-packet.sh --sweep` (8:30 AM) builds an HTML "posting packet" per unsent post — three independently-voiced pieces (X raw / LinkedIn personal / LinkedIn company), UTM-tagged links (`utm_source=x|linkedin|substack|medium`), a "loud" canonical card for Substack/Medium, and any **Jeremy-approved** disclaimer (from `references/disclaimer-library.json`; fail-closed HOLD if a governed entity has no approved string). Voice copy is generated by a bounded `claude -p` (the ONE LLM touch on the syndication path, always AFTER publish); bash appends the links deterministically (UTM is the measurement keystone). Ezekiel's onboarding + daily SOP: `references/ezekiel/`.

The API scripts `post-to-medium.sh`/`post-to-substack.sh` and the disabled `sync-startaitools.{yml,py,sh}` were removed 2026-07-05 (Medium + Substack are now manual via the packet).

`drafts/` is a manual staging area for WIP content. Hugo ignores it (not under `content/`). Holds `_index.md` and one subdirectory per WIP article — contents churn, don't treat any specific draft as canonical.

## Autonomous Daily Automation

Local cron jobs (user crontab — `crontab -l` to inspect) drive the entire content pipeline without human intervention. **All run on this machine via headless `claude -p`** — they require local file access (skill files, decisions.jsonl, project repos), so they cannot be migrated to remote routines.

| When (America/Chicago) | Script | What it does |
|---|---|---|
| 06:30 daily | `scripts/blog/web-analytics-daily.sh` | Headless `/web-analytics medium --email` — portfolio brief (startaitools, tonsofskills, jeremylongshore, intentsolutions) emailed to Jeremy each morning. Fail-loud on error. Tier tunable via `WEB_ANALYTICS_TIER`. (Added 2026-07-05, WS0.) |
| 07:00 daily | `scripts/blog/blog-backfill-daily.sh` | Headless `claude -p "/blog-backfill"` for yesterday — the skill PRODUCES the post + decisions + a readiness sentinel (**no git**). The wrapper then runs `scripts/blog/blog-land.sh`, which deterministically verifies preconditions (sentinel `ready:true` + classifier record + audit addendum + hugo build) and only then commits/pushes/dual-publishes/queues — else **quarantines** the half-baked post so tomorrow is unblocked. `flock`-serialized against hand-runs; disk-guarded; remote-liveness gated. Idempotent. Emails summary. (Inverted 2026-07-05, WS1.) |
| 08:30 daily | `scripts/blog/blog-posting-packet.sh --sweep` | Builds the per-post **Ezekiel posting packet** (v3 HTML: X raw + LinkedIn personal + LinkedIn company + Substack/Medium for Tier 2+), UTM-tags every syndicated link, selects any approved disclaimer (fail-closed HOLD if none), emails it TO Ezekiel (CC Jeremy), marks `packet_sent` in the ledger. Merges a multi-post day into one email. Heartbeat "NO PACKET TODAY" if nothing. Replaced `blog-social-email.sh`. (Added 2026-07-05, WS2.) |
| 08:00 Monday | `scripts/blog/blog-team-rollup.sh` | Weekly growth rollup to the whole team (`TEAM_EMAILS` in `intent-mail/.env`) — portfolio analytics + syndication UTM breakdown + an evergreen re-share nomination + "amplify these" asks. Replaces the daily 5-CC firehose. (Added 2026-07-05, WS2b.) |
| 09:00 monthly (1st) | `scripts/blog/blog-monthly-calibrate.sh` | Headless `claude -p "/blog-calibrate"` — analyzes the past month's decisions.jsonl for tier creep, emails the report. |
| 09:30 monthly (1st) | `scripts/blog/blog-monthly-retro.sh` | Headless `claude -p "/blog-backfill monthly"` — generates the previous month's retrospective at `content/monthly-recaps/<month>-<year>.md`, commits, pushes, emails summary. Idempotent. |
| 10:00 weekly (Sunday) | `scripts/blog/blog-feedback-sweep.sh` | Deterministic structural rubric grader. Walks every classifier record without a feedback entry and writes auto-confirms to `feedback.jsonl`. No LLM. Emails digest of mismatches. Added 2026-05-16. |
| 11:00 weekly (Sunday) | `scripts/blog/blog-tier-creep-guard.sh` | Deterministic tier-distribution tripwire (`tier-creep-guard.py`, no LLM). Checks the rolling-30 tier mix against tolerance bands (T1 60-70 / T2 25-35 / T3 5-10) for Tier-2/3 inflation OR Tier-1 over-deflation. **Hysteresis:** alerts (ntfy high + email) only on breach **onset or worsening** (new band, or a metric past its high-water by ≥5pts); a persistent breach is suppressed (not a weekly nag); a one-time low-priority all-clear on recovery. Reads `decisions.jsonl`; writes only its hysteresis state to `~/.local/state/blog-tier-creep-guard/state.json` (outside the repo — never dirties the tree). Manual check: `tier-creep-guard.py --stateless`. Added 2026-07-03, hysteresis 2026-07-05. |
| 03:25 weekly (Sunday) | `/etc/cron.weekly/disk-cleanup` | Trims Docker, snap revisions, journal logs when `/` is over 70%. Unrelated to blog. |

**Email destination:** `jeremy@intentsolutions.io` (set in `~/000-projects/blog/.env` as `TO_EMAILS`). Sent via local Gmail SMTP through `~/.claude/skills/email/scripts/send-email.cjs` — NOT the claude.ai Gmail MCP connector.

**Logs:** `~/.local/state/blog-backfill-daily/`, `~/.local/state/blog-land/`, `~/.local/state/blog-posting-packet/`, `~/.local/state/blog-team-rollup/`, `~/.local/state/web-analytics-daily/`, `~/.local/state/blog-monthly-calibrate/`, `~/.local/state/blog-monthly-retro/`.

**Failure modes:** if cron's `claude -p` exits non-zero, the summary email reports `FAILED (exit N)` with the last 50 log lines + an ntfy push at `Priority: high`. If a day is missed (machine off, etc.), the gap stays open until manually backfilled — no auto-catchup. The April 2026 monthly retro was missed because the local monthly-retro cron didn't exist yet; this is fixed.

**Safe to run `/blog-backfill` manually** alongside the cron. The skill checks `content/posts/` for existing dates before generating, so manual + autonomous never collide. Same for `/blog-backfill monthly` — checks for the target retro file before writing.

## Top-Level Doc Files (Orientation)

| File | Purpose |
|------|---------|
| `README.md` | Public-facing pitch. Claims "37+ posts" — **outdated** (real count: ~291). |
| `AGENTS.md` | Beads workflow + mandatory "Landing the Plane" push discipline. |
| `CONTRIBUTING.md` | Guest post policy, bug-report format, style guidelines. |
| `CHANGELOG.md` | Release notes with commit hashes. Updated by `release.yml`. |
| `LICENSE` | MIT (2024 Jeremy Longshore). |
| `version.txt` | Source-of-truth semver (`0.12.0`). |
| `GEMINI.md`, `RELEASES.md`, `SETUP_GITHUB.md` | **Misplaced** — describe jeremylongshore.com, not this repo. Likely template-copy artifacts. Do not treat as authoritative for startaitools. |

## Submodule Reality vs. `.gitmodules`

`.gitmodules` declares three submodules: `archie`, `PaperMod`, `hugo-bearblog`. On disk only `archie/` is active. `book/` is present but manually added, not in `.gitmodules`. `PaperMod` and `hugo-bearblog` are stale legacy entries from theme evaluation — safe to leave but do not check them out.

## Link Checkers (All Stale, None in CI)

Three different tools exist. None are wired into CI; all are manual-run and partially redundant.

- `check-links.py` — concurrent HTTP tester for all markdown URLs. Most complete.
- `check_links.sh` — shell wrapper, checks internal links on `/research/` only.
- `verify_links.sh` — post-build filesystem check for 6 hardcoded paths in `public/`.

Prefer `check-links.py` if you need comprehensive validation.

## Related Skills

**In-repo (project-scoped, lives in `.claude/skills/`)** — load only when working in this repo:
- `/blog-backfill` — daily post generation with tier classification
- `/blog-calibrate` — monthly calibration report from decisions.jsonl + feedback.jsonl
- `/blog-feedback` — post-publication tier assessment (interactive + `--auto-sweep` mode)

**Still global (live in `~/.claude/skills/`)** — separate workflows not blog-pipeline-specific:
- `/blog-research-article` — Tier 4 interactive workflow
- `/content-nuke` — multi-platform publishing (StartAI + JeremyLongshore + X + LinkedIn)
- `/blog-single-startai`, `/blog-startaitools` — single-post workflows

## Gotchas Summary

- Build must use `--buildFuture` or same-day posts silently drop.
- Local Hugo is 0.163.3; Netlify locks 0.150.0.
- `list.html` flips between content-page and article-list modes based on `_index.md` body content.
- `sync-startaitools.yml` workflow exists but is disabled (its `posts/startai/` target directory is also gone).
- Three misplaced top-level docs (GEMINI/RELEASES/SETUP_GITHUB) describe a different project.
- README post count is stale (37+ vs actual ~291).
- Front matter must include explicit `slug` to avoid URL drift.
- `master`, not `main`, is the deploy target.
- Blog pipeline skills are **project-scoped** at `.claude/skills/` — `/blog-backfill`, `/blog-feedback`, `/blog-calibrate` only resolve when working inside this repo. Cron scripts live at `scripts/blog/`.
- `decisions.jsonl` + `feedback.jsonl` are tracked, append-only. Daily cron writes one line per post; weekly sweep writes feedback entries. Both produce visible git diffs.
- Classifier rubric has hard anchor enforcement (TCH≥4 needs named artifact; SCP≥3 needs multi-system) and a Step-0 distribution check that reads past 14 days before scoring. Calibration examples at `.claude/skills/blog-backfill/references/content-tier-classification.md`.


<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:7510c1e2 -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data` on your git remote; `.beads/issues.jsonl` is a passive export. See https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md for details and anti-patterns.

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->
