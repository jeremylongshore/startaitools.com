#!/usr/bin/env bash
# Daily autonomous blog pipeline. Runs at 04:00 local host time via cron.
#
# ARCHITECTURE (inverted 2026-07-05): the LLM PRODUCES, deterministic code LANDS.
#   1. preflight: lock, disk/admission guard, verified isolated remote checkout
#   2. Producer writes the post + decisions + readiness sentinel (no git):
#      primary Claude toolchain on the established static MiniMax transport;
#      failure remains visible; shell-only agents are explicit legacy modes.
#      BLOG_PRODUCER=auto|claude|minimax|grok; claude explicitly uses OAuth.
#   3. blog-land.sh (pure bash) verifies preconditions and, only if they pass,
#      commits + pushes + dual-publishes + queues cross-posts + verifies live.
#      If they fail (timeout mid-gates, fact-check block, broken build) it
#      QUARANTINES the stranded files so tomorrow is unblocked, and never
#      publishes something half-baked.
#
# - Idempotent: if yesterday already has a post, exits clean (no-op).
# - flock-serialized against a hand-run /blog-backfill (no concurrent-tree race).
# - Fail-loud: any abnormal early exit pings Buzz sys-automation + emails Jeremy,
#   naming the target date, the reason, the log, free vs required disk, and the
#   exact recovery command.
#
# Usage:
#   blog-backfill-daily.sh                 # cron: yesterday (calendar day)
#   blog-backfill-daily.sh --date DATE     # recover ONE missed day; same guards,
#                                          # same producer, same lander, same
#                                          # idempotency — safe to re-run
#   blog-backfill-daily.sh --disk-check    # print free vs floor/warn and exit
#                                          # 0 ok / 1 below floor; no lock, no
#                                          # log, no alert (runbook helper)
# Env: BLOG_BACKFILL_DISK_MIN_MB (500, the hard floor — see disk_guard in
#      lib-cron-common.sh for why it is never lowered), BLOG_BACKFILL_DISK_WARN_MB
#      (2048, early warning), BLOG_BACKFILL_LOG_KEEP_DAYS (180),
#      BLOG_QUARANTINE_MAX_ENTRIES (12).

set -uo pipefail

# Cron PATH is minimal (often /usr/bin:/bin). Prepend ~/.local/bin (claude,
# node, minimax-agent.py) and ~/bin (sops, grok, notify.sh, age) so the
# MiniMax fallback can decrypt ~/.config/intentsolutions/api-providers.sops.json
# (else it FATALs with "no API key" and we double-fail when Claude is rate-limited).
# Mirrors scripts/blog/web-analytics-daily.sh:34. Bug surfaced 2026-07-25 after
# Claude hit its weekly quota; MiniMax fallback had no working sops PATH.
export PATH="${HOME}/.local/bin:${HOME}/.bun/bin:${HOME}/bin:/usr/local/bin:/usr/bin:/bin:${PATH:-}"

LOG_DIR="${BLOG_LOG_DIR:-$HOME/.local/state/blog-backfill-daily}"
BLOG_DIR=${BLOG_REPO_DIR:-/home/jeremy/000-projects/blog/startaitools}
mkdir -p "$LOG_DIR"

# --- Arguments (parsed before anything touches state: --help and --disk-check
# must not drop a liveness beat, take the lock, or open a run log) ----------------
TARGET_ARG=""
DISK_CHECK_ONLY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --date)   TARGET_ARG="${2:-}"; shift 2 ;;
    --date=*) TARGET_ARG="${1#--date=}"; shift ;;
    --disk-check) DISK_CHECK_ONLY=1; shift ;;
    -h|--help) sed -n '/^# Usage:/,/^# Env:/p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "blog-backfill-daily.sh: unknown argument '$1' (see --help)" >&2; exit 64 ;;
  esac
done

DISK_MIN_MB="${BLOG_BACKFILL_DISK_MIN_MB:-500}"
DISK_WARN_MB="${BLOG_BACKFILL_DISK_WARN_MB:-2048}"

# --disk-check is the runbook's first question ("can the producer run right
# now?"). Read-only and lib-independent on purpose: it runs before the liveness
# beat, the lock, the log, and the library source, so it can never masquerade
# as a cron run or hide behind a broken source line. Same df -Pm reading (MiB)
# the guard uses.
if [ "$DISK_CHECK_ONLY" = "1" ]; then
  read -r free_mb mount < <(df -Pm "$BLOG_DIR" 2>/dev/null | awk 'NR==2 {print $4, $6}')
  printf 'free=%sMiB mount=%s floor=%sMiB warn=%sMiB ' "${free_mb:-?}" "${mount:-?}" "$DISK_MIN_MB" "$DISK_WARN_MB"
  if [ -z "${free_mb:-}" ]; then echo "state=unknown"; exit 0; fi
  if [ "$free_mb" -lt "$DISK_MIN_MB" ]; then echo "state=BELOW-FLOOR (producer will refuse)"; exit 1; fi
  if [ "$free_mb" -lt "$DISK_WARN_MB" ]; then echo "state=warn (runs, but free space soon)"; exit 0; fi
  echo "state=ok"; exit 0
fi

# Liveness heartbeat: drop a per-run beat so the estate dead-man's-switch
# (~/bin/automation-liveness-sweep.sh) can tell this schedule still fires. The
# beat marks "the cron ran"; the fail-loud trap below covers "ran but failed".
if [ "${BLOG_CANARY:-0}" != "1" ]; then
  mkdir -p "$HOME/.local/state/intent-os/liveness" 2>/dev/null || true
  : > "$HOME/.local/state/intent-os/liveness/blog-backfill-daily.beat" 2>/dev/null || true
fi

EMAIL_SCRIPT=/home/jeremy/.claude/skills/email/scripts/send-email.cjs
POSTS_DIR="$BLOG_DIR/content/posts"
LAND_SCRIPT="$(dirname "${BASH_SOURCE[0]}")/blog-land.sh"
SELF="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"
RUNBOOK="$BLOG_DIR/000-docs/004-OP-RUNB-blog-low-disk-recovery.md"

# Shared helpers: preflight_branch_normalize, post_exists_for_date, disk_guard,
# resolve_target_date, prune_run_logs, quarantine_census, acquire_pipeline_lock,
# count_consecutive_failures, cron_fail.
# shellcheck source=./lib-cron-common.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib-cron-common.sh"

# Calendar-day target (never "now - 24h": DST-fragile). --date pins one day for
# recovery; every guard and the idempotency gate below apply identically.
if ! YESTERDAY=$(resolve_target_date "$TARGET_ARG"); then exit 64; fi
LOG="$LOG_DIR/run-${YESTERDAY}.log"
BLOG_RUN_ID=$(python3 -c 'import uuid; print(uuid.uuid4())')
BLOG_INCIDENT_ID="blog-daily-${YESTERDAY}"
export BLOG_RUN_ID BLOG_INCIDENT_ID
RECOVERY_CMD="$SELF --date $YESTERDAY"
FAIL_REASON=""

log() { echo "[$(date -Is)] $*" | tee -a "$LOG"; }

# A large structured log line can exceed Linux's per-argument limit. Preserve
# the complete notification body in a private file, never an exec argument.
send_notification() {
  (
    local notification_dir
    notification_dir=$(mktemp -d) || return 1
    trap 'rm -rf -- "$notification_dir"' EXIT
    printf '%s' "$2" > "$notification_dir/body.txt"
    chmod 600 "$notification_dir/body.txt"
    node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io --subject "$1" \
      --body-file "$notification_dir/body.txt"
  )
}
if [ -n "$TARGET_ARG" ]; then
  log "=== Daily blog-backfill start (target: $YESTERDAY — explicit --date recovery run) ==="
else
  log "=== Daily blog-backfill start (target: $YESTERDAY) ==="
fi

