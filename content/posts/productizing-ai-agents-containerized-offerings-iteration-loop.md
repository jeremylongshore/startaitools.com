+++
title = 'Productizing AI Agents: Containerized Offerings and the 9-Commit Iteration Loop'
slug = 'productizing-ai-agents-containerized-offerings-iteration-loop'
date = 2025-10-26T10:00:00-05:00
draft = false
tags = ["ai-agents", "product-design", "landing-pages", "iteration", "astro"]
categories = ["Technical Deep-Dive"]
description = "Building a containerized AI agents page with tiered pricing, then watching it go through a classic build-promote-revert-refine cycle across 9 commits in one evening session."
+++

Sunday evening. 9 PM. I had three AI agent concepts that worked in demos but had no public packaging. By 11 PM I had a product page, had promoted it to hero position, reverted that decision, and repositioned the entire offering for a different market. Nine commits. The git log reads like a product strategy argument with yourself.

## The Starting Point: Agents Without a Home

The Intent Solutions landing site had service offerings, but the AI agents existed only as internal prototypes. LinkedIn Outbound automation. Meeting intelligence summarization. Customer support triage. Each worked. None had pricing, packaging, or a public page.

The gap between "this works" and "you can buy this" is wider than most engineers think. A working agent needs to become a product — with tiers, pricing anchors, deployment expectations, and a clear target buyer.

## Building the Agents Page

The first commit was the largest. 355 insertions. An `/agents` page in Astro with three containerized offerings:

**LinkedIn Outbound Agent** — $197/mo (Self-Serve) to $647/mo (Custom)
- Automated prospect research and outreach sequencing
- CRM sync, response classification, handoff rules

**Meeting Intelligence Agent** — $97/mo to $297/mo
- Real-time transcription, action item extraction, follow-up generation
- Calendar integration, attendee matching, sentiment tracking

**Customer Support Triage Agent** — $147/mo to $497/mo
- Ticket classification, routing, auto-response for known patterns
- Escalation rules, SLA tracking, knowledge base suggestions

Each agent had three tiers: Self-Serve (you configure it), Managed (we configure it), and Custom (we build it around your workflow). The tiered structure does double duty — it's a pricing ladder and a qualification filter. Self-serve buyers validate themselves. Custom buyers signal budget.

The page structure:

```astro
---
// /agents page component
const agents = [
  {
    name: "LinkedIn Outbound",
    tagline: "Prospect research and outreach on autopilot",
    tiers: [
      { name: "Self-Serve", price: 197, features: [...] },
      { name: "Managed",    price: 397, features: [...] },
      { name: "Custom",     price: 647, features: [...] },
    ]
  },
  // Meeting Intelligence, Support Triage...
];
---

<Layout title="AI Agents | Intent Solutions">
  {agents.map(agent => (
    <AgentCard agent={agent} />
  ))}
</Layout>
```

Nothing exotic. The interesting part wasn't the code — it was what happened next.

## The Promotion-Reversion Cycle

Commit 4 promoted the agents to hero position on the homepage. Full-width featured card. ROI stats badge ("247% ROI in 90 days"). Deploy time badges. The agents page was now the first thing visitors saw.

```astro
<!-- Hero treatment: full-width featured card -->
<div class="hero-offering">
  <h2>AI Agents — Deploy in Days</h2>
  <div class="stats-row">
    <span class="badge">247% ROI in 90 days</span>
    <span class="badge">Deploy in 48 hours</span>
  </div>
  <a href="/agents">Explore Agents →</a>
</div>
```

Commit 5 reverted it. Back to the uniform 4-column grid. 9 insertions, 44 deletions.

Why? The hero treatment broke the visual hierarchy of the homepage. Intent Solutions offers more than agents — there are consulting engagements, platform builds, data engineering projects. Elevating one offering above the others made the site look like an agent company that also does consulting, rather than a solutions company that also deploys agents.

This is the kind of decision you can only make by seeing it live. The mockup in your head always looks right. The deployed version tells the truth.

## The Refinement Sequence

After reverting the layout, the next four commits refined the copy:

