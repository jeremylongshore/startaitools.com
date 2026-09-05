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
if [ -d "$PUSH_FIX/e/.git/rebase-merge" ] || [ -d "$PUSH_FIX/e/.git/rebase-apply" ]; then
  echo "FAIL: reconcile_repo left a rebase in progress" >&2
  exit 1
fi

echo "push-recovery invariant tests: pass"

# ---------------------------------------------------------------------------
# Pattern-engine receipt. `applied_patterns: []` proved nothing, because the
# engine emits it when nothing matched and a writing agent that skipped step 2b
# emits the identical thing by hand. Three months of records carried the key
# while v_pattern_usage stayed empty. The receipt is what makes the land gate
# real, so its properties are guarded here.
# ---------------------------------------------------------------------------
ENGINE="$HERE/../../.claude/skills/blog-backfill/scripts/apply-patterns.py"
DIGEST=$(python3 "$ENGINE" digest)
[ -n "$DIGEST" ] || { echo "FAIL: ruleset digest is empty" >&2; exit 1; }

# Every exit path stamps a receipt, including the no-tier early return.
for FIXTURE in \
  '{"slug":"a","tier":2,"dimensions":{"novelty":3,"arc":3,"nar":3,"tch":3,"scp":3,"rpr":3}}' \
  '{"slug":"b","tier":2}' \
  '{"slug":"c","tier":null}' ; do
  OUT=$(printf '%s' "$FIXTURE" | python3 "$ENGINE" apply)
  printf '%s' "$OUT" | jq -e '.pattern_engine.ran == true' >/dev/null || {
    echo "FAIL: no receipt stamped for fixture $FIXTURE" >&2; exit 1; }
  printf '%s' "$OUT" | jq -e --arg d "$DIGEST" '.pattern_engine.ruleset_digest == $d' >/dev/null || {
    echo "FAIL: receipt digest does not match the live ruleset for $FIXTURE" >&2; exit 1; }
done

# The digest must be a FUNCTION of the ruleset, or it cannot detect a stale record.
TMP_PAT=$TEST_REPO/patterns-alt.jsonl
jq -c '.' "$HERE/../../.claude/skills/blog-backfill/methodology/patterns.jsonl" > "$TMP_PAT"
printf '%s\n' '{"pattern_id":"test-x","active":true,"rule":{"all":[{"feature":"nov","op":">=","value":9}],"action":{"type":"cap_tier","tier":1}}}' >> "$TMP_PAT"
ALT=$(python3 - "$ENGINE" "$TMP_PAT" <<'EOF'
import importlib.util,sys,pathlib
spec=importlib.util.spec_from_file_location("ap",sys.argv[1])
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(m.ruleset_digest(pathlib.Path(sys.argv[2])))
EOF
)
[ "$ALT" != "$DIGEST" ] || {
  echo "FAIL: digest did not change when a rule was added; it cannot detect a stale ruleset" >&2
  exit 1; }

# The gate's own jq extraction must actually find the digest on a record.
REC=$(printf '%s' '{"date":"2026-08-11","slug":"probe","tier":2,"dimensions":{"novelty":3,"arc":3,"nar":3,"tch":3,"scp":3,"rpr":3}}' \
  | python3 "$ENGINE" apply | jq -c '. + {date:"2026-08-11", slug:"probe"}')
GOT=$(printf '%s\n' "$REC" | jq -r --arg d 2026-08-11 --arg s probe \
  'select(.date==$d and .slug==$s and .tier!=null) | .pattern_engine.ruleset_digest // ""' | head -1)
[ "$GOT" = "$DIGEST" ] || {
  echo "FAIL: the land gate's jq expression did not extract the digest (got '$GOT')" >&2; exit 1; }

# A receiptless record must yield the empty string the gate treats as a failure.
NOREC=$(printf '%s\n' '{"date":"2026-08-11","slug":"probe","tier":2,"applied_patterns":[]}' \
  | jq -r --arg d 2026-08-11 --arg s probe \
  'select(.date==$d and .slug==$s and .tier!=null) | .pattern_engine.ruleset_digest // ""' | head -1)
