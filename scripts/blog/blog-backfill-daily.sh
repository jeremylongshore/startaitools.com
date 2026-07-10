#!/usr/bin/env bash
# Daily autonomous blog pipeline. Runs at 7am via cron.
#
# ARCHITECTURE (inverted 2026-07-05): the LLM PRODUCES, deterministic code LANDS.
#   1. preflight: lock, disk guard, clean-tree + default-branch normalize
#   2. `claude -p /blog-backfill` writes the post + decisions record + a readiness
#      sentinel to the working tree. It does NO git commit/push/publish.
#   3. blog-land.sh (pure bash) verifies preconditions and, only if they pass,
#      commits + pushes + dual-publishes + queues cross-posts + verifies live.
#      If they fail (timeout mid-gates, fact-check block, broken build) it
#      QUARANTINES the stranded files so tomorrow is unblocked, and never
#      publishes something half-baked.
#
# - Idempotent: if yesterday already has a post, exits clean (no-op).
# - flock-serialized against a hand-run /blog-backfill (no concurrent-tree race).
# - Fail-loud: any abnormal early exit pings Slack #cron-failures + emails Jeremy.

set -uo pipefail

LOG_DIR=/home/jeremy/.local/state/blog-backfill-daily
mkdir -p "$LOG_DIR"

# Liveness heartbeat: drop a per-run beat so the estate dead-man's-switch
# (~/bin/automation-liveness-sweep.sh) can tell this schedule still fires. The
# beat marks "the cron ran"; the fail-loud trap below covers "ran but failed".
mkdir -p "$HOME/.local/state/notify-lib" 2>/dev/null || true
: > "$HOME/.local/state/notify-lib/blog-backfill-daily.beat" 2>/dev/null || true

YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
LOG="$LOG_DIR/run-${YESTERDAY}.log"
EMAIL_SCRIPT=/home/jeremy/.claude/skills/email/scripts/send-email.cjs
BLOG_DIR=/home/jeremy/000-projects/blog/startaitools
POSTS_DIR="$BLOG_DIR/content/posts"
LAND_SCRIPT="$(dirname "${BASH_SOURCE[0]}")/blog-land.sh"

# Shared helpers: preflight_branch_normalize, post_exists_for_date, disk_guard,
# acquire_pipeline_lock, count_consecutive_failures, slack_fail.
# shellcheck source=./lib-cron-common.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib-cron-common.sh"

log() { echo "[$(date -Is)] $*" | tee -a "$LOG"; }
log "=== Daily blog-backfill start (target: $YESTERDAY) ==="

# --- Fail-loud guard: an early exit must never be silent (startaitools-74z) ---
# From 2026-06-15 the dirty-tree preflight aborted every run for 11 days with
# ZERO alerts. This trap fires on any non-zero exit that bypassed the normal
# notification and pings Slack #cron-failures + email. Clean exits (rc=0, incl.
# the idempotency/lock no-ops) and the normal path (NOTIFIED=1) are skipped.
NOTIFIED=0
notify_unexpected_exit() {
  local rc=$?
  liveness_markers "blog-backfill-daily" "$rc"   # .beat every run; .ok iff rc==0
  [ "$rc" -eq 0 ] && return
  [ "$NOTIFIED" -eq 1 ] && return
  log "ABNORMAL EXIT (rc=$rc) before normal notification — sending fail-loud alert"
  slack_fail "blog-backfill-daily" "${YESTERDAY}: early exit rc=${rc} — NO POST. Check ${LOG}"
  node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io \
    --subject "🚨 blog-backfill aborted early: ${YESTERDAY} (rc=${rc})" \
    --body "$(printf 'Daily blog-backfill exited abnormally (rc=%s) BEFORE its normal summary email.\n\nNo post was landed for %s.\n\nLast 30 log lines:\n--------------------------------------------------------------------------------\n%s\n' "$rc" "$YESTERDAY" "$(tail -30 "$LOG" 2>/dev/null)")" \
    >/dev/null 2>&1 || true
}
trap notify_unexpected_exit EXIT

# --- Concurrency lock: never let the cron race a hand-run /blog-backfill ------
acquire_pipeline_lock "/tmp/blog-pipeline.lock" "$LOG"; _lk=$?
if [ "$_lk" -eq 2 ]; then NOTIFIED=1; exit 0; fi   # another run holds it — benign
if [ "$_lk" -eq 1 ]; then log "FATAL: could not acquire lock"; exit 1; fi
export BLOG_PIPELINE_LOCK_HELD=1   # so the child blog-land.sh does not re-lock

# --- Disk guard: a wedged disk turns commit/build into corruption ------------
if ! disk_guard "$BLOG_DIR" "${BLOG_BACKFILL_DISK_MIN_MB:-500}" "$LOG"; then exit 1; fi

# --- Idempotency: skip if yesterday already has a post (D-1 fixed regex) ------
# post_exists_for_date matches TOML unquoted/quoted AND YAML dates — the old
# inline grep omitted the unquoted-TOML case and regenerated duplicates.
if EXISTING=$(post_exists_for_date "$POSTS_DIR" "$YESTERDAY"); then
  log "Post already exists for $YESTERDAY ($EXISTING) — skipping (no-op)."
  NOTIFIED=1
  exit 0
fi

# --- Pre-flight: clean tree, on default branch, fast-forward ------------------
# This runs BEFORE generation. The tree MUST be clean here (yesterday's post was
# committed by yesterday's land step). A dirty tree means external uncommitted
# work — legitimately abort. May repoint BLOG_DIR if pivoting to a worktree.
preflight_branch_normalize "$BLOG_DIR" "$LOG"