1. **Restore original header** — "Explore Tailored Build Paths" instead of the agents-focused headline. The homepage needed to stay general.
2. **Update `/agents` headlines with brand voice** — The agents page itself still needed personality. Generic SaaS copy got replaced with language that matched the rest of the site.
3. **Change headline to "Solutions Delivered"** — Moving from feature-speak to outcome-speak. Nobody buys an agent. They buy solved problems.
4. **Reposition for service businesses** — The biggest shift. The original copy targeted tech companies. The final version targeted service businesses: law firms worried about client meeting follow-through, agencies losing CRM accuracy, consultancies drowning in support tickets.

That last commit changed the competitive frame entirely. Tech companies can build their own agents. Service businesses cannot and will not. The willingness to pay is fundamentally different.

## What the Iteration Pattern Teaches

Nine commits in under two hours. The git log:

```
e84573e feat: reposition agents for service businesses
63ca720 fix: change headline to 'solutions delivered'
e9e0df9 feat: update /agents page headlines with brand
bb078bf fix: restore original 'explore tailored build paths' header
6aed5d1 fix: revert to uniform card layout
5e6fd1f feat: make AI Agents the hero offering on home page
2905bf8 fix: update home page AI Agents card link
9325d02 fix: restore original hero heading
5d01f63 feat: add AI agents page with containerized offerings
```

Read it bottom to top: build, fix a link, fix a heading, promote to hero, revert promotion, restore original layout, refine copy, refine copy again, reposition for target market.

Three patterns worth noting:

**1. Build first, position second.** The page existed before I figured out where it belonged in the site hierarchy. Trying to solve placement and content simultaneously leads to neither being right.

**2. Reverts are data, not failures.** Commits 4 and 5 look like wasted work. They weren't. Seeing the hero treatment live confirmed that the homepage needed to stay neutral. That's a product decision you can't make in a text editor.

**3. Target market is the last thing you nail.** The first version targeted tech companies because that's who I talk to most. The final version targeted service businesses because that's who would actually pay. The copy changed four times before the target market felt right.

## The Containerized Offering Model

The tiered pricing structure is worth examining separately. Each agent ships as a "container" — not a Docker container (though that's how they deploy), but a conceptual container with defined boundaries:

| Tier | You Do | We Do | Price Range |
|------|--------|-------|-------------|
| Self-Serve | Configure, maintain, monitor | Provide the agent + docs | $97-197/mo |
| Managed | Use it | Configure, maintain, monitor | $297-397/mo |
| Custom | Describe your workflow | Everything | $497-647/mo |

The Self-Serve tier exists primarily to anchor the price. Most service businesses will self-select into Managed because they don't want to configure AI agents. The Custom tier exists for enterprise conversations where the stated price is a starting point.

This is standard SaaS pricing psychology applied to agent deployment. The difference is that agents have ongoing operational costs (API calls, compute, monitoring) that vary by usage, so the tiers need to account for that variance without exposing per-call billing to non-technical buyers.

The "containerized" framing matters. When you say "AI agent," a technical buyer hears "thing I need to integrate, monitor, and maintain." When you say "containerized solution," a non-technical buyer hears "thing that works inside a boundary I understand." The container metaphor — defined inputs, defined outputs, defined cost — maps to how service businesses already think about vendor relationships. They don't want to understand the agent. They want to understand the contract.

## Outcome

By 11 PM, the Intent Solutions site had a live `/agents` page with three productized AI offerings, correctly positioned in the homepage grid (not as hero), targeted at service businesses, with three-tier pricing. The hero heading was back to the original brand voice. Nine commits, zero PRs, shipped.

The page exists to convert a specific visitor: a service business owner who's heard about AI agents, doesn't know how to build one, and wants to see a price before booking a call. Every copy decision in those final four commits optimized for that person.

---

*Related posts:*
- [IAE Product Architecture: A2A Protocol and Modular Pricing](/posts/iae-product-architecture-a2a-framework-modular-pricing/) — The technical architecture behind agent productization
- [Engine to Product: Three Interfaces, One Codebase](/posts/engine-to-product-three-interfaces-one-codebase/) — Another build-to-product transition story
- [Three Projects, Two Reverts, One Day](/posts/three-projects-two-reverts-one-day/) — More revert-driven development
