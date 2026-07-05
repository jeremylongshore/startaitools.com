#!/usr/bin/env bash
# Daily portfolio web-analytics email to Jeremy. Runs each morning via cron.
#
# Invokes the /web-analytics skill headlessly. The SKILL itself emails the brief
# to jeremy@intentsolutions.io (its `--email` delivery path, hardcoded recipient).
# This wrapper is deliberately thin — it does NOT send the analytics content; it
# only provides the same operational spine as the blog crons:
#   - a wall-clock ceiling + pty-wrapped incremental logging
#   - fail-loud alerting (ntfy + email) if `claude -p` errors, so a silent stall
#     can never recur the way blog-backfill did (startaitools-74z)
#   - consecutive-failure escalation + optional #cron-failures Slack
#
# Independent of the blog pipeline: no git, no staging, no publish, no branch
# normalize. Portfolio scope (startaitools, tonsofskills, jeremylongshore,
# intentsolutions) + recipient are the skill's defaults — see
# ~/.claude/skills/web-analytics/SKILL.md Step 4 (Email delivery).
#
# Tunables (env):
#   WEB_ANALYTICS_TIER     mini | medium | full   (default: medium)
#   WEB_ANALYTICS_TIMEOUT  hard ceiling seconds    (default: 900)

set -uo pipefail

LOG_DIR=/home/jeremy/.local/state/web-analytics-daily
mkdir -p "$LOG_DIR"

TODAY=$(date +%Y-%m-%d)
LOG="$LOG_DIR/run-${TODAY}.log"
EMAIL_SCRIPT=/home/jeremy/.claude/skills/email/scripts/send-email.cjs
TIER="${WEB_ANALYTICS_TIER:-medium}"
TIMEOUT_SECS="${WEB_ANALYTICS_TIMEOUT:-900}"

# Shared helpers: count_consecutive_failures, slack_fail, _log.
# shellcheck source=./lib-cron-common.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib-cron-common.sh"

log() { echo "[$(date -Is)] $*" | tee -a "$LOG"; }
log "=== Daily web-analytics email start (tier: ${TIER}, target: ${TODAY}) ==="

# --- Fail-loud guard: an early/abnormal exit must never be silent ---
# Mirrors blog-backfill-daily.sh. If claude -p or anything before the normal
# notify block exits non-zero, push a high-priority ntfy + email so a broken
# analytics cron surfaces the same day instead of quietly not-emailing for days.
NOTIFIED=0
notify_unexpected_exit() {
  local rc=$?
  [ "$rc" -eq 0 ] && return
  [ "$NOTIFIED" -eq 1 ] && return
  log "ABNORMAL EXIT (rc=$rc) before normal notification — sending fail-loud alert"
  local topic
  topic=$(cat /home/jeremy/.ntfy-topic 2>/dev/null)
  if [ -n "$topic" ]; then
    curl -s -H "Title: 🚨 web-analytics email aborted early" -H "Priority: high" -H "Tags: rotating_light" \
      -d "${TODAY}: early exit rc=${rc} — NO analytics brief emailed. Check ${LOG}" \
      "https://ntfy.sh/$topic" >/dev/null 2>&1 || true
  fi
  node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io \
    --subject "🚨 web-analytics email aborted early: ${TODAY} (rc=${rc})" \
    --body "$(printf 'The daily web-analytics cron exited abnormally (rc=%s) BEFORE completing.\nNo analytics brief was emailed for %s.\n\nLast 30 log lines:\n--------------------------------------------------------------------------------\n%s\n' "$rc" "$TODAY" "$(tail -30 "$LOG" 2>/dev/null)")" \
    >/dev/null 2>&1 || true
}
trap notify_unexpected_exit EXIT

# Run the skill headlessly. script(1) gives claude -p a pty so its CLI flushes
# incrementally instead of buffering until SIGKILL (same rationale as the blog
# crons — the pty is the precondition for diagnosing a wall-time creep).
log "Invoking: claude -p /web-analytics ${TIER} --email (timeout ${TIMEOUT_SECS}s, pty-wrapped)"
T0=$(date +%s)
if /usr/bin/timeout "$TIMEOUT_SECS" script -e -q -a -c "claude -p '/web-analytics ${TIER} --email' --dangerously-skip-permissions" "$LOG" >/dev/null 2>&1; then
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

