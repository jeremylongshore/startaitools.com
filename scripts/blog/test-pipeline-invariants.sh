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
# push_with_rebase: the land script's push recovery must work in a DIRTY tree.
#
# blog-land.sh says in its own header that it does not require a clean tree,
# then its recovery path called a bare `git pull --rebase`, which refuses to run
# with unstaged changes. On 2026-08-09 a release-bot commit landed between the
# fetch and the push while a tracked file was modified, the rebase bailed, and a
# perfectly good post commit was stranded with an urgent page. These fixtures
# reproduce that exact shape against a real remote.
# ---------------------------------------------------------------------------
PUSH_FIX=$TEST_REPO/pushfix
mkdir -p "$PUSH_FIX"
git init -q --bare "$PUSH_FIX/remote.git"
git clone -q "$PUSH_FIX/remote.git" "$PUSH_FIX/a"
git -C "$PUSH_FIX/a" config user.name test
git -C "$PUSH_FIX/a" config user.email test@example.invalid
printf 'seed\n' > "$PUSH_FIX/a/tracked.txt"
git -C "$PUSH_FIX/a" add tracked.txt
git -C "$PUSH_FIX/a" commit -qm seed
BR=$(git -C "$PUSH_FIX/a" rev-parse --abbrev-ref HEAD)
git -C "$PUSH_FIX/a" push -q origin "$BR"

# A second clone stands in for the release bot, which pushes to the same branch
# on nearly every push and is what wins the race in production.
git clone -q "$PUSH_FIX/remote.git" "$PUSH_FIX/bot"
git -C "$PUSH_FIX/bot" config user.name bot
git -C "$PUSH_FIX/bot" config user.email bot@example.invalid
bot_push() {
  # Re-sync first: earlier fixtures push to the same remote, so the bot clone is
  # behind by the time it is called again. The real release workflow always runs
  # against a fresh checkout, so a stale clone is a fixture artifact, not the
  # behaviour under test.
  git -C "$PUSH_FIX/bot" fetch -q origin "$BR"
  git -C "$PUSH_FIX/bot" reset -q --hard "origin/$BR"
  printf '%s\n' "$1" > "$PUSH_FIX/bot/release.txt"
  git -C "$PUSH_FIX/bot" add release.txt
  git -C "$PUSH_FIX/bot" commit -qm "chore: release $1 [skip ci]"
  git -C "$PUSH_FIX/bot" push -q origin "$BR"
}

PUSH_LOG=$TEST_REPO/push.log; : > "$PUSH_LOG"

# The reproduction: bot lands first, our post commit exists, and a TRACKED file
# is modified but unstaged. This is the case that stranded the commit.
bot_push v1.0.0
printf 'post\n' > "$PUSH_FIX/a/post.md"
git -C "$PUSH_FIX/a" add post.md
git -C "$PUSH_FIX/a" commit -qm "post: the one that got stranded"
printf 'dirty\n' >> "$PUSH_FIX/a/tracked.txt"   # <- unstaged, tracked

# Prove the OLD behaviour actually fails, so this test cannot pass vacuously.
if git -C "$PUSH_FIX/a" pull --rebase origin "$BR" >/dev/null 2>&1; then
  echo "FAIL: bare 'pull --rebase' succeeded in a dirty tree; fixture does not reproduce" >&2
  exit 1
fi

( cd "$PUSH_FIX/a" && push_with_rebase "$BR" "$PUSH_LOG" ) || {
  echo "FAIL: push_with_rebase could not land a commit from a dirty tree" >&2
  /usr/bin/tail -5 "$PUSH_LOG" >&2; exit 1; }

# The post reached the remote...
git -C "$PUSH_FIX/a" fetch -q origin
git -C "$PUSH_FIX/a" cat-file -e "origin/$BR:post.md" 2>/dev/null || {
  echo "FAIL: the post commit did not reach the remote" >&2; exit 1; }
# ...the bot's commit survived (we rebased onto it, not over it)...
git -C "$PUSH_FIX/a" cat-file -e "origin/$BR:release.txt" 2>/dev/null || {
  echo "FAIL: rebase clobbered the concurrent commit" >&2; exit 1; }
# ...and the uncommitted local work was restored by the autostash, not eaten.
case "$(/usr/bin/cat "$PUSH_FIX/a/tracked.txt")" in *dirty*) ;; *)
  echo "FAIL: autostash lost the uncommitted working-tree change" >&2; exit 1;; esac
# Nothing may be left stashed after a clean run.
[ -z "$(git -C "$PUSH_FIX/a" stash list)" ] || {
  echo "FAIL: push_with_rebase left a stash behind" >&2; exit 1; }

