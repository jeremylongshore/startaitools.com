# CLAUDE.md

Guidance for Claude Code working in this repository. Read this file first every session before touching code or content.

## What This Repo Is

Hugo static blog at **https://startaitools.com** documenting AI development, data engineering, and DevOps. 220 posts in `content/posts/`, plus monthly retrospectives, research, and ecosystem hub pages. Auto-deploys to Netlify on push to `master` (watched branches: `main`, `master`, `clean-main` — master is the active deploy target).

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
├── posts/                    # 220 blog posts (flat, except posts/startai/ for synced RSS)
├── monthly-recaps/           # 6 retrospectives (Oct 2025 – Mar 2026) + _index.md stub
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
├── sync-startaitools.py      # RSS → content/posts/startai/ (downloads images locally)
└── sync-startaitools.sh      # Deprecated companion — describes sync to jeremylongshore.com
```

## Hugo Version Gap (Critical)

- **Netlify**: 0.150.0 (locked in `netlify.toml`)
- **Local**: 0.160.1-extended (snap) — 10 minor versions ahead

Test builds locally but expect Netlify to use older behavior. If a feature works locally and not in production, check Hugo release notes between 0.150 and 0.160.

## Critical Rules

1. **Never edit `public/`** — auto-generated by Hugo on every build.
2. **Never edit files inside `themes/archie/`** — it's a submodule. Override via `layouts/`.
3. **Never commit broken builds** — run `hugo --buildFuture --gc --minify --cleanDestinationDir` locally first.
4. **Always include `slug = 'filename'`** in post front matter. Hugo derives slug from title if omitted, producing URL drift.
5. **Always use `--buildFuture`** in build commands — without it, same-day posts with afternoon timestamps get silently excluded from the build.
6. **Deploy branch is `master`** (not `main`). `main` exists but master is the active target.
7. **Finish by pushing** — per `AGENTS.md`, work is not complete until `git push` succeeds and `git status` shows "up to date with origin".

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

- **`posts/`** — flat directory. Only subdirectory is `posts/startai/` (historical RSS-synced content).
- **`mcp-for-beginners/`** — a bundled mini-repo (~100+ files). Chapters `00-Introduction` through `11-MCPServerHandsOnLabs`, translations in 6 languages, own `.github/`, `.devcontainer/`. Be careful with bulk operations inside this directory.
- **`agentic-design-patterns/`, `tiny-recursive-models/`** — use the `book` theme via section `_index.md` with body content.
- **`research/`** — 3 standalone articles + `_index.md`. Not a book section.
- **`irsb-ecosystem.md`, `wild-ecosystem.md`** — top-level ecosystem hub pages (not in `posts/`). Both have `menu = 'main'` and `weight` for nav ordering. Deep-dive series posts live in `posts/` and link back to their hub.

## Content Pipeline (blog-backfill)

Daily posts are generated via the global `/blog-backfill` skill (lives in `~/.claude/skills/blog-backfill/`, not this repo). It auto-classifies each day's work:

| Tier | Name | Length | Quality Gate |
|------|------|--------|-------------|
| 1 | Field Note | 80–140 lines | Hugo build |
| 2 | Technical Deep-Dive | 150–250 lines | Hugo build + consistency audit |
| 3 | Case Study | 300–500 lines | Hugo build + consistency + fact-check |
| 4 | Distinguished Paper | 1200–1800 words | Manual via `/blog-research-article` |

All classification decisions land in `~/.claude/skills/blog-backfill/methodology/decisions.jsonl` (append-only — never edit). Monthly retrospectives go to `content/monthly-recaps/` (not `content/posts/`).

## Cross-Posting

`.crosspost-queue.json` (untracked) tracks syndication per post across dev.to, hashnode, medium, substack, and x. Each post has `publish_after` delays — typically +24h for dev.to/hashnode, +48h for medium — to let the canonical URL index first. Current queue is processed by `~/.claude/skills/blog-backfill/scripts/check-crosspost-queue.sh`.

`drafts/` is a manual staging area for WIP content. Hugo ignores it (not under `content/`). Currently holds `_index.md` + `software-supply-chain-security/` staging dir.

## Top-Level Doc Files (Orientation)

| File | Purpose |
|------|---------|
| `README.md` | Public-facing pitch. Claims "37+ posts" — **outdated** (real count: 220). |
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

## Related Global Skills

Skills that operate on this repo (all live in `~/.claude/skills/`, not here):
- `/blog-backfill` — daily post generation with tier classification
- `/blog-calibrate` — monthly calibration report from decisions.jsonl
- `/blog-feedback` — post-publication tier assessment
- `/blog-research-article` — Tier 4 interactive workflow
- `/content-nuke` — multi-platform publishing (StartAI + JeremyLongshore + X + LinkedIn)
- `/blog-single-startai`, `/blog-startaitools` — single-post workflows

## Gotchas Summary

- Build must use `--buildFuture` or same-day posts silently drop.
- Local Hugo is 0.160.1; Netlify locks 0.150.0.
- `list.html` flips between content-page and article-list modes based on `_index.md` body content.
- `sync-startaitools.yml` workflow exists but is disabled.
- Three misplaced top-level docs (GEMINI/RELEASES/SETUP_GITHUB) describe a different project.
- README post count is stale (37+ vs actual 220).
- Front matter must include explicit `slug` to avoid URL drift.
- `master`, not `main`, is the deploy target.
