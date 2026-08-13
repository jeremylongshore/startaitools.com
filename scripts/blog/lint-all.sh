#!/usr/bin/env bash
# lint-all.sh: run every check `.github/workflows/scripts-lint.yml` runs, locally.
#
# WHY THIS EXISTS
#   On 2026-08-11 three commits were pushed with a failing scripts-lint, each
#   time because the local pre-flight was a REMEMBERED SUBSET of what CI runs:
#   bash -n instead of shellcheck, then shellcheck without ruff, then ruff that
#   was not installed at all and whose absence was mistaken for a pass. The
#   pattern was not carelessness about which commands to type. It was that the
#   real gate lived in a YAML file nobody ran locally, which is the same defect
#   this repo keeps finding elsewhere: a contract with no local enforcement.
#
#   So the gate becomes one command. Run this before every commit that touches
#   scripts/, .claude/skills/*/scripts/, or tests/.
#
#   The globs below are copied from the workflow deliberately. If you change one
#   here, change it there. A drift between them is the failure mode this script
#   exists to prevent, and `--check-drift` asserts they still match.
#
# USAGE
#   scripts/blog/lint-all.sh                # run everything, fail on first error
#   scripts/blog/lint-all.sh --check-drift  # verify the globs still match CI
#
# Requires: shellcheck, ruff (uv tool install ruff), pytest.

set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.." || exit 1
export PATH="$HOME/.local/bin:$PATH"   # uv installs ruff here
shopt -s globstar nullglob

FAILED=0
step() { printf '\n\033[1m== %s\033[0m\n' "$1"; }
ok()   { printf '   \033[32mOK\033[0m %s\n' "$1"; }
bad()  { printf '   \033[31mFAIL\033[0m %s\n' "$1"; FAILED=1; }
missing_tool() {
  printf '   \033[31mMISSING TOOL\033[0m %s — %s\n' "$1" "$2"
  printf '   Treating an absent linter as a FAILURE, not a pass. An uninstalled\n'
  printf '   checker that reports nothing is indistinguishable from a clean run,\n'
  printf '   which is exactly how a ruff violation shipped on 2026-08-11.\n'
  FAILED=1
}

SH_FILES=(scripts/blog/*.sh .claude/skills/blog-*/scripts/*.sh verify_links.sh check_links.sh)
PY_FILES=(scripts/blog/*.py .claude/skills/blog-*/scripts/*.py tests/*.py check-links.py)

if [ "${1:-}" = "--check-drift" ]; then
  WF=.github/workflows/scripts-lint.yml
  for glob in "scripts/blog/*.sh" ".claude/skills/blog-*/scripts/*.sh" \
              "scripts/blog/*.py" ".claude/skills/blog-*/scripts/*.py" "tests/*.py"; do
    if grep -qF -- "$glob" "$WF"; then ok "glob present in CI: $glob"
    else bad "glob NOT in $WF: $glob"; fi
  done
  exit "$FAILED"
fi

step "shellcheck -S style (${#SH_FILES[@]} files)"
if ! command -v shellcheck >/dev/null 2>&1; then
  missing_tool shellcheck "sudo apt-get install shellcheck"
elif shellcheck -S style "${SH_FILES[@]}"; then ok "shell scripts clean"
else bad "shellcheck"; fi

step "ruff check (${#PY_FILES[@]} files)"
if ! command -v ruff >/dev/null 2>&1; then
  missing_tool ruff "uv tool install ruff"
elif ruff check "${PY_FILES[@]}"; then ok "python clean"
else bad "ruff"; fi

step "pipeline invariants"
if bash scripts/blog/test-pipeline-invariants.sh >/dev/null 2>&1; then
  ok "all invariant groups pass"
else
  bad "test-pipeline-invariants.sh (re-run it directly for the failing group)"
fi

step "pytest"
if python3 -m pytest tests/ -q 2>&1 | tail -1; then ok "tests pass"
else bad "pytest"; fi

printf '\n'
if [ "$FAILED" -eq 0 ]; then
  printf '\033[32mALL CHECKS PASS\033[0m — safe to commit.\n'
else
  printf '\033[31mFAILURES ABOVE\033[0m — do not push; CI runs exactly these.\n'
fi
exit "$FAILED"

# canary probe 2026-08-12T20:59:19-06:00: does a pull_request event dispatch scripts-lint?
