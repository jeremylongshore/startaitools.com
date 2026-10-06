#!/usr/bin/env bash
# Monthly autonomous /blog-backfill monthly. Runs at 9:30am on the 1st of each
# month via cron, after the 7am daily backfill (which lands the last day of
# the previous month) and after the 9am calibrate report.
#
# - Idempotent: if last month's retro already exists, exits clean (no-op).
# - Logs everything.
# - Emails a summary on completion (success or failure).
# - Buzz sys-automation on failure only (success is silent — ntfy retired 2026-06-13).
# - Workspace (authority map 000-docs/014 §4.4): the producer runs in a detached
#   worktree of FRESH origin/<default> under the state dir, with BLOG_REPO_DIR
#   bound to it. Only content/monthly-recaps/ may be committed there; the wrapper
#   pushes HEAD to origin. It never checks out, pulls, commits or pushes in the
#   primary checkout. A failed push keeps the workspace for the next run.

set -uo pipefail

LOG_DIR="${BLOG_RETRO_STATE_DIR:-$HOME/.local/state/blog-monthly-retro}"
mkdir -p "$LOG_DIR"

# Liveness heartbeat: drop a per-run beat so the estate dead-man's-switch
# (~/bin/automation-liveness-sweep.sh) can tell this schedule still fires. The
# beat marks "the cron ran"; fail-alerting (below) covers "ran but failed".
mkdir -p "$HOME/.local/state/intent-os/liveness" 2>/dev/null || true
: > "$HOME/.local/state/intent-os/liveness/blog-monthly-retro.beat" 2>/dev/null || true

# Shared helpers: preflight_branch_normalize, count_consecutive_failures.
# shellcheck source=./lib-cron-common.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib-cron-common.sh"

# Compute previous month — "previous month from today" works correctly on the
# 1st (yesterday's month) and any later day too (this month's previous).
# Use "first day of this month - 1 day" to land on the last day of the prior month.
PREV_DATE=$(date -d "$(date +%Y-%m-01) -1 day" +%Y-%m-%d)
PREV_MONTH_LOWER=$(date -d "$PREV_DATE" +%B | tr '[:upper:]' '[:lower:]')
PREV_YEAR=$(date -d "$PREV_DATE" +%Y)
PREV_YM=$(date -d "$PREV_DATE" +%Y-%m)

LOG="$LOG_DIR/run-${PREV_YM}.log"
EMAIL_SCRIPT="${BLOG_EMAIL_SCRIPT:-$HOME/.claude/skills/email/scripts/send-email.cjs}"
# The primary checkout is used ONLY as the object store the workspace is added
# from; nothing is written to its working tree, index, HEAD or branches.
BLOG_DIR="${BLOG_MONTHLY_REPO:-/home/jeremy/000-projects/blog/startaitools}"
CLAUDE_BIN="${BLOG_CLAUDE_BIN:-claude}"
WS="$LOG_DIR/workspace-${PREV_YM}"
OUT_ALLOWED='^content/monthly-recaps/[a-z]+-[0-9]{4}\.md$'

log() { echo "[$(date -Is)] $*" | tee -a "$LOG"; }
log "=== Monthly blog-backfill retro start (target: ${PREV_MONTH_LOWER} ${PREV_YEAR}) ==="

# --- Fail-loud guard: an early exit must never be silent ----------------------
# This is one of the two scripts the "Nine Days Silent" postmortem was about: a
# dirty-tree/worktree FATAL inside preflight_branch_normalize below EXITs before
# the normal Slack + email path at the bottom, so the failure went unalerted.
# Ported verbatim from blog-backfill-daily.sh: this trap fires on any non-zero
# exit that bypassed the normal notification and pings Buzz sys-automation +
# email. Clean exits (rc=0, incl. the idempotency no-op) and the normal path
# (NOTIFIED=1) are skipped.
NOTIFIED=0
notify_unexpected_exit() {
  local rc=$?
  liveness_markers "blog-monthly-retro" "$rc"   # .beat every run; .ok iff rc==0
  [ "$rc" -eq 0 ] && return
  [ "$NOTIFIED" -eq 1 ] && return
  log "ABNORMAL EXIT (rc=$rc) before normal notification — sending fail-loud alert"
  cron_fail "blog-monthly-retro" "${PREV_MONTH_LOWER^} ${PREV_YEAR}: early exit rc=${rc} — NO retro. Check ${LOG}"
  node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io \
    --subject "🚨 blog-monthly-retro aborted early: ${PREV_MONTH_LOWER^} ${PREV_YEAR} (rc=${rc})" \
    --body "$(printf 'Monthly blog retro exited abnormally (rc=%s) BEFORE its normal summary email.\n\nNo retro was produced for %s %s.\n\nLast 30 log lines:\n--------------------------------------------------------------------------------\n%s\n' "$rc" "${PREV_MONTH_LOWER^}" "$PREV_YEAR" "$(tail -30 "$LOG" 2>/dev/null)")" \
    >/dev/null 2>&1 || true
}
trap notify_unexpected_exit EXIT