# --- Fail-loud guard: an early exit must never be silent (startaitools-74z) ---
# From 2026-06-15 the dirty-tree preflight aborted every run for 11 days with
# ZERO alerts. This trap fires on any non-zero exit that bypassed the normal
# notification and pings Buzz sys-automation + email. Clean exits (rc=0, incl.
# the idempotency/lock no-ops) and the normal path (NOTIFIED=1) are skipped.
NOTIFIED=0
notify_unexpected_exit() {
  local rc=$?   # FIRST: any test below would overwrite it
  # A failover child never pages on its own, not even on an early abnormal exit: the
  # parent run that started it owns the single alert for this date.
  if { [ "${BLOG_FAILOVER_DEPTH:-0}" != "0" ] || [ "${BLOG_QUIET_FAILURE:-0}" = "1" ]; } \
      && [ "${NOTIFIED:-0}" != "1" ] && [ "$rc" -ne 0 ]; then
    echo "[$(date -Is)] QUIET-CHILD: abnormal exit rc=$rc; quiet, the parent run alerts" >> "${LOG:-/dev/null}"
    return 0
  fi
  if [ "${BLOG_CANARY:-0}" = "1" ]; then
    log "CANARY-EXIT: rc=$rc; no production heartbeat or notification"
    return
  fi
  [ -z "${PRODUCER_GUARD_DIR:-}" ] || rm -rf "$PRODUCER_GUARD_DIR"
  liveness_markers "blog-backfill-daily" "$rc"   # .beat every run; .ok iff rc==0
  [ "$rc" -eq 0 ] && return
  [ "$NOTIFIED" -eq 1 ] && return
  log "ABNORMAL EXIT (rc=$rc) before normal notification — sending fail-loud alert"
  # Everything an operator needs to act without opening the box: the date that
  # has no post, why, where the log is, the capacity numbers, and the one
  # command that recovers the day once the cause is fixed.
  local detail free_line early_body
  free_line="disk: ${DISK_GUARD_FREE_MB:-unknown}MiB free on ${DISK_GUARD_MOUNT:-/}, floor ${DISK_MIN_MB}MiB, warn ${DISK_WARN_MB}MiB"
  detail="${YESTERDAY}: NO POST — early exit rc=${rc}"
  [ -n "$FAIL_REASON" ] && detail="${detail}; reason: ${FAIL_REASON}"
  detail="${detail}; ${free_line}; log: ${LOG}; recover with: ${RECOVERY_CMD}"
  cron_fail "blog-backfill-daily" "$detail"
  early_body="$(printf 'Daily blog-backfill exited abnormally (rc=%s) BEFORE its normal summary email.\n\nTarget date : %s (NO POST landed)\nReason      : %s\nCapacity    : %s\nLog         : %s\n\nRecovery (idempotent, safe to re-run once the cause is fixed):\n  %s\n  %s --sweep\nRunbook: %s\n\nLast 30 log lines:\n--------------------------------------------------------------------------------\n%s\n' "$rc" "$YESTERDAY" "${FAIL_REASON:-see log}" "$free_line" "$LOG" "$RECOVERY_CMD" "$BLOG_DIR/scripts/blog/blog-posting-packet.sh" "$RUNBOOK" "$(tail -30 "$LOG" 2>/dev/null)")"
  send_notification \
    "🚨 blog-backfill aborted early: ${YESTERDAY} (rc=${rc})${FAIL_REASON:+ — ${FAIL_REASON%%:*}}" \
    "$early_body" \
    >> "$LOG" 2>&1 || log "ERROR: early-exit email notification failed; cron failure remains active"
}
trap notify_unexpected_exit EXIT

# --- Concurrency lock: never let the cron race a hand-run /blog-backfill ------
acquire_pipeline_lock "/tmp/blog-pipeline.lock" "$LOG"; _lk=$?
if [ "$_lk" -eq 2 ]; then NOTIFIED=1; exit 0; fi   # another run holds it — benign
if [ "$_lk" -eq 1 ]; then log "FATAL: could not acquire lock"; exit 1; fi
export BLOG_PIPELINE_LOCK_HELD=1   # so the child blog-land.sh does not re-lock

# --- Disk guard: a wedged disk turns commit/build into corruption ------------
# Hard floor (refuse) + early-warning line (run, but say so). The floor is not
# tunable downward in practice — see disk_guard in lib-cron-common.sh.
DISK_WARNING=""
if ! disk_guard "$BLOG_DIR" "$DISK_MIN_MB" "$LOG" "$DISK_WARN_MB"; then
  FAIL_REASON="disk guard refused: ${DISK_GUARD_FREE_MB:-?}MiB free on ${DISK_GUARD_MOUNT:-/} is under the ${DISK_MIN_MB}MiB floor"
  exit 1
fi
if [ "${DISK_GUARD_STATE:-ok}" = "warn" ]; then
  DISK_WARNING="${DISK_GUARD_FREE_MB}MiB free on ${DISK_GUARD_MOUNT} (warn line ${DISK_WARN_MB}MiB, floor ${DISK_MIN_MB}MiB)"
  disk_warn_alert "blog-backfill-daily" "${DISK_WARNING}. The producer still ran for ${YESTERDAY}; below the floor it will refuse. Free space now — runbook ${RUNBOOK}"
fi

# --- Isolated source: never normalize/stash/clean the owner's checkout --------
BLOG_SOURCE_DIR="$BLOG_DIR"
WORKSPACE_HELPER="$(dirname "$SELF")/blog-run-workspace.py"
WORKSPACE_RESULT=$(python3 "$WORKSPACE_HELPER" create \
  --repo "$BLOG_SOURCE_DIR" --date "$YESTERDAY" --run-id "$BLOG_RUN_ID" \
  --state-dir "${BLOG_RUN_STATE_DIR:-$HOME/.local/state/blog-run-workspaces}" \
  --expected-remote "${BLOG_EXPECTED_REMOTE:-https://github.com/jeremylongshore/startaitools.com.git}" \
  --recover-abandoned 2>> "$LOG") || { FAIL_REASON="isolated run creation/admission failed; inspect logged validation and capacity evidence"; log "FATAL: $FAIL_REASON; owner work preserved"; exit 1; }
BLOG_RUN_MANIFEST=$(printf '%s' "$WORKSPACE_RESULT" | jq -r '.manifest')
BLOG_RUN_DIAGNOSTICS_DIR=$(printf '%s' "$WORKSPACE_RESULT" | jq -er '.diagnostics_dir')
BLOG_RUN_WORKSPACE_HELPER="$WORKSPACE_HELPER"
BLOG_DIR=$(printf '%s' "$WORKSPACE_RESULT" | jq -r '.workspace')
BLOG_REPO_DIR="$BLOG_DIR"
BLOG_STATE_DIR="$BLOG_SOURCE_DIR"
export BLOG_RUN_MANIFEST BLOG_REPO_DIR BLOG_STATE_DIR BLOG_RUN_DIAGNOSTICS_DIR BLOG_RUN_WORKSPACE_HELPER
POSTS_DIR="$BLOG_DIR/content/posts"
LAND_SCRIPT="$(dirname "$SELF")/blog-land.sh"
cd "$BLOG_DIR" || exit 1
log "WORKSPACE: $BLOG_DIR manifest=$BLOG_RUN_MANIFEST"
RETENTION_SUMMARY=$(printf '%s' "$WORKSPACE_RESULT" | jq -c '.retention | if . == null then {cleanup:"not-run"} else {registry_bytes,workspace_bytes,protected_bytes,retired_runs,protected_runs} end')
log "CHECKOUT-RETENTION: $RETENTION_SUMMARY"
rebuild_canonical_index() {
  python3 "$(dirname "$SELF")/blog-methodology-published-index.py" \
    --repo "$BLOG_SOURCE_DIR" \
    --output "$BLOG_SOURCE_DIR/.claude/skills/blog-backfill/methodology/index.db" \
    --expected-remote "${BLOG_EXPECTED_REMOTE:-https://github.com/jeremylongshore/startaitools.com.git}"
}
PUBLICATION_HELPER="$(dirname "$SELF")/blog_publication_state.py"
RECOVERY_DEGRADED=0
if [ "${BLOG_CANARY:-0}" != "1" ]; then
  RECOVERY_RESULT=$(python3 "$PUBLICATION_HELPER" recover --manifest "$BLOG_RUN_MANIFEST" 2>> "$LOG")
  RECOVERY_RC=$?
  printf '%s\n' "$RECOVERY_RESULT" >> "$LOG"
  case "$RECOVERY_RC" in
    0) ;;
    2) RECOVERY_DEGRADED=1
       FAIL_REASON="older publication delivery remains pending; current target proceeds independently"
       log "DEGRADED: $FAIL_REASON" ;;
    *) FAIL_REASON="publication recovery registry failed validation"
       log "FATAL: $FAIL_REASON"; exit 1 ;;
  esac
