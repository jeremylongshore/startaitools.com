#!/usr/bin/env bash
# Email social bundles (X thread + LinkedIn) for any recently-generated posts
# that haven't been emailed yet. Tracks state in a flat file.
# Runs from cron — silent on no-op, log on action.

set -uo pipefail

LOG=/home/jeremy/.local/state/blog-social-email/email.log
SENT=/home/jeremy/.local/state/blog-social-email/sent.txt
mkdir -p "$(dirname "$LOG")"
touch "$SENT"

X_DIR=/home/jeremy/000-projects/blog/x-threads
LI_DIR=/home/jeremy/000-projects/blog/linkedin-posts
POSTS_DIR=/home/jeremy/000-projects/blog/startaitools/content/posts
EMAIL_SCRIPT=/home/jeremy/.claude/skills/email/scripts/send-email.cjs

log() { echo "[$(date -Is)] $*" >> "$LOG"; }
log "=== Run start ==="

shopt -s nullglob
sent_count=0

for x_file in "$X_DIR"/*-backfill-x3.txt; do
  base=$(basename "$x_file" -backfill-x3.txt)
  date_part=$(echo "$base" | grep -oE '^[0-9]{4}-[0-9]{2}-[0-9]{2}')
  slug=${base#"${date_part}-"}

  # Already emailed?
  if grep -qxF "$slug" "$SENT" 2>/dev/null; then
    continue
  fi

  li_file="$LI_DIR/${date_part}-${slug}.txt"
  if [ ! -f "$li_file" ]; then
    log "  $slug: x-thread present but no LinkedIn file — skipping"
    continue
  fi

  # Pull title from Hugo post if present
  hugo_post="$POSTS_DIR/${slug}.md"
  title="$slug"
  if [ -f "$hugo_post" ]; then
    t=$(sed -n "s/^title = '\(.*\)'/\1/p" "$hugo_post" | head -1)
    [ -z "$t" ] && t=$(sed -n 's/^title = "\(.*\)"/\1/p' "$hugo_post" | head -1)
    [ -n "$t" ] && title="$t"
  fi

  body="Social bundle for: ${title}
Canonical: https://startaitools.com/posts/${slug}/

================================================================================
X THREAD (3 tweets)
================================================================================

$(cat "$x_file")

================================================================================
LINKEDIN POST
================================================================================

$(cat "$li_file")

================================================================================
ACTION ITEMS
================================================================================
[ ] Post X thread (paste into X.com or use /post-x)
[ ] Post LinkedIn (paste into LinkedIn personal or Intent Solutions company page)

Source files (if you want to edit before posting):
  X:  ${x_file}
  LI: ${li_file}
"

  subject="Social bundle ready: ${title}"

  if node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io --subject "$subject" --body "$body" >> "$LOG" 2>&1; then
    echo "$slug" >> "$SENT"
    sent_count=$((sent_count + 1))
    log "  $slug: SENT"

    # ntfy push (status only — full content in the email)
    NTFY_TOPIC=$(cat /home/jeremy/.ntfy-topic 2>/dev/null)
    if [ -n "$NTFY_TOPIC" ]; then
      curl -s -H "Title: Social bundle ready" -H "Priority: default" -H "Tags: bird,briefcase" \
        -d "${title}" \
        "https://ntfy.sh/$NTFY_TOPIC" >> "$LOG" 2>&1 || true
    fi
  else
    log "  $slug: SEND FAILED — will retry next run"
  fi
done

log "=== Run end. Bundles sent: $sent_count ==="
