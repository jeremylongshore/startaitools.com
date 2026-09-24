#!/usr/bin/env bash
# blog-team-rollup.sh — weekly growth rollup to the content team (WS2b).
#
# This is the team's cadence — it REPLACES the old daily 5-CC firehose. Once a
# week it produces a portfolio growth report and emails it to the whole team
# (TEAM_EMAILS), so per-post packets can go to Ezekiel alone.
#
# It reuses the same engine + recipient source as the growth flywheel:
#   - engine:     the /web-analytics skill (direct Umami REST, all sites in the installed estate registry)
#   - recipients: TEAM_EMAILS in intent-mail/.env (shared with blog-team-digest)
# and AUGMENTS the base brief with three growth-specific sections:
#   - the syndication UTM breakdown (which of X/LinkedIn/Substack/Medium drove
#     startaitools traffic — does Ezekiel's posting actually move the number?)
#   - one evergreen re-share nomination (a proven older post to re-post fresh)
#   - "amplify these" asks for the week
#
# The LLM PRODUCES the report to an HTML file; this wrapper emails it to the team
# deterministically (the skill's own --email path is jeremy-only). Fail-loud:
# an abnormal exit alerts Buzz sys-automation + emails Jeremy (ntfy retired 2026-06-13).

set -uo pipefail
umask 077

LOG_DIR="${ROLLUP_LOG_DIR:-/home/jeremy/.local/state/blog-team-rollup}"
mkdir -p "$LOG_DIR"

# Liveness heartbeat: drop a per-run beat so the estate dead-man's-switch
# (~/bin/automation-liveness-sweep.sh) can tell this schedule still fires. The
# beat marks "the cron ran"; the fail-loud trap below covers "ran but failed".
if [ "${ROLLUP_DRY_RUN:-0}" != 1 ]; then
  mkdir -p "$HOME/.local/state/intent-os/liveness" 2>/dev/null || true
  : > "$HOME/.local/state/intent-os/liveness/blog-team-rollup.beat" 2>/dev/null || true
fi

TODAY=$(date +%Y-%m-%d)
if [ "${ROLLUP_DRY_RUN:-0}" = 1 ] && [ -n "${ROLLUP_DATE:-}" ]; then
  if [ "$(date -d "$ROLLUP_DATE" +%F 2>/dev/null)" != "$ROLLUP_DATE" ] ||
     [ "$ROLLUP_DATE" \> "$(date +%F)" ]; then
    printf '%s\n' 'ROLLUP_DATE must be an ISO date no later than today' >&2
    exit 2
  fi
  TODAY="$ROLLUP_DATE"
fi
LOG="$LOG_DIR/run-${TODAY}.log"
EMAIL_SCRIPT="${ROLLUP_EMAIL_SCRIPT:-/home/jeremy/.claude/skills/email/scripts/send-email.cjs}"
BLOG_DIR="${ROLLUP_BLOG_DIR:-/home/jeremy/000-projects/blog/startaitools}"
LEDGER_FILE="$BLOG_DIR/.blog-syndication-ledger.json"
INTENT_MAIL_ENV=/home/jeremy/000-projects/intent-mail/.env
TIMEOUT_SECS="${ROLLUP_TIMEOUT:-1200}"
ROLLUP_PROVIDER="${ROLLUP_PROVIDER:-minimax}"
ANALYTICS_SKILL_DIR="${ANALYTICS_SKILL_DIR:-$HOME/.claude/skills/web-analytics}"
REGISTRY_HELPER="$ANALYTICS_SKILL_DIR/scripts/estate_registry.py"
ROLLUP_AGENT_BIN="${ROLLUP_AGENT_BIN:-/home/jeremy/.local/bin/claude}"
ROLLUP_MINIMAX_KEY_FILE="${ROLLUP_MINIMAX_KEY_FILE:-$HOME/.config/intentsolutions/api-providers.sops.json}"
ROLLUP_SOPS_BIN="${ROLLUP_SOPS_BIN:-$HOME/bin/sops}"
ROLLUP_MINIMAX_MODEL="${ROLLUP_MINIMAX_MODEL:-MiniMax-M3}"

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
  [ "${ROLLUP_DRY_RUN:-0}" = 1 ] && return
  liveness_markers "blog-team-rollup" "$rc"   # .beat every run; .ok iff rc==0
  [ "$rc" -eq 0 ] && return
  [ "$NOTIFIED" -eq 1 ] && return
  log "ABNORMAL EXIT (rc=$rc) before normal notification — fail-loud alert"
  cron_fail "blog-team-rollup" "${TODAY}: rc=${rc} — NO rollup emailed. Check ${LOG}"
  node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io --subject "🚨 weekly team rollup aborted: ${TODAY} (rc=${rc})" \
    --body "$(printf 'The weekly team rollup exited abnormally (rc=%s). No rollup emailed.\n\nLast 30 log lines:\n%s\n' "$rc" "$(tail -30 "$LOG" 2>/dev/null)")" >/dev/null 2>&1 || true
}
trap notify_unexpected_exit EXIT

