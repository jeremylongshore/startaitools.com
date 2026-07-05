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
  # Accept either env name. The canonical var is SLACK_WEBHOOK_CRON, but ~/.env
  # historically carries the value under SLACK_WEBHOOK_CRON_FAILURES (the channel
  # name). Read env first (either name), then ~/.env (either name) — so the
  # existing ~/.env entry activates this without a rename. (WS1 notify fidelity.)
  local hook="${SLACK_WEBHOOK_CRON:-${SLACK_WEBHOOK_CRON_FAILURES:-}}"
  if [ -z "$hook" ] && [ -f "$HOME/.env" ]; then
    hook=$(grep -m1 -E '^SLACK_WEBHOOK_CRON(_FAILURES)?=' "$HOME/.env" 2>/dev/null | cut -d= -f2-)
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

# ─────────────────────────────────────────────────────────────────────────────
# default_branch_of <repo>
#
# Resolves the branch a repo publishes/deploys from, robustly. The old
# reconcile_repo hardcoded a `master` fallback (B-2 bug): claude-code-plugins has
# NO master branch (its default is `main`), so an ff-push to `:master` there
# failed every time. This resolves the true branch per repo:
#   1. local origin/HEAD symref (fast; often unset on these clones)
#   2. self-heal it via `git remote set-head origin -a`, re-read
#   3. `git remote show origin` HEAD branch (authoritative — startaitools→master,
#      ccp→main both resolve correctly here)
#   4. prefer an existing origin/master then origin/main ref
#   5. last resort: the current branch
# Stdout: the branch name.
# ─────────────────────────────────────────────────────────────────────────────
default_branch_of() {
  local repo="$1" db
  db=$(git -C "$repo" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')
  if [ -z "$db" ]; then
    git -C "$repo" remote set-head origin -a >/dev/null 2>&1 || true
    db=$(git -C "$repo" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')
  fi
  if [ -z "$db" ]; then
    db=$(git -C "$repo" remote show origin 2>/dev/null | sed -n 's/.*HEAD branch: //p')
  fi
  if [ -z "$db" ] || [ "$db" = "(unknown)" ]; then
    local c
    for c in master main; do
      git -C "$repo" show-ref --verify --quiet "refs/remotes/origin/$c" && { db="$c"; break; }
    done
  fi
  [ -z "$db" ] && db=$(git -C "$repo" rev-parse --abbrev-ref HEAD 2>/dev/null)
  echo "$db"
}

# ─────────────────────────────────────────────────────────────────────────────
# post_exists_for_date <posts_dir> <YYYY-MM-DD>
#
# The single canonical "does a post already exist for this date" check. Matches
# the post's front-matter `date` in ALL forms the pipeline emits:
#   TOML unquoted:  date = 2026-07-02T08:00:00-05:00   (archetype default)
#   TOML single:    date = '2026-07-02'
#   TOML double:    date = "2026-07-02"
#   YAML:           date: 2026-07-02  /  date: "2026-07-02"
# The D-1 bug lived in blog-backfill-daily.sh:54, which omitted the unquoted TOML
# case and so regenerated a DUPLICATE for any date whose post used the archetype
# default. Centralizing here means one regex, every caller.
# Stdout: matching file path(s). Return: 0 if a post exists, 1 if none.
# ─────────────────────────────────────────────────────────────────────────────
post_exists_for_date() {
  local posts_dir="$1" d="$2" hit
  hit=$(grep -rlE "^date = ['\"]?${d}|^date: ['\"]?${d}" "$posts_dir" 2>/dev/null | head -1)
  [ -n "$hit" ] && { echo "$hit"; return 0; }
  return 1
}

# ─────────────────────────────────────────────────────────────────────────────
# disk_guard <path> <min_free_mb> <log_file>
#
# Refuses to proceed when the filesystem holding <path> has less than
# <min_free_mb> MiB free. A wedged disk turns `git commit`/`hugo build` into
# half-written corruption; failing fast + loud is safer than landing garbage.
# Return: 0 ok, 1 under threshold.
# ─────────────────────────────────────────────────────────────────────────────
disk_guard() {
  local path="$1" min_mb="$2" log_file="$3" avail_mb
  avail_mb=$(df -Pm "$path" 2>/dev/null | awk 'NR==2 {print $4}')
  if [ -z "$avail_mb" ]; then
    _log "$log_file" "WARN: disk_guard could not read free space for $path — continuing"
    return 0
  fi
  if [ "$avail_mb" -lt "$min_mb" ]; then
    _log "$log_file" "FATAL: only ${avail_mb}MiB free on $(df -Pm "$path" | awk 'NR==2{print $6}') (need ${min_mb}MiB) — refusing to run"
    return 1
  fi
  return 0
}

# ─────────────────────────────────────────────────────────────────────────────
# remote_live_check <url> <max_secs> <log_file>
#
# Polls <url> with `curl -sf` until it returns 2xx or <max_secs> elapse. This is
# the STATUS=OK gate for the land step: it catches a non-fast-forward push, a
# remote/DNS outage, AND a failed Netlify build in one probe — a bare `git push`
# exit-0 proves none of those. Netlify's build lag is why we poll rather than
# probe once. Return: 0 live, 1 not live within budget.
# ─────────────────────────────────────────────────────────────────────────────
remote_live_check() {
  local url="$1" max_secs="$2" log_file="$3"
  local waited=0 interval=15
  command -v curl >/dev/null 2>&1 || { _log "$log_file" "WARN: curl absent — skipping liveness check"; return 0; }
  while [ "$waited" -lt "$max_secs" ]; do
    if curl -sfL --max-time 20 -o /dev/null "$url" 2>/dev/null; then
      _log "$log_file" "Liveness OK: $url (after ${waited}s)"
      return 0
    fi
    sleep "$interval"
    waited=$((waited + interval))
  done
  _log "$log_file" "Liveness FAILED: $url not 2xx within ${max_secs}s"
  return 1
}

# ─────────────────────────────────────────────────────────────────────────────
# validate_json <file>
#
# True (0) iff <file> is parseable JSON. Guards the gitignored
# .crosspost-queue.json against the half-written-file corruption that a crashed
# mid-write leaves behind. Return: 0 valid, 1 invalid/missing/no-jq.
# ─────────────────────────────────────────────────────────────────────────────
validate_json() {
  local f="$1"
  [ -f "$f" ] || return 1
  command -v jq >/dev/null 2>&1 || return 1
  jq -e . "$f" >/dev/null 2>&1
}

# ─────────────────────────────────────────────────────────────────────────────
# atomic_json_write <target_file>   (JSON content on stdin)
#
# Validates stdin as JSON, writes it to a temp file in the same directory, then
# atomically renames over <target_file>. A crash mid-write leaves the old file
# intact instead of a truncated one. Return: 0 written, 1 invalid JSON.
# ─────────────────────────────────────────────────────────────────────────────
atomic_json_write() {
  local target="$1" tmp
  tmp=$(mktemp "$(dirname "$target")/.$(basename "$target").XXXXXX") || return 1
  cat > "$tmp"
  if command -v jq >/dev/null 2>&1 && ! jq -e . "$tmp" >/dev/null 2>&1; then
    rm -f "$tmp"
    return 1
  fi
  mv -f "$tmp" "$target"
}

# ─────────────────────────────────────────────────────────────────────────────
# reconcile_repo <repo> <label> <log_file> [<branch>]
#
# Moved here from blog-backfill-daily.sh + blog-monthly-retro.sh (they carried
# drifting copies). If a run defensively committed to a feature branch, try a
# fast-forward push of that branch tip onto the repo's deploy branch. Uses
# default_branch_of (B-2 fix) unless an explicit <branch> is given.
# Appends a human line to the caller-global RECONCILED. Never exits the caller.
# ─────────────────────────────────────────────────────────────────────────────
reconcile_repo() {
  local repo="$1" label="$2" log_file="$3" branch="${4:-}"
  [ -d "$repo/.git" ] || return 0
  cd "$repo" || return 1
  local current default sha
  current=$(git rev-parse --abbrev-ref HEAD 2>/dev/null) || return 1
  default="${branch:-$(default_branch_of "$repo")}"
  default="${default:-master}"
  if [ "$current" = "$default" ]; then
    RECONCILED="${RECONCILED}${label}: on $default ✓\n"
    return 0
  fi
  if [ -z "$(git log "origin/$default..$current" --oneline 2>/dev/null)" ]; then
    RECONCILED="${RECONCILED}${label}: $current has no commits ahead of origin/$default ✓\n"
    return 0
  fi
  if git push origin "$current:$default" >> "$log_file" 2>&1; then
    sha=$(git rev-parse --short HEAD)
    _log "$log_file" "✓ FF-pushed $label: $current → origin/$default ($sha)"
    RECONCILED="${RECONCILED}${label}: ✓ auto-merged $current → origin/$default ($sha)\n"
  else
    _log "$log_file" "✗ FF-push failed for $label ($current → origin/$default) — manual merge required"
    RECONCILED="${RECONCILED}${label}: ⚠ ORPHANED on $current — needs manual merge\n"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# acquire_pipeline_lock <lockfile> <log_file>
#
# Non-blocking flock on fd 9, held for the life of the process. Serializes the
# daily cron against a hand-run `/blog-backfill` (or a second cron) so two
# generators never race on the same working tree. The daily wrapper acquires it
# and exports BLOG_PIPELINE_LOCK_HELD=1 so a child blog-land.sh does NOT try to
# re-lock the same file (which would self-deadlock the non-blocking attempt).
# Return: 0 acquired, 2 already held (benign — caller should exit 0), 1 error.
# ─────────────────────────────────────────────────────────────────────────────
acquire_pipeline_lock() {
  local lockfile="$1" log_file="$2"
  command -v flock >/dev/null 2>&1 || { _log "$log_file" "WARN: flock absent — running without a lock"; return 0; }
  exec 9>"$lockfile" || { _log "$log_file" "FATAL: cannot open lock $lockfile"; return 1; }
  if ! flock -n 9; then
    _log "$log_file" "LOCKED: another blog pipeline run holds $lockfile — exiting to avoid a concurrent-run race"
    return 2
  fi
  return 0
}
