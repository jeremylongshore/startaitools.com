#!/usr/bin/env bash
# Publish a prepared release (HEAD = generated release commits on <base-sha>)
# as one atomic push of master plus a new annotated tag.
#
# Usage: release-publish-refs.sh <base-sha> <tag> [remote] [branch]
#
# Prints key=value lines on stdout: published=true, or superseded=true with
# superseded-by=<sha>. A superseded run creates no tag (local or remote) and
# exits 0: the newer commit's own Release run, serialised by the workflow
# concurrency group, releases it together with this run's commit. An existing
# tag is never replaced, and any other refused push stays a failure.

set -euo pipefail

BASE=${1:?usage: release-publish-refs.sh <base-sha> <tag> [remote] [branch]}
TAG=${2:?usage: release-publish-refs.sh <base-sha> <tag> [remote] [branch]}
REMOTE=${3:-origin}
BRANCH=${4:-master}
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

classify() {
  local out
  out=$("$HERE/release-supersede-check.sh" "$BASE" "$REMOTE" "$BRANCH")
  STATE=$(printf '%s\n' "$out" | sed -n 's/^state=//p')
  NEWER=$(printf '%s\n' "$out" | sed -n 's/^newer=//p')
}

superseded() {
  echo "Release superseded by $NEWER: a newer commit reached $BRANCH; its Release run publishes both. No tag created." >&2
  echo "superseded=true"
  echo "superseded-by=$NEWER"
  exit 0
}

[[ "$TAG" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "invalid tag $TAG" >&2; exit 1; }

# Check the live tip before creating anything.
classify
case "$STATE" in
  superseded) superseded ;;
  current) ;;
  *) echo "unexpected pre-publish state '$STATE' for $BASE" >&2; exit 1 ;;
esac

# Never replace an existing tag, locally or on the remote.
if git rev-parse -q --verify "refs/tags/$TAG" >/dev/null \
    || [ -n "$(git ls-remote "$REMOTE" "refs/tags/$TAG")" ]; then
  echo "Release tag $TAG already exists; refusing a conflicting publication" >&2
  exit 1
fi

git tag -a "$TAG" -m "Release $TAG"
if git push --atomic "$REMOTE" "HEAD:refs/heads/$BRANCH" "refs/tags/$TAG:refs/tags/$TAG" >&2; then
  echo "published=true"
  exit 0
fi

# The push was refused. A newer commit landing between the check and the push
# is the only refusal this run may absorb; the atomic push guarantees no ref
# moved, so drop the unpublished local tag and classify again.
git tag -d "$TAG" >/dev/null
if [ -n "$(git ls-remote "$REMOTE" "refs/tags/$TAG")" ]; then
  echo "remote tag $TAG appeared during a refused push; leaving it untouched" >&2
  exit 1
fi
classify
if [ "$STATE" = "superseded" ]; then
  superseded
fi
echo "push refused and $BRANCH was not superseded (state=$STATE)" >&2
exit 1
