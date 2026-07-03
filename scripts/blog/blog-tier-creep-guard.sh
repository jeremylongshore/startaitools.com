#!/usr/bin/env bash
# blog-tier-creep-guard.sh — weekly deterministic tier-distribution tripwire.
#
# Runs tier-creep-guard.py against decisions.jsonl. Alerts (ntfy high + email)
# ONLY when the rolling tier distribution breaches its tolerance bands — catches
# Tier-2/3 inflation AND Tier-1 over-deflation. Silent when healthy (tripwire
# semantics: no news is good news). No LLM, reads one file, writes nothing
# tracked — so it never dirties the tree for the daily backfill's preflight.
#
# Schedule: weekly, Sunday 11:00 local (after the 10:00 feedback-sweep settles).

set -uo pipefail

LOG_DIR=/home/jeremy/.local/state/blog-tier-creep-guard
mkdir -p "$LOG_DIR"
TS=$(date +%Y-%m-%d)
LOG="$LOG_DIR/guard-${TS}.log"
GUARD=/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/scripts/tier-creep-guard.py
EMAIL_SCRIPT=/home/jeremy/.claude/skills/email/scripts/send-email.cjs

log() { echo "[$(date -Is)] $*" | tee -a "$LOG"; }
log "=== tier-creep-guard start ==="

if [ ! -f "$GUARD" ]; then
  log "FATAL: $GUARD not found"
  exit 1
fi

REPORT=$(python3 "$GUARD" 2>&1)
RC=$?
echo "$REPORT" | tee -a "$LOG"

if [ "$RC" -eq 0 ]; then
  log "HEALTHY — no alert sent"
  log "=== tier-creep-guard end ==="
  exit 0
fi

if [ "$RC" -ge 2 ]; then
  log "guard errored (rc=$RC) — treating as alert"
fi

# --- Breach (or error): alert ------------------------------------------------
SUBJECT="⚠ Blog tier creep detected — ${TS}"
BODY="The deterministic tier-distribution guard tripped on ${TS}.

${REPORT}

--------------------------------------------------------------------------------
This is an early-warning tripwire. To act:
  1. Run /blog-calibrate for the full analysis (Brier, dimension breakdown).
  2. If Tier-2 is inflated, tighten the narrative-or-standout floor
     (pattern auto-2026-07-001) in content-tier-classification.md — e.g. require
     a dimension>=4 (drop the NAR>=3 escape) or raise the T2 gate floor.
  3. If Tier-1 is over-deflated (>85%), the classifier is too timid — relax.

Full log: ${LOG}
Guard: ${GUARD}
"

node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io --subject "$SUBJECT" --body "$BODY" >> "$LOG" 2>&1 \
  && log "Alert email sent" || log "Email send failed — report preserved in log"

NTFY_TOPIC=$(cat /home/jeremy/.ntfy-topic 2>/dev/null)
if [ -n "$NTFY_TOPIC" ]; then
  curl -s -H "Title: Blog tier creep detected" -H "Priority: high" -H "Tags: warning,chart_with_downwards_trend" \
    -d "${TS}: tier distribution breached tolerance — see email + run /blog-calibrate" \
    "https://ntfy.sh/$NTFY_TOPIC" >> "$LOG" 2>&1 || true
fi

log "=== tier-creep-guard end (ALERT) ==="
