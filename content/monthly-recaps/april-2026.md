+++
title = 'April 2026: Tier 3 Finds Its Footing — Eight Case Studies, the Audit Harness Ships, and the Schema Postmortem'
slug = 'april-2026'
date = 2026-04-30T18:00:00-05:00
draft = false
tags = ["monthly-retro", "metrics", "retrospective", "tier-3", "audit-harness", "schema-postmortem", "case-study"]
categories = ["Monthly Retrospective"]
description = "April 2026 retrospective — 30 posts, 162 commits, eight Tier 3 case studies (the first real month of Tier 3 publishing), audit-harness v0.1.0 shipped, the rubric-on-spec postmortem set the architectural rule, and the daily classification pipeline ran clean for half the month."
+++

April was the month Tier 3 found its footing. March's retrospective predicted "a natural T2 rate of roughly 5–10%" — about two to three deep-dives per month out of thirty. April blew past that. Of the eighteen posts that ran through the classifier, eight were Tier 3 case studies. Five of them landed at the top of the depth charts at three hundred lines or more. The teaching dimension scored a flat **TCH=4** on every one of them — the highest score the rubric assigns short of "this changes the field."

This was not inflation. The work itself was deeper. The audit harness shipped as a packaged dev dependency. The Braves Booth dashboard hit v1.0 and added a four-tier LLM fallback chain forty-four minutes before a live broadcast. The schema validator debacle generated a postmortem that defined the architectural rule for every future "rubric on top of spec" decision. The CLAUDE.md spec entries reached the threshold where propagating them across nine repositories became a script run instead of a manual chore. That is a different shape of month than March was, and the classifier caught it.

Thirty posts. One hundred sixty-two commits across twenty-four active repositories. The commit count compressed again — January 627, February 446, March 295, April 162 — and the trend remains a signal, not noise. Less code, denser writing, more posts that someone will still want to read a year from now.

## Velocity Dashboard

| Metric | April 2026 | March 2026 | Delta |
|--------|-----------|-----------|-------|
| Posts published | 30 | 35 | -5 |
| Total commits (Jeremy-authored, all repos) | 162 | 295 | -45% |
| Commits per post | 5.4 | 8.4 | -36% |
| Active repos | 24 | ~5 | +19 (breadth) |
| Posts classified | 18 of 30 (60%) | 1 of 35 (3%) | +57 pp |
| Tier 1 (Field Note) | 5 (28%) | 0 of 1 (0%) | — |
| Tier 2 (Deep-Dive) | 4 (22%) | 1 of 1 (100%) | — |
| Tier 3 (Case Study) | 8 (44%) | 0 of 1 (0%) | +8 |
| Avg confidence (classified posts) | 0.81 | — | — |
| Anti-inflation flags raised | 18+ | — | — |
| Top-5 post depth (lines) | 327, 306, 303, 300, 300 | — | — |

A few notes on the table because the numbers tell more than one story:

**Posts classified jumped from 3% to 60%.** March's classification rate was an artifact of timing — the system shipped late in the month and only one post went through it. April was the first full month with classification running on the daily pipeline. The 60% rate, not 100%, reflects two things: the classification runner did not start firing until April 14th (so April 1–13 were never classified), and a handful of posts were generated through paths that bypassed the classifier (manual backfill of older drafts, weekly recap stubs). May should be the first month at or near 100% classification coverage.

**Active repos jumped from ~5 to 24.** That is not a true increase in scope — it is a broader accounting. March's retrospective counted "active projects" by what carried a thesis-level narrative. April's number counts every repo with at least one Jeremy-authored commit in the month. The April number is more honest. Both numbers describe the same underlying reality: the project portfolio is wide and a small subset carries the headline narratives at any given time.

**Anti-inflation flags raised on every Tier 3 classification.** The classifier's job is not to award high tiers — it is to gatekeep them. Every one of the eight Tier 3 calls came with a documented anti-inflation reason: *year-from-now test passes*, *Tier 3 budget check applied*, *volume-not-quality watch acknowledged*, *first-time-for-me-not-novel disqualified*, *busy-not-distinguished considered and rejected*. The audit trail in `decisions.jsonl` shows the classifier reasoning its way to each call rather than reaching for the highest tier by default. That is the calibration working as designed.

## Top 5 Posts by Teaching Potential (TCH=4 across all)

Every Tier 3 post in April scored TCH=4 — the same teaching dimension that distinguishes a useful case study from a working journal entry. Five stand out:

### 1. The Rubric Sits On Top Of The Spec — A Schema Validator Postmortem (Apr 28)

[The post](/posts/schema-debacle-rubric-on-spec-postmortem/). 300 lines.

This is the one that earned the architectural rule. The skill validator's required-field set was reframed mid-development as "marketplace polish" instead of "marketplace gating," which broke the marketplace tier's enforcement model and cost half a day of conversational repair. The lesson translates beyond the validator: when an enterprise rubric lives on top of an open spec, the rubric must be **strictly additive**, never a redefinition of the spec's floor. The non-negotiables now live in the schema changelog so future contributors cannot make the same drift accidentally.

