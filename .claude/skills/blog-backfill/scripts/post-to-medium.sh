#!/usr/bin/env bash
# post-to-medium.sh — Cross-post a markdown blog post to Medium
#
# Usage: ./post-to-medium.sh <post.md> [--draft]
#
# Requires: MEDIUM_INTEGRATION_TOKEN environment variable
# Sets canonicalUrl to startaitools.com
# Medium has no update API — posts are create-only. Uses .medium-published.log to avoid duplicates.

set -euo pipefail

if [[ -z "${MEDIUM_INTEGRATION_TOKEN:-}" ]]; then
  echo "SKIP: MEDIUM_INTEGRATION_TOKEN not set, skipping Medium cross-post" >&2
  exit 0
fi

input="${1:?Usage: $0 <post.md> [--draft]}"
draft_mode=false
[[ "${2:-}" == "--draft" ]] && draft_mode=true

# Parse Astro YAML frontmatter
title=$(sed -n 's/^title: *"\(.*\)" *$/\1/p' "$input" | head -1)
tags_raw=$(sed -n 's/^tags: *\[\(.*\)\] *$/\1/p' "$input" | head -1)
# Medium: strip hyphens, max 5 tags
tags=$(echo "$tags_raw" | tr ',' '\n' | sed 's/^ *"//;s/" *$//' | sed 's/-//g' | head -5 | jq -R . | jq -s '.')

slug=$(basename "$input" .md)
canonical_url="${CANONICAL_OVERRIDE:-https://startaitools.com/posts/${slug}/}"

# Duplicate guard — Medium has no update API
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
log_file="${SCRIPT_DIR}/.medium-published.log"
if [[ -f "$log_file" ]] && command grep -q "^${slug}$" "$log_file" 2>/dev/null; then
  echo "SKIP: ${slug} already published to Medium (found in .medium-published.log)" >&2
  exit 0
fi

# Extract body (everything after second ---)
body=$(awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$input")

# Step 1: Get author ID
echo "Fetching Medium author ID..." >&2
me_response=$(curl -s -w "\n%{http_code}" \
  -H "Authorization: Bearer ${MEDIUM_INTEGRATION_TOKEN}" \
  -H "Content-Type: application/json" \
  "https://api.medium.com/v1/me")

http_code=$(echo "$me_response" | tail -1)
me_body=$(echo "$me_response" | sed '$d')

if [[ "$http_code" -lt 200 ]] || [[ "$http_code" -ge 300 ]]; then
  echo "  ERROR fetching author: HTTP $http_code" >&2
  echo "$me_body" | jq . 2>/dev/null || echo "$me_body" >&2
  exit 1
fi

author_id=$(echo "$me_body" | jq -r '.data.id // empty')
if [[ -z "$author_id" ]]; then
  echo "  ERROR: No author ID in response" >&2
  echo "$me_body" | jq . 2>/dev/null || echo "$me_body" >&2
  exit 1
fi

echo "  Author ID: $author_id" >&2

# Step 2: Create post
publish_status="public"
$draft_mode && publish_status="draft"

json_payload=$(jq -n \
  --arg title "$title" \
  --arg content "$body" \
  --arg canonical "$canonical_url" \
  --argjson tags "$tags" \
  --arg status "$publish_status" \
  '{
    title: $title,
    contentFormat: "markdown",
    content: $content,
    canonicalUrl: $canonical,
    tags: $tags,
    publishStatus: $status
  }')

echo "Publishing to Medium: $title" >&2
echo "  Canonical: $canonical_url" >&2
echo "  Status: $publish_status" >&2

response=$(curl -s -w "\n%{http_code}" \
  -X POST "https://api.medium.com/v1/users/${author_id}/posts" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${MEDIUM_INTEGRATION_TOKEN}" \
  -d "$json_payload")

http_code=$(echo "$response" | tail -1)
body_response=$(echo "$response" | sed '$d')

if [[ "$http_code" -ge 200 ]] && [[ "$http_code" -lt 300 ]]; then
  url=$(echo "$body_response" | jq -r '.data.url // "unknown"')
  id=$(echo "$body_response" | jq -r '.data.id // "unknown"')
  echo "  Published: $url (id: $id)" >&2
  # Record in duplicate guard log
  echo "$slug" >> "$log_file"
  echo "$url"
else
  echo "  ERROR: HTTP $http_code" >&2
  echo "$body_response" | jq . 2>/dev/null || echo "$body_response" >&2
  exit 1
fi
