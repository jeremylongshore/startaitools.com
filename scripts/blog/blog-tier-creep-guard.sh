#!/usr/bin/env bash
# blog-tier-creep-guard.sh — weekly deterministic tier-distribution tripwire.
#
# Runs tier-creep-guard.py (stateful/hysteresis mode) against decisions.jsonl.
# The guard's exit code drives notification:
#   0 = silent  (healthy, or a persistent breach already alerted — hysteresis)
#   1 = ALERT   (breach onset or worsening) -> Slack #cron-failures + email
#   3 = RECOVER (was breached, now healthy) -> email (one-time all-clear)
#   2 = error   (decisions unreadable)      -> treat as alert (fail loud)
# Silent when a breach merely persists, so it isn't a weekly nag. No LLM. The
# guard's state file lives outside the repo, so nothing tracked is written and
# the daily backfill's dirty-tree preflight is never tripped.
#
# Schedule: weekly, Sunday 11:00 local (after the 10:00 feedback-sweep settles).

set -uo pipefail

# Shared helper: slack_fail (posts failures to #cron-failures). Side-effect-free
# at source time — defines functions only.
# shellcheck source=./lib-cron-common.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib-cron-common.sh"

LOG_DIR=/home/jeremy/.local/state/blog-tier-creep-guard
mkdir -p "$LOG_DIR"

# Liveness heartbeat: drop a per-run beat so the estate dead-man's-switch
# (~/bin/automation-liveness-sweep.sh) can tell this schedule still fires. The
# beat marks "the cron ran"; fail-alerting covers "ran but failed". Silence is
# never valid on this tripwire — even a healthy (rc=0, no-alert) week must beat.
mkdir -p "$HOME/.local/state/notify-lib" 2>/dev/null || true
: > "$HOME/.local/state/notify-lib/blog-tier-creep-guard.beat" 2>/dev/null || true

# Health marker: on exit, beat again and write <job>.ok iff this run ended
# rc==0 (two-marker protocol — see lib-cron-common.sh:liveness_markers). This
# script has no other EXIT trap; the trap-string `$?` expands at exit time.
trap 'liveness_markers "blog-tier-creep-guard" "$?"' EXIT

TS=$(date +%Y-%m-%d)
LOG="$LOG_DIR/guard-${TS}.log"
GUARD=/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/scripts/tier-creep-guard.py
EMAIL_SCRIPT=/home/jeremy/.claude/skills/email/scripts/send-email.cjs

log() { echo "[$(date -Is)] $*" | tee -a "$LOG"; }
log "=== tier-creep-guard start ==="

if [ ! -f "$GUARD" ]; then
  log "FATAL: $GUARD not found"
  # Fail loud: this early FATAL previously bypassed slack_fail, silently no-oping
  # the weekly tripwire (a missing guard means NO distribution check ran at all).
  slack_fail "blog-tier-creep-guard" "${TS}: FATAL — guard script missing (${GUARD}); weekly tier tripwire did NOT run. Check ${LOG}"
  exit 1
fi

REPORT=$(python3 "$GUARD" 2>&1)
RC=$?
echo "$REPORT" | tee -a "$LOG"

case "$RC" in
  0)
    log "silent — healthy or persistent breach suppressed by hysteresis"
    ;;
  3)
    log "RECOVER — sending one-time all-clear"
    node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io \
      --subject "✅ Blog tier distribution recovered — ${TS}" \
      --body "$(printf 'The tier distribution is back within tolerance.\n\n%s\n\nFull log: %s\n' "$REPORT" "$LOG")" \
      >> "$LOG" 2>&1 || log "all-clear email failed"
    ;;
  *)
    # rc=1 (alert) or rc>=2 (error) — fail loud either way
    [ "$RC" -ge 2 ] && log "guard errored (rc=$RC) — treating as alert"
    log "ALERT — breach onset/worsening (rc=$RC)"
    BODY="The deterministic tier-distribution guard tripped on ${TS}.

${REPORT}

--------------------------------------------------------------------------------
This alert fires on breach ONSET or WORSENING only (hysteresis suppresses a
merely-persistent breach). To act:
  1. Run /blog-calibrate for the full analysis (Brier, dimension breakdown).
  2. If Tier-2 is inflated, tighten the narrative-or-standout floor
     (pattern auto-2026-07-001) in content-tier-classification.md.
  3. If Tier-1 is over-deflated (>85%), the classifier is too timid — relax.

Full log: ${LOG}
Guard: ${GUARD}
"
    if node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io \
        --subject "⚠ Blog tier creep — ${TS}" --body "$BODY" >> "$LOG" 2>&1; then
      log "Alert email sent"
    else
      log "Email send failed — report preserved in log"
    fi
    slack_fail "blog-tier-creep-guard" "${TS}: tier distribution breached (onset/worsening) — see email + run /blog-calibrate"
    ;;
esac

log "=== tier-creep-guard end (rc=$RC) ==="