The post earned its Tier 3 designation on candor as much as content. The original mistake is documented in detail. The fix is documented. The rule that prevents the repeat is documented. That is the pattern the Tier 3 budget is supposed to fund.

### 2. Propagation Day — When the CLAUDE.md Spec Becomes the Migration Plan (Apr 30)

[The post](/posts/propagation-day-when-the-spec-becomes-the-migration-plan/). 306 lines.

Three CLAUDE.md spec entries hit critical mass on the same day: testing SOP, secrets posture, and VPS-as-the-home deployment pattern. Each had been written first, debated, refined, and then propagated. When the propagation actually happened across nine repositories, it was not a manual chore — it was a script run. The spec, written deliberately and ahead of time, **was** the migration plan.

The teaching dimension is the prerequisite, not the propagation: every spec that turned into a script run was written with propagation in mind. Specs written for "this repo only" do not transfer. Specs written for "every repo we will ever ship" carry the migration shape inside them. That distinction is worth more than the script.

### 3. Gemini PR Review Silent Fail — Cross-Repo Triangulation (Apr 23)

[The post](/posts/gemini-pr-review-silent-fail-cross-repo-triangulation/). 303 lines.

A Gemini PR review workflow appeared green in CI but silently failed every actual review for two weeks. The fix was not in any single repo. It was in cross-repo triangulation: comparing the workflow file across three different projects, identifying what changed in the one that worked versus the two that did not, and finding the single missing permission grant that all three thought they had configured.

The teachable pattern: **when CI passes but the work product is empty, the bug is almost always in the seam between two systems neither of which fully owns the contract.** Looking inside the failing repo will not find it. Looking across repos will.

### 4. FLOPs Correction — Unchecked Derivation Peer Review (Apr 15)

[The post](/posts/flops-correction-unchecked-derivation-peer-review/). 300 lines.

A FLOPs derivation in an earlier post had an unchecked exponent that propagated through the conclusion. A peer review caught it. The post is the correction, the analysis of how the original error survived self-review, and the addition of "show your work in the post itself, not in a comment thread" to the personal style guide. Public correction is the only correction that lands.

### 5. Forty-Four Minutes Before First Pitch — An LLM Fallback Chain (Apr 29)

[The post](/posts/broadcast-day-llm-fallback-jchads-challenge/). 327 lines — the longest April post.

Groq quota died forty-four minutes before a live Atlanta Braves radio broadcast. The Braves Booth narrative engine depends on it. The fix was a four-tier LLM fallback chain: Groq → Vertex Gemini → Anthropic Claude → facts-only deterministic renderer. The facts-only renderer is the load-bearing layer. When every LLM is unavailable, the broadcast still gets numbers and structured commentary; it just gets them without the prose. Then JChad's Challenge — a live probability gauge — shipped in the same session.

The teaching value: **fallback chains terminate in a deterministic component, never another probabilistic one.** A chain that goes LLM → LLM → LLM does not actually fall back. A chain that goes LLM → LLM → deterministic does.

## Projects: Started / Shipped / In Progress

### Shipped This Month

