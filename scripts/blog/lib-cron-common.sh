# Shared helpers for blog cron wrappers.
# Sourced by blog-backfill-daily.sh, blog-monthly-retro.sh, blog-monthly-calibrate.sh.
# Intentionally side-effect-free at source time — defines functions only.
#
# Why this exists: three wrappers had three independently-drifting copies of
# the pre-flight + escalation logic. PR #16/#17 only hardened the daily one;
# monthly retro timed out 2026-06-01 with no pty wrap (opaque log), and
# calibrate fired "done" at default priority despite exit-non-zero with a
# 0-byte report. Putting the helpers in one file keeps the three in lock-step.

# Delivery is owned by Intent OS's governed Buzz runtime. The blog fleet no
# longer reads a webhook or talks to Slack/ntfy directly.
INTENT_RUNTIME="${INTENT_RUNTIME:-$HOME/bin/lib/intent-runtime.sh}"
if [ -r "$INTENT_RUNTIME" ]; then
  # shellcheck disable=SC1090
  . "$INTENT_RUNTIME" 2>/dev/null || true
fi

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
  local default_branch current_branch other_path beads_dirty=0

  cd "$blog_dir" || { _log "$log_file" "FATAL: cd to $blog_dir failed"; exit 1; }

  default_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
  default_branch="${default_branch:-master}"
  current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)

  # (1) Uncommitted changes only matter when they touch what the pipeline WRITES.
  #
  # ROOT-CAUSE FIX (2026-08-29). The producer + lander write to exactly four
  # places: content/posts/, .blog-staging/, decisions.jsonl, and the lander's
  # image assets under static/images/posts/. Uncommitted changes there ARE
  # dangerous — a half-written post or a mid-edit audit log could corrupt or
  # mislabel a run, so those still FATAL.
  #
  # Uncommitted changes ANYWHERE ELSE are none of the pipeline's business. A
  # 000-docs reference someone edited, a draft, an unrelated file — the producer
  # never reads or writes them, so they cannot collide. The old rule FATAL'd on
  # ALL dirt, which is why a forgotten doc edit bricked the 04:00 run three times
  # (persona files 2026-08-13, image race 2026-08-18, promotion reference
  # 2026-08-29). We now leave that dirt exactly where it is and run. Nothing is
  # stashed, moved, or committed on anyone's behalf: the pipeline simply stops
  # caring about dirt outside its own lane. The .beads/interactions.jsonl
  # carve-out (an append-only log any `bd close` dirties) is subsumed by this —
  # it is outside the write-set, so it was always benign.
  _porcelain=$(git status --porcelain --untracked-files=no 2>/dev/null || true)
  if [ -n "$_porcelain" ]; then
    _dangerous=$(printf '%s\n' "$_porcelain" | grep -E '^.. (content/posts/|\.blog-staging/|static/images/posts/|\.claude/skills/blog-backfill/methodology/decisions\.jsonl)' || true)
    if [ -n "$_dangerous" ]; then
      _log "$log_file" "FATAL: uncommitted changes to the pipeline's own files on '$current_branch' — refusing to proceed"
      _log "$log_file" "       These paths are what the producer writes; a half-finished post or edit here is unsafe to build on. Resolve and re-run:"
      printf '%s\n' "$_dangerous" >> "$log_file" 2>&1
      exit 1
    fi
    _benign=$(printf '%s\n' "$_porcelain" | grep -c . || true)
    _log "$log_file" "Pre-flight: $_benign uncommitted file(s) outside the pipeline write-set — ignoring, they will not be touched"
    # Preserve the branch-carry behaviour for the append-only beads log, used
    # only if step (2) below has to switch branches.
    printf '%s\n' "$_porcelain" | grep -q '^.. \.beads/interactions\.jsonl$' && beads_dirty=1
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
        if [ "$beads_dirty" -eq 1 ]; then
          _log "$log_file" "FATAL: cannot pivot to sibling worktree while .beads/interactions.jsonl is dirty"
          exit 1
        fi
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
  #     -c pull.rebase=false is load-bearing: with pull.rebase=true in local
  #     config, git routes --ff-only through the rebase path, which refuses the
  #     deliberately-carried dirty .beads/interactions.jsonl ("cannot pull with
  #     rebase: You have unstaged changes") — that killed the 2026-08-01 run.
  #     A ff-only merge pull tolerates unrelated dirty files; force that path.
  if ! git -c pull.rebase=false pull --ff-only origin "$default_branch" >> "$log_file" 2>&1; then
    _log "$log_file" "FATAL: git pull --ff-only origin $default_branch failed — stale or diverged state is not safe for generation"
    exit 1
  fi

  # Commit the append-only Beads log only after branch normalization and a
  # successful fast-forward. Committing it on a stale feature branch was the
  # source of the 2026-07-29 divergence incident.
  if [ "$beads_dirty" -eq 1 ]; then
    if git add .beads/interactions.jsonl \
      && git commit --no-verify -m "chore(beads): append interaction log (cron preflight auto-commit)" >> "$log_file" 2>&1; then
      _log "$log_file" "Pre-flight: committed interactions.jsonl on $default_branch @ $(git rev-parse --short HEAD)"
    else
      _log "$log_file" "FATAL: could not commit .beads/interactions.jsonl on $default_branch"
      exit 1
    fi
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
# liveness_markers <job> <rc>
#
# Two-marker estate liveness/health protocol (2026-07-10; mirrors
# Intent runtime's owner-neutral exit handler. Touches, under
# $HOME/.local/state/intent-os/liveness/:
#   <job>.beat  on EVERY call        — "the schedule fired" (liveness)
#   <job>.ok    ONLY when <rc> is 0  — "and the run succeeded" (health)
# The estate dead-man's-switch (~/bin/automation-liveness-sweep.sh) reads the
# pair: stale .beat = stopped running; fresh .beat + stale/missing .ok =
# running-but-failing. A failure run must NOT touch .ok — that gap IS the
# signal, so never call this with a forged rc.
#
# Call it from the wrapper's EXIT trap, immediately after `local rc=$?`, so the
# markers land on every exit path. The raw top-of-script beat drop each wrapper
# carries still covers a crash BEFORE the trap is armed (and is intentionally
# lib-independent so a broken source line can't hide a run). Never fails the
# caller.
# ─────────────────────────────────────────────────────────────────────────────
liveness_markers() {
  local job="$1" rc="${2:-1}"
  local dir="$HOME/.local/state/intent-os/liveness"
  local safe="${job//[^A-Za-z0-9_-]/_}"
  mkdir -p "$dir" 2>/dev/null || true
  : > "$dir/${safe}.beat" 2>/dev/null || true
  if [ "$rc" = "0" ]; then
    : > "$dir/${safe}.ok" 2>/dev/null || true
  fi
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

# published_post_for_date <repo> <posts_dir> <YYYY-MM-DD>
#
# A local file is not proof that a date was published. Return the first matching
# post that is tracked by Git and unchanged at HEAD. Untracked/modified producer
# debris must never satisfy the daily idempotency gate.
published_post_for_date() {
  local repo="$1" posts_dir="$2" d="$3" hit rel
  while IFS= read -r hit; do
    [ -n "$hit" ] || continue
    rel=${hit#"$repo"/}
    if git -C "$repo" ls-files --error-unmatch "$rel" >/dev/null 2>&1 \
      && git -C "$repo" diff --quiet HEAD -- "$rel" 2>/dev/null; then
      echo "$hit"
      return 0
    fi
  done < <(grep -rlE "^date = ['\"]?${d}|^date: ['\"]?${d}" "$posts_dir" 2>/dev/null || true)
  return 1
}

# ─────────────────────────────────────────────────────────────────────────────
# disk_free_mb <path> / disk_mount_of <path>
#
# The single place the pipeline reads free space. `df -Pm` reports MiB (the
# POSIX -P format keeps one line per filesystem so awk column 4 is stable), and
# every threshold in this library is in MiB too — do not mix in `df -h` output.
# Tests override these two functions to inject a fake reading; nothing here
# ever touches the real filesystem's contents.
# ─────────────────────────────────────────────────────────────────────────────
disk_free_mb()  { df -Pm "$1" 2>/dev/null | awk 'NR==2 {print $4}'; }
disk_mount_of() { df -Pm "$1" 2>/dev/null | awk 'NR==2 {print $6}'; }

# ─────────────────────────────────────────────────────────────────────────────
# disk_guard <path> <min_free_mb> <log_file> [warn_free_mb]
#
# Hard floor + early warning for every job that commits, builds, or writes
# state on this filesystem. Return 1 (refuse) when free < min_free_mb; return 0
# otherwise, logging a WARN line when free < warn_free_mb. Sets, for callers
# that want to build an actionable alert:
#   DISK_GUARD_STATE    ok | warn | fatal | unknown
#   DISK_GUARD_FREE_MB  the reading (MiB)
#   DISK_GUARD_MOUNT    the mount point the reading is for
#
# WHY THE FLOOR MUST NEVER BE LOWERED OR BYPASSED (2026-09-05 incident): with
# 217 MiB free the guard refused the 04:00 producer and that refusal was the
# correct outcome. A commit, a hugo build, or an atomic JSON write on a wedged
# disk fails half-way and leaves a corrupted tree, a torn ledger, or a partial
# post that the next run then has to quarantine. The guard is the reason a
# full disk costs one missed day instead of a corrupted pipeline. Fix capacity
# (see 000-docs/004-OP-RUNB-blog-low-disk-recovery.md); do not fix the number.
# The warning line exists so the floor is never the first anyone hears of it.
# ─────────────────────────────────────────────────────────────────────────────
# shellcheck disable=SC2034 # DISK_GUARD_* are read by callers after the call returns
disk_guard() {
  local path="$1" min_mb="$2" log_file="$3" warn_mb="${4:-0}" avail_mb mount
  DISK_GUARD_STATE="unknown"; DISK_GUARD_FREE_MB=""; DISK_GUARD_MOUNT=""
  avail_mb=$(disk_free_mb "$path")
  if [ -z "$avail_mb" ]; then
    _log "$log_file" "WARN: disk_guard could not read free space for $path — continuing"
    return 0
  fi
  mount=$(disk_mount_of "$path")
  DISK_GUARD_FREE_MB="$avail_mb"; DISK_GUARD_MOUNT="${mount:-?}"
  if [ "$avail_mb" -lt "$min_mb" ]; then
    DISK_GUARD_STATE="fatal"
    _log "$log_file" "FATAL: only ${avail_mb}MiB free on ${mount} (need ${min_mb}MiB) — refusing to run"
    return 1
  fi
  if [ "$warn_mb" -gt 0 ] 2>/dev/null && [ "$avail_mb" -lt "$warn_mb" ]; then
    DISK_GUARD_STATE="warn"
    _log "$log_file" "WARN: ${avail_mb}MiB free on ${mount} is under the ${warn_mb}MiB early-warning line (hard floor ${min_mb}MiB) — running, but free space now before the floor stops the pipeline"
    return 0
  fi
  DISK_GUARD_STATE="ok"
  return 0
}

# ─────────────────────────────────────────────────────────────────────────────
# disk_warn_alert <job> <text>
#
# Deliver an early-warning disk alert through the governed alert floor. It is
# sent at `high` on purpose: the floor drops anything below `high`, and a
# warning nobody sees is the 2026-09-05 failure mode (the weekly cleanup logged
# "100% -> 100%" for three weeks and nobody was told). The text says WARNING
# explicitly so it is not read as an outage. Never fails the caller.
# ─────────────────────────────────────────────────────────────────────────────
disk_warn_alert() {
  local job="$1" text="$2"
  if command -v buzz_post >/dev/null 2>&1; then
    buzz_post "WARNING (not a failure) ${job}: ${text}" sys-automation high
  fi
  return 0
}

# ─────────────────────────────────────────────────────────────────────────────
# resolve_target_date [YYYY-MM-DD]
#
# The one place a pipeline date comes from. With no argument: yesterday by
# CALENDAR day, never "now minus 24 hours" (a DST transition would make that
# land on the wrong date). BLOG_CLOCK (an absolute timestamp) replaces "now"
# so tests can pin the clock. With an argument: it must be a real calendar
# date in strict YYYY-MM-DD form, not in the future. Prints the date; exit 1
# and a message on stderr otherwise.
#
# The box runs a fixed -06:00 zone (Etc/GMT+6, no DST); the calendar-day form
# is still what keeps the target correct if that ever changes.
# ─────────────────────────────────────────────────────────────────────────────
resolve_target_date() {
  local want="${1:-}" now="${BLOG_CLOCK:-now}" d today
  if [ -z "$want" ]; then
    date -d "${now} 1 day ago" +%Y-%m-%d
    return 0
  fi
  case "$want" in
    [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]) ;;
    *) echo "resolve_target_date: '$want' is not YYYY-MM-DD" >&2; return 1 ;;
  esac
  d=$(date -d "$want" +%Y-%m-%d 2>/dev/null) || { echo "resolve_target_date: '$want' is not a real date" >&2; return 1; }
  [ "$d" = "$want" ] || { echo "resolve_target_date: '$want' is not a real date" >&2; return 1; }
  today=$(date -d "$now" +%Y-%m-%d)
  [[ "$want" > "$today" ]] && { echo "resolve_target_date: '$want' is in the future (today is $today)" >&2; return 1; }
  echo "$want"
}

