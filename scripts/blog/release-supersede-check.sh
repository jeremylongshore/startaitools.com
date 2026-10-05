#!/usr/bin/env bash
# Classify a Release (or deploy) run against the live tip of master.
#
# Usage: release-supersede-check.sh <base-sha> [remote] [branch]
#
# Fetches <remote>/<branch> and compares it with <base-sha> (the commit the run
# built on: GITHUB_SHA for a release, the released commit for a deploy check).
# Prints key=value lines on stdout:
#
#   state=current     the tip IS <base-sha>; the run may publish
#   state=resume      the tip is <base-sha> plus only generated release commits
#                     (a retry of the run that already released); the existing
#                     reconcile logic decides what, if anything, to resume
#   state=superseded  a newer source commit reached the tip; its own Release run
#                     (serialised behind this one) releases everything, so this
#                     run must publish nothing and exit cleanly
#   tip=<sha>         the fetched tip
#   newer=<sha>       (superseded only) the newest non-release commit
#
# Exit codes: 0 classified; 1 usage/fetch error; 2 the tip does not descend from
# <base-sha> (history rewritten: never paper over that); 3 every newer source
# commit carries a CI-skip marker, so no later Release run will hand off and
# this must stay a visible failure.

set -euo pipefail

BASE=${1:?usage: release-supersede-check.sh <base-sha> [remote] [branch]}
REMOTE=${2:-origin}
BRANCH=${3:-master}

BOT='github-actions[bot]|41898282+github-actions[bot]@users.noreply.github.com'
RELEASE_SUBJECT='^(chore: release|docs: update changelog for) v[0-9]+\.[0-9]+\.[0-9]+ \[skip ci\]$'
SKIP_MARKER='\[(skip ci|ci skip|no ci|skip actions|actions skip)\]'

BASE=$(git rev-parse --verify "${BASE}^{commit}")
git fetch --quiet --no-tags "$REMOTE" "+refs/heads/$BRANCH:refs/remotes/$REMOTE/$BRANCH"
TIP=$(git rev-parse --verify "refs/remotes/$REMOTE/$BRANCH^{commit}")
echo "tip=$TIP"

if [ "$TIP" = "$BASE" ]; then
  echo "state=current"
  exit 0
fi

if ! git merge-base --is-ancestor "$BASE" "$TIP"; then
  echo "$REMOTE/$BRANCH ($TIP) does not descend from $BASE; refusing to classify" >&2
  exit 2
fi

NEWER=""
while IFS= read -r COMMIT; do
  IDENTITY=$(git show -s --format='%an|%ae' "$COMMIT")
  SUBJECT=$(git show -s --format=%s "$COMMIT")
  if [ "$IDENTITY" = "$BOT" ] && [[ "$SUBJECT" =~ $RELEASE_SUBJECT ]]; then
    continue
  fi
  NEWER=$COMMIT
  break
done < <(git rev-list "$BASE..$TIP")

if [ -z "$NEWER" ]; then
  echo "state=resume"
  exit 0
fi

MESSAGE=$(git show -s --format=%B "$NEWER")
if printf '%s\n' "$MESSAGE" | grep -Eiq "$SKIP_MARKER"; then
  echo "newest source commit $NEWER carries a CI-skip marker; no later Release run will release it" >&2
  exit 3
fi

echo "state=superseded"
echo "newer=$NEWER"