fi
if EXISTING=$(published_post_for_date "$BLOG_DIR" "$POSTS_DIR" "$YESTERDAY"); then
  if [ "${BLOG_CANARY:-0}" != "1" ]; then
    EXISTING_SLUG=$(basename "$EXISTING" .md)
    if ! remote_live_check "https://startaitools.com/posts/$EXISTING_SLUG/" 60 "$LOG"; then
      FAIL_REASON="public article unavailable for existing remote post $YESTERDAY/$EXISTING_SLUG"
      log "FATAL: $FAIL_REASON; source presence does not prove successful publication"
      exit 1
    fi
    python3 "$PUBLICATION_HELPER" check-existing --manifest "$BLOG_RUN_MANIFEST" \
      --slug "$EXISTING_SLUG" >> "$LOG" 2>&1 || {
      FAIL_REASON="existing public article has incomplete delivery state and no recoverable sealed run"
      log "FATAL: $FAIL_REASON"
      exit 1
    }
    "$BLOG_SOURCE_DIR/scripts/blog/blog-crosspost-sweep.sh" >> "$LOG" 2>&1 || exit 1
    if ! rebuild_canonical_index >> "$LOG" 2>&1; then
      FAIL_REASON="existing published article has an unreconciled canonical methodology index"
      log "FATAL: $FAIL_REASON; publication alone cannot authorize healthy no-op"
      exit 1
    fi
    log "Verified public article already covers $YESTERDAY ($EXISTING); generation is idempotent."
  else
    log "CANARY: remote source already covers $YESTERDAY; public and cross-post checks omitted."
  fi
  python3 "$WORKSPACE_HELPER" complete-noop --manifest "$BLOG_RUN_MANIFEST" >> "$LOG" 2>&1 || exit 1
  if [ "$RECOVERY_DEGRADED" -eq 1 ]; then
    log "FAILED: current target verified; older delivery recovery remains pending"
    exit 1
  fi
  NOTIFIED=1
  exit 0
fi
# Hugo theme is a pinned Git submodule; only this run workspace is initialized.
git submodule update --init --recursive >> "$LOG" 2>&1 || exit 1

# --- Generate: LLM produces artifacts ONLY (no git) --------------------------
# Primary: Claude skill toolchain using static MiniMax credentials (auto).
# Explicit claude mode retains OAuth for interactive operators. Commit/publish stay
# in blog-land.sh either way. Failed producers retain their owned work through
# the workspace helper; they cannot invoke the publishing lander.
TIMEOUT_SECS="${BLOG_BACKFILL_TIMEOUT:-2700}"
GROK_BIN="${GROK_BIN:-$HOME/.grok/bin/grok}"
MINIMAX_AGENT="${MINIMAX_AGENT:-$HOME/.local/bin/minimax-agent.py}"
# auto (default) = full Claude toolchain on MiniMax. This removes expiring
# OAuth from unattended
# generation while retaining required Agent/Skill gates. Explicit claude uses
# OAuth; minimax/grok remain opt-in legacy shell-agent modes.
PRODUCER_MODE="${BLOG_PRODUCER:-auto}"
PRODUCER_USED=""
PRODUCER_STATUS="NOT-RUN"
log "RUN-IDENTITY: incident=$BLOG_INCIDENT_ID run=$BLOG_RUN_ID source=$(git rev-parse HEAD)"

verify_producer_contract() {
  local transcript
  transcript=$(find "$HOME/.claude/projects" -name "${BLOG_RUN_ID:-missing}.jsonl" -type f -print -quit 2>/dev/null)
  BLOG_PRODUCER_TRANSCRIPT="$transcript"
  # The verifier's and the write-set validator's output is ALSO captured on its own, so a
  # repair reason can only ever come from them, never from what the producer printed into
  # the pty transcript (blogpipe/recovery.py: verifier_message).
  VERIFIER_CAPTURE="${LOG_DIR:-${TMPDIR:-/tmp}}/.verifier-${BLOG_RUN_ID:-missing}.txt"
  : > "$VERIFIER_CAPTURE" 2>/dev/null || VERIFIER_CAPTURE=/dev/null
  if [ -n "${BLOG_RUN_MANIFEST:-}" ]; then
    python3 "$WORKSPACE_HELPER" validate --manifest "$BLOG_RUN_MANIFEST" 2>&1 | tee -a "$VERIFIER_CAPTURE" >> "$LOG"
    [ "${PIPESTATUS[0]}" -eq 0 ] || {
      PRODUCER_STATUS="FAILED (run write-set integrity; process exited 0)"
      return 1
    }
  fi
  export BLOG_PRODUCER_TRANSCRIPT
  python3 "$BLOG_DIR/scripts/blog/blog-producer-contract.py" verify \
      --repo "$BLOG_DIR" --date "$YESTERDAY" --run-id "${BLOG_RUN_ID:-missing}" \
      --transcript "$transcript" 2>&1 | tee -a "$VERIFIER_CAPTURE" >> "$LOG"
  if [ "${PIPESTATUS[0]}" -eq 0 ]; then
    log "PRODUCER-CONTRACT: complete incident=${BLOG_INCIDENT_ID:-unknown} run=${BLOG_RUN_ID:-missing}"
    return 0
  fi
  PRODUCER_STATUS="FAILED (producer artifact contract; process exited 0)"
  log "$PRODUCER_STATUS; required outputs are incomplete, invalid or unscoped"
  return 1
}

# Put a read-only git shim first on PATH for every producer. The prompt boundary
# is backed by an executable boundary: add/commit/push/branch mutations are
# rejected before the deterministic lander takes over.
REAL_GIT_BIN=$(command -v git)
PRODUCER_GUARD_DIR=$(mktemp -d)
export REAL_GIT_BIN
# shellcheck disable=SC2016 # literals are the generated shim, expanded when it runs
printf '%s\n' \
  '#!/usr/bin/env bash' \
  'set -euo pipefail' \
  'args=("$@")' \
  'i=0' \
  'while [ "$i" -lt "${#args[@]}" ]; do' \
  '  case "${args[$i]}" in' \
  '    -C|-c|--git-dir|--work-tree) i=$((i + 2)); continue ;;' \
  '    -*) i=$((i + 1)); continue ;;' \
  '    *) command_name=${args[$i]}; break ;;' \
  '  esac' \
  'done' \
  'case "${command_name:-}" in' \
  '  add|am|apply|branch|checkout|cherry-pick|clean|commit|merge|mv|pull|push|rebase|reset|restore|rm|stash|switch|tag)' \
  '    echo "producer git guard: mutation rejected (${command_name})" >&2; exit 73 ;;' \
  'esac' \
  'exec "$REAL_GIT_BIN" "$@"' \
  > "$PRODUCER_GUARD_DIR/git"
chmod 0755 "$PRODUCER_GUARD_DIR/git"