- **`@intentsolutions/audit-harness` v0.1.0** ([npm](https://www.npmjs.com/package/@intentsolutions/audit-harness)). The canonical Intent Solutions testing package — hash-pinning, escape-scan, CRAP, architecture, bias, Gherkin lint — packaged so every repo installs it as a dev dependency rather than referencing `~/.claude/` paths. Companion to `/audit-tests` and `/implement-tests` skills. The "enforcement travels with the code" principle is now an artifact, not just a slogan.

- **Braves Booth v1.0** ([scorecardecho.com](https://scorecardecho.com)). Player drilldown shipped, broadcast operations stable, four-tier LLM fallback chain landed, JChad's Challenge live probability gauge added. Currently running for live Atlanta Braves radio broadcasts.

- **Claude Code Slack Channel v0.2.0** — security hardening for external contributors. Hash-chained tamper-evident audit journal, per-thread session isolation, policy-gated MCP tools, five-layer prompt-injection defense. The full security sprint shipped five releases in one day on April 19th.

- **Schema validator postmortem rules** — the non-negotiables now live in the schema changelog: required fields are not negotiable, marketplace tier errors are not warnings, the IS rubric sits on top of the spec and never beneath it. Engineering rules with permanent provenance.

### In Progress

- **CLAUDE.md spec propagation** — the Apr 30 propagation day was one wave of nine repos. There are more to go. The pattern is now mechanized; what remains is identifying which repos still need the SOPs/testing/VPS-deploy entries applied.

- **VPS-as-the-home program** — the migration plan documented in `intentsolutions-vps-runbook` continued through April. Several priorities (P0–P3) closed; remaining priorities track to May. Per-priority discipline (code change → repo CLAUDE.md → 000-docs → runbook → AAR → bead+GH closure) held throughout.

- **cad-dxf-agent** — continued from March. AEC drawing intelligence platform; v0.2.0 milestone targeting May.

- **Knowledge OS / `intentional-cognition-os`** — local-first knowledge OS bootstrap. Seven epics scoped early in the month, several completed. The marketplace-security thread inside the Knowledge OS work was the source of one of April's Tier 2 deep-dives.

### Started This Month

- **`audit-harness` propagation** — every Intent Solutions repo will adopt the package as the testing-quality gate. Started in April with the canonical install in two reference repos; rollout to the rest is a May/June priority.

- **`/contribute` skill** ([contributing-clanker](https://github.com/jeremylongshore/contributing-clanker)) — local-only OSS contribution workspace. Tracks in-flight PRs, builds per-repo dossiers (CLA, DCO, branch convention, AI-assistance policy), and runs deterministic gates before any AI-assisted PR reaches a maintainer. April was the bootstrap month; the skill is in active use against open-source contribution work.

## Methodology Calibration

This is the first month with enough classification volume to actually calibrate.

- **Tier distribution (classified posts only):** Tier 1 = 5 (28%), Tier 2 = 4 (22%), Tier 3 = 8 (44%), unclassified-or-recap = 1.
- **Average confidence:** 0.81 across classified posts. The classifier was confidently wrong on zero posts and uncertain (confidence ≤ 0.7) on zero posts. Every call landed in the 0.72–0.92 range.
- **Anti-inflation flags raised:** every Tier 3 call came with at least one explicit flag. Most common: *year-from-now test passes* (used as a positive justification rather than a brake), *volume-not-quality watch* (raised on multi-commit days that could have inflated to Tier 3 on activity rather than thesis), *first-time-for-me-not-novel* (used to keep "I just learned X" from being mistaken for "X is novel to the field").
- **Calibration drift:** the Tier 3 rate jumped from 0% in March to 44% of classified posts in April. That looks like inflation on its face. It is not — March's denominator was 1 post (the system had just shipped), and the sample-of-one is the wrong baseline. April is the first month with a real distribution. May will be the first month with a comparison.

The honest read: April was unusually deep, not unusually inflated. The schema postmortem, the LLM fallback chain, and propagation day were all genuinely Tier 3 material under any reasonable definition of "year-from-now teaching value." Whether the 44% rate persists or settles toward March's predicted 5–10% is what May tells us.

The 12 unclassified posts (April 1–13 plus a few cron skips) will be retroactively classified as part of May's calibration pass. That data will retroactively settle April's true distribution.

## Wins

- **The audit harness shipped as a real package.** "Enforcement travels with the code" stopped being an aspiration and started being an `npm install` command.
- **The schema postmortem became the architectural rule.** Mistakes that generate a permanent rule are the cheapest mistakes a system makes.
- **The Braves broadcast survived the Groq outage.** The fallback chain worked under real game-day pressure. The deterministic facts-only tier was the load-bearing component.
- **Tier 3 became routine, not exceptional.** Eight Tier 3 case studies in one month is more than every prior month combined. The site is now publishing the kind of content that distinguishes a working blog from a journal.
- **Propagation day proved spec-first works.** Three CLAUDE.md entries propagated across nine repos in a script run. The discipline of writing the spec ahead of the migration paid off in measurable hours.

## Lessons Learned

- **The classifier needs an early-month catch-up runner.** April 1–13 went unclassified because the daily runner did not start firing until mid-month. May's calibration pass will retroactively classify those, but the lesson is to build the catch-up runner into the cron itself so the gap never reopens.
- **Anti-inflation flags need a counter-flag for genuine depth.** The classifier currently raises *year-from-now test passes* as a flag, which reads ambiguously — is that a brake or a justification? The phrasing should split into two distinct fields: one for "raised but not blocking" and one for "active brake."
- **Tier 3 case studies cluster around postmortems.** Four of the eight Tier 3 posts in April were postmortems (schema debacle, FLOPs correction, Gemini silent fail, deploy gotchas). That is not a coincidence — postmortems force candor and cause-effect mapping, which is exactly what teaching value rewards. Future months should not avoid postmortem material out of brand-protection instinct; the audience reads them harder than any other format.
- **Active-repo count without a depth filter overcounts.** The 24-repo April number is technically true but overstates the work that mattered. May's retrospective should report both numbers (total active + carries-narrative subset) so the trend in each is visible separately.

## Next Month Focus

1. **Close the classification coverage gap.** Build the catch-up runner so May reports 100% classification coverage, including any cron skips. Backfill April 1–13 retroactively as part of May's calibration pass.
2. **Audit-harness propagation across the portfolio.** Adopt the package as a dev dependency in every active Intent Solutions repo. Track adoption count and update the testing SOP entry in each repo's CLAUDE.md.
3. **VPS-as-the-home P4–P8.** Continue the disciplined per-priority closure pattern. Each priority lands as a complete unit (code → CLAUDE.md → 000-docs → runbook → AAR → beads+GH).
4. **Watch the Tier 3 rate.** If May settles to 5–15% Tier 3, the system is calibrated correctly and April was a genuine peak. If May stays at 40%+ Tier 3, the classifier's anti-inflation flags need re-tuning.

April was the month the daily output got dense enough that the rubric had real distributions to work with. May is when calibration gets to do its job.
