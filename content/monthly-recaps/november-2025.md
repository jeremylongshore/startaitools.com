+++
title = 'November 2025: The Depth Month — Fewer Posts, Triple the Commits'
slug = 'november-2025'
date = 2025-11-30T18:00:00-06:00
draft = false
tags = ["monthly-retro", "metrics", "retrospective", "hustlestats", "pipelinepilot", "perception", "nixtla"]
categories = ["Monthly Retrospective"]
description = "18 posts, 516 commits, 69% T1 rate. HustleStats hit v1.0.0, PipelinePilot went from 4 agents to 1, and Perception went from nothing to 8 agents."
+++

October said "write everything." November said "ship everything." The numbers tell the story: post count dropped 60% while commits more than doubled. That's what depth over breadth looks like in practice.

## Velocity Dashboard

| Metric | November 2025 | October 2025 | Delta |
|--------|--------------|--------------|-------|
| Posts Published | 18 | 45 | -60% |
| Commits | 516 | 220 | +135% |
| Posts Classified | 16 | 11 | +45% |
| T1 (Deep-Dive / Case Study) | 11 (69%) | 5 (45%) | +24pp |
| T2 (Field Note) | 5 (31%) | 6 (55%) | -24pp |
| Avg Confidence Score | 0.88 | 0.89 | -0.01 |
| Classification Rate | 89% | 24% | +65pp |

Every trend moved in the right direction. 89% classification rate versus October's 24% — that was the number one goal and it's basically solved. The T1 rate jumping to 69% means the posts that did get written were substantial. No more "today I updated a dependency" filler.

516 commits is real output. That's nearly 26 commits per post, which means the code-to-content ratio shifted heavily toward building. October was 4.9 commits per post. The delta here is the story: November was a building month that happened to produce writing, not a writing month that happened to produce code.

## Top 3 Posts by Teaching Potential

| Rank | Post | TCH | Why It Landed |
|------|------|-----|---------------|
| 1 | perception-agent-system-zero-to-mcp-dashboard | 3 | Building an 8-agent perception system from scratch, with MCP integration and a live dashboard. The architecture decisions around agent specialization carry real teaching weight. |
| 2 | hustlestats-launch-sprint-stripe-billing-paywall | 3 | End-to-end SaaS launch sprint: Firebase auth cutover, Stripe billing integration, paywall implementation. Every indie SaaS builder hits these same walls. |
| 3 | pipelinepilot-vertex-ai-migration-architecture-pivot | 3 | The 4-agent to 1-agent pivot. Documenting why you killed your own architecture is rare and valuable. Most people just quietly refactor and never explain the reasoning. |

No TCH=4 posts this month, unlike October's PipelinePilot SDR orchestrator. But the three TCH=3 posts cover fundamentally different domains — perception systems, SaaS billing, and architecture pivots. That's breadth of teaching even with fewer total posts.

The PipelinePilot pivot post deserves special attention. Writing "I over-engineered this and here's why the simpler version is better" is harder than writing "look at my clever multi-agent system." But it's more useful to readers by a wide margin. The tech blogging ecosystem is saturated with "look what I built" posts. It's severely lacking in "look what I tore down and why." The pivot post fills that gap: it documents the original architecture, the specific pain points that made it untenable, the simplification process, and the measured improvements after the refactor. That's the kind of post that saves someone else six weeks of learning the same lesson.

The HustleStats launch sprint post is the most broadly applicable. Every indie SaaS builder eventually hits the Firebase + Stripe + paywall trifecta. Having a real-world walkthrough that doesn't hand-wave the webhook complexity or pretend that subscription state management is trivial — that's useful content that ages well.

## Projects

### Shipped

**HustleStats v1.0.0** — The big one. Firebase migration completed (auth cutover from NextAuth), Stripe billing integrated, paywall live. This went from "production auth is broken" in October to "paying customers can sign up" in November.

The Firebase migration alone was a multi-week effort:
- Rewriting the auth layer (Firebase Auth SDK replacing NextAuth)
- Migrating user data (Prisma/Postgres → Firestore documents)
- Updating every API route that touched sessions
- Rebuilding the test suite around Firebase emulators

The Stripe integration was the second mountain — webhook handling, subscription lifecycle management, paywall middleware that checks entitlements on every protected route. Nothing about SaaS billing is as straightforward as the documentation suggests. The webhook idempotency alone took two days to get right.

