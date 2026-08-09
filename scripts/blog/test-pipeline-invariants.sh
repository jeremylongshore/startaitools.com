#!/usr/bin/env bash
# Owner-independent regression checks for publication-aware idempotency.

set -euo pipefail

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=./lib-cron-common.sh
source "$HERE/lib-cron-common.sh"

TEST_REPO=$(mktemp -d)
trap 'rm -rf "$TEST_REPO"' EXIT
mkdir -p "$TEST_REPO/content/posts"
git -C "$TEST_REPO" init -q
git -C "$TEST_REPO" config user.name test
git -C "$TEST_REPO" config user.email test@example.invalid

printf '%s\n' '+++' "title = 'Tracked'" "date = 2026-07-29T07:00:00-06:00" '+++' \
  > "$TEST_REPO/content/posts/tracked.md"
git -C "$TEST_REPO" add content/posts/tracked.md
git -C "$TEST_REPO" commit -qm seed

published_post_for_date "$TEST_REPO" "$TEST_REPO/content/posts" 2026-07-29 >/dev/null

printf '%s\n' '+++' "title = 'Orphan'" "date = 2026-07-30T07:00:00-06:00" '+++' \
  > "$TEST_REPO/content/posts/orphan.md"
post_exists_for_date "$TEST_REPO/content/posts" 2026-07-30 >/dev/null
if published_post_for_date "$TEST_REPO" "$TEST_REPO/content/posts" 2026-07-30 >/dev/null; then
  echo "FAIL: untracked producer artifact counted as published" >&2
  exit 1
fi

printf '%s\n' '# local modification' >> "$TEST_REPO/content/posts/tracked.md"
if published_post_for_date "$TEST_REPO" "$TEST_REPO/content/posts" 2026-07-29 >/dev/null; then
  echo "FAIL: modified tracked post counted as published" >&2
  exit 1
fi

echo "pipeline invariant tests: pass"

# Cross-posting must preserve the queue's canonical URL regardless of the
# transformed file's temporary location, record only the URL from stdout, and
# leave transient failures pending for a later retry.
BLOG_FIXTURE="$TEST_REPO/blog"
STUBS="$TEST_REPO/stubs"
mkdir -p "$BLOG_FIXTURE/content/posts" "$BLOG_FIXTURE/scripts/blog" "$STUBS"
cp "$HERE/lib-cron-common.sh" "$BLOG_FIXTURE/scripts/blog/lib-cron-common.sh"
printf '%s\n' '---' 'title: "Canonical Fixture"' '---' 'Body' \
  > "$BLOG_FIXTURE/content/posts/canonical-fixture.md"

cat > "$STUBS/transform" <<'EOF'
#!/usr/bin/env bash
cp "$1" "$2"
EOF
cat > "$STUBS/success" <<'EOF'
#!/usr/bin/env bash
[[ $(basename "$1") == "canonical-fixture.md" ]]
[[ "$CANONICAL_OVERRIDE" == "https://startaitools.com/posts/canonical-fixture/" ]]
echo "diagnostic output" >&2
echo "https://external.example/canonical-fixture"
EOF
cat > "$STUBS/fail" <<'EOF'
#!/usr/bin/env bash
echo "HTTP 429: retry later" >&2
exit 1
EOF
chmod +x "$STUBS/transform" "$STUBS/success" "$STUBS/fail"

jq -n '[{
  slug: "canonical-fixture",
  canonical_url: "https://startaitools.com/posts/canonical-fixture/",
  devto: {status: "pending", publish_after: "1970-01-01T00:00:00Z"},
  hashnode: {status: "published"},
  medium: {status: "skipped"}
}]' > "$BLOG_FIXTURE/.crosspost-queue.json"

PROCESSOR="$HERE/../../.claude/skills/blog-backfill/scripts/check-crosspost-queue.sh"
BLOG_DIR="$BLOG_FIXTURE" ASTRO_SCRIPT="$STUBS/transform" DEVTO_SCRIPT="$STUBS/success" \
  DEVTO_API_KEY=test "$PROCESSOR" >/dev/null
jq -e '.[0].devto.status == "published" and
  .[0].devto.url == "https://external.example/canonical-fixture"' \
  "$BLOG_FIXTURE/.crosspost-queue.json" >/dev/null

jq '.[0].devto = {status: "pending", publish_after: "1970-01-01T00:00:00Z"}' \
  "$BLOG_FIXTURE/.crosspost-queue.json" > "$BLOG_FIXTURE/.crosspost-queue.next"