[ -z "$NOREC" ] || {
  echo "FAIL: a hand-written applied_patterns:[] record passed the receipt check" >&2; exit 1; }

# The land script must carry the gate with a DATE-based flip, not a human's memory.
LAND="$HERE/blog-land.sh"
/usr/bin/grep -q 'PATTERN_GATE_ENFORCE_FROM="20' "$LAND" || {
  echo "FAIL: blog-land.sh has no dated pattern-gate flip" >&2; exit 1; }
/usr/bin/grep -q 'pattern_engine.ruleset_digest' "$LAND" || {
  echo "FAIL: blog-land.sh does not check the receipt digest" >&2; exit 1; }

echo "pattern-receipt invariant tests: pass"

# ---------------------------------------------------------------------------
# The grader must be able to disagree in BOTH directions. The retired title
# heuristic could only ever demote, which is why 90 of 90 corpus mismatches were
# downgrades and got misread for months as classifier over-confidence.
# ---------------------------------------------------------------------------
SWEEP="$HERE/../../.claude/skills/blog-backfill/scripts/feedback-sweep.py"
/usr/bin/grep -q "def apparent_tier" "$SWEEP" && {
  echo "FAIL: the one-directional title heuristic apparent_tier() is back" >&2; exit 1; }
if ! python3 - "$SWEEP" <<'EOF'
import importlib.util,sys
spec=importlib.util.spec_from_file_location("fs",sys.argv[1])
fs=importlib.util.module_from_spec(spec); spec.loader.exec_module(fs)
# A narrative title must not change the grade. This is the whole defect.
for t in ["The Drills Passed. Reality Did Not.", "Empty Is Not Clean",
          "A Framework For Guard Patterns"]:
    for st in (1,2,3):
        assert fs.rubric_tier(st,t)==st, f"title '{t}' altered the grade at struct {st}"
# And the rubric must be able to produce every tier, or "too low" stays unreachable.
assert {fs.rubric_tier(s) for s in (1,2,3)} == {1,2,3}, "rubric cannot express all tiers"
EOF
then
  echo "FAIL: grader directionality checks failed" >&2
  exit 1
fi

echo "grader-directionality invariant tests: pass"

# ---------------------------------------------------------------------------
# Recommendation worker: the label boundary is the entire safety model, so it is
# guarded structurally. The worker implements auto-ok beads unattended and must
# never touch owner-gated ones (those change what gets published or how it reads).
# ---------------------------------------------------------------------------
WORKER="$HERE/blog-recommendation-worker.sh"
if [ -f "$WORKER" ]; then
  # It must require a POSITIVE allow assertion, not merely the absence of deny.
  # That is what makes a broken parse fail CLOSED: when `bd show --json` shape
  # changed under it, the deny check silently matched nothing, and only the
  # positive allow check kept it from proceeding.
  /usr/bin/grep -q 'LABEL_ALLOW=' "$WORKER" || {
    echo "FAIL: worker has no allow label" >&2; exit 1; }
  /usr/bin/grep -q 'LABEL_DENY=' "$WORKER" || {
    echo "FAIL: worker has no deny label" >&2; exit 1; }
  # shellcheck disable=SC2016 # the $ is a literal being grepped for, not an expansion
  /usr/bin/grep -q 'if ! printf .* jq -e --arg a "\$LABEL_ALLOW"' "$WORKER" || {
    echo "FAIL: worker does not REQUIRE the allow label (fail-open risk)" >&2; exit 1; }
  # bd show --json returns an array; without the unwrap every label check is a
  # silent no-op.
  /usr/bin/grep -q 'if type=="array" then .\[0\] else . end' "$WORKER" || {
    echo "FAIL: worker does not unwrap bd's JSON array; label checks would no-op" >&2
    exit 1; }
  # It must never merge or push the deploy branch.
  if /usr/bin/grep -nE '^[^#]*(gh pr merge|git merge |--admin|push .*origin .?\$?DEPLOY_BRANCH)' "$WORKER"; then
    echo "FAIL: worker contains a merge or a deploy-branch push" >&2; exit 1
  fi
  # It must re-run the deterministic gate itself rather than trust the agent.
  /usr/bin/grep -q 'lint-all.sh' "$WORKER" || {
    echo "FAIL: worker does not re-run the gate after the agent" >&2; exit 1; }
  # A crashed run must release the bead, or the queue stalls on it forever.
  # shellcheck disable=SC2016 # the $ is a literal being grepped for, not an expansion
  /usr/bin/grep -q 'bd update "\$BEAD" --status open' "$WORKER" || {
    echo "FAIL: worker never releases a claimed bead" >&2; exit 1; }
  echo "worker-safety invariant tests: pass"
