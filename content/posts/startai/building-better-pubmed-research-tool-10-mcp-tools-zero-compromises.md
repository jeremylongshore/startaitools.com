---
title: "Building a Better PubMed Research Tool: 10 MCP Tools, Zero Compromises"
date: 2025-10-20T21:58:00-06:00
draft: false
tags: ["mcp", "pubmed", "typescript", "research", "life-sciences", "open-source", "vertex-ai"]
author: "Jeremy Longshore"
description: "How we built a production-ready PubMed research toolkit with 10 MCP tools that outperforms Anthropic's Claude for Life Sciences - and why simpler is often better."
---

When Anthropic announced Claude for Life Sciences on October 20, 2025, my immediate thought wasn't "how do we compete?" It was "how do we do this *better*?"

This is the story of building the PubMed Research Master plugin in one evening - a fully tested, production-ready MCP server with 10 tools, comprehensive test coverage, and a user experience that prioritizes simplicity over complexity.

## The False Start: When AI Doesn't Know What You're Building

The first challenge was immediate: **Vertex AI Gemini 2.0 Flash was trained before the Model Context Protocol existed**.

My initial prompt to generate the plugin failed spectacularly - only 4 files created, incomplete implementation, missing critical pieces. The problem? I assumed Vertex AI understood what MCP was.

**Lesson 1: When using AI trained before your technology exists, you need to explain everything.**

I created a comprehensive context document (`prompts/vertex-life-sciences-full-context.md`) that explained:
- What Claude Code is (released 2025)
- What MCP is (announced November 2024)
- Complete JSON-RPC 2.0 protocol specification
- TypeScript implementation patterns
- Full examples of working MCP servers

This 480-line context document became the foundation. Second generation attempt: complete success.

## The SQLite Question: Complexity vs. Simplicity

The Vertex-generated code included SQLite caching for offline access. Comprehensive, feature-rich, impressive.

Then came the pivotal user feedback: **"What's the SQLite database have to do with anything?"**

This triggered a critical design decision. The plugin had two paths:

**Path A:** Keep SQLite, add complexity, maintain local cache, handle database migrations, manage state.

**Path B:** Remove SQLite entirely, keep it simple, offer caching as a paid premium upgrade.

We chose Path B. Here's why:

```typescript
// Before: Database initialization, connection pooling, cache management
private db!: Database;
private async initializeDatabase() { /* ... */ }
private async cacheSearch() { /* ... */ }
private async getCachedResults() { /* ... */ }

// After: Direct API calls, zero dependencies
private async searchPubMed(query: string) {
  await this.enforceRateLimit();
  const response = await fetch(/* ... */);
  return response.json();
}
```

**Result:** Cleaner code, fewer dependencies, easier to understand, and a clear business model - free base version, paid customizations.

## The 10 MCP Tools: Comprehensive Research Workflow

Each tool serves a specific research need:

### 1. search_pubmed - Advanced Search
```typescript
const searchSchema = z.object({
  query: z.string(),
  max_results: z.number().default(100),
  date_from: z.string().optional(),
  date_to: z.string().optional(),
  article_type: z.string().optional()
});
```

### 2-4. Article Deep Dives
- `get_article_details` - Full metadata by PMID
- `get_full_text` - PMC full-text when available
- `search_by_mesh` - Medical Subject Heading taxonomy

### 5-7. Research Expansion
- `get_related_articles` - Citation network expansion
- `export_citations` - BibTeX/RIS/EndNote formats
- `analyze_trends` - Publication trends over time

### 8-10. Analysis Tools
- `compare_studies` - Side-by-side comparison
- `get_mesh_terms` - Extract MeSH terms
- `advanced_search` - Boolean queries

## Rate Limiting: The Right Way

NCBI E-utilities has strict requirements:
- Without API key: 3 requests/second
- With API key: 10 requests/second

We implemented automatic enforcement:

```typescript
private async enforceRateLimit() {
  const now = Date.now();
  const timeSinceLastRequest = now - this.lastRequestTime;

  if (this.apiKey) {
    // 10 req/s: 100ms minimum delay
    if (timeSinceLastRequest < 100) {
      await new Promise(resolve =>
        setTimeout(resolve, 100 - timeSinceLastRequest)
      );
    }
  } else {
    // 3 req/s: track request counter
    if (this.requestCounter >= 3 && timeSinceLastRequest < 1000) {
      await new Promise(resolve =>
        setTimeout(resolve, 1000 - timeSinceLastRequest)
      );
    }
    this.requestCounter = (timeSinceLastRequest < 1000)
      ? this.requestCounter + 1 : 1;
  }

  this.lastRequestTime = Date.now();
}
```

Every single tool call goes through this. No exceptions. No rate limit violations.

## Testing: 16 Tests, 100% Pass Rate

