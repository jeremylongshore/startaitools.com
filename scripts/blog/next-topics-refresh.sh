#!/usr/bin/env bash
# next-topics-refresh.sh — refresh the analytics-driven topic queue (Thread D Phase 1).
#
# THE PERFORMANCE LOOP (front of funnel):
#   Umami content-performance  ->  content-seo agent (LLM)  ->  .next-topics.jsonl  ->  writers
#
# This wrapper mirrors web-analytics-daily.sh's operational spine (pty-wrapped
# headless agent, wall-clock ceiling, fail-loud alerting, liveness heartbeat) but
# is INDEPENDENT of the blog pipeline: no git, no staging-sentinel, no publish,
# no branch normalize. It only:
#   1. asks the content-seo agent to read real Umami traffic and PRODUCE ranked
#      next-topic candidates into .next-topics.staging.jsonl (LLM half), then
#   2. runs next-topics.py ingest (deterministic half) to validate, dedup, and
#      append them to .next-topics.jsonl. A bad model run cannot corrupt the queue.
#
# The queue is gitignored + transient. Writers (/blog-research-article, and
# /blog-backfill for angle inspiration) read the top open item via next-topics.py.
#
# Agent: NEXT_TOPICS_AGENT=claude|grok (default claude — it has the umami MCP
# get_content_performance tool; grok falls back to Umami REST like web-analytics).
#
# Tunables (env):
#   NEXT_TOPICS_TIMEOUT    hard ceiling seconds     (default 900)
#   NEXT_TOPICS_AGENT      claude | grok            (default claude)
#   NEXT_TOPICS_MAX_TURNS  max agent turns          (default 40)
#   NEXT_TOPICS_LOOKBACK   days of Umami history    (default 30)
#   NEXT_TOPICS_COUNT      candidates to propose    (default 5)

set -uo pipefail
export PATH="${HOME}/.local/bin:${HOME}/.bun/bin:${HOME}/bin:/usr/local/bin:/usr/bin:/bin:${PATH:-}"

LOG_DIR=/home/jeremy/.local/state/next-topics-refresh
mkdir -p "$LOG_DIR"
mkdir -p "$HOME/.local/state/intent-os/liveness" 2>/dev/null || true
: > "$HOME/.local/state/intent-os/liveness/next-topics-refresh.beat" 2>/dev/null || true

TODAY=$(date +%Y-%m-%d)
LOG="$LOG_DIR/run-${TODAY}.log"
BLOG_DIR=/home/jeremy/000-projects/blog/startaitools
STAGING="$BLOG_DIR/.next-topics.staging.jsonl"
# the live queue (.next-topics.jsonl) is written by next-topics.py, not this wrapper — no bash var needed
NT_PY="$BLOG_DIR/scripts/blog/next-topics.py"
EMAIL_SCRIPT=/home/jeremy/.claude/skills/email/scripts/send-email.cjs

TIMEOUT_SECS="${NEXT_TOPICS_TIMEOUT:-900}"
AGENT_NAME="${NEXT_TOPICS_AGENT:-claude}"
MAX_TURNS="${NEXT_TOPICS_MAX_TURNS:-40}"
LOOKBACK="${NEXT_TOPICS_LOOKBACK:-30}"
COUNT="${NEXT_TOPICS_COUNT:-5}"
GROK_BIN="${GROK_BIN:-$(command -v grok 2>/dev/null || true)}"
CLAUDE_BIN="${CLAUDE_BIN:-$(command -v claude 2>/dev/null || true)}"

# Umami site IDs from the content-seo site registry.
SITE_STARTAI="4071f4db-4249-4ce6-a929-665598975d67"
SITE_TONS="0cee47ed-bee5-48da-8fed-46b3d8a2ddd3"

# shellcheck source=./lib-cron-common.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib-cron-common.sh"
log() { echo "[$(date -Is)] $*" | tee -a "$LOG"; }
log "=== next-topics refresh start (${TODAY}, agent=${AGENT_NAME}, lookback=${LOOKBACK}d) ==="