fi

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
  destinations:["x","li_personal","li_company","substack","medium","x_article","buymeacoffee"],
  links:{x:"https://x.test/p/?utm_source=x",
         x_article:"https://x.test/p/?utm_source=x&utm_content=x_article",
         buymeacoffee:"https://x.test/p/?utm_source=buymeacoffee"},
  x_post:"raw",li_personal:"personal",li_company:"house",
  substack_subtitle:"sub",bmc_note:"A line for the people who back this.",
  x_article_title:"An Honest Title",x_article_subtitle:"One line of framing."}')
HTML=$(render_packet "$T2")
case "$HTML" in *"Post it to <strong>7</strong> places"*) ;; *)
  echo "FAIL: tier-2 checklist does not count seven destinations" >&2; exit 1;; esac
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
[ "$SECTIONS" -eq 7 ] || {
  echo "FAIL: checklist says 7 destinations but $SECTIONS sections rendered" >&2; exit 1; }
# The caveat is the point of the destination, not decoration: an X article cannot carry
# a canonical, so Ezekiel has to be told this one is not SEO-neutral.
case "$HTML" in *"not an SEO-neutral syndication"*) ;; *)
  echo "FAIL: X-article section does not disclose the missing canonical" >&2; exit 1;; esac

case "$HTML" in *"Buy Me a Coffee (supporter post)"*) ;; *)
  echo "FAIL: tier-2 packet rendered no Buy Me a Coffee section" >&2; exit 1;; esac
case "$HTML" in *"utm_source=buymeacoffee"*) ;; *)
  echo "FAIL: BMC link is missing its own utm_source" >&2; exit 1;; esac
case "$HTML" in *"Visibility: Public"*) ;; *)
  echo "FAIL: BMC section does not state the visibility choice" >&2; exit 1;; esac

# An empty supporter note degrades loudly, like every other destination.
NO_NOTE=$(jq -nc '{post_title:"T",canonical_url:"https://x.test/p/",tier:2,
  destinations:["buymeacoffee"],links:{buymeacoffee:"https://x.test/p/?utm_source=buymeacoffee"},
  bmc_note:""}')
case "$(render_packet "$NO_NOTE")" in *"COPY MISSING"*) ;; *)
  echo "FAIL: empty bmc_note did not produce a loud degraded box" >&2; exit 1;; esac

# Tier 1 gets three destinations and NO X article.
T1=$(jq -nc '{post_title:"T",canonical_url:"https://x.test/p/",tier:1,
  destinations:["x","li_personal","li_company"],
  x_post:"raw",li_personal:"personal",li_company:"house"}')
HTML=$(render_packet "$T1")
case "$HTML" in *"Post it to <strong>3</strong> places"*) ;; *)
  echo "FAIL: tier-1 checklist does not count three destinations" >&2; exit 1;; esac
case "$HTML" in *"X (long-form article)"*)
  echo "FAIL: tier-1 packet rendered an X-article section" >&2; exit 1;; esac
