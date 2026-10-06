#!/usr/bin/env bash
# Run /blog-calibrate locally and email the result.
# Runs from cron on the 1st of each month at 9am local.
#
# Usage: blog-monthly-calibrate.sh [YYYY-MM]
#   No argument: the previous COMPLETE month (the cron case). The period is
#   computed here, logged with explicit [start, end) boundaries, PASSED to the
#   skill as its argument, and used for every label (log, report, commit,
#   email), so the analysed month and the reported month cannot diverge.
#   Before 2026-10 the wrapper labelled runs with the current month while the
#   skill silently defaulted to the previous one (the 2026-09-01 run was titled
#   "2026-09" and reported August).
#
# Workspace (authority map 000-docs/014 §4.4): the skill runs in a detached
# worktree of FRESH origin/<default> under the state dir, with BLOG_REPO_DIR
# bound to it. The wrapper commits only the calibration report and
# patterns.jsonl there and pushes HEAD to origin. It never checks out, pulls,
# commits or pushes in the primary checkout. A run whose push fails keeps its
# workspace; the next run publishes it first (recovery command in the alert).

set -uo pipefail

LOG_DIR="${BLOG_CALIBRATE_STATE_DIR:-$HOME/.local/state/blog-monthly-calibrate}"
LOG="$LOG_DIR/calibrate.log"
mkdir -p "$LOG_DIR"

# Liveness heartbeat: drop a per-run beat so the estate dead-man's-switch
# (~/bin/automation-liveness-sweep.sh) can tell this schedule still fires. The
# beat marks "the cron ran"; fail-alerting (below) covers "ran but failed".
mkdir -p "$HOME/.local/state/intent-os/liveness" 2>/dev/null || true
: > "$HOME/.local/state/intent-os/liveness/blog-monthly-calibrate.beat" 2>/dev/null || true

# Shared helpers: preflight_branch_normalize, count_consecutive_failures.
# shellcheck source=./lib-cron-common.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib-cron-common.sh"

# Arg validation happens before the fail-loud trap is armed: a typo by a human
# at a shell is a usage error, not a cron failure.
if ! PERIOD=$(calibration_period "${1:-}"); then
  echo "usage: $0 [YYYY-MM]  (got '${1:-}')" >&2
  exit 64
fi
read -r YM PERIOD_START PERIOD_END <<< "$PERIOD"
# Per-TARGET-month log so count_consecutive_failures can bisect. Named target-*
# (not run-*) because the old run-YYYY-MM.log files are keyed by the RUN month;
# reusing that name for the target month would append to a previous failure.
PER_RUN_LOG="$LOG_DIR/target-${YM}.log"
REPORT=/tmp/blog-calibrate-${YM}.txt
EMAIL_SCRIPT="${BLOG_EMAIL_SCRIPT:-$HOME/.claude/skills/email/scripts/send-email.cjs}"
# The primary checkout is used ONLY as the object store the workspace is added
# from; nothing is written to its working tree, index, HEAD or branches.
BLOG_DIR="${BLOG_MONTHLY_REPO:-/home/jeremy/000-projects/blog/startaitools}"
CLAUDE_BIN="${BLOG_CLAUDE_BIN:-claude}"
WS="$LOG_DIR/workspace-${YM}"
METH_REL=.claude/skills/blog-backfill/methodology
OUT_ALLOWED="^${METH_REL//./\\.}/(calibration-[0-9]{4}-[0-9]{2}\\.md|patterns\\.jsonl)\$"

log() { echo "[$(date -Is)] $*" | tee -a "$LOG" "$PER_RUN_LOG"; }
log "=== Monthly calibration start (target: $YM, period [$PERIOD_START, $PERIOD_END)${1:+, explicit override}) ==="

# --- Fail-loud guard: an early exit must never be silent ----------------------
# This is one of the two scripts the "Nine Days Silent" postmortem was about: a
# dirty-tree/worktree FATAL inside preflight_branch_normalize below EXITs before
# the normal Slack + email path at the bottom, so the failure went unalerted.
# Ported verbatim from blog-backfill-daily.sh: this trap fires on any non-zero
# exit that bypassed the normal notification and pings Buzz sys-automation +
# email. Clean exits (rc=0) and the normal path (NOTIFIED=1) are skipped.
NOTIFIED=0
notify_unexpected_exit() {
  local rc=$?
  liveness_markers "blog-monthly-calibrate" "$rc"   # .beat every run; .ok iff rc==0
  [ "$rc" -eq 0 ] && return
  [ "$NOTIFIED" -eq 1 ] && return
  log "ABNORMAL EXIT (rc=$rc) before normal notification — sending fail-loud alert"
  cron_fail "blog-monthly-calibrate" "${YM}: early exit rc=${rc} — NO calibration report. Check ${LOG}"
  node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io \
    --subject "🚨 blog-monthly-calibrate aborted early: ${YM} (rc=${rc})" \
    --body "$(printf 'Monthly blog calibration exited abnormally (rc=%s) BEFORE its normal summary email.\n\nNo calibration report was produced for %s.\n\nLast 30 log lines:\n--------------------------------------------------------------------------------\n%s\n' "$rc" "$YM" "$(tail -30 "$LOG" 2>/dev/null)")" \
    >/dev/null 2>&1 || true
}
trap notify_unexpected_exit EXIT

