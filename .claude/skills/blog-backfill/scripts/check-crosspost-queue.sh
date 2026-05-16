#!/usr/bin/env bash
# check-crosspost-queue.sh — Process pending cross-posts from the queue
#
# Usage: ./check-crosspost-queue.sh [--dry-run]
#
# Reads .crosspost-queue.json from the startaitools directory.
# For each entry past its publish_after timestamp, runs the appropriate posting script.
# Updates the queue file with results.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BLOG_DIR="/home/jeremy/000-projects/blog/startaitools"
QUEUE_FILE="${BLOG_DIR}/.crosspost-queue.json"
ASTRO_SCRIPT="${SCRIPT_DIR}/transform-hugo-to-astro.sh"
DEVTO_SCRIPT="${SCRIPT_DIR}/post-to-devto.sh"
HASHNODE_SCRIPT="${SCRIPT_DIR}/post-to-hashnode.sh"
MEDIUM_SCRIPT="${SCRIPT_DIR}/post-to-medium.sh"

dry_run=false
[[ "${1:-}" == "--dry-run" ]] && dry_run=true

# Load env
if [[ -f "${BLOG_DIR}/.env" ]]; then
  set -a
  source "${BLOG_DIR}/.env"
  set +a
fi

if [[ ! -f "$QUEUE_FILE" ]]; then
  echo "No cross-post queue found at $QUEUE_FILE" >&2
  exit 0
fi

now=$(date -u +%s)
queue=$(cat "$QUEUE_FILE")
count=$(echo "$queue" | jq 'length')

if [[ "$count" -eq 0 ]]; then
  echo "Cross-post queue is empty." >&2
  exit 0
fi

echo "Processing cross-post queue ($count entries)..." >&2
processed=0

