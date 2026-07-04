#!/usr/bin/env bash
# Daily autonomous /blog-backfill. Runs at 7am via cron.
# - Idempotent: if yesterday's post already exists, exits clean (no-op).
# - Logs everything.
# - Emails a summary on completion (success or failure).

set -uo pipefail

LOG_DIR=/home/jeremy/.local/state/blog-backfill-daily
mkdir -p "$LOG_DIR"

YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
LOG="$LOG_DIR/run-${YESTERDAY}.log"
EMAIL_SCRIPT=/home/jeremy/.claude/skills/email/scripts/send-email.cjs
BLOG_DIR=/home/jeremy/000-projects/blog/startaitools
POSTS_DIR="$BLOG_DIR/content/posts"

# Shared helpers: preflight_branch_normalize, count_consecutive_failures.
# shellcheck source=./lib-cron-common.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib-cron-common.sh"

log() { echo "[$(date -Is)] $*" | tee -a "$LOG"; }
log "=== Daily blog-backfill start (target: $YESTERDAY) ==="

# --- Fail-loud guard: an early exit must never be silent (startaitools-74z) ---
# preflight_branch_normalize and the branch-switch logic can `exit 1` BEFORE the
# normal email/ntfy block at the end of this script. From 2026-06-15 the
# dirty-tree preflight aborted every run for 11 days with ZERO alerts. This trap
# fires on any non-zero exit that bypassed the normal notification and pushes a
# max-priority ntfy + email so a silent stall can't recur. Clean exits (rc=0,
# incl. the idempotency no-op below) and the normal notify path (NOTIFIED=1) are
# skipped.
NOTIFIED=0
notify_unexpected_exit() {
  local rc=$?
  [ "$rc" -eq 0 ] && return
  [ "$NOTIFIED" -eq 1 ] && return
  log "ABNORMAL EXIT (rc=$rc) before normal notification — sending fail-loud alert"
  local topic
  topic=$(cat /home/jeremy/.ntfy-topic 2>/dev/null)
  if [ -n "$topic" ]; then
    curl -s -H "Title: 🚨 blog-backfill aborted early" -H "Priority: max" -H "Tags: rotating_light" \
      -d "${YESTERDAY}: early exit rc=${rc} (likely dirty-tree preflight) — NO POST. Check ${LOG}" \
      "https://ntfy.sh/$topic" >/dev/null 2>&1 || true
  fi
  node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io \
    --subject "🚨 blog-backfill aborted early: ${YESTERDAY} (rc=${rc})" \
    --body "$(printf 'Daily blog-backfill exited abnormally (rc=%s) BEFORE its normal summary email.\nMost likely the dirty-tree preflight guard refused to run.\n\nNo post was generated for %s.\n\nLast 30 log lines:\n--------------------------------------------------------------------------------\n%s\n' "$rc" "$YESTERDAY" "$(tail -30 "$LOG" 2>/dev/null)")" \
    >/dev/null 2>&1 || true
}
trap notify_unexpected_exit EXIT

# Idempotency: skip if yesterday already has a post
if grep -rl "^date = '$YESTERDAY\|^date = \"$YESTERDAY\|^date: $YESTERDAY" "$POSTS_DIR" >/dev/null 2>&1; then
  log "Post already exists for $YESTERDAY — skipping (no-op)."
  exit 0
fi

# Run /blog-backfill headlessly. Hard wall-clock ceiling, overridable via env.
# Default is 1800s (30 min). Wrap claude -p in script(1) so node's CLI sees a
# pty on stdout and flushes incrementally — without this, all output buffers
# until SIGKILL, leaving the log opaque on timeout. The pty is the precondition
# for diagnosing wall-time creep (bead startaitools-6jf).
TIMEOUT_SECS="${BLOG_BACKFILL_TIMEOUT:-1800}"

# Pre-flight: clean working tree, switch to default branch (pivoting into a
# sibling worktree if the branch is held there), fast-forward. May mutate
# BLOG_DIR if pivoting. See scripts/blog/lib-cron-common.sh.
preflight_branch_normalize "$BLOG_DIR" "$LOG"

