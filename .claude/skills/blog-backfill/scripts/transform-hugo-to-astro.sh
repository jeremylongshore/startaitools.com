#!/usr/bin/env bash
# transform-hugo-to-astro.sh — Convert Hugo frontmatter (TOML or YAML) to Astro YAML
#
# Usage:
#   ./transform-hugo-to-astro.sh <input.md> [output.md]
#   ./transform-hugo-to-astro.sh --batch <input-dir> <output-dir>
#
# Handles both TOML (+++) and YAML (---) Hugo frontmatter.
# Drops: categories, slug, draft, author, series, featured_image
# Adds: featured: false (if not present)
# Normalizes date to YYYY-MM-DD string

set -euo pipefail

transform_single() {
  local input="$1"
  local output="${2:-/dev/stdout}"

  # Detect frontmatter type by first line
  local first_line
  first_line=$(head -1 "$input")

  local title="" date="" description="" tags="" featured="false" body=""

  if [[ "$first_line" == "+++" ]]; then
    # TOML frontmatter
    local in_frontmatter=true
    local frontmatter=""
    local line_num=0

    while IFS= read -r line; do
      line_num=$((line_num + 1))
      if [[ $line_num -eq 1 ]]; then
        continue  # skip opening +++
      fi
      if [[ "$line" == "+++" ]] && [[ $line_num -gt 1 ]]; then
        in_frontmatter=false
        continue
      fi
      if $in_frontmatter; then
        frontmatter+="$line"$'\n'
      else
        body+="$line"$'\n'
      fi
    done < "$input"

    # Parse TOML fields
    title=$(echo "$frontmatter" | sed -n "s/^title *= *['\"]\\(.*\\)['\"] *$/\\1/p" | head -1)
    # Date: strip quotes first, then extract YYYY-MM-DD
    local raw_date
    raw_date=$(echo "$frontmatter" | sed -n "s/^date *= *\\(.*\\) *$/\\1/p" | head -1)
    raw_date="${raw_date//\"/}"  # strip all double quotes
    raw_date="${raw_date//\'/}"  # strip all single quotes
    date=$(echo "$raw_date" | grep -oP '\d{4}-\d{2}-\d{2}' || echo "$raw_date")
    description=$(echo "$frontmatter" | sed -n "s/^description *= *['\"]\\(.*\\)['\"] *$/\\1/p" | head -1)
    # Tags: extract the array content
    tags=$(echo "$frontmatter" | sed -n 's/^tags *= *\[\(.*\)\] *$/\1/p' | head -1)
    # Check for featured field
    local feat_val
    feat_val=$(echo "$frontmatter" | sed -n 's/^featured *= *\(.*\) *$/\1/p' | head -1)
    if [[ -n "$feat_val" ]]; then
      featured="$feat_val"
    fi

  elif [[ "$first_line" == "---" ]]; then
    # YAML frontmatter
    local in_frontmatter=true
    local frontmatter=""
    local line_num=0

    while IFS= read -r line; do
      line_num=$((line_num + 1))
      if [[ $line_num -eq 1 ]]; then
        continue  # skip opening ---
      fi
      if [[ "$line" == "---" ]] && [[ $line_num -gt 1 ]]; then
        in_frontmatter=false
        continue
      fi
      if $in_frontmatter; then
        frontmatter+="$line"$'\n'
      else
        body+="$line"$'\n'
      fi
    done < "$input"

    # Parse YAML fields
    title=$(echo "$frontmatter" | sed -n 's/^title: *"\(.*\)" *$/\1/p' | head -1)
    if [[ -z "$title" ]]; then
      title=$(echo "$frontmatter" | sed -n "s/^title: *'\\(.*\\)' *$/\\1/p" | head -1)
    fi
    if [[ -z "$title" ]]; then
      title=$(echo "$frontmatter" | sed -n 's/^title: *\(.*\) *$/\1/p' | head -1)
    fi
    local raw_date
    raw_date=$(echo "$frontmatter" | sed -n 's/^date: *\(.*\) *$/\1/p' | head -1)
    raw_date="${raw_date//\"/}"  # strip all double quotes
    raw_date="${raw_date//\'/}"  # strip all single quotes
    date=$(echo "$raw_date" | grep -oP '\d{4}-\d{2}-\d{2}' || echo "$raw_date")
    description=$(echo "$frontmatter" | sed -n 's/^description: *"\(.*\)" *$/\1/p' | head -1)
    if [[ -z "$description" ]]; then
      description=$(echo "$frontmatter" | sed -n "s/^description: *'\\(.*\\)' *$/\\1/p" | head -1)
    fi
    tags=$(echo "$frontmatter" | sed -n 's/^tags: *\[\(.*\)\] *$/\1/p' | head -1)
    local feat_val
    feat_val=$(echo "$frontmatter" | sed -n 's/^featured: *\(.*\) *$/\1/p' | head -1)
    if [[ -n "$feat_val" ]]; then
      featured="$feat_val"
    fi
  else
    echo "ERROR: Unknown frontmatter format in $input (first line: $first_line)" >&2
    return 1
  fi

  # Fallback: use title as description if empty
  if [[ -z "$description" ]]; then
    description="$title"
  fi

  # Normalize tags: strip quotes, rebuild as YAML array
  # Input could be: "AI Development", "Hugo", 'stuff' or unquoted
  local normalized_tags=""
  if [[ -n "$tags" ]]; then
    # Remove surrounding quotes from each tag, lowercase
    normalized_tags=$(echo "$tags" | tr ',' '\n' | sed 's/^ *//;s/ *$//;s/^["'"'"']//;s/["'"'"']$//' | \
      awk '{print tolower($0)}' | sed 's/ /-/g' | \
      awk 'NF{printf "\"%s\", ", $0}' | sed 's/, $//')
    normalized_tags="[$normalized_tags]"
  else
    normalized_tags="[]"
  fi

  # Escape double quotes in title and description for YAML output
  local safe_title="${title//\"/\\\"}"
  local safe_desc="${description//\"/\\\"}"

  # Write Astro YAML frontmatter
  {
    echo "---"
    echo "title: \"$safe_title\""
    echo "description: \"$safe_desc\""
    echo "date: \"$date\""
    echo "tags: $normalized_tags"
    echo "featured: $featured"
    echo "---"
    # Body: strip leading blank lines, keep the rest
    echo "$body" | sed '/./,$!d'
  } > "$output"

  echo "  Transformed: $(basename "$input") → $(basename "$output")" >&2
}

# --- Main ---

if [[ "${1:-}" == "--batch" ]]; then
  input_dir="${2:?Usage: $0 --batch <input-dir> <output-dir>}"
  output_dir="${3:?Usage: $0 --batch <input-dir> <output-dir>}"
  mkdir -p "$output_dir"

  count=0
  errors=0
  for f in "$input_dir"/*.md; do
    [[ -f "$f" ]] || continue
    slug=$(basename "$f")
    if transform_single "$f" "$output_dir/$slug"; then
      count=$((count + 1))
    else
      errors=$((errors + 1))
    fi
  done
  echo "" >&2
  echo "Batch complete: $count transformed, $errors errors" >&2

elif [[ -n "${1:-}" ]]; then
  transform_single "$1" "${2:-/dev/stdout}"

else
  echo "Usage:" >&2
  echo "  $0 <input.md> [output.md]" >&2
  echo "  $0 --batch <input-dir> <output-dir>" >&2
  exit 1
fi
