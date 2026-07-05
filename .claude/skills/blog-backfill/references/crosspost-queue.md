# Step 4: Cross-Post Queue (Staggered Publishing)

Add each published post to the cross-post queue with staggered timing. The queue is processed at the start of each `/blog-backfill` run (Phase 0) or manually via `check-crosspost-queue.sh`.

## Queue schema

**As of 2026-07-05 the queue is appended + processed by `scripts/blog/blog-land.sh`, not the skill** (see the WS1 inversion). The queue is now **API-cross-posts only** (Dev.to + Hashnode). The old `substack_emailed` / `x_thread_emailed` booleans are gone — per-destination "did-he-post" tracking moved to the **syndication ledger** (`.blog-syndication-ledger.json`), which the Ezekiel posting packet reads/updates. Do not resurrect those fields.

Queue entry schema (`~/000-projects/blog/startaitools/.crosspost-queue.json`):

```json
{
  "slug": "SLUG",
  "title": "POST TITLE",
  "canonical_url": "https://startaitools.com/posts/SLUG/",
  "published_at": "NOW_ISO8601",
  "tier": 2,
  "devto": { "status": "pending", "publish_after": "NOW+24H_ISO8601" },
  "hashnode": { "status": "pending", "publish_after": "NOW+24H_ISO8601" },
  "medium": { "status": "skipped", "error": "No MEDIUM_INTEGRATION_TOKEN; Medium API cross-posting retired (manual via the packet)." }
}
```

The land step only appends this entry for **Tier ≥ 2** posts (Tier 1 = startaitools + tonsofskills only). If the queue file already exists it appends to the array (atomic write + jq validation); otherwise it creates `[entry]`.

## Channel status (updated 2026-06-30)

**Dev.to** and **Hashnode** are active API cross-post channels. **Medium** is queued `skipped`.

- **Hashnode** — re-enabled 2026-06-30 on the paid **Pro** plan. The API moved to `https://gql-beta.hashnode.com/` with `Authorization: Bearer $HASHNODE_PAT` (per [Hashnode/gql-skill](https://github.com/Hashnode/gql-skill)); `post-to-hashnode.sh` updated (endpoint + Bearer + TOML/colon-safe parse). Token in `~/000-projects/blog/.env` (`HASHNODE_PAT`, chat-pasted — rotate when convenient). Publishes with `originalArticleURL` = the startaitools canonical.
- **Medium** has no `MEDIUM_INTEGRATION_TOKEN` (Medium stopped issuing tokens). Re-enable by setting the token in `~/000-projects/blog/.env` and flipping the template `medium` back to `pending`.

Substack (manual paste, no API) and the X/LinkedIn social bundles are unaffected.

## Stagger timing

- **Immediate:** Publish to startaitools.com (canonical)
- **+24h:** Dev.to + Hashnode
- Medium: retired (see above)

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

## Substack + Medium (manual — via the posting packet)

Substack and Medium are **manual** now (the `post-to-substack.sh` / `post-to-medium.sh`
API scripts were removed 2026-07-05). The Ezekiel posting packet
(`scripts/blog/blog-posting-packet.sh`) hands Ezekiel exact copy-paste steps + the
verbatim canonical URL for both. Nothing to script here.