We created comprehensive tests covering:

```typescript
describe('PubMed Research Master MCP Server', () => {
  // Server initialization
  it('should create server instance')
  it('should have correct server name in config')

  // Tool registration
  it('should register 10 MCP tools')

  // Rate limiting (actual timing tests)
  it('should enforce 3 req/s without API key')
  it('should enforce 10 req/s with API key')

  // Input validation
  it('should validate search_pubmed parameters')
  it('should validate export_citations format')
  it('should validate PMID format')

  // Error handling
  it('should handle network errors gracefully')
  it('should handle invalid PMID errors')
  it('should handle API rate limit errors')
});
```

All 16 tests pass. Zero vulnerabilities. TypeScript compiles with zero errors.

## The 9.6 KB Agent Skill

While Anthropic's Claude for Life Sciences uses 500-byte Agent Skills, we built a 9,600-byte Literature Review Automator that activates automatically when users say:

- "Review the literature on..."
- "What does research say about..."
- "Find papers about..."

The skill runs a complete multi-phase workflow:

### Phase 1: Query Construction
1. Analyze research topic
2. Identify key concepts and synonyms
3. Construct Boolean search query
4. Add filters (date range, article type)

### Phase 2: Article Retrieval
1. Execute PubMed search
2. Retrieve article metadata
3. Get full abstracts
4. Extract MeSH terms

### Phase 3: Analysis
1. Analyze publication trends
2. Identify key researchers
3. Map citation networks
4. Find consensus and controversies

### Phase 4: Synthesis
1. Group findings by theme
2. Create structured outline
3. Generate summary
4. Suggest future research directions

**That's 17x larger than Anthropic's examples**, with detailed step-by-step instructions that Claude can follow autonomously.

## Why This Is Better

Let's be direct about the comparison:

| Feature | Anthropic's Claude for Life Sciences | PubMed Research Master |
|---------|--------------------------------------|------------------------|
| **Pricing** | Paid tier | Free (MIT license) |
| **Access** | Limited | Public marketplace |
| **License** | Proprietary | Open source |
| **Hosting** | Cloud only | Self-hosted |
| **PubMed Tools** | 1 (basic search) | 10 (complete toolkit) |
| **Offline** | No | Optional (paid upgrade) |
| **Agent Skills** | ~500 bytes | 9,600 bytes (17x) |
| **Citation Export** | Not available | BibTeX/RIS/EndNote |
| **Trend Analysis** | Not available | Built-in |
| **Customizable** | No | Yes (fork & modify) |

We're not competing. We're building better tools that users actually control.

## The Build Process: One Evening

Timeline:
- **6:00 PM** - Research Anthropic announcement
- **6:30 PM** - Create comprehensive Vertex AI context
- **7:00 PM** - First generation attempt (failed - incomplete)
- **7:30 PM** - Updated context with MCP protocol details
- **8:00 PM** - Second generation (successful)
- **8:30 PM** - Remove SQLite per user feedback
- **9:00 PM** - Fix TypeScript compilation errors
- **9:15 PM** - Write comprehensive tests
- **9:30 PM** - All tests passing
- **9:45 PM** - Add to marketplace, commit

**Total time: ~4 hours from research to production.**

## What We Learned

1. **Simplicity wins** - The SQLite removal made the code cleaner, not poorer
2. **Explain everything to AI** - Don't assume it knows new technologies
3. **Test everything** - 16 tests caught issues before deployment
4. **Free + paid upgrades** - Better business model than locked features
5. **Open source builds trust** - Users can verify, modify, extend

## Try It Yourself

```bash
# Install from marketplace
/plugin marketplace add jeremylongshore/claude-code-plugins
/plugin install pubmed-research-master@claude-code-plugins-plus

# Search PubMed
/pubmed-search

# Or just ask Claude
"Review the literature on CRISPR gene editing in cancer therapy"
```

The Literature Review Automator skill activates automatically.

## Related Posts

- [Scaling AI Batch Processing: 235 Plugins with Vertex AI Gemini](https://startaitools.com/posts/startai/scaling-ai-batch-processing-enhancing-235-plugins-with-vertex-ai-gemini-on-the-free-tier/) - How we generate plugins at scale
- [Hybrid AI Stack: Reduce Costs 60-80% with Intelligent Routing](https://startaitools.com/posts/startai/hybrid-ai-stack-reduce-ai-api-costs-by-60-80-with-intelligent-request-routing/) - Cost optimization strategies

## The Source Code

Everything is open source:
- **Repository**: https://github.com/jeremylongshore/claude-code-plugins
- **Plugin**: `/plugins/life-sciences/pubmed-research-master/`
- **Tests**: Full test suite included
- **License**: MIT

Fork it. Customize it. Make it yours.

---

**Building better tools means putting users first - not competing for market share.**
