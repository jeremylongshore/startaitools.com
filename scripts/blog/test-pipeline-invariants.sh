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