# Republish any retro a previous DEGRADED run committed in its workspace but
# could not push (one bounded attempt per stranded workspace).
RECONCILED=""
for _pending in "$LOG_DIR"/workspace-*; do
  [ -d "$_pending" ] || continue
  WS_BRANCH=$(default_branch_of "$BLOG_DIR"); WS_BRANCH="${WS_BRANCH:-master}"
  git -C "$_pending" fetch -q origin "+refs/heads/${WS_BRANCH}:refs/remotes/origin/${WS_BRANCH}" >> "$LOG" 2>&1 || true
  if periodic_workspace_publish "$_pending" "$LOG" "docs(retro): monthly retrospective" "$OUT_ALLOWED"; then
    RECONCILED="${RECONCILED}startaitools $(basename "$_pending"): ${WS_NOTE}\n"
    periodic_workspace_close "$BLOG_DIR" "$_pending" "$LOG" || true
  else
    RECONCILED="${RECONCILED}startaitools $(basename "$_pending"): NOT published (${WS_NOTE})\n"
  fi
done
[ -n "$RECONCILED" ] && log "startup reconcile: $(printf '%b' "$RECONCILED" | tr '\n' ' ')"

# Idempotency: skip only if last month's retro is PUBLISHED on fresh origin. A
# local file proves nothing (it may be an unpushed commit), so the check reads
# origin, never the primary checkout's working tree.
RETRO_REL="content/monthly-recaps/${PREV_MONTH_LOWER}-${PREV_YEAR}.md"
published_on_origin "$BLOG_DIR" "$RETRO_REL" "$LOG"; _pub=$?
if [ "$_pub" -eq 0 ]; then
  log "Retro already on origin ($RETRO_REL) — no-op."
  NOTIFIED=1
  exit 0
elif [ "$_pub" -eq 2 ]; then
  log "FATAL: cannot reach origin to check whether $RETRO_REL is published"
  exit 1
fi

if ! periodic_workspace_open "$BLOG_DIR" "$WS" "$LOG"; then
  log "FATAL: could not open the run workspace $WS (a stranded workspace may need a human; see startup reconcile above)"
  exit 1
fi
export BLOG_REPO_DIR="$WS"
cd "$WS" || exit 1
RETRO_FILE="$WS/$RETRO_REL"

# Run /blog-backfill monthly headlessly. 60-min hard timeout — the May 2026
# retro hit the prior 1800s ceiling exactly. Monthly synthesizes the whole
# month's posts; 2x daily headroom is the right floor. Override via env.
TIMEOUT_SECS="${BLOG_MONTHLY_TIMEOUT:-3600}"
log "Invoking: claude -p /blog-backfill monthly (timeout ${TIMEOUT_SECS}s, pty-wrapped)"
T0=$(date +%s)
# script(1) gives claude -p a pty so output flushes incrementally instead of
# buffering until SIGKILL. Same pattern as the daily wrapper after PR #16.
if /usr/bin/timeout "$TIMEOUT_SECS" script -e -q -a -c "$CLAUDE_BIN -p '/blog-backfill monthly' --dangerously-skip-permissions" "$LOG" >/dev/null 2>&1; then
  STATUS="OK"
  WALL=$(( $(date +%s) - T0 ))
  log "claude -p exited cleanly after ${WALL}s ($((WALL/60))m $((WALL%60))s)"
else
  EXIT=$?
  WALL=$(( $(date +%s) - T0 ))
  STATUS="FAILED (exit $EXIT)"
  if [ "$EXIT" = "124" ]; then
    log "claude -p TIMED OUT after ${WALL}s (hard ceiling ${TIMEOUT_SECS}s)"
  else
    log "claude -p exited non-zero (exit $EXIT) after ${WALL}s"
  fi
fi

# Verify the retro actually landed
if [ -f "$RETRO_FILE" ]; then
  RETRO_BASENAME=$(basename "$RETRO_FILE" .md)
  RETRO_TITLE=$(grep -m1 "^title" "$RETRO_FILE" | sed -E "s/^title = ['\"](.*)['\"]$/\1/")
  log "Retro file present: $RETRO_FILE"
else
  RETRO_BASENAME="(not generated)"
  RETRO_TITLE=""
  log "WARNING: retro file $RETRO_FILE does not exist after run"
  if [ "$STATUS" = "OK" ]; then STATUS="FAILED (retro file missing)"; fi
fi

