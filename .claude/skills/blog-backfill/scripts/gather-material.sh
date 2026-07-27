#!/usr/bin/env bash
# gather-material.sh — pre-gather the high-cost Phase-1 signals for /blog-backfill
# in parallel. Phase 1 of the SKILL.md "Gather Source Material" section does this
# inline via sequential `git log` + `bd list` walks across ~40 repos + 9 beads
# workspaces, which the 2026-05-28 23-min transcript decomposed into 2m 10s of
# serial Phase-1 wall time. This script parallelizes the two big serial loops
# (git log walk + beads list walk) using xargs -P so wall time tracks the slowest
# single repo instead of summing across them.
#
# Usage:
#   PREV_DAY=YYYY-MM-DD DAY=YYYY-MM-DD bash gather-material.sh
#   PREV_DAY=2026-05-27 DAY=2026-05-28 bash gather-material.sh > /tmp/gather.log
#
# Output: a single concatenated stream of "=== <repo> ===\n<git log>" + the
# beads history for the day, ready to feed into the SKILL.md Phase 1.
#
# Failure modes:
# - Each child job runs `git -C "$dir" log ...` with stderr suppressed; a
#   permission-denied repo would simply emit empty stdout (skipped).
# - Each `bd list` failure is also silent (best-effort).
# - OOM bound: 16 parallel jobs × ~50MB git process ≈ <1GB. Comfortably below
#   the 4GB default for claude -p child shells.
#
# Knobs:
#   GATHER_PARALLELISM   jobs to run in parallel (default 16)
#   GATHER_PROJECTS_ROOT  dir containing the project repos (default
#                         /home/jeremy/000-projects)
#   BEADS_WORKSPACES     space-separated list of beads workspaces to walk
#                         (default the SKILL.md list)

set -uo pipefail

PARALLELISM="${GATHER_PARALLELISM:-16}"
PROJECTS_ROOT="${GATHER_PROJECTS_ROOT:-/home/jeremy/000-projects}"
BEADS_WORKSPACES="${BEADS_WORKSPACES:-claude-code-plugins git-with-intent irsb irsb/solver irsb/watchtower irsb-monorepo kilo iams/bobs-brain}"

if [ -z "${PREV_DAY:-}" ] || [ -z "${DAY:-}" ]; then
  echo "ERROR: PREV_DAY and DAY env vars are required" >&2
  echo "  example: PREV_DAY=2026-05-27 DAY=2026-05-28 bash $0" >&2
  exit 2
fi

PREV_T="${PREV_DAY}T23:59:59-06:00"
DAY_T="${DAY}T23:59:59-06:00"

# --- Step A: Parallel git log walk across /home/jeremy/000-projects/*/ ---
# Each job: if the dir has .git, dump commits in [PREV_T, DAY_T) prefixed
# by a "=== <repo> ===" header. Empty output (no commits / no .git) is skipped
# by the consumer via the [ -n "$out" ] check.
#
# xargs -P spawns $PARALLELISM concurrent jobs. GNU xargs (default on Linux)
# is portable; BSD xargs on macOS differs but this script only runs on the
# dev box (Linux) per the project layout.
gather_one_repo() {
  local dir="$1"
  local out
  out=$(git -C "$dir" log --oneline --after="$PREV_T" --before="$DAY_T" 2>/dev/null) || return 0
  if [ -n "$out" ]; then
    printf '=== %s ===\n' "$(basename "$dir")"
    printf '%s\n' "$out"
  fi
}
export -f gather_one_repo
export PREV_T DAY_T

# Collect the list of git-bearing top-level dirs under $PROJECTS_ROOT/*/.
# Glob is sh-safe (no nullglob); use find with -maxdepth 1 + -prune to get
# only the top-level children (avoid descending into every repo).
mapfile -t repo_dirs < <(find "$PROJECTS_ROOT" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | sort)

# Filter to those with .git inside. Fast (stat only). Then xargs -P for parallelism.
printf '' > /tmp/gather-git-xargs.stdin
for dir in "${repo_dirs[@]}"; do
  if [ -d "$dir/.git" ]; then
    printf '%s\n' "$dir" >> /tmp/gather-git-xargs.stdin
  fi
done

xargs -a /tmp/gather-git-xargs.stdin -P "$PARALLELISM" -I {} bash -c 'gather_one_repo "$@"' _ {}
rm -f /tmp/gather-git-xargs.stdin

# --- Step B: Parallel beads list walk across configured workspaces ---
# Each workspace has its own .beads/ dir; bd list reads from there. We
# cd into each workspace and run bd list; failures are silenced (best
# effort — a workspace without the right commit context shouldn't fail
# the whole backfill).
gather_one_workspace() {
  local ws="$1"
  local out
  out=$(cd "$PROJECTS_ROOT/$ws" 2>/dev/null && bd list --closed-after "$DAY" --closed-before "${NEXT_DAY:-$DAY}" --all --flat 2>/dev/null) || return 0
  if [ -n "$out" ]; then
    printf '=== beads:%s ===\n' "$ws"
    printf '%s\n' "$out"
  fi
}
export -f gather_one_workspace
export PROJECTS_ROOT DAY NEXT_DAY

printf '' > /tmp/gather-beads-xargs.stdin
for ws in $BEADS_WORKSPACES; do
  printf '%s\n' "$ws" >> /tmp/gather-beads-xargs.stdin
done

xargs -a /tmp/gather-beads-xargs.stdin -P "$PARALLELISM" -I {} bash -c 'gather_one_workspace "$@"' _ {}
rm -f /tmp/gather-beads-xargs.stdin

# Step C (merged PRs) and Step D (PR review bot comments) are already GH
# API calls, not local filesystem walks — they don't parallelize well at the
# shell level (gh rate limits), and the SKILL.md's bullet-list form is the
# natural outer loop. Reference doc doesn't change those steps.
