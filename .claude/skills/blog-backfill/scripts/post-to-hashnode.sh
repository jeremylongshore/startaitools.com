#!/usr/bin/env bash
# post-to-hashnode.sh — Cross-post a markdown blog post to Hashnode
#
# Usage: ./post-to-hashnode.sh <post.md> [--draft]
#
# Requires: HASHNODE_PAT and HASHNODE_PUBLICATION_ID environment variables
# Sets originalArticleURL (canonical) to startaitools.com
# Two-step: createDraft → publishDraft

set -euo pipefail

if [[ -z "${HASHNODE_PAT:-}" ]]; then
  echo "SKIP: HASHNODE_PAT not set, skipping Hashnode cross-post" >&2
  exit 0
fi

if [[ -z "${HASHNODE_PUBLICATION_ID:-}" ]]; then
  echo "SKIP: HASHNODE_PUBLICATION_ID not set, skipping Hashnode cross-post" >&2
  exit 0
fi

input="${1:?Usage: $0 <post.md> [--draft]}"
draft_only=false
[[ "${2:-}" == "--draft" ]] && draft_only=true

# Parse Astro YAML frontmatter
title=$(sed -n 's/^title: *"\(.*\)" *$/\1/p' "$input" | head -1)
# Extract tags as array of {name, slug} objects
tags_raw=$(sed -n 's/^tags: *\[\(.*\)\] *$/\1/p' "$input" | head -1)

slug=$(basename "$input" .md)
canonical_url="${CANONICAL_OVERRIDE:-https://startaitools.com/posts/${slug}/}"

# Extract body (everything after second ---)
body=$(awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$input")

# Build tags array for Hashnode GraphQL
tags_gql="[]"
if [[ -n "$tags_raw" ]]; then
  tags_gql=$(echo "$tags_raw" | tr ',' '\n' | sed 's/^ *"//;s/" *$//' | head -5 | \
    jq -R '{name: ., slug: (. | gsub(" "; "-") | ascii_downcase)}' | jq -s '.')
fi

# Step 1: Create draft
echo "Creating Hashnode draft: $title" >&2
echo "  Canonical: $canonical_url" >&2

create_draft_query=$(cat <<'GRAPHQL'
mutation CreateDraft($input: CreateDraftInput!) {
  createDraft(input: $input) {
    draft {
      id
      title
    }
  }
}
GRAPHQL
)

draft_variables=$(jq -n \
  --arg title "$title" \
  --arg content "$body" \
  --arg pubId "$HASHNODE_PUBLICATION_ID" \
  --arg canonical "$canonical_url" \
  --argjson tags "$tags_gql" \
  '{
    input: {
      title: $title,
      contentMarkdown: $content,
      publicationId: $pubId,
      originalArticleURL: $canonical,
      tags: $tags
    }
  }')

draft_payload=$(jq -n \
  --arg query "$create_draft_query" \
  --argjson variables "$draft_variables" \
  '{ query: $query, variables: $variables }')

draft_response=$(curl -s -w "\n%{http_code}" \
  -X POST "https://gql.hashnode.com/" \
  -H "Content-Type: application/json" \
  -H "Authorization: ${HASHNODE_PAT}" \
  -d "$draft_payload")

http_code=$(echo "$draft_response" | tail -1)
draft_body=$(echo "$draft_response" | sed '$d')

# Detect API host redirect — observed 2026-05-27, every draft creation returns
# 301 from gql.hashnode.com via Cloudflare. Exit non-zero so the cross-post
# queue manager registers this as a failure and keeps the entry recoverable,
# rather than silently marking it "published" with an empty URL (which would
# remove it from the queue permanently). Tracked via bead startaitools-6jf.
if [[ "$http_code" == "301" ]] || [[ "$http_code" == "302" ]]; then
  echo "ENDPOINT_MOVED: Hashnode GraphQL returned HTTP $http_code from gql.hashnode.com" >&2
  echo "Investigate new endpoint URL before re-running post-to-hashnode.sh." >&2
  exit 1
fi

if [[ "$http_code" -lt 200 ]] || [[ "$http_code" -ge 300 ]]; then
  echo "  ERROR creating draft: HTTP $http_code" >&2
  echo "$draft_body" | jq . 2>/dev/null || echo "$draft_body" >&2
  exit 1
fi

draft_id=$(echo "$draft_body" | jq -r '.data.createDraft.draft.id // empty')
if [[ -z "$draft_id" ]]; then
  echo "  ERROR: No draft ID in response" >&2
  echo "$draft_body" | jq . 2>/dev/null || echo "$draft_body" >&2
  exit 1
fi

echo "  Draft created: $draft_id" >&2

if $draft_only; then
  echo "  Draft-only mode, skipping publish" >&2
  echo "$draft_id"
  exit 0
fi

# Step 2: Publish draft
publish_query=$(cat <<'GRAPHQL'
mutation PublishDraft($input: PublishDraftInput!) {
  publishDraft(input: $input) {
    post {
      id
      url
      title
    }
  }
}
GRAPHQL
)

publish_variables=$(jq -n --arg draftId "$draft_id" '{ input: { draftId: $draftId } }')

publish_payload=$(jq -n \
  --arg query "$publish_query" \
  --argjson variables "$publish_variables" \
  '{ query: $query, variables: $variables }')

publish_response=$(curl -s -w "\n%{http_code}" \
  -X POST "https://gql.hashnode.com/" \
  -H "Content-Type: application/json" \
  -H "Authorization: ${HASHNODE_PAT}" \
  -d "$publish_payload")

http_code=$(echo "$publish_response" | tail -1)
publish_body=$(echo "$publish_response" | sed '$d')

if [[ "$http_code" -ge 200 ]] && [[ "$http_code" -lt 300 ]]; then
  url=$(echo "$publish_body" | jq -r '.data.publishDraft.post.url // "unknown"')
  echo "  Published: $url" >&2
  echo "$url"
else
  echo "  ERROR publishing: HTTP $http_code" >&2
  echo "$publish_body" | jq . 2>/dev/null || echo "$publish_body" >&2
  exit 1
fi