case "$HTML" in *"Buy Me a Coffee"*)
  echo "FAIL: tier-1 packet rendered a Buy Me a Coffee section" >&2; exit 1;; esac

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

# ── Disk headroom: the guard that refused the 2026-09-04 run ─────────────────
# Evidence for the incident: at 04:00 the producer saw 217 MiB free against a
# 500 MiB floor and refused. These tests pin the floor semantics, the early
# warning line, the message content an operator needs, and the units. The
# reading is injected (disk_free_mb is overridden); no test touches real space.
DG_LOG=$(mktemp)
DG_FAKE=""
# shellcheck disable=SC2317 # test doubles, invoked indirectly by disk_guard
disk_free_mb()  { printf '%s' "$DG_FAKE"; }
# shellcheck disable=SC2317
disk_mount_of() { printf '/'; }

dg_expect() { # <free_mb> <expected_rc> <expected_state> <label>
  local free="$1" want_rc="$2" want_state="$3" label="$4" rc=0
  DG_FAKE="$free"; : > "$DG_LOG"
  disk_guard /any/path 500 "$DG_LOG" 2048 >/dev/null || rc=$?
  if [ "$rc" != "$want_rc" ] || [ "${DISK_GUARD_STATE:-}" != "$want_state" ]; then
    echo "FAIL: disk_guard free=${free}MiB: rc=$rc state=${DISK_GUARD_STATE:-} (wanted rc=$want_rc state=$want_state) [$label]" >&2
    exit 1
  fi
}
dg_expect 217   1 fatal "the incident reading"
dg_expect 0     1 fatal "empty disk"
dg_expect 499   1 fatal "one MiB under the floor"
dg_expect 500   0 warn  "exactly at the floor runs (floor is exclusive)"
dg_expect 2047  0 warn  "one MiB under the warning line"
dg_expect 2048  0 ok    "exactly at the warning line is clean"
dg_expect 60000 0 ok    "healthy"
DG_FAKE=""; : > "$DG_LOG"
disk_guard /any/path 500 "$DG_LOG" 2048 >/dev/null || { echo "FAIL: unreadable free space must not block" >&2; exit 1; }
[ "${DISK_GUARD_STATE:-}" = "unknown" ] || { echo "FAIL: unreadable free space must report state=unknown" >&2; exit 1; }

# Refusal message carries the numbers an operator acts on, in MiB, and keeps
# the FATAL marker the consecutive-failure counter greps for.
DG_FAKE=217; : > "$DG_LOG"; disk_guard /any/path 500 "$DG_LOG" 2048 >/dev/null || true
for needle in "FATAL:" "217MiB free" "need 500MiB" "refusing to run"; do
  grep -qF "$needle" "$DG_LOG" || { echo "FAIL: refusal log line lacks '$needle'" >&2; exit 1; }
done
if ! { [ "$DISK_GUARD_FREE_MB" = "217" ] && [ "$DISK_GUARD_MOUNT" = "/" ]; }; then
  echo "FAIL: DISK_GUARD_FREE_MB/MOUNT not exported for the alert" >&2; exit 1; fi
DG_FAKE=900; : > "$DG_LOG"; disk_guard /any/path 500 "$DG_LOG" 2048 >/dev/null
if ! { grep -qF "WARN:" "$DG_LOG" && grep -qF "900MiB free" "$DG_LOG" && grep -qF "2048MiB" "$DG_LOG"; }; then
  echo "FAIL: warning log line lacks the reading or the line it crossed" >&2; exit 1; fi
grep -qF "FATAL" "$DG_LOG" && { echo "FAIL: a warning must not carry the FATAL marker" >&2; exit 1; }
# Three-argument callers (blog-land.sh) keep the old contract: no warning tier.
DG_FAKE=900; : > "$DG_LOG"; disk_guard /any/path 500 "$DG_LOG" >/dev/null
[ "$DISK_GUARD_STATE" = "ok" ] || { echo "FAIL: legacy 3-arg call must not warn" >&2; exit 1; }

