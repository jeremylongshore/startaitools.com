+++
title = 'IAE Product Architecture: Building a Sellable AI Agent with A2A Protocol and Modular Pricing'
slug = 'iae-product-architecture-a2a-framework-modular-pricing'
date = 2025-10-27T10:00:00-05:00
draft = false
tags = ["a2a", "ai-agents", "product-architecture", "google-cloud", "pricing", "vertex-ai"]
categories = ["Technical Deep-Dive"]
description = "How we turned a consulting-shaped AI agent into a product with Google A2A Protocol, two-layer architecture, and modular M1/M2/M3 pricing that sells."
+++

Most AI agent projects die as consulting engagements. Someone builds a custom workflow, charges hourly, and the moment they stop touching it, the client churns. The agent was never a product — it was a service wearing a product's clothes.

I spent the last week turning our intelligence agent into something with a SKU. The result is the Intent Agent Engine (IAE): a two-layer architecture built on Google's A2A Protocol, with modular pricing that lets customers buy exactly the capability they need. Here's how the architecture decisions drove the pricing, and why the obvious approach — one agent, one price — would have killed the business.

## The Problem: AI Agents Are Hard to Productize

The default path for an AI agent startup looks like this:

1. Build a powerful agent that does everything
2. Price it as a monthly subscription
3. Watch customers churn because they're paying for capabilities they don't use
4. Slide into custom consulting to keep revenue alive

The root cause is architectural. A monolithic agent forces monolithic pricing. If the intelligence layer (research, scoring, recommendations) is welded to the execution layer (outbound, CRM updates, follow-ups), you can't sell them independently. Every customer pays for the full stack whether they need it or not.

We needed to separate concerns at the architecture level so the pricing could follow.

## The Approach: Two-Layer Architecture on A2A

Google's [Agent-to-Agent (A2A) Protocol](https://google.github.io/A2A/) gave us the contract layer we needed. Instead of one agent that does everything, we split into two cooperating agents with a clean protocol boundary:

```
┌─────────────────────────────────────────────┐
│              IAE Platform (A2A)              │
│                                              │
│  ┌──────────────────┐  ┌─────────────────┐  │
│  │ Intelligence Agent│  │ Automation Agent │  │
│  │   (Model 1)       │  │   (Model 2)      │  │
│  │                    │  │                   │  │
│  │ • ICP Scoring      │──│ • Email Sequences │  │
│  │ • Market Research  │  │ • CRM Updates     │  │
│  │ • Lead Enrichment  │  │ • Follow-up Logic │  │
│  │ • Signal Detection │  │ • Calendar Booking│  │
│  └──────────────────┘  └─────────────────┘  │
│            │                     │            │
│            └──────┬──────────────┘            │
│                   │                           │
│         A2A Protocol (JSON-RPC)               │
└─────────────────────────────────────────────┘
```

The Intelligence Agent researches and scores. The Automation Agent acts on those scores. They communicate over A2A's JSON-RPC transport, which means either agent can be replaced, upgraded, or sold independently.

### Why Not a Single Agent?

A single agent with both capabilities sounds simpler. It is — until you try to price it, scale it, or explain it.

**Pricing problem**: A customer who only needs lead intelligence shouldn't subsidize the execution infrastructure. With a monolithic agent priced at $3,000/mo, you lose every deal where the buyer only needs half the capability.

**Scaling problem**: Intelligence workloads are bursty (batch research runs) while automation workloads are steady (drip campaigns). Coupling them means you scale infrastructure for the peak of both simultaneously.

**Trust problem**: Customers adopt intelligence before automation. They want to see the scores and recommendations before they let an agent send emails on their behalf. A single agent forces an all-or-nothing adoption curve.

## The Google Cloud Stack

The full IAE runs on Google Cloud, chosen for Vertex AI's managed Anthropic Claude access and native A2A support:

```toml
# IAE Infrastructure Map
[intelligence_layer]
  llm        = "Vertex AI (Anthropic Claude)"
  datastore  = "Firestore"
  analytics  = "BigQuery"
  compute    = "Cloud Run"

[automation_layer]
  orchestration = "Cloud Functions"
  messaging     = "Pub/Sub"
  scheduling    = "Cloud Scheduler"
  compute       = "Cloud Run"

[shared]
  auth       = "Firebase Auth"
  monitoring = "Cloud Monitoring"
  protocol   = "A2A over Cloud Run endpoints"
```

Each layer gets its own Cloud Run service. The Intelligence Agent is a stateless scorer — it takes a company domain, enriches it, and returns a structured score. The Automation Agent subscribes to Pub/Sub topics that the Intelligence Agent publishes to. Clean decoupling, no shared state beyond the message bus.

## ICP Scoring: The Intelligence Core

The heart of Model 1 is the Ideal Customer Profile (ICP) scoring engine. This is the piece that makes the intelligence layer worth buying on its own:

```python
from dataclasses import dataclass
from enum import Enum

class SignalStrength(Enum):
    STRONG = 3
    MODERATE = 2
    WEAK = 1
    NONE = 0

@dataclass
class ICPScore:
    company: str
    total_score: float
    signals: dict[str, SignalStrength]
    recommendation: str
    confidence: float

def score_lead(company_data: dict) -> ICPScore:
    """Score a lead against ICP criteria.

    Weights are calibrated from closed-won analysis:
    - Tech stack fit: 30%  (do they use tools we integrate with?)
    - Company size:   25%  (10-500 employees sweet spot)
    - Growth signals: 25%  (hiring, funding, product launches)
    - Intent signals: 20%  (job posts mentioning AI, visiting pricing pages)
    """
    weights = {
        "tech_stack_fit": 0.30,
        "company_size":   0.25,
        "growth_signals":  0.25,
        "intent_signals":  0.20,
    }

    signals = {}
    signals["tech_stack_fit"] = _evaluate_tech_stack(company_data)
    signals["company_size"] = _evaluate_size(company_data)
    signals["growth_signals"] = _evaluate_growth(company_data)
    signals["intent_signals"] = _evaluate_intent(company_data)

    total = sum(
        signals[k].value * weights[k]
        for k in weights
    )
    # Normalize to 0-100
    max_possible = sum(
        SignalStrength.STRONG.value * w for w in weights.values()
    )
    normalized = (total / max_possible) * 100

    return ICPScore(
        company=company_data["domain"],
        total_score=normalized,
        signals=signals,
        recommendation=_get_recommendation(normalized),
        confidence=_calculate_confidence(signals),
    )

def _get_recommendation(score: float) -> str:
    if score >= 75:
        return "PRIORITY_OUTREACH"
    elif score >= 50:
        return "NURTURE_SEQUENCE"
    elif score >= 25:
        return "MONITOR"
    return "DISQUALIFY"
```

The weights came from analyzing our own closed-won deals. Tech stack fit matters most because integration friction kills deals faster than anything else. A company already running on Google Cloud with Firestore and BigQuery can adopt IAE in days, not weeks.

The scoring function is deterministic — same input, same output. That matters for auditability. When a customer asks "why did you recommend outreach to this company?", the signal breakdown gives a concrete answer, not a black-box confidence score.

## Modular Pricing: M1/M2/M3

With the architecture split clean, the pricing follows naturally:

```
┌─────────────────────────────────────────────────────────┐
│                   IAE Pricing Models                     │
├──────────────┬──────────────┬──────────────┬────────────┤
│   Model 1    │   Model 2    │   Model 3    │  Full Stack│
│  Intelligence│  Execution   │   Support    │   Bundle   │
│    Core      │    Layer     │ Intelligence │            │
├──────────────┼──────────────┼──────────────┼────────────┤
│ $1,497/mo    │ $1,997/mo    │ $997/mo      │ $2,997/mo  │
├──────────────┼──────────────┼──────────────┼────────────┤
│ ICP Scoring  │ Email Seqs   │ Ticket       │ Everything │
│ Lead Enrich  │ CRM Sync     │ Triage       │            │
│ Market Intel │ Follow-ups   │ Knowledge    │ 33% savings│
│ Signal Det.  │ Calendar     │ Base Mgmt    │ vs à la    │
│              │ Booking      │              │ carte      │
└──────────────┴──────────────┴──────────────┴────────────┘
```

