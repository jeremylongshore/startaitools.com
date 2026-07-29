#!/usr/bin/env bash
# test-transform-hugo-to-astro.sh — regression corpus for the Hugo→Astro transform.
#
# WHY THIS EXISTS
# ---------------
# On 2026-07-26 every post the dual-publish pipeline emitted ended with TWO
# newlines. The consuming repo (claude-code-plugins) lints blog content with
# markdownlint, so MD012/no-multiple-blanks failed the `markdownlint` job, which
# fails the `ci-required` aggregate, which blocks EVERY open PR in that repo.
# It recurred five times in one day and was hand-patched four times before the
# root cause was fixed here.
#
# Root cause: `body` accumulates as `body+="$line"$'\n'`, so it always ends in a
# newline; the writer then used `echo "$body"`, appending a second one.
#
# These tests pin the emitted-file contract so that regression cannot return
# silently. Run: bash test-transform-hugo-to-astro.sh

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$HERE/transform-hugo-to-astro.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

pass=0
fail=0

ok()   { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
bad()  { printf '  FAIL %s\n     expected: %s\n     actual:   %s\n' "$1" "$2" "$3"; fail=$((fail + 1)); }

check() { # name expected actual
  if [[ "$2" == "$3" ]]; then ok "$1"; else bad "$1" "$2" "$3"; fi
}

trailing_newlines() { python3 -c "
import sys
s = open(sys.argv[1], encoding='utf-8').read()
print(len(s) - len(s.rstrip(chr(10))))" "$1"; }

interior_blanks() { python3 -c "
import sys
s = open(sys.argv[1], encoding='utf-8').read().rstrip(chr(10))
print(sum(1 for l in s.split(chr(10)) if l == ''))" "$1"; }

make_post() { # path body-suffix
  cat > "$1" <<'FM'
+++
title = "Test Post"
date = "2026-07-27"
description = "A fixture"
tags = ["testing"]
+++

# Heading

First paragraph.

Second paragraph after an interior blank line.
FM
  printf '%s' "$2" >> "$1"
}

echo "transform-hugo-to-astro regression corpus"
echo

# 1. The exact defect: source ending with a single newline must emit ONE newline.
make_post "$TMP/a.md" ''
bash "$TRANSFORM" "$TMP/a.md" "$TMP/a.out.md" >/dev/null 2>&1
check "single trailing newline in source -> exactly 1 in output" "1" "$(trailing_newlines "$TMP/a.out.md")"

# 2. Source with trailing blank lines must still emit exactly ONE newline.
make_post "$TMP/b.md" $'\n\n\n'
bash "$TRANSFORM" "$TMP/b.md" "$TMP/b.out.md" >/dev/null 2>&1
check "multiple trailing blank lines collapse to 1 newline" "1" "$(trailing_newlines "$TMP/b.out.md")"

# 3. Interior blank lines are structural markdown and must survive untouched.
#    The fixture body is: <blank> / "# Heading" / <blank> / "First paragraph." /
#    <blank> / "Second paragraph...". The LEADING blank is stripped by design
#    (`sed '/./,$!d'`), leaving the 2 genuinely interior blanks.
check "interior blank lines preserved (not collapsed)" "2" "$(interior_blanks "$TMP/a.out.md")"

# 4. Frontmatter is still emitted and the body is not truncated.
check "astro frontmatter opens the file" "---" "$(head -1 "$TMP/a.out.md")"
check "body content survives" "1" "$(grep -c 'Second paragraph after an interior blank line.' "$TMP/a.out.md")"

# 5. The consuming repo's actual gate: MD012 must not fire.
if command -v npx >/dev/null 2>&1; then
  # The cd+lint runs in its own subshell so a cd failure cannot fall through to
  # the `|| true`; that guard exists solely for `grep -c`, which exits 1 when the
  # count is legitimately 0 — which is the passing case here.
  md012=$( (cd "$TMP" && timeout 120 npx -y markdownlint-cli2 'a.out.md' 'b.out.md' 2>&1) | grep -c 'MD012' || true)
  check "markdownlint MD012/no-multiple-blanks does not fire" "0" "$md012"
else
  echo "  skip markdownlint check (npx unavailable)"
fi

# 6. Canonical — the syndicated copy must point at the ORIGINAL on startaitools.
#    Without it the dual-published copy self-canonicalises and the two properties
#    compete as duplicate content. Must be the FILENAME slug: deriving from the
#    title breaks current posts (e.g. "Now-LMS 2.0" -> now-lms-20-... which 404s).
canon=$(grep '^canonical:' "$TMP/a.out.md" | sed 's/canonical: "//;s/"$//')
check "canonical is emitted" "1" "$(grep -c '^canonical:' "$TMP/a.out.md")"
check "canonical uses the filename slug" "https://startaitools.com/posts/a/" "$canon"
check "canonical sits inside the frontmatter" "1" \
  "$(awk '/^---$/{c++} c==1 && /^canonical:/{found=1} END{print found+0}' "$TMP/a.out.md")"

# 7. Hugo /posts/ links must not survive into the syndicated copy.
#    Hugo serves /posts/<slug>/; the destination serves /blog/<slug>/, so a
#    verbatim carry-over 404s on the destination's own domain. 121 such links
#    across 32 posts were dead before this was fixed.
mklinked() { # path
  cat > "$1" <<'FM'
+++
title = "Linked Post"
date = "2026-07-29"
description = "Has post links"
tags = ["testing"]
+++

See [a syndicated one](/posts/sibling-exists/) and
[one that is not syndicated](/posts/never-syndicated/).
Bare form: [no slash](/posts/sibling-exists).
Already correct: [leave me](/blog/sibling-exists/).
External: [ext](https://example.com/posts/foo/).
FM
}

mkdir -p "$TMP/out"
: > "$TMP/out/sibling-exists.md"          # target IS syndicated
mklinked "$TMP/linked.md"
bash "$TRANSFORM" "$TMP/linked.md" "$TMP/out/linked.md" >/dev/null 2>&1
L="$TMP/out/linked.md"

# grep -c counts LINES; these assertions are about OCCURRENCES, and several
# land on the same line, so count matches instead.
occ() { grep -o "$1" "$2" 2>/dev/null | wc -l | tr -d ' '; }

# Three links resolve to the syndicated target: the slashed form, the bare form,
# and the one that was already correct.
check "syndicated target rewrites to /blog/<slug>/" "3" "$(occ '](/blog/sibling-exists/)' "$L")"
check "no /posts/ link survives for a syndicated target" "0" "$(occ '](/posts/sibling-exists' "$L")"
check "unsyndicated target falls back to the startaitools original" "1" \
  "$(occ '](https://startaitools.com/posts/never-syndicated/)' "$L")"
check "no site-relative /posts/ link survives at all" "0" "$(occ '](/posts/' "$L")"
check "an external URL containing /posts/ is untouched" "1" \
  "$(occ '](https://example.com/posts/foo/)' "$L")"

# The rewrite runs a command substitution over the body, which strips trailing
# newlines — so re-pin the newline contract on a post that was actually rewritten.
check "rewritten post still ends with exactly 1 newline" "1" "$(trailing_newlines "$L")"
check "rewritten post keeps its canonical" "1" "$(grep -c '^canonical:' "$L")"

echo
echo "  $pass passed, $fail failed"
[[ "$fail" -eq 0 ]] || exit 1
