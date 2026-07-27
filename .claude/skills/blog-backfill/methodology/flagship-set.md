# Curated Flagship Set

**Scope:** the short list of public repos that Jeremy references as evidence of the operational + OSS track record. Source of truth for both `startaitools.com` posts and `jeremylongshore.com` flagship sections.

**Bead:** startaitools-12a

**Last refreshed:** 2026-07-27 (this file is rebuilt whenever a new addition or removal of a flagship makes the prior statement out of date).

---

## The set, ranked by stars (as of 2026-07-27)

| Tier | Repo | Stars | Forks | Notes |
|---|---|---|---|---|
| **anchor** | `jeremylongshore/claude-code-plugins-plus-skills` | 2,558 | 368 | Indexes 425+ plugins, 2,810 skills, 200+ agents. Powers [tonsofskills.com](https://tonsofskills.com). Monorepo at `private: true`; only `@intentsolutionsio/ccpi` is on npm. Used as the canonical star-count + OSS-tier reference across all startaitools.com + jeremylongshore.com copy. |
| **support** | `jeremylongshore/Hybrid-ai-stack-intent-solutions` | 5 | 1 | Production AI orchestration doc — routing between local CPU models and cloud APIs. The reference implementation behind the "60-80% cost reduction" claim in `startaitools.com/research/`. |
| **support** | `intent-solutions-io/iam-git-with-intent` | (data stale; needs re-pull — last verified <5) | — | CLI for intent-driven git commits. Lower traction; included for completeness because the startaitools.com beat mentioned it. |
| **support** | `jeremylongshore/intent-agent-model-jvp-base` | 2 | 0 | Reference agent-model integration. Early-stage proof-of-concept; included so the reasoning in the startaitools.com beat has a code-anchor. |

## What got cut from the curatorial shortlist (and why)

The `jeremylongshore.com/data/projects.yml` file lists 25+ repositories across `intent_solutions_repos`, `personal_repos`, `products`, and `client_projects` categories. **Most of them have 0 GitHub stars as of 2026-07-27.** They are real, working repos (verified via grep on the GH API), but they don't meet the "flagship" bar (non-trivial public adoption).

Specifically excluded from this flagship set:

- `intent-solutions-io/intent-mail` (0 stars) — internal email platform at `/home/jeremy/000-projects/intent-mail/`. Private infra; track via Internal Resources instead.
- `intent-solutions-io/intent-catalog` (0 stars) — same: internal tooling.
- `intent-solutions-io/DiagnosticPro` (0 stars) — founder-arc back-reference; the OSS scoring is the SaaS scoring post-mortem, not the repo.
- `intent-solutions-io/executive-intent` (0 stars) — demo deployment; not a flagship.
- `jeremylongshore/iam-bob-adk`, `jeremylongshore/irsb`, `jeremylongshore/pipelinepilot`, `jeremylongshore/wild-rails-safe-introspection-mcp`, etc. (each with 0-2 stars) — all real, all working, all cited in specific startaitools.com beats; "support" or "reference" tier only, not flagship.

Excluded-by-default does **not** mean these repos aren't interesting — it just means they haven't earned the public-adoption bar yet. They live in the long-tail `.claude/skills/blog-backfill/` references or `data/projects.yml`; that's enough for the blog pipeline to cite them, but they don't show up in the "flagship" framing on landing surfaces.

## What "flagship" actually means here

A flagship repo is one where:

1. **Public adoption signal exists** (>= 5 GitHub stars, OR >= 3 external contributors, OR external blog post / news mention, OR explicit third-party link). The anchor repo clears 2,500+ stars; the support tier clears the 5-star / fork bar; everything else is "long-tail."
2. **Source code is public, MIT or compatible license**. (All 4 listed above are MIT-licensed.) The intent-solutions-io org repos that aren't MIT-licensed (private infra) are not eligible.
3. **Used in published startaitools.com content or jeremylongshore.com profiles.** Pure-internal repos without external references don't belong on a flagship list.

This rules out a lot of repos. The flagship set is intentionally small so the on-site copy ("X real GitHub stars on Y") doesn't have to dilute across many second- and third-tier items.

---

## Cross-references

- `startaitools.com/about/` references the anchor's star count (verified 2026-07-27: 2,558 stars, 368 forks, 14 open issues). The "2,500+ GitHub stars" claim in about.md is now date-pinned and verify-linked.
- `startaitools.com/content/posts/` sometimes cites the support-tier repos as "reference implementations." When cited, each post must cite a live URL (e.g., `github.com/jeremylongshore/Hybrid-ai-stack-intent-solutions`) so the citation can be re-verified when stars move.
- `jeremylongshore.com/config.yml` line 77 footer: "Claude Code Plugins creator (X stars)" — X is now read live from `github_stars['jeremylongshore/claude-code-plugins-plus-skills']` via the `GithubRepoStarsCountPlugin` (per PR #20 — bead `startaitools-9ve`).
- `intent-os/persona/master.md` line 81 — canonical claim format still uses "2,500+ GitHub stars, 360+ forks, 45,000+ npm downloads" (the npm number is unverified; see publishing-gates.md rule 5). The persona-level drift on the npm claim is a separate bead.

## Maintenance protocol

- Whenever Jeremy publishes a Tier 1+ post that adds a new flagship citation, append a row to the flagship table (with the live-star-as-of-date).
- Whenever a flagship loses ≥ 20% of its stars (a wave of "star-unstarring" events) OR the repo is archived/moved, update this doc and file a bead for the on-site copy.
- The refresh cadence is **monthly** OR **on-PR-merge** (whichever fires first). See `next-topics.py` for the cron-driven candidate scanner that flags drift items.