OUTPUT_HTML=$(mktemp --suffix=.html)
rm -f "$OUTPUT_HTML"   # the LLM creates it; we require its presence as the success gate

# Age eligible `pending` syndication rows to `assumed_posted` BEFORE the model
# reads the ledger. Without this the rollup sees rows nobody has ever written to
# and, on 2026-08-11, reported them to the whole team as a 38-post backlog owed by
# Ezekiel. Idempotent and deterministic; failure here must not abort the rollup.
RECONCILE="$(dirname "${BASH_SOURCE[0]}")/syndication-reconcile.py"
if [ "${ROLLUP_DRY_RUN:-0}" != 1 ] && [ -f "$RECONCILE" ]; then
  python3 "$RECONCILE" >> "$LOG" 2>&1 || log "WARN: syndication reconcile failed; rollup continues"
fi

# Both scheduled reports consume the same installed, versioned site registry.
# Do not silently fall back to the former four-site prompt if it is missing.
if ! ESTATE_SITES=$(python3 "$REGISTRY_HELPER"); then
  log "ERROR: analytics registry is unavailable or invalid"
  exit 1
fi

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

Data access: Umami REST, auth with UMAMI_PASSWORD from ~/.env. The ENTIRE site selection below comes from the same registry as the daily report. Include a separate table row for EVERY domain, even when there is zero traffic or a query fails. A failed query is unavailable, never zero. Use the explicit website_id; when hostname is non-null pass hostname=<exact value> to EVERY stats/metrics request. This separates OMA from the main company site and excludes DiagnosticPro test traffic. Never sum an unfiltered shared property alongside its hostname-filtered rows. Do not use the old UMAMI_SITE_* env variables or static Markdown registry to choose sites.
${ESTATE_SITES}

Before querying, list ALL Umami properties with pagination (pageSize=100, then page increments until count is satisfied). Check that each configured property exists and matches property_domain, and flag any unregistered-in-config property as a coverage gap. Query stats using startAt/endAt as epoch milliseconds; endAt is exclusive boundary minus 1 ms. Windows below use the scheduler timezone (fixed UTC-06:00). Portfolio visitors are summed site counts, not estate-wide distinct people. No prior traffic means no percentage baseline; use n/a. Use actual data availability, never invent a tracking start date.

1. TIME-COMPARISON DASHBOARD (the headline section). For BOTH the portfolio total AND each registry site, report visitors AND pageviews for each window below, each with the delta % vs its comparison window. Use these EXACT pre-computed ranges — do not compute your own:
   - Week over week (WoW):   this [${W_THIS_A} .. ${W_THIS_B}]  vs prior [${W_PREV_A} .. ${W_PREV_B}]
   - Month over month (MoM): this [${M_THIS_A} .. ${M_THIS_B}]  vs prior [${M_PREV_A} .. ${M_PREV_B}]  (same day-of-month range, apples to apples)
   - Year over year (YoY):   YTD [${Y_THIS_A} .. ${Y_THIS_B}]   vs prior-year same range [${Y_PREV_A} .. ${Y_PREV_B}]
   - Year-to-date TOTAL:     [${Y_THIS_A} .. ${Y_THIS_B}]
   - Trailing 12 months TOTAL: [${T12_A} .. ${T12_B}]
   Present as a clean table: rows = Portfolio + EVERY registry domain, columns = WoW %, MoM %, YoY %, YTD total, T12 total. Use ▲/▼ + the % for deltas.
   DATA-AVAILABILITY RULE: if a site has no history for a comparison window (Umami returns 0 for the prior period because tracking started later), do NOT print a fake or infinite delta — write 'n/a (tracking started <date>)' or 'new' instead. Be honest about which numbers are trustworthy.