log "Invoking: claude -p /blog-backfill (timeout ${TIMEOUT_SECS}s, pty-wrapped)"
T0=$(date +%s)
# script(1) gives claude -p a pty so its CLI flushes incrementally instead of
# buffering until SIGKILL. -e propagates child exit status; -q suppresses the
# "Script started" framing; -a appends to "$LOG" (the typescript output file
# is script's trailing positional arg). The >/dev/null sink discards script's
# own stdout duplicate — the file copy is what we care about.
if /usr/bin/timeout "$TIMEOUT_SECS" script -e -q -a -c "claude -p '/blog-backfill' --dangerously-skip-permissions" "$LOG" >/dev/null 2>&1; then
  STATUS="OK"
  WALL=$(( $(date +%s) - T0 ))
  log "claude -p exited cleanly after ${WALL}s ($((WALL/60))m $((WALL%60))s)"
else
  EXIT=$?
  WALL=$(( $(date +%s) - T0 ))
  STATUS="FAILED (exit $EXIT)"
  if [ "$EXIT" = "124" ]; then
    log "claude -p TIMED OUT after ${WALL}s (hard ceiling ${TIMEOUT_SECS}s)"
  else
    log "claude -p exited non-zero (exit $EXIT) after ${WALL}s"
  fi
fi

# Identify what got produced
NEW_POST=$(grep -rl "^date = '$YESTERDAY\|^date = \"$YESTERDAY\|^date = $YESTERDAY\|^date: $YESTERDAY" "$POSTS_DIR" 2>/dev/null | head -1)
NEW_POST_BASENAME=$(basename "${NEW_POST:-none}" .md)

# ----- Post-flight: reconcile branch drift -----
# /blog-backfill defensively commits to a feature branch when master has unrelated
# in-progress changes. That's correct for safety, but blogs then never reach the
# live site. Try a fast-forward push of the current branch tip to the default
# branch — succeeds when the feature branch is just default+commits and there
# are no conflicting commits on origin. Falls back to a loud warning otherwise.
RECONCILED=""
reconcile_repo() {
  local repo="$1"
  local label="$2"
  [ -d "$repo/.git" ] || return 0
  cd "$repo" || return 1
  local current default sha
  current=$(git rev-parse --abbrev-ref HEAD 2>/dev/null) || return 1
  default=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
  default="${default:-master}"
  if [ "$current" = "$default" ]; then
    RECONCILED="${RECONCILED}${label}: on $default ✓\n"
    return 0
  fi
  # Only act if there's actually something to push
  if [ -z "$(git log "origin/$default..$current" --oneline 2>/dev/null)" ]; then
    RECONCILED="${RECONCILED}${label}: $current has no commits ahead of origin/$default ✓\n"
    return 0
  fi
  if git push origin "$current:$default" >> "$LOG" 2>&1; then
    sha=$(git rev-parse --short HEAD)
    log "✓ FF-pushed $label: $current → origin/$default ($sha)"
    RECONCILED="${RECONCILED}${label}: ✓ auto-merged $current → origin/$default ($sha)\n"
  else
    log "✗ FF-push failed for $label ($current → origin/$default) — manual merge required"
    RECONCILED="${RECONCILED}${label}: ⚠ ORPHANED on $current — needs manual merge\n"
  fi
}
# ----- Methodology bookkeeping gate (added 2026-05-16, hoisted 2026-05-28) -----
# /blog-backfill is required by SKILL.md to write a classifier record (step 3)
# and an agent_audit addendum (step 8) to decisions.jsonl for each post.
# This check runs BEFORE reconcile_repo: a half-state (post on disk, no
# methodology record) signals an aborted/timed-out run; we don't want to
# ff-push such a state to master. The reconcile gate below requires strict
# STATUS=OK, so missing bookkeeping suppresses the push and surfaces a warning.
DECISIONS=/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/methodology/decisions.jsonl
if [ "$STATUS" = "OK" ] && [ -n "${NEW_POST_BASENAME:-}" ] && [ "$NEW_POST_BASENAME" != "none" ]; then
  if ! /usr/bin/grep -q "\"date\"[[:space:]]*:[[:space:]]*\"$YESTERDAY\"" "$DECISIONS"; then
    log "WARN: no decisions.jsonl record for $YESTERDAY — classifier step 3 was skipped"
    STATUS="OK-WITH-WARNING (missing classifier record)"
  elif ! /usr/bin/grep "\"slug\"[[:space:]]*:[[:space:]]*\"$NEW_POST_BASENAME\"" "$DECISIONS" | /usr/bin/grep -q 'audit_addendum'; then
    log "WARN: no agent_audit addendum for $NEW_POST_BASENAME — step 8 was skipped"
    STATUS="OK-WITH-WARNING (missing audit addendum)"
  fi
fi