# $1 (optional) = prompt, default the normal /blog-backfill invocation.
# $2 (optional) = "resume": continue THIS run's session in THIS workspace (repair round)
#                 instead of starting it. run_producer permits repeated attempts while
#                 the run is ready and unsealed; each one replaces producer_attempt.
LAST_PRODUCER_EXIT=0
run_claude_producer() {
  local t0 exitc wall command_prefix=claude provider=claude
  local prompt="${1:-/blog-backfill $YESTERDAY $YESTERDAY}" session_flag="--session-id"
  [ "${2:-}" = "resume" ] && session_flag="--resume"
  local -a runner=()
  LAST_PRODUCER_EXIT=0
  local prompt_file
  prompt_file=$(mktemp "${LOG_DIR:-${TMPDIR:-/tmp}}/.producer-prompt.XXXXXX") || {
    PRODUCER_STATUS="FAILED (could not stage the producer prompt)"
    LAST_PRODUCER_EXIT=1
    return 1
  }
  printf '%s' "$prompt" > "$prompt_file"
  if [ -n "${BLOG_RUN_MANIFEST:-}" ]; then
    runner=(python3 "$WORKSPACE_HELPER" run --manifest "$BLOG_RUN_MANIFEST" --)
  fi
  if [ "${PRODUCER_MODE:-auto}" = "auto" ]; then
    # Same MiniMax Anthropic-compatible Claude path already used by the governed
    # compiler. The full Agent/Skill tools remain available; only child env changes.
    command_prefix="python3 '$BLOG_DIR/scripts/blog/claude-minimax-producer.py'"
    provider=claude-minimax
  fi
  log "Invoking: $provider /blog-backfill $YESTERDAY $YESTERDAY (${2:-start}; timeout ${TIMEOUT_SECS}s, pty-wrapped)"
  t0=$(date +%s)
  # script(1) gives claude -p a pty so its CLI flushes incrementally instead of
  # buffering until SIGKILL — the precondition for diagnosing wall-time creep.
  if "${runner[@]}" env PATH="$PRODUCER_GUARD_DIR:$PATH" /usr/bin/timeout "$TIMEOUT_SECS" script -e -q -a -c \
      "$command_prefix -p \"\$(cat '$prompt_file')\" $session_flag '${BLOG_RUN_ID:-missing}' --dangerously-skip-permissions" "$LOG" >/dev/null 2>&1; then
    rm -f -- "$prompt_file"
    wall=$(( $(date +%s) - t0 ))
    log "claude -p exited cleanly after ${wall}s ($((wall/60))m $((wall%60))s)"
    verify_producer_contract || return 1
    PRODUCER_USED="$provider"
    PRODUCER_STATUS="OK ($provider)"
    return 0
  else
    exitc=$?
  fi
  rm -f -- "$prompt_file"
  LAST_PRODUCER_EXIT=$exitc
  wall=$(( $(date +%s) - t0 ))
  if [ "$exitc" = "124" ]; then
    log "claude -p TIMED OUT after ${wall}s (hard ceiling ${TIMEOUT_SECS}s)"
    PRODUCER_STATUS="FAILED (claude timeout exit 124)"
  else
    log "claude -p exited non-zero (exit $exitc) after ${wall}s"
    PRODUCER_STATUS="FAILED (claude exit $exitc)"
  fi
  return 1
}

run_grok_producer() {
  if [ ! -x "$GROK_BIN" ]; then
    log "Grok fallback skipped: GROK_BIN not executable ($GROK_BIN)"
    PRODUCER_STATUS="${PRODUCER_STATUS}; grok missing"
    return 1
  fi
  local prompt t0 exitc wall
  local -a runner=(python3 "$WORKSPACE_HELPER" run --manifest "$BLOG_RUN_MANIFEST" --)
  prompt="You are the /blog-backfill producer for startaitools.com. Target date: ${YESTERDAY}.
Follow /home/jeremy/.claude/skills/blog-backfill/SKILL.md and its references/ fully.
Produce ONLY: content/posts/<slug>.md + append methodology/decisions.jsonl (with agent_audit.audit_addendum) + the run-scoped .blog-staging/${YESTERDAY}.<run>.*.json records run-contract.md requires (classifier, audit, role outputs, roles receipt) + .blog-staging/${YESTERDAY}.intent.json ready:true only if every required gate passed including python3 .claude/skills/blog-backfill/scripts/lint-post-voice.py (hard ban em/en dashes and AI-slop phrases).
Do NOT git commit, push, dual-publish, or email. blog-land.sh handles land.
If a post for ${YESTERDAY} already exists, stop. Record producer as grok-fallback in agent_audit.writer."
  log "Invoking: grok fallback producer (timeout ${TIMEOUT_SECS}s) for ${YESTERDAY}"
  t0=$(date +%s)
  if "${runner[@]}" env PATH="$PRODUCER_GUARD_DIR:$PATH" /usr/bin/timeout "$TIMEOUT_SECS" "$GROK_BIN" \
      --cwd "$BLOG_DIR" \
      --permission-mode bypassPermissions \
      --always-approve \
      --max-turns "${BLOG_GROK_MAX_TURNS:-120}" \
      -p "$prompt" >>"$LOG" 2>&1; then
    wall=$(( $(date +%s) - t0 ))
    log "grok producer exited cleanly after ${wall}s ($((wall/60))m $((wall%60))s)"
    verify_producer_contract || return 1
    PRODUCER_USED="grok"
    PRODUCER_STATUS="OK (grok-fallback)"
    return 0
  else
    exitc=$?
  fi
  wall=$(( $(date +%s) - t0 ))
  if [ "$exitc" = "124" ]; then
    log "grok producer TIMED OUT after ${wall}s"
    PRODUCER_STATUS="${PRODUCER_STATUS}; grok timeout"
  else
    log "grok producer exited non-zero (exit $exitc) after ${wall}s"
    PRODUCER_STATUS="${PRODUCER_STATUS}; grok exit $exitc"
  fi
  return 1
}

run_minimax_producer() {
  if [ ! -x "$MINIMAX_AGENT" ]; then
    log "MiniMax fallback skipped: MINIMAX_AGENT not executable ($MINIMAX_AGENT)"
    PRODUCER_STATUS="${PRODUCER_STATUS}; minimax missing"
    return 1
  fi
  local prompt t0 exitc wall
  local -a runner=(python3 "$WORKSPACE_HELPER" run --manifest "$BLOG_RUN_MANIFEST" --)
  prompt="You are the /blog-backfill producer for startaitools.com. Target date: ${YESTERDAY}.
Follow /home/jeremy/.claude/skills/blog-backfill/SKILL.md and its references/ fully.
Produce ONLY: content/posts/<slug>.md + append methodology/decisions.jsonl (with agent_audit.audit_addendum) + the run-scoped .blog-staging/${YESTERDAY}.<run>.*.json records run-contract.md requires (classifier, audit, role outputs, roles receipt) + .blog-staging/${YESTERDAY}.intent.json ready:true only if every required gate passed including python3 .claude/skills/blog-backfill/scripts/lint-post-voice.py (hard ban em/en dashes and AI-slop phrases).
Do NOT git commit, push, dual-publish, or email. blog-land.sh handles land.
If a post for ${YESTERDAY} already exists, stop. Record producer as minimax-fallback in agent_audit.writer."
  log "Invoking: minimax fallback producer (timeout ${TIMEOUT_SECS}s) for ${YESTERDAY}"
  t0=$(date +%s)
  if "${runner[@]}" env PATH="$PRODUCER_GUARD_DIR:$PATH" /usr/bin/timeout "$TIMEOUT_SECS" "$MINIMAX_AGENT" \
      "$prompt" \
      --cwd "$BLOG_DIR" \
      --skill-dir "$HOME/.claude/skills/blog-backfill" \
      --max-turns "${BLOG_MINIMAX_MAX_TURNS:-120}" \
      --timeout "$TIMEOUT_SECS" >>"$LOG" 2>&1; then
    wall=$(( $(date +%s) - t0 ))
    log "minimax producer exited cleanly after ${wall}s ($((wall/60))m $((wall%60))s)"
    verify_producer_contract || return 1
    PRODUCER_USED="minimax"
    PRODUCER_STATUS="OK (minimax-fallback)"
    return 0
  else
    exitc=$?
  fi
  wall=$(( $(date +%s) - t0 ))
  if [ "$exitc" = "2" ]; then
    log "minimax producer EXCEEDED max-turns after ${wall}s"
    PRODUCER_STATUS="${PRODUCER_STATUS}; minimax max-turns"
  elif [ "$exitc" = "124" ] || [ "$exitc" = "3" ]; then
    log "minimax producer TIMED OUT after ${wall}s"
    PRODUCER_STATUS="${PRODUCER_STATUS}; minimax timeout"
  else
    log "minimax producer exited non-zero (exit $exitc) after ${wall}s"
    PRODUCER_STATUS="${PRODUCER_STATUS}; minimax exit $exitc"
  fi
  return 1
}

