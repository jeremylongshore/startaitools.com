#!/usr/bin/env bash
# Independent, idempotent sweep for due Dev.to and Hashnode cross-posts.

set -uo pipefail

BLOG_DIR=/home/jeremy/000-projects/blog/startaitools
PROCESSOR="$BLOG_DIR/.claude/skills/blog-backfill/scripts/check-crosspost-queue.sh"
LOG_DIR="$HOME/.local/state/blog-crosspost-sweep"
LOG="$LOG_DIR/run-$(date +%Y-%m-%d).log"
mkdir -p "$LOG_DIR" "$HOME/.local/state/intent-os/liveness"
: > "$HOME/.local/state/intent-os/liveness/blog-crosspost-sweep.beat"

# shellcheck source=./lib-cron-common.sh
source "$BLOG_DIR/scripts/blog/lib-cron-common.sh"

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
  "$PROCESSOR"
  echo "[$(date -Is)] cross-post sweep complete"
} >> "$LOG" 2>&1
