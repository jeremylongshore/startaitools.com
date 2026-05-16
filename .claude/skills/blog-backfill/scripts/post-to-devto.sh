#!/usr/bin/env bash
# post-to-devto.sh — Cross-post a markdown blog post to Dev.to
#
# Usage: ./post-to-devto.sh <post.md> [--draft]
#
# Requires: DEVTO_API_KEY environment variable
# Sets canonical_url to startaitools.com BY DEFAULT.
# Override: set CANONICAL_OVERRIDE env var to a URL to use that instead.
# (Used for SOW-deliverable cases where canonical lives on a partner domain,
# e.g. CANONICAL_OVERRIDE="https://kobiton.com/blog/..." for Kobiton-canonical
# M2 blogs. Cron jobs don't set this, so default startaitools-canonical is
# preserved for personal-blog daily backfills.)

set -euo pipefail

if [[ -z "${DEVTO_API_KEY:-}" ]]; then
  echo "SKIP: DEVTO_API_KEY not set, skipping Dev.to cross-post" >&2
  exit 0
fi

input="${1:?Usage: $0 <post.md> [--draft]}"
draft_mode=false
[[ "${2:-}" == "--draft" ]] && draft_mode=true

# Parse Astro YAML frontmatter
title=$(sed -n 's/^title: *"\(.*\)" *$/\1/p' "$input" | head -1)
description=$(sed -n 's/^description: *"\(.*\)" *$/\1/p' "$input" | head -1)
date=$(sed -n 's/^date: *"\(.*\)" *$/\1/p' "$input" | head -1)
# Extract tags as comma-separated, max 4 for Dev.to
# Dev.to tags: alphanumeric only, no hyphens, max 4
tags_raw=$(sed -n 's/^tags: *\[\(.*\)\] *$/\1/p' "$input" | head -1)
tags=$(echo "$tags_raw" | tr ',' '\n' | sed 's/^ *"//;s/" *$//' | sed 's/-//g' | head -4 | paste -sd ',' -)

slug=$(basename "$input" .md)
canonical_url="${CANONICAL_OVERRIDE:-https://startaitools.com/posts/${slug}/}"

# Extract body (everything after second ---)
body=$(awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$input")

# Build JSON payload
published=true
$draft_mode && published=false

json_payload=$(jq -n \
  --arg title "$title" \
  --arg body "$body" \
  --arg tags "$tags" \
  --arg canonical "$canonical_url" \
  --arg desc "$description" \
  --argjson published "$published" \
  '{
    article: {
      title: $title,
      body_markdown: $body,
      published: $published,
      tags: ($tags | split(",")),
      canonical_url: $canonical,
      description: $desc
    }
  }')

echo "Publishing to Dev.to: $title" >&2
echo "  Canonical: $canonical_url" >&2
echo "  Tags: $tags" >&2
echo "  Published: $published" >&2

response=$(curl -s -w "\n%{http_code}" \
  -X POST "https://dev.to/api/articles" \
  -H "Content-Type: application/json" \
  -H "api-key: ${DEVTO_API_KEY}" \
  -d "$json_payload")

http_code=$(echo "$response" | tail -1)
body_response=$(echo "$response" | sed '$d')

if [[ "$http_code" -ge 200 ]] && [[ "$http_code" -lt 300 ]]; then
  url=$(echo "$body_response" | jq -r '.url // "unknown"')
  id=$(echo "$body_response" | jq -r '.id // "unknown"')
  echo "  Published: $url (id: $id)" >&2
  echo "$url"
else
  echo "  ERROR: HTTP $http_code" >&2
  echo "$body_response" | jq . 2>/dev/null || echo "$body_response" >&2
  exit 1
fi
