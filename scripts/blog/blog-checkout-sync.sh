#!/usr/bin/env bash
# blog-checkout-sync.sh — daily fast-forward of the cron execution surface.
#
# Host cron runs scripts/blog/*.sh straight from the primary checkout, and until
# this job existed nothing moved that checkout: a merged script fix was not live
# for cron until someone pulled by hand (62 commits behind on 2026-11-23). This
# job fast-forwards the checkout to origin's default branch once a day, just
# before the 04:00 producer.
#
# It only ever fast-forwards. It never switches branch, stashes, resets, rebases
# or commits, and it never touches a dirty file: git refuses a fast-forward that
# would overwrite one, and that refusal is reported, not worked around.
#
# Outcomes:
#   exit 0  already current, fast-forwarded, or skipped because a pipeline run
#           holds the lock (scripts are never swapped under a running job)
#   exit 1  REFUSED — wrong branch, local commits origin lacks, fetch failure, or
#           a fast-forward git would not do. Alerts Buzz sys-automation; no .ok.
#
# Backstop: host-drift-check.py reports a checkout that stays behind origin for
# longer than a day, so a dead or permanently-refusing sync still surfaces.
#
# Schedule: daily 03:45 local (scripts/blog/host/blog-cron.manifest).

set -uo pipefail
export PATH="$HOME/bin:$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin"

JOB="blog-checkout-sync"
# Liveness beat before anything can fail (lib-independent on purpose).
mkdir -p "$HOME/.local/state/intent-os/liveness" 2>/dev/null || true
: > "$HOME/.local/state/intent-os/liveness/${JOB}.beat" 2>/dev/null || true

# shellcheck source=./lib-cron-common.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib-cron-common.sh"

# The whole body is one function so bash has parsed it before the fast-forward
# replaces this file on disk.
main() {
  local repo log_dir log lock branch current old new rc ahead behind scripts
  repo="${BLOG_CHECKOUT_SYNC_REPO:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
  log_dir="${BLOG_CHECKOUT_SYNC_STATE_DIR:-$HOME/.local/state/$JOB}"
  lock="${BLOG_PIPELINE_LOCK:-/tmp/blog-pipeline.lock}"
  mkdir -p "$log_dir"
  log="$log_dir/sync-$(date +%Y-%m).log"

  refuse() {
    _log "$log" "REFUSED: $*"
    if command -v cron_fail >/dev/null 2>&1; then
      cron_fail "$JOB" "$* — the cron checkout at $repo was NOT updated; cron keeps running the old scripts. Log: $log"
    fi
    exit 1
  }

  acquire_pipeline_lock "$lock" "$log"; rc=$?
  if [ "$rc" -eq 2 ]; then
    _log "$log" "SKIPPED: a pipeline run is in progress; not changing scripts under it"
    exit 0
  fi
  [ "$rc" -eq 0 ] || refuse "could not take the pipeline lock $lock"

  git -C "$repo" rev-parse --git-dir >/dev/null 2>&1 || refuse "$repo is not a git checkout"
  branch=$(default_branch_of "$repo"); branch="${branch:-master}"
  current=$(git -C "$repo" rev-parse --abbrev-ref HEAD 2>/dev/null)
  [ "$current" = "$branch" ] \
    || refuse "checkout is on '$current', not '$branch' (this job never switches branch)"

  git -C "$repo" fetch -q origin "+refs/heads/${branch}:refs/remotes/origin/${branch}" >> "$log" 2>&1 \
    || refuse "git fetch origin $branch failed"

  old=$(git -C "$repo" rev-parse HEAD)
  new=$(git -C "$repo" rev-parse "refs/remotes/origin/${branch}")
  if [ "$old" = "$new" ]; then
    _log "$log" "CURRENT: $branch @ ${old:0:8}"
    exit 0
  fi
  ahead=$(git -C "$repo" rev-list --count "${new}..${old}")
  behind=$(git -C "$repo" rev-list --count "${old}..${new}")
  [ "$ahead" -eq 0 ] \
    || refuse "checkout has $ahead local commit(s) origin/$branch lacks (and is $behind behind); publish or remove them by hand"

  if ! git -C "$repo" -c pull.rebase=false merge --ff-only "refs/remotes/origin/${branch}" >> "$log" 2>&1; then
    refuse "fast-forward of $behind commit(s) to origin/$branch failed: $(tail -n 3 "$log" | tr '\n' ' ' | cut -c1-300)"
  fi

  scripts=$(git -C "$repo" diff --name-only "$old" "$new" -- scripts/blog .claude/skills/blog-backfill/scripts | wc -l)
  _log "$log" "UPDATED: $branch ${old:0:8} -> ${new:0:8} ($behind commit(s), $scripts pipeline file(s) changed)"
  exit 0
}

trap 'liveness_markers "$JOB" "$?"' EXIT
main "$@"
