#!/usr/bin/env bash
# Daily portfolio web-analytics email to Jeremy. Runs each morning via cron.
#
# Invokes the /web-analytics skill headlessly. The SKILL itself emails the brief
# to jeremy@intentsolutions.io (its `--email` delivery path, hardcoded recipient).
# This wrapper is deliberately thin — it does NOT send the analytics content; it
# only provides the same operational spine as the blog crons:
#   - a wall-clock ceiling + pty-wrapped incremental logging
#   - fail-loud alerting (ntfy + email) if the headless agent errors, so a silent
#     stall can never recur the way blog-backfill did (startaitools-74z)
#   - consecutive-failure escalation + optional #cron-failures Slack
#
# Independent of the blog pipeline: no git, no staging, no publish, no branch
# normalize. Portfolio scope (startaitools, tonsofskills, jeremylongshore,
# intentsolutions) + recipient are the skill's defaults — see
# ~/.claude/skills/web-analytics/SKILL.md Step 4 (Email delivery).
#
# Agent: WEB_ANALYTICS_AGENT=minimax|grok|claude (default: minimax). Claude's weekly
# rate-limit killed the 2026-07-15 06:30 run (exit 1 in ~8s). Grok loads the
# skill via Claude-compat discovery (~/.claude/skills/web-analytics). Data path
# is Umami REST (curl + UMAMI_PASSWORD from ~/.env), not a required MCP server.
# Override WEB_ANALYTICS_AGENT=claude after the limit resets if you want the
# original path.
#
# Tunables (env):
#   WEB_ANALYTICS_TIER      mini | medium | full   (default: medium)
#   WEB_ANALYTICS_TIMEOUT   hard ceiling seconds    (default: 900)
#   WEB_ANALYTICS_AGENT     minimax | grok | claude (default: minimax)
#   WEB_ANALYTICS_MAX_TURNS max agent turns (grok)  (default: 100)

set -uo pipefail

# Cron PATH is minimal — keep local tools reachable.
export PATH="${HOME}/.local/bin:${HOME}/.bun/bin:${HOME}/bin:/usr/local/bin:/usr/bin:/bin:${PATH:-}"

LOG_DIR=/home/jeremy/.local/state/web-analytics-daily
mkdir -p "$LOG_DIR"

# Liveness heartbeat: drop a per-run beat so the estate dead-man's-switch
# (~/bin/automation-liveness-sweep.sh) can tell this schedule still fires. The
# beat marks "the cron ran"; the fail-loud trap below covers "ran but failed".
mkdir -p "$HOME/.local/state/notify-lib" 2>/dev/null || true
: > "$HOME/.local/state/notify-lib/web-analytics-daily.beat" 2>/dev/null || true

TODAY=$(date +%Y-%m-%d)
LOG="$LOG_DIR/run-${TODAY}.log"
EMAIL_SCRIPT=/home/jeremy/.claude/skills/email/scripts/send-email.cjs
SKILL_DIR="${HOME}/.claude/skills/web-analytics"
TIER="${WEB_ANALYTICS_TIER:-medium}"
TIMEOUT_SECS="${WEB_ANALYTICS_TIMEOUT:-900}"
WEB_ANALYTICS_AGENT="${WEB_ANALYTICS_AGENT:-minimax}"
WEB_ANALYTICS_MAX_TURNS="${WEB_ANALYTICS_MAX_TURNS:-100}"
GROK_BIN="${GROK_BIN:-$(command -v grok 2>/dev/null || true)}"
CLAUDE_BIN="${CLAUDE_BIN:-$(command -v claude 2>/dev/null || true)}"

# Shared helpers: count_consecutive_failures, slack_fail, _log.
# shellcheck source=./lib-cron-common.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib-cron-common.sh"

log() { echo "[$(date -Is)] $*" | tee -a "$LOG"; }

