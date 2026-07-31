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
BLOG_DIR="${BLOG_DIR:-/home/jeremy/000-projects/blog/startaitools}"
QUEUE_FILE="${CROSSPOST_QUEUE_FILE:-${BLOG_DIR}/.crosspost-queue.json}"
ASTRO_SCRIPT="${ASTRO_SCRIPT:-${SCRIPT_DIR}/transform-hugo-to-astro.sh}"
DEVTO_SCRIPT="${DEVTO_SCRIPT:-${SCRIPT_DIR}/post-to-devto.sh}"
HASHNODE_SCRIPT="${HASHNODE_SCRIPT:-${SCRIPT_DIR}/post-to-hashnode.sh}"
# Medium API channel retired 2026-07-05 (manual via the posting packet now).

dry_run=false
[[ "${1:-}" == "--dry-run" ]] && dry_run=true

# shellcheck source=../../../../scripts/blog/lib-cron-common.sh
source "$BLOG_DIR/scripts/blog/lib-cron-common.sh"

# Load env — the API tokens (HASHNODE_PAT, HASHNODE_PUBLICATION_ID, DEVTO_API_KEY)
# live in the PARENT blog/.env (per SKILL.md + references/crosspost-queue.md), NOT
# ${BLOG_DIR}/.env (startaitools/.env, which does not exist). Sourcing only the
# local path was a silent no-op, so cross-posts SKIPped (tokens never loaded) — the
# Dev.to/Hashnode auto-cross-post had been dead. Try the parent first, local as fallback.
for _envf in "$(dirname "$BLOG_DIR")/.env" "${BLOG_DIR}/.env"; do
  if [[ -f "$_envf" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$_envf"
    set +a
    break
  fi
done

if [[ ! -f "$QUEUE_FILE" ]]; then
  echo "No cross-post queue found at $QUEUE_FILE" >&2
  exit 0
fi

now=$(date -u +%s)
queue=$(cat "$QUEUE_FILE")
count=$(echo "$queue" | jq 'length')
tmp_root=$(mktemp -d)
trap 'rm -rf "$tmp_root"' EXIT

if [[ "$count" -eq 0 ]]; then
  echo "Cross-post queue is empty." >&2
  exit 0
fi

echo "Processing cross-post queue ($count entries)..." >&2
processed=0

for i in $(seq 0 $((count - 1))); do
  entry=$(echo "$queue" | jq ".[$i]")
  slug=$(echo "$entry" | jq -r '.slug')
  canonical_url=$(echo "$entry" | jq -r '.canonical_url')

  echo "" >&2
  echo "=== $slug ===" >&2

  # Find the Hugo source file
  hugo_file="${BLOG_DIR}/content/posts/${slug}.md"
  if [[ ! -f "$hugo_file" ]]; then
    echo "  WARN: Hugo source not found at $hugo_file, skipping" >&2
    continue
  fi

  # Transform to Astro format in a temp file for the posting scripts
  astro_tmp="${tmp_root}/${slug}.md"
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
      devto_err="${tmp_root}/${slug}.devto.err"
      if devto_url=$(CANONICAL_OVERRIDE="$canonical_url" "$DEVTO_SCRIPT" "$astro_tmp" 2>"$devto_err") &&
        [[ "$devto_url" == https://* ]]; then
        cat "$devto_err" >&2
        devto_url=$(printf '%s\n' "$devto_url" | tail -1)
        queue=$(printf '%s\n' "$queue" | jq --arg url "$devto_url" --arg at "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
          ".[${i}].devto.status = \"published\" | .[${i}].devto.url = \$url | .[${i}].devto.published_at = \$at | del(.[${i}].devto.error, .[${i}].devto.retry_after)")
        echo "  Dev.to: published" >&2
        processed=$((processed + 1))
        printf '%s\n' "$queue" | atomic_json_write "$QUEUE_FILE"
      else
        cat "$devto_err" >&2
        devto_error=$(tail -1 "$devto_err")
        [[ -n "$devto_error" ]] || devto_error="posting script returned no valid URL"
        retry_after=$(date -u -d '+15 minutes' +%Y-%m-%dT%H:%M:%SZ)
        echo "  Dev.to: retryable failure — $devto_error" >&2
        queue=$(printf '%s\n' "$queue" | jq --arg error "$devto_error" --arg retry "$retry_after" \
          ".[${i}].devto.status = \"pending\" | .[${i}].devto.error = \$error | .[${i}].devto.publish_after = \$retry | .[${i}].devto.retry_after = \$retry | .[${i}].devto.attempts = ((.[${i}].devto.attempts // 0) + 1)")
        printf '%s\n' "$queue" | atomic_json_write "$QUEUE_FILE"
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
      hashnode_err="${tmp_root}/${slug}.hashnode.err"
      if hashnode_url=$(CANONICAL_OVERRIDE="$canonical_url" "$HASHNODE_SCRIPT" "$astro_tmp" 2>"$hashnode_err") &&
        [[ "$hashnode_url" == https://* ]]; then
        cat "$hashnode_err" >&2
        hashnode_url=$(printf '%s\n' "$hashnode_url" | tail -1)
        queue=$(printf '%s\n' "$queue" | jq --arg url "$hashnode_url" --arg at "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
          ".[${i}].hashnode.status = \"published\" | .[${i}].hashnode.url = \$url | .[${i}].hashnode.published_at = \$at | del(.[${i}].hashnode.error, .[${i}].hashnode.retry_after)")
        echo "  Hashnode: published" >&2
        processed=$((processed + 1))
        printf '%s\n' "$queue" | atomic_json_write "$QUEUE_FILE"
      else
        cat "$hashnode_err" >&2
        hashnode_error=$(tail -1 "$hashnode_err")
        [[ -n "$hashnode_error" ]] || hashnode_error="posting script returned no valid URL"
        retry_after=$(date -u -d '+15 minutes' +%Y-%m-%dT%H:%M:%SZ)
        echo "  Hashnode: retryable failure — $hashnode_error" >&2
        queue=$(printf '%s\n' "$queue" | jq --arg error "$hashnode_error" --arg retry "$retry_after" \
          ".[${i}].hashnode.status = \"pending\" | .[${i}].hashnode.error = \$error | .[${i}].hashnode.publish_after = \$retry | .[${i}].hashnode.retry_after = \$retry | .[${i}].hashnode.attempts = ((.[${i}].hashnode.attempts // 0) + 1)")
        printf '%s\n' "$queue" | atomic_json_write "$QUEUE_FILE"
      fi
    else
      echo "  SKIP: HASHNODE_PAT or HASHNODE_PUBLICATION_ID not set" >&2
    fi
  elif [[ "$hashnode_status" == "pending" ]]; then
    echo "  Hashnode: waiting until $(date -d "@$hashnode_ts" '+%Y-%m-%d %H:%M')" >&2
  fi

  # --- Medium ---
  # Retired as an API channel (post-to-medium.sh removed 2026-07-05). Medium is
  # now a MANUAL step in the Ezekiel posting packet (via Import). Entries land
  # with medium.status="skipped"; nothing to do here. Left as a no-op comment so
  # the completed-entry filter below (which checks .medium.status != "pending")
  # still resolves — skipped counts as terminal.

done

completed=$(echo "$queue" | jq '[.[] | select(
  (.devto.status != "pending") and
  (.hashnode.status != "pending") and
  (.medium.status != "pending")
)] | length')

# Retain terminal entries as the durable idempotency record. Deleting completed
# rows made later reconciliation unable to distinguish "never queued" from
# "already posted", which can create duplicate external articles.
printf '%s\n' "$queue" | atomic_json_write "$QUEUE_FILE"

echo "" >&2
echo "Queue processed: $processed published, $completed terminal entries retained." >&2
echo "Pending entries: $(echo "$queue" | jq '[.[] | select(.devto.status == "pending" or .hashnode.status == "pending" or .medium.status == "pending")] | length')" >&2
