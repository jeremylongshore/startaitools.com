+++
title = 'Vertex AI Agent Engine Forced a Same-Day Architecture Pivot'
slug = 'pipelinepilot-vertex-ai-migration-architecture-pivot'
date = 2025-11-01T10:00:00-06:00
draft = false
tags = ["vertex-ai", "google-adk", "agent-engine", "architecture", "pipelinepilot", "ci-cd", "firebase"]
categories = ["Technical Deep-Dive"]
description = "Agent Engine cannot run multiple non-search tools on a single agent. That undocumented limitation forced a same-day collapse from 4 specialized agents to 1 orchestrator carrying all tools."
+++

## The Plan That Died on Deployment

PipelinePilot had a clean four-agent architecture. Orchestrator routes to Research, Enrichment, and Outreach. Each agent owns its tools. Each agent has a single responsibility. The Python ADK migration from YAML was already done. CI passed. Local tests passed.

Then I deployed to Vertex AI Agent Engine and the entire multi-agent topology fell apart.

Agent Engine cannot have multiple non-search tools on a single agent.

That sentence took me hours to discover. The documentation does not say this. No error message says this clearly. The agent deploys. It accepts requests. Then it silently ignores tools or throws cryptic errors when the orchestrator tries to route to a sub-agent carrying two custom tools.

## What the Limitation Actually Looks Like

Here's the four-agent topology I deployed:

```
Orchestrator (classify_intent, select_stage, validate_arv)
├── Research Agent (search_companies, search_contacts)
├── Enrich Agent (enrich_apollo, enrich_clearbit, enrich_zoominfo)
└── Outreach Agent (generate_sequence, schedule_delivery)
```

Research Agent works. It only has search-type tools. Agent Engine treats search tools differently from custom function tools.

Enrich Agent fails silently. Three custom function tools. Agent Engine only binds the first one and ignores the rest. No warning. No error log. The agent responds but only ever calls `enrich_apollo`, even when explicitly instructed to use ZoomInfo.

I spent two hours thinking this was a prompt engineering problem. Rewrote instructions. Added explicit tool selection logic. Nothing changed. The agent would acknowledge the instruction and then call the same tool again.

## The Debugging Timeline

**10:00 AM** -- Deploy four-agent topology. Orchestrator routes correctly. Research agent returns results. Ship it.

**10:45 AM** -- QA the enrichment pipeline. Enrich agent only calls Apollo regardless of instruction. Assume prompt issue.

**11:30 AM** -- Rewrite enrich agent instructions three times. Add explicit `TOOL SELECTION RULES` block. Same behavior.

**12:15 PM** -- Strip the agent down to one tool. It works. Add a second tool. First tool still works, second never fires. Third tool never fires.

**12:30 PM** -- Test with the outreach agent. Same pattern. Two tools, only the first one activates.

**12:45 PM** -- Search the ADK docs. Nothing. Search the Agent Engine API reference. Nothing. Search GitHub issues. One thread from two weeks ago describing similar behavior. No official response.

**1:00 PM** -- Accept reality. Agent Engine imposes a constraint the docs don't mention: one custom function tool per agent. Search tools (Google Search, Vertex AI Search) are exempt. Custom `FunctionTool` instances are not.

## The Forced Architecture

The only viable path: collapse everything into a single orchestrator carrying all tools. No sub-agents. One agent with every function registered.

```python
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

orchestrator = Agent(
    name="pipeline_orchestrator",
    model="gemini-2.0-flash",
    instruction="""You are PipelinePilot. You manage the entire SDR pipeline.

ROUTING RULES:
- Prospect discovery: use search_companies and search_contacts
- Enrichment: use enrich_apollo, enrich_clearbit, enrich_zoominfo
  - Try Apollo first, fall back to Clearbit, then ZoomInfo
  - Stop when confidence >= 0.85
- Outreach: use generate_sequence only after enrichment passes ARV
- ALWAYS validate_arv before generating any outreach

HARD CONSTRAINTS:
- Never generate outreach for accounts below ARV threshold
- Log every tool call for audit trail
- If enrichment confidence < 0.70, flag for human review
""",
    tools=[
        FunctionTool(search_companies),
        FunctionTool(search_contacts),
        FunctionTool(enrich_apollo),
        FunctionTool(enrich_clearbit),
        FunctionTool(enrich_zoominfo),
        FunctionTool(validate_arv),
        FunctionTool(generate_sequence),
        FunctionTool(schedule_delivery),
    ],
)
```