# Umami REST needs UMAMI_PASSWORD — skill sources ~/.env, but export it here so
# any shell the agent spawns already has it (cron does not load user profile).
if [ -z "${UMAMI_PASSWORD:-}" ] && [ -r "$HOME/.env" ]; then
  # shellcheck disable=SC1090
  set -a
  # shellcheck disable=SC1091
  source "$HOME/.env"
  set +a
fi

resolve_agent() {
  case "${WEB_ANALYTICS_AGENT}" in
    grok|Grok|GROK)
      if [ -n "$GROK_BIN" ] && [ -x "$GROK_BIN" ]; then
        AGENT_NAME=grok; AGENT_BIN="$GROK_BIN"; return 0
      fi
      if [ -n "$CLAUDE_BIN" ] && [ -x "$CLAUDE_BIN" ]; then
        log "WARN: WEB_ANALYTICS_AGENT=grok but grok not on PATH — falling back to claude"
        AGENT_NAME=claude; AGENT_BIN="$CLAUDE_BIN"; return 0
      fi
      ;;
    claude|Claude|CLAUDE)
      if [ -n "$CLAUDE_BIN" ] && [ -x "$CLAUDE_BIN" ]; then
        AGENT_NAME=claude; AGENT_BIN="$CLAUDE_BIN"; return 0
      fi
      if [ -n "$GROK_BIN" ] && [ -x "$GROK_BIN" ]; then
        log "WARN: WEB_ANALYTICS_AGENT=claude but claude not on PATH — falling back to grok"
        AGENT_NAME=grok; AGENT_BIN="$GROK_BIN"; return 0
      fi
      ;;
    *)
      log "FATAL: unknown WEB_ANALYTICS_AGENT=${WEB_ANALYTICS_AGENT} (want minimax|grok|claude)"; return 1
      ;;
  esac
  log "FATAL: no agent binary found (grok=$GROK_BIN claude=$CLAUDE_BIN)"; return 1
}

log "=== Daily web-analytics email start (tier: ${TIER}, target: ${TODAY}) ==="

if [ "${WEB_ANALYTICS_AGENT}" = "minimax" ]; then
  log "agent: minimax deterministic pipeline (Umami fetch -> MiniMax M3 narrative -> render -> send)"
else
  if ! resolve_agent; then
    log "FATAL: cannot resolve agent"; exit 1
  fi
  log "agent resolved: name=${AGENT_NAME} bin=${AGENT_BIN} (WEB_ANALYTICS_AGENT=${WEB_ANALYTICS_AGENT})"
fi

# --- Fail-loud guard: an early/abnormal exit must never be silent ---
# Mirrors blog-backfill-daily.sh. If the agent or anything before the normal
# notify block exits non-zero, push a high-priority alert + email so a broken
# analytics cron surfaces the same day instead of quietly not-emailing for days.
NOTIFIED=0
notify_unexpected_exit() {
  local rc=$?
  liveness_markers "web-analytics-daily" "$rc"   # .beat every run; .ok iff rc==0
  [ "$rc" -eq 0 ] && return
  [ "$NOTIFIED" -eq 1 ] && return
  log "ABNORMAL EXIT (rc=$rc) before normal notification — sending fail-loud alert"
  # ntfy retired 2026-06-13 — route the abnormal-exit alert to #cron-failures
  # via lib-cron-common:slack_fail (already sourced above). Email still fires below.
  slack_fail "web-analytics-daily" "aborted early: exit rc=${rc} — NO analytics brief emailed. Check ${LOG}"
  node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io \
    --subject "🚨 web-analytics email aborted early: ${TODAY} (rc=${rc})" \
    --body "$(printf 'The daily web-analytics cron exited abnormally (rc=%s) BEFORE completing.\nNo analytics brief was emailed for %s.\n\nLast 30 log lines:\n--------------------------------------------------------------------------------\n%s\n' "$rc" "$TODAY" "$(tail -30 "$LOG" 2>/dev/null)")" \
    >/dev/null 2>&1 || true
}
trap notify_unexpected_exit EXIT

