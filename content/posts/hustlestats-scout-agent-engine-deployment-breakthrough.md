+++
title = 'Scout Agent Deployment Saga: Python SDK Fails, CLI Saves, REST API Discovered'
slug = 'hustlestats-scout-agent-engine-deployment-breakthrough'
date = 2025-11-19T10:00:00-06:00
draft = false
tags = ["vertex-ai", "agent-engine", "multi-agent-systems", "google-adk", "gemini", "debugging", "deployment", "firestore"]
categories = ["Technical Deep-Dive"]
description = "Deploying a multi-agent Scout team to Vertex AI Agent Engine: why the Python SDK returned 400, why the CLI worked, and the undocumented REST API that makes it production-ready."
+++

## The Scout Team

HustleStats needed intelligent scouting reports. Not template-filled stat summaries -- actual analysis that cross-references a player's stats against league averages, identifies trends, and produces recruiting-grade assessments.

The architecture: a Lead Scout orchestrator that delegates to four specialist agents.

- **Stats Logger** -- ingests raw game data, normalizes across different scoring formats, maintains per-player longitudinal records
- **Performance Analyst** -- computes percentile rankings within position groups, identifies statistically significant trends across a minimum 5-game window
- **Recruitment Advisor** -- maps player profiles to recruiting criteria for travel teams and club programs, surfaces fit scores
- **Benchmark Specialist** -- maintains league-wide and national percentile baselines, adjusts for age group and competition level

All five agents run Gemini 2.0 Flash. The Lead Scout uses function calling to delegate to specialists and synthesize their outputs into a single scouting report.

Local validation: 4 out of 5 test scenarios passed on the first run. The fifth failed on a edge case where the Stats Logger received game data with zero minutes played -- division by zero in the per-minute normalization. Fixed with a guard clause. Multi-agent delegation was working correctly. The Lead Scout routed tasks to the right specialists, collected responses, and produced coherent reports.

Then came deployment.

## The Python SDK Wall

Vertex AI Agent Engine is Google's managed runtime for ADK agents. You deploy an agent, get a resource name, and call it through the API. The Python SDK provides `agent_engines.create()` for deployment.

It returned a 400 error. No useful message. The request body looked correct -- agent module path, requirements, display name, all present. The error payload was a generic "Invalid argument" with no field-level detail.

I tried every permutation:

- Stripped the agent config to a single agent (no multi-agent delegation)
- Removed all custom tools
- Reduced to a bare `LlmAgent` with only a model and instruction
- Pinned every dependency version in requirements.txt
- Switched regions from `us-central1` to `us-east1`

Every attempt: 400. Same unhelpful error. The SDK's internal request serialization was doing something the API rejected, but the SDK didn't expose what it was actually sending.

I checked the SDK source code. The `create()` method serializes the agent configuration into a JSON payload and sends it inline in the request body. For simple single-agent configurations, this works. For multi-agent configurations with tool definitions, sub-agent references, and custom session handlers, the serialized payload exceeds what the API expects in an inline request.

## The CLI Breakthrough

Google's ADK ships a CLI tool: `adk deploy agent_engine`. Unlike the Python SDK's `create()` method, the CLI handles packaging, dependency resolution, and request serialization differently. Specifically, it creates a proper Cloud Storage staging bundle, uploads agent source as a zip, and references the staged artifact in the deployment request.

The Python SDK tries to inline the agent configuration. The CLI stages it externally.

```bash
adk deploy agent_engine \
  --project hustlestats-prod \
  --region us-central1 \
  --display_name "scout-lead" \
  --agent_module scout.lead_scout
```

It worked. First try. The agent deployed, got a resource name, showed up in the Vertex AI console. The multi-agent team was live.

The difference: the CLI's deployment path and the Python SDK's deployment path are not equivalent. They hit different internal code paths on the API side. The CLI's staging approach handles agent packaging that the SDK's inline approach cannot. This is not documented. I found it by reading the CLI's source code and noticing the staging step that the SDK skips.

## The Session Serialization Problem

Agent deployed. Time to call it. The first call worked -- a scouting report generated correctly through the multi-agent delegation chain. The second call, attempting to continue the same session, failed.

```
PicklingError: Can't pickle <class 'VertexAiSessionService'>: 
it's not the same object as google.adk.sessions.VertexAiSessionService
```

Vertex AI Agent Engine uses Firestore-backed sessions via `VertexAiSessionService`. When the agent runtime tries to serialize session state between turns, it attempts to pickle the session service object itself. Python's pickle module requires that the class reference at unpickle time matches the class reference at pickle time. If the module has been reloaded or imported through a different path, the identity check fails.

This is a known limitation of pickle-based serialization in long-running Python processes where module reloading can occur. The workaround: don't persist session state between calls. Treat each API call as stateless and pass relevant context in the request payload.

