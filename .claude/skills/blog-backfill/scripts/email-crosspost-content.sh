#!/usr/bin/env bash
# email-crosspost-content.sh — Email Substack + X thread content for manual posting
#
# Usage: ./email-crosspost-content.sh <slug> <drafts-dir>
#
# Reads platform-adapted files from the drafts directory and sends a single email
# with Substack version + X thread formatted for copy-paste.
# Falls back to printing file paths if email send fails.

set -euo pipefail

slug="${1:?Usage: $0 <slug> <drafts-dir>}"
drafts_dir="${2:?Usage: $0 <slug> <drafts-dir>}"

EMAIL_SCRIPT="/home/jeremy/.claude/skills/email/scripts/send-email.cjs"
BLOG_DIR="/home/jeremy/000-projects/blog/startaitools"

# Load env
if [[ -f "${BLOG_DIR}/.env" ]]; then
  set -a
  source "${BLOG_DIR}/.env"
  set +a
fi

# Load from intent-mail .env for GMAIL creds
if [[ -f "/home/jeremy/000-projects/intent-mail/.env" ]]; then
  set -a
  source "/home/jeremy/000-projects/intent-mail/.env"
  set +a
fi

platforms_dir="${drafts_dir}/07-platforms"

# Read platform files
substack_file="${platforms_dir}/substack.md"
xthread_file="${platforms_dir}/x-thread.md"

if [[ ! -f "$substack_file" ]] && [[ ! -f "$xthread_file" ]]; then
  echo "ERROR: No platform files found in $platforms_dir" >&2
  exit 1
fi

substack_content="(No Substack version generated)"
if [[ -f "$substack_file" ]]; then
  substack_content=$(cat "$substack_file")
fi

xthread_content="(No X thread generated)"
if [[ -f "$xthread_file" ]]; then
  xthread_content=$(cat "$xthread_file")
fi

# Read title from Hugo post or final draft
title="$slug"
hugo_file="${BLOG_DIR}/content/posts/${slug}.md"
final_file="${drafts_dir}/06-final.md"

if [[ -f "$hugo_file" ]]; then
  title=$(sed -n "s/^title = '\(.*\)'/\1/p" "$hugo_file" | head -1)
  [[ -z "$title" ]] && title=$(sed -n 's/^title = "\(.*\)"/\1/p' "$hugo_file" | head -1)
elif [[ -f "$final_file" ]]; then
  title=$(sed -n "s/^title = '\(.*\)'/\1/p" "$final_file" | head -1)
  [[ -z "$title" ]] && title=$(sed -n 's/^title = "\(.*\)"/\1/p' "$final_file" | head -1)
fi
[[ -z "$title" ]] && title="$slug"

# Determine schedule from queue
schedule_info="Check .crosspost-queue.json for schedule"
queue_file="${BLOG_DIR}/.crosspost-queue.json"
if [[ -f "$queue_file" ]]; then
  entry=$(jq -r ".[] | select(.slug == \"$slug\")" "$queue_file" 2>/dev/null || echo "")
  if [[ -n "$entry" ]]; then
    devto_after=$(echo "$entry" | jq -r '.devto.publish_after // "not scheduled"')
    hashnode_after=$(echo "$entry" | jq -r '.hashnode.publish_after // "not scheduled"')
    medium_after=$(echo "$entry" | jq -r '.medium.publish_after // "not scheduled"')
    schedule_info="Dev.to: ${devto_after}
Hashnode: ${hashnode_after}
Medium: ${medium_after}"
  fi
fi

# Build email body
email_body="SUBSTACK VERSION
================
(Copy-paste into Substack editor)

${substack_content}

---

X THREAD
========
(Copy-paste or use /post-x)

${xthread_content}

---

AUTO-PUBLISH SCHEDULE
=====================
${schedule_info}

These will be published automatically when you next run /blog-backfill
or when check-crosspost-queue.sh runs.

MANUAL ACTION NEEDED
====================
- [ ] Paste Substack version into Substack editor
- [ ] Post X thread (use /post-x or paste manually)

Canonical URL: https://startaitools.com/posts/${slug}/"

# Save to temp file (fallback if email fails)
tmp_file="/tmp/crosspost-email-${slug}.txt"
echo "$email_body" > "$tmp_file"

# Try to send email
subject="Cross-post ready: ${title}"

if [[ -x "$EMAIL_SCRIPT" ]] || [[ -f "$EMAIL_SCRIPT" ]]; then
  echo "Sending cross-post email: $subject" >&2
  if node "$EMAIL_SCRIPT" \
    --to "jeremy@intentsolutions.io" \
    --subject "$subject" \
    --body "$email_body" 2>&1; then
    echo "Email sent successfully." >&2
    rm -f "$tmp_file"
  else
    echo "Email send failed. Content saved to: $tmp_file" >&2
  fi
else
  echo "Email script not found at $EMAIL_SCRIPT" >&2
  echo "Content saved to: $tmp_file" >&2
fi
