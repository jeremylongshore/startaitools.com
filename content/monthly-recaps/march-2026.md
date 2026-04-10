+++
title = 'March 2026: 35 Posts, the Eval Framework That Shipped 10 Epics in a Day, and a Meta-Milestone'
slug = 'march-2026'
date = 2026-03-31T18:00:00-05:00
draft = false
tags = ["monthly-retro", "metrics", "retrospective", "eval-framework", "tier-classification", "meta"]
categories = ["Monthly Retrospective"]
description = "March 2026 retrospective — 35 posts published, 340 commits, j-rig binary eval framework shipped 10 epics in one day, and the tier classification system itself was designed and built."
+++

March was the month the machinery became self-aware. Not in a dramatic AI sense — in the sense that the content system started tracking itself. The tier classification system was designed, built, and deployed. The blog-backfill pipeline went operational. And the j-rig binary eval framework proved that a well-structured evaluation system can move at sprint speed: ten epics from planning to production in a single day.

Thirty-five posts. Three hundred forty commits. The commit count dropped again — January had 627, February had 446, March has 340 — and that trend is now clearly a signal, not noise. The work is getting more focused. Fewer repositories are active. Each commit carries more weight. And the blog is capturing more of the work, which means the commits-per-post ratio continues to compress.

## Velocity Dashboard

| Metric | March 2026 | February 2026 | Delta |
|--------|-----------|--------------|-------|
| Posts published | 35 | 28 | +25% |
| Total commits | 340 | 446 | -24% |
| Commits per post | 9.7 | 15.9 | -39% |
| Tier 1 (Field Note) | — | 15 (100%) | — |
| Tier 2 (Deep-Dive) | 1* | 0 | +1 |
| Tier 3 (Case Study) | 0 | 0 | — |
| Avg confidence | — | 0.87 | — |
| Posts classified | 1/35* | 15/28 | — |
| Active projects | 5 | 7 | -2 |
| Projects shipped | 3 | 2 | +1 |

*Only 1 post was classified via the backfill system (j-rig binary eval framework, T2). The remaining 34 posts were published before the backfill pipeline existed. Most March content (Mar 1-28) was already published using the established daily cadence before the classification infrastructure came online. Only the final days of March went through the new pipeline.

The 35-post count is the highest of any month so far. This reflects the existing daily publishing cadence plus a few multi-post days. The cadence is no longer something that requires discipline to maintain — it is the default state.

The classification gap is a known artifact of the rollout timeline. April will be the first full month where every post goes through classification at publish time. That is the real baseline.

## Top 3 Posts by Teaching Potential

### 1. j-rig Binary Eval Framework: 10 Epics, One Day (TCH=3)

This is the post that earned Tier 2. Ten epics from spec to shipped in a single day: Zod schemas for type-safe evaluation definitions, SQLite evidence layer for persistent audit trails, calibration engine for tracking evaluator agreement, drift detection for catching model regression before it hits production.

The teaching value is not just the eval framework itself — it is the demonstration that a well-scoped epic structure with clear acceptance criteria can compress what looks like a month of work into sixteen hours. The prerequisites: each epic had a concrete deliverable, each deliverable had a verification step, and the epics were ordered so each one built on the previous output. No epic depended on ambiguous research or open-ended exploration.

The key technical insight: binary evaluation (pass/fail, not 1-5 scales) eliminates the calibration ambiguity that makes most eval frameworks unreliable. When you force every evaluation to a binary decision, you can actually measure inter-rater reliability. Two evaluators either agree or they do not. With Likert scales, two evaluators can give scores of 3 and 4, and the system reports "high agreement" even though they had fundamentally different interpretations of the criteria. Binary forces clarity. It is less granular and more honest.

### 2. Tier Classification System Design and Implementation

This post does not have a TCH score because it was never run through the classifier — it is the post about building the classifier. The meta-circularity is noted and set aside.

The system itself is straightforward: three tiers (Field Note, Deep-Dive, Case Study) with defined criteria, a confidence score, and a decisions.jsonl audit trail. The interesting design decisions are in the audit layer. Every classification gets logged with the inputs, the decision, the confidence, and a methodology note explaining the reasoning. This creates a calibration feedback loop: every month, you can ask "were the Tier 2 posts actually deeper than the Tier 1 posts?" and get a data-driven answer instead of relying on memory.

The three-tier structure was deliberate. Two tiers (short/long) do not capture enough variation. Five tiers create ambiguity in the middle three. Three tiers with clear boundaries — daily log, technical narrative, multi-week investigation — give the classifier enough resolution to be useful without creating borderline-case paralysis.

### 3. Blog-Backfill Pipeline

The backfill pipeline solves a specific problem: what do you do with the 90+ posts published before the classification system existed? Manual review of every post is not practical at daily publishing cadence. Automated classification with human override flags is.

The pipeline reads existing posts, classifies them, generates a confidence score, and flags anything below the confidence threshold for manual review. Posts above the threshold get auto-classified. The threshold is set conservatively — better to flag too many for review than to silently misclassify.

