+++
title = 'Local RAG NEXUS Upgrade and Nixtla Validation Infrastructure'
slug = 'local-rag-nexus-upgrade-nixtla-validation-infra'
date = 2025-12-22T10:00:00-06:00
draft = false
tags = ["rag", "multi-provider", "python", "ci-cd", "sqlite", "architecture", "vertex-ai", "release-engineering"]
categories = ["Technical Deep-Dive"]
description = "The local-rag-agent ships the NEXUS Hybrid Cloud Upgrade: multi-provider router for Anthropic/OpenAI/Vertex, PolicyRedactor, workspace API, and run ledger — plus Nixtla universal validator and git-with-intent SQLite migration."
+++

December 22nd was a 35-commit day across four repos. The headline: local-rag-agent shipped a complete hybrid cloud architecture in 17 commits and a versioned release. Nixtla hardened its validation infrastructure. git-with-intent migrated its grading system to SQLite.

One of those days where every project moved forward.

## NEXUS Hybrid Cloud Upgrade

The local-rag-agent had been locked to a single LLM provider since its inception. Anthropic's Claude, hardcoded. That works for a personal tool. It doesn't work when you want to run the same RAG pipeline against different providers for cost comparison, latency testing, or compliance reasons where certain data can't leave a specific cloud tenant.

The NEXUS upgrade (phases 0 through 4) added a multi-provider router that sits between the RAG pipeline and the LLM backends. The router handles three providers: Anthropic Claude, OpenAI GPT, and Google Vertex AI (Gemini). Each provider gets a standardized adapter that normalizes request/response formats.

### The Router Architecture

The router doesn't just switch between providers. It makes routing decisions based on configurable policies:

```python
class ProviderRouter:
    def __init__(self, config: RouterConfig):
        self.providers = {
            "anthropic": AnthropicAdapter(config.anthropic),
            "openai": OpenAIAdapter(config.openai),
            "vertex": VertexAdapter(config.vertex),
        }
        self.policy = config.routing_policy  # "cost", "latency", "preferred"
        self.metrics = ProviderMetrics()

    async def route(self, request: LLMRequest) -> LLMResponse:
        provider = self._select_provider(request)
        try:
            response = await self.providers[provider].complete(request)
            self.metrics.record(provider, response.latency_ms, response.token_count)
            return response
        except ProviderUnavailableError:
            return await self._fallback(request, exclude=[provider])
```

The `_select_provider` method evaluates the routing policy. Cost routing picks the cheapest provider for the token estimate. Latency routing picks the fastest based on a rolling average of recent response times. Preferred routing uses a priority list with automatic fallback.

Each adapter normalizes provider-specific quirks. Anthropic expects `messages` with a `system` parameter. OpenAI expects `messages` with a system message in the array. Vertex expects a `GenerateContentRequest` with a different structure entirely. The adapters translate from the router's unified format to each provider's native format, so the RAG pipeline never knows which provider it's talking to.

The fallback chain is important. If the preferred provider is down or rate-limited, the router tries the next provider without the caller knowing. The RAG pipeline sees a unified interface. It doesn't know or care which provider answered. Fallback ordering respects the routing policy — if you're routing by cost and the cheapest provider is down, the next cheapest gets the request, not the fastest.

The retry logic distinguishes between transient and permanent failures. A 429 (rate limited) triggers a fallback to another provider immediately — waiting for the rate limit to reset wastes time when another provider is available. A 401 (auth failure) is permanent for that provider and gets logged without retry. A 500 gets one retry with exponential backoff before falling back, because server errors are often transient.

### PolicyRedactor

Phase 2 of the upgrade added the PolicyRedactor — a preprocessing layer that scans outgoing LLM requests for content that shouldn't leave the local environment.

The redactor operates on configurable rules. Each rule defines a pattern (regex or named entity type), a replacement strategy (mask, hash, or remove), and a scope (which providers the rule applies to). You might trust Vertex AI with internal project names because it's on your GCP tenant, but redact them before sending to external providers.

```python
redaction_rules = [
    RedactionRule(
        pattern=r"\b[A-Z]{2,}-\d{3,}\b",  # Internal ticket IDs
        strategy="mask",
        scope=["openai", "anthropic"],  # Trust Vertex, redact others
    ),
    RedactionRule(
        entity_type="PERSON_NAME",
        strategy="hash",
        scope=["openai", "anthropic", "vertex"],  # Redact everywhere
    ),
]
```

After the LLM responds, the redactor reverses masked values so the user sees the original content. Hashed values stay hashed — that's the point. The reversibility tracking uses a per-request mapping stored in memory only. The mapping never touches disk and is garbage collected when the request completes.

### Workspace API and Run Ledger

Phases 3 and 4 added the workspace API and run ledger. The workspace API organizes documents into isolated collections — one workspace per project, with separate vector stores and metadata indices. Switching between projects doesn't pollute search results.

Each workspace tracks its own embedding configuration. A workspace for legal documents might use a different embedding model than one for code documentation. The workspace API handles model selection transparently — add a document to a workspace and it gets embedded with that workspace's configured model.

Workspace isolation also affects search results. A query against the "legal-contracts" workspace only searches that workspace's vector store, even if the same embedding model is used across workspaces. This prevents a search for "terms" in a legal workspace from returning results about "terminal" from a code documentation workspace. The isolation is physical — separate vector store files on disk — not just filtered queries against a shared index.

The run ledger records every RAG query: which workspace, which provider, token counts, latency, and the routing decision. Not for billing — for understanding. When you're comparing providers, the ledger shows you concrete data: Anthropic averaged 1.2 seconds on your corpus, OpenAI averaged 0.8 seconds, Vertex averaged 1.5 seconds but cost 40% less.

