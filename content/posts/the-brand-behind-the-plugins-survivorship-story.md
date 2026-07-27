+++
title = 'The Brand Behind the Plugins: A Survivorship Story'
slug = 'the-brand-behind-the-plugins-survivorship-story'
date = 2026-07-27T07:30:00-05:00
draft = false
tags = ['origin-story', 'operator', 'distribution', 'brand', 'verified']
categories = ['DevOps']
description = 'Why the plugin marketplace ran away. Lead with survivorship + the distribution gap, not the repo count. Tier 2 brand piece.'
+++

The plugin marketplace that hit 2,558 GitHub stars did not start as a plugin marketplace. It started as a $4.99 second-opinion tool for truckers who had a check-engine light at 2 AM and a shop that wanted to upsell them on parts they did not need. DiagnosticPro was the seed.

That was the first version. Then it was rebuilt. Then rebuilt again. Three rebuilds before it landed anywhere close to right. The repo is still live at diagnosticpro.io if you want to read the diff history; the story matters more than the code, and that is the only reason a self-taught ex-restaurant-operator who never wrote production code has 2,558 GitHub stars, 368 forks, four publicly-verifiable inbound conversations, and a Claude Partner credential issued by Anthropic. The road here was not clean and the honest version of it is not the version most people would tell.

## Survivorship is the moat

Most founder stories lead with the scoreboard. Two thousand five hundred stars. Forty-five thousand npm downloads a year, except that number was a guess and the real answer is closer to two thousand, which is what npm's registry honestly tells you when you look. The point is the scoreboard is what someone reads after they have already decided whether to trust you, not before. The thing that earns the trust is the long, boring middle where everything almost died and didn't.

Twenty years in restaurant operations first. Multi-unit P&L ownership with Bloomin' Brands: Outback Steakhouse and Bonefish Grill: across markets in the Southeast, plus an open-deck / flatbed trucking authority that ran for six years and ended cleanly in mid-2025. Both taught the same muscle: a CI gate is a line check. A fail-closed pipeline is a health inspection. Managing distributed people across regions for two decades is the same muscle as running a modern AI build team, except one of them pays your rent and the other one writes good blog posts. The operator lens is the whole differentiator and nobody else in AI publishes from exactly this angle. That is the point.

## The honest distribution gap

The thing nobody says out loud about the OSS playbook is that 2,558 stars is small. Marketplace-class traction is six figures, not four. A community of 425 plus plugins and 2,810 plus skills indexed across an ecosystem is meaningful relative to its peers and small relative to the problem it tries to solve. Most AI tooling sits in a distribution valley: too big for a personal project, too small for an enterprise platform. The companies that escape the valley are not the ones with the best code; they are the ones who figure out distribution first.

That is the bind this piece lands alongside. Four people in the funding community self-discovered the work in public. Polygon CTO Mudit Gupta called it out publicly on X and LinkedIn: that is searchable. Nixtla paid us to ship against it. Lit Protocol and Elm both reached out. Anthropic shipped a Claude Partner credential in July 2026: public Credly record, no NDA, no partner-program disclosure required because it is verifiable on the public web. The Kilo AI inbound is in flight; will update if it becomes a fifth. Five companies whose combined funding exceeds 500 million dollars found the work without outbound. The product worked, the documentation told the right story, the right people found it.

The seven-person Claude Partner cohort that Anthropic runs is the closest institutional benchmark. Less than a tenth of one percent of the people who learned Claude Code in 2025 are formally certified to scope, deploy, and run activations. The work is real and the credential is verifiable, but the distribution is the long pole and the long pole has not been pulled.

## What this means for the next ninety days

The Distribution move is not going to be a launch event. The Distribution move is going to be four pieces of work executed on the same week:
1. The brand piece (this one) ships + is dual-published to tonsofskills.com/blog + cross-posted to Dev.to / Hashnode / Medium / Substack per the publishing packet in intent-solutions-io/intent-blueprint-docs.
2. A diagnostic engagement offer: scoped at the four inbound conversations, no NDA required: published as a public list on intentsolutions.io.
3. A weekly dispatch cadence on Jeremys blog: Tue / Thu against the next-topics queue, Tier 2 minimum per piece, with the voice deny-list enforced by lint-post-voice.py on every merge.
4. The flagship plugin set: three premium Skills, three premium commands, three premium agents surfaced on tonsofskills.com/explore behind a clean capability-graph UI.

