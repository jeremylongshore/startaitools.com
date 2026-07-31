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