# A clean fast-forward push must NOT rebase at all (no spurious log noise).
: > "$PUSH_LOG"
printf 'second\n' > "$PUSH_FIX/a/post2.md"
git -C "$PUSH_FIX/a" add post2.md
git -C "$PUSH_FIX/a" commit -qm "post: uncontested"
( cd "$PUSH_FIX/a" && push_with_rebase "$BR" "$PUSH_LOG" ) || {
  echo "FAIL: uncontested push failed" >&2; exit 1; }
case "$(/usr/bin/cat "$PUSH_LOG")" in *"push rejected"*)
  echo "FAIL: an uncontested push went down the rebase path" >&2; exit 1;; esac

# A push that can never succeed must give up and report failure rather than loop.
: > "$PUSH_LOG"
git clone -q "$PUSH_FIX/remote.git" "$PUSH_FIX/c"
git -C "$PUSH_FIX/c" config user.name test
git -C "$PUSH_FIX/c" config user.email test@example.invalid
git -C "$PUSH_FIX/c" remote set-url origin "$PUSH_FIX/does-not-exist.git"
printf 'x\n' > "$PUSH_FIX/c/x.md"; git -C "$PUSH_FIX/c" add x.md
git -C "$PUSH_FIX/c" commit -qm "post: unpushable"
if ( cd "$PUSH_FIX/c" && push_with_rebase "$BR" "$PUSH_LOG" 2 ); then
  echo "FAIL: push_with_rebase reported success against a dead remote" >&2
  exit 1
fi

# reconcile_repo carries a feature branch across a moved default branch.
# An FF-push cannot succeed once origin/<default> has moved, and the release
# workflow moves it constantly, so the old code reported "needs manual merge"
# for a case whose real remedy was a rebase.
git clone -q "$PUSH_FIX/remote.git" "$PUSH_FIX/d"
git -C "$PUSH_FIX/d" config user.name test
git -C "$PUSH_FIX/d" config user.email test@example.invalid
git -C "$PUSH_FIX/d" checkout -q -b feat/defensive
printf 'defensive\n' > "$PUSH_FIX/d/defensive.md"
git -C "$PUSH_FIX/d" add defensive.md
git -C "$PUSH_FIX/d" commit -qm "post: committed defensively to a feature branch"
bot_push v2.0.0          # origin/<default> moves out from under the FF
: > "$PUSH_LOG"; RECONCILED=""
( cd "$PUSH_FIX/d" && RECONCILED="" && reconcile_repo "$PUSH_FIX/d" fixture "$PUSH_LOG" "$BR" \
  && git fetch -q origin && git cat-file -e "origin/$BR:defensive.md" ) || {
  echo "FAIL: reconcile_repo did not carry the branch across a moved default" >&2
  /usr/bin/tail -5 "$PUSH_LOG" >&2; exit 1; }
# The concurrent release commit must survive the rebase.
git -C "$PUSH_FIX/d" cat-file -e "origin/$BR:release.txt" 2>/dev/null || {
  echo "FAIL: reconcile_repo's rebase clobbered the concurrent commit" >&2; exit 1; }

# A genuine conflict must still report ORPHANED rather than inventing a merge.
git clone -q "$PUSH_FIX/remote.git" "$PUSH_FIX/e"
git -C "$PUSH_FIX/e" config user.name test
git -C "$PUSH_FIX/e" config user.email test@example.invalid
git -C "$PUSH_FIX/e" checkout -q -b feat/conflicting
printf 'ours\n' > "$PUSH_FIX/e/release.txt"     # same path the bot owns
git -C "$PUSH_FIX/e" add release.txt
git -C "$PUSH_FIX/e" commit -qm "post: conflicts with the release file"
bot_push v3.0.0
: > "$PUSH_LOG"; RECONCILED=""
( cd "$PUSH_FIX/e" && RECONCILED="" && reconcile_repo "$PUSH_FIX/e" fixture "$PUSH_LOG" "$BR"
  case "$RECONCILED" in *ORPHANED*) exit 0;; *) exit 1;; esac ) || {
  echo "FAIL: a conflicting reconcile did not report ORPHANED" >&2; exit 1; }
# And it must not leave the fixture mid-rebase.
[ ! -d "$PUSH_FIX/e/.git/rebase-merge" ] && [ ! -d "$PUSH_FIX/e/.git/rebase-apply" ] || {
  echo "FAIL: reconcile_repo left a rebase in progress" >&2; exit 1; }

echo "push-recovery invariant tests: pass"

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
# X gained a second surface (the long-form article) for the same reason LinkedIn has
# two. Both resolve to utm_source=x, so without utm_content the tweet row and the
# article row collapse into one and neither can be attributed.
U_XA=$(utm "$CANON" x x_article)
if [ "$U_X" = "$U_XA" ]; then
  echo "FAIL: X tweet and X article links are identical ($U_X)" >&2
  exit 1
