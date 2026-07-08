#!/usr/bin/env bash
# Run /blog-calibrate locally and email the result.
# Runs from cron on the 1st of each month at 9am local.

set -uo pipefail

LOG_DIR=/home/jeremy/.local/state/blog-monthly-calibrate
LOG="$LOG_DIR/calibrate.log"
mkdir -p "$LOG_DIR"

# Shared helpers: preflight_branch_normalize, count_consecutive_failures.
# shellcheck source=./lib-cron-common.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib-cron-common.sh"

YM=$(date +%Y-%m)
PER_RUN_LOG="$LOG_DIR/run-${YM}.log"   # per-run log so count_consecutive_failures can bisect
REPORT=/tmp/blog-calibrate-${YM}.txt
EMAIL_SCRIPT=/home/jeremy/.claude/skills/email/scripts/send-email.cjs
BLOG_DIR=/home/jeremy/000-projects/blog/startaitools

log() { echo "[$(date -Is)] $*" | tee -a "$LOG" "$PER_RUN_LOG"; }
log "=== Monthly calibration start (target: $YM) ==="

# Pre-flight: clean tree, switch to default branch (pivot if held in a sibling
# worktree), fast-forward. Same helper the daily uses.
preflight_branch_normalize "$BLOG_DIR" "$PER_RUN_LOG"

# Run /blog-calibrate via headless Claude Code. 15-min ceiling — the previous
# 300s was too tight (2026-06-01 calibrate exited non-zero with 0-byte report
# at exactly 5 min). Override via env.
TIMEOUT_SECS="${BLOG_CALIBRATE_TIMEOUT:-900}"
log "Invoking: claude -p /blog-calibrate (timeout ${TIMEOUT_SECS}s, pty-wrapped)"
T0=$(date +%s)
# Capture into both the report file (for emailing) and the per-run log (for
# consecutive-failure detection + diagnosis). script(1) pty wrap so the CLI
# flushes incrementally instead of buffering until SIGKILL.
if /usr/bin/timeout "$TIMEOUT_SECS" script -e -q -a -c "claude -p '/blog-calibrate' --dangerously-skip-permissions" "$PER_RUN_LOG" >/dev/null 2>&1; then
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

# Extract the report from the per-run log. /blog-calibrate prints its report
# to stdout, which the pty captures into $PER_RUN_LOG. Copy that to $REPORT.
# This replaces the prior `claude ... > "$REPORT" 2>&1` redirect that broke
# the pty wrap pattern.
\cp -f "$PER_RUN_LOG" "$REPORT"
size=$(wc -c < "$REPORT" 2>/dev/null || echo 0)
log "Report size: ${size} bytes"

# A 0-byte report alongside a non-zero exit means the call produced nothing.
# Was previously masked: the wrapper reported "calibration done" regardless. Now reflected.
if [ "$STATUS" = "OK" ] && [ "$size" -lt 100 ]; then
  STATUS="FAILED (empty report despite zero exit)"
  log "WARN: report is suspiciously small (${size} bytes) — treating as failure"
fi

# Commit + push whatever /blog-calibrate produced. The skill writes tracked files
# (calibration-YYYY-MM.md + an append to patterns.jsonl) but does NOT commit them.
# Left uncommitted, the tracked patterns.jsonl change dirties the working tree and
# trips the daily-backfill clean-tree preflight the next morning — the root cause of
# the 2026-07-01 no-post incident. preflight_branch_normalize guaranteed a clean tree
# at start, so the only changes now are calibrate's output; scope the add to those two
# artifacts so nothing unrelated is ever swept in. A failed push leaves the tree clean
# (committed), so it never blocks the daily pipeline — it just retries next month.
if [ "$STATUS" = "OK" ]; then
  METH_DIR="$BLOG_DIR/.claude/skills/blog-backfill/methodology"
  git -C "$BLOG_DIR" add "$METH_DIR"/calibration-*.md "$METH_DIR"/patterns.jsonl >> "$LOG" 2>&1 || true
  if git -C "$BLOG_DIR" diff --cached --quiet 2>/dev/null; then
    log "No calibrate output to commit (tree already clean)"
  elif git -C "$BLOG_DIR" commit -m "chore(methodology): ${YM} calibration report + pattern updates" >> "$LOG" 2>&1; then
    if git -C "$BLOG_DIR" push origin HEAD >> "$LOG" 2>&1; then
      log "✓ committed + pushed calibrate output (tree clean for daily backfill)"
    else
      log "⚠ committed calibrate output but push failed — tree is clean; will push next run"
    fi
  else
    log "⚠ git commit of calibrate output failed — tree may be dirty; daily backfill could block"
  fi
fi

# Consecutive-failure escalation (lower threshold than daily — monthly runs
# once, so two failures is a 60-day gap).
CONSEC_FAILS=$(count_consecutive_failures "$LOG_DIR" "run-*.log" "FATAL|TIMED OUT|FAILED" 12)
ESCALATE_PREFIX=""
if [ "$CONSEC_FAILS" -ge 2 ]; then
  log "ESCALATION: ${CONSEC_FAILS} consecutive failed calibrate runs — elevating alert priority"
  ESCALATE_PREFIX="🚨 ${CONSEC_FAILS}-MONTH STREAK: "
fi

# Slack #cron-failures on a hard failure only (dormant until SLACK_WEBHOOK_CRON
# is set in ~/.env). See scripts/blog/lib-cron-common.sh § slack_fail.
case "$STATUS" in
  FAILED*) slack_fail "blog-monthly-calibrate" "${ESCALATE_PREFIX}${YM}: ${STATUS} (${CONSEC_FAILS}-month streak). Log: $LOG" ;;
esac

SUBJECT="${ESCALATE_PREFIX}Monthly blog calibration: ${YM} — ${STATUS}"
BODY="Calibration report for ${YM}.
Status: ${STATUS}
Consecutive failures (incl. this run): ${CONSEC_FAILS}

Source: $BLOG_DIR/.claude/skills/blog-backfill/methodology/decisions.jsonl
Per-run log: $PER_RUN_LOG

================================================================================

$(cat "$REPORT")
"

if node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io --subject "$SUBJECT" --body "$BODY" >> "$LOG" 2>&1; then
  log "Emailed report"
else
  log "EMAIL FAILED — report kept at $REPORT"
fi

log "=== Monthly calibration end ==="
