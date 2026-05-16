#!/usr/bin/env bash
# sync-to-intentsolutions.sh — Copy a marketplace blog post to intentsolutions.io field-notes
# Adds canonical URL pointing to startaitools.com
#
# Usage:
#   ./sync-to-intentsolutions.sh <marketplace-post-path>
#   ./sync-to-intentsolutions.sh --batch   # Batch mode: re-sync all matching posts
#
# Professional tag filter (only posts with at least one of these tags are synced):
#   architecture, ai-agents, technical-leadership, vertex-ai, portfolio,
#   multi-agent-systems, cost-optimization, google-cloud, infrastructure-as-code,
#   cloud-architecture, ai-systems, infrastructure-automation, systems-architecture,
#   ai-engineering, data-architecture, enterprise-automation, case-study, agent-orchestration

set -euo pipefail

FIELD_NOTES_DIR="/home/jeremy/000-projects/intent-solutions-landing/astro-site/src/content/field-notes"
MARKETPLACE_DIR="/home/jeremy/000-projects/claude-code-plugins/marketplace/src/content/blog-posts"

PROFESSIONAL_TAGS="architecture|ai-agents|technical-leadership|vertex-ai|portfolio|multi-agent-systems|cost-optimization|google-cloud|infrastructure-as-code|cloud-architecture|ai-systems|infrastructure-automation|systems-architecture|ai-engineering|data-architecture|enterprise-automation|case-study|agent-orchestration"

has_professional_tag() {
  local file="$1"
  local tags_line
  tags_line=$(grep -m1 '^tags:' "$file" 2>/dev/null || echo "")
  if [[ -z "$tags_line" ]]; then
    return 1
  fi
  echo "$tags_line" | grep -qiE "$PROFESSIONAL_TAGS"
}

add_canonical() {
  local src="$1"
  local dst="$2"
  local slug
  slug=$(basename "$src" .md)
  local canonical="https://startaitools.com/posts/${slug}/"

  # Check if canonical already exists in frontmatter
  if grep -q '^canonical:' "$src" 2>/dev/null; then
    cp "$src" "$dst"
    return
  fi

  # Insert canonical before the closing --- of frontmatter
  awk -v canon="canonical: \"${canonical}\"" '
    BEGIN { count=0 }
    /^---$/ {
      count++
      if (count == 2) {
        print canon
      }
    }
    { print }
  ' "$src" > "$dst"
}

sync_single() {
  local src="$1"
  local fname
  fname=$(basename "$src")

  if ! has_professional_tag "$src"; then
    echo "SKIP (no professional tags): $fname"
    return 1
  fi

  mkdir -p "$FIELD_NOTES_DIR"
  add_canonical "$src" "$FIELD_NOTES_DIR/$fname"
  echo "SYNCED: $fname"
  return 0
}

# --- Main ---
if [[ "${1:-}" == "--batch" ]]; then
  echo "Batch sync: scanning $MARKETPLACE_DIR"
  count=0
  for f in "$MARKETPLACE_DIR"/*.md; do
    if sync_single "$f" 2>/dev/null; then
      ((count++))
    fi
  done
  echo "Synced $count posts to field-notes"
elif [[ -n "${1:-}" ]]; then
  sync_single "$1"
else
  echo "Usage: $0 <post-path> | --batch"
  exit 1
fi
