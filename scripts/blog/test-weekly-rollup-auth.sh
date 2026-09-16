#!/usr/bin/env bash
# Offline reproduction of expired interactive OAuth. All mail, ledger, and alert
# paths are replaced inside a disposable copy of the wrapper.
set -euo pipefail

SOURCE="${1:-$(dirname "$0")/blog-team-rollup.sh}"
EXPECTED="${2:-success}"
TEST_ROOT=$(mktemp -d)
trap 'rm -rf "$TEST_ROOT"' EXIT
mkdir -p "$TEST_ROOT/bin" "$TEST_ROOT/state" "$TEST_ROOT/blog"
cp -f "$SOURCE" "$TEST_ROOT/blog-team-rollup.sh"
cat > "$TEST_ROOT/lib-cron-common.sh" <<'COMMON'
cron_fail() { :; }
liveness_markers() { :; }
count_consecutive_failures() { printf '0'; }
COMMON
cat > "$TEST_ROOT/bin/claude" <<'AGENT'
#!/usr/bin/env bash
set -euo pipefail
if [ "${ANTHROPIC_BASE_URL:-}" != https://api.minimax.io/anthropic ] ||
   [ "${ANTHROPIC_API_KEY:-}" != synthetic-test-key ]; then
  printf '%s\n' 'Failed to authenticate: OAuth session expired and could not be refreshed' >&2
  exit 1
fi
if [ "${1:-}" != -p ]; then exit 2; fi
REPORT=$(printf '%s' "$2" | grep -oE '/tmp/[^[:space:]]+\.html' | head -n 1)
[ -n "$REPORT" ] || exit 3
printf '<div>%0500d</div>\n' 0 > "$REPORT"
AGENT
cat > "$TEST_ROOT/bin/node" <<'MAIL'
#!/usr/bin/env bash
printf '%s\n' 'mail intercepted' >> "$TEST_ROOT/mail-calls"
MAIL
chmod 700 "$TEST_ROOT/bin/claude" "$TEST_ROOT/bin/node"
python3 - "$TEST_ROOT/blog-team-rollup.sh" "$TEST_ROOT" <<'SANITIZE'
from pathlib import Path
import sys
path, root = Path(sys.argv[1]), sys.argv[2]
text = path.read_text()
text = text.replace('LOG_DIR=/home/jeremy/.local/state/blog-team-rollup', f'LOG_DIR={root}/state')
text = text.replace('EMAIL_SCRIPT=/home/jeremy/.claude/skills/email/scripts/send-email.cjs', f'EMAIL_SCRIPT={root}/mail.js')
text = text.replace('BLOG_DIR=/home/jeremy/000-projects/blog/startaitools', f'BLOG_DIR={root}/blog')
text = text.replace('INTENT_MAIL_ENV=/home/jeremy/000-projects/intent-mail/.env', f'INTENT_MAIL_ENV={root}/missing.env')
path.write_text(text)
SANITIZE

run_case() {
  local key="$1" rc=0
  env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL \
    HOME="$TEST_ROOT" PATH="$TEST_ROOT/bin:/usr/bin:/bin" \
    TEST_ROOT="$TEST_ROOT" MINIMAX_API_KEY="$key" \
    ROLLUP_AGENT_BIN="$TEST_ROOT/bin/claude" ROLLUP_BLOG_DIR="$TEST_ROOT/blog" \
    ROLLUP_EMAIL_SCRIPT="$TEST_ROOT/mail.js" ROLLUP_LOG_DIR="$TEST_ROOT/state" \
    ROLLUP_DRY_RUN=1 ROLLUP_TIMEOUT=20 \
    bash "$TEST_ROOT/blog-team-rollup.sh" > "$TEST_ROOT/stdout" 2>&1 || rc=$?
  printf '%s' "$rc"
}

RC=$(run_case synthetic-test-key)
if [ "$EXPECTED" = success ]; then
  [ "$RC" = 0 ] || { cat "$TEST_ROOT/stdout"; exit 1; }
  [ -s "$TEST_ROOT/state/dryrun-$(date +%F).html" ] || exit 1
  [ ! -e "$TEST_ROOT/mail-calls" ] || { printf '%s\n' 'dry run attempted mail' >&2; exit 1; }
  rm -f "$TEST_ROOT/state/dryrun-$(date +%F).html"
  RC=$(run_case '')
  [ "$RC" != 0 ] || { printf '%s\n' 'missing key was accepted' >&2; exit 1; }
  [ ! -e "$TEST_ROOT/mail-calls" ] || { printf '%s\n' 'missing-key dry run attempted mail' >&2; exit 1; }
  printf '%s\n' 'weekly rollup auth regression: static key succeeds, missing key fails, no mail sent'
elif [ "$EXPECTED" = failure ]; then
  [ "$RC" != 0 ] || { printf '%s\n' 'old OAuth path unexpectedly succeeded' >&2; exit 1; }
  grep -q 'OAuth session expired' "$TEST_ROOT/state/run-$(date +%F).log" || exit 1
  printf '%s\n' 'old weekly rollup: expired OAuth reproduced'
else
  printf '%s\n' 'Expected success or failure' >&2
  exit 2
fi
