+++
title = 'Perception Agent System: Zero to MCP Server and Dashboard in One Day'
slug = 'perception-agent-system-zero-to-mcp-dashboard'
date = 2025-11-14T10:00:00-06:00
draft = false
tags = ["mcp", "agents", "fastapi", "react", "firebase", "gcp", "vertex-ai", "docker"]
categories = ["Technical Deep-Dive"]
description = "Building an 8-agent news intelligence platform from zero to working MCP server and React dashboard in a single day. 13,881 lines of initial scaffold, FastAPI MCP service, Firestore integration, and GitHub Actions CI."
+++

## The Problem

I wanted a system that could monitor news feeds, detect emerging trends, and surface relevant articles without manual curation. Not a feed reader — a multi-agent intelligence platform where specialized agents handle different aspects of the news pipeline: ingestion, deduplication, relevance scoring, topic classification, trending detection, summarization, alerting, and archival.

The project name: Perception. GCP project: `perception-with-intent`.

The constraint: build the entire system — agents, MCP service, dashboard, infrastructure — in one day.

## Architecture Decisions Made in the First Hour

Eight agents, each with a single responsibility:

| Agent | Job |
|-------|-----|
| **Ingestor** | Fetches RSS feeds, normalizes article format |
| **Deduplicator** | URL + content hash deduplication |
| **Scorer** | Relevance scoring against topic watchlists |
| **Classifier** | Topic and category assignment |
| **Trending** | Velocity detection across time windows |
| **Summarizer** | Article summarization with key entity extraction |
| **Alerter** | Threshold-based notifications |
| **Archivist** | Retention policy enforcement, cold storage |

Each agent is defined in YAML, not code. The YAML specifies the agent's name, model, instructions, tools it can access, and output schema. The runtime reads these configs and constructs agent instances. Adding a new agent means adding a YAML file, not writing a new class.

```yaml
# agents/ingestor.yaml
name: ingestor
model: gemini-2.0-flash
instructions: |
  You are a news feed ingestion agent. Fetch articles from
  assigned RSS sources. Normalize each article into the
  standard schema: title, url, published_at, source, content,
  author. Deduplicate by URL before storing.
tools:
  - fetch_rss_feed
  - store_articles
output_schema:
  type: object
  properties:
    articles_fetched: { type: integer }
    articles_stored: { type: integer }
    errors: { type: array, items: { type: string } }
```

This YAML-first approach means the agent definitions are version-controlled, diffable, and reviewable without reading Python code.

## The MCP Service

FastAPI was the obvious choice for the MCP server. The service exposes tools that agents can call, with each tool registered as an MCP-compliant endpoint.

The first real tool: `fetch_rss_feed`. Not a mock — actual RSS parsing with `feedparser` and `httpx` for async HTTP:

```python
@mcp_tool(name="fetch_rss_feed", description="Fetch and parse an RSS feed")
async def fetch_rss_feed(url: str, max_items: int = 50) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url)
        response.raise_for_status()

    feed = feedparser.parse(response.text)

    articles = []
    for entry in feed.entries[:max_items]:
        articles.append({
            "title": entry.get("title", ""),
            "url": entry.get("link", ""),
            "published_at": parse_date(entry.get("published", "")),
            "source": feed.feed.get("title", url),
            "content": entry.get("summary", ""),
            "author": entry.get("author", "unknown"),
        })

    return {
        "feed_title": feed.feed.get("title", ""),
        "articles": articles,
        "count": len(articles),
    }
```

The `store_articles` tool writes to Firestore with URL-based deduplication. Document IDs are `art-{sha256(url)[:16]}`, so storing the same article twice is a no-op merge.

Additional tools built on day one: `get_articles` (paginated reads), `search_articles` (keyword search across Firestore), `get_trending` (time-windowed velocity queries), and `get_sources` (RSS source catalog management).

## Dashboard: React + Vite + Firestore

The dashboard needed to show three things: what articles the system found, which agents are running, and what topics are being monitored.

React with Vite for the frontend. Firebase SDK for direct Firestore reads (the dashboard reads the same collections the MCP service writes to). No backend-for-frontend — the dashboard connects to Firestore directly with security rules limiting read access.

```typescript
// Real-time article feed
const articlesQuery = query(
  collection(db, 'articles'),
  orderBy('published_at', 'desc'),
  limit(50)
);

const unsubscribe = onSnapshot(articlesQuery, (snapshot) => {
  const articles = snapshot.docs.map(doc => ({
    id: doc.id,
    ...doc.data()
  }));
  setArticles(articles);
});
```

