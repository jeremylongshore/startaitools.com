#!/usr/bin/env bash
# blog-feedback-sweep.sh — weekly cron wrapper for feedback-sweep.py
#
# Runs the deterministic retrospective grader against every classifier record
# without a feedback.jsonl entry. Emails the digest. No LLM in the loop.
#
# Schedule: weekly, Sunday 10:00 local (cron line in $HOME crontab).

set -uo pipefail

LOG_DIR=/home/jeremy/.local/state/blog-feedback-sweep
mkdir -p "$LOG_DIR"

# Liveness heartbeat: drop a per-run beat so the estate dead-man's-switch
# (~/bin/automation-liveness-sweep.sh) can tell this schedule still fires. The
# beat marks "the cron ran"; fail-alerting (below) covers "ran but failed".
mkdir -p "$HOME/.local/state/notify-lib" 2>/dev/null || true
: > "$HOME/.local/state/notify-lib/blog-feedback-sweep.beat" 2>/dev/null || true

TS=$(date +%Y-%m-%d)
LOG="$LOG_DIR/sweep-${TS}.log"
SCRIPT=/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/scripts/feedback-sweep.py
EMAIL_SCRIPT=/home/jeremy/.claude/skills/email/scripts/send-email.cjs

# Shared helper: slack_fail (posts failures to #cron-failures). Side-effect-free
# at source time — defines functions only.
# shellcheck source=./lib-cron-common.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib-cron-common.sh"

log() { echo "[$(date -Is)] $*" | tee -a "$LOG"; }
log "=== feedback-sweep start ==="

# --- Fail-loud guard: an early exit must never be silent ----------------------
# Before this trap the only alerting was a best-effort email whose own failure
# was merely logged — the FATAL below (feedback-sweep.py missing/not executable)
# EXITed with ZERO Slack alert. Ported from blog-backfill-daily.sh: this fires on
# any non-zero exit that bypassed the normal notification and pings Slack
# #cron-failures + email. Clean exits (rc=0) and the normal path (NOTIFIED=1) are
# skipped.
NOTIFIED=0
notify_unexpected_exit() {
  local rc=$?
  liveness_markers "blog-feedback-sweep" "$rc"   # .beat every run; .ok iff rc==0
  [ "$rc" -eq 0 ] && return
  [ "$NOTIFIED" -eq 1 ] && return
  log "ABNORMAL EXIT (rc=$rc) before normal notification — sending fail-loud alert"
  slack_fail "blog-feedback-sweep" "${TS}: early exit rc=${rc} — sweep did not complete. Check ${LOG}"
  node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io \
    --subject "🚨 blog-feedback-sweep aborted early: ${TS} (rc=${rc})" \
    --body "$(printf 'Weekly blog feedback-sweep exited abnormally (rc=%s) BEFORE its normal summary email.\n\nNo digest was sent for %s.\n\nLast 30 log lines:\n--------------------------------------------------------------------------------\n%s\n' "$rc" "$TS" "$(tail -30 "$LOG" 2>/dev/null)")" \
    >/dev/null 2>&1 || true
}
trap notify_unexpected_exit EXIT

if [ ! -x "$SCRIPT" ]; then
  log "FATAL: $SCRIPT not executable"
  exit 1
fi

DIGEST=$("$SCRIPT" 2>&1 | tee -a "$LOG") || {
  log "feedback-sweep.py exited non-zero"
  STATUS="FAILED"
}
STATUS="${STATUS:-OK}"

# --- Commit (and best-effort push) the sweep's own output --------------------
# feedback-sweep.py appends records to feedback.jsonl. If those changes are left
# uncommitted, the NEXT daily blog-backfill aborts at its dirty-tree preflight
# guard (preflight_branch_normalize, lib-cron-common.sh) — which silently
# stalled the blog for 11 days from 2026-06-14 (bead startaitools-74z). A local
# commit is what unblocks the daily run; the push is best-effort (the daily
# backfill's FF-push carries it forward if this fails).
REPO=/home/jeremy/000-projects/blog/startaitools
FEEDBACK=.claude/skills/blog-backfill/methodology/feedback.jsonl
if [ "$STATUS" = "OK" ] && cd "$REPO" 2>/dev/null; then
  if git diff --quiet -- "$FEEDBACK" 2>/dev/null; then
    log "No feedback.jsonl changes to commit (sweep added 0 records)"
  elif git add "$FEEDBACK" && git commit -q -m "chore(methodology): weekly feedback-sweep ${TS}"; then
    log "Committed feedback.jsonl (weekly sweep ${TS}) — tree left clean for daily backfill"
    if git push -q >> "$LOG" 2>&1; then
      log "Pushed feedback.jsonl to origin"
    else
      log "WARN: push failed — committed locally; daily backfill will carry it forward"
    fi
  else
    log "WARN: git commit of feedback.jsonl failed — tree may be left dirty for daily backfill"
  fi
fi

BODY="Weekly feedback sweep for ${TS}
Status: ${STATUS}

================================================================================

${DIGEST}

================================================================================
Full log: ${LOG}
Source-of-truth: /home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/methodology/feedback.jsonl

Mismatches above are where the structural rubric disagrees with the classifier.
Review with:  /blog-feedback <slug> --correct        (rubric was right)
              /blog-feedback <slug> --wrong N        (override rubric)
"

SUBJECT="Weekly blog feedback-sweep: ${TS} — ${STATUS}"

node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io --subject "$SUBJECT" --body "$BODY" >> "$LOG" 2>&1 \
  || log "Email send failed — digest preserved in log"

# Normal notification path completed — disarm the fail-loud trap.
NOTIFIED=1
log "=== feedback-sweep end ==="

# Exit truthfully for the liveness trap (review finding on PR #26): a handled
# failure must still exit non-zero so the EXIT trap withholds .ok and the estate
# sweep's running-but-failing signal stays live. NOTIFIED=1 above guarantees the
# trap does NOT double-alert.
case "$STATUS" in OK*) exit 0 ;; *) exit 1 ;; esac