PRODUCER_HEAD=$(git -C "$BLOG_DIR" rev-parse HEAD)
# --- Catch-up of missed recent dates (startaitools-bhn.7, slice 2) -------------
# Repair and failover save a night when one attempt or one provider fails. They cannot
# save a night when everything is down. This does: after the night's own date, look back
# BLOG_CATCHUP_DAYS, find dates with no post on the deploy branch (one `git grep`), and
# run each as a QUIET child that may itself repair and fail over. Attempts per date are
# capped; a date that reaches the cap is reported ONCE, the only moment a human is needed.
# Only the scheduled run does this: an explicit --date run and every child skip it.
CATCHUP_HELPER="$(dirname "$SELF")/blog-catchup.py"
CATCHUP_STATE="${BLOG_CATCHUP_STATE:-$LOG_DIR/catchup-state.json}"
wait_for_release_to_settle() {
  # The lander's post push is a plain fast-forward push and the release bot commits to the
  # deploy branch minutes after every landing. Starting the next date before that settles
  # gets its push refused. Bounded; without gh, a fixed wait longer than a content release.
  local waited=0 limit="${BLOG_CATCHUP_SETTLE_SECS:-900}" busy
  command -v gh >/dev/null 2>&1 || { sleep "${BLOG_CATCHUP_BLIND_WAIT_SECS:-420}"; return 0; }
  sleep "${BLOG_CATCHUP_SETTLE_GRACE_SECS:-45}"
  while [ "$waited" -lt "$limit" ]; do
    # A gh that errors, is rate limited or prints junk tells us NOTHING. Treating that as
    # "settled" would defeat the wait; fall back to the blind wait instead.
    if ! busy=$(gh run list --workflow Release --limit 3 --json status \
        --repo "${BLOG_GH_REPO:-jeremylongshore/startaitools.com}" \
        -q '[.[]|select(.status!="completed")]|length' 2>/dev/null) \
        || ! [[ "$busy" =~ ^[0-9]+$ ]]; then
      log "CATCH-UP: release status unreadable; waiting ${BLOG_CATCHUP_BLIND_WAIT_SECS:-420}s blind"
      sleep "${BLOG_CATCHUP_BLIND_WAIT_SECS:-420}"
      return 0
    fi
    [ "$busy" = "0" ] && return 0
    sleep 20; waited=$((waited + 20))
  done
  log "CATCH-UP: release still busy after ${limit}s; proceeding"
}
run_catch_up() {
  [ "${BLOG_CATCHUP_DAYS:-3}" -gt 0 ] 2>/dev/null || return 0
  [ -z "${BLOG_CATCHUP_CHILD:-}" ] && [ "${BLOG_FAILOVER_DEPTH:-0}" = "0" ] || return 0
  [ -z "$TARGET_ARG" ] || [ "${BLOG_CATCHUP_FORCE:-0}" = "1" ] || return 0
  [ "${BLOG_RECOVERY:-1}" = "1" ] && [ -f "$CATCHUP_HELPER" ] || return 0
  local plan_json date deadline rc landed=0 offset remaining
  deadline=$(( $(date +%s) + ${BLOG_CATCHUP_BUDGET_SECS:-14400} ))
  git -C "$BLOG_SOURCE_DIR" fetch --quiet origin "${BLOG_DEPLOY_BRANCH:-master}" >> "$LOG" 2>&1 || true
  plan_json=$(python3 "$CATCHUP_HELPER" --state "$CATCHUP_STATE" plan --repo "$BLOG_SOURCE_DIR" \
    --ref "${BLOG_CATCHUP_REF:-origin/${BLOG_DEPLOY_BRANCH:-master}}" --target "$YESTERDAY" \
    --days "${BLOG_CATCHUP_DAYS:-3}" --max-attempts "${BLOG_CATCHUP_MAX_ATTEMPTS:-3}" 2>>"$LOG") || return 0
  log "CATCH-UP: plan=$plan_json"
  case "$STATUS" in OK*|PENDING*) landed=1 ;; esac
  for date in $(printf '%s' "$plan_json" | jq -r '.attempt[]?' 2>/dev/null); do
    if [ "$(date +%s)" -ge "$deadline" ]; then log "CATCH-UP: time budget spent; ${date} waits for the next run"; break; fi
    [ "$landed" -eq 1 ] && wait_for_release_to_settle
    python3 "$CATCHUP_HELPER" --state "$CATCHUP_STATE" record --date "$date" --outcome attempt >> "$LOG" 2>&1
    log "CATCH-UP: ${date} has no post on the deploy branch; running it now, quietly"
    offset=$(stat -c %s "$LOG_DIR/run-${date}.log" 2>/dev/null || echo 0)
    # The budget is checked before each child AND enforced on it: a running child is killed
    # at the deadline, so the whole night has a hard ceiling and cannot run into the next
    # 04:00 fire, where it would hold the lock and that night's run would exit as LOCKED.
    remaining=$(( deadline - $(date +%s) )); [ "$remaining" -lt 60 ] && remaining=60
    timeout --signal=TERM --kill-after=120 "$remaining" \
    env -u BLOG_RUN_MANIFEST -u BLOG_RUN_ID -u BLOG_INCIDENT_ID -u BLOG_STATE_DIR \
        -u BLOG_RUN_DIAGNOSTICS_DIR -u BLOG_RUN_WORKSPACE_HELPER -u BLOG_PRODUCER_TRANSCRIPT \
        -u REAL_GIT_BIN -u BLOG_DIR -u BLOG_TARGET_DATE -u BLOG_RECOVERY_DEADLINE \
        BLOG_REPO_DIR="$BLOG_SOURCE_DIR" BLOG_CATCHUP_CHILD=1 BLOG_QUIET_FAILURE=1 \
        BLOG_PIPELINE_LOCK_INHERITED=1 \
      "$SELF" --date "$date" >/dev/null 2>&1
    rc=$?
    if [ "$rc" -eq 0 ] && tail -c +"$((offset + 1))" "$LOG_DIR/run-${date}.log" 2>/dev/null \
        | grep -Eq 'Overall STATUS: (OK|PENDING)|generation is idempotent'; then
      python3 "$CATCHUP_HELPER" --state "$CATCHUP_STATE" record --date "$date" --outcome published >> "$LOG" 2>&1
      log "CATCH-UP: ${date} recovered; no human involved"
      landed=1
    else
      log "CATCH-UP: ${date} still missing (rc=$rc); it will be tried again at the next run"
      landed=0
    fi
  done
  for date in $(printf '%s' "$plan_json" | jq -r '.newly_gave_up[]?' 2>/dev/null); do
    log "CATCH-UP: GAVE UP on ${date} after ${BLOG_CATCHUP_MAX_ATTEMPTS:-3} attempts; this needs a human"
    if [ "${BLOG_CANARY:-0}" != "1" ]; then
      cron_fail "blog-backfill-daily" "${date}: NO POST after ${BLOG_CATCHUP_MAX_ATTEMPTS:-3} automatic catch-up attempts. Logs: $LOG_DIR/run-${date}.log. Recover with: $SELF --date ${date}"
    fi
    python3 "$CATCHUP_HELPER" --state "$CATCHUP_STATE" record --date "$date" --outcome gave-up-reported >> "$LOG" 2>&1
  done
}

