# Shared helpers for blog cron wrappers.
# Sourced by blog-backfill-daily.sh, blog-monthly-retro.sh, blog-monthly-calibrate.sh.
# Intentionally side-effect-free at source time — defines functions only.
#
# Why this exists: three wrappers had three independently-drifting copies of
# the pre-flight + escalation logic. PR #16/#17 only hardened the daily one;
# monthly retro timed out 2026-06-01 with no pty wrap (opaque log), and
# calibrate fired "done" at default priority despite exit-non-zero with a
# 0-byte report. Putting the helpers in one file keeps the three in lock-step.

# ─────────────────────────────────────────────────────────────────────────────
# preflight_branch_normalize
#
# Ensures the cron operates from a clean, up-to-date default-branch worktree.
# Handles the sibling-worktree case: when `master` is held by a sibling
# worktree (typically `.git/beads-worktrees/master`), `git checkout master`
# fails. This function detects that and pivots `cd` into the sibling worktree
# so the cron actually runs from a real default-branch checkout.
#
# Args:
#   $1  blog dir (initial working tree path)
#   $2  log file path (for the wrapper's log() function output)
# Globals it sets in the caller's scope:
#   BLOG_DIR  may be repointed to the sibling worktree path if pivoted
# Returns:
#   0 on success (caller may proceed). exit 1 on FATAL.
# ─────────────────────────────────────────────────────────────────────────────
preflight_branch_normalize() {
  local blog_dir="$1"
  local log_file="$2"
  local default_branch current_branch other_path

  cd "$blog_dir" || { _log "$log_file" "FATAL: cd to $blog_dir failed"; exit 1; }

  default_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
  default_branch="${default_branch:-master}"
  current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)

  # (1) Uncommitted changes are NEVER OK — regardless of branch.
  if [ -n "$(git status --porcelain --untracked-files=no 2>/dev/null)" ]; then
    _log "$log_file" "FATAL: working tree has uncommitted changes on '$current_branch' — refusing to proceed"
    _log "$log_file" "       Resolve manually (commit, stash, or restore) and re-run."
    git status --porcelain --untracked-files=no >> "$log_file" 2>&1
    exit 1
  fi

  # (2) Switch to default branch if needed; handle worktree-conflict by pivot.
  if [ "$current_branch" != "$default_branch" ]; then
    _log "$log_file" "Pre-flight: not on '$default_branch' (currently on '$current_branch')"
    if git checkout "$default_branch" >> "$log_file" 2>&1; then
      _log "$log_file" "Pre-flight: switched to '$default_branch' in main checkout"
    else
      other_path=$(git worktree list --porcelain 2>/dev/null | awk -v b="refs/heads/$default_branch" '
        /^worktree / { wt=$2 }
        $0=="branch "b { print wt; exit }
      ')
      if [ -n "$other_path" ] && [ "$other_path" != "$blog_dir" ]; then
        _log "$log_file" "Pre-flight: '$default_branch' is checked out at $other_path — pivoting cron to that worktree"
        cd "$other_path" || { _log "$log_file" "FATAL: cd to $other_path failed"; exit 1; }
        # shellcheck disable=SC2034 # consumed by caller scripts via source
        BLOG_DIR="$other_path"   # callers may rely on $BLOG_DIR — repoint it
        if [ -n "$(git status --porcelain --untracked-files=no 2>/dev/null)" ]; then
          _log "$log_file" "FATAL: pivoted worktree $other_path has uncommitted changes — refusing to proceed"
          git status --porcelain --untracked-files=no >> "$log_file" 2>&1
          exit 1
        fi
      else
        _log "$log_file" "FATAL: git checkout $default_branch failed and no sibling worktree has it"
        exit 1
      fi
    fi
  fi

  # (3) Always fast-forward — a stale local default branch lands commits on
  #     obsolete state, then ff-push fails non-fast-forward.
  if ! git pull --ff-only origin "$default_branch" >> "$log_file" 2>&1; then
    _log "$log_file" "WARN: git pull --ff-only origin $default_branch failed — continuing with current local state"
  fi

  _log "$log_file" "Pre-flight OK: on $(git rev-parse --abbrev-ref HEAD) @ $(git rev-parse --short HEAD)"
}