# --- Generate: claude -p produces artifacts ONLY (no git) --------------------
# Hard wall-clock ceiling. The tier is decided inside the run, so the ceiling
# must fit the worst case (Tier-3 Case Study + all gate agents). Commit/publish
# now happen OUTSIDE claude -p (in blog-land.sh), so a timeout here can no longer
# leave a half-published post — blog-land.sh will quarantine any partial state.
TIMEOUT_SECS="${BLOG_BACKFILL_TIMEOUT:-2700}"
log "Invoking: claude -p /blog-backfill (timeout ${TIMEOUT_SECS}s, pty-wrapped)"
T0=$(date +%s)
# script(1) gives claude -p a pty so its CLI flushes incrementally instead of
# buffering until SIGKILL — the precondition for diagnosing wall-time creep.
if /usr/bin/timeout "$TIMEOUT_SECS" script -e -q -a -c "claude -p '/blog-backfill' --dangerously-skip-permissions" "$LOG" >/dev/null 2>&1; then
  CLAUDE_STATUS="OK"
  WALL=$(( $(date +%s) - T0 ))
  log "claude -p exited cleanly after ${WALL}s ($((WALL/60))m $((WALL%60))s)"
else
  CLAUDE_EXIT=$?
  WALL=$(( $(date +%s) - T0 ))
  CLAUDE_STATUS="FAILED (exit $CLAUDE_EXIT)"
  if [ "$CLAUDE_EXIT" = "124" ]; then
    log "claude -p TIMED OUT after ${WALL}s (hard ceiling ${TIMEOUT_SECS}s) — land step will quarantine any partial state"
  else
    log "claude -p exited non-zero (exit $CLAUDE_EXIT) after ${WALL}s"
  fi
fi

# --- Land: deterministic verify → commit → push → publish → OR quarantine ----
# Runs unconditionally (even after a claude -p failure) — landing is also what
# cleans up / quarantines any partial state so tomorrow is unblocked.
log "Invoking blog-land.sh for $YESTERDAY..."
"$LAND_SCRIPT" "$YESTERDAY" >> "$LOG" 2>&1
LAND_RC=$?
LAND_RESULT=$(grep -oE 'LAND-RESULT: .*' "$LOG" | tail -1 | sed 's/LAND-RESULT: //')
log "blog-land.sh returned rc=$LAND_RC (${LAND_RESULT:-unknown})"

# Map land rc + claude status → overall STATUS.
case "$LAND_RC" in
  0)  STATUS="OK" ;;
  3)  STATUS="OK-WITH-WARNING (pushed, not live yet)" ;;
  10) STATUS="FAILED (QUARANTINED — preconditions failed, tree cleaned)" ;;
  11) STATUS="FAILED (land infra — see log)" ;;
  20) if [ "$CLAUDE_STATUS" = "OK" ]; then STATUS="OK (no post — no activity)"; else STATUS="FAILED (${CLAUDE_STATUS}, no post produced)"; fi ;;
  21) STATUS="OK (already landed)" ;;
  *)  STATUS="FAILED (land rc=$LAND_RC)" ;;
esac
log "Overall STATUS: $STATUS"

# --- Methodology index rebuild (derived index.db from decisions.jsonl) --------
REBUILD="$BLOG_DIR/.claude/skills/blog-backfill/scripts/rebuild-methodology-index.sh"
if [ -x "$REBUILD" ]; then
  log "Rebuilding methodology index..."
  "$REBUILD" >> "$LOG" 2>&1 || log "WARN: methodology index rebuild failed"
fi

# --- Consecutive-failure escalation ------------------------------------------
CONSEC_FAILS=$(count_consecutive_failures "$LOG_DIR" "run-*.log" "FATAL|TIMED OUT|FAILED \(" 10)
ESCALATE_PREFIX=""
if [ "$CONSEC_FAILS" -ge 3 ]; then
  log "ESCALATION: ${CONSEC_FAILS} consecutive failed runs detected — elevating alert priority"
  ESCALATE_PREFIX="🚨 ${CONSEC_FAILS}-DAY STREAK: "
fi

# Slack #cron-failures on a hard failure only (reads SLACK_WEBHOOK_CRON[_FAILURES]).
case "$STATUS" in
  FAILED*) slack_fail "blog-backfill-daily" "${ESCALATE_PREFIX}${YESTERDAY}: ${STATUS} (${CONSEC_FAILS}-day streak). Log: $LOG" ;;
esac

# --- Summary email -----------------------------------------------------------
TAIL=$(tail -50 "$LOG")
BODY="Daily /blog-backfill run for ${YESTERDAY}
Status: ${STATUS}
Land result: ${LAND_RESULT:-n/a} (rc=${LAND_RC})
claude -p: ${CLAUDE_STATUS}
Consecutive failures (incl. this run): ${CONSEC_FAILS}

================================================================================
Last 50 log lines (full log: ${LOG}):
================================================================================

${TAIL}
"
SUBJECT="${ESCALATE_PREFIX}Daily blog-backfill: ${YESTERDAY} — ${STATUS}"
node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io --subject "$SUBJECT" --body "$BODY" >> "$LOG" 2>&1 \
  || log "Email send failed — see log"

# Failure alerting is handled above by slack_fail (#cron-failures) + the summary
# email; success/status is silent now (ntfy retired 2026-06-13).

# Normal notification path completed — disarm the fail-loud trap.
NOTIFIED=1
log "=== Daily blog-backfill end ==="

# Exit truthfully for the liveness trap (review finding on PR #26): a handled
# failure must still exit non-zero so the EXIT trap withholds .ok and the estate
# sweep's running-but-failing signal stays live. NOTIFIED=1 above guarantees the
# trap does NOT double-alert.
case "$STATUS" in OK*) : ;; *) exit 1 ;; esac