# Soft delivery check: the skill exits 0 even if the /email step silently no-ops.
# Look for evidence an email was actually attempted (send-email.cjs / Analytics
# subject in the pty log). Absence downgrades to OK-WITH-WARNING — non-blocking,
# but it distinguishes "brief emailed" from "ran clean but sent nothing".
if [ "$STATUS" = "OK" ]; then
  if ! grep -qiE 'send-email|Analytics (mini|medium|full)|Message sent|messageId|Email sent' "$LOG" 2>/dev/null; then
    log "WARN: no email-send evidence in log — the brief may not have been delivered"
    STATUS="OK-WITH-WARNING (no email-send evidence)"
  fi
fi

# Consecutive-failure escalation (same pattern as the blog crons).
CONSEC_FAILS=$(count_consecutive_failures "$LOG_DIR" "run-*.log" "FATAL|TIMED OUT|FAILED \(exit" 10)
ESCALATE_PREFIX=""
ESCALATE_PRIORITY="default"
if [ "$CONSEC_FAILS" -ge 3 ]; then
  log "ESCALATION: ${CONSEC_FAILS} consecutive failed runs — elevating alert priority"
  ESCALATE_PREFIX="🚨 ${CONSEC_FAILS}-DAY STREAK: "
  ESCALATE_PRIORITY="max"
fi

# Slack #cron-failures on a hard failure only (dormant until the webhook is set).
case "$STATUS" in
  FAILED*) slack_fail "web-analytics-daily" "${ESCALATE_PREFIX}${TODAY}: ${STATUS} (${CONSEC_FAILS}-day streak). Log: $LOG" ;;
esac

# Notifications:
#  - OK: the analytics brief IS the deliverable email (sent by the skill). We do
#    NOT send a duplicate wrapper summary — just a low-priority ntfy heartbeat.
#  - OK-WITH-WARNING / FAILED: email + ntfy Jeremy so the gap is visible.
NTFY_TOPIC=$(cat /home/jeremy/.ntfy-topic 2>/dev/null)
case "$STATUS" in
  OK)
    if [ -n "$NTFY_TOPIC" ]; then
      curl -s -H "Title: Daily analytics email OK" -H "Priority: min" -H "Tags: chart_with_upwards_trend" \
        -d "${TODAY}: ${TIER} brief emailed" "https://ntfy.sh/$NTFY_TOPIC" >> "$LOG" 2>&1 || true
    fi
    ;;
  *)
    # Capture the tail BEFORE the append redirect so we don't read+write $LOG in
    # one pipeline (SC2094). Matches blog-backfill-daily.sh's pattern.
    TAIL=$(tail -50 "$LOG")
    FAIL_BODY=$(printf 'Daily web-analytics cron for %s\nStatus: %s\nConsecutive failures (incl. this run): %s\n\n================================================================================\nLast 50 log lines (full log: %s):\n================================================================================\n\n%s\n' "$TODAY" "$STATUS" "$CONSEC_FAILS" "$LOG" "$TAIL")
    node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io \
      --subject "${ESCALATE_PREFIX}Daily web-analytics: ${TODAY} — ${STATUS}" \
      --body "$FAIL_BODY" \
      >> "$LOG" 2>&1 || log "Email send failed — see log"
    if [ -n "$NTFY_TOPIC" ]; then
      _ntfy_prio="high"; [ "$ESCALATE_PRIORITY" = "max" ] && _ntfy_prio="max"
      curl -s -H "Title: ${ESCALATE_PREFIX}Daily analytics email ${STATUS%% *}" -H "Priority: ${_ntfy_prio}" -H "Tags: rotating_light" \
        -d "${TODAY}: ${STATUS} (${CONSEC_FAILS}-day streak). Check $LOG" "https://ntfy.sh/$NTFY_TOPIC" >> "$LOG" 2>&1 || true
    fi
    ;;
esac

# Normal notification path completed — disarm the fail-loud trap.
NOTIFIED=1
log "=== Daily web-analytics email end (${STATUS}) ==="
