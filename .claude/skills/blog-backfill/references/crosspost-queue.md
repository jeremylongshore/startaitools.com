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
  "hashnode": { "status": "skipped", "error": "Hashnode GraphQL API moved to paid access 2026-05-13; free cross-posting retired." },
  "medium": { "status": "skipped", "error": "No MEDIUM_INTEGRATION_TOKEN; Medium API cross-posting retired." },
  "substack_emailed": false,
  "x_thread_emailed": false
}
```

If the queue file already exists, append to the array. If not, create it with `[entry]`.

## Retired channels (2026-06-26)

Only **Dev.to** is an active API cross-post channel. Hashnode and Medium are queued as `skipped` by default so the queue stays drainable and the daily run stops re-accruing dead-channel failures:

- **Hashnode** moved its GraphQL API to a **paid** offering on 2026-05-13 (`gql.hashnode.com` 301-redirects to the paid-access changelog). The free API used by `post-to-hashnode.sh` no longer works. Re-enable only with a paid plan + updated auth.
- **Medium** has no `MEDIUM_INTEGRATION_TOKEN` configured (Medium stopped issuing new integration tokens). Re-enable by setting the token in `~/000-projects/blog/.env` and flipping the template back to `pending`.

Substack (manual paste, no API) and the X/LinkedIn social bundles are unaffected.

## Stagger timing

- **Immediate:** Publish to startaitools.com (canonical)
- **+24h:** Dev.to (the one active API channel)
- Hashnode / Medium: retired (see above)

## Process the queue

After adding entries, immediately run the queue processor to handle any that are already past their `publish_after` time (e.g., when backfilling old posts):

```bash
/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/scripts/check-crosspost-queue.sh
```

## Queue processor behavior

- Reads `.crosspost-queue.json`
- For each entry where `publish_after` is past: runs the appropriate posting script
- Updates status to `"published"` with URL and timestamp, or `"failed"` with error
- Removes fully-completed entries (every platform in a terminal state: published, failed, or skipped — i.e. none still `pending`)
- Skips gracefully if API keys are not set

## Substack draft (no API)

```bash
/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/scripts/post-to-substack.sh \
  /home/jeremy/000-projects/claude-code-plugins/marketplace/src/content/blog-posts/SLUG.md
```

Generates ready-to-paste markdown in `$SUBSTACK_OUTPUT_DIR` with canonical attribution footer. Requires `SUBSTACK_OUTPUT_DIR` env var.
