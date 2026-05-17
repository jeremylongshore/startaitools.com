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

# ntfy low-priority (weekly housekeeping)
NTFY_TOPIC=$(cat /home/jeremy/.ntfy-topic 2>/dev/null)
if [ -n "$NTFY_TOPIC" ]; then
  curl -s -H "Title: feedback-sweep ${STATUS}" -H "Priority: low" -H "Tags: chart_with_upwards_trend" \
    -d "${TS}: see email for digest" \
    "https://ntfy.sh/$NTFY_TOPIC" >> "$LOG" 2>&1 || true
fi

log "=== feedback-sweep end ==="