**Nixtla Baseline Lab** — From first commit to enterprise v1.0.0 in one month. This started as "maybe I should build a forecasting toolkit" and ended with a production-grade baseline lab with statistical baselines (ARIMA, ETS, seasonal naive), evaluation harness, and a clean API for running comparisons.

The velocity here surprised me. Clean-slate projects with well-defined scope move fast when you're not fighting legacy decisions.

### Major Pivots

**PipelinePilot Architecture** — Killed the 4-agent design. Replaced it with a single-agent architecture on Vertex AI.

The original design had agents for lead qualification, outreach sequencing, response handling, and coordination. In practice, the coordination overhead between four agents was higher than the complexity each agent was supposed to manage. One well-structured agent with clear function boundaries does the same work with half the latency and a quarter of the debugging surface area.

The key insight: agent boundaries should map to trust boundaries or data boundaries, not to logical steps in a workflow. When all four agents shared the same data, the same permissions, and the same deployment target, the boundaries were artificial.

### Started from Zero

**Perception** — 8-agent perception system. This went from empty directory to functional prototype in November. Eight specialized agents:

1. Visual analysis
2. Audio processing
3. Text extraction
4. Context building
5. Pattern recognition
6. Anomaly detection
7. Summary generation
8. Dashboard rendering

The MCP integration lets external tools query any agent directly. Unlike PipelinePilot's artificial agent boundaries, Perception's eight agents have genuine specialization — each one processes a different data modality with different models, different latency profiles, and different failure modes. That's why eight agents is the right call here while four was wrong for PipelinePilot.

**NWSL AI Video Pipeline** — Veo for video generation, Lyria for music/audio. An AI-powered content pipeline for women's soccer highlights. Early stage but the Veo integration is working and producing usable clips.

The interesting challenge is editorial coherence — generating a highlight clip that tells a story rather than just concatenating cool plays. Lyria adds soundtrack generation that matches the energy of the footage. Still experimental, but the quality is already better than generic stock music over raw clips.

### Continued

**Claude Code Plugin Marketplace** — Maintenance mode. 62 plugins stable. Focus shifted to other projects. The marketplace is self-sustaining enough that it doesn't need daily attention, which is the whole point of building good automation in October.

## Methodology Calibration

The classification system is working now. 89% classification rate means nearly every post gets a tier call and a confidence score. The data is getting useful.

**T1 at 69% is probably right, not inflated.** October's concern was that T1 might be too generous. But with fewer total posts and each one being more substantial, 69% T1 is defensible. When you go from 45 posts to 18, the thin ones get cut first. What's left is the real work.

**Confidence at 0.88 is stable.** Basically unchanged from October's 0.89. The classifier isn't getting more uncertain as it sees more variety — that's a good sign. It means the tier definitions are clear enough to apply consistently.

**The missing 11% unclassified** (2 posts) were likely social media cross-posts or very short updates. Acceptable noise.

**Key calibration question for December:** Does the T1 rate hold if post volume goes back up? Or was November's high T1 rate an artifact of low volume? If I write 30+ posts next month and T1 stays above 60%, the system is working. If T1 drops below 50%, October's concern about classifier generosity was right.

## Wins

1. **HustleStats went from broken auth to v1.0.0 with billing.** That's the full SaaS lifecycle compressed into two months: crisis → stability → monetization. The Firebase migration was the hardest part — not technically, but organizationally. Every test had to be rewritten. Every deployment script updated. Every environment variable changed. And it all had to happen without downtime for existing users. The Stripe integration on top was almost anticlimactic by comparison — webhooks, subscription management, and paywall checks are well-documented patterns. The hard part was already done.

2. **The PipelinePilot pivot was the right call.** Killing a 4-agent architecture you spent weeks building is painful. But one agent with clear function boundaries is faster to debug, cheaper to run, and easier to explain to anyone who joins the project. Complexity has to earn its place, and four agents hadn't earned theirs. The single-agent version processes the same lead volume with 50% less latency because there's no inter-agent communication overhead. Sometimes the best architecture decision is subtraction.

3. **Perception from zero to 8 agents in one month.** When the architecture is right, velocity follows. The MCP integration pattern — each agent exposes its capabilities through a standard protocol — meant I could build agents independently and compose them later. No coordination code until the dashboard layer. This is the opposite lesson from PipelinePilot: when agents have genuine specialization (different data modalities, different models, different failure modes), multi-agent architecture earns its complexity.

