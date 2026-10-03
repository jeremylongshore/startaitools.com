#!/usr/bin/env bash
# Monthly autonomous /blog-backfill monthly. Runs at 9:30am on the 1st of each
# month via cron, after the 7am daily backfill (which lands the last day of
# the previous month) and after the 9am calibrate report.
#
# - Idempotent: if last month's retro already exists, exits clean (no-op).
# - Logs everything.
# - Emails a summary on completion (success or failure).
# - Buzz sys-automation on failure only (success is silent — ntfy retired 2026-06-13).

set -uo pipefail

LOG_DIR=/home/jeremy/.local/state/blog-monthly-retro
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
EMAIL_SCRIPT=/home/jeremy/.claude/skills/email/scripts/send-email.cjs
BLOG_DIR=/home/jeremy/000-projects/blog/startaitools
RETRO_FILE="$BLOG_DIR/content/monthly-recaps/${PREV_MONTH_LOWER}-${PREV_YEAR}.md"

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

# Idempotency: skip only if last month's retro is PUBLISHED. A local file alone
# is not enough: a previous DEGRADED run may have committed it without pushing,
# and a bare "file exists" no-op would then exit 0 and write .ok over an
# unpublished retro. ensure_published re-checks origin and makes one bounded,
# fast-forward-only reconcile pass before deciding.
RETRO_REL="content/monthly-recaps/${PREV_MONTH_LOWER}-${PREV_YEAR}.md"
if [ -f "$RETRO_FILE" ]; then
  RECONCILED=""
  if ensure_published "$BLOG_DIR" "startaitools" "$RETRO_REL" "$LOG"; then
    log "Retro already exists and is on origin ($PUBLISH_NOTE) — no-op."
    NOTIFIED=1
    exit 0
  fi
  STATUS="DEGRADED (retro exists locally but is not published: $PUBLISH_NOTE)"
  log "$STATUS"
  RB=$(default_branch_of "$BLOG_DIR"); RB="${RB:-master}"
  RECOVER="on branch $RB in $BLOG_DIR: git push origin $RB:$RB (fast-forward only); if the retro was never committed, commit it first"
  cron_fail "blog-monthly-retro" "${PREV_MONTH_LOWER^} ${PREV_YEAR}: ${STATUS}. Reconcile: $(printf '%b' "$RECONCILED" | tr '\n' ' ') Recover: ${RECOVER}. Log: $LOG"
  GATE_BODY=$(printf '%s\n\nReconcile:\n%b\nRecover: %s\n\nLast 30 log lines:\n%s\n' \
    "$STATUS" "$RECONCILED" "$RECOVER" "$(tail -30 "$LOG" 2>/dev/null)")
  node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io \
    --subject "Monthly blog retro: ${PREV_MONTH_LOWER^} ${PREV_YEAR} — ${STATUS}" \
    --body "$GATE_BODY" >> "$LOG" 2>&1 || log "Email send failed — see log"
  NOTIFIED=1
  exit 1
fi

# Pre-flight: clean tree, switch to default branch (pivoting if held in a
# sibling worktree), fast-forward. Same helper the daily uses.
preflight_branch_normalize "$BLOG_DIR" "$LOG"

# Run /blog-backfill monthly headlessly. 60-min hard timeout — the May 2026
# retro hit the prior 1800s ceiling exactly. Monthly synthesizes the whole
# month's posts; 2x daily headroom is the right floor. Override via env.
TIMEOUT_SECS="${BLOG_MONTHLY_TIMEOUT:-3600}"
log "Invoking: claude -p /blog-backfill monthly (timeout ${TIMEOUT_SECS}s, pty-wrapped)"
T0=$(date +%s)
# script(1) gives claude -p a pty so output flushes incrementally instead of
# buffering until SIGKILL. Same pattern as the daily wrapper after PR #16.
if /usr/bin/timeout "$TIMEOUT_SECS" script -e -q -a -c "claude -p '/blog-backfill monthly' --dangerously-skip-permissions" "$LOG" >/dev/null 2>&1; then
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
RECONCILED=""
if [ "$STATUS" = "OK" ]; then
  RECONCILE_FAILED=""
  reconcile_repo "$BLOG_DIR" "startaitools" "$LOG" || RECONCILE_FAILED="${RECONCILE_FAILED} startaitools"
  reconcile_repo "/home/jeremy/000-projects/claude-code-plugins" "tonsofskills" "$LOG" || RECONCILE_FAILED="${RECONCILE_FAILED} tonsofskills"
  cd "$BLOG_DIR" || true
  if [ -n "$RECONCILE_FAILED" ]; then
    STATUS="DEGRADED (reconcile refused/unpushed:${RECONCILE_FAILED})"
    log "reconcile did not complete for:${RECONCILE_FAILED} — run is not OK"
  fi
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