The `onSnapshot` listener means articles appear in the dashboard within seconds of ingestion. No polling, no refresh button. An agent ingests an article, writes to Firestore, and the dashboard updates.

Agent status panel shows each of the 8 agents with their last run time, articles processed, and error count. This reads from a `agent_runs` collection that each agent updates after execution.

## Infrastructure in an Afternoon

Firebase Hosting for the dashboard. Firebase serves the built React app from CDN with automatic SSL.

Workload Identity Federation (WIF) for GitHub Actions. No service account keys stored as secrets — GitHub Actions authenticates to GCP using OIDC tokens. The WIF configuration maps the GitHub repo to a GCP service account with specific IAM roles.

```yaml
# .github/workflows/deploy.yml
- uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: 'projects/123/locations/global/workloadIdentityPools/github/providers/github'
    service_account: 'github-actions@perception-with-intent.iam.gserviceaccount.com'

- uses: google-github-actions/deploy-appengine@v2
  # or firebase deploy, depending on target
```

Docker configuration for the MCP service. Multi-stage build: Python 3.12 slim base, pip install from `requirements.txt`, copy application code, expose port 8080. The Dockerfile runs the FastAPI service with uvicorn.

CI pipeline: lint with ruff, type-check with mypy, test with pytest, build Docker image, push to Artifact Registry. All triggered on push to main.

## The 13,881-Line Scaffold

The initial commit had 13,881 lines. That number looks alarming until you break it down:

- **Agent YAML configs**: 8 files, ~400 lines total
- **MCP service**: FastAPI app, 6 tools, Firestore integration, ~1,200 lines
- **Dashboard**: React components, Firestore hooks, routing, styles, ~3,500 lines
- **Infrastructure**: Dockerfiles, CI workflows, Firebase config, security rules, ~800 lines
- **Generated files**: `package-lock.json`, `requirements.txt` hashes, TypeScript declarations, ~8,000 lines

The actual authored code was closer to 6,000 lines. Still significant for one day, but not the 14K the raw diff suggests.

## What Was Working at EOD

- MCP service running locally with all 6 tools functional
- `fetch_rss_feed` tool successfully parsing real RSS feeds
- `store_articles` writing to Firestore with deduplication
- Dashboard displaying articles from Firestore in real-time
- All 8 agent YAML configs in place with correct schemas
- Firebase Hosting configured and deployable
- Docker build passing
- CI pipeline green

## What Was Not Working at EOD

The agents were configured but not deployed to Vertex AI. The YAML definitions existed, the MCP tools they needed existed, but the orchestration layer that actually runs agents on Vertex AI was stubbed out. That's Day 2 work.

The trending detection tool returned placeholder data. The time-windowed velocity calculation needed historical data that didn't exist yet — the system had been running for hours, not days.

No alerting. The Alerter agent had a config but no notification backend. Slack integration was planned but not built.

## Patterns Worth Stealing

**YAML-configured agents.** The agent definitions are data, not code. You can review, diff, and version-control agent behavior without reading implementation files. When you want to change an agent's behavior, you edit a YAML file and redeploy.

**Direct Firestore from the dashboard.** Skipping a BFF layer removed an entire service from the architecture. Security rules handle authorization. The dashboard reads what it needs, and Firestore handles the real-time sync.

**WIF over service account keys.** No secrets to rotate. No keys to leak. GitHub Actions proves its identity to GCP via OIDC, and GCP grants access based on the repository identity. This should be the default for every GCP + GitHub project.

**MCP tools as the agent interface.** Agents don't call internal functions — they call MCP tools. This means you can test tools independently, swap agent implementations without touching tools, and add new tools without modifying agents.

## What I'd Do Differently

The 8-agent design was ambitious for day one. In practice, only 2 agents (Ingestor and Deduplicator) had meaningful work to do on launch day. The other 6 needed data to accumulate before they were useful. Starting with 2-3 agents and adding more as data grew would have been more pragmatic.

The Firestore schema was designed before any agents ran. Some of the index requirements only became obvious after the first real queries. Pre-designing schemas for agent workloads is guesswork — better to start with the minimum and add indexes as agents demand them.

---

**Related Posts:**

- [Perception Dashboard: Wiring Real Triggers, Topic Watchlists, and the BSL-1.1 Decision](/posts/perception-dashboard-real-triggers-topic-watchlists/) — Where Perception went after this initial build
- [OSS Agent Lab: Meta-Agent System in One Day](/posts/oss-agent-lab-meta-agent-system-one-day/) — Another single-day multi-agent system build
- [Productizing AI Agents: Containerized Offerings and the Iteration Loop](/posts/productizing-ai-agents-containerized-offerings-iteration-loop/) — The business side of agent system architecture
