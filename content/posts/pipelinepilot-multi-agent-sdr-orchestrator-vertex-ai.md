+++
title = 'PipelinePilot: Building a Multi-Agent SDR Orchestrator on Vertex AI in One Day'
slug = 'pipelinepilot-multi-agent-sdr-orchestrator-vertex-ai'
date = 2025-10-31T10:00:00-05:00
draft = false
tags = ["vertex-ai", "multi-agent-systems", "google-adk", "sdr-automation", "sales-engineering", "firebase", "ci-cd"]
categories = ["Technical Deep-Dive"]
description = "From YAML agent configs to Python ADK: building a production multi-agent SDR orchestrator on Vertex AI with Firebase dashboard, 6 data connectors, and CI/CD in a single day."
+++

## The Problem Nobody Talks About

Sales development pipelines are stitched together with duct tape. A typical SDR stack looks like this: Apollo for contact discovery, ZoomInfo for enrichment, a CRM for tracking, a sequencing tool for outreach. Each one has its own login, its own API, its own data model. The SDR spends half their day copying data between tabs.

The answer isn't another SaaS integration platform. It's agents that own the workflow end to end.

PipelinePilot is a multi-tenant SDR orchestrator built on Google Vertex AI. An orchestrator coordinates three specialist agents — research, enrichment, and outreach — with an ARV (Account Revenue Validation) framework gating the pipeline between stages. I built the entire system — scaffold, agents, connectors, dashboard, CI/CD — in one day. 18 commits. 12,000+ insertions across 80+ files.

This post covers the real engineering journey, including the critical decision to abandon YAML agents and migrate to Python ADK mid-project.

## Phase 1: The YAML Agent Scaffold

The first commit was the full MVP scaffold. Dockerfile, CI/CD pipeline, Firestore utilities, Secret Manager integration, billing/usage/tenant/export modules, six operational docs. 4,302 insertions across 29 files. The foundation.

For the agents themselves, I started with YAML configurations — the same pattern I'd used on BrightStream. Four agents defined declaratively:

```yaml
# agents/orchestrator.yaml
name: orchestrator
agent_class: LlmAgent
model: gemini-2.0-flash
description: Routes SDR pipeline tasks to specialist agents

instruction: |
  You are the PipelinePilot orchestrator. You coordinate the SDR pipeline:
  1. Receive prospect lists or campaign briefs
  2. Route to research_agent for company/contact discovery
  3. Route to enrich_agent for data enrichment via connectors
  4. Route to outreach_agent for personalized sequence generation
  
  ROUTING RULES:
  - New prospects → research_agent first
  - Known contacts needing data → enrich_agent
  - Enriched contacts ready for outreach → outreach_agent
  - Always validate ARV before outreach generation

sub_agents:
  - research_agent
  - enrich_agent
  - outreach_agent

tools:
  - name: pipeline_tools
```

Six data connectors backed the enrichment agent: Apollo, Clay, Clearbit, Crunchbase, SalesNavigator, ZoomInfo. Each connector normalized its response into a unified contact schema so agents didn't need to know which source provided what.

I also built an ARV (Account Revenue Validation) framework. Before the outreach agent generates a single email, the system validates that the target account meets minimum revenue thresholds. No point burning agent compute on prospects that don't qualify.

This worked. Agents routed correctly. The newsfeed demo proved the orchestration pattern. But within hours, I hit the wall.

## Why YAML Agents Weren't Enough

Three problems surfaced fast:

**1. No conditional logic.** YAML agents route based on static rules in the instruction prompt. But SDR workflows need branching: if Apollo returns no results, try Clearbit. If enrichment confidence is below 70%, flag for human review. You can describe this in the instruction, but the LLM interprets it inconsistently.

**2. No tool composition.** Each YAML agent gets a flat list of tools. I needed the enrich agent to call Apollo, check the result, then conditionally call ZoomInfo — within a single turn. YAML doesn't express that. You end up making the LLM orchestrate tool calls through prompt engineering alone.

**3. No testable units.** YAML configs aren't code. You can't unit test an agent's routing logic. You can't mock a connector response and verify the agent handles a partial failure. The only testing path is end-to-end, which is slow and flaky.

The YAML approach works for simple orchestration. For production SDR pipelines with six data sources and conditional enrichment chains, it's the wrong abstraction.

## Phase 2: The Python ADK Migration

The migration was a complete rewrite. 2,165 insertions, 289 deletions. New orchestrator, research, enrich, and outreach agents — all in Python using Google's Agent Development Kit.

Here's what the orchestrator looks like after migration:

```python
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from tools.routing import classify_intent, select_pipeline_stage
from tools.arv import validate_account_revenue
from agents.research import research_agent
from agents.enrich import enrich_agent
from agents.outreach import outreach_agent


orchestrator = Agent(
    name="pipeline_orchestrator",
    model="gemini-2.0-flash",
    instruction="""You are PipelinePilot's orchestrator. You manage the SDR pipeline.

DECISION FRAMEWORK:
1. Classify the inbound request (new prospect, enrichment, outreach)
2. Validate account revenue before any outreach generation
3. Route to the correct specialist agent
4. Synthesize results and report back

HARD RULES:
- Never generate outreach for accounts below ARV threshold
- Always enrich before outreach — no cold sequences on partial data
- Log every routing decision for audit trail
""",
    sub_agents=[research_agent, enrich_agent, outreach_agent],
    tools=[
        FunctionTool(classify_intent),
        FunctionTool(select_pipeline_stage),
        FunctionTool(validate_account_revenue),
    ],
)
```

The difference is structural. Python agents compose tools programmatically. The enrich agent can now do this:

```python
async def enrich_contact(contact_id: str, sources: list[str]) -> dict:
    """Enrich a contact by querying multiple data sources with fallback."""
    results = {}
    confidence = 0.0

    for source in sources:
        connector = CONNECTOR_REGISTRY[source]
        try:
            data = await connector.fetch(contact_id)
            results[source] = data
            confidence = max(confidence, data.get("confidence", 0.0))
            if confidence >= 0.85:
                break  # Good enough, stop burning API calls
        except ConnectorError as e:
            results[source] = {"error": str(e), "status": "failed"}
            continue  # Try next source

    return {
        "contact_id": contact_id,
        "enrichment": results,
        "confidence": confidence,
        "sources_queried": len(results),
        "needs_review": confidence < 0.70,
    }
```

This is real code. It has early exit logic. It has fallback behavior. It flags low-confidence results for human review. None of this is possible in a YAML instruction block — not reliably.

## The CI/CD Pipeline

Two GitHub Actions workflows gate every merge:

**ADK Guard** runs on every PR. It validates agent configurations, checks tool function signatures against the ADK schema, and runs the unit test suite. If an agent references a tool that doesn't exist, the PR fails.

**ARV Gate** validates the revenue validation framework itself. It runs synthetic prospect data through the ARV pipeline and asserts that accounts below threshold are correctly rejected. This catches regressions in the qualification logic before they reach production.

```yaml
# .github/workflows/adk-guard.yml
name: ADK Guard
on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install google-adk pytest
      - run: python -m pytest tests/agents/ -v
      - run: python -m pytest tests/arv/ -v

  deploy-check:
    runs-on: ubuntu-latest
    needs: validate
    steps:
      - uses: actions/checkout@v4
      - uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.SA_EMAIL }}
      - run: |
          adk deploy agent_engine \
            --project=${{ secrets.GCP_PROJECT }} \
            --region=us-central1 \
            --dry-run \
            ./agents/orchestrator.py
```

Production deployment uses Workload Identity Federation — no service account keys stored in GitHub. The deploy job authenticates through WIF, runs a dry-run validation, then deploys to Vertex AI Agent Engine.

## The Firebase Dashboard

Agents without a UI are agents nobody uses. The dashboard commit was the biggest single change: 5,604 insertions across 29 files. Next.js frontend with Firebase Auth and Firestore integration.

What it provides:

- **Campaign management.** Create outreach campaigns, assign prospect lists, monitor pipeline progress.
- **Agent activity feed.** Real-time view of which agents are running, what they're processing, routing decisions made.
- **Settings and API keys.** Tenant-level configuration for data connector credentials (Apollo API key, ZoomInfo credentials). Encrypted at rest via Secret Manager.
- **Usage and billing.** Per-tenant tracking of agent invocations, connector API calls, and compute time.

The dashboard talks to Firestore, which the agents also write to. When the enrich agent completes a contact enrichment, it writes the result to `tenants/{tenantId}/contacts/{contactId}`. The dashboard picks it up in real time through Firestore's snapshot listeners. No polling. No webhooks. Just shared state.

## Migration Audit and Decision Record

I wrote a formal ADR (Architecture Decision Record) for the YAML-to-ADK migration and a migration AAR (After Action Review). This matters for a multi-tenant system. Future developers need to understand *why* the YAML agents were abandoned, not just that they were.

The ADR captures three things:

1. **Context.** YAML agents worked for simple orchestration but couldn't express conditional enrichment logic.
2. **Decision.** Migrate to Python ADK for testability, composability, and programmatic tool control.
3. **Consequences.** Higher initial complexity. Requires Python expertise. But gains unit testability, connector fallback logic, and proper error handling.

The AAR is blunter: what went well (fast scaffold, clean separation of concerns), what didn't (underestimated the YAML limitations upfront), what to do differently (start with Python ADK for any pipeline with more than two data sources).

## What This Architecture Enables

PipelinePilot is multi-tenant by design. Each tenant gets:

- Isolated Firestore collections
- Separate Secret Manager entries for API keys
- Per-tenant usage metering
- Independent agent configurations (different ARV thresholds, different connector priorities)

One deployment serves multiple SDR teams. The orchestrator reads tenant config at runtime and adjusts routing, enrichment source priority, and outreach templates accordingly.

The four-agent architecture is deliberately narrow. Research, enrich, validate, generate. Each agent has a single responsibility and clear input/output contracts. Adding a fifth agent (say, a CRM sync agent) means implementing one Python class and registering it with the orchestrator. The scaffold supports it without architectural changes.

## Key Takeaways

**Start with YAML only if your orchestration is linear.** If agents need conditional logic, fallback chains, or tool composition — go straight to Python ADK.

**ARV validation is non-negotiable.** Agents will happily generate outreach for garbage prospects. Build the qualification gate early and enforce it in CI.

**Multi-tenancy is an architecture decision, not a feature.** PipelinePilot was multi-tenant from commit one. Retrofitting tenant isolation into a single-tenant agent system is painful.

**Ship the dashboard with the agents.** An SDR orchestrator without a UI is a demo. The Firebase dashboard took one commit but turned the project from "interesting prototype" into "deployable product."

## Related Posts

- [Building a Production Multi-Agent AI System: BrightStream's 10-Agent Architecture on Vertex AI](/posts/building-production-multi-agent-ai-brightstream-vertex-ai/) — The predecessor project that established the YAML agent pattern
- [Architecting Production Multi-Agent AI Platform - Technical Leadership](/posts/architecting-production-multi-agent-ai-platform-technical-leadership/) — Platform-level architecture decisions for multi-agent systems
- [Building Idempotent Stripe Billing Enforcement in Firestore](/posts/building-idempotent-stripe-billing-enforcement-firestore/) — Billing patterns used in PipelinePilot's usage metering