The ledger also tracks redaction events. If a query triggered the PolicyRedactor, the ledger records how many fields were redacted and which rules fired, without recording the actual redacted content. This gives you visibility into whether your redaction rules are too aggressive (redacting everything) or too permissive (rarely firing).

### v1.1.0

All of this shipped as v1.1.0. The release includes migration scripts for existing users (single-provider configs get wrapped in a router config with one provider), updated documentation, and a CLI command to verify the multi-provider setup works. The migration is non-destructive — existing vector stores and document indices carry over unchanged.

## Nixtla: Universal Validator and CI Validation

Nixtla had 13 commits focused on validation infrastructure. The universal validator moved from a per-skill check to a workspace-wide sweep. Run it once, get a report covering every skill, every manifest, and every configuration file in the repo.

The CI integration runs the universal validator on every PR. A PR that adds a new skill must pass validation before merge. A PR that modifies an existing skill must still pass all existing validations. The validator output gets posted as a PR comment with pass/fail status per skill, so reviewers see validation results without leaving the GitHub UI.

The workspace-wide sweep also catches cross-skill issues that per-skill validation misses. Duplicate tool names across different skills. Conflicting output schemas where two skills claim to produce the same output type but with different field sets. Port conflicts in skills that spin up local servers. These are integration-level problems that only surface when you validate the workspace as a whole.

This is the kind of infrastructure that feels like overhead on day one and saves hours by week two. The first time a malformed skill manifest gets caught before merge instead of after deploy, the CI gate pays for itself.

The 13 commits also included test coverage expansion — the validator itself now has tests for every validation rule, including edge cases like empty manifests, manifests with extra fields, and manifests with correct structure but invalid field values. Testing the testing infrastructure sounds redundant until a validator bug lets a broken skill through.

One specific test caught a real issue during development: a manifest with a `version` field set to `"1.0"` instead of `"1.0.0"` was passing validation because the semver regex accepted two-part versions. The stricter test required three-part semver and the fix was a one-character regex change. But that one character prevented every future skill from shipping with an invalid version that would break dependency resolution.

## git-with-intent: Auto-Fix Grading and SQLite Migration

### Auto-Fix Grading

Four commits on git-with-intent, all focused on the grading system. The auto-fix feature evaluates code changes and assigns a quality grade based on patterns: did the fix address the root cause or just the symptom? Does the fix introduce new complexity? Is it tested?

### JSON to SQLite Migration

The grading data migrated from JSON files to SQLite. JSON files worked when there were dozens of grading records. With hundreds accumulating, the file-based approach was hitting performance limits on queries — filtering by grade, by date range, or by repository required reading and parsing every JSON file.

SQLite gives you indexed queries out of the box. The migration script reads every existing JSON file, inserts the records into SQLite with proper indexes on `grade`, `created_at`, and `repository`, then archives the JSON originals. No data loss, no schema guesswork — the SQLite schema mirrors the JSON structure exactly. The migration ran in under 2 seconds for 847 existing records.

The query improvement was dramatic. Filtering grades by repository went from ~3 seconds (read all JSON files, parse, filter in Python) to ~2ms (indexed SQLite query). That's the difference between a grading dashboard that feels sluggish and one that feels instant. The archive of original JSON files stays around as a backup — if the SQLite migration had a bug, the JSON originals are the recovery path.

One Lumera commit also landed — a minor config fix that didn't warrant its own mention but keeps the commit log accurate.

## Why This Architecture Matters

The interesting thing about the NEXUS upgrade is that it didn't change what the local-rag-agent does. It still ingests documents, embeds them, and answers questions about them. What changed is where the computation happens and who controls it. A user who needs to keep medical records on their GCP tenant can route those queries to Vertex AI while sending general queries to OpenAI for better latency. A user optimizing for cost can route everything through the cheapest provider and fall back to premium providers only when the cheap one is unavailable.

The PolicyRedactor makes the compliance story concrete. Before NEXUS, the only way to ensure sensitive data didn't leak to an external provider was to not use external providers at all. After NEXUS, you can use external providers for most queries and selectively redact the sensitive parts.

That's the difference between "we can't use AI for this" and "we can use AI for this with guardrails." For any team evaluating RAG solutions, multi-provider routing with content-aware redaction is table stakes. Most tools force you to pick one provider. NEXUS lets you use all of them, with policies that enforce what data goes where.

## The Multi-Provider Router as a Pattern

The NEXUS router is specific to the local-rag-agent, but the pattern is transferable to any system that talks to multiple LLM providers. The key design decisions:

1. **Standardized adapters** — each provider gets the same interface. The router doesn't know about provider-specific parameters.
2. **Policy-based routing** — the selection logic is configurable, not hardcoded. Different use cases get different policies.
3. **Automatic fallback** — provider failures are handled at the router level, invisible to callers.
4. **Redaction as middleware** — content policies run before the request leaves, not after the response arrives.
5. **Observable routing** — the run ledger captures every decision so you can audit and optimize the routing policy based on real data.

These five pieces compose into a routing layer that works for RAG, for agent tool calls, for batch processing — anywhere you're calling LLMs and want flexibility in which provider handles the request.

---

Four repos, 35 commits, one release. The local-rag-agent is no longer a single-vendor tool.

### Related Posts

- [Hybrid AI Stack: Reduce Costs 60-80% with Intelligent Routing](/posts/hybrid-ai-stack-reduce-costs-60-80-percent-intelligent-routing/)
- [Nixtla 21 Skills, Production Validator, v1.6.0](/posts/nixtla-21-skills-production-validator-v160/)
- [Fixing Provider Registry Mutations and Sandbox Permissions](/posts/fixing-provider-registry-mutations-sandbox-permissions/)
