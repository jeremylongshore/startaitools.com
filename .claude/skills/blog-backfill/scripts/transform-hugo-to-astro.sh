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

  # Rewrite Hugo post links so the syndicated copy contains no dead links.
  #
  # Hugo serves posts at /posts/<slug>/ and the source bodies link that way (768
  # such links across content/posts). The destination serves them at /blog/<slug>/,
  # so every /posts/ link carried across verbatim 404s on the destination. Because
  # nothing rewrote them, 121 links in 32 syndicated posts were dead — pointing at
  # the destination's own domain, on the very pages whose canonical tags tell
  # Google to treat them as copies of startaitools. A one-time sweep had fixed the
  # then-existing 82 posts; the pipeline was never fixed, so drift resumed.
  #
  # Resolution rule, per target:
  #   syndicated (a sibling .md exists) -> /blog/<slug>/            (internal, keeps the reader)
  #   not syndicated                    -> the startaitools original (always resolves)
  #
  # The fallback is correct unconditionally, so a bulk backfill that has not yet
  # written a sibling merely yields a cross-domain link instead of an internal
  # one — never a broken one. That is why the check is allowed to be racy.
  local _outdir _slug _target
  _outdir=$(dirname "$output")
  for _slug in $(printf '%s' "$body" \
      | grep -oE '\]\(/posts/[A-Za-z0-9._-]+/?\)' \
      | sed -E 's#^\]\(/posts/##; s#/?\)$##' | sort -u); do
    if [[ -f "$_outdir/$_slug.md" ]]; then
      _target="/blog/$_slug/"
    else
      _target="https://startaitools.com/posts/$_slug/"
    fi
    # '#' as the delimiter because both pattern and replacement contain '/'.
    # Slugs are [A-Za-z0-9._-] so they carry no sed metacharacters. Both the
    # trailing-slash and bare forms are matched.
    body=$(printf '%s' "$body" | sed \
      -e "s#](/posts/$_slug/)#]($_target)#g" \
      -e "s#](/posts/$_slug)#]($_target)#g")
  done

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
    # canonical — the syndicated copy must point at the ORIGINAL on
    # startaitools, or the two properties compete for the same keywords as
    # duplicate content and Google picks a winner arbitrarily.
    #
    # The slug is the FILENAME, matching Hugo's /posts/:slug/ permalink for
    # every post this pipeline has produced since 2026-02 (verified: all 124
    # filename-slug posts resolve 200; the 52 title-derived URLs are historical,
    # from an older convention, and are backfilled explicitly downstream rather
    # than derived). Deriving from the title instead breaks current posts —
    # e.g. "Now-LMS 2.0" yields now-lms-20-... which 404s.
    _canon_slug=$(basename "$input" .md)
    echo "canonical: \"https://startaitools.com/posts/${_canon_slug}/\""
    echo "---"
    # Body: strip leading AND trailing blank lines, end with exactly one newline.
    # `body` accumulates as `body+="$line"$'\n'`, so it ALWAYS ends in a newline;
    # `echo` then appended a second one, so every emitted post ended `\n\n` and
    # tripped markdownlint MD012 (no-multiple-blanks) in the consuming repo, turning
    # its main red on every publish. Command substitution strips ALL trailing
    # newlines; printf restores exactly one. Interior blank lines are untouched.
    printf '%s\n' "$(printf '%s' "$body" | sed '/./,$!d')"
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