# A published-but-not-yet-live post is the wrapper's call (PENDING), so the lander must not
# page for it as well. Same switch as the rest of recovery.
if [ "${BLOG_RECOVERY:-1}" = "1" ] && [ "${BLOG_CANARY:-0}" != "1" ]; then
  export BLOG_LAND_QUIET_UNAVAILABLE=1
fi

PRODUCER_ACCEPTED=0
case "$PRODUCER_MODE" in
  grok)
    if run_grok_producer; then PRODUCER_ACCEPTED=1; fi
    ;;
  claude)
    if run_claude_producer; then PRODUCER_ACCEPTED=1; fi
    ;;
  minimax)
    if run_minimax_producer; then PRODUCER_ACCEPTED=1; fi
    ;;
  auto|*)
    # A shell-only fallback cannot execute the mandatory independent Agent gates.
    # Only process success AND the full verified contract authorize landing.
    if run_claude_producer; then PRODUCER_ACCEPTED=1; fi
    ;;

esac

# --- Recovery, part 1: repair rounds (startaitools-bhn.7) ----------------------
# A finished post the contract refused for a nameable reason is not worth a human.
# Hand the verifier's exact message back to the SAME session in the SAME workspace,
# at most BLOG_REPAIR_ROUNDS times. The router (blog-recovery.py) matches our own
# error strings first and asks a cheap model only about failures it does not
# recognise. The loop may fix the POST; it never edits the pipeline, never touches
# git, and the contract re-verifies after every round exactly as it does after the
# first attempt. Off in canary mode unless BLOG_RECOVERY=1 is set explicitly, so
# refusal scenarios stay refusal scenarios.
RECOVERY_HELPER="$(dirname "$SELF")/blog-recovery.py"
RECOVERY_DEFAULT=1; [ "${BLOG_CANARY:-0}" = "1" ] && RECOVERY_DEFAULT=0
BLOG_RECOVERY="${BLOG_RECOVERY:-$RECOVERY_DEFAULT}"
REPAIR_ROUNDS="${BLOG_REPAIR_ROUNDS:-2}"
# ONE wall-clock budget for the whole date, shared with the failover child: worst case is
# 1 + 2 repairs in each of two runs at up to TIMEOUT_SECS apiece, which unbounded could run
# into the next night's fire. Past the deadline nothing new is started.
RECOVERY_DEADLINE="${BLOG_RECOVERY_DEADLINE:-$(( $(date +%s) + ${BLOG_RECOVERY_BUDGET_SECS:-10800} ))}"
RECOVERY_ACTION=""
RECOVERY_ROUND=0
ATTEMPT_LOG_OFFSET=${ATTEMPT_LOG_OFFSET:-0}
recovery_decide() {
  local evidence decision
  evidence=$(mktemp "$LOG_DIR/.recovery-evidence.XXXXXX") || return 1
  # Only THIS attempt's output: an earlier, already-handled error must not be re-read.
  tail -c +"$((ATTEMPT_LOG_OFFSET + 1))" "$LOG" 2>/dev/null | tail -c 20000 > "$evidence"
  [ -n "${BLOG_RUN_MANIFEST:-}" ] && tail -c 6000 "$(dirname "$BLOG_RUN_MANIFEST")/producer.log" >> "$evidence" 2>/dev/null
  decision=$(python3 "$RECOVERY_HELPER" classify --exit-code "$LAST_PRODUCER_EXIT" \
    --evidence-file "$evidence" --verifier-file "${VERIFIER_CAPTURE:-}" --ask-model 2>>"$LOG") || decision=""
  rm -f -- "$evidence"
  printf '%s' "$decision"
}
case "$PRODUCER_MODE" in auto|claude) RECOVERY_CAPABLE=1 ;; *) RECOVERY_CAPABLE=0 ;; esac
while [ "$PRODUCER_ACCEPTED" -ne 1 ] && [ "$BLOG_RECOVERY" = "1" ] && [ "$RECOVERY_CAPABLE" -eq 1 ] \
    && [ -f "$RECOVERY_HELPER" ]; do
  RECOVERY_DECISION=$(recovery_decide)
  RECOVERY_ACTION=$(printf '%s' "$RECOVERY_DECISION" | jq -r '.action // empty' 2>/dev/null)
  RECOVERY_DETAIL=$(printf '%s' "$RECOVERY_DECISION" | jq -r '.detail // empty' 2>/dev/null)
  log "RECOVERY: decision=${RECOVERY_DECISION:-unavailable}"
  if [ "$RECOVERY_ACTION" != "repair" ] || [ "$RECOVERY_ROUND" -ge "$REPAIR_ROUNDS" ]; then
    break
  fi
  if [ "$(date +%s)" -ge "$RECOVERY_DEADLINE" ]; then log "RECOVERY: time budget spent; no further repair"; break; fi
  if [ "$(git -C "$BLOG_DIR" rev-parse HEAD)" != "$PRODUCER_HEAD" ]; then break; fi
  RECOVERY_ROUND=$((RECOVERY_ROUND + 1))
  REPAIR_PROMPT=$(python3 "$RECOVERY_HELPER" repair-prompt --date "$YESTERDAY" \
    --reason="$RECOVERY_DETAIL" --round "$RECOVERY_ROUND" --rounds "$REPAIR_ROUNDS") || break
  log "RECOVERY: repair round ${RECOVERY_ROUND}/${REPAIR_ROUNDS}; reason: ${RECOVERY_DETAIL:-none captured}"
  ATTEMPT_LOG_OFFSET=$(stat -c %s "$LOG" 2>/dev/null || echo 0)
  if run_claude_producer "$REPAIR_PROMPT" resume; then
    PRODUCER_ACCEPTED=1
    log "RECOVERY: repaired in round ${RECOVERY_ROUND}; no human involved"
  fi
done
# The captured verifier output has served its purpose; the full text is in the run log.
case "${VERIFIER_CAPTURE:-}" in ""|/dev/null) : ;; *) rm -f -- "$VERIFIER_CAPTURE" ;; esac
if [ "$(git -C "$BLOG_DIR" rev-parse HEAD)" != "$PRODUCER_HEAD" ]; then
  log "FATAL: producer changed Git HEAD; producer/lander boundary was violated. Refusing to land or push additional state."
  exit 1
fi
rm -rf "$PRODUCER_GUARD_DIR"
PRODUCER_GUARD_DIR=""
# Backward-compatible name used in the summary email below.
CLAUDE_STATUS="${PRODUCER_STATUS} [producer=${PRODUCER_USED:-none}]"

# --- Land: deterministic verify → commit → push → publish → OR quarantine ----
# Artifact readiness cannot override a failed/timed-out producer or failed
# contract. Quarantine below preserves evidence without entering publication.
if [ "$PRODUCER_ACCEPTED" -eq 1 ]; then
  log "Invoking blog-land.sh for $YESTERDAY..."
  if [ "${BLOG_CANARY:-0}" = "1" ]; then
    "$LAND_SCRIPT" "$YESTERDAY" --dry-run >> "$LOG" 2>&1
  else
    "$LAND_SCRIPT" "$YESTERDAY" >> "$LOG" 2>&1
  fi
  LAND_RC=$?
  LAND_RESULT=$(grep -oE 'LAND-RESULT: .*' "$LOG" | tail -1 | sed 's/LAND-RESULT: //')
  log "blog-land.sh returned rc=$LAND_RC (${LAND_RESULT:-unknown})"
