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
  exit 1
fi

# One kernel lease covers outbound requests as well as result reconciliation.
# Children inherit it: a surviving request keeps a killed wrapper from being
# immediately duplicated. Kernel ownership expires when the last holder exits.
QUEUE_ROOT="$(cd "$(dirname "$QUEUE_FILE")" && pwd)"
CONSUMER_LOCK="$QUEUE_ROOT/.blog-crosspost-consumer.lock"
[[ ! -L "$CONSUMER_LOCK" ]] || { echo "Invalid symlinked consumer lock" >&2; exit 1; }
exec 8>"$CONSUMER_LOCK"
if ! flock -n 8; then
  echo "Cross-post consumer busy; this invocation performed no delivery." >&2
  exit 0
fi

# Atomic publication means a read-only snapshot needs no writer lock.
queue_state() {
  PYTHONPATH="$SCRIPT_DIR/../../../../scripts/blog${PYTHONPATH:+:$PYTHONPATH}" \
    python3 - "$QUEUE_FILE" <<'PYQUEUE'
import json
import sys
from pathlib import Path
from blog_publication_state import load_state
path = Path(sys.argv[1])
if not path.is_file():
    raise ValueError("cross-post queue is missing")
print(json.dumps(load_state(path)))
PYQUEUE
}
DISPATCH_SCRIPT="$SCRIPT_DIR/../../../../scripts/blog/blog_crosspost_dispatch.py"
if ! $dry_run; then
  python3 "$DISPATCH_SCRIPT" recover --queue "$QUEUE_FILE"
fi

now=$(date -u +%s)
queue=$(queue_state snapshot)
count=$(echo "$queue" | jq 'length')
tmp_root=$(mktemp -d)
trap 'rm -rf "$tmp_root"' EXIT

if [[ "$count" -eq 0 ]]; then
  echo "Cross-post queue is empty." >&2
  exit 0
fi

echo "Processing cross-post queue ($count entries)..." >&2
processed=0
problems=0

slugs=$(printf '%s\n' "$queue" | jq -r '.[].slug')
while IFS= read -r slug; do
  queue=$(queue_state snapshot)
  entry=$(printf '%s\n' "$queue" | jq -c --arg s "$slug" '.[] | select(.slug==$s)')
  [[ -n "$entry" ]] || { echo "Queue identity disappeared: $slug" >&2; exit 1; }
  canonical_url=$(echo "$entry" | jq -r '.canonical_url')

  echo "" >&2
  echo "=== $slug ===" >&2

  # Find the Hugo source file
  hugo_file="${BLOG_DIR}/content/posts/${slug}.md"
  if [[ ! -f "$hugo_file" ]]; then
    echo "  WARN: Hugo source not found at $hugo_file, skipping" >&2
    if ! $dry_run && printf '%s\n' "$entry" | jq -e '.devto.status == "pending" or .hashnode.status == "pending"' >/dev/null; then
      problems=$((problems + 1))
    fi
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
      CANONICAL_OVERRIDE="$canonical_url" python3 "$DISPATCH_SCRIPT" dispatch \
        --queue "$QUEUE_FILE" --slug "$slug" --platform devto \
        --provider "$DEVTO_SCRIPT" --source "$astro_tmp"
      queue=$(queue_state snapshot)
      if [[ $(printf '%s\n' "$queue" | jq -r --arg s "$slug" '.[] | select(.slug==$s) | .devto.status') == "published" ]]; then
        processed=$((processed + 1))
      fi
    else
      echo "  ERROR: Due Dev.to delivery has no DEVTO_API_KEY" >&2
      problems=$((problems + 1))
    fi
  elif [[ "$devto_status" == "pending" ]]; then
    echo "  Dev.to: waiting until $(date -d "@$devto_ts" '+%Y-%m-%d %H:%M')" >&2
  fi

  # Reload the other destination after the external call; never act on the
  # pre-call snapshot if another writer has already advanced it.
  queue=$(queue_state snapshot)
  entry=$(printf '%s\n' "$queue" | jq -c --arg s "$slug" '.[] | select(.slug==$s)')
  [[ -n "$entry" ]] || { echo "Queue identity disappeared: $slug" >&2; exit 1; }

  # --- Hashnode ---
  hashnode_status=$(echo "$entry" | jq -r '.hashnode.status // "none"')
  hashnode_after=$(echo "$entry" | jq -r '.hashnode.publish_after // "1970-01-01T00:00:00Z"')
  hashnode_ts=$(date -d "$hashnode_after" +%s 2>/dev/null || echo 0)

  if [[ "$hashnode_status" == "pending" ]] && [[ "$now" -ge "$hashnode_ts" ]]; then
    if $dry_run; then
      echo "  DRY RUN: Would post to Hashnode" >&2
    elif [[ -n "${HASHNODE_PAT:-}" ]] && [[ -n "${HASHNODE_PUBLICATION_ID:-}" ]]; then
      echo "  Posting to Hashnode..." >&2
      CANONICAL_OVERRIDE="$canonical_url" python3 "$DISPATCH_SCRIPT" dispatch \
        --queue "$QUEUE_FILE" --slug "$slug" --platform hashnode \
        --provider "$HASHNODE_SCRIPT" --source "$astro_tmp"
      queue=$(queue_state snapshot)
      if [[ $(printf '%s\n' "$queue" | jq -r --arg s "$slug" '.[] | select(.slug==$s) | .hashnode.status') == "published" ]]; then
        processed=$((processed + 1))
      fi
    else
      echo "  ERROR: Due Hashnode delivery lacks required credentials" >&2
      problems=$((problems + 1))
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

done <<< "$slugs"

queue=$(queue_state snapshot)
completed=$(echo "$queue" | jq '[.[] | . as $row | select(
  (["published","skipped","n/a"] | index($row.devto.status)) != null and
  (["published","skipped","n/a"] | index($row.hashnode.status)) != null and
  (["published","skipped","n/a"] | index($row.medium.status)) != null
)] | length')

# Retain terminal entries as the durable idempotency record. Deleting completed
# rows made later reconciliation unable to distinguish "never queued" from
# "already posted", which can create duplicate external articles.

echo "" >&2
echo "Queue processed: $processed published, $completed terminal entries retained." >&2
echo "Pending entries: $(echo "$queue" | jq '[.[] | select(.devto.status == "pending" or .hashnode.status == "pending" or .medium.status == "pending")] | length')" >&2
held=$(echo "$queue" | jq '[.[] | select(.devto.status == "ambiguous" or .hashnode.status == "ambiguous" or .devto.status == "dispatching" or .hashnode.status == "dispatching" or .devto.status == "failed" or .hashnode.status == "failed")] | length')
echo "Held entries (verify remote acceptance before retry): $held" >&2
if ! $dry_run && (( held > 0 || problems > 0 )); then
  echo "ERROR: Cross-post delivery is incomplete; inspect held attempts, source identity and credentials. Do not reset ambiguous status without provider reconciliation." >&2
  exit 1
fi