The more interesting output of the backfill pipeline is the aggregate statistics. When you classify three months of posts retroactively, you get a baseline distribution that reveals the natural shape of the content. January was 93/7 T1/T2. February was 100/0. March's single classified post was T2. These ratios, taken together, suggest a natural T2 rate of roughly 5-10% — about two to three deep-dives per month out of thirty posts. That is the target to calibrate against going forward.

## Projects: Started / Shipped / In Progress

### Started This Month

- **Blog tier classification system** — Designed, implemented, and deployed within March. Three tiers, confidence scoring, JSONL audit trail, calibration feedback loop. This is the meta-project that makes all future retrospectives data-driven instead of vibes-based. The system was designed to be simple enough that classification adds less than 30 seconds per post. If it takes longer, adoption will fail.

- **Blog-backfill pipeline** — Automated retroactive classification for pre-existing posts. Reads markdown frontmatter and content, classifies against the tier criteria, generates confidence scores, and writes results to the audit trail. The pipeline processed the full archive in under ten minutes.

### Shipped

- **j-rig binary eval framework** — Ten epics in one day. Zod schemas for type-safe evaluation definitions. SQLite evidence layer for persistent audit trails. Calibration engine for inter-rater reliability tracking. Drift detection for catching model regression. The whole stack, from schema design to production deployment, in sixteen hours. Shipped and immediately usable by downstream projects.

- **Tier classification system v1.0** — Operational and classifying posts. The v1.0 designation is meaningful — the system has defined criteria, a logging pipeline, and a calibration methodology. It is not a prototype.

- **Backfill pipeline v1.0** — Running against the full post archive. The retroactive classification data is already being used in this retrospective. The pipeline paid for itself before it was officially "shipped."

### In Progress

- **cad-dxf-agent** — Continued development from February. The planner self-correction architecture is stable and handling real failures. Moving toward processing actual engineering DXF files. The agent works but is not yet at a version milestone worth announcing.

- **Content strategy and methodology tracking** — The infrastructure for tracking publishing decisions over time. Built on top of the tier classification system. The decisions.jsonl file is the foundation — every classification decision is logged with enough context to reconstruct the reasoning months later.

## Methodology Calibration

This section is different this month because March is when the calibration methodology was built. There is no historical baseline to compare against internally — the baseline comes from the backfill pipeline's retroactive classification of January and February posts.

The one classified post (j-rig at T2) is correctly classified. It has genuine architectural depth (Zod schemas, SQLite evidence layer, calibration engine), transferable patterns (binary evaluation, epic scoping), and a multi-step technical narrative (ten epics with dependencies). A sample size of one does not support trend analysis, but it does validate that the T2 criteria correctly identify deep-dive content.

What I can say about the criteria after building them: the boundary between T1 (field note) and T2 (deep-dive) is clear in practice. A field note documents what happened. A deep-dive explains why it works, how to replicate it, and what the failure modes are. The j-rig post is unambiguously a deep-dive. The daily logs from March 1-28 are unambiguously field notes. There are no borderline cases in the March corpus that would challenge the criteria.

The T2-to-T3 boundary is less tested. Tier 3 (Case Study) requires a multi-week investigation with original data. No post in the first three months qualifies. This is expected — case studies are rare by definition. If one appears every quarter, that is probably the right frequency.

April will be the real test. Full-month coverage. Every post classified at publish time. No backfill gaps. That is when we will see whether the criteria hold under daily use and whether the confidence distribution settles into a healthy shape.

### Three-Month Trend Analysis

With three months of data (even incomplete), some patterns emerge:

| Month | Posts | Commits | Commits/Post | T1% | T2% | Confidence |
|-------|-------|---------|-------------|-----|-----|------------|
| Jan | 32 | 627 | 19.6 | 93% | 7% | 0.89 |
| Feb | 28 | 446 | 15.9 | 100% | 0% | 0.87 |
| Mar | 35 | 340 | 9.7 | —* | —* | —* |

The declining commits-per-post ratio is the most interesting trend. From 19.6 to 15.9 to 9.7. Three possible interpretations: (1) the posts are getting thinner, (2) the commits are getting denser, or (3) the blog is simply capturing more of the work that previously went undocumented. Based on post length data (which has remained stable at 700-900 words for field notes), interpretation three is the most likely. The blog is not getting thinner — the coverage is getting broader.

The post count trend (32, 28, 35) shows natural variation around a daily publishing baseline. February's dip is calendar-driven (28 days). March's spike reflects a few multi-post days during the j-rig sprint. The underlying cadence — one post per day minimum — is stable.

### The Meta-Milestone

This deserves its own callout. March is the month the blog system became self-referential. The tier classification system classifies blog posts. The calibration system evaluates the classifier. The retrospective (this post) analyzes the calibration. And the backfill pipeline retroactively applies all of this to the historical archive.

This is not over-engineering. This is the minimum viable infrastructure for making data-driven content decisions at daily publishing cadence. Without classification, every post is equivalent. Without calibration, the classification drifts. Without retrospectives, nobody asks whether the system is working. Without backfill, the historical data is a black hole.

The system is complete as of March 31. April is the first month where it runs end-to-end without manual intervention.

## Wins

1. **j-rig: 10 epics in one day.** This is the headline. Zod schemas, SQLite evidence layer, calibration engine, drift detection — all from spec to shipped in sixteen hours. The epic structure and binary evaluation decision made this possible. This is the proof that epic scoping is a force multiplier, not overhead.

2. **The tier classification system exists and works.** This sounds minor. It is not. Every post from April forward will carry a tier classification, a confidence score, and an audit trail. Content strategy becomes data-driven instead of vibes-based. Decisions become reviewable. Calibration becomes automated.

3. **Highest post count of any month.** Thirty-five posts. The daily cadence is not just maintained — it occasionally produces multiple posts per day. The writing muscle is strong enough that publishing does not feel like a separate task from the engineering work.

4. **The commit-to-post ratio hit its lowest point.** 9.7 commits per post, down from January's 19.6 and December's 40.4. This means more of the work is being captured in writing. The blog is catching up to the code. Dark matter in the git log is shrinking.

5. **Three projects shipped.** j-rig, tier classification, backfill pipeline. All three are infrastructure that makes future work better. Shipping tooling is less visible than shipping features, but the compound returns are higher.

## Lessons Learned

1. **Binary decisions beat scales.** The j-rig eval framework validated this at the system level. The tier classification system validated it at the content level. When you force a binary pass/fail, you eliminate the ambiguity that hides in 3-out-of-5 scores. This principle applies to code reviews, hiring decisions, and feature prioritization. If you cannot say yes or no, you do not have enough information to decide — go get more information instead of hiding behind a 3.

2. **Build the tracking system before you need it.** The tier classification system should have existed in January. Building it in March means 60+ posts need retroactive classification. Starting measurement early — even imperfect measurement — beats retrofitting. The backfill pipeline exists solely because the classification system was built two months late.

3. **Meta-work is real work.** Building the classification system and backfill pipeline does not produce user-facing features. It produces the infrastructure for making better decisions about what to build next. That is a different kind of value, and it is easy to deprioritize because it never feels urgent. But the first retrospective written with real data (this one) is already better than the ones written from memory.

4. **Commit volume will keep dropping, and that is fine.** January 627, February 446, March 340. Each month the work gets more focused and each commit carries more weight. This is not a productivity decline — it is a maturity signal. The reflex to worry about declining commit counts is a holdover from measuring effort instead of output. Stop it.

5. **Epic scoping is the highest-leverage planning activity.** The j-rig experience proved that ten well-scoped epics can ship in a day. The key is "well-scoped" — each epic has a concrete deliverable, a verification step, and a clear dependency chain. Poorly scoped epics (open-ended research, ambiguous acceptance criteria) would have turned that same day into a planning session that produced a backlog instead of a product.

## By the Numbers

- **Days with zero posts:** 0. Three consecutive months of daily publishing. 95 posts total across Q1.
- **Total Q1 output:** 95 posts, 1,413 commits across January through March.
- **j-rig sprint duration:** 16 hours from first epic to final deployment.
- **Backfill pipeline processing time:** Under 10 minutes for the full 90+ post archive.
- **New infrastructure shipped:** 3 systems (tier classification, backfill pipeline, j-rig eval framework).
- **Tier 2 posts across Q1:** 3 total (2 in January, 0 in February, 1 in March). That is a 3.2% T2 rate against 95 total posts.
- **Active project count trend:** 8, 7, 5. Projects are consolidating. Focus is narrowing.

The Q1 totals reveal the real story. Ninety-five posts and 1,413 commits in three months. The post count is consistent. The commit count is declining. The project count is declining. Everything is converging toward fewer projects with deeper engagement and better documentation. That is the trajectory you want.

## Next Month Focus

- **Full classification coverage.** Every April post gets classified at publish time. No backfill. No gaps. This is the non-negotiable baseline for all future calibration work.

- **First formal calibration report.** With a full month of classification data, run the first formal calibration analysis. Are the tier boundaries holding? Is there inflation? What does the confidence distribution look like? Are there posts the classifier flagged as borderline that a human would classify differently?

- **j-rig production deployment.** The eval framework shipped fast. Now put it under real load with real evaluators and see if the binary decision framework holds up when the stakes are not synthetic.

- **cad-dxf-agent to a major milestone.** This project has been "in progress" for two months. March did not push it forward as much as planned. April needs a clear deliverable — a version number, a capability gate, something concrete.

- **Content strategy documentation.** The methodology exists in code (the classifier) and in my head (the criteria). It needs to exist in writing so it is reviewable, challengeable, and improvable by someone other than me. Not for the blog — for internal reference.

- **Watch the commit-to-post ratio.** 9.7 is low. If it drops below 5, the blog is outpacing the engineering work, which means the posts are getting thinner. The ratio should stabilize, not continue to fall. Find the equilibrium.