For the Scout team, this meant restructuring the scouting workflow. Instead of a multi-turn conversation where the Lead Scout progressively builds a report, each call receives the full context (player data, game history, league baselines) and produces a complete report in a single turn. Stateless by design.

This is arguably better architecture anyway. Stateful multi-turn agents are fragile in production. Network interruptions, agent restarts, and session expiration all create failure modes that stateless single-turn agents simply don't have. The context window of Gemini 2.0 Flash is large enough that passing full player histories per request is not a token budget problem. The trade-off is higher per-request cost (more input tokens) in exchange for zero session management complexity. For a scouting tool that generates reports on demand rather than maintaining long-running conversations, stateless wins.

## The REST API Discovery

The Python SDK and the CLI are both wrappers. The underlying API is REST. Finding the correct endpoints required reading Google's API discovery documents and testing with curl.

Two endpoints matter:

**Create a session:**

```
POST https://{region}-aiplatform.googleapis.com/v1beta1/projects/{project}/locations/{region}/agentEngines/{engine_id}:query

{
  "class_method": "async_create_session",
  "input": {
    "user_id": "user-123"
  }
}
```

Note the `:query` suffix and the `class_method` parameter. This is not a standard REST convention. The Agent Engine API uses a generic `:query` endpoint with method dispatch via the request body. Every operation -- session creation, agent invocation, state retrieval -- goes through the same endpoint with different `class_method` values.

**Stream a response:**

```
POST https://{region}-aiplatform.googleapis.com/v1beta1/projects/{project}/locations/{region}/agentEngines/{engine_id}:streamQuery?alt=sse

{
  "class_method": "stream_query",
  "input": {
    "session_id": "session-abc",
    "message": "Generate a scouting report for player XYZ"
  }
}
```

The `?alt=sse` parameter enables server-sent events streaming. Without it, you get a single response after the full agent execution completes. With it, you get incremental updates as each specialist agent produces output -- which is exactly what you want for a UI that shows "Analyzing stats..." then "Computing benchmarks..." then "Generating report..."

These endpoints are not in the public Vertex AI documentation as of this writing. They exist in the API discovery document and in the ADK CLI source code. If you're deploying agents to Agent Engine and want programmatic control beyond what the SDK offers, this is the path.

## QA and Documentation

The rest of the day was infrastructure:

**QA automation.** Five GitHub issue templates covering bug reports, feature requests, scouting accuracy reports, data quality issues, and performance regressions. A synthetic QA harness that generates test scenarios from historical game data and validates scouting report outputs against known-good baselines.

**ADK documentation crawler.** Scraped 118 pages from the ADK documentation site, chunked them into 2,568 RAG fragments, and indexed them in a local vector store. When I'm debugging ADK issues, I can now search the docs with semantic queries instead of keyword ctrl-F on a docs site.

**DevOps playbook.** A 12,500-word operational reference covering deployment procedures, monitoring dashboards, incident response, cost tracking ($250/month actual), and system health scoring (72/100 -- loses points on test coverage and session management). The playbook is the artifact that makes this system operable by someone other than me.

The system health score breakdown: 90/100 on deployment automation, 85/100 on monitoring coverage, 60/100 on test coverage (the multi-agent integration tests are manual), 55/100 on session management (the pickle issue means sessions are effectively stateless). Those last two are the priorities for the next sprint.

## What Agent Engine Deployment Actually Requires

The official documentation makes Agent Engine deployment look like a three-step process: define agent, call `create()`, done. The reality:

1. **Use the CLI, not the SDK** for initial deployment. The SDK's inline packaging path has unresolved issues with complex agent configurations.
2. **Design for stateless single-turn interactions.** Firestore session serialization breaks on pickle edge cases. Pass full context per request.
3. **Use the REST API directly** for production integrations. The `:query` endpoint with `class_method` dispatch gives you full control that neither the SDK nor the CLI exposes.
4. **Stage your agent code in Cloud Storage.** The CLI does this automatically. If you're building your own deployment tooling, replicate the staging step.

The Scout team is live in production. Five agents, single-turn stateless architecture, REST API integration, streaming responses. The deployment path was not what the docs described. But the end result works.

If you're building on Agent Engine today, start with the CLI deployment and the REST API. Skip the Python SDK for anything beyond single-agent configurations. Save yourself the debugging hours.

---

**Related Posts:**

- [PipelinePilot: Building a Multi-Agent SDR Orchestrator on Vertex AI in One Day](/posts/pipelinepilot-multi-agent-sdr-orchestrator-vertex-ai/) -- Another multi-agent system on Vertex AI, different deployment approach
- [How to Get Your ADK Agent into Google's Community Showcase](/posts/how-to-get-adk-agent-into-google-community-showcase/) -- The community side of ADK agent development
- [HustleStats Production Auth Debugging: NextAuth, PrismaAdapter, and Cascading Failures](/posts/hustlestats-production-auth-debugging-nextauth-prisma/) -- Previous HustleStats production debugging saga