else
  LAND_RC=22  # Wrapper disposition; the lander was never invoked.
  LAND_RESULT="SKIPPED (producer was not accepted)"
  FAIL_REASON="producer was not accepted: $PRODUCER_STATUS"
  log "LAND-SKIPPED: $FAIL_REASON; preserving owned run without publication"
fi

# Map land rc + claude status → overall STATUS.
case "$LAND_RC" in
  0)  STATUS="OK" ;;
  3)  STATUS="FAILED (legacy lander reported public article unavailable)" ;;
  10) STATUS="FAILED (QUARANTINED — preconditions failed; evidence preserved)" ;;
  11) STATUS="FAILED (land infra — orphaned local commit, manual push needed)" ;;
  12) STATUS="FAILED (land BLOCKED before commit — nothing orphaned; re-run land from a normal shell)" ;;
  13) # Published, not yet live. Not a failed night: the source is on the deploy branch
      # and the sealed run is retained, so the next run's startup recovery completes
      # delivery once the page answers. A date that stays dark surfaces there as
      # "older delivery recovery pending", which DOES page.
      STATUS="PENDING (published; page not live within ${BLOG_LAND_LIVENESS_SECS:-1500}s; delivery completes at the next run)" ;;
  14) STATUS="FAILED (source published; ledger/queue delivery remains pending)" ;;
  20) case "$PRODUCER_STATUS" in
        OK*) STATUS="FAILED (no post; no validated no-activity receipt)" ;;
        *)   STATUS="FAILED (${PRODUCER_STATUS}, no post produced)" ;;
      esac ;;
  21) STATUS="OK (already landed)" ;;
  22) STATUS="FAILED (producer rejected; ${PRODUCER_STATUS}; land not invoked)" ;;
  *)  STATUS="FAILED (land rc=$LAND_RC)" ;;
esac
# Deploy patience, the one active step: nudge the deploy ONCE. Kept OUT of the pure status
# mapping above on purpose: unit tests execute that case block, and a test must never be
# able to reach a real GitHub call. Refused harmlessly if no release exists yet.
if [ "$LAND_RC" -eq 13 ] && [ "${BLOG_CANARY:-0}" != "1" ] && [ "${BLOG_RECOVERY:-1}" = "1" ] \
    && command -v gh >/dev/null 2>&1; then
  if gh workflow run deploy.yml --ref "${BLOG_DEPLOY_BRANCH:-master}" \
      --repo "${BLOG_GH_REPO:-jeremylongshore/startaitools.com}" >> "$LOG" 2>&1; then
    log "DEPLOY-PATIENCE: dispatched deploy.yml once"
  else
    log "DEPLOY-PATIENCE: deploy.yml dispatch not accepted; the release pipeline will deploy"
  fi
fi
if [ "$RECOVERY_DEGRADED" -eq 1 ]; then
  STATUS="FAILED (older delivery recovery pending; current target: $STATUS)"
fi
if [ "$LAND_RC" -eq 20 ] || [ "$PRODUCER_ACCEPTED" -ne 1 ] || [ "${BLOG_CANARY:-0}" = "1" ]; then
  python3 "$WORKSPACE_HELPER" quarantine --manifest "$BLOG_RUN_MANIFEST" \
    --reason "${STATUS}; canary=${BLOG_CANARY:-0}; no publication" >> "$LOG" 2>&1 || {
    log "QUARANTINE-PENDING: manifest=$BLOG_RUN_MANIFEST; original workspace/evidence retained; prior=$STATUS"
    STATUS="FAILED (quarantine pending; original evidence retained; prior=$STATUS)"
  }
fi
# --- Recovery, part 2: provider failover (startaitools-bhn.7) ------------------
# The other full-toolchain provider gets ONE fresh run: a new session id and a new
# workspace, because a second provider cannot reuse the first one's session. This run
# is already quarantined above, so nothing is shared but the date and the lock.
# Depth-capped at 1: a failover child never fails over again, and it stays quiet on
# failure so the parent sends the single alert. "stop" means integrity damage; then
# nothing is retried here.
FAILOVER_NOTE=""
if [ "$PRODUCER_ACCEPTED" -ne 1 ] && [ "$BLOG_RECOVERY" = "1" ] && [ "$RECOVERY_CAPABLE" -eq 1 ] \
    && [ "${BLOG_FAILOVER_DEPTH:-0}" = "0" ] && [ "${BLOG_PRODUCER_FAILOVER:-1}" = "1" ] \
    && [ "$RECOVERY_ACTION" != "stop" ] && [ "$(date +%s)" -lt "$RECOVERY_DEADLINE" ]; then
  case "$PRODUCER_MODE" in claude) FAILOVER_TO=auto ;; *) FAILOVER_TO=claude ;; esac
  log "FAILOVER: ${PRODUCER_MODE} did not produce ${YESTERDAY} (${PRODUCER_STATUS}); one fresh run on '${FAILOVER_TO}'"
  FAILOVER_OFFSET=$(stat -c %s "$LOG" 2>/dev/null || echo 0)
  # The child is a whole new run and must start from the SOURCE repo. This run re-pointed
  # BLOG_REPO_DIR (and friends) at its own isolated workspace for the producer; inherited
  # as-is, the child would register that workspace as the source repo and the registry
  # would refuse it ("publication owner mismatch").
  env -u BLOG_RUN_MANIFEST -u BLOG_RUN_ID -u BLOG_INCIDENT_ID -u BLOG_STATE_DIR \
      -u BLOG_RUN_DIAGNOSTICS_DIR -u BLOG_RUN_WORKSPACE_HELPER -u BLOG_PRODUCER_TRANSCRIPT \
      -u REAL_GIT_BIN -u BLOG_DIR -u BLOG_TARGET_DATE \
      BLOG_REPO_DIR="$BLOG_SOURCE_DIR" BLOG_PRODUCER="$FAILOVER_TO" BLOG_FAILOVER_DEPTH=1 \
      BLOG_PIPELINE_LOCK_INHERITED=1 BLOG_RECOVERY_DEADLINE="$RECOVERY_DEADLINE" \
    "$SELF" --date "$YESTERDAY" >/dev/null 2>&1
  FAILOVER_RC=$?
  # PENDING counts: the child PUBLISHED and the page is merely slow. Reading that as a failed
  # failover would page at 4am for a night that succeeded (independent review of #96).
  if [ "$FAILOVER_RC" -eq 0 ] && tail -c +"$((FAILOVER_OFFSET + 1))" "$LOG" \
      | grep -Eq 'Overall STATUS: (OK|PENDING)|generation is idempotent'; then
    log "FAILOVER: ${YESTERDAY} published by '${FAILOVER_TO}'; no human involved"
    # The child already sent the normal summary and wrote liveness; do not alert.
    NOTIFIED=1
    log "=== Daily blog-backfill end (recovered by failover) ==="
    run_catch_up
    exit 0
  fi
  FAILOVER_NOTE="; failover to '${FAILOVER_TO}' also failed (rc=${FAILOVER_RC})"
  STATUS="${STATUS}${FAILOVER_NOTE}"
fi
log "Overall STATUS: $STATUS"

# --- Canonical index from committed source, never unpublished producer files --
REBUILD="$(dirname "$SELF")/blog-methodology-published-index.py"
REBUILD_COMMAND=(rebuild_canonical_index)
if [ "${BLOG_CANARY:-0}" = "1" ]; then
  # Unpublished canary analytics belong only to its isolated workspace.
  REBUILD="$BLOG_DIR/.claude/skills/blog-backfill/scripts/rebuild-methodology-index.sh"
  REBUILD_COMMAND=("$REBUILD")
fi
if [ -f "$REBUILD" ]; then
  log "Rebuilding methodology index (canary=${BLOG_CANARY:-0}; production uses authoritative committed source)..."
  if ! "${REBUILD_COMMAND[@]}" >> "$LOG" 2>&1; then
    log "ERROR: methodology index integrity failed; last-good index preserved"
    STATUS="FAILED (methodology index integrity; ${STATUS})"
  fi