NOTIFIED=0
# shellcheck disable=SC2317  # body reached only via `trap ... EXIT` (shellcheck can't see the dynamic call)
notify_unexpected_exit() {
  local rc=$?
  liveness_markers "next-topics-refresh" "$rc" 2>/dev/null || true
  [ "$rc" -eq 0 ] && return
  [ "$NOTIFIED" -eq 1 ] && return
  log "ABNORMAL EXIT (rc=$rc) — fail-loud alert"
  cron_fail "next-topics-refresh" "${TODAY}: exit rc=${rc} — topic queue not refreshed. Check ${LOG}" 2>/dev/null || true
  node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io \
    --subject "🚨 next-topics refresh failed: ${TODAY} (rc=${rc})" \
    --body "$(printf 'next-topics-refresh exited abnormally (rc=%s). Queue not refreshed.\n\nLast 30 log lines:\n%s\n' "$rc" "$(tail -30 "$LOG" 2>/dev/null)")" \
    >/dev/null 2>&1 || true
}
trap notify_unexpected_exit EXIT

START_DATE=$(date -d "${LOOKBACK} days ago" +%Y-%m-%d)
END_DATE="$TODAY"

# The producer instruction (LLM half). Deliberately narrow: read real traffic,
# emit ONLY staging JSONL, touch nothing else.
read -r -d '' RULES <<EOF || true
You are the content-seo agent for Intent Solutions. Framework: /home/jeremy/.claude/skills/web-analytics/agents/content-seo.md. Site registry: /home/jeremy/.claude/skills/web-analytics/references/site-registry.md.
TASK, two sweeps feeding one queue:

SWEEP 1 (performance): pull Umami content performance for startaitools.com (website_id ${SITE_STARTAI}) and tonsofskills.com (website_id ${SITE_TONS}) from ${START_DATE} to ${END_DATE}. Use the umami get_content_performance tool if available; otherwise Umami REST at https://analytics.intentsolutions.io with UMAMI_PASSWORD from ~/.env.

SWEEP 2 (trend x receipts): run 2-3 web searches for what is trending THIS WEEK in the AI-dev world this blog lives in (AI coding agents, Claude Code, agent skills, MCP, model releases, agent orchestration). Then read the first ~15 lines of /home/jeremy/000-projects/CROSS-SESSION-LOG.md and the 10 newest titles in /home/jeremy/000-projects/blog/startaitools/content/posts/ to see what Jeremy has ACTUALLY built recently. Propose up to 2 candidates that tie a live trend to work he has real receipts for: the trend supplies the search demand, the receipts supply the substance nobody else has. A trend candidate with no matching receipt is worthless; skip it rather than stretch. Mark these with "trend_hook" inside source_signals naming the trend and why this week. If web search is unavailable, skip sweep 2 silently and do sweep 1 alone.
Identify top performers, underperformers, content gaps, and topic clusters, grounded in the actual view/bounce numbers. Then propose the ${COUNT} highest-leverage NEXT blog topics for startaitools.com.

SCORING RUBRIC (derived from 90-day channel + UTM attribution on 2026-09-01 — apply it, do not restate it):
- The biggest real channel is ORGANIC SEARCH, and here Bing + DuckDuckGo out-refer Google ~3:1. The winners are SEARCHABLE, NAMED-TOOL, HOW-TO posts: "Fixing Claude Code Hooks: the New Matcher Format" (37 visitors), "Building a CAD-DXF Agent from Zero to v0.1.0" (45), a vision-language model guide (65). They name a specific tool, error, or version someone would type into a search box.
- The LOSERS on traffic are introspective / governance / meta / "what I learned today" posts — well-written but they only reach the small syndication audience and cluster at 10-17 visitors. The whole daily-syndication machine nets ~24 social clicks a quarter; one ranked how-to post out-pulls it alone.
- The LLM channel (ChatGPT, Perplexity, Kagi citing us) is small but growing — reward topics that answer a question cleanly enough to be quoted in an AI answer.
- THEREFORE: score HIGHER a topic whose title reads like a search query and names a concrete tool / error / framework / version, and that answers a "how do I X" a real person searches. Score LOWER a topic that is introspective, meta, or governance-flavored with no searchable named artifact — however substantive it is. The tier the post earns is separate; a Field Note that answers a googleable question outranks a Deep-Dive nobody searches for.

