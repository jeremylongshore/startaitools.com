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
#   - a narration of the DETERMINISTIC referral-arrivals table that
#     weekly_metrics.py computes (Layer B contract, intent-os 226g section 10);
#     the model never queries, computes or zero-fills UTM numbers itself
#   - one evergreen re-share nomination (a proven older post to re-post fresh)
#   - "amplify these" asks for the week
#
# The LLM supplies structured qualitative suggestions; code binds all metric references
# and renders the HTML before this wrapper emails it to the team
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
# Owner status line in Buzz blog-ops (non-fatal by construction; see the library).
# shellcheck source=./lib-blog-ops-notify.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib-blog-ops-notify.sh"
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
OUTPUT_DRAFT=$(mktemp --suffix=.json)
METRIC_REFS=$(mktemp --suffix=.json)
NARRATIVE_RENDERER="$(dirname "${BASH_SOURCE[0]}")/rollup_narrative.py"
rm -f "$OUTPUT_HTML" "$OUTPUT_DRAFT"

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

# Materialize metrics and the numeric dashboard before asking for narrative.
# The model cannot choose date boundaries or replace the deterministic table.
METRICS_JSON=$(mktemp --suffix=.json)
DASHBOARD_HTML=$(mktemp --suffix=.html)
if ! /usr/bin/timeout 300 python3 "$ANALYTICS_SKILL_DIR/scripts/weekly_metrics.py" \
  --date "$TODAY" --json "$METRICS_JSON" --html "$DASHBOARD_HTML" >> "$LOG" 2>&1; then
  log "ERROR: deterministic estate metrics failed; refusing an incomplete report"
  exit 1
fi
# Contract preflight. The prompt below tells the model to narrate the filtered tier
# and referral table and never to compute them. If the installed skill predates that
# contract (claude-skills-private#23 not merged, or merged but ~/.claude/skills not
# pulled), those keys are absent and the model would have nothing true to say, so
# refuse: the EXIT trap alerts Jeremy and no team mail is sent.
if ! python3 - "$METRICS_JSON" >> "$LOG" 2>&1 <<'CONTRACT'
import json, sys
data = json.load(open(sys.argv[1]))
missing = []
if not (data.get('automation_rule') or {}).get('version'):
    missing.append('automation_rule')
sites = data.get('sites') or []
if not sites or any('filtered' not in row for row in sites):
    missing.append('sites[].filtered')
if not any(row.get('domain') == 'startaitools.com' and 'referrals' in row for row in sites):
    missing.append('sites[startaitools.com].referrals')
if missing:
    print('weekly_metrics contract missing: ' + ', '.join(missing))
    sys.exit(1)
CONTRACT
then
  log "ERROR: weekly_metrics.py output lacks the filtered-tier/referral contract (pull the web-analytics skill); refusing to send"
  exit 1
fi

# Report version + coverage + native panel header (startaitools-9a8.13.3). The
# header names the report version, metric dictionary version and filter, the
# week's unavailable fields, a one-time baseline-reset note, and the Dev.to
# native panel in its own units. It is deterministic; if it cannot be built the
# rollup still goes out with a minimal version line, never unversioned.
HEADER_SCRIPT="$(dirname "${BASH_SOURCE[0]}")/rollup-report-header.py"
DICTIONARY_FILE="${ROLLUP_METRIC_DICTIONARY:-$(dirname "${BASH_SOURCE[0]}")/metric-dictionary.json}"
NATIVE_LOG="${ROLLUP_NATIVE_LOG:-$BLOG_DIR/.native-metrics.jsonl}"
RESET_MARKER="$LOG_DIR/baseline-reset-communicated"
HEADER_HTML=$(mktemp --suffix=.html)
if ! python3 "$HEADER_SCRIPT" render --metrics "$METRICS_JSON" --date "$TODAY" --out "$HEADER_HTML" \
    --native "$NATIVE_LOG" --reset-marker "$RESET_MARKER" --dictionary "$DICTIONARY_FILE" >> "$LOG" 2>&1; then
  log "WARN: report header failed; sending a minimal version line instead (native panel unavailable)"
  printf '<p><b>Report version:</b> weekly growth rollup; metric dictionary %s; native platform panel unavailable this week.</p>\n' \
    "$(python3 "$(dirname "${BASH_SOURCE[0]}")/metric_dictionary.py" stamp --path "$DICTIONARY_FILE" 2>/dev/null || printf 'unavailable')" > "$HEADER_HTML"
fi
DICTIONARY_STAMP=$(python3 "$(dirname "${BASH_SOURCE[0]}")/metric_dictionary.py" stamp --path "$DICTIONARY_FILE" 2>/dev/null || printf 'unavailable')

