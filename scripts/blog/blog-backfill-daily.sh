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

# Run /blog-backfill headlessly. Hard wall-clock ceiling, overridable via env.
# Default is 1800s (30 min). Wrap claude -p in script(1) so node's CLI sees a
# pty on stdout and flushes incrementally — without this, all output buffers
# until SIGKILL, leaving the log opaque on timeout. The pty is the precondition
# for diagnosing wall-time creep (bead startaitools-6jf).
TIMEOUT_SECS="${BLOG_BACKFILL_TIMEOUT:-1800}"
cd "$BLOG_DIR" || { log "FATAL: cd to $BLOG_DIR failed"; exit 1; }

# ----- Pre-flight branch normalization -----
# Telemetry from the 2026-05-28 07:00 run showed the AI spent ~3m 30s on a
# git-worktree dance because the working tree was on a feat branch when cron
# fired. The skill detoured through /tmp/startaitools-master to commit the
# blog to master without entangling the open PR. Cheaper fix: cron should
# never invoke /blog-backfill from a non-default branch in the first place.
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
DEFAULT_BRANCH="${DEFAULT_BRANCH:-master}"
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
if [ "$CURRENT_BRANCH" != "$DEFAULT_BRANCH" ]; then
  log "Pre-flight: working tree on '$CURRENT_BRANCH', not '$DEFAULT_BRANCH'"
  # Only switch if the working tree is fully clean — any uncommitted change
  # could be in-flight work the engineer left mid-stream; we'd rather abort
  # loudly than risk losing it.
  if [ -n "$(git status --porcelain --untracked-files=no 2>/dev/null)" ]; then
    log "FATAL: working tree has uncommitted changes on '$CURRENT_BRANCH' — refusing to switch"
    log "       Resolve manually (commit, stash, or restore) and re-run; cron will retry tomorrow."
    exit 1
  fi
  log "Pre-flight: working tree clean, switching to '$DEFAULT_BRANCH' and fast-forwarding"
  if ! git checkout "$DEFAULT_BRANCH" >> "$LOG" 2>&1; then
    log "FATAL: git checkout $DEFAULT_BRANCH failed"
    exit 1
  fi
  if ! git pull --ff-only origin "$DEFAULT_BRANCH" >> "$LOG" 2>&1; then
    log "WARN: git pull --ff-only failed — continuing with stale local $DEFAULT_BRANCH"
  fi
fi
log "Pre-flight OK: on $(git rev-parse --abbrev-ref HEAD) @ $(git rev-parse --short HEAD)"
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
  elif ! /usr/bin/grep -q "\"slug\"[[:space:]]*:[[:space:]]*\"$NEW_POST_BASENAME\".*audit_addendum" "$DECISIONS"; then
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
