#!/usr/bin/env bash
# post-to-substack.sh — Prepare a ready-to-paste markdown draft for Substack
#
# Usage: ./post-to-substack.sh <post.md> [--draft]
#
# Requires: SUBSTACK_OUTPUT_DIR environment variable (path to output directory)
# Substack has no public API — this generates a formatted file for manual copy-paste.
# Adds canonical attribution footer pointing to startaitools.com.

set -euo pipefail

if [[ -z "${SUBSTACK_OUTPUT_DIR:-}" ]]; then
  echo "SKIP: SUBSTACK_OUTPUT_DIR not set, skipping Substack draft preparation" >&2
  exit 0
fi

input="${1:?Usage: $0 <post.md> [--draft]}"
# --draft flag accepted for interface consistency but has no effect (all output is a draft file)

# Parse Astro YAML frontmatter
title=$(sed -n 's/^title: *"\(.*\)" *$/\1/p' "$input" | head -1)
description=$(sed -n 's/^description: *"\(.*\)" *$/\1/p' "$input" | head -1)
tags_raw=$(sed -n 's/^tags: *\[\(.*\)\] *$/\1/p' "$input" | head -1)
tags=$(echo "$tags_raw" | tr ',' '\n' | sed 's/^ *"//;s/" *$//' | paste -sd ', ' -)

slug=$(basename "$input" .md)
canonical_url="${CANONICAL_OVERRIDE:-https://startaitools.com/posts/${slug}/}"

# Extract body (everything after second ---)
body=$(awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$input")

# Strip Hugo/Astro shortcodes ({{< ... >}} and {{% ... %}})
clean_body=$(echo "$body" | sed 's/{{[<%] *[^}]* *[>%]}}//g')

# Ensure output directory exists
mkdir -p "$SUBSTACK_OUTPUT_DIR"

output_file="${SUBSTACK_OUTPUT_DIR}/${slug}.md"

# Derive footer link text from canonical URL hostname so cron-default
# (startaitools.com) and CANONICAL_OVERRIDE cases (e.g. kobiton.com) both
# show accurate attribution.
canonical_host=$(echo "$canonical_url" | awk -F[/:] '{print $4}')

# Write ready-to-paste markdown
cat > "$output_file" <<EOF
# ${title}

${clean_body}

---

*Originally published at [${canonical_host}](${canonical_url})*

<!-- Suggested tags: ${tags} -->
<!-- Subtitle suggestion: ${description} -->
EOF

echo "Substack draft prepared: $title" >&2
echo "  Output: $output_file" >&2
echo "  Canonical: $canonical_url" >&2
echo "$output_file"
