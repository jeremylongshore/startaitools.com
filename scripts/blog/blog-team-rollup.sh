#!/usr/bin/env bash
# blog-team-rollup.sh — weekly growth rollup to the content team (WS2b).
#
# This is the team's cadence — it REPLACES the old daily 5-CC firehose. Once a
# week it produces a portfolio growth report and emails it to the whole team
# (TEAM_EMAILS), so per-post packets can go to Ezekiel alone.
#
# It reuses the same engine + recipient source as the growth flywheel:
#   - engine:     the /web-analytics skill (direct Umami REST, all 4 live sites)
#   - recipients: TEAM_EMAILS in intent-mail/.env (shared with blog-team-digest)
# and AUGMENTS the base brief with three growth-specific sections:
#   - the syndication UTM breakdown (which of X/LinkedIn/Substack/Medium drove
#     startaitools traffic — does Ezekiel's posting actually move the number?)
#   - one evergreen re-share nomination (a proven older post to re-post fresh)
#   - "amplify these" asks for the week
#
# The LLM PRODUCES the report to an HTML file; this wrapper emails it to the team
# deterministically (the skill's own --email path is jeremy-only). Fail-loud:
# an abnormal exit alerts Slack #cron-failures + emails Jeremy (ntfy retired 2026-06-13).

set -uo pipefail

LOG_DIR=/home/jeremy/.local/state/blog-team-rollup
mkdir -p "$LOG_DIR"
TODAY=$(date +%Y-%m-%d)
LOG="$LOG_DIR/run-${TODAY}.log"
EMAIL_SCRIPT=/home/jeremy/.claude/skills/email/scripts/send-email.cjs
BLOG_DIR=/home/jeremy/000-projects/blog/startaitools
LEDGER_FILE="$BLOG_DIR/.blog-syndication-ledger.json"
INTENT_MAIL_ENV=/home/jeremy/000-projects/intent-mail/.env
TIMEOUT_SECS="${ROLLUP_TIMEOUT:-1200}"

# shellcheck source=./lib-cron-common.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib-cron-common.sh"
log() { echo "[$(date -Is)] $*" | tee -a "$LOG"; }
log "=== Weekly team rollup start (${TODAY}) ==="

# Recipients from the shared source (env wins — lets a test scope to one address).
if [ -z "${TEAM_EMAILS:-}" ] && [ -f "$INTENT_MAIL_ENV" ]; then
  TEAM_EMAILS=$(grep -m1 '^TEAM_EMAILS=' "$INTENT_MAIL_ENV" 2>/dev/null | cut -d= -f2-)
fi
TEAM_EMAILS="${TEAM_EMAILS:-jeremy@intentsolutions.io}"
log "Team recipients: $TEAM_EMAILS"

# Fail-loud trap.
NOTIFIED=0
notify_unexpected_exit() {
  local rc=$?
  [ "$rc" -eq 0 ] && return
  [ "$NOTIFIED" -eq 1 ] && return
  log "ABNORMAL EXIT (rc=$rc) before normal notification — fail-loud alert"
  slack_fail "blog-team-rollup" "${TODAY}: rc=${rc} — NO rollup emailed. Check ${LOG}"
  node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io --subject "🚨 weekly team rollup aborted: ${TODAY} (rc=${rc})" \
    --body "$(printf 'The weekly team rollup exited abnormally (rc=%s). No rollup emailed.\n\nLast 30 log lines:\n%s\n' "$rc" "$(tail -30 "$LOG" 2>/dev/null)")" >/dev/null 2>&1 || true
}
trap notify_unexpected_exit EXIT

OUTPUT_HTML=$(mktemp --suffix=.html)
rm -f "$OUTPUT_HTML"   # the LLM creates it; we require its presence as the success gate

# --- Deterministic comparison windows -----------------------------------------
# Compute every date range in bash so the model never does date math (a common
# source of wrong deltas). 10#$DOM forces base-10 so 08/09 don't parse as octal.
DOM=$(date -d "$TODAY" +%d)
W_THIS_A=$(date -d "$TODAY -7 days" +%F);   W_THIS_B="$TODAY"
W_PREV_A=$(date -d "$TODAY -14 days" +%F);  W_PREV_B=$(date -d "$TODAY -7 days" +%F)
M_THIS_A=$(date -d "$TODAY" +%Y-%m-01);     M_THIS_B="$TODAY"
M_PREV_A=$(date -d "$M_THIS_A -1 month" +%F)
M_PREV_B=$(date -d "$M_PREV_A +$((10#$DOM - 1)) days" +%F)
Y_THIS_A=$(date -d "$TODAY" +%Y-01-01);     Y_THIS_B="$TODAY"
Y_PREV_A=$(date -d "$Y_THIS_A -1 year" +%F)
Y_PREV_B=$(date -d "$TODAY -1 year" +%F)
T12_A=$(date -d "$TODAY -1 year" +%F);      T12_B="$TODAY"

PROMPT="You are producing the WEEKLY GROWTH ROLLUP for the Intent Solutions content team. Do all of the following, then WRITE the final report as a single self-contained HTML fragment (no <html>/<head>, just a styled <div>) to this exact file using the Write tool: ${OUTPUT_HTML}

Data access: Umami REST, auth with UMAMI_PASSWORD from ~/.env (see the /web-analytics skill for the exact login + endpoints). Site IDs are in ~/.env: UMAMI_SITE_STARTAITOOLS, UMAMI_SITE_TONSOFSKILLS, UMAMI_SITE_JEREMYLONGSHORE, UMAMI_SITE_INTENTSOLUTIONS. Query Umami stats with startAt/endAt as epoch-MILLISECONDS (date -d '<YYYY-MM-DD>' +%s then append 000).