## Lessons Learned

1. **Fewer posts, more depth works.** 18 posts with 69% T1 is objectively better than 45 posts with 45% T1. The math: November produced roughly 12 deep-dive posts. October produced roughly 5. Fewer posts, but more than double the high-quality output. The implication is counterintuitive — publishing less often produces more high-quality content, not less. The selection pressure of "is this worth writing up?" filters out the thin posts before they're written, and the time saved goes into making the remaining posts better.

2. **Kill your architecture before it kills you.** The PipelinePilot 4→1 agent pivot saved weeks of future debugging. The sunk cost fallacy is real in software. "But I already built four agents" is never a good reason to keep four agents. The question is always "does the architecture serve the problem?" and if the answer is no, refactor now, not later. Every week you delay a necessary simplification, the complexity accrues interest. Dependencies form. Tests get written against the complex version. Documentation assumes the complex version. Simplifying in week 2 is a refactor. Simplifying in month 6 is a rewrite.

3. **Firebase migration is underestimated by everyone.** Every blog post about "migrating to Firebase" makes it sound like a weekend project. It's not. Auth migration alone touches every route, every test, every deployment config, and every user session. Budget two weeks minimum and you'll still be fixing edge cases in week three. The specific trap: Firebase Auth and NextAuth both work fine in isolation. The migration path between them is where the dragons live — session format differences, token refresh timing, callback URL patterns, and the subtle ways each system handles "user not found."

4. **Nixtla velocity came from having no legacy.** Starting from zero with clear requirements and no technical debt is a gift. Enterprise v1.0.0 in one month wouldn't have been possible if there were existing users, existing data, or existing patterns to work around. This is worth remembering every time I'm frustrated by slow progress on a mature project — the speed difference between greenfield and brownfield is at least 3x, and pretending otherwise leads to unrealistic timelines.

## Two-Month Trend Analysis

Two data points isn't a trend, but the direction is consistent enough to be worth noting:

| Signal | Direction | Interpretation |
|--------|-----------|---------------|
| Post volume | Down 60% | Intentional. Quality filter is working. |
| Commit volume | Up 135% | More building, less narrating. |
| T1 rate | Up 24pp | Fewer thin posts → higher quality share. |
| Classification rate | Up 65pp | Methodology adoption. System is being used. |
| Confidence | Flat (-0.01) | Tier boundaries are stable. No classifier drift. |
| Commits per post | Up 5.9x | Each post represents dramatically more work. |

The most important row is commits per post. October's 4.9 meant most posts were observation — "I noticed this" or "I deployed that." November's 28.7 means each post represents a substantial chunk of engineering. That's the ratio I want to maintain.

## Next Month Focus

- **Nixtla deep sprint.** The baseline lab is at v1.0.0 but the skills system needs to scale. Target: 20+ skills, production validation, and automated PR reviews. This is the highest-priority project for December.
- **Git With Intent bootstrap.** The git tooling project has been in planning too long. Time to write code. From empty repo to working prototype.
- **Beads organization rollout.** Task tracking across all repos needs standardization. The ad-hoc approach isn't scaling — each project has its own tracking method and none of them talk to each other.
- **Maintain T1 rate above 60%** even if post volume increases. This is the calibration test that determines whether November's quality improvement was structural or just an artifact of writing less.
- **Commit velocity target: 800+.** November's 516 was a step up from October's 220. December should push further. The Nixtla sprint alone could drive 500+ if the skills system build goes as planned.

## Closing Thought

November proved something specific: the relationship between post quantity and post quality is not inverse. It's about selection pressure. October published everything. November published things worth publishing. The result wasn't fewer insights — it was more, concentrated into posts that actually teach something.

The PipelinePilot pivot and the Perception build also proved a meta-point about agent architecture: the number of agents is not a quality metric. Four agents that share boundaries is worse than one agent with clean functions. Eight agents with genuine specialization is better than either. The question is never "how many agents" — it's "do these boundaries earn their coordination cost?"

---

*November proved the thesis: depth beats breadth. The numbers are unambiguous — 135% more commits, 60% fewer posts, and every quality metric improved. October was the baseline. November was the proof that measuring matters. December will tell us if the improvements hold at higher volume.*