mv "$BLOG_FIXTURE/.crosspost-queue.next" "$BLOG_FIXTURE/.crosspost-queue.json"
BLOG_DIR="$BLOG_FIXTURE" ASTRO_SCRIPT="$STUBS/transform" DEVTO_SCRIPT="$STUBS/fail" \
  DEVTO_API_KEY=test "$PROCESSOR" >/dev/null
jq -e '.[0].devto.status == "pending" and .[0].devto.attempts == 1 and
  (.[0].devto.retry_after | type == "string")' "$BLOG_FIXTURE/.crosspost-queue.json" >/dev/null

echo "cross-post invariant tests: pass"

# ---------------------------------------------------------------------------
# Posting-packet invariants (added 2026-08-09 with the packet defect fixes).
#
# These pull the real function bodies out of blog-posting-packet.sh rather than
# reimplementing them, so a regression in the script fails here. Sourcing the
# whole script is not an option: it runs its main body at load time.
# ---------------------------------------------------------------------------
PACKET="$HERE/blog-posting-packet.sh"
extract_fn() { sed -n "/^$1() {/,/^}/p" "$PACKET"; }

# --- 1. UTM distinctness ---------------------------------------------------
# Both LinkedIn surfaces resolve to utm_source=linkedin. Without utm_content the
# personal and company links were byte-identical, so neither could be attributed
# and the weekly rollup could not tell the two apart. This is the regression
# guard for that: the two links must differ.
eval "$(extract_fn utm)"
CANON="https://startaitools.com/posts/fixture/"
U_X=$(utm "$CANON" x)
U_P=$(utm "$CANON" linkedin li_personal)
U_C=$(utm "$CANON" linkedin li_company)
if [ "$U_P" = "$U_C" ]; then
  echo "FAIL: LinkedIn personal and company links are identical ($U_P)" >&2
  exit 1
fi
case "$U_P" in *utm_content=li_personal*) ;; *)
  echo "FAIL: personal link carries no utm_content: $U_P" >&2; exit 1;; esac
case "$U_C" in *utm_content=li_company*) ;; *)
  echo "FAIL: company link carries no utm_content: $U_C" >&2; exit 1;; esac
case "$U_X" in *utm_source=x*) ;; *)
  echo "FAIL: x link carries no utm_source: $U_X" >&2; exit 1;; esac
# A URL that already has a query string must extend it, not start a second one.
U_Q=$(utm "https://startaitools.com/p/?a=1" linkedin li_company)
case "$U_Q" in *"?a=1&utm_source="*) ;; *)
  echo "FAIL: existing query string not extended: $U_Q" >&2; exit 1;; esac

# --- 2. Disclaimer gate is fail-CLOSED -------------------------------------
# A missing library used to `return 0`, which reads as "no governed entity
# matched" and lets a post about a governed partner ship with no disclaimer. Not
# being able to tell is a HOLD, not an all-clear.
eval "$(extract_fn select_disclaimers)"
DISC_FIXTURE="$TEST_REPO/body.txt"
printf 'This post is about a governed partner.\n' > "$DISC_FIXTURE"

DISCLAIMER_LIB="$TEST_REPO/definitely-not-here.json"
if out=$(select_disclaimers "$DISC_FIXTURE"); then
  echo "FAIL: missing disclaimer library returned success (fails open)" >&2
  exit 1
fi
case "$out" in HOLD:*) ;; *)
  echo "FAIL: missing disclaimer library did not emit a HOLD (got: $out)" >&2; exit 1;; esac

DISCLAIMER_LIB="$TEST_REPO/broken-lib.json"
printf 'not json at all' > "$DISCLAIMER_LIB"
if out=$(select_disclaimers "$DISC_FIXTURE"); then
  echo "FAIL: unreadable disclaimer library returned success (fails open)" >&2
  exit 1
fi
case "$out" in HOLD:*) ;; *)
  echo "FAIL: unreadable disclaimer library did not emit a HOLD (got: $out)" >&2; exit 1;; esac

# A well-formed library with a matching entity and NO approved string still HOLDs.
DISCLAIMER_LIB="$TEST_REPO/governed-lib.json"
jq -n '{default_footer:"f",entities:{acme:{match:["governed partner"],approved:[]}}}' \
  > "$DISCLAIMER_LIB"
if out=$(select_disclaimers "$DISC_FIXTURE"); then
  echo "FAIL: governed entity with no approved string returned success" >&2
  exit 1
fi
case "$out" in *HOLD:acme*) ;; *)
  echo "FAIL: expected HOLD:acme, got: $out" >&2; exit 1;; esac