# ─────────────────────────────────────────────────────────────────────────────
# prune_run_logs <dir> <keep_days> <log_file>
#
# Bounded retention for a cron job's per-run logs. Deletes ONLY regular files
# named exactly run-YYYY-MM-DD.log, directly inside <dir>, older than
# <keep_days>. Everything else is refused, loudly:
#   * <dir> must live under $HOME/.local/state (the only place run logs live);
#   * keep_days under 30 is refused (a typo must not empty the audit trail);
#   * any other filename (a manifest, an incident note, a hand-kept log) is
#     left alone even if it is old.
# Prints the number of files removed. This is the whole reclaim surface the
# blog pipeline is allowed — it never deletes anything it did not write.
# ─────────────────────────────────────────────────────────────────────────────
prune_run_logs() {
  local dir="$1" keep_days="$2" log_file="$3" n=0 f base
  case "$dir" in
    "$HOME/.local/state/"*) ;;
    *) _log "$log_file" "WARN: prune_run_logs refused: $dir is outside \$HOME/.local/state" >&2; echo 0; return 1 ;;
  esac
  if ! [ "$keep_days" -ge 30 ] 2>/dev/null; then
    _log "$log_file" "WARN: prune_run_logs refused: keep_days=$keep_days is under the 30-day minimum" >&2
    echo 0; return 1
  fi
  [ -d "$dir" ] || { echo 0; return 0; }
  while IFS= read -r f; do
    base=$(basename "$f")
    case "$base" in
      run-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].log) ;;
      *) continue ;;
    esac
    rm -f -- "$f" && n=$((n + 1))
  done < <(find "$dir" -maxdepth 1 -type f -name 'run-*.log' -mtime +"$keep_days" 2>/dev/null)
  [ "$n" -gt 0 ] && _log "$log_file" "Retention: removed $n run log(s) older than ${keep_days}d from $dir" >&2
  echo "$n"
  return 0
}

