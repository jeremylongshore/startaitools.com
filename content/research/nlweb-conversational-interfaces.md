+++
title = 'NLWeb: Building the AI Web with Natural Language Interfaces'
date = 2025-10-09T19:30:00-06:00
draft = false
tags = ["AI", "MCP", "Natural Language Processing", "Schema.org", "Web Architecture", "Open Source"]
categories = ["Research & Curriculum", "AI Engineering", "Web Development"]
description = "Exploring Microsoft's NLWeb framework for building conversational interfaces on websites using Model Context Protocol (MCP) and Schema.org standards"
author = "Jeremy Longshore"
+++

## Overview

**NLWeb** is an open-source framework from Microsoft that simplifies building conversational interfaces for websites. It represents a foundational shift in how we think about web interaction—moving from traditional search and navigation to natural language conversations with structured data.

**Key Innovation**: NLWeb natively supports Model Context Protocol (MCP), allowing the same natural language APIs to serve both humans and AI agents. As the project states: *"NLWeb is to MCP/A2A what HTML is to HTTP."*

---

## The Vision: An AI-Native Web

Just as HTML revolutionized document sharing in the 1990s, NLWeb aims to establish a foundational layer for the AI Web. The framework leverages existing web standards—particularly Schema.org markup used by over 100 million websites—to enable natural language interfaces without requiring sites to rebuild their entire infrastructure.

### Core Principles

1. **Leverage Existing Standards** - Schema.org and RSS are already widely adopted
2. **Conversational by Default** - Natural language as a first-class interface
3. **Hallucination-Free Results** - All responses come from actual database records
4. **Extensible Architecture** - Tools, prompts, and workflows can be customized
5. **Platform Agnostic** - Works on data centers, laptops, and (soon) mobile devices

---

## How It Works

NLWeb has two primary components:

### 1. Simple Natural Language Protocol

A RESTful API that accepts natural language queries and returns responses in JSON using Schema.org vocabulary:

```http
POST /ask
{
  "query": "Find vegan recipes for a summer party",
  "site": "recipe-site",
  "mode": "list"
}
```

**Response Format:**
```json
{
  "query_id": "abc123",
  "results": [
    {
      "url": "https://example.com/recipes/grilled-veggie-skewers",
      "name": "Grilled Veggie Skewers",
      "score": 0.95,
      "description": "Perfect summer appetizer with seasonal vegetables",
      "schema_object": { /* Full Schema.org Recipe object */ }
    }
  ]
}
```

### 2. Straightforward Implementation

The framework uses existing markup on sites with structured lists (products, recipes, events, reviews) and provides:

- Vector database integration (Qdrant, Milvus, Snowflake, Postgres, Elasticsearch, Azure AI Search, Cloudflare AutoRAG)
- LLM connectors (OpenAI, DeepSeek, Gemini, Anthropic, HuggingFace)
- Web server front-end with sample UI
- Tools for ingesting Schema.org JSONL and RSS feeds

---

## Life of a Chat Query

NLWeb processes queries through a sophisticated pipeline that mirrors modern web search but uses LLMs for tasks that previously required specialized algorithms:

```
┌─────────────────────────────────────────────────────────────┐
│                     User submits query                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Parallel Analysis (Step 2)                                  │
│  • Check relevancy                                           │
│  • Decontextualize based on conversation history            │
│  • Determine memory requirements                            │
│  • Fast-track check (most queries skip heavy processing)    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Tool Selection & Execution (Step 3)                         │
│  • LLM selects appropriate tool from manifest               │
│  • Extract parameters                                       │
│  • Execute tool (Search, Item Details, Ensemble Queries)    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Result Scoring & Snippet Generation (Step 4)               │
│  • Score results with LLM calls                             │
│  • Generate appropriate snippets                            │
│  • Collect top N results above threshold                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Optional Post-Processing (Step 4a)                         │
│  • Summarize results                                        │
│  • Generate answers from results                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Return results in specified format                         │
└─────────────────────────────────────────────────────────────┘
```