# The alert helper never fails the caller and never fires above the floor when
# the guard said ok. (buzz_post is stubbed: the test must not reach Buzz.)
DG_SENT=""
# shellcheck disable=SC2317 # test double, invoked indirectly by disk_warn_alert
buzz_post() { DG_SENT="$1|$2|$3"; }
disk_warn_alert "blog-backfill-daily" "900MiB free" || { echo "FAIL: disk_warn_alert returned non-zero" >&2; exit 1; }
case "$DG_SENT" in "WARNING (not a failure) blog-backfill-daily: 900MiB free|sys-automation|high") ;; *)
  echo "FAIL: warning alert text/topic/severity wrong: $DG_SENT" >&2; exit 1;; esac

# NEGATIVE TEST: prove the assertions above would catch a broken guard. Mutate
# the floor comparison in a COPY of the library (never the real file), source
# it in a subshell, and require the incident reading to be (wrongly) accepted.
MUTANT=$(mktemp)
# shellcheck disable=SC2016 # the $ signs are sed/grep literals, not expansions
sed 's/\[ "\$avail_mb" -lt "\$min_mb" \]/[ "$avail_mb" -gt "$min_mb" ]/' "$HERE/lib-cron-common.sh" > "$MUTANT"
# shellcheck disable=SC2016
grep -qF '"$avail_mb" -gt "$min_mb"' "$MUTANT" || { echo "FAIL: mutant did not apply (floor comparison moved?)" >&2; exit 1; }
# shellcheck disable=SC1090,SC2317 # sourcing the mutant copy; doubles run indirectly
if ( source "$MUTANT"; disk_free_mb() { printf '217'; }; disk_mount_of() { printf '/'; }
     disk_guard /any/path 500 "$DG_LOG" 2048 >/dev/null 2>&1 ); then
  echo "negative test: mutant with inverted floor accepted 217MiB (as expected) and the real assertion above rejects it"
else
  echo "FAIL: negative test is not sensitive: the inverted-floor mutant still refused 217MiB" >&2; exit 1
fi
rm -f "$MUTANT" "$DG_LOG"
unset -f disk_free_mb disk_mount_of buzz_post
echo "disk-headroom invariant tests: pass"

# ── Target date: calendar day, injectable clock, DST-safe ─────────────────────
# shellcheck source=./lib-cron-common.sh
source "$HERE/lib-cron-common.sh"
td() { local want="$1"; shift; local got; got=$("$@" 2>/dev/null) || got="(rejected)"
  [ "$got" = "$want" ] || { echo "FAIL: $* -> '$got' (wanted '$want')" >&2; exit 1; }; }
# Spring-forward night (US): 2026-03-08 02:00 local does not exist. A "now minus
# 24 hours" target computed at 00:30 on the 9th would land on the 7th in a DST
# zone; calendar-day arithmetic lands on the 8th in every zone.
BLOG_CLOCK="2026-03-09 00:30:00" TZ=America/Chicago td 2026-03-08 resolve_target_date ""
BLOG_CLOCK="2026-03-09 00:30:00" TZ=Etc/GMT+6        td 2026-03-08 resolve_target_date ""
BLOG_CLOCK="2026-11-02 00:30:00" TZ=America/Chicago td 2026-11-01 resolve_target_date ""
BLOG_CLOCK="2026-03-01 04:00:00" TZ=Etc/GMT+6        td 2026-02-28 resolve_target_date ""
BLOG_CLOCK="2026-01-01 04:00:00" TZ=Etc/GMT+6        td 2025-12-31 resolve_target_date ""
# Explicit --date: strict, real, not in the future.
BLOG_CLOCK="2026-09-05 09:00:00" td 2026-09-04   resolve_target_date 2026-09-04
BLOG_CLOCK="2026-09-05 09:00:00" td 2026-09-05   resolve_target_date 2026-09-05
BLOG_CLOCK="2026-09-05 09:00:00" td "(rejected)" resolve_target_date 2026-09-06
BLOG_CLOCK="2026-09-05 09:00:00" td "(rejected)" resolve_target_date 2026-9-4
BLOG_CLOCK="2026-09-05 09:00:00" td "(rejected)" resolve_target_date 2026-02-30
BLOG_CLOCK="2026-09-05 09:00:00" td "(rejected)" resolve_target_date yesterday
BLOG_CLOCK="2026-09-05 09:00:00" td "(rejected)" resolve_target_date "2026-09-04; rm -rf /"
echo "target-date invariant tests: pass"