2. TOP CONTENT & SOURCES: for each site, top 3 pages and top 3 referrers this week (${W_THIS_A} .. ${W_THIS_B}).
3. SYNDICATION UTM BREAKDOWN (startaitools only): use Umami's UTM report / utm_source filtering to show which of x / linkedin / substack / medium drove traffic this week (visits + WoW trend). This measures whether the team's posting is working. If a source shows zero, say so plainly.
4. EVERGREEN RE-SHARE NOMINATION: nominate exactly ONE older (>30 days) high-performing startaitools post for the team to re-share on X with a fresh angle. Give the live URL + a one-line 'fresh raw angle' suggestion Ezekiel can run with.
5. AMPLIFY THESE: 2-3 concrete asks for the team this week (which post to boost, which channel is underperforming and what to do).

LEDGER, AND WHAT IT IS NOT. The ledger at ${LEDGER_FILE} lists which posts had a packet SENT to Ezekiel. Its per-surface \`syndication\` statuses are NOT evidence of whether he posted, and you must not report them as if they were.

  * A reply-ingest path now exists, but missing replies are not proof of missing posts. Historically for five weeks every row read 'pending' and that meant 'nobody has ever told this file anything', not 'he did not post'. On 2026-08-11 a rollup read those as a 38-post backlog and told the whole team to clear it. That was an accusation manufactured out of a field with no writer. Do not repeat it.
  * Owner standing instruction (2026-08-11): ASSUME Ezekiel posted to X, LinkedIn, Substack and Medium every day unless Jeremy says otherwise. Aged rows now read 'assumed_posted', which records a belief and its provenance, not a receipt.
  * 'assumed_posted' means we believe it and cannot prove it. 'posted' would mean a real URL and timestamp exist. Only 'not_posted' means he actually missed one, and only Jeremy sets that.
  * NEVER write a section that counts unconfirmed rows as a backlog, a gap, or work owed. If you want to say something about posting volume, the honest sentence is that we have no confirmation path and distinguish actual destination receipts from assumptions; UTM measures arriving traffic.

Section 3 (UTM) is therefore the authoritative measure of whether syndication is working, because it counts actual arriving traffic rather than a self-reported flag. If a surface shows zero visits, report that as a REACH problem to diagnose, not as evidence that nobody posted.

Keep the whole thing skimmable for a busy team — this replaces a daily email, so it must earn the open. Do NOT email anything yourself; the wrapper emails the file. Write ONLY to ${OUTPUT_HTML}."

resolve_minimax_key() {
  if [ -n "${MINIMAX_API_KEY:-}" ]; then
    printf '%s' "$MINIMAX_API_KEY"
    return 0
  fi
  [ -r "$ROLLUP_MINIMAX_KEY_FILE" ] && [ -x "$ROLLUP_SOPS_BIN" ] || return 1
  "$ROLLUP_SOPS_BIN" -d --output-type json "$ROLLUP_MINIMAX_KEY_FILE" 2>/dev/null \
    | jq -er '.minimax.key | select(type == "string" and length > 0)' 2>/dev/null
}

if [ ! -x "$ROLLUP_AGENT_BIN" ]; then
  log "ERROR: rollup agent executable unavailable"
  STATUS="FAILED (agent unavailable)"
elif [ "$ROLLUP_PROVIDER" != minimax ] && [ "$ROLLUP_PROVIDER" != claude ]; then
  log "ERROR: invalid ROLLUP_PROVIDER"
  STATUS="FAILED (invalid provider)"
else
  STATUS=""
fi

MINIMAX_KEY=""
if [ -z "$STATUS" ] && [ "$ROLLUP_PROVIDER" = minimax ]; then
  MINIMAX_KEY=$(resolve_minimax_key) || MINIMAX_KEY=""
  if [ -z "$MINIMAX_KEY" ]; then
    log "ERROR: MiniMax credential unavailable; no interactive OAuth fallback in cron"
    STATUS="FAILED (provider credential unavailable)"
  fi
fi

log "Invoking ${ROLLUP_PROVIDER} for the rollup report (timeout ${TIMEOUT_SECS}s)..."
T0=$(date +%s)
if [ -z "$STATUS" ]; then
  AGENT_CMD="$ROLLUP_AGENT_BIN -p '$(printf '%s' "$PROMPT" | sed "s/'/'\\\\''/g")' --dangerously-skip-permissions"
  if [ "$ROLLUP_PROVIDER" = minimax ]; then
    if ANTHROPIC_BASE_URL="https://api.minimax.io/anthropic" \
       ANTHROPIC_API_KEY="$MINIMAX_KEY" ANTHROPIC_AUTH_TOKEN="" CLAUDE_CODE_OAUTH_TOKEN="" \
       ANTHROPIC_MODEL="$ROLLUP_MINIMAX_MODEL" ANTHROPIC_SMALL_FAST_MODEL="$ROLLUP_MINIMAX_MODEL" \
       /usr/bin/timeout "$TIMEOUT_SECS" script -e -q -a -c "$AGENT_CMD" "$LOG" >/dev/null 2>&1; then
      EXIT=0
    else EXIT=$?; fi
  elif /usr/bin/timeout "$TIMEOUT_SECS" script -e -q -a -c "$AGENT_CMD" "$LOG" >/dev/null 2>&1; then
    EXIT=0
  else EXIT=$?; fi
  WALL=$(( $(date +%s) - T0 ))
  if [ "$EXIT" -eq 0 ]; then
    log "${ROLLUP_PROVIDER} exited cleanly after ${WALL}s"
  else
    STATUS="FAILED (provider exit ${EXIT})"
    log "${ROLLUP_PROVIDER} exited non-zero ($EXIT) after ${WALL}s"
  fi
fi
MINIMAX_KEY=""

# Success gate: the report file must exist and be non-trivial.
if [ -z "$STATUS" ] && [ -s "$OUTPUT_HTML" ] && [ "$(wc -c < "$OUTPUT_HTML")" -gt 400 ] && \
   python3 "$REGISTRY_HELPER" --check-report "$OUTPUT_HTML" >> "$LOG" 2>&1; then
  STATUS="OK"
  if [ "${ROLLUP_DRY_RUN:-0}" = 1 ]; then
    cp -f "$OUTPUT_HTML" "$LOG_DIR/dryrun-${TODAY}.html"
    log "Dry run: valid HTML retained, no team email sent"
  else
  # Email to the team (comma list → repeatable --to).
  declare -a TO_ARGS=()
  IFS=',' read -ra _tos <<< "$TEAM_EMAILS"
  for t in "${_tos[@]}"; do t=$(echo "$t" | xargs); [ -n "$t" ] && TO_ARGS+=(--to "$t"); done
  if node "$EMAIL_SCRIPT" "${TO_ARGS[@]}" --subject "📊 Weekly growth rollup — week of ${TODAY}" --html "$OUTPUT_HTML" >> "$LOG" 2>&1; then
    log "Rollup emailed to team ($(( ${#TO_ARGS[@]} / 2 )) recipients)"
  else
    STATUS="FAILED (email send)"; log "ERROR: rollup email failed"
  fi
  fi
else
  STATUS="${STATUS:-FAILED (no report produced)}"
  log "ERROR: provider did not write a usable report to $OUTPUT_HTML"
fi

# Notifications.
CONSEC_FAILS=$(count_consecutive_failures "$LOG_DIR" "run-*.log" "FAILED|ABNORMAL" 8)
if [ "${ROLLUP_DRY_RUN:-0}" != 1 ]; then
  case "$STATUS" in FAILED*) cron_fail "blog-team-rollup" "${TODAY}: ${STATUS}. Log: $LOG" ;; esac
fi
# On failure, also email Jeremy the log tail (Buzz sys-automation already pinged above).
if [ "$STATUS" != "OK" ] && [ "${ROLLUP_DRY_RUN:-0}" != 1 ]; then
  # Capture the tail BEFORE the append redirect (SC2094: don't read+write $LOG in one pipeline).
  ROLLUP_TAIL=$(tail -40 "$LOG")
  node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io --subject "Weekly rollup FAILED: ${TODAY}" \
    --body "$(printf 'Status: %s\nConsecutive fails: %s\n\nLast 40 log lines:\n%s\n' "$STATUS" "$CONSEC_FAILS" "$ROLLUP_TAIL")" >> "$LOG" 2>&1 || true
fi

rm -f "$OUTPUT_HTML" 2>/dev/null || true
NOTIFIED=1
log "=== Weekly team rollup end (${STATUS}) ==="

# Exit truthfully for the liveness trap (review finding on PR #26): a handled
# failure must still exit non-zero so the EXIT trap withholds .ok and the estate
# sweep's running-but-failing signal stays live. NOTIFIED=1 above guarantees the
# trap does NOT double-alert.
case "$STATUS" in OK*) : ;; *) exit 1 ;; esac
