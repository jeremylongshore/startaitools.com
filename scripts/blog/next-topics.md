# The performance loop: `next-topics.jsonl`

Thread D Phase 1 (2026-07-16). The front of the funnel: turn what already
performed into what to write next, grounded in real traffic, not guesswork.

```
Umami content-performance  ->  content-seo agent (LLM)  ->  .next-topics.jsonl  ->  writers
```

Before this, the pipeline had post-hoc analytics (Umami, web-analytics) and a
tier-calibration loop, but nothing bridged "what performed" to "what to write
next." This is that bridge, built only from parts that already existed.

## The three pieces

1. **`next-topics-refresh.sh`** (cron, weekly). Mirrors `web-analytics-daily.sh`'s
   operational spine (pty-wrapped headless agent, wall-clock ceiling, fail-loud
   alerting, liveness heartbeat) but is independent of the blog pipeline: no git,
   no publish. It asks the `content-seo` agent to read real Umami content
   performance for startaitools.com (and tonsofskills.com) and PRODUCE ranked
   next-topic candidates into `.next-topics.staging.jsonl`, then runs
   `next-topics.py ingest`.
2. **`next-topics.py`** (deterministic). The land half. `ingest` validates each
   staged candidate, dedups against open items by `slug_hint`, assigns an id, and
   appends to `.next-topics.jsonl` atomically. A bad model run cannot corrupt the
   queue. Also `top`, `list`, `consume`, `validate`.
3. **`.next-topics.jsonl`** (repo root, gitignored, transient). The ranked queue
   writers consume. Gitignored so the daily blog cron's clean-tree preflight is
   never disturbed by a queue refresh.

## Queue schema (one JSON object per line)

```json
{
  "id": "nt-YYYYMMDD-NNN",
  "generated_at": "ISO8601",
  "topic": "short human title",
  "slug_hint": "kebab-slug",
  "angle": "the specific thesis or angle",
  "rationale": "why now, grounded in real traffic numbers",
  "source_signals": { "top_performer": "slug (N views)", "gap": "...", "cluster": "..." },
  "score": 0.0,
  "target_tier": 2,
  "status": "open",
  "consumed_by": null,
  "consumed_at": null
}
```

`score` (0.0 to 1.0) is ranking priority. `target_tier` 4 means the topic warrants
`/blog-research-article`; 1 to 3 feed `/blog-backfill`.

## How writers consume it

```bash
# highest-priority open topic (human readout)
python3 scripts/blog/next-topics.py top
# highest-priority Tier-4-worthy topic, as JSON
python3 scripts/blog/next-topics.py top --tier 4 --json
# after publishing, mark it consumed so it stops being suggested
python3 scripts/blog/next-topics.py consume <id-or-slug> --by <post-slug>
```

- **`/blog-research-article`**: when invoked without a specific topic or URL, it
  may pull the top open item (prefer `--tier 4`) as its subject, then `consume` it
  after publishing.
- **`/blog-backfill`**: date-driven, so it does not pick topics from the queue,
  but it may consult `top` for an ANGLE on the day's work when the queue's themes
  overlap what shipped.

## Cadence and cost

Weekly (topic strategy is not a daily signal). One bounded headless agent run.
Reuses the `content-seo` agent and the Umami access the web-analytics skill
already uses (`get_content_performance` MCP tool for Claude, Umami REST for Grok).

## Roadmap (later phases, not built here)

- **Phase 2 — trend discovery.** New `~/bin` monitors (HN, Reddit, Google Trends)
  feed topic candidates + a trend score into the same queue.
- **Phase 3 — live SEO keyword data.** A paid source (DataForSEO/Ahrefs) enriches
  ranking with volume/difficulty/SERP.
- **Virality.** A pre-publish headline/hook scorer over title candidates.