# ── Retention: bounded, allowlisted, refuses the unknown ──────────────────────
RT_ROOT="$HOME/.local/state/blog-invariant-test.$$"
RT_LOG=$(mktemp)
mkdir -p "$RT_ROOT/nested"
trap 'rm -rf "$TEST_REPO" "$RT_ROOT" "$RT_LOG"' EXIT
touch -d "200 days ago" "$RT_ROOT/run-2026-01-01.log" "$RT_ROOT/run-2026-01-02.log" \
  "$RT_ROOT/incident-notes.txt" "$RT_ROOT/run-evil.log" "$RT_ROOT/run-2026-01-03.log.gz" \
  "$RT_ROOT/nested/run-2025-12-01.log"
touch -d "10 days ago" "$RT_ROOT/run-2026-08-26.log"
touch "$RT_ROOT/run-2026-09-04.log"
n=$(prune_run_logs "$RT_ROOT" 180 "$RT_LOG")
[ "$n" = "2" ] || { echo "FAIL: prune_run_logs removed $n files (wanted exactly the 2 old run-YYYY-MM-DD.log)" >&2; exit 1; }
for keep in incident-notes.txt run-evil.log run-2026-01-03.log.gz nested/run-2025-12-01.log run-2026-08-26.log run-2026-09-04.log; do
  [ -e "$RT_ROOT/$keep" ] || { echo "FAIL: prune_run_logs deleted protected/unknown file $keep" >&2; exit 1; }
done
[ -e "$RT_ROOT/run-2026-01-01.log" ] && { echo "FAIL: old run log survived retention" >&2; exit 1; }
n=$(prune_run_logs "$RT_ROOT" 180 "$RT_LOG"); [ "$n" = "0" ] || { echo "FAIL: second prune is not idempotent ($n)" >&2; exit 1; }
# Refusals: outside the state dir, and a keep window that would gut the audit trail.
OUT=$(mktemp -d); touch -d "200 days ago" "$OUT/run-2026-01-01.log"
if prune_run_logs "$OUT" 180 "$RT_LOG" >/dev/null; then echo "FAIL: pruned outside \$HOME/.local/state" >&2; exit 1; fi
[ -e "$OUT/run-2026-01-01.log" ] || { echo "FAIL: refused call still deleted" >&2; exit 1; }
rm -rf "$OUT"
touch -d "200 days ago" "$RT_ROOT/run-2026-02-01.log"
if prune_run_logs "$RT_ROOT" 7 "$RT_LOG" >/dev/null; then echo "FAIL: keep_days=7 accepted" >&2; exit 1; fi
[ -e "$RT_ROOT/run-2026-02-01.log" ] || { echo "FAIL: refused keep_days still deleted" >&2; exit 1; }
grep -qF "refused" "$RT_LOG" || { echo "FAIL: refusals are silent" >&2; exit 1; }

