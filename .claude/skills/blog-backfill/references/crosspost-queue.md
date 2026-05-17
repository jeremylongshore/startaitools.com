# Step 4: Cross-Post Queue (Staggered Publishing)

Add each published post to the cross-post queue with staggered timing. The queue is processed at the start of each `/blog-backfill` run (Phase 0) or manually via `check-crosspost-queue.sh`.

## Queue schema

Add an entry to `~/000-projects/blog/startaitools/.crosspost-queue.json`:

```json
{
  "slug": "SLUG",
  "title": "POST TITLE",
  "canonical_url": "https://startaitools.com/posts/SLUG/",
  "published_at": "NOW_ISO8601",
  "devto": { "status": "pending", "publish_after": "NOW+24H_ISO8601" },
  "hashnode": { "status": "pending", "publish_after": "NOW+24H_ISO8601" },
  "medium": { "status": "pending", "publish_after": "NOW+48H_ISO8601" },
  "substack_emailed": false,
  "x_thread_emailed": false
}
```

If the queue file already exists, append to the array. If not, create it with `[entry]`.

## Stagger timing

- **Immediate:** Publish to startaitools.com (canonical)
- **+24h:** Dev.to + Hashnode
- **+48h:** Medium

## Process the queue

After adding entries, immediately run the queue processor to handle any that are already past their `publish_after` time (e.g., when backfilling old posts):

```bash
/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/scripts/check-crosspost-queue.sh
```

## Queue processor behavior

- Reads `.crosspost-queue.json`
- For each entry where `publish_after` is past: runs the appropriate posting script
- Updates status to `"published"` with URL and timestamp, or `"failed"` with error
- Removes fully-completed entries (all 3 platforms done or failed)
- Skips gracefully if API keys are not set

## Substack draft (no API)

```bash
/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/scripts/post-to-substack.sh \
  /home/jeremy/000-projects/claude-code-plugins/marketplace/src/content/blog-posts/SLUG.md
```

Generates ready-to-paste markdown in `$SUBSTACK_OUTPUT_DIR` with canonical attribution footer. Requires `SUBSTACK_OUTPUT_DIR` env var.
