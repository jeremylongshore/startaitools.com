#!/usr/bin/env bash
# Monthly autonomous /blog-backfill monthly. Runs at 9:30am on the 1st of each
# month via cron, after the 7am daily backfill (which lands the last day of
# the previous month) and after the 9am calibrate report.
#
# - Idempotent: if last month's retro already exists, exits clean (no-op).
# - Logs everything.
# - Emails a summary on completion (success or failure).
# - ntfy push on result.

set -uo pipefail

LOG_DIR=/home/jeremy/.local/state/blog-monthly-retro
mkdir -p "$LOG_DIR"

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

# Idempotency: skip if last month's retro already exists
if [ -f "$RETRO_FILE" ]; then
  log "Retro already exists at $RETRO_FILE — skipping (no-op)."
  exit 0
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

# ----- Post-flight: reconcile branch drift (same pattern as daily) -----
RECONCILED=""
reconcile_repo() {
  local repo="$1"
  local label="$2"
  [ -d "$repo/.git" ] || return 0
  cd "$repo" || return 1
  local current default sha
  current=$(git rev-parse --abbrev-ref HEAD 2>/dev/null) || return 1
  default=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
  default="${default:-master}"
  if [ "$current" = "$default" ]; then
    RECONCILED="${RECONCILED}${label}: on $default ✓\n"
    return 0
  fi
  if [ -z "$(git log "origin/$default..$current" --oneline 2>/dev/null)" ]; then
    RECONCILED="${RECONCILED}${label}: $current has no commits ahead of origin/$default ✓\n"
    return 0
  fi
  if git push origin "$current:$default" >> "$LOG" 2>&1; then
    sha=$(git rev-parse --short HEAD)
    log "✓ FF-pushed $label: $current → origin/$default ($sha)"
    RECONCILED="${RECONCILED}${label}: ✓ auto-merged $current → origin/$default ($sha)\n"
  else
    log "✗ FF-push failed for $label ($current → origin/$default) — manual merge required"
    RECONCILED="${RECONCILED}${label}: ⚠ ORPHANED on $current — needs manual merge\n"
  fi
}
if [ "$STATUS" = "OK" ]; then
  reconcile_repo "$BLOG_DIR" "startaitools"
  reconcile_repo "/home/jeremy/000-projects/claude-code-plugins" "tonsofskills"
fi

# Consecutive-failure escalation (mirrors the daily pattern).
CONSEC_FAILS=$(count_consecutive_failures "$LOG_DIR" "run-*.log" "FATAL|TIMED OUT|FAILED \(exit|FAILED \(retro" 12)
ESCALATE_PREFIX=""
ESCALATE_PRIORITY="default"
if [ "$CONSEC_FAILS" -ge 2 ]; then
  # Threshold lower (2) than daily (3) because monthly only fires once per
  # month — two missed retros means a 60-day gap.
  log "ESCALATION: ${CONSEC_FAILS} consecutive failed monthly runs — elevating alert priority"
  ESCALATE_PREFIX="🚨 ${CONSEC_FAILS}-MONTH STREAK: "
  ESCALATE_PRIORITY="max"
fi

# Slack #cron-failures on a hard failure only (dormant until SLACK_WEBHOOK_CRON
# is set in ~/.env). See scripts/blog/lib-cron-common.sh § slack_fail.
case "$STATUS" in
  FAILED*) slack_fail "blog-monthly-retro" "${ESCALATE_PREFIX}${PREV_MONTH_LOWER^} ${PREV_YEAR}: ${STATUS} (${CONSEC_FAILS}-month streak). Log: $LOG" ;;
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

# ntfy push notification
NTFY_TOPIC=$(cat /home/jeremy/.ntfy-topic 2>/dev/null)
if [ -n "$NTFY_TOPIC" ]; then
  if [ "$STATUS" = "OK" ]; then
    curl -s -H "Title: Monthly blog retro OK" -H "Priority: default" -H "Tags: scroll" \
      -d "${PREV_MONTH_LOWER^} ${PREV_YEAR}: ${RETRO_BASENAME}" \
      "https://ntfy.sh/$NTFY_TOPIC" >> "$LOG" 2>&1 || true
  else
    _ntfy_prio="high"
    [ "$ESCALATE_PRIORITY" = "max" ] && _ntfy_prio="max"
    curl -s -H "Title: ${ESCALATE_PREFIX}Monthly blog retro FAILED" -H "Priority: ${_ntfy_prio}" -H "Tags: rotating_light" \
      -d "${PREV_MONTH_LOWER^} ${PREV_YEAR}: ${STATUS} (${CONSEC_FAILS}-month streak). Check log at $LOG" \
      "https://ntfy.sh/$NTFY_TOPIC" >> "$LOG" 2>&1 || true
  fi
fi

log "=== Monthly blog-backfill retro end ==="