# Quarantine is counted, never touched.
QD="$RT_ROOT/quarantine"; mkdir -p "$QD/a" "$QD/b" "$QD/c"; echo x > "$QD/a/post.md"
: > "$RT_LOG"
if quarantine_census "$QD" 2 "$RT_LOG"; then echo "FAIL: 3 entries over a 2-entry line did not warn" >&2; exit 1; fi
[ "$QUARANTINE_COUNT" = "3" ] || { echo "FAIL: QUARANTINE_COUNT=$QUARANTINE_COUNT" >&2; exit 1; }
grep -qF "WARN: quarantine holds 3 entries" "$RT_LOG" || { echo "FAIL: census warning text" >&2; exit 1; }
if ! { [ -f "$QD/a/post.md" ] && [ -d "$QD/c" ]; }; then echo "FAIL: census deleted quarantine content" >&2; exit 1; fi
quarantine_census "$QD" 3 "$RT_LOG" || { echo "FAIL: at the line must be ok" >&2; exit 1; }
quarantine_census "$RT_ROOT/no-such-dir" 1 "$RT_LOG" || { echo "FAIL: missing quarantine dir must be ok" >&2; exit 1; }
echo "retention invariant tests: pass"

# ── Recovery invariants: exact date, idempotent rerun, partial state, ledger ──
# The recovery contract for a missed day (runbook 000-docs/004): the same
# wrapper with --date runs the same gates; a tracked+clean post makes the rerun
# a no-op; untracked producer debris is refused, never treated as published;
# and the ledger ends with exactly one entry for the day.
RC_REPO=$(mktemp -d); trap 'rm -rf "$TEST_REPO" "$RT_ROOT" "$RT_LOG" "$RC_REPO"' EXIT
mkdir -p "$RC_REPO/content/posts"; git -C "$RC_REPO" init -q
git -C "$RC_REPO" config user.name t; git -C "$RC_REPO" config user.email t@example.invalid
printf '%s\n' '+++' "title = 'Landed'" "date = 2026-09-04T07:00:00-06:00" '+++' > "$RC_REPO/content/posts/landed.md"
git -C "$RC_REPO" add -A; git -C "$RC_REPO" commit -qm landed
# 1. exact-date idempotency: the day is covered, a rerun must find it and stop.
published_post_for_date "$RC_REPO" "$RC_REPO/content/posts" 2026-09-04 >/dev/null \
  || { echo "FAIL: landed post not recognised on rerun" >&2; exit 1; }
# 2. a different day is not covered by it (no cross-date leakage).
if published_post_for_date "$RC_REPO" "$RC_REPO/content/posts" 2026-09-03 >/dev/null; then
  echo "FAIL: 2026-09-04 post satisfied a 2026-09-03 query" >&2; exit 1; fi
# 3. partial prior state: an untracked post for the missed day is debris, not a publication.
printf '%s\n' '+++' "title = 'Half'" "date = 2026-09-03T07:00:00-06:00" '+++' > "$RC_REPO/content/posts/half.md"
post_exists_for_date "$RC_REPO/content/posts" 2026-09-03 >/dev/null || { echo "FAIL: debris not detected" >&2; exit 1; }
if published_post_for_date "$RC_REPO" "$RC_REPO/content/posts" 2026-09-03 >/dev/null; then
  echo "FAIL: untracked debris counted as published" >&2; exit 1; fi
# 4. ledger: exactly one entry per recovered day; duplicates and gaps are visible.
LEDGER="$RC_REPO/.blog-syndication-ledger.json"
jq -nc '[{date:"2026-09-03",slug:"a"},{date:"2026-09-04",slug:"b"}]' > "$LEDGER"
[ "$(ledger_entries_for_date "$LEDGER" 2026-09-04)" = "1" ] || { echo "FAIL: ledger count for a landed day" >&2; exit 1; }
[ "$(ledger_entries_for_date "$LEDGER" 2026-09-02)" = "0" ] || { echo "FAIL: ledger count for a missing day" >&2; exit 1; }
jq -nc '[{date:"2026-09-04",slug:"b"},{date:"2026-09-04",slug:"b"}]' > "$LEDGER"
[ "$(ledger_entries_for_date "$LEDGER" 2026-09-04)" = "2" ] || { echo "FAIL: duplicate ledger entries not counted" >&2; exit 1; }
[ "$(ledger_entries_for_date "$RC_REPO/missing.json" 2026-09-04)" = "0" ] || { echo "FAIL: missing ledger" >&2; exit 1; }
echo "recovery invariant tests: pass"