OUTPUT: write ONLY to ${STAGING}, one JSON object per line (JSONL), no prose, no markdown, no other files, no git. Each line:
{"topic":"short title","slug_hint":"kebab-slug","angle":"specific thesis","rationale":"why now, cite the traffic numbers","source_signals":{"top_performer":"slug (N views)","gap":"what is missing","cluster":"topic cluster"},"score":0.0-1.0,"target_tier":1-4}
score = priority (traffic evidence + strategic fit). target_tier 4 means it warrants /blog-research-article. Do NOT invent numbers; if Umami is unreachable, write an empty file and say so.
EOF

: > "$STAGING"  # start clean each run

AGENT_CMD=""
case "$AGENT_NAME" in
  grok)
    [ -x "$GROK_BIN" ] || { log "FATAL: grok not executable ($GROK_BIN)"; exit 1; }
    AGENT_CMD="$GROK_BIN -p '${RULES}' --always-approve --max-turns ${MAX_TURNS} --cwd '$BLOG_DIR'"
    ;;
  claude|*)
    [ -x "$CLAUDE_BIN" ] || { log "FATAL: claude not executable ($CLAUDE_BIN)"; exit 1; }
    AGENT_CMD="$CLAUDE_BIN -p '${RULES}' --dangerously-skip-permissions"
    ;;
esac

log "Invoking ${AGENT_NAME} producer (timeout ${TIMEOUT_SECS}s, pty-wrapped)"
T0=$(date +%s)
if /usr/bin/timeout "$TIMEOUT_SECS" script -e -q -a -c "$AGENT_CMD" "$LOG" >/dev/null 2>&1; then
  WALL=$(( $(date +%s) - T0 )); log "${AGENT_NAME} exited cleanly after ${WALL}s"
else
  EXIT=$?; WALL=$(( $(date +%s) - T0 ))
  if [ "$EXIT" = "124" ]; then log "${AGENT_NAME} TIMED OUT after ${WALL}s"; else log "${AGENT_NAME} exited ${EXIT} after ${WALL}s"; fi
  # not fatal on its own — ingest below handles an empty/partial staging file
fi

# Deterministic half: validate + dedup + append. This is what actually mutates
# the queue; the LLM only ever wrote to staging.
STAGED_LINES=$(grep -c . "$STAGING" 2>/dev/null || echo 0)
log "Staged candidates: ${STAGED_LINES}"
INGEST_OUT=$(python3 "$NT_PY" ingest 2>&1) || true
log "ingest: ${INGEST_OUT}"
VALIDATE_OUT=$(python3 "$NT_PY" validate 2>&1) || true
log "queue: ${VALIDATE_OUT}"

# Summary email (non-fatal). Shows what got added + the current top of queue.
TOP_OUT=$(python3 "$NT_PY" list 2>&1 | head -8)
node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io \
  --subject "Next-topics queue refreshed: ${TODAY} (${INGEST_OUT})" \
  --body "$(printf 'next-topics refresh for %s (agent=%s, %sd lookback).\n\n%s\n%s\n\nOpen queue (top):\n%s\n' "$TODAY" "$AGENT_NAME" "$LOOKBACK" "$INGEST_OUT" "$VALIDATE_OUT" "$TOP_OUT")" \
  >/dev/null 2>&1 || log "WARN: summary email failed"

NOTIFIED=1
log "=== next-topics refresh done ==="
exit 0