**Performance Note**: Processing a single query might involve **over 50 LLM API calls**. However, these calls are narrow, specific, and can use different models optimized for each task.

---

## Built-in Tools

NLWeb includes three primary tools out of the box:

### 1. Search Tool
Traditional search flow with AI enhancements:
- Query sent to vector database (TF-IDF scores on embeddings)
- Results returned as Schema.org JSON objects
- LLM scoring with snippet generation
- Top N results above threshold collected

### 2. Item Details Tool
Retrieves specific information about items:
- Items specified by name, description, or context
- Vector database query for candidates
- LLM scoring to match candidates
- Detail extraction via LLM calls

### 3. Ensemble Queries Tool
Combines multiple items of different types:
- Handles complex queries: "appetizer, entree and dessert, Asian fusion themed"
- Extracts separate queries for each item type
- Independent vector database queries
- LLM ranking for appropriateness
- Creates ensembles from top 2-3 of each query

---

## MCP Integration

Every NLWeb instance acts as an **MCP server** and supports core MCP methods:

- `list_tools` - Enumerate available tools
- `list_prompts` - Show available prompts
- `call_tool` - Execute a specific tool
- `get_prompt` - Retrieve a prompt template

The `/mcp` endpoint returns responses in MCP-compatible format, making NLWeb instances discoverable and usable by any MCP client.

**Future Vision**: NLWeb will enable calling other NLWeb/MCP servers, allowing distributed tool execution across different services.

---

## Platform Support

### Operating Systems
- Windows
- macOS
- Linux

