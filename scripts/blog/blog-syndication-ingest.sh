#!/usr/bin/env bash
# Close the syndication feedback loop, and alarm when it goes quiet.
#
# Runs ingest-syndication-replies.py in two passes:
#   ingest  parse the poster's packet replies -> record real URLs in the ledger
#   check   dead-man: packeted posts with nothing recorded after N hours
#
# WHY THIS EXISTS: the poster's SOP says "reply to the packet with the URLs",
# but nothing read those replies, so every ledger destination stayed "pending"
# forever and the Monday rollup reported zero syndication as though no work had
# happened. On 2026-08-05 that silent gap was 29 posts deep, back to 2026-07-05.
# An open loop with no alarm is indistinguishable from a loop nobody is running.
#
# Fail-loud, read-only on the mailbox, and safe to run by hand at any time.

set -uo pipefail

BLOG_DIR="${BLOG_DIR:-$HOME/000-projects/blog/startaitools}"
LOG_DIR="$HOME/.local/state/blog-syndication-ingest"
LOG="$LOG_DIR/ingest-$(date +%F).log"
INGEST="$BLOG_DIR/scripts/blog/ingest-syndication-replies.py"
STALE_HOURS="${STALE_HOURS:-48}"

mkdir -p "$LOG_DIR"

# PATH first, log open before any precondition: a script that dies before its
# log exists is indistinguishable from one that never ran. (Learned 2026-08-05,
# the backup-fabric incident: one script lacked this and failed silently for
# eight nights.)
export PATH="/usr/local/bin:/usr/bin:/bin:$HOME/bin:$PATH"

log() { echo "[$(date -Is)] $*" | tee -a "$LOG"; }

log "=== syndication ingest start ==="

# Governed Buzz dispatch (cron_fail / liveness markers); no-op if unavailable.
INTENT_RUNTIME="${INTENT_RUNTIME:-$HOME/bin/lib/intent-runtime.sh}"
if [ -r "$INTENT_RUNTIME" ]; then
  # shellcheck disable=SC1090
  . "$INTENT_RUNTIME" 2>/dev/null || true
fi

alert() {
  local msg="$1"
  if command -v cron_fail >/dev/null 2>&1; then
    cron_fail "blog-syndication-ingest" "$msg"
  fi
}

if [ ! -f "$INGEST" ]; then
  log "FATAL: $INGEST missing"
  alert "ingester script missing at $INGEST"
  exit 1
fi

# --- Pass 1: ingest replies -------------------------------------------------
if python3 "$INGEST" ingest --days "${INGEST_DAYS:-14}" >> "$LOG" 2>&1; then
  log "ingest OK"
else
  rc=$?
  log "ingest FAILED (rc=$rc)"
  alert "reply ingest failed rc=$rc; see $LOG"
fi

# --- Pass 2: dead-man check (hysteresis) ------------------------------------
# Packets going out with nothing coming back is a real operational failure
# (poster inactive, mailbox misrouted, or parser drift) and is exactly the
# condition that hid for a month. Exit contract mirrors blog-tier-creep-guard:
#   0 silent (healthy, or a persistent breach already alerted)
#   1 ALERT  (onset or worsening)
#   3 RECOVER (one-time all-clear)
# Hysteresis is why this is safe to run daily: a known-broken state that has
# not worsened stays quiet instead of paging every morning.
python3 "$INGEST" check --stale-hours "$STALE_HOURS" >> "$LOG" 2>&1
CHECK_RC=$?

case "$CHECK_RC" in
  0)
    log "check silent (healthy, or persistent gap suppressed by hysteresis)"
    ;;
  1)
    STALE_COUNT=$(grep -oE "SYNDICATION GAP: [0-9]+" "$LOG" | tail -1 | grep -oE "[0-9]+")
    log "ALERT: syndication gap onset/worsening (${STALE_COUNT:-?} post(s))"
    alert "${STALE_COUNT:-?} packeted post(s) have no recorded syndication after ${STALE_HOURS}h (onset/worsening) — poster inactive or replies not reaching the ingester"
    ;;
  3)
    log "RECOVERED: syndication gap cleared"
    ;;
  *)
    log "check errored (rc=$CHECK_RC)"
    alert "syndication check errored rc=$CHECK_RC"
    ;;
esac

# Liveness markers so the estate dead-man's-switch sees this schedule fire.
if command -v liveness_markers >/dev/null 2>&1; then
  liveness_markers "blog-syndication-ingest" 0
else
  mkdir -p "$HOME/.local/state/intent-os/liveness" 2>/dev/null || true
  : > "$HOME/.local/state/intent-os/liveness/blog-syndication-ingest.beat" 2>/dev/null || true
fi

log "=== syndication ingest end ==="
exit 0
