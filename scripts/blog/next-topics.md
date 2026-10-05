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
   queue. Also `top`, `list`, `consume`, `cluster`, `validate`.
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

## Clusters: merging repeated near-duplicates

The weekly refresh re-proposes the same reader problem under new slugs, so one
problem can pile up as many open rows. `cluster` folds them into one row with
child questions, without deleting anything:

```bash
python3 scripts/blog/next-topics.py cluster --spec spec.json --dry-run   # preview
python3 scripts/blog/next-topics.py cluster --spec spec.json
```

The spec names the cluster (`topic`, `slug_hint`, `score`, `target_tier`), the
rows to fold in (`merged_from`), and the `children`, each with a `key`, a
`question`, its `source_ids`, and optional `partial_source_ids` for rows that
only partly belong (those stay open). The command refuses unknown ids, rows that
are not open, duplicate child keys, and a partial source listed as merged.

Each folded row keeps every field and gets `status: "merged"` plus
`merged_into: <cluster id>`. `top` and `list` hide merged rows (`list --all`
shows them), `ingest` will not re-add a merged row's exact slug, and `validate`
checks that merged rows and their cluster point at each other.

A cluster is consumed one child at a time, and only with the published URL:

```bash
python3 scripts/blog/next-topics.py consume <cluster-id> --child q1 \
  --by <post-slug> --url https://<published-url>/
```

Consume a child only after the lander has verified the post is live. The cluster
row turns `consumed` when every child is. Consuming a merged row directly is
refused with a pointer to its cluster.

## Demand evidence on existing rows (E03, 2026-10-05)

An optional, manually run research step may check how people search for at most
five existing **open** rows and stage one `demand_check` object per row:

```json
{"queue_id": "nt-...", "checked_at": "ISO8601",
 "query_forms": [{"q": "...", "source": "serp", "evidence_url": "https://..."}],
 "serp_top": [{"title": "...", "url": "https://..."}], "intent": "...", "gap": "...",
 "demand": "observed|weak|none|estimated", "merge_of": ["nt-..."],
 "recommended_title_form": null, "uncertainty": "what could not be observed"}
```

```bash
python3 scripts/blog/next-topics.py annotate --staging demand.staging.jsonl --dry-run
python3 scripts/blog/next-topics.py annotate --staging demand.staging.jsonl
```

`annotate` writes the object under one key, `demand`, on the SAME row. It never
adds, removes, reorders, rescores or re-topics a row: search evidence describes a
row a person already queued and never chooses what gets written. Every query form
needs a source URL unless `demand` is `estimated`; an `uncertainty` statement is
always required; `merge_of` only flags likely duplicates (folding them is still
the explicit `cluster` command). One invalid object refuses the whole batch and
leaves the queue bytes unchanged. Readers that do not know the key ignore it, so
rollback is simply not running the step.

The daily counterpart, search phrasing for a post whose subject is already fixed
by the day's finding, is validated by `python3 -B -m blogpipe search-phrasing`
(scripts/blog/blogpipe/phrasing.py). It is off unless `BLOG_SEARCH_PHRASING=1`
and never fails a run: missing or bad output becomes a recorded skip.

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