# ----- Post-flight: reconcile branch drift -----
# reconcile_repo now lives in lib-cron-common.sh (deduped from the drifting daily
# + monthly copies; carries the B-2 fix so claude-code-plugins resolves to `main`
# instead of the old hardcoded `master` fallback).
# A refused or unpushed reconcile is NOT an OK run (startaitools-8oc.16): the
# retro may be committed locally but not live, so the status says DEGRADED,
# Buzz is alerted, the exit is non-zero and .ok is withheld. (DEGRADED, not
# FAILED: the retro itself was produced; only its publication is unproven.)
if [ "$STATUS" = "OK" ]; then
  RECONCILE_FAILED=""
  if periodic_workspace_publish "$WS" "$LOG" "docs(retro): ${PREV_MONTH_LOWER^} ${PREV_YEAR} monthly retrospective" \
      "$OUT_ALLOWED" "$RETRO_REL"; then
    RECONCILED="${RECONCILED}startaitools: ${WS_NOTE}\n"
  else
    RECONCILE_FAILED="${RECONCILE_FAILED} startaitools"
    RECONCILED="${RECONCILED}startaitools: NOT published (${WS_NOTE}); workspace kept at $WS — recover: git -C $WS push origin HEAD:refs/heads/${WS_BRANCH}\n"
  fi
  reconcile_repo "${BLOG_TOS_REPO:-/home/jeremy/000-projects/claude-code-plugins}" "tonsofskills" "$LOG" || RECONCILE_FAILED="${RECONCILE_FAILED} tonsofskills"
  cd "$LOG_DIR" || true
  case "$RECONCILE_FAILED" in *startaitools*) : ;; *) periodic_workspace_close "$BLOG_DIR" "$WS" "$LOG" || true ;; esac
  if [ -n "$RECONCILE_FAILED" ]; then
    STATUS="DEGRADED (reconcile refused/unpushed:${RECONCILE_FAILED})"
    log "reconcile did not complete for:${RECONCILE_FAILED} — run is not OK"
  fi
fi

if [ "$STATUS" != "OK" ] && [ "${RECONCILE_FAILED:-}" = "" ]; then
  cd "$LOG_DIR" || true
  periodic_workspace_close "$BLOG_DIR" "$WS" "$LOG" || true
fi

# Consecutive-failure escalation (mirrors the daily pattern).
CONSEC_FAILS=$(count_consecutive_failures "$LOG_DIR" "run-*.log" "FATAL|TIMED OUT|FAILED \(exit|FAILED \(retro" 12)
ESCALATE_PREFIX=""
if [ "$CONSEC_FAILS" -ge 2 ]; then
  # Threshold lower (2) than daily (3) because monthly only fires once per
  # month — two missed retros means a 60-day gap.
  log "ESCALATION: ${CONSEC_FAILS} consecutive failed monthly runs — elevating alert priority"
  ESCALATE_PREFIX="🚨 ${CONSEC_FAILS}-MONTH STREAK: "
fi

# Buzz sys-automation on a hard failure only (dormant until governed Buzz dispatch
# is set in ~/.env). See scripts/blog/lib-cron-common.sh § cron_fail.
case "$STATUS" in
  FAILED*|DEGRADED*) cron_fail "blog-monthly-retro" "${ESCALATE_PREFIX}${PREV_MONTH_LOWER^} ${PREV_YEAR}: ${STATUS} (${CONSEC_FAILS}-month streak). Log: $LOG" ;;
esac

# Build summary
TAIL=$(tail -50 "$LOG")
BODY="Monthly /blog-backfill retro for ${PREV_MONTH_LOWER^} ${PREV_YEAR}
Status: ${STATUS}
Consecutive failures (incl. this run): ${CONSEC_FAILS}
Retro file: ${RETRO_BASENAME}
Title: ${RETRO_TITLE}
Branch reconciliation:
$(printf "%b" "${RECONCILED:-(skipped — run failed)}")

================================================================================
Last 50 log lines (full log: ${LOG}):
================================================================================

${TAIL}
"

SUBJECT="${ESCALATE_PREFIX}Monthly blog retro: ${PREV_MONTH_LOWER^} ${PREV_YEAR} — ${STATUS}"

node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io --subject "$SUBJECT" --body "$BODY" >> "$LOG" 2>&1 \
  || log "Email send failed — see log"

# Normal notification path completed — disarm the fail-loud trap.
NOTIFIED=1
log "=== Monthly blog-backfill retro end ==="

# Exit truthfully for the liveness trap (review finding on PR #26): a handled
# failure must still exit non-zero so the EXIT trap withholds .ok and the estate
# sweep's running-but-failing signal stays live. NOTIFIED=1 above guarantees the
# trap does NOT double-alert.
case "$STATUS" in OK*) : ;; *) exit 1 ;; esac
