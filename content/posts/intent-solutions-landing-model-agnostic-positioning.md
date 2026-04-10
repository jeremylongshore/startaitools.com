+++
title = 'Model-Agnostic Positioning and the IAE Branding Back-and-Forth'
slug = 'intent-solutions-landing-model-agnostic-positioning'
date = 2025-11-03T10:00:00-06:00
draft = false
tags = ["intent-solutions", "landing-page", "positioning", "pricing", "product-strategy"]
categories = ["Development Journey"]
description = "Removing IAE branding, adding model-agnostic messaging, building a pricing education hub, then restoring IAE branding the same day. The messy reality of product positioning."
+++

Six commits on the Intent Solutions landing site today. The throughline: figuring out how to position an AI agent product when the product itself is still forming.

## The Model-Agnostic Pivot

The landing page started with IAE (Intelligent Automation Engine) branding front and center. IAE is PipelinePilot's agent framework -- specific tools, specific architecture, specific Vertex AI integration. But Intent Solutions is not just PipelinePilot. The company offers consulting, custom agent builds, and integration work across multiple platforms.

Leading with IAE branding told visitors: "We sell one thing." That's wrong. We sell outcomes that happen to use agents.

First commit removed IAE references from the hero section, tagline, and feature cards. Replaced with model-agnostic language: "AI agents that work with your existing stack." No mention of Vertex AI specifically. No mention of Gemini. The messaging became about capabilities, not implementation details.

The theory was sound: buyers care about what agents do, not what framework powers them. A CTO evaluating agent platforms does not wake up thinking about ADK vs LangChain. They think about reducing headcount cost per qualified lead.

## The Pricing Education Hub

Second major change: a `/learn` section with four subpages. Not a pricing page. A pricing *education* hub.

AI agent pricing is confusing for buyers. Per-agent? Per-seat? Per-invocation? Usage-based with a floor? Most companies hide behind "Contact Sales" because the pricing models are genuinely complex. The confusion keeps buyers from even starting a conversation.

The `/learn` hub addresses this by teaching before selling. Four subpages, each targeting a different buyer question:

1. **How AI Agent Pricing Works** -- explains the cost components (inference, storage, API calls, orchestration overhead). Breaks down a real monthly bill for a 3-agent system so buyers see where the money goes.
2. **Vertex AI vs n8n: Security Comparison** -- side-by-side for buyers evaluating self-hosted vs managed. Covers data residency, secrets management, network isolation, and patch cadence.
3. **White-Label for Resellers** -- how agencies can rebrand the agent platform. Includes the technical requirements (custom domain, branding assets, API key isolation).
4. **Total Cost of Ownership** -- real numbers for a 3-agent deployment over 12 months. Includes infrastructure, maintenance hours, and the cost of the expertise needed to run it.

The Vertex vs n8n comparison is the most useful page. Buyers keep asking about self-hosted n8n as an alternative. The security comparison addresses the question directly: n8n gives you control but you own the patching, the secrets management, the network isolation. Vertex AI handles all of that but you're locked into GCP.

Neither is wrong. The comparison just makes the tradeoffs visible. Buyers who want control pick n8n. Buyers who want managed pick Vertex. The page helps them decide faster instead of going through three sales calls to learn what we could have told them upfront.

## Restoring IAE Branding

Three hours after removing IAE branding, I added it back.

The model-agnostic positioning was technically correct but emotionally flat. "AI agents that work with your existing stack" could be any consulting shop. There was no differentiation. No product identity. Nothing to remember.

IAE is a real product with real architecture. PipelinePilot is an implementation of IAE. Removing the brand didn't make the product more accessible -- it made it invisible.

The corrected positioning: Intent Solutions is the company. IAE is the platform. PipelinePilot is one implementation. The landing page now shows all three in a hierarchy instead of hiding two of them.

## The CLAUDE.md Commit

Created a CLAUDE.md for the landing site repo. Standard practice now for every project: what it is, how to build it, what not to touch. This is the sixth project CLAUDE.md I've written and the format is stable.

The landing site uses Astro with Tailwind. Build is `astro build`. Dev is `astro dev`. Static deployment to Netlify. No server-side rendering, no API routes, no database. Pure marketing site.

The CLAUDE.md captures three things that matter for the landing site specifically: the Astro component structure (which layouts wrap which pages), the Tailwind config customizations (custom brand colors, spacing scale), and the deployment pipeline (push to main triggers Netlify build). A new developer -- or a future Claude session -- can go from zero context to productive in under two minutes.

Every project gets this file now. The overhead is 15 minutes. The payoff is every subsequent session starting warm instead of cold.

## The Reseller Page

The white-label reseller page was the one net-new addition that survived every iteration. Agencies and MSPs want to offer AI agent services under their own brand. They do not want to explain Vertex AI to their clients. They want a product they can slap their logo on and sell.

The reseller page lays out the model: minimum 10-seat commitment, custom subdomain, their branding on the dashboard, our infrastructure underneath. Technical integration requires a single API key swap and a DNS CNAME record. No code changes on the reseller side.

This page generates more inbound interest than the main product page. Agencies already have the client relationships. They need the product. That signal was useful -- it reframed Intent Solutions from "sell to end users" toward "sell through partners."

## Lessons from the Back-and-Forth

The branding reversal looks like wasted work. It wasn't. The three hours of model-agnostic positioning produced the `/learn` section, the Vertex vs n8n comparison, and the reseller page. All three survived the reversal. The pricing education content is permanently useful regardless of how the hero section reads.

Product positioning is iterative and looks messy from the commit log. Remove branding, add branding, change tagline, revert tagline. Each iteration sharpens the message even if the diff looks like thrashing.

The real mistake would have been shipping the model-agnostic version without testing the emotional response. Flat messaging that nobody remembers is worse than specific messaging that some people reject. Specificity is a feature, not a limitation.

---

**Related Posts:**
- [Productizing AI Agents: Containerized Offerings and Iteration Loops](/posts/productizing-ai-agents-containerized-offerings-iteration-loop/) -- The containerization and pricing decisions that informed this positioning
- [Marketing Automation and Pricing Exploration](/posts/marketing-automation-project-pricing-exploration/) -- Earlier pricing model experiments