### Vector Stores
- [Qdrant](https://qdrant.tech/) (local and cloud)
- [Snowflake](https://www.snowflake.com/)
- [Milvus](https://milvus.io/)
- [Azure AI Search](https://azure.microsoft.com/en-us/products/ai-services/ai-search)
- [Elasticsearch](https://www.elastic.co/)
- [Postgres](https://www.postgresql.org/) (with pgvector)
- [Cloudflare AutoRAG](https://developers.cloudflare.com/)

### LLM Providers
- OpenAI (GPT-4, GPT-4 Turbo, GPT-3.5)
- DeepSeek
- Google Gemini
- Anthropic Claude
- Inception
- HuggingFace models

---

## Quick Start Example

### Prerequisites
- Python 3.10+
- API key for your preferred LLM provider

### Setup (5 minutes)

```bash
# Clone repository
git clone https://github.com/nlweb-ai/NLWeb.git
cd NLWeb

# Create virtual environment
python -m venv myenv
source myenv/bin/activate  # Windows: myenv\Scripts\activate

# Install dependencies
cd code/python
pip install -r requirements.txt

# Configure environment
cd ../../
cp .env.template .env
# Edit .env with your LLM API keys

# Verify configuration
cd code/python
python testing/check_connectivity.py

# Load sample data (podcast RSS feed)
python -m data_loading.db_load https://feeds.libsyn.com/121695/rss Behind-the-Tech

# Start server
python app-aiohttp.py

# Visit http://localhost:8000/
```

You now have a working conversational interface for podcast episodes!

---

## REST API

### Endpoints

**`/ask`** - Returns results in standard JSON format
**`/mcp`** - Returns results in MCP-compatible format

### Required Parameter
- `query` - The current query in natural language

### Optional Parameters
- `site` - Token for a subset of data (multi-site support)
- `prev` - Comma-separated list of previous queries (conversation context)
- `decontextualized_query` - Pre-decontextualized query (skips server-side processing)
- `streaming` - Enable/disable streaming (default: true)
- `query_id` - Custom query ID (auto-generated if not provided)
- `mode` - Response mode:
  - `list` (default) - Top matches from backend
  - `summarize` - Summary + list
  - `generate` - RAG-style answer generation

### Response Format

```json
{
  "query_id": "unique-id",
  "results": [
    {
      "url": "https://example.com/item",
      "name": "Item Name",
      "site": "site-token",
      "score": 0.95,
      "description": "LLM-generated description",
      "schema_object": { /* Full Schema.org object */ }
    }
  ]
}
```

---

## Hallucination-Free Guarantee

**Critical Feature**: Since all returned items come directly from the database, **results cannot be hallucinated**. Each result includes the full `schema_object` from the data store.

- Results may be less than perfectly relevant
- Results may be ranked sub-optimally
- But results will **never be fabricated**

**Note**: Post-processing (summarize/generate modes) may degrade this guarantee, so test carefully.

---

## Architecture Insights

### Customization Points

1. **Prompts** - Declaratively specialized for object types (Recipe vs. Real Estate)
2. **Tools** - Domain-specific tools with additional knowledge (e.g., recipe substitutions)
3. **Control Flow** - Modify query processing pipeline
4. **User Interface** - Replace sample UI with custom design
5. **Memory** - Add conversation memory and context retention

### Production Considerations

Most production deployments will:

1. **Custom UI** - Replace sample interface with branded design
2. **Direct Integration** - Integrate NLWeb into application environment
3. **Live Database Connection** - Connect to production databases (avoid data freshness issues)
4. **Multi-Model Strategy** - Use different LLMs for different tasks (cost optimization)
5. **Caching & Performance** - Implement query caching and result optimization

---

## Use Cases

### E-Commerce
Natural language product search with filtering:
- "Find wireless headphones under $200 with noise cancellation"
- "Show me vegan protein powders with chocolate flavor"

### Recipe Sites
Dietary restriction handling and meal planning:
- "Gluten-free desserts for a birthday party"
- "Plan a week of dinners under 500 calories"

### Real Estate
Property search with complex criteria:
- "3 bedroom homes near good schools under $500k"
- "Condos with mountain views and low HOA fees"

### Content Discovery
Podcast, blog, and video recommendations:
- "Episodes about AI ethics from the last 6 months"
- "Articles explaining quantum computing for beginners"

### Event Platforms
Smart event discovery and planning:
- "Family-friendly events this weekend downtown"
- "Networking events for software engineers"

---

## Technical Deep-Dive: Schema.org Integration

NLWeb exploits a key insight: **LLMs understand Schema.org markup very well** because it's prevalent in their training data (100+ million websites use it).

### Why Schema.org Works

1. **Common Vocabulary** - Standardized types and properties across domains
2. **Rich Semantics** - Detailed descriptions of entities and relationships
3. **LLM Native** - Models trained on billions of pages with Schema.org markup
4. **Type Hierarchy** - Inheritance allows specialized and generalized handling

### Example: Recipe Schema

```json
{
  "@type": "Recipe",
  "name": "Chocolate Chip Cookies",
  "recipeIngredient": [
    "2 cups all-purpose flour",
    "1 cup butter",
    "1 cup chocolate chips"
  ],
  "recipeInstructions": [
    {"@type": "HowToStep", "text": "Preheat oven to 350°F"},
    {"@type": "HowToStep", "text": "Mix butter and sugar"}
  ],
  "nutrition": {
    "@type": "NutritionInformation",
    "calories": "150 calories"
  },
  "suitableForDiet": "https://schema.org/VegetarianDiet"
}
```

LLMs can:
- Extract dietary restrictions (`suitableForDiet`)
- Calculate serving sizes (`nutrition`)
- Suggest substitutions (domain knowledge + schema structure)
- Generate cooking instructions summaries

---

## Comparison to Traditional RAG

| Feature | Traditional RAG | NLWeb |
|---------|----------------|-------|
| **Data Format** | Unstructured text chunks | Structured Schema.org objects |
| **Hallucination Risk** | High (LLM generates freely) | Low (results from database) |
| **Result Granularity** | Passage-level | Entity-level |
| **Multi-faceted Queries** | Limited | Native support (ensemble queries) |
| **Conversation Context** | Basic | Decontextualization pipeline |
| **Tool Ecosystem** | Custom per deployment | Extensible tool manifest |
| **Agent Compatibility** | Manual integration | Native MCP support |

---

## Development Roadmap

### Current Status
- ✅ REST API (`/ask` and `/mcp` endpoints)
- ✅ MCP server implementation
- ✅ Multiple vector store connectors
- ✅ Multiple LLM provider support
- ✅ Docker deployment
- ✅ Azure deployment guides

### Coming Soon
- 🚧 A2A (Agent-to-Agent) protocol support
- 🚧 Distributed NLWeb/MCP server calling
- 🚧 Mobile device deployment
- 🚧 GCP deployment guides
- 🚧 AWS deployment guides
- 🚧 CI/CD pipeline templates

---

## Learning Resources

### Official Documentation
- **GitHub Repository**: [https://github.com/nlweb-ai/NLWeb](https://github.com/nlweb-ai/NLWeb)
- **Hello World Tutorial**: [Getting Started Guide](https://github.com/nlweb-ai/NLWeb/blob/main/docs/nlweb-hello-world.md)
- **Life of a Chat Query**: [Architecture Deep-Dive](https://github.com/nlweb-ai/NLWeb/blob/main/docs/life-of-a-chat-query.md)
- **REST API Docs**: [API Reference](https://github.com/nlweb-ai/NLWeb/blob/main/docs/nlweb-rest-api.md)

### Setup Guides
- [Docker Setup](https://github.com/nlweb-ai/NLWeb/blob/main/docs/setup-docker.md)
- [Azure Deployment](https://github.com/nlweb-ai/NLWeb/blob/main/docs/setup-azure.md)
- [Qdrant Integration](https://github.com/nlweb-ai/NLWeb/blob/main/docs/setup-qdrant.md)
- [Snowflake Integration](https://github.com/nlweb-ai/NLWeb/blob/main/docs/setup-snowflake.md)

### Customization
- [Modifying Prompts](https://github.com/nlweb-ai/NLWeb/blob/main/docs/nlweb-prompts.md)
- [Changing Control Flow](https://github.com/nlweb-ai/NLWeb/blob/main/docs/nlweb-control-flow.md)
- [User Interface Customization](https://github.com/nlweb-ai/NLWeb/blob/main/docs/nlweb-user-interface.md)
- [Adding Memory](https://github.com/nlweb-ai/NLWeb/blob/main/docs/nlweb-memory.md)

---

## Integration Examples

### Example 1: Recipe Site Integration

```python
# Load recipe data from RSS feed
python -m data_loading.db_load https://example.com/recipes.rss RecipeSite

# Query for vegan desserts
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "query": "vegan chocolate desserts",
    "site": "RecipeSite",
    "mode": "list"
  }'
```

### Example 2: E-Commerce Product Search

```python
# Load product catalog (Schema.org JSONL)
python -m data_loading.db_load products.jsonl MyStore

# Search with filters
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "query": "wireless headphones with ANC under $200",
    "site": "MyStore",
    "mode": "summarize"
  }'
```

### Example 3: MCP Client Integration

```python
# Using NLWeb as MCP server
import mcp_client

server = mcp_client.connect("http://localhost:8000/mcp")

# List available tools
tools = server.list_tools()

# Call search tool
result = server.call_tool(
    "search",
    query="Find episodes about machine learning",
    site="Behind-the-Tech"
)
```

---

## Performance Optimization

### Multi-Model Strategy

Different tasks have different requirements:

```yaml
# config_llm.yaml example
tasks:
  relevancy_check:
    model: gpt-4o-mini  # Fast, cheap for simple classification
  decontextualization:
    model: gpt-4o       # Better context understanding
  scoring:
    model: gpt-4o-mini  # Simple scoring task
  snippet_generation:
    model: gpt-4o       # Creative text generation
```

### Caching Strategies

1. **Query Caching** - Cache decontextualized queries
2. **Embedding Caching** - Cache vector embeddings
3. **Result Caching** - Cache scored results for common queries
4. **LLM Response Caching** - Cache LLM responses for identical prompts

### Fast-Track Optimization

The "fast-track" path bypasses heavy processing for simple queries:

- Lightweight relevancy check
- Skip decontextualization if not needed
- Parallel execution with full pipeline
- Results blocked until validation completes

**Impact**: 2-3x speedup for 60-70% of queries.

---

## Security & Privacy

### Data Privacy
- **No Server-Side State** - Conversation context passed by client
- **Local Deployment** - Run entirely on-premises if required
- **Data Isolation** - Multi-site support with access controls

### API Security
- OAuth integration available
- GitHub OAuth example included
- Token-based authentication supported

### Content Safety
- Relevancy checks prevent off-topic queries
- Domain-specific tools limit scope
- Database-only results prevent hallucinated content

---

## Community & Contribution

### Contributing

NLWeb is open source under the **MIT License**. Contributions welcome:

- **Code Contributions** - New tools, connectors, optimizations
- **Documentation** - Guides, tutorials, examples
- **Testing** - Vector store testing, LLM provider testing
- **Use Cases** - Share production deployments and lessons learned

**Contact**: [NLWebSup@microsoft.com](mailto:NLWebSup@microsoft.com)

### License

```
MIT License
Copyright (c) Microsoft Corporation.
```

Full license: [https://github.com/nlweb-ai/NLWeb/blob/main/LICENSE](https://github.com/nlweb-ai/NLWeb/blob/main/LICENSE)

---

## Why This Matters

NLWeb represents a paradigm shift in web architecture:

1. **Democratizes AI Interfaces** - Any site with structured data can add conversational UI
2. **Builds on Standards** - Schema.org and RSS provide instant data readiness
3. **Enables Agent Ecosystem** - MCP compatibility makes sites agent-accessible
4. **Prevents Hallucination** - Database-backed results ensure accuracy
5. **Extensible by Design** - Tools, prompts, and flows are customizable

**The Vision**: Just as HTML enabled document sharing across the internet, NLWeb aims to enable conversational interaction across the AI Web—with shared protocols, sample implementations, and community participation.

---

## Getting Started Checklist

- [ ] Clone NLWeb repository
- [ ] Set up Python 3.10+ virtual environment
- [ ] Configure `.env` with LLM API keys
- [ ] Choose vector store (Qdrant local for testing)
- [ ] Run connectivity check script
- [ ] Load sample data (RSS feed or Schema.org JSONL)
- [ ] Start server and test at `http://localhost:8000`
- [ ] Explore sample UIs in `static/` directory
- [ ] Read Life of a Chat Query docs
- [ ] Experiment with custom prompts and tools

---

## Attribution

**Project**: NLWeb - Natural Language Interfaces for Websites
**Organization**: Microsoft Corporation
**Repository**: [https://github.com/nlweb-ai/NLWeb](https://github.com/nlweb-ai/NLWeb)
**License**: MIT License
**Documentation**: [https://github.com/nlweb-ai/NLWeb/tree/main/docs](https://github.com/nlweb-ai/NLWeb/tree/main/docs)

*This article is an educational resource created for Start AI Tools. All credit for NLWeb development goes to Microsoft Corporation and the NLWeb contributors. For official project information, please visit the GitHub repository.*

---

## Next Steps

1. **Explore the Documentation** - Deep-dive into [Life of a Chat Query](https://github.com/nlweb-ai/NLWeb/blob/main/docs/life-of-a-chat-query.md)
2. **Run Hello World** - Follow the [5-minute setup guide](https://github.com/nlweb-ai/NLWeb/blob/main/docs/nlweb-hello-world.md)
3. **Join the Community** - Star the repo and contribute
4. **Build Something** - Create a conversational interface for your site
5. **Share Your Experience** - Document your use case and lessons learned

**Ready to build the AI Web?** Start with NLWeb today.

---

*Last Updated: October 9, 2025*
*Research & Curriculum Article by Jeremy Longshore*
*[Start AI Tools](https://startaitools.com) - Presented by Intent Solutions*