# Republish anything a previous DEGRADED run committed in its workspace but
# could not push (bounded: one publish attempt per stranded workspace). Its
# result is logged; a workspace that still cannot publish is left for a human
# and, if it is this month's, this run fails below instead of overwriting it.
RECONCILED=""
for _pending in "$LOG_DIR"/workspace-*; do
  [ -d "$_pending" ] || continue
  WS_BRANCH=$(default_branch_of "$BLOG_DIR"); WS_BRANCH="${WS_BRANCH:-master}"
  git -C "$_pending" fetch -q origin "+refs/heads/${WS_BRANCH}:refs/remotes/origin/${WS_BRANCH}" >> "$LOG" 2>&1 || true
  if periodic_workspace_publish "$_pending" "$LOG" "chore(methodology): calibration report + pattern updates" "$OUT_ALLOWED"; then
    RECONCILED="${RECONCILED}$(basename "$_pending"): ${WS_NOTE}\n"
    periodic_workspace_close "$BLOG_DIR" "$_pending" "$LOG" || true
  else
    RECONCILED="${RECONCILED}$(basename "$_pending"): NOT published (${WS_NOTE})\n"
  fi
done
[ -n "$RECONCILED" ] && log "startup reconcile: $(printf '%b' "$RECONCILED" | tr '\n' ' ')"

if ! periodic_workspace_open "$BLOG_DIR" "$WS" "$PER_RUN_LOG"; then
  log "FATAL: could not open the run workspace $WS"
  exit 1
fi
export BLOG_REPO_DIR="$WS"
cd "$WS" || exit 1

# Run /blog-calibrate via headless Claude Code. 15-min ceiling — the previous
# 300s was too tight (2026-06-01 calibrate exited non-zero with 0-byte report
# at exactly 5 min). Override via env.
TIMEOUT_SECS="${BLOG_CALIBRATE_TIMEOUT:-900}"
log "Invoking: claude -p '/blog-calibrate ${YM}' (timeout ${TIMEOUT_SECS}s, pty-wrapped)"
T0=$(date +%s)
# Capture into both the report file (for emailing) and the per-run log (for
# consecutive-failure detection + diagnosis). script(1) pty wrap so the CLI
# flushes incrementally instead of buffering until SIGKILL.
if /usr/bin/timeout "$TIMEOUT_SECS" script -e -q -a -c "$CLAUDE_BIN -p '/blog-calibrate ${YM}' --dangerously-skip-permissions" "$PER_RUN_LOG" >/dev/null 2>&1; then
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

# Publish whatever /blog-calibrate produced: calibration-YYYY-MM.md and any
# patterns.jsonl change, committed in the workspace and pushed to origin. Any
# commit touching another path is refused (DEGRADED, workspace kept). A failed
# push keeps the workspace and makes the run DEGRADED; the next run republishes
# it at startup, or a human runs $RECOVER.
if [ "$STATUS" = "OK" ]; then
  if periodic_workspace_publish "$WS" "$LOG" "chore(methodology): ${YM} calibration report + pattern updates" \
      "$OUT_ALLOWED" "$METH_REL/calibration-${YM}.md" "$METH_REL/patterns.jsonl"; then
    log "✓ calibrate output: ${WS_NOTE}"
    cd "$LOG_DIR" || true
    periodic_workspace_close "$BLOG_DIR" "$WS" "$LOG" || true
  else
    STATUS="DEGRADED (report not published: ${WS_NOTE})"
    RECOVER="git -C $WS push origin HEAD:refs/heads/${WS_BRANCH} (or wait for the next run's startup reconcile)"
    log "⚠ calibrate output NOT published — ${WS_NOTE}. Workspace kept. Recover: $RECOVER"
  fi
else
  cd "$LOG_DIR" || true
  periodic_workspace_close "$BLOG_DIR" "$WS" "$LOG" || true
fi

# Consecutive-failure escalation (lower threshold than daily — monthly runs
# once, so two failures is a 60-day gap).
CONSEC_FAILS=$(count_consecutive_failures "$LOG_DIR" "target-*.log" "FATAL|TIMED OUT|FAILED" 12)
ESCALATE_PREFIX=""
if [ "$CONSEC_FAILS" -ge 2 ]; then
  log "ESCALATION: ${CONSEC_FAILS} consecutive failed calibrate runs — elevating alert priority"
  ESCALATE_PREFIX="🚨 ${CONSEC_FAILS}-MONTH STREAK: "
fi

# Buzz sys-automation on a hard failure only (dormant until governed Buzz dispatch
# is set in ~/.env). See scripts/blog/lib-cron-common.sh § cron_fail.
case "$STATUS" in
  FAILED*|DEGRADED*) cron_fail "blog-monthly-calibrate" "${ESCALATE_PREFIX}${YM}: ${STATUS} (${CONSEC_FAILS}-month streak).${RECOVER:+ Recover: $RECOVER.} Log: $LOG" ;;
esac

SUBJECT="${ESCALATE_PREFIX}Monthly blog calibration: ${YM} — ${STATUS}"
BODY="Calibration report for ${YM} (period [${PERIOD_START}, ${PERIOD_END})).
Status: ${STATUS}${RECOVER:+
Recover: ${RECOVER}}
Consecutive failures (incl. this run): ${CONSEC_FAILS}

Source: origin/${WS_BRANCH:-master}:${METH_REL}/decisions.jsonl (workspace snapshot)
Per-run log: $PER_RUN_LOG

================================================================================

$(cat "$REPORT")
"

if node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io --subject "$SUBJECT" --body "$BODY" >> "$LOG" 2>&1; then
  log "Emailed report"
else
  log "EMAIL FAILED — report kept at $REPORT"
fi

# Normal notification path completed — disarm the fail-loud trap.
NOTIFIED=1
log "=== Monthly calibration end ==="

# Exit truthfully for the liveness trap (review finding on PR #26): a handled
# failure must still exit non-zero so the EXIT trap withholds .ok and the estate
# sweep's running-but-failing signal stays live. NOTIFIED=1 above guarantees the
# trap does NOT double-alert.
case "$STATUS" in OK*) : ;; *) exit 1 ;; esac