# Only deterministic code supplies numeric statements and their measurement labels.
if ! python3 "$NARRATIVE_RENDERER" --metrics "$METRICS_JSON" --out "$METRIC_REFS" >> "$LOG" 2>&1; then
  log "ERROR: metric evidence catalog invalid; refusing to generate a report"
  exit 1
fi
# The agent may write its draft, but changing its read inputs must never change the report.
REPORT_INPUT_DIGEST=$(sha256sum "$METRICS_JSON" "$METRIC_REFS" "$DASHBOARD_HTML" "$HEADER_HTML") || exit 1

PROMPT="Report date: ${TODAY}. Write a WEEKLY GROWTH ROLLUP narrative as strict JSON (no markdown fences, no HTML) to ${OUTPUT_DRAFT} using the Write tool.
Read ${METRIC_REFS}: it maps allowed evidence keys to complete verified measurements. Read ${METRICS_JSON} for context, including sites[].referrals. The deterministic dashboard already contains every registry site and the complete numeric tables. Never create another totals table.

Required JSON object has exactly these fields:
- interpretation: array of one to three objects with text (plain qualitative explanation) and evidence (array of one to four exact keys from the evidence catalog).
- referrals: array of one to three objects with the same text/evidence shape, referring to referral evidence keys.
- evergreen: object with url (https://startaitools.com/posts/... without query or fragment) and angle (short plain text). Nominate exactly ONE older (>30 days) live post; confirm its publication date in the local content under ${BLOG_DIR}/content/posts or the live page. The title/URL may contain digits; only the URL is emitted, so keep the angle qualitative.
- actions: array of two or three objects with text/evidence, giving concrete amplification or measurement actions grounded in those references.

All text and angle strings must be plain, nonempty, at most a thousand characters, and contain NO numbers, number words, percentages, numeric comparisons or HTML. Do not quote traffic figures, dates, counts or article titles containing numbers in prose. Put metric references in evidence instead: the renderer inserts their value WITH their own population, period, tier and unit. Unknown keys and numeric prose refuse the email; the whole report does not silently fall back to the unsupported text.

The headline numbers are the FILTERED tier; raw is context. Never call a filtered figure the total audience or verified humans: removing suspected automation does not establish human identity. Describe observed differences without inventing causes or claiming that filtering proves why traffic changed. Metric definitions follow ${DICTIONARY_STAMP}. Sessions are not people, clicks are attempts not outcomes, and platform-native readers are outside Umami. Do not query Umami for traffic, UTM or referral numbers and do not compute your own. The same site registry drives both reports:
${ESTATE_SITES}

For referrals, 'unavailable' means the query failed: never treat it as zero. 'untagged — unmeasurable' means links carry no tags yet: never print a 0 for it or recommend action on its reach. Reference the existing evidence keys; never invent a zero or state what native-platform reach must be.

The ledger ${LEDGER_FILE} records packet delivery, not proof of publication. Missing replies do not prove missed posts. Rows marked assumed_posted have no destination receipt: report such rows only as unverified. Never count unconfirmed rows as a backlog or work owed. Only an authenticated destination URL and timestamp prove posting. Zero arrivals are not evidence that nobody posted.

Keep it short and useful for the content team. Do NOT email anything or change the ledger. Write ONLY to ${OUTPUT_DRAFT}."

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

invoke_rollup_agent() {
  local task="$1" remaining="$2" agent_cmd
  agent_cmd="$ROLLUP_AGENT_BIN -p '$(printf '%s' "$task" | sed "s/'/'\\\\''/g")' --dangerously-skip-permissions --tools Read,Glob,Grep,Write,WebFetch --strict-mcp-config --mcp-config '{\"mcpServers\":{}}'"
  if [ "$ROLLUP_PROVIDER" = minimax ]; then
    ANTHROPIC_BASE_URL="https://api.minimax.io/anthropic" \
      ANTHROPIC_API_KEY="$MINIMAX_KEY" ANTHROPIC_AUTH_TOKEN="" CLAUDE_CODE_OAUTH_TOKEN="" \
      ANTHROPIC_MODEL="$ROLLUP_MINIMAX_MODEL" ANTHROPIC_SMALL_FAST_MODEL="$ROLLUP_MINIMAX_MODEL" \
      /usr/bin/timeout "$remaining" script -e -q -a -c "$agent_cmd" "$LOG" >/dev/null 2>&1
  else
    /usr/bin/timeout "$remaining" script -e -q -a -c "$agent_cmd" "$LOG" >/dev/null 2>&1
  fi
}
render_narrative() {
  verify_report_inputs || { log "ERROR: report inputs changed during generation"; return 1; }
  python3 "$NARRATIVE_RENDERER" --metrics "$METRICS_JSON" --draft "$OUTPUT_DRAFT" \
    --out "$OUTPUT_HTML" >> "$LOG" 2>&1
}
verify_report_inputs() {
  local current
  current=$(sha256sum "$METRICS_JSON" "$METRIC_REFS" "$DASHBOARD_HTML" "$HEADER_HTML" 2>> "$LOG") || return 1
  [ "$current" = "$REPORT_INPUT_DIGEST" ]
}

log "Invoking ${ROLLUP_PROVIDER} for the rollup report (timeout ${TIMEOUT_SECS}s)..."
T0=$(date +%s)
if [ -z "$STATUS" ]; then
  if invoke_rollup_agent "$PROMPT" "$TIMEOUT_SECS"; then EXIT=0; else EXIT=$?; fi
  WALL=$(( $(date +%s) - T0 ))
  if [ "$EXIT" -eq 0 ]; then
    log "${ROLLUP_PROVIDER} exited cleanly after ${WALL}s"
  else
    STATUS="FAILED (provider exit ${EXIT})"
    log "${ROLLUP_PROVIDER} exited non-zero ($EXIT) after ${WALL}s"
  fi
fi

if [ -z "$STATUS" ] && ! verify_report_inputs; then
  STATUS="FAILED (metric input mutation)"
  log "ERROR: report inputs changed during generation; no repair or delivery"
fi

# One bounded repair may correct a draft; validation remains mandatory on every attempt.
# Both attempts share the original deadline. Never retry missing credentials or transport failures.
if [ -z "$STATUS" ] && ! render_narrative; then
  REJECTED="$LOG_DIR/rejected-${TODAY}-$(date +%s)-$$.json"
  if [ -s "$OUTPUT_DRAFT" ]; then cp -f "$OUTPUT_DRAFT" "$REJECTED"; fi
  REMAINING=$(( TIMEOUT_SECS - $(date +%s) + T0 ))
  log "Narrative refused; retained private draft at $REJECTED; one repair allowed inside deadline"
  REPAIR_PROMPT="$PROMPT
The previous draft failed validation. Read your existing draft, keep its supported meaning, and correct its schema and evidence keys. Remove EVERY numeric word from text/angle strings, including one, two, zero, half, percent, double. For example, say a surface instead of one surface. Keep all figures only in the evidence catalog references. Do not change the metric data or registry. Write the corrected JSON to the same draft path."
  if [ "$REMAINING" -le 0 ] || ! invoke_rollup_agent "$REPAIR_PROMPT" "$REMAINING" || ! render_narrative; then
    STATUS="FAILED (narrative contract)"
    log "ERROR: unsupported narrative or metric reference; no report will be sent"
  else
    log "Narrative repair passed the same metric contract"
  fi
fi
MINIMAX_KEY=""

# Prepend the immutable numeric dashboard; validated narrative follows it.
if [ -z "$STATUS" ] && [ -s "$OUTPUT_HTML" ]; then
  COMBINED_HTML=$(mktemp --suffix=.html)
  cat "$HEADER_HTML" "$DASHBOARD_HTML" "$OUTPUT_HTML" > "$COMBINED_HTML"
  mv -f "$COMBINED_HTML" "$OUTPUT_HTML"
fi

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
    # The baseline-reset note is one-time: record that a SENT rollup carried it.
    python3 "$HEADER_SCRIPT" mark-reset --reset-marker "$RESET_MARKER" --dictionary "$DICTIONARY_FILE" >> "$LOG" 2>&1 \
      || log "WARN: could not record the baseline-reset note as communicated; it will repeat next week"
    log "$(blog_ops_post "Weekly growth rollup for the week of ${TODAY} was emailed to the team; read it in your inbox (subject: Weekly growth rollup)." blog-team-rollup)"
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

rm -f "$OUTPUT_HTML" "$METRICS_JSON" "$DASHBOARD_HTML" "$HEADER_HTML" "$OUTPUT_DRAFT" "$METRIC_REFS" 2>/dev/null || true
NOTIFIED=1
log "=== Weekly team rollup end (${STATUS}) ==="

# Exit truthfully for the liveness trap (review finding on PR #26): a handled
# failure must still exit non-zero so the EXIT trap withholds .ok and the estate
# sweep's running-but-failing signal stays live. NOTIFIED=1 above guarantees the
# trap does NOT double-alert.
case "$STATUS" in OK*) : ;; *) exit 1 ;; esac