**Model 1 (Intelligence Core) — $1,497/mo**: The scoring engine, enrichment pipeline, and signal detection. No execution. Customers get intelligence they can act on manually or feed into their existing tools.

**Model 2 (Execution Layer) — $1,997/mo**: Automated outbound, CRM updates, follow-up sequences. Requires M1 data as input (either through the bundle or via API).

**Model 3 (Support Intelligence) — $997/mo**: Customer support triage, knowledge base management, ticket routing. A third agent that plugs into the same A2A backbone.

**Full Stack Bundle — $2,997/mo**: All three models. The bundle price ($2,997) vs à la carte ($4,491) gives a 33% discount and a clear incentive to go all-in.

### The ROI Argument

A traditional SDR team costs roughly $50K/month when you factor in salaries, tools, and overhead. The Intel Engine detail page includes an ROI calculator that breaks this down:

- **Traditional SDR team**: ~$50K/mo (2-3 SDRs + tooling + management)
- **IAE Full Stack**: $2,997/mo
- **Savings**: ~$47K/mo (89% reduction)

That's the number that closes deals. Not "AI-powered intelligence" — a concrete dollar figure against a line item the buyer already has in their budget.

### Why Modular Beats Monolithic

The M1-only tier exists because most buyers aren't ready to hand execution to an AI agent on day one. They want to validate the intelligence first. M1 is the land, M2 is the expand. A monolithic $3,000/mo product forces the buyer to bet on both layers simultaneously, which raises the perceived risk and extends the sales cycle.

In practice, 60-70% of M1 customers add M2 within 90 days once they see the scoring accuracy. The modular structure turns a single high-stakes purchase into a two-step adoption with built-in proof points.

## What Actually Shipped

The week produced 12 commits across two repos:

- **68 files changed** in the landing site with 25,131 insertions — A2A framework documentation, executive summary, technical architecture docs, and a 6-week implementation roadmap
- **477-line Intel Engine detail page** with the ROI calculator
- **Full rebrand** from generic "Intel Engine" to "IAE (Intent Agent Engine)" with Google Cloud positioning
- **Excel Analyst Pro v1.0.0** shipped as a side release — 4 auto-invoked Skills (DCF, LBO, Variance, Pivot) with investment banking-grade templates and local Excel processing via MCP integration

The A2A documentation alone runs five core docs: executive summary, technical architecture, intelligence layer deep dive, production code samples, and the implementation roadmap. Overkill for a landing page? Maybe. But when an enterprise buyer's technical lead opens the docs section, they need to see production thinking, not marketing slides.

## Takeaways

**Architecture dictates pricing.** If you can't sell layers independently, your architecture is too coupled. Split the concerns first, then let pricing follow the seams.

**Intelligence before execution.** Customers trust AI recommendations before they trust AI actions. Give them an entry point that's read-only.

**ROI beats features.** "89% savings vs traditional SDR team" closes more deals than "powered by Vertex AI with A2A Protocol." Lead with the number.

---

### Related Posts

- [Hybrid AI Stack: Reduce AI API Costs by 60-80%](/posts/hybrid-ai-stack-reduce-costs-60-80-percent-intelligent-routing/) — The cost optimization architecture that informed IAE's infrastructure decisions
- [Building an Idempotent Stripe Billing Enforcement Engine](/posts/building-idempotent-stripe-billing-enforcement-firestore/) — How we handle subscription state for modular pricing tiers
- [Deploying Next.js 15 on Google Cloud Run](/posts/deploying-nextjs-15-google-cloud-run-custom-domain-ssl/) — The deployment pattern IAE's Cloud Run services follow
