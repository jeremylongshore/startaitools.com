+++
title = 'git-with-intent Competitive Strategy and Perception Real Ingestion Pipeline'
slug = 'gwi-competitive-strategy-perception-real-ingestion'
date = 2026-02-13T10:00:00-06:00
draft = false
tags = ["git-with-intent", "strategy", "competitive-analysis", "perception", "fastapi", "firestore", "ingestion"]
categories = ["Development Journey"]
description = "git-with-intent gets competitive strategy docs and a model selection rubric. Perception wires real store_articles, a trigger endpoint, and dashboard button to complete the ingestion pipeline."
+++

Two commits across two repos. A light day by commit count, but both commits landed meaningful capability that had been blocking next steps. git-with-intent got its competitive positioning documented — which unblocked the pricing page design and the README rewrite that followed later in the month. Perception closed the loop between the dashboard button and real article storage, which meant the product was finally demo-able without apologies about mock data.

## git-with-intent: Competitive Strategy

The competitive strategy document maps git-with-intent against four categories of adjacent tools:

- **Git hooks + linters** (Husky, lint-staged, Commitlint) — Enforce commit message format but don't analyze intent or content
- **AI commit generators** (aicommits, gitmoji-cli) — Generate messages but don't classify or enforce policy
- **Code review assistants** (CodeRabbit, Sourcery, Qodo) — Operate at PR level, not commit level
- **Governance platforms** (Backstage, Port) — Track service ownership, not commit-level compliance

git-with-intent sits in the gap between commit-time enforcement and PR-level review. It classifies every commit by intent (feature, fix, refactor, chore, docs, test), validates that the classification matches the actual diff, and generates compliance reports that aggregate across branches, time ranges, and contributors.

The document also includes a model selection rubric for the intent classification engine. The rubric scores models across five dimensions: latency (must classify a commit in under 2 seconds), accuracy (95%+ on the internal benchmark of 500 labeled commits), cost (under $0.001 per classification for sustainable batch usage), context window (must handle 10K+ token diffs), and offline capability (must support a local model path for air-gapped environments).

Current model selection: Gemini 1.5 Flash for cloud, Mistral 7B for local. Flash hits 97% accuracy on the benchmark with 400ms median latency. Mistral 7B drops to 91% but runs entirely offline on an M2 MacBook in under 3 seconds.

The rubric also established a testing methodology for future model evaluations. The 500-commit benchmark is split 80/20 into train and test sets. Each commit has a human-labeled intent classification and a difficulty rating (trivial, standard, ambiguous). The "ambiguous" category — commits that mix refactoring with bug fixes, or documentation updates with feature additions — accounts for 15% of the benchmark and is where models diverge most. Flash handles ambiguous commits at 89% accuracy. Mistral 7B drops to 72% on the same subset, which is the primary driver of its lower overall score.

The strategy document concluded with three pricing scenarios: free tier (100 classifications/month per repo), pro tier ($9/month for unlimited), and enterprise (self-hosted with the local model). The free tier targets open-source projects and individual developers. The pro tier targets teams that want compliance reports. Enterprise targets regulated environments where commit data can't leave the network.

## Perception: Real Ingestion Pipeline

Perception's ingestion pipeline had three pieces that existed independently: the `store_articles` function (which was still a mock), the `POST /trigger/ingestion` endpoint (which existed but called the mock), and the dashboard "Run Ingestion" button (which existed but wasn't wired to the endpoint). This commit connected all three.

The real `store_articles` implementation:

```python
def store_articles(articles: list[dict], db: firestore.Client) -> int:
    stored = 0
    batch = db.batch()
    for article in articles[:500]:
        doc_id = f"art-{hashlib.sha256(article['url'].encode()).hexdigest()[:16]}"
        ref = db.collection('articles').document(doc_id)
        batch.set(ref, {
            'url': article['url'],
            'title': article['title'],
            'source': article['source'],
            'published_at': article.get('published_at'),
            'content_snippet': article.get('content', '')[:500],
            'ingested_at': firestore.SERVER_TIMESTAMP,
        }, merge=True)
        stored += 1
    batch.commit()
    return stored
```

URL-based deduplication via SHA-256 hash prefix. Batch writes capped at 500 (Firestore's batch limit). `merge=True` preserves any AI-enriched fields from previous ingestion runs. The `content_snippet` is truncated to 500 characters to keep document size manageable — full content lives in a separate `article_content` collection for the analysis pipeline.

The trigger endpoint now calls the real function and updates a Firestore `ingestion_runs` document with phase progress. The endpoint returns 202 immediately and runs the pipeline in a background task. The progress document tracks four phases: `loading_sources`, `fetching_feeds`, `storing_articles`, and `complete`. Each phase update includes a timestamp and a count (sources loaded, feeds fetched, articles stored).

The dashboard button polls this progress document every 3 seconds and displays the current phase with elapsed time. If the run takes longer than 5 minutes, the button shows a warning and offers a cancel action. If a run is already active when the button is clicked, the endpoint returns 409 Conflict and the button shows "Ingestion already running" with the time elapsed since the active run started.

The result: log in, click the button, watch 128 RSS feeds get ingested into Firestore in real time. No mock data, no cron dependency, no separate terminal window running a script.

The separation between `articles` and `article_content` collections is worth explaining. Article metadata (URL, title, source, timestamp) is queried frequently for listings, filters, and trending calculations. Full article content (the complete text, up to 50KB per article) is only needed when a user clicks into a specific article or when the analysis pipeline processes it. Keeping them in separate collections means listing queries stay fast — they read small documents from the `articles` collection without pulling the full text. The analysis pipeline reads from `article_content` in batch, where the per-document overhead doesn't matter.

## What I Learned

**Competitive strategy docs clarify product scope.** Writing down "we do X, they do Y, the gap is Z" forces precision about what you're actually building. git-with-intent kept creeping toward PR-level review features — adding diff summaries, suggesting reviewers, generating PR descriptions. The competitive map made it clear: stay at commit-level, where nobody else operates. Let CodeRabbit own PR review. Own the commit.

**Wire the whole pipeline before polishing any piece.** Perception had a good mock, a good endpoint, and a good button — all disconnected. Connecting them took one commit and delivered more user value than the previous five commits of individual improvements.

**Model benchmarks need difficulty stratification.** A single accuracy number (97%, 91%) hides the interesting signal. Both models handle clear-cut commits identically. The divergence is entirely in the ambiguous 15% — commits where even a human reviewer would debate the classification. Reporting accuracy on the ambiguous subset separately gives a much clearer picture of which model is worth the latency and cost tradeoff.

**Separate metadata from content in document stores.** Perception's split between `articles` (metadata) and `article_content` (full text) keeps listing queries fast. If full text lived in the metadata document, every list render would read 50KB per article instead of 500 bytes. This pattern applies anywhere you have a list-detail UI backed by a document database.

**Related Posts:**
- [git-with-intent v0.9 to v0.10: Docker Upgrades, README Rewrites, and Strategic Research](/posts/git-with-intent-v090-v0100-docker-upgrades/)
- [Perception Dashboard: Wiring Real Triggers, Topic Watchlists, and the BSL-1.1 Decision](/posts/perception-dashboard-real-triggers-topic-watchlists/)
- [Architecture Reboot: git-with-intent Connector Framework and GA Hardening](/posts/gwi-architecture-reboot-connector-framework/)