Each is verifiable in a public registry. Each ships behind a deterministic gate. None of them require outbound selling, and that is by design. The inbound velocity has been the only growth motion that has ever worked for this practice, and the Distribution question is what speed the inbound arrives at, not whether inbound is the right motion.

## The verified receipt

For the GC verifiability pass that closes every Tier 1 plus publish (per `.claude/skills/blog-backfill/methodology/publishing-gates.md`):

- Claude Partner Badge: `https://www.credly.com/badges/ddf22fb4-0aa6-46b3-a93b-0b45b509e471` (issued 2026-07).
- Plugin marketplace live star + fork count: `https://github.com/jeremylongshore/claude-code-plugins-plus-skills`. As of 2026-07-27 the canonical observed figures are 2,558 stars, 368 forks. The footer on jeremylongshore.com and the .about page on startaitools.com both render the same live count via the GithubRepoStarsCountPlugin, not hand-maintained.
- npm registry ground truth: `https://api.npmjs.org/downloads/point/last-year/@intentsolutionsio/ccpi`: 2,084 downloads over the last 365 days as of 2026-07-27. The earlier 45,000-plus NPM figure was an overclaim. The corrected figure is two thousand a year and that is the honest answer.
- Inbounds found independently: see `.claude/skills/blog-backfill/methodology/they-found-me.md` for the maintained dossier with per-entry confidence and source of evidence.

The 500-million-dollar figure for the four named inbounds combines Nixtlas disclosed seed + Series A, Lit Protocols disclosed round, Elms disclosed seed, and Mudit Guptas public association with Polygon. None of the dollar amounts are private. They are public. Use them.

## Why this is the spine

Every Tier 1 plus piece going forward references this spine. The next dispatch: a case study on the four concurrent IRSB-Bob compliance rollouts that landed in the same week in March: points back here for the operator-lens framing. The piece after that: on the Eight-Stage gate framework that came out of the trucking-DOT regulatory practice: points back here too. The point is not that this is the best thing we will ever write. The point is that this is the bridge from twenty years of operations into twenty-five years of no ops, and the bridge has to be load-bearing because we are going to drive every subsequent piece of work across it.

Survivorship is the moat. The honest distribution gap is the lever. The verified receipts are the only reason anyone is going to believe either.

## What you can do with this if you run a team

If you run your own AI tooling practice and the survivorship framing matches your lived experience, here is the operating playbook that came out of this organization across the last year. Six behaviors, each load-bearing:

1. Instrument every gate so the gate produces evidence that survives an audit. The deterministic gates (shellcheck, ruff, actionlint, voice-lint, link checks, the 7-layer testing taxonomy) are not the constraint. The constraint is everything they produce is reproducible. Operators, not engineers, are the ones who can read this output. That is the point.

2. Treat every public registry as a source of truth. The npm downloads point referenced above is the same registry the agent just queried; the GitHub stars point on the about page renders from the live API at build time. The drift between what the codebase says and what the public sees is the source of every credibility loss the practice has ever taken.

3. Pin every dependency by commit SHA in the workflow file. The SHA pin across both startaitools.com and jeremylongshore.com: 11 lines, 7 references, zero behavior change, and the next time GitHub ships a backport the team does not have to remember to apply it manually.

4. Ship a piece of diagnostic work every week. Tuesday and Thursday. Tier 2 minimum. Voice-deny-list on every merge. The cadence matters more than the cadence. Daily case studies surface empirical evidence and the empirical evidence compounds.

5. Keep the inbound-credibility dossier live. Every named third party who talks about this practice in public gets a row in `.claude/skills/blog-backfill/methodology/they-found-me.md`. The GC verifiability gate ties to the dossier row. PII stays out. The cadence is what keeps the dossier honest.

6. Make every flagship product version-control its acceptance criteria. A flagship without version-controlled acceptance is a wishlist. The Flagships listed in `.claude/skills/blog-backfill/methodology/flagship-set.md` each carry a star + fork count and a verify-link. Acceptance lives in the same file as the product itself.

Survivorship is the moat. The honest distribution gap is the lever. The verified receipts are the only reason anyone is going to believe either. The six behaviors above are how the receipts get manufactured at a cadence that compounds.
