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

log() { echo "[$(date -Is)] $*" | tee -a "$LOG"; }
log "=== Daily blog-backfill start (target: $YESTERDAY) ==="

# Idempotency: skip if yesterday already has a post
if grep -rl "^date = '$YESTERDAY\|^date = \"$YESTERDAY\|^date: $YESTERDAY" "$POSTS_DIR" >/dev/null 2>&1; then
  log "Post already exists for $YESTERDAY — skipping (no-op)."
  exit 0
fi

# Run /blog-backfill headlessly. 30-min hard timeout.
cd "$BLOG_DIR"
log "Invoking: claude -p /blog-backfill"
if /usr/bin/timeout 1800 claude -p "/blog-backfill" --dangerously-skip-permissions >> "$LOG" 2>&1; then
  STATUS="OK"
  log "claude -p exited cleanly"
else
  STATUS="FAILED (exit $?)"
  log "claude -p exited non-zero"
fi

# Identify what got produced
NEW_POST=$(grep -rl "^date = '$YESTERDAY\|^date = \"$YESTERDAY\|^date: $YESTERDAY" "$POSTS_DIR" 2>/dev/null | head -1)
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
if [ "$STATUS" = "OK" ]; then
  reconcile_repo "$BLOG_DIR" "startaitools"
  reconcile_repo "/home/jeremy/000-projects/claude-code-plugins" "tonsofskills"
fi

# ----- Methodology bookkeeping gate (added 2026-05-16) -----
# /blog-backfill is required by SKILL.md to write a classifier record (step 3)
# and an agent_audit addendum (step 8) to decisions.jsonl for each post.
# Multiple May 2026 runs skipped one or both. Treat missing bookkeeping as a
# soft failure: STATUS gets a "WITH-WARNING" suffix so the email + ntfy surface it.
DECISIONS=/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/methodology/decisions.jsonl
if [ "$STATUS" = "OK" ] && [ -n "${NEW_POST_BASENAME:-}" ] && [ "$NEW_POST_BASENAME" != "none" ]; then
  if ! /usr/bin/grep -q "\"date\"[[:space:]]*:[[:space:]]*\"$YESTERDAY\"" "$DECISIONS"; then
    log "WARN: no decisions.jsonl record for $YESTERDAY — classifier step 3 was skipped"
    STATUS="OK-WITH-WARNING (missing classifier record)"
  elif ! /usr/bin/grep -q "\"slug\"[[:space:]]*:[[:space:]]*\"$NEW_POST_BASENAME\".*audit_addendum" "$DECISIONS"; then
    log "WARN: no agent_audit addendum for $NEW_POST_BASENAME — step 8 was skipped"
    STATUS="OK-WITH-WARNING (missing audit addendum)"
  fi
fi

# ----- Methodology index rebuild (mandated by SKILL.md line 173) -----
REBUILD=/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/scripts/rebuild-methodology-index.sh
if [ -x "$REBUILD" ]; then
  log "Rebuilding methodology index..."
  "$REBUILD" >> "$LOG" 2>&1 || log "WARN: methodology index rebuild failed"
fi

# Build summary
TAIL=$(tail -50 "$LOG")
BODY="Daily /blog-backfill run for ${YESTERDAY}
Status: ${STATUS}
New post: ${NEW_POST_BASENAME}
Branch reconciliation:
$(printf "%b" "${RECONCILED:-(skipped — run failed)}")

================================================================================
Last 50 log lines (full log: ${LOG}):
================================================================================

${TAIL}
"

SUBJECT="Daily blog-backfill: ${YESTERDAY} — ${STATUS}"

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
      curl -s -H "Title: Daily blog-backfill FAILED" -H "Priority: high" -H "Tags: rotating_light" \
        -d "${YESTERDAY}: ${STATUS}. Check log at $LOG" \
        "https://ntfy.sh/$NTFY_TOPIC" >> "$LOG" 2>&1 || true
      ;;
  esac
fi

log "=== Daily blog-backfill end ==="