# MiniMax path: a deterministic pipeline owns fetch + render + send. Numbers come from Umami REST,
# MiniMax M3 writes ONLY the narrative (one API call), the shared renderer owns 100% of the HTML, and
# send-email.cjs --html delivers. The email can never go out plain or with wrong numbers regardless of
# the model; if MiniMax is unavailable the pipeline uses a deterministic fallback narrative. The key is
# read from local SOPS if present (it is a GH Actions secret today — add it to the LLM-keys .env.sops
# to enable MiniMax narration; until then the correct-numbers fallback runs).
if [ "${WEB_ANALYTICS_AGENT}" = "minimax" ]; then
  MINIMAX_SOPS="$HOME/000-projects/intent-eval-platform/intent-eval-lab/.env.sops"
  if [ -z "${MINIMAX_API_KEY:-}" ] && [ -r "$MINIMAX_SOPS" ] && command -v sops >/dev/null 2>&1; then
    MINIMAX_API_KEY="$(sops -d --input-type dotenv --output-type dotenv "$MINIMAX_SOPS" 2>/dev/null | sed -nE 's/^MINIMAX_API_KEY=(.*)$/\1/p' | tr -d "\"'" )"
    export MINIMAX_API_KEY
  fi
  log "Invoking: MiniMax deterministic pipeline (timeout ${TIMEOUT_SECS}s)"
  T0=$(date +%s)
  if /usr/bin/timeout "$TIMEOUT_SECS" python3 "$SKILL_DIR/scripts/web-analytics-minimax.py" >>"$LOG" 2>&1; then
    STATUS="OK"; WALL=$(( $(date +%s) - T0 ))
    log "MiniMax pipeline delivered the brief after ${WALL}s ($((WALL/60))m $((WALL%60))s)"
  else
    EXIT=$?; WALL=$(( $(date +%s) - T0 )); STATUS="FAILED (exit $EXIT)"
    log "MiniMax pipeline exited non-zero (exit $EXIT) after ${WALL}s"
  fi
  PIPELINE_DONE=1
fi

# Run the skill headlessly (grok/claude agentic path). script(1) gives the agent a pty so its CLI
# flushes incrementally instead of buffering until SIGKILL (same rationale as the blog crons).
if [ -z "${PIPELINE_DONE:-}" ]; then
export CLAUDE_SKILL_DIR="$SKILL_DIR"
AGENT_CMD=""
case "$AGENT_NAME" in
  grok)
    AGENT_CMD="$AGENT_BIN -p '/web-analytics ${TIER} --email' --always-approve --max-turns ${WEB_ANALYTICS_MAX_TURNS} --cwd '$HOME' --rules 'CLAUDE_SKILL_DIR=$SKILL_DIR. Use absolute path $SKILL_DIR for references/ and agents/. Source ~/.env for UMAMI_PASSWORD; fetch Umami via REST (analytics.intentsolutions.io) per the skill. Deliver via /email skill to jeremy@intentsolutions.io. Prefer medium-tier path without infinite agent fanout.'"
    ;;
  claude)
    AGENT_CMD="$AGENT_BIN -p '/web-analytics ${TIER} --email' --dangerously-skip-permissions"
    ;;
esac

log "Invoking: ${AGENT_NAME} -p /web-analytics ${TIER} --email (timeout ${TIMEOUT_SECS}s, max-turns ${WEB_ANALYTICS_MAX_TURNS}, pty-wrapped)"
T0=$(date +%s)
if CLAUDE_SKILL_DIR="$SKILL_DIR" /usr/bin/timeout "$TIMEOUT_SECS" script -e -q -a \
     -c "$AGENT_CMD" \
     "$LOG" >/dev/null 2>&1; then
  STATUS="OK"
  WALL=$(( $(date +%s) - T0 ))
  log "${AGENT_NAME} -p exited cleanly after ${WALL}s ($((WALL/60))m $((WALL%60))s)"