# ─────────────────────────────────────────────────────────────────────────────
# quarantine_census <quarantine_dir> <max_entries> <log_file>
#
# Quarantine holds the only copy of a post that failed its gates — evidence,
# never garbage. This never deletes; it counts. Return 1 (and log a WARN) when
# the count exceeds <max_entries>, so a growing quarantine becomes a visible
# signal in the run log and summary instead of silent disk growth. Sets
# QUARANTINE_COUNT / QUARANTINE_MB for the caller's summary.
# ─────────────────────────────────────────────────────────────────────────────
quarantine_census() {
  local qdir="$1" max="$2" log_file="$3"
  QUARANTINE_COUNT=0; QUARANTINE_MB=0
  [ -d "$qdir" ] || return 0
  QUARANTINE_COUNT=$(find "$qdir" -mindepth 1 -maxdepth 1 2>/dev/null | wc -l | tr -d ' ')
  QUARANTINE_MB=$(du -sm "$qdir" 2>/dev/null | awk '{print $1}')
  if [ "$QUARANTINE_COUNT" -gt "$max" ]; then
    _log "$log_file" "WARN: quarantine holds ${QUARANTINE_COUNT} entries (${QUARANTINE_MB}MiB) — over the ${max}-entry review line; triage $qdir (nothing is auto-deleted)"
    return 1
  fi
  return 0
}