Eight tools on one agent. This is the opposite of good agent design. Every agent architecture guide says: keep agents focused, give each one a small tool surface, let the orchestrator coordinate.

Agent Engine does not care about your architecture guide.

## What Gets Lost

**Separation of concerns.** A monolithic agent with eight tools can call any tool at any time. The only thing preventing the agent from calling `generate_sequence` before enrichment is the instruction prompt. In the four-agent design, the outreach agent literally could not access enrichment tools. The constraint was structural, not aspirational.

**Testability.** Four agents means four test suites, each with a narrow tool surface. One agent means one massive test suite covering every tool interaction. The combinatorial explosion of "which tool gets called when" is much harder to verify.

**Audit clarity.** With sub-agents, the audit log shows which agent handled which phase. With one agent, every action comes from "pipeline_orchestrator." You lose the natural tracing boundary.

## What Gets Gained

**It actually works.** The single-agent deployment processes requests end to end. All eight tools fire when appropriate. The prompt engineering for tool selection is heavier, but Gemini 2.0 Flash handles it well enough in practice.

**Simpler deployment.** One agent to deploy, one agent to monitor, one agent to update. The four-agent deployment required coordinating versions across sub-agents and verifying inter-agent communication on every deploy.

**Lower latency.** No orchestrator-to-sub-agent routing overhead. The single agent decides and acts in one inference pass instead of multiple.

## Policy Enforcement via CI

With the structural tool isolation gone, I built policy.yml enforcement in CI to compensate. The policy file defines which tools are allowed in which pipeline stages:

```yaml
# policy.yml
stages:
  discovery:
    allowed_tools: [search_companies, search_contacts]
    required_before: [enrichment]
  enrichment:
    allowed_tools: [enrich_apollo, enrich_clearbit, enrich_zoominfo]
    required_before: [outreach]
    gates:
      - validate_arv
  outreach:
    allowed_tools: [generate_sequence, schedule_delivery]
    requires: [enrichment.confidence >= 0.70]
```

A CI check parses the policy file and validates that the agent's instruction prompt references the correct tool ordering. It also runs integration tests that assert stage dependencies: outreach tests fail if enrichment has not been called first.

This is duct tape over a missing platform feature. But it works, and it catches regressions before they reach Agent Engine.

## The Documentation Gap

I wrote 10+ docs for this project in a single day. Migration audit, ADR, AAR, policy enforcement spec, deployment runbook. When the platform does not document its limitations, you document them yourself.

The ADR for this pivot has one key sentence: "Agent Engine's multi-tool constraint is not a bug to be fixed. It is a platform assumption to be designed around."

The AAR is harsher. The key lesson: always deploy to the target platform before finalizing architecture. I spent a week designing a four-agent topology that only worked locally. One deployment to Agent Engine would have surfaced this constraint on day one.

## The Firebase Dashboard

The dashboard deployment was the one thing that went smoothly. Firebase Hosting, Firestore for state, Firebase Auth for access control. The dashboard shows pipeline status, agent activity, and per-tenant usage metrics.

With the single-agent architecture, the dashboard's activity feed is simpler. One agent, one stream of events. No inter-agent routing visualization needed. The architecture constraint accidentally simplified the UI.

## Key Takeaways

**Deploy to your target platform before you finalize architecture.** Local testing with `adk web` does not surface Agent Engine's constraints. The multi-tool limitation only appears on actual deployment.

**When the platform constrains your architecture, document the constraint formally.** An ADR that says "we collapsed to one agent because of platform limitation X" is invaluable for the next developer who tries to refactor back to multi-agent.

**CI policy enforcement compensates for lost structural constraints.** If you can't enforce tool isolation through agent boundaries, enforce it through automated tests and policy files.

**Undocumented limitations are the most expensive kind.** Two hours of debugging a "prompt engineering problem" that was actually a platform constraint. The total cost of this discovery: half a day of work plus a complete architecture rethink.

---

**Related Posts:**
- [PipelinePilot: Building a Multi-Agent SDR Orchestrator on Vertex AI](/posts/pipelinepilot-multi-agent-sdr-orchestrator-vertex-ai/) -- The initial build that established the four-agent architecture
- [How to Get an ADK Agent into Google's Community Showcase](/posts/how-to-get-adk-agent-into-google-community-showcase/) -- ADK deployment patterns and Google ecosystem integration
- [IAE Product Architecture: A2A Framework with Modular Pricing](/posts/iae-product-architecture-a2a-framework-modular-pricing/) -- The broader product architecture context for agent systems
