#!/usr/bin/env bash
# Independent, idempotent sweep for due Dev.to and Hashnode cross-posts.

set -uo pipefail

BLOG_DIR="${BLOG_DIR:-/home/jeremy/000-projects/blog/startaitools}"
PROCESSOR="$BLOG_DIR/.claude/skills/blog-backfill/scripts/check-crosspost-queue.sh"
LOG_DIR="${BLOG_CROSSPOST_LOG_DIR:-$HOME/.local/state/blog-crosspost-sweep}"
LOG="$LOG_DIR/run-$(date +%Y-%m-%d).log"
if [[ "${BLOG_CANARY:-0}" == "1" ]]; then
  echo "Canary refuses cross-post sweep side effects" >&2
  exit 1
fi
mkdir -p "$LOG_DIR"


# shellcheck source=./lib-cron-common.sh
source "$BLOG_DIR/scripts/blog/lib-cron-common.sh"
mkdir -p "$HOME/.local/state/intent-os/liveness"
: > "$HOME/.local/state/intent-os/liveness/blog-crosspost-sweep.beat"

finish() {
  local rc=$?
  liveness_markers "blog-crosspost-sweep" "$rc"
  if [ "$rc" -ne 0 ]; then
    cron_fail "blog-crosspost-sweep" "queue processor failed; see $LOG"
  fi
}
trap finish EXIT

if [ ! -x "$PROCESSOR" ]; then
  echo "FATAL: cross-post processor missing: $PROCESSOR" | tee -a "$LOG"
  exit 1
fi

{
  echo "[$(date -Is)] cross-post sweep start"
  processor_rc=0
  "$PROCESSOR" || processor_rc=$?
  if (( processor_rc != 0 )); then
    echo "[$(date -Is)] cross-post sweep failed (processor exit $processor_rc)"
    exit "$processor_rc"
  fi
  echo "[$(date -Is)] cross-post sweep complete"
} >> "$LOG" 2>&1
