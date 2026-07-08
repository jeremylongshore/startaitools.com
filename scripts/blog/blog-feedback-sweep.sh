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
TS=$(date +%Y-%m-%d)
LOG="$LOG_DIR/sweep-${TS}.log"
SCRIPT=/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/scripts/feedback-sweep.py
EMAIL_SCRIPT=/home/jeremy/.claude/skills/email/scripts/send-email.cjs

log() { echo "[$(date -Is)] $*" | tee -a "$LOG"; }
log "=== feedback-sweep start ==="

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

log "=== feedback-sweep end ==="