else
  log "ERROR: required methodology consumer is missing"
  STATUS="FAILED (missing methodology consumer; ${STATUS})"
fi

if [ "${BLOG_CANARY:-0}" = "1" ]; then
  log "CANARY-RESULT: $STATUS; land_rc=$LAND_RC; no publication, ledger mutation or production notification"
  run_catch_up   # a no-op here unless BLOG_CATCHUP_FORCE=1: a canary is always an explicit --date run
  case "$STATUS" in FAILED*) exit 1 ;; *) exit 0 ;; esac
fi

# --- Bounded retention + storage census (this job's own footprint only) ------
# Completed owned checkouts retire during admission after durable evidence and
# identity verification. Quarantine and unfinished work are counted, never pruned.
PRUNED=$(prune_run_logs "$LOG_DIR" "${BLOG_BACKFILL_LOG_KEEP_DAYS:-180}" "$LOG")
QUARANTINE_NOTE=""
if ! quarantine_census "$BLOG_SOURCE_DIR/.blog-quarantine" "${BLOG_QUARANTINE_MAX_ENTRIES:-12}" "$LOG"; then
  QUARANTINE_NOTE=" — QUARANTINE OVER LINE (${QUARANTINE_COUNT} entries)"
fi
REGISTRY_NOTE="unavailable"
REGISTRY_RESULT=$(python3 "$WORKSPACE_HELPER" census --repo "$BLOG_SOURCE_DIR" \
  --state-dir "${BLOG_RUN_STATE_DIR:-$HOME/.local/state/blog-run-workspaces}" 2>> "$LOG")
REGISTRY_RC=$?
if [ "$REGISTRY_RC" -ne 0 ] || ! printf '%s' "$REGISTRY_RESULT" | jq -e '
  (.registry_bytes | type == "number" and . >= 0) and
  (.workspace_bytes | type == "number" and . >= 0) and
  (.protected_bytes | type == "number" and . >= 0) and
  (.runs | type == "array") and
  all(.runs[]; (.status | type == "string") and
    (.workspace_bytes | type == "number" and . >= 0) and
    (.quarantine_bytes | type == "number" and . >= 0))' > /dev/null; then
  log "ERROR: external run-registry census failed validation"
  STATUS="FAILED (run-registry storage census; ${STATUS})"
else
  EXTERNAL_QUARANTINE_COUNT=$(printf '%s' "$REGISTRY_RESULT" | jq '[.runs[] | select(.status == "quarantined")] | length')
  EXTERNAL_QUARANTINE_BYTES=$(printf '%s' "$REGISTRY_RESULT" | jq '[.runs[] | select(.status == "quarantined") | .workspace_bytes + .quarantine_bytes] | add // 0')
  QUARANTINE_COUNT=$((QUARANTINE_COUNT + EXTERNAL_QUARANTINE_COUNT))
  REGISTRY_NOTE=$(printf '%s' "$REGISTRY_RESULT" | jq -c '{registry_bytes,workspace_bytes,protected_bytes,runs:(.runs|length)}')
  log "RUN-REGISTRY-CENSUS: $REGISTRY_NOTE; external_quarantined=$EXTERNAL_QUARANTINE_COUNT; protected_quarantine_bytes=$EXTERNAL_QUARANTINE_BYTES"
  if [ "$QUARANTINE_COUNT" -gt "${BLOG_QUARANTINE_MAX_ENTRIES:-12}" ]; then
    QUARANTINE_NOTE=" — QUARANTINE OVER LINE (${QUARANTINE_COUNT} entries across owner and external registry)"
    log "WARN: $QUARANTINE_NOTE; evidence remains protected"
  fi
fi

# --- Consecutive-failure escalation ------------------------------------------
CONSEC_FAILS=$(count_consecutive_failures "$LOG_DIR" "run-*.log" "FATAL|TIMED OUT|FAILED \(" 10)
ESCALATE_PREFIX=""
if [ "$CONSEC_FAILS" -ge 3 ]; then
  log "ESCALATION: ${CONSEC_FAILS} consecutive failed runs detected — elevating alert priority"
  ESCALATE_PREFIX="🚨 ${CONSEC_FAILS}-DAY STREAK: "
fi

# Buzz sys-automation on a hard failure only (reads governed Buzz dispatch).
FAILOVER_CHILD_FAILED=0
case "$STATUS" in FAILED*)
  if [ "${BLOG_FAILOVER_DEPTH:-0}" != "0" ] || [ "${BLOG_QUIET_FAILURE:-0}" = "1" ]; then FAILOVER_CHILD_FAILED=1; fi ;;
esac
case "$STATUS" in
  FAILED*)
    if [ "$FAILOVER_CHILD_FAILED" -eq 1 ]; then
      log "QUIET-CHILD: failed quietly; the parent run owns alerting for this date"
    else
      cron_fail "blog-backfill-daily" "${ESCALATE_PREFIX}${YESTERDAY}: ${STATUS} (${CONSEC_FAILS}-day streak). Log: $LOG"
    fi ;;
esac

# --- Summary email -----------------------------------------------------------
TAIL=$(tail -50 "$LOG")
BODY="Daily /blog-backfill run for ${YESTERDAY}
Status: ${STATUS}
Land result: ${LAND_RESULT:-n/a} (rc=${LAND_RC})
Producer: ${CLAUDE_STATUS}
Consecutive failures (incl. this run): ${CONSEC_FAILS}
Disk: ${DISK_GUARD_FREE_MB:-?}MiB free on ${DISK_GUARD_MOUNT:-/} (floor ${DISK_MIN_MB}MiB, warn ${DISK_WARN_MB}MiB)${DISK_WARNING:+ — WARNING: under the early-warning line}
Quarantine: ${QUARANTINE_COUNT:-0} entries across owner and external registry; owner evidence ${QUARANTINE_MB:-0}MiB; external protected evidence ${EXTERNAL_QUARANTINE_BYTES:-unknown} bytes${QUARANTINE_NOTE}
Run registry: ${REGISTRY_NOTE}
Run-log retention: ${PRUNED:-0} log(s) older than ${BLOG_BACKFILL_LOG_KEEP_DAYS:-180}d removed
Recovery command for a missed day: ${RECOVERY_CMD}

================================================================================
Last 50 log lines (full log: ${LOG}):
================================================================================

${TAIL}
"
DISK_PREFIX=""; [ -n "$DISK_WARNING" ] && DISK_PREFIX="⚠️ DISK ${DISK_GUARD_FREE_MB}MiB: "
SUBJECT="${ESCALATE_PREFIX}${DISK_PREFIX}Daily blog-backfill: ${YESTERDAY} — ${STATUS}${QUARANTINE_NOTE}"
if [ "$FAILOVER_CHILD_FAILED" -eq 1 ]; then
  :  # quiet: see above
elif ! send_notification "$SUBJECT" "$BODY" >> "$LOG" 2>&1; then
  log "ERROR: email notification failed; run remains unhealthy — see log"
  STATUS="FAILED (notification delivery failed; prior land result: ${LAND_RESULT:-n/a})"
fi

# Failure alerting is handled above by cron_fail (#cron-failures) + the summary
# email; success/status is silent now (ntfy retired 2026-06-13).

# Normal notification path completed — disarm the fail-loud trap.
NOTIFIED=1
log "=== Daily blog-backfill end ==="

# Exit truthfully for the liveness trap (review finding on PR #26): a handled
# failure must still exit non-zero so the EXIT trap withholds .ok and the estate
# sweep's running-but-failing signal stays live. NOTIFIED=1 above guarantees the
# trap does NOT double-alert.
run_catch_up
case "$STATUS" in OK*|PENDING*) : ;; *) exit 1 ;; esac