# ─────────────────────────────────────────────────────────────────────────────
# count_consecutive_failures
#
# Walks the cron's log directory newest-first and counts how many consecutive
# log files contain a failure marker. Used to fire high-priority escalation
# alerts when the cron has been silently dying for multiple days.
#
# Args:
#   $1  log directory
#   $2  glob pattern for log files (e.g. "run-*.log")
#   $3  egrep pattern matching failure markers (e.g. "FATAL|TIMED OUT|FAILED")
#   $4  max files to look back (e.g. 10)
# Stdout:
#   integer count of consecutive failing log files at the head of mtime order.
#   0 means the most recent run was clean.
# ─────────────────────────────────────────────────────────────────────────────
count_consecutive_failures() {
  local logdir="$1"
  local glob="$2"
  local pattern="$3"
  local max_lookback="$4"
  local n=0
  local f
  # newest-first via find+printf+sort (more robust than ls). max_lookback caps
  # depth so a long history of failures doesn't blow up.
  while IFS= read -r f; do
    if grep -qE "$pattern" "$f" 2>/dev/null; then
      n=$((n + 1))
    else
      break
    fi
  done < <(find "$logdir" -maxdepth 1 -name "$glob" -printf '%T@ %p\n' 2>/dev/null \
           | sort -rn | head -n "$max_lookback" | awk '{print $2}')
  echo "$n"
}

# ─────────────────────────────────────────────────────────────────────────────
# Internal: log helper used by lib functions when the caller's log() isn't
# in scope (sourced lib functions can't see caller-local functions reliably).
# ─────────────────────────────────────────────────────────────────────────────
_log() {
  local log_file="$1"; shift
  echo "[$(date -Is)] $*" | tee -a "$log_file"
}

# ─────────────────────────────────────────────────────────────────────────────
# slack_fail
#
# Posts a one-line failure notice to the #cron-failures Slack channel.
#
# DORMANT until SLACK_WEBHOOK_CRON exists (read from the environment first, else
# a line in ~/.env): with no webhook it returns 0 and does nothing. Wiring this
# into a cron wrapper is therefore a no-op until Jeremy mints the channel + its
# incoming webhook and drops SLACK_WEBHOOK_CRON into ~/.env — at which point the
# call sites below start firing with zero further code change.
#
# Failures-only by design: success and OK-WITH-WARNING stay on email + ntfy so
# #cron-failures carries signal, not routine chatter (mirrors the ntfy-first
# split on the VPS — see intentsolutions-vps-runbook/docs/alert-routing.md).
#
# Never fails the caller: curl/jq errors are swallowed and it always returns 0,
# so a Slack outage can't flip a cron wrapper's exit status.
#
# Args:
#   $1  job name (e.g. "blog-backfill-daily")
#   $2  short one-line message
# ─────────────────────────────────────────────────────────────────────────────
slack_fail() {
  local job="$1"
  local msg="$2"
  local hook="${SLACK_WEBHOOK_CRON:-}"
  if [ -z "$hook" ] && [ -f "$HOME/.env" ]; then
    hook=$(grep -m1 '^SLACK_WEBHOOK_CRON=' "$HOME/.env" 2>/dev/null | cut -d= -f2-)
  fi
  [ -z "$hook" ] && return 0   # dormant until the channel + webhook exist
  command -v curl >/dev/null 2>&1 || return 0
  local text=":rotating_light: *cron-failures* — \`${job}\`: ${msg}"
  local payload
  if command -v jq >/dev/null 2>&1; then
    payload=$(jq -n --arg t "$text" '{text:$t}')
  else
    # jq-less fallback: escape backslash then double-quote for valid JSON.
    local esc=${text//\\/\\\\}; esc=${esc//\"/\\\"}
    payload="{\"text\":\"${esc}\"}"
  fi
  curl -sS --max-time 10 -X POST -H 'Content-type: application/json' \
    --data "$payload" "$hook" >/dev/null 2>&1 || true
  return 0
}