if [ "$STATUS" = "OK" ]; then
  reconcile_repo "$BLOG_DIR" "startaitools"
  reconcile_repo "/home/jeremy/000-projects/claude-code-plugins" "tonsofskills"
else
  log "Skipping branch reconciliation — STATUS is '$STATUS' (not strict OK)"
  RECONCILED="(skipped — STATUS=$STATUS)\n"
fi

# ----- Methodology index rebuild (mandated by SKILL.md line 173) -----
REBUILD=/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/scripts/rebuild-methodology-index.sh
if [ -x "$REBUILD" ]; then
  log "Rebuilding methodology index..."
  "$REBUILD" >> "$LOG" 2>&1 || log "WARN: methodology index rebuild failed"
fi

# Consecutive-failure escalation: if N≥3 days of FATAL/TIMED OUT/FAILED in a
# row, prefix the email subject and elevate the ntfy priority. Catches the
# "8 days of silent FATAL nobody noticed" mode that triggered 2026-06-05.
# Counts only AFTER recording today's result by writing the marker first.
CONSEC_FAILS=$(count_consecutive_failures "$LOG_DIR" "run-*.log" "FATAL|TIMED OUT|FAILED \(exit" 10)
ESCALATE_PREFIX=""
ESCALATE_PRIORITY="default"
if [ "$CONSEC_FAILS" -ge 3 ]; then
  log "ESCALATION: ${CONSEC_FAILS} consecutive failed runs detected — elevating alert priority"
  ESCALATE_PREFIX="🚨 ${CONSEC_FAILS}-DAY STREAK: "
  ESCALATE_PRIORITY="max"
fi

# Slack #cron-failures on a hard failure only (dormant until SLACK_WEBHOOK_CRON
# is set in ~/.env). OK / OK-WITH-WARNING stay on email + ntfy — Slack is
# failures-only. See scripts/blog/lib-cron-common.sh § slack_fail.
case "$STATUS" in
  FAILED*) slack_fail "blog-backfill-daily" "${ESCALATE_PREFIX}${YESTERDAY}: ${STATUS} (${CONSEC_FAILS}-day streak). Log: $LOG" ;;
esac

# Build summary
TAIL=$(tail -50 "$LOG")
BODY="Daily /blog-backfill run for ${YESTERDAY}
Status: ${STATUS}
Consecutive failures (incl. this run): ${CONSEC_FAILS}
New post: ${NEW_POST_BASENAME}
Branch reconciliation:
$(printf "%b" "${RECONCILED:-(skipped — run failed)}")

================================================================================
Last 50 log lines (full log: ${LOG}):
================================================================================

${TAIL}
"

SUBJECT="${ESCALATE_PREFIX}Daily blog-backfill: ${YESTERDAY} — ${STATUS}"

node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io --subject "$SUBJECT" --body "$BODY" >> "$LOG" 2>&1 \
  || log "Email send failed — see log"

# ntfy push notification (status only — content stays in the email)
NTFY_TOPIC=$(cat /home/jeremy/.ntfy-topic 2>/dev/null)
if [ -n "$NTFY_TOPIC" ]; then
  case "$STATUS" in
    OK)
      curl -s -H "Title: Daily blog-backfill OK" -H "Priority: default" -H "Tags: white_check_mark" \
        -d "${YESTERDAY}: ${NEW_POST_BASENAME:-no post (no activity)}" \
        "https://ntfy.sh/$NTFY_TOPIC" >> "$LOG" 2>&1 || true
      ;;
    OK-WITH-WARNING*)
      curl -s -H "Title: Daily blog-backfill OK (with warning)" -H "Priority: default" -H "Tags: warning" \
        -d "${YESTERDAY}: ${STATUS}" \
        "https://ntfy.sh/$NTFY_TOPIC" >> "$LOG" 2>&1 || true
      ;;
    *)
      # If escalation fired, use max priority; otherwise high.
      _ntfy_prio="high"
      [ "$ESCALATE_PRIORITY" = "max" ] && _ntfy_prio="max"
      curl -s -H "Title: ${ESCALATE_PREFIX}Daily blog-backfill FAILED" -H "Priority: ${_ntfy_prio}" -H "Tags: rotating_light" \
        -d "${YESTERDAY}: ${STATUS} (${CONSEC_FAILS}-day streak). Check log at $LOG" \
        "https://ntfy.sh/$NTFY_TOPIC" >> "$LOG" 2>&1 || true
      ;;
  esac
fi

# Normal notification path completed — disarm the fail-loud trap.
NOTIFIED=1

log "=== Daily blog-backfill end ==="