# And a matching entity WITH an approved string passes, emitting the string.
DISCLAIMER_LIB="$TEST_REPO/ok-lib.json"
jq -n '{default_footer:"f",entities:{acme:{match:["governed partner"],approved:["Approved note."]}}}' \
  > "$DISCLAIMER_LIB"
if ! out=$(select_disclaimers "$DISC_FIXTURE"); then
  echo "FAIL: approved disclaimer path returned non-zero (got: $out)" >&2
  exit 1
fi
[ "$out" = "Approved note." ] || {
  echo "FAIL: expected the approved note, got: $out" >&2; exit 1; }

echo "posting-packet invariant tests: pass"

# --- 3. Empty copy field degrades LOUDLY, never silently ------------------
# `dest.has('li_personal') && p.li_personal` made the whole section vanish when
# the copy was empty, so the checklist still said "post it to 3 places" while
# only two boxes existed. Ezekiel could not tell a dropped section from one that
# was never meant to be there.
HTML_GEN="$HERE/blog-packet-html.cjs"
render_packet() { printf '%s' "$1" | node "$HTML_GEN" --fragment; }

EMPTY_LIP=$(jq -nc '{post_title:"T",canonical_url:"https://x.test/p/",tier:1,
  destinations:["x","li_personal","li_company"],
  x_post:"raw copy",li_personal:"",li_company:"house copy"}')
HTML=$(render_packet "$EMPTY_LIP")
case "$HTML" in *"COPY MISSING"*) ;; *)
  echo "FAIL: empty li_personal did not produce a loud degraded box" >&2; exit 1;; esac
case "$HTML" in *"Post #2"*) ;; *)
  echo "FAIL: empty li_personal silently dropped the Post #2 section" >&2; exit 1;; esac
# The sections that DO have copy must still render their copy, not a warning.
case "$HTML" in *"house copy"*) ;; *)
  echo "FAIL: populated li_company section went missing" >&2; exit 1;; esac

# Populated fields must NOT trigger the degraded box.
FULL=$(jq -nc '{post_title:"T",canonical_url:"https://x.test/p/",tier:1,
  destinations:["x","li_personal","li_company"],
  x_post:"raw",li_personal:"personal",li_company:"house"}')
case "$(render_packet "$FULL")" in *"COPY MISSING"*)
  echo "FAIL: fully populated packet showed a degraded box" >&2; exit 1;; esac

# --- 4. Media block reaches the packet ------------------------------------
# Ezekiel posts image plus text; if the packet does not name the files the post
# goes out bare.
MEDIA=$(jq -nc '{post_title:"T",canonical_url:"https://x.test/p/",tier:1,
  destinations:["x"],x_post:"raw",
  media:{generated:"https://startaitools.com/images/posts/a.png",
         card_og:"https://startaitools.com/images/posts/cards/a-og.png",
         card_square:"https://startaitools.com/images/posts/cards/a-square.png",
         generated_failed:false}}')
HTML=$(render_packet "$MEDIA")
for needle in "Generated art" "1200x630" "1080x1080" "a-og.png"; do
  case "$HTML" in *"$needle"*) ;; *)
    echo "FAIL: media block missing '$needle'" >&2; exit 1;; esac
done
# Ezekiel is remote: a public URL must render as a clickable link, never as a
# path he cannot open.
case "$HTML" in *'<a href="https://startaitools.com/images/posts/a.png"'*) ;; *)
  echo "FAIL: media URL did not render as a link" >&2; exit 1;; esac
# A local path (outside static/) must be flagged as unusable rather than shown
# as if it were a link.
LOCAL_MEDIA=$(jq -nc '{post_title:"T",canonical_url:"https://x.test/p/",tier:1,
  destinations:["x"],x_post:"raw",
  media:{generated:"/home/jeremy/somewhere/a.png",card_og:null,card_square:null,
         generated_failed:false}}')
case "$(render_packet "$LOCAL_MEDIA")" in *"local file, ask Jeremy"*) ;; *)
  echo "FAIL: local-only media path was not flagged as unusable" >&2; exit 1;; esac
# A generation failure has to be visible, not silently swallowed by the card.
FELL_BACK=$(jq -nc '{post_title:"T",canonical_url:"https://x.test/p/",tier:1,
  destinations:["x"],x_post:"raw",
  media:{generated:null,card_og:"/repo/a-og.png",card_square:"/repo/a-square.png",
         generated_failed:true}}')
case "$(render_packet "$FELL_BACK")" in *"generation failed"*) ;; *)
  echo "FAIL: card fallback did not announce that generation failed" >&2; exit 1;; esac

echo "packet-rendering invariant tests: pass"