else
  EXIT=$?
  WALL=$(( $(date +%s) - T0 ))
  STATUS="FAILED (exit $EXIT)"
  if [ "$EXIT" = "124" ]; then
    log "${AGENT_NAME} -p TIMED OUT after ${WALL}s (hard ceiling ${TIMEOUT_SECS}s)"
  else
    log "${AGENT_NAME} -p exited non-zero (exit $EXIT) after ${WALL}s"
  fi
fi

# Soft delivery check: the skill exits 0 even if the /email step silently no-ops.
# Look for evidence an email was actually attempted (send-email.cjs / Analytics
# subject in the pty log). Absence downgrades to OK-WITH-WARNING — non-blocking,
# but it distinguishes "brief emailed" from "ran clean but sent nothing".
if [ "$STATUS" = "OK" ]; then
  if ! grep -qiE 'send-email|Analytics (mini|medium|full)|Message sent|messageId|Email sent|✓ Email' "$LOG" 2>/dev/null; then
    log "WARN: no email-send evidence in log — the brief may not have been delivered"
    STATUS="OK-WITH-WARNING (no email-send evidence)"
  fi
fi
fi  # end grok/claude agentic path (skipped when the MiniMax pipeline ran)

# Consecutive-failure escalation (same pattern as the blog crons).
CONSEC_FAILS=$(count_consecutive_failures "$LOG_DIR" "run-*.log" "FATAL|TIMED OUT|FAILED \(exit" 10)
ESCALATE_PREFIX=""
if [ "$CONSEC_FAILS" -ge 3 ]; then
  log "ESCALATION: ${CONSEC_FAILS} consecutive failed runs — elevating alert priority"
  ESCALATE_PREFIX="🚨 ${CONSEC_FAILS}-DAY STREAK: "
fi

# Slack #cron-failures on a hard failure only (dormant until the webhook is set).
case "$STATUS" in
  FAILED*) slack_fail "web-analytics-daily" "${ESCALATE_PREFIX}${TODAY}: ${STATUS} (${CONSEC_FAILS}-day streak). Log: $LOG" ;;
esac

# Notifications (ntfy retired 2026-06-13):
#  - OK: the analytics brief IS the deliverable email (sent by the skill). Success
#    needs no extra ping — no duplicate wrapper summary.
#  - OK-WITH-WARNING / FAILED: email Jeremy the full detail below; #cron-failures
#    already got the one-line escalation via slack_fail above (FAILED only).
case "$STATUS" in
  OK)
    : ;;   # success is the emailed brief itself — no extra chatter
  *)
    # Capture the tail BEFORE the append redirect so we don't read+write $LOG in
    # one pipeline (SC2094). Matches blog-backfill-daily.sh's pattern.
    TAIL=$(tail -50 "$LOG")
    FAIL_BODY=$(printf 'Daily web-analytics cron for %s\nStatus: %s\nConsecutive failures (incl. this run): %s\n\n================================================================================\nLast 50 log lines (full log: %s):\n================================================================================\n\n%s\n' "$TODAY" "$STATUS" "$CONSEC_FAILS" "$LOG" "$TAIL")
    node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io \
      --subject "${ESCALATE_PREFIX}Daily web-analytics: ${TODAY} — ${STATUS}" \
      --body "$FAIL_BODY" \
      >> "$LOG" 2>&1 || log "Email send failed — see log"
    # (#cron-failures already alerted via slack_fail above; ntfy removed.)
    ;;
esac

# Normal notification path completed — disarm the fail-loud trap.
NOTIFIED=1
log "=== Daily web-analytics email end (${STATUS}) ==="

# Exit truthfully for the liveness trap (review finding on PR #26): a handled
# failure must still exit non-zero so the EXIT trap withholds .ok and the estate
# sweep's running-but-failing signal stays live. NOTIFIED=1 above guarantees the
# trap does NOT double-alert.
case "$STATUS" in OK*) : ;; *) exit 1 ;; esac