1. TIME-COMPARISON DASHBOARD (the headline section). For BOTH the portfolio total AND each of the four sites, report visitors AND pageviews for each window below, each with the delta % vs its comparison window. Use these EXACT pre-computed ranges — do not compute your own:
   - Week over week (WoW):   this [${W_THIS_A} .. ${W_THIS_B}]  vs prior [${W_PREV_A} .. ${W_PREV_B}]
   - Month over month (MoM): this [${M_THIS_A} .. ${M_THIS_B}]  vs prior [${M_PREV_A} .. ${M_PREV_B}]  (same day-of-month range, apples to apples)
   - Year over year (YoY):   YTD [${Y_THIS_A} .. ${Y_THIS_B}]   vs prior-year same range [${Y_PREV_A} .. ${Y_PREV_B}]
   - Year-to-date TOTAL:     [${Y_THIS_A} .. ${Y_THIS_B}]
   - Trailing 12 months TOTAL: [${T12_A} .. ${T12_B}]
   Present as a clean table: rows = Portfolio + each site, columns = WoW %, MoM %, YoY %, YTD total, T12 total. Use ▲/▼ + the % for deltas.
   DATA-AVAILABILITY RULE: if a site has no history for a comparison window (Umami returns 0 for the prior period because tracking started later), do NOT print a fake or infinite delta — write 'n/a (tracking started <date>)' or 'new' instead. Be honest about which numbers are trustworthy.
2. TOP CONTENT & SOURCES: for each site, top 3 pages and top 3 referrers this week (${W_THIS_A} .. ${W_THIS_B}).
3. SYNDICATION UTM BREAKDOWN (startaitools only): use Umami's UTM report / utm_source filtering to show which of x / linkedin / substack / medium drove traffic this week (visits + WoW trend). This measures whether the team's posting is working. If a source shows zero, say so plainly.
4. EVERGREEN RE-SHARE NOMINATION: nominate exactly ONE older (>30 days) high-performing startaitools post for the team to re-share on X with a fresh angle. Give the live URL + a one-line 'fresh raw angle' suggestion Ezekiel can run with.
5. AMPLIFY THESE: 2-3 concrete asks for the team this week (which post to boost, which channel is underperforming and what to do).

Recently-syndicated posts (for context on what was posted) are in the ledger: ${LEDGER_FILE} (may be empty). Keep the whole thing skimmable for a busy team — this replaces a daily email, so it must earn the open. Do NOT email anything yourself; the wrapper emails the file. Write ONLY to ${OUTPUT_HTML}."

log "Invoking claude -p for the rollup report (timeout ${TIMEOUT_SECS}s)..."
T0=$(date +%s)
if /usr/bin/timeout "$TIMEOUT_SECS" script -e -q -a -c "claude -p '$(printf '%s' "$PROMPT" | sed "s/'/'\\\\''/g")' --dangerously-skip-permissions" "$LOG" >/dev/null 2>&1; then
  WALL=$(( $(date +%s) - T0 )); log "claude -p exited cleanly after ${WALL}s"
else
  EXIT=$?; WALL=$(( $(date +%s) - T0 )); log "claude -p exited non-zero ($EXIT) after ${WALL}s"
fi

# Success gate: the report file must exist and be non-trivial.
if [ -s "$OUTPUT_HTML" ] && [ "$(wc -c < "$OUTPUT_HTML")" -gt 400 ]; then
  STATUS="OK"
  # Email to the team (comma list → repeatable --to).
  declare -a TO_ARGS=()
  IFS=',' read -ra _tos <<< "$TEAM_EMAILS"
  for t in "${_tos[@]}"; do t=$(echo "$t" | xargs); [ -n "$t" ] && TO_ARGS+=(--to "$t"); done
  if node "$EMAIL_SCRIPT" "${TO_ARGS[@]}" --subject "📊 Weekly growth rollup — week of ${TODAY}" --html "$OUTPUT_HTML" >> "$LOG" 2>&1; then
    log "Rollup emailed to team ($(( ${#TO_ARGS[@]} / 2 )) recipients)"
  else
    STATUS="FAILED (email send)"; log "ERROR: rollup email failed"
  fi
else
  STATUS="FAILED (no report produced)"
  log "ERROR: claude -p did not write a usable report to $OUTPUT_HTML"
fi

# Notifications.
CONSEC_FAILS=$(count_consecutive_failures "$LOG_DIR" "run-*.log" "FAILED|ABNORMAL" 8)
case "$STATUS" in FAILED*) slack_fail "blog-team-rollup" "${TODAY}: ${STATUS}. Log: $LOG" ;; esac
# On failure, also email Jeremy the log tail (Slack #cron-failures already pinged above).
if [ "$STATUS" != "OK" ]; then
  node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io --subject "Weekly rollup FAILED: ${TODAY}" \
    --body "$(printf 'Status: %s\nConsecutive fails: %s\n\nLast 40 log lines:\n%s\n' "$STATUS" "$CONSEC_FAILS" "$(tail -40 "$LOG")")" >> "$LOG" 2>&1 || true
fi

rm -f "$OUTPUT_HTML" 2>/dev/null || true
NOTIFIED=1
log "=== Weekly team rollup end (${STATUS}) ==="