fi
case "$U_XA" in *utm_content=x_article*) ;; *)
  echo "FAIL: x article link carries no utm_content: $U_XA" >&2; exit 1;; esac
case "$U_X" in *utm_content=*)
  echo "FAIL: the plain tweet link picked up a utm_content: $U_X" >&2; exit 1;; esac
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

# --- 5. The X long-form article is a real sixth destination ------------------
# It is tier-gated with Substack and Medium, it renders its own section, and the
# checklist count at the top has to match the sections below it. That count is
# derived from the destination list, so a mismatch means the destination was added
# in one place and not the other, which is exactly how a checklist starts lying.
T2=$(jq -nc '{post_title:"T",canonical_url:"https://x.test/p/",tier:2,
  destinations:["x","li_personal","li_company","substack","medium","x_article"],
  links:{x:"https://x.test/p/?utm_source=x",
         x_article:"https://x.test/p/?utm_source=x&utm_content=x_article"},
  x_post:"raw",li_personal:"personal",li_company:"house",
  substack_subtitle:"sub",
  x_article_title:"An Honest Title",x_article_subtitle:"One line of framing."}')
HTML=$(render_packet "$T2")
case "$HTML" in *"Post it to <strong>6</strong> places"*) ;; *)
  echo "FAIL: tier-2 checklist does not count six destinations" >&2; exit 1;; esac
case "$HTML" in *"X (long-form article)"*) ;; *)
  echo "FAIL: tier-2 packet rendered no X-article section" >&2; exit 1;; esac
case "$HTML" in *"An Honest Title"*) ;; *)
  echo "FAIL: X-article title did not render" >&2; exit 1;; esac
case "$HTML" in *"utm_content=x_article"*) ;; *)
  echo "FAIL: X-article link is missing its distinguishing utm_content" >&2; exit 1;; esac
# The checklist count must equal the number of destination sections actually below it.
# Every destination section is an <h2>; the media block is the one other <h2>, and this
# fixture carries no media.
SECTIONS=$(printf '%s' "$HTML" | grep -o '<h2>' | wc -l)
[ "$SECTIONS" -eq 6 ] || {
  echo "FAIL: checklist says 6 destinations but $SECTIONS sections rendered" >&2; exit 1; }
# The caveat is the point of the destination, not decoration: an X article cannot carry
# a canonical, so Ezekiel has to be told this one is not SEO-neutral.
case "$HTML" in *"not an SEO-neutral syndication"*) ;; *)
  echo "FAIL: X-article section does not disclose the missing canonical" >&2; exit 1;; esac

# Tier 1 gets three destinations and NO X article.
T1=$(jq -nc '{post_title:"T",canonical_url:"https://x.test/p/",tier:1,
  destinations:["x","li_personal","li_company"],
  x_post:"raw",li_personal:"personal",li_company:"house"}')
HTML=$(render_packet "$T1")
case "$HTML" in *"Post it to <strong>3</strong> places"*) ;; *)
  echo "FAIL: tier-1 checklist does not count three destinations" >&2; exit 1;; esac
case "$HTML" in *"X (long-form article)"*)
  echo "FAIL: tier-1 packet rendered an X-article section" >&2; exit 1;; esac

# An empty title degrades LOUDLY. This is the defect that deleted a whole LinkedIn
# section while the checklist still counted it, and the new destination must not
# reintroduce it.
NO_TITLE=$(jq -nc '{post_title:"T",canonical_url:"https://x.test/p/",tier:2,
  destinations:["x","substack","medium","x_article"],
  links:{x_article:"https://x.test/p/?utm_source=x&utm_content=x_article"},
  x_post:"raw",x_article_title:"",x_article_subtitle:""}')
HTML=$(render_packet "$NO_TITLE")
case "$HTML" in *"X (long-form article)"*) ;; *)
  echo "FAIL: empty X-article title silently dropped the section" >&2; exit 1;; esac
case "$HTML" in *"COPY MISSING"*) ;; *)
  echo "FAIL: empty X-article title did not produce a loud degraded box" >&2; exit 1;; esac
# The destination stays actionable even degraded: he still gets the link to paste.
case "$HTML" in *"utm_content=x_article"*) ;; *)
  echo "FAIL: degraded X-article section dropped its link" >&2; exit 1;; esac

# NOTE: the behavioural check that lint_voice_fields actually REJECTS bad X-article
# copy lives in tests/test_blog_pipeline.py, not here. It needs known-bad fixtures
# (an em dash, a deny-listed phrase) and this file is itself held to the voice lint,
# so carrying those literals here would fail the gate it exists to protect. The
# pytest module is already exempt for exactly that reason.

echo "packet-rendering invariant tests: pass"