for i in $(seq 0 $((count - 1))); do
  entry=$(echo "$queue" | jq ".[$i]")
  slug=$(echo "$entry" | jq -r '.slug')
  title=$(echo "$entry" | jq -r '.title // .slug')
  canonical=$(echo "$entry" | jq -r '.canonical_url')

  echo "" >&2
  echo "=== $slug ===" >&2

  # Find the Hugo source file
  hugo_file="${BLOG_DIR}/content/posts/${slug}.md"
  if [[ ! -f "$hugo_file" ]]; then
    echo "  WARN: Hugo source not found at $hugo_file, skipping" >&2
    continue
  fi

  # Transform to Astro format in a temp file for the posting scripts
  astro_tmp="/tmp/crosspost-${slug}.md"
  if [[ -x "$ASTRO_SCRIPT" ]]; then
    "$ASTRO_SCRIPT" "$hugo_file" "$astro_tmp" 2>/dev/null || cp "$hugo_file" "$astro_tmp"
  else
    cp "$hugo_file" "$astro_tmp"
  fi

  # --- Dev.to ---
  devto_status=$(echo "$entry" | jq -r '.devto.status // "none"')
  devto_after=$(echo "$entry" | jq -r '.devto.publish_after // "1970-01-01T00:00:00Z"')
  devto_ts=$(date -d "$devto_after" +%s 2>/dev/null || echo 0)

  if [[ "$devto_status" == "pending" ]] && [[ "$now" -ge "$devto_ts" ]]; then
    if $dry_run; then
      echo "  DRY RUN: Would post to Dev.to" >&2
    elif [[ -n "${DEVTO_API_KEY:-}" ]]; then
      echo "  Posting to Dev.to..." >&2
      if devto_url=$("$DEVTO_SCRIPT" "$astro_tmp" 2>&1); then
        queue=$(echo "$queue" | jq ".[${i}].devto.status = \"published\" | .[${i}].devto.url = \"${devto_url}\" | .[${i}].devto.published_at = \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"")
        echo "  Dev.to: published" >&2
        processed=$((processed + 1))
        echo "$queue" | jq '.' > "$QUEUE_FILE"
      else
        echo "  Dev.to: FAILED — $devto_url" >&2
        queue=$(echo "$queue" | jq ".[${i}].devto.status = \"failed\" | .[${i}].devto.error = \"$(echo "$devto_url" | tail -1 | sed 's/"/\\"/g')\"")
        echo "$queue" | jq '.' > "$QUEUE_FILE"
      fi
    else
      echo "  SKIP: DEVTO_API_KEY not set" >&2
    fi
  elif [[ "$devto_status" == "pending" ]]; then
    echo "  Dev.to: waiting until $(date -d "@$devto_ts" '+%Y-%m-%d %H:%M')" >&2
  fi

  # --- Hashnode ---
  hashnode_status=$(echo "$entry" | jq -r '.hashnode.status // "none"')
  hashnode_after=$(echo "$entry" | jq -r '.hashnode.publish_after // "1970-01-01T00:00:00Z"')
  hashnode_ts=$(date -d "$hashnode_after" +%s 2>/dev/null || echo 0)

  if [[ "$hashnode_status" == "pending" ]] && [[ "$now" -ge "$hashnode_ts" ]]; then
    if $dry_run; then
      echo "  DRY RUN: Would post to Hashnode" >&2
    elif [[ -n "${HASHNODE_PAT:-}" ]] && [[ -n "${HASHNODE_PUBLICATION_ID:-}" ]]; then
      echo "  Posting to Hashnode..." >&2
      if hashnode_url=$("$HASHNODE_SCRIPT" "$astro_tmp" 2>&1); then
        queue=$(echo "$queue" | jq ".[${i}].hashnode.status = \"published\" | .[${i}].hashnode.url = \"${hashnode_url}\" | .[${i}].hashnode.published_at = \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"")
        echo "  Hashnode: published" >&2
        processed=$((processed + 1))
        echo "$queue" | jq '.' > "$QUEUE_FILE"
      else
        echo "  Hashnode: FAILED — $hashnode_url" >&2
        queue=$(echo "$queue" | jq ".[${i}].hashnode.status = \"failed\" | .[${i}].hashnode.error = \"$(echo "$hashnode_url" | tail -1 | sed 's/"/\\"/g')\"")
        echo "$queue" | jq '.' > "$QUEUE_FILE"
      fi
    else
      echo "  SKIP: HASHNODE_PAT or HASHNODE_PUBLICATION_ID not set" >&2
    fi
  elif [[ "$hashnode_status" == "pending" ]]; then
    echo "  Hashnode: waiting until $(date -d "@$hashnode_ts" '+%Y-%m-%d %H:%M')" >&2
  fi

  # --- Medium ---
  medium_status=$(echo "$entry" | jq -r '.medium.status // "none"')
  medium_after=$(echo "$entry" | jq -r '.medium.publish_after // "1970-01-01T00:00:00Z"')
  medium_ts=$(date -d "$medium_after" +%s 2>/dev/null || echo 0)

  if [[ "$medium_status" == "pending" ]] && [[ "$now" -ge "$medium_ts" ]]; then
    if $dry_run; then
      echo "  DRY RUN: Would post to Medium" >&2
    elif [[ -n "${MEDIUM_INTEGRATION_TOKEN:-}" ]]; then
      echo "  Posting to Medium..." >&2
      if medium_url=$("$MEDIUM_SCRIPT" "$astro_tmp" 2>&1); then
        queue=$(echo "$queue" | jq ".[${i}].medium.status = \"published\" | .[${i}].medium.url = \"${medium_url}\" | .[${i}].medium.published_at = \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"")
        echo "  Medium: published" >&2
        processed=$((processed + 1))
        echo "$queue" | jq '.' > "$QUEUE_FILE"
      else
        echo "  Medium: FAILED — $medium_url" >&2
        queue=$(echo "$queue" | jq ".[${i}].medium.status = \"failed\" | .[${i}].medium.error = \"$(echo "$medium_url" | tail -1 | sed 's/"/\\"/g')\"")
        echo "$queue" | jq '.' > "$QUEUE_FILE"
      fi
    else
      echo "  SKIP: MEDIUM_INTEGRATION_TOKEN not set" >&2
    fi
  elif [[ "$medium_status" == "pending" ]]; then
    echo "  Medium: waiting until $(date -d "@$medium_ts" '+%Y-%m-%d %H:%M')" >&2
  fi

  # Clean up temp file
  rm -f "$astro_tmp"
done

# Remove fully-completed entries (all 3 platforms done or failed, emails sent)
updated_queue=$(echo "$queue" | jq '[.[] | select(
  (.devto.status == "pending") or
  (.hashnode.status == "pending") or
  (.medium.status == "pending")
)]')

completed=$(echo "$queue" | jq '[.[] | select(
  (.devto.status != "pending") and
  (.hashnode.status != "pending") and
  (.medium.status != "pending")
)] | length')

# Write updated queue
echo "$updated_queue" | jq '.' > "$QUEUE_FILE"

echo "" >&2
echo "Queue processed: $processed published, $completed completed entries removed." >&2
echo "Remaining in queue: $(echo "$updated_queue" | jq 'length')" >&2