# ─────────────────────────────────────────────────────────────────────────────
# ledger_entries_for_date <ledger_json> <YYYY-MM-DD>
#
# Prints how many syndication-ledger entries carry .date == the given day. The
# post-recovery invariant is exactly one; 0 means the land step never wrote
# the entry, 2+ means a duplicate landed. Missing/invalid ledger prints 0.
# ─────────────────────────────────────────────────────────────────────────────
ledger_entries_for_date() {
  local ledger="$1" d="$2"
  [ -f "$ledger" ] || { echo 0; return 0; }
  jq -r --arg d "$d" '[.[] | select(.date == $d)] | length' "$ledger" 2>/dev/null || echo 0
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
    return 0
  fi
  # An FF-push cannot succeed once origin/<default> has moved, and it moves often
  # here: the release workflow pushes version + changelog commits on nearly every
  # push. That produced a false "needs manual merge" whose actual remedy was a
  # rebase. Try exactly that, once, and only accept it if it lands cleanly.
  #
  # Guarded, because this rewrites a branch: a rebase that conflicts is aborted
  # and we fall through to the original ORPHANED report, so the worst case here
  # is identical to the behaviour this replaces, never worse.
  _log "$log_file" "FF-push failed for $label — origin/$default likely moved; attempting one rebase"
  if git fetch -q origin "$default" >> "$log_file" 2>&1 \
     && git rebase --autostash "origin/$default" >> "$log_file" 2>&1 \
     && git push origin "$current:$default" >> "$log_file" 2>&1; then
    sha=$(git rev-parse --short HEAD)
    _log "$log_file" "✓ FF-pushed $label after rebase: $current → origin/$default ($sha)"
    RECONCILED="${RECONCILED}${label}: ✓ auto-merged after rebase $current → origin/$default ($sha)\n"
    return 0
  fi
  git rebase --abort >/dev/null 2>&1 || true
  _log "$log_file" "✗ FF-push failed for $label ($current → origin/$default) — manual merge required"
  RECONCILED="${RECONCILED}${label}: ⚠ ORPHANED on $current — needs manual merge\n"
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

# ─────────────────────────────────────────────────────────────────────────────
# push_with_rebase <branch> <log> [attempts]
#
# Push the current branch to origin/<branch>, rebasing onto a newer tip if the
# push is rejected. Run from inside the repo.
#
# Why --autostash, and why this is a function instead of two inline lines:
# blog-land.sh states in its own header that it does NOT require a clean tree,
# because the staged post is an expected uncommitted change. Its recovery path
# then called a bare `git pull --rebase`, which REFUSES to run with unstaged
# changes to tracked files. So the script declared a dirty tree normal and then
# could not recover in one. On 2026-08-09 a release-bot commit landed between
# this script's fetch and its push while `.beads/interactions.jsonl` was
# modified: the rebase bailed with "cannot pull with rebase: You have unstaged
# changes", the post commit was stranded, and the run paged as a hard failure
# even though nothing was actually wrong with the post.
#
# --autostash is exactly the fix: stash the unstaged work, rebase, re-apply. If
# the re-apply conflicts the rebase still lands and the stash survives, which is
# strictly better than refusing to rebase at all.
#
# The retry exists because the losing race is not rare here. The release
# workflow pushes version and changelog commits to the same branch on nearly
# every push, so the bot can land again DURING our rebase. Chose a bounded retry
# over a lock because the bot is a GitHub-side workflow we cannot take a lock
# against.
# Return: 0 pushed, 1 failed (after attempts).
# ─────────────────────────────────────────────────────────────────────────────
push_with_rebase() {
  local branch="$1" log_file="$2" attempts="${3:-3}" i
  for ((i = 1; i <= attempts; i++)); do
    if git push origin "$branch" >> "$log_file" 2>&1; then
      [ "$i" -gt 1 ] && _log "$log_file" "push succeeded on attempt $i (after rebase)"
      return 0
    fi
    if [ "$i" -eq "$attempts" ]; then
      _log "$log_file" "push still rejected after $attempts attempt(s)"
      return 1
    fi
    _log "$log_file" "push rejected — rebasing onto origin/$branch (attempt $i/$attempts, autostash on)"
    if ! git pull --rebase --autostash origin "$branch" >> "$log_file" 2>&1; then
      _log "$log_file" "rebase onto origin/$branch FAILED (conflict, or a rebase is already in progress)"
      return 1
    fi
  done
  return 1
}

# ─────────────────────────────────────────────────────────────────────────────
# publish_file_to_repo <repo_hint> <branch> <src_file> <dest_abs_path> <msg> <log>
#
# Publish a single file to a repo's <branch> WITHOUT touching any working tree,
# using git plumbing (hash-object → read-tree → commit-tree → push). It always
# bases the new commit on the FRESH origin/<branch> tip and retries on a
# push race, so it survives a fast-moving shared repo.
#
# Why: the old dual-publish did `cd repo && git add && commit && push` on the
# SHARED, often-dirty, often-behind claude-code-plugins PRIMARY tree. When local
# main was behind origin the push was rejected non-fast-forward and the mirror
# silently 404'd (2026-07-06). This never touches the working tree, so a
# concurrent session's dirty tree / behind-branch can't break it.
#
# <repo_hint> is any path inside the repo (the real toplevel is resolved, so it
# works even when the deploy dir is a subdir — e.g. intent-solutions-landing's
# astro-site). <dest_abs_path> is the file's absolute path in the working tree;
# its path relative to the repo toplevel is what gets committed.
# Return: 0 pushed, 1 failed (after retries).
# ─────────────────────────────────────────────────────────────────────────────
publish_file_to_repo() {
  local hint="$1" branch="$2" src="$3" dest_abs="$4" msg="$5" log_file="$6"
  local top rel base blob tree commit tmpidx attempt
  top=$(git -C "$hint" rev-parse --show-toplevel 2>/dev/null) \
    || { _log "$log_file" "publish_file_to_repo: '$hint' is not in a git repo"; return 1; }
  [ -f "$src" ] || { _log "$log_file" "publish_file_to_repo: src '$src' missing"; return 1; }
  rel="${dest_abs#"$top"/}"
  if [ "$rel" = "$dest_abs" ]; then
    _log "$log_file" "publish_file_to_repo: dest '$dest_abs' is not under toplevel '$top'"; return 1
  fi
  for attempt in 1 2 3; do
    git -C "$top" fetch origin "$branch" -q 2>>"$log_file" || true
    base=$(git -C "$top" rev-parse "origin/$branch" 2>/dev/null) \
      || { _log "$log_file" "publish_file_to_repo: no origin/$branch in $top"; return 1; }
    blob=$(git -C "$top" hash-object -w "$src" 2>>"$log_file") || return 1
    tmpidx=$(mktemp)
    if ! GIT_INDEX_FILE="$tmpidx" git -C "$top" read-tree "$base" 2>>"$log_file"; then rm -f "$tmpidx"; return 1; fi
    GIT_INDEX_FILE="$tmpidx" git -C "$top" update-index --add --cacheinfo "100644,$blob,$rel" 2>>"$log_file"
    tree=$(GIT_INDEX_FILE="$tmpidx" git -C "$top" write-tree 2>>"$log_file"); rm -f "$tmpidx"
    [ -n "$tree" ] || return 1
    commit=$(git -C "$top" commit-tree "$tree" -p "$base" -m "$msg" 2>>"$log_file") || return 1
    if git -C "$top" push origin "$commit:$branch" >>"$log_file" 2>&1; then
      _log "$log_file" "published $rel → origin/$branch ($(printf '%s' "$commit" | cut -c1-9))"
      return 0
    fi
    _log "$log_file" "publish_file_to_repo: push attempt $attempt for origin/$branch failed (moved?) — retrying"
  done
  return 1
}
