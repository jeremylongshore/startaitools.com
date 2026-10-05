#!/usr/bin/env bash
# Replay of near-simultaneous merges against the real release publish scripts.
#
# A bare repository stands in for GitHub. Each "run" clones it, checks out its
# triggering commit detached (as actions/checkout does for GITHUB_SHA), adds
# the same two generated release commits the Release workflow makes, and calls
# release-publish-refs.sh. Runs execute one after another, as the workflow
# concurrency group serialises them.

set -euo pipefail

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PUBLISH="$HERE/release-publish-refs.sh"
CHECK="$HERE/release-supersede-check.sh"
SANDBOX=$(mktemp -d)
trap 'rm -rf "$SANDBOX"' EXIT
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
BOT_NAME='github-actions[bot]'
BOT_EMAIL='41898282+github-actions[bot]@users.noreply.github.com'
PASS=0

fail() { echo "FAIL: $*" >&2; exit 1; }
ok() { PASS=$((PASS + 1)); echo "ok - $*"; }
remote_tip() { git -C "$REMOTE" rev-parse refs/heads/master; }
remote_tags() { git -C "$REMOTE" tag --list 'v*' --sort=v:refname | tr '\n' ' '; }

reset_remote() {
  rm -rf "${SANDBOX:?}"/*
  REMOTE="$SANDBOX/remote.git"
  git init -q --bare -b master "$REMOTE"
  DEV="$SANDBOX/dev"
  git clone -q "$REMOTE" "$DEV" 2>/dev/null
  git -C "$DEV" config user.name dev
  git -C "$DEV" config user.email dev@example.invalid
  echo 1.0.0 > "$DEV/version.txt"
  printf '# Release v1.0.0\n' > "$DEV/CHANGELOG.md"
  git -C "$DEV" add -A
  git -C "$DEV" commit -qm "seed"
  git -C "$DEV" tag -a v1.0.0 -m "Release v1.0.0"
  git -C "$DEV" push -q origin master v1.0.0
}

# merge <name>: land a source commit on master (a PR merge), print its sha.
merge() {
  git -C "$DEV" pull -q --ff-only origin master
  echo "$1" > "$DEV/$1.md"
  git -C "$DEV" add "$1.md"
  git -C "$DEV" commit -qm "Merge pull request: $1"
  git -C "$DEV" push -q origin master
  git -C "$DEV" rev-parse HEAD
}

# prepare_run <dir> <sha> <tag>: a release job's checkout plus generated commits.
prepare_run() {
  local dir=$1 sha=$2 tag=$3
  git clone -q "$REMOTE" "$dir" 2>/dev/null
  git -C "$dir" config user.name "$BOT_NAME"
  git -C "$dir" config user.email "$BOT_EMAIL"
  git -C "$dir" checkout -q --detach "$sha"
  echo "${tag#v}" > "$dir/version.txt"
  git -C "$dir" commit -qam "chore: release $tag [skip ci]"
  printf '# Release %s\n' "$tag" > "$dir/CHANGELOG.md"
  git -C "$dir" commit -qam "docs: update changelog for $tag [skip ci]"
}

# publish <dir> <sha> <tag>: run the real publish script; capture stdout+status.
publish() {
  local rc=0
  OUT=$(cd "$1" && "$PUBLISH" "$2" "$3" 2>"$SANDBOX/stderr") || rc=$?
  RC=$rc
  ERR=$(cat "$SANDBOX/stderr")
  printf '%s\n' "$ERR" >&2
}

contains() { git -C "$REMOTE" merge-base --is-ancestor "$1" "$2"; }

# 1. Two merges land before either Release run starts (runs 37273975009 /
#    37274788846 shape). The older run is superseded; the newer releases both.
reset_remote
A=$(merge a)
B=$(merge b)
prepare_run "$SANDBOX/run-a" "$A" v1.0.1
publish "$SANDBOX/run-a" "$A" v1.0.1
[ "$RC" -eq 0 ] || fail "superseded run exited $RC"
grep -qx 'superseded=true' <<<"$OUT" || fail "older run not reported superseded: $OUT"
grep -qx "superseded-by=$B" <<<"$OUT" || fail "superseded-by not the newer merge: $OUT"
[ "$(remote_tags)" = "v1.0.0 " ] || fail "superseded run created a tag: $(remote_tags)"
[ -z "$(git -C "$SANDBOX/run-a" tag --list v1.0.1)" ] || fail "superseded run left a local tag"
[ "$(remote_tip)" = "$B" ] || fail "superseded run moved master"
ok "older run exits 0 as superseded by the newer merge and creates no tag"
prepare_run "$SANDBOX/run-b" "$B" v1.0.1
publish "$SANDBOX/run-b" "$B" v1.0.1
if ! { [ "$RC" -eq 0 ] && grep -qx 'published=true' <<<"$OUT"; }; then fail "newer run did not publish ($RC): $OUT"; fi
REL=$(git -C "$REMOTE" rev-parse 'v1.0.1^{commit}')
[ "$REL" = "$(remote_tip)" ] || fail "tag does not point at released master"
if ! { contains "$A" "$REL" && contains "$B" "$REL"; }; then fail "release does not contain both merges"; fi
[ "$(remote_tags)" = "v1.0.0 v1.0.1 " ] || fail "unexpected tags: $(remote_tags)"
ok "newer run publishes one release (v1.0.1) containing both merges"

# 2. The newer merge lands while the older run is already past its early
#    checks: the pre-tag check catches it (no tag is ever created).
reset_remote
A=$(merge a)
prepare_run "$SANDBOX/run-a" "$A" v1.0.1
EARLY=$(cd "$SANDBOX/run-a" && "$CHECK" "$A" | sed -n 's/^state=//p')
[ "$EARLY" = current ] || fail "early check before the newer merge was '$EARLY'"
B=$(merge b)
publish "$SANDBOX/run-a" "$A" v1.0.1
if ! { [ "$RC" -eq 0 ] && grep -qx 'superseded=true' <<<"$OUT"; }; then fail "late merge not superseded ($RC): $OUT"; fi
[ "$(remote_tags)" = "v1.0.0 " ] || fail "late-superseded run created a tag"
if grep -q 'rejected' <<<"$ERR"; then fail "pre-tag check missed the newer merge; push was attempted"; fi
ok "a merge landing after the early checks is caught before tagging"

# 3. The newer merge lands between the pre-tag check and the push (the narrow
#    window). A pre-push hook lands it, so the atomic push is refused for real.
reset_remote
A=$(merge a)
prepare_run "$SANDBOX/run-a" "$A" v1.0.1
mkdir -p "$SANDBOX/run-a/.git/hooks"
cat > "$SANDBOX/run-a/.git/hooks/pre-push" <<HOOK
#!/usr/bin/env bash
cd "$DEV" && git pull -q --ff-only origin master && echo late > late.md \
  && git add late.md && git commit -qm "Merge pull request: late" && git push -q origin master
HOOK
chmod +x "$SANDBOX/run-a/.git/hooks/pre-push"
publish "$SANDBOX/run-a" "$A" v1.0.1
LATE=$(remote_tip)
if ! { [ "$RC" -eq 0 ] && grep -qx "superseded-by=$LATE" <<<"$OUT"; }; then fail "refused push not absorbed ($RC): $OUT"; fi
[ "$(remote_tags)" = "v1.0.0 " ] || fail "refused push left a remote tag"
[ -z "$(git -C "$SANDBOX/run-a" tag --list v1.0.1)" ] || fail "refused push left a local tag"
ok "a merge racing the push itself is absorbed: push refused atomically, run exits 0, no tag"

# 4. A retry of the run that already released is 'resume', never 'superseded'.
reset_remote
A=$(merge a)
prepare_run "$SANDBOX/run-a" "$A" v1.0.1
publish "$SANDBOX/run-a" "$A" v1.0.1
[ "$RC" -eq 0 ] || fail "plain release failed"
git clone -q "$REMOTE" "$SANDBOX/retry" 2>/dev/null
STATE=$(cd "$SANDBOX/retry" && "$CHECK" "$A" | sed -n 's/^state=//p')
[ "$STATE" = resume ] || fail "retry of the releasing run classified '$STATE'"
ok "a retry of the releasing run is classified resume (existing reconcile path)"

# 5. An existing tag is never overwritten (e.g. a dangling tag from an
#    earlier refused publication already holds the computed version).
C=$(merge c)
git -C "$DEV" tag -a v1.0.2 -m "Release v1.0.2" "$A"
git -C "$DEV" push -q origin v1.0.2
TAG_OBJ=$(git -C "$REMOTE" rev-parse refs/tags/v1.0.2)
prepare_run "$SANDBOX/run-dup" "$C" v1.0.2
git -C "$SANDBOX/run-dup" tag -d v1.0.2 >/dev/null
publish "$SANDBOX/run-dup" "$C" v1.0.2
[ "$RC" -ne 0 ] || fail "duplicate tag publication exited 0"
[ "$(git -C "$REMOTE" rev-parse refs/tags/v1.0.2)" = "$TAG_OBJ" ] || fail "existing tag was replaced"
[ "$(remote_tip)" = "$C" ] || fail "refused duplicate publication moved master"
ok "an existing tag is refused, never replaced"

# 6. Rewritten history (tip not descended from the run's commit) fails loudly.
reset_remote
A=$(merge a)
prepare_run "$SANDBOX/run-a" "$A" v1.0.1
git -C "$DEV" reset -q --hard HEAD~1
echo other > "$DEV/other.md"; git -C "$DEV" add other.md; git -C "$DEV" commit -qm other
git -C "$DEV" push -q -f origin master
publish "$SANDBOX/run-a" "$A" v1.0.1
[ "$RC" -ne 0 ] || fail "non-descendant tip was accepted"
[ "$(remote_tags)" = "v1.0.0 " ] || fail "non-descendant case created a tag"
ok "a rewritten master is a failure, not a supersede"

# 7. A newer commit that carries a CI-skip marker cannot hand off: stay red.
reset_remote
A=$(merge a)
prepare_run "$SANDBOX/run-a" "$A" v1.0.1
git -C "$DEV" pull -q --ff-only origin master
echo s > "$DEV/s.md"; git -C "$DEV" add s.md; git -C "$DEV" commit -qm "docs: tweak [skip ci]"
git -C "$DEV" push -q origin master
publish "$SANDBOX/run-a" "$A" v1.0.1
[ "$RC" -ne 0 ] || fail "skip-marked newer commit was treated as a hand-off"
ok "a newer skip-marked commit keeps the run a visible failure"

echo "PASS: $PASS release supersede cases"
