#!/usr/bin/env bash
# Daily autonomous blog pipeline. Runs at 04:00 local host time via cron.
#
# ARCHITECTURE (inverted 2026-07-05): the LLM PRODUCES, deterministic code LANDS.
#   1. preflight: lock, disk guard, clean-tree + default-branch normalize
#   2. Producer writes the post + decisions + readiness sentinel (no git):
#      primary `claude -p /blog-backfill`; on failure with no post on disk,
#      Grok headless fallback (BLOG_PRODUCER=auto|claude|grok).
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

LOG_DIR=/home/jeremy/.local/state/blog-backfill-daily
BLOG_DIR=/home/jeremy/000-projects/blog/startaitools
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
mkdir -p "$HOME/.local/state/intent-os/liveness" 2>/dev/null || true
: > "$HOME/.local/state/intent-os/liveness/blog-backfill-daily.beat" 2>/dev/null || true

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
RECOVERY_CMD="$SELF --date $YESTERDAY"
FAIL_REASON=""

log() { echo "[$(date -Is)] $*" | tee -a "$LOG"; }
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
  local rc=$?
  [ -z "${PRODUCER_GUARD_DIR:-}" ] || rm -rf "$PRODUCER_GUARD_DIR"
  liveness_markers "blog-backfill-daily" "$rc"   # .beat every run; .ok iff rc==0
  [ "$rc" -eq 0 ] && return
  [ "$NOTIFIED" -eq 1 ] && return
  log "ABNORMAL EXIT (rc=$rc) before normal notification — sending fail-loud alert"
  # Everything an operator needs to act without opening the box: the date that
  # has no post, why, where the log is, the capacity numbers, and the one
  # command that recovers the day once the cause is fixed.
  local detail free_line
  free_line="disk: ${DISK_GUARD_FREE_MB:-unknown}MiB free on ${DISK_GUARD_MOUNT:-/}, floor ${DISK_MIN_MB}MiB, warn ${DISK_WARN_MB}MiB"
  detail="${YESTERDAY}: NO POST — early exit rc=${rc}"
  [ -n "$FAIL_REASON" ] && detail="${detail}; reason: ${FAIL_REASON}"
  detail="${detail}; ${free_line}; log: ${LOG}; recover with: ${RECOVERY_CMD}"
  cron_fail "blog-backfill-daily" "$detail"
  node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io \
    --subject "🚨 blog-backfill aborted early: ${YESTERDAY} (rc=${rc})${FAIL_REASON:+ — ${FAIL_REASON%%:*}}" \
    --body "$(printf 'Daily blog-backfill exited abnormally (rc=%s) BEFORE its normal summary email.\n\nTarget date : %s (NO POST landed)\nReason      : %s\nCapacity    : %s\nLog         : %s\n\nRecovery (idempotent, safe to re-run once the cause is fixed):\n  %s\n  %s --sweep\nRunbook: %s\n\nLast 30 log lines:\n--------------------------------------------------------------------------------\n%s\n' "$rc" "$YESTERDAY" "${FAIL_REASON:-see log}" "$free_line" "$LOG" "$RECOVERY_CMD" "$BLOG_DIR/scripts/blog/blog-posting-packet.sh" "$RUNBOOK" "$(tail -30 "$LOG" 2>/dev/null)")" \
    >/dev/null 2>&1 || true
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

# --- Pre-flight: clean tree, on default branch, fast-forward ------------------
# This runs BEFORE generation. The tree MUST be clean here (yesterday's post was
# committed by yesterday's land step). A dirty tree means external uncommitted
# work — legitimately abort. May repoint BLOG_DIR if pivoting to a worktree.
preflight_branch_normalize "$BLOG_DIR" "$LOG"
POSTS_DIR="$BLOG_DIR/content/posts"
LAND_SCRIPT="$BLOG_DIR/scripts/blog/blog-land.sh"

# --- Publication-aware idempotency -------------------------------------------
# A producer orphan on disk is not a published post. Only a tracked, unchanged
# post on the normalized deploy branch covers the date. Even on a covered date,
# sweep due cross-posts before exiting so the API queue cannot stall.
if EXISTING=$(published_post_for_date "$BLOG_DIR" "$POSTS_DIR" "$YESTERDAY"); then
  log "Published post already covers $YESTERDAY ($EXISTING) — generation is a no-op."
  "$BLOG_DIR/scripts/blog/blog-crosspost-sweep.sh" >> "$LOG" 2>&1 || {
    log "FATAL: independent cross-post sweep failed on idempotent run"
    exit 1
  }
  NOTIFIED=1
  exit 0
fi
if LOCAL_ONLY=$(post_exists_for_date "$POSTS_DIR" "$YESTERDAY"); then
  log "FATAL: local post for $YESTERDAY is not tracked and clean ($LOCAL_ONLY); refusing to treat producer debris as published"
  exit 1
fi

# --- Generate: LLM produces artifacts ONLY (no git) --------------------------
# Primary: claude -p /blog-backfill. Fallback: grok headless (BLOG_PRODUCER=auto
# by default) when Claude is rate-limited or otherwise fails. Commit/publish stay
# in blog-land.sh either way — a producer failure still runs land (quarantine or
# no-op). Incident 2026-07-15: Claude weekly limit left NO-POST; Grok recovered.
TIMEOUT_SECS="${BLOG_BACKFILL_TIMEOUT:-2700}"
GROK_BIN="${GROK_BIN:-$HOME/.grok/bin/grok}"
MINIMAX_AGENT="${MINIMAX_AGENT:-$HOME/.local/bin/minimax-agent.py}"
# auto (default) = claude then minimax (since 2026-07-24: grok Build usage
# exhausted 402; MiniMax is the new fallback). claude = claude only; minimax =
# minimax only; grok = legacy, kept available but not in the auto chain.
PRODUCER_MODE="${BLOG_PRODUCER:-auto}"
PRODUCER_USED=""
PRODUCER_STATUS="NOT-RUN"
post_exists_now() { post_exists_for_date "$POSTS_DIR" "$YESTERDAY" >/dev/null 2>&1; }

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

run_claude_producer() {
  log "Invoking: claude -p /blog-backfill $YESTERDAY $YESTERDAY (timeout ${TIMEOUT_SECS}s, pty-wrapped)"
  local t0 exitc wall
  t0=$(date +%s)
  # script(1) gives claude -p a pty so its CLI flushes incrementally instead of
  # buffering until SIGKILL — the precondition for diagnosing wall-time creep.
  if env PATH="$PRODUCER_GUARD_DIR:$PATH" /usr/bin/timeout "$TIMEOUT_SECS" script -e -q -a -c \
      "claude -p '/blog-backfill $YESTERDAY $YESTERDAY' --dangerously-skip-permissions" "$LOG" >/dev/null 2>&1; then
    wall=$(( $(date +%s) - t0 ))
    log "claude -p exited cleanly after ${wall}s ($((wall/60))m $((wall%60))s)"
    PRODUCER_USED="claude"
    PRODUCER_STATUS="OK"
    return 0
  fi
  exitc=$?
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
  prompt="You are the /blog-backfill producer for startaitools.com. Target date: ${YESTERDAY}.
Follow /home/jeremy/.claude/skills/blog-backfill/SKILL.md and its references/ fully.
Produce ONLY: content/posts/<slug>.md + append methodology/decisions.jsonl (with agent_audit.audit_addendum) + .blog-staging/${YESTERDAY}.intent.json ready:true only if every required gate passed including python3 .claude/skills/blog-backfill/scripts/lint-post-voice.py (hard ban em/en dashes and AI-slop phrases).
Do NOT git commit, push, dual-publish, or email. blog-land.sh handles land.
If a post for ${YESTERDAY} already exists, stop. Record producer as grok-fallback in agent_audit.writer."
  log "Invoking: grok fallback producer (timeout ${TIMEOUT_SECS}s) for ${YESTERDAY}"
  t0=$(date +%s)
  if env PATH="$PRODUCER_GUARD_DIR:$PATH" /usr/bin/timeout "$TIMEOUT_SECS" "$GROK_BIN" \
      --cwd "$BLOG_DIR" \
      --permission-mode bypassPermissions \
      --always-approve \
      --max-turns "${BLOG_GROK_MAX_TURNS:-120}" \
      -p "$prompt" >>"$LOG" 2>&1; then
    wall=$(( $(date +%s) - t0 ))
    log "grok producer exited cleanly after ${wall}s ($((wall/60))m $((wall%60))s)"
    PRODUCER_USED="grok"
    PRODUCER_STATUS="OK (grok-fallback)"
    return 0
  fi
  exitc=$?
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
  prompt="You are the /blog-backfill producer for startaitools.com. Target date: ${YESTERDAY}.
Follow /home/jeremy/.claude/skills/blog-backfill/SKILL.md and its references/ fully.
Produce ONLY: content/posts/<slug>.md + append methodology/decisions.jsonl (with agent_audit.audit_addendum) + .blog-staging/${YESTERDAY}.intent.json ready:true only if every required gate passed including python3 .claude/skills/blog-backfill/scripts/lint-post-voice.py (hard ban em/en dashes and AI-slop phrases).
Do NOT git commit, push, dual-publish, or email. blog-land.sh handles land.
If a post for ${YESTERDAY} already exists, stop. Record producer as minimax-fallback in agent_audit.writer."
  log "Invoking: minimax fallback producer (timeout ${TIMEOUT_SECS}s) for ${YESTERDAY}"
  t0=$(date +%s)
  if env PATH="$PRODUCER_GUARD_DIR:$PATH" /usr/bin/timeout "$TIMEOUT_SECS" "$MINIMAX_AGENT" \
      "$prompt" \
      --cwd "$BLOG_DIR" \
      --skill-dir "$HOME/.claude/skills/blog-backfill" \
      --max-turns "${BLOG_MINIMAX_MAX_TURNS:-120}" \
      --timeout "$TIMEOUT_SECS" >>"$LOG" 2>&1; then
    wall=$(( $(date +%s) - t0 ))
    log "minimax producer exited cleanly after ${wall}s ($((wall/60))m $((wall%60))s)"
    PRODUCER_USED="minimax"
    PRODUCER_STATUS="OK (minimax-fallback)"
    return 0
  fi
  exitc=$?
  wall=$(( $(date +%s) - t0 ))
  if [ "$exitc" = "2" ]; then
    log "minimax producer EXCEEDED max-turns after ${wall}s"
    PRODUCER_STATUS="${PRODUCER_STATUS}; minimax max-turns"
  elif [ "$exitc" = "124" ]; then
    log "minimax producer TIMED OUT after ${wall}s"
    PRODUCER_STATUS="${PRODUCER_STATUS}; minimax timeout"
  else
    log "minimax producer exited non-zero (exit $exitc) after ${wall}s"
    PRODUCER_STATUS="${PRODUCER_STATUS}; minimax exit $exitc"
  fi
  return 1
}

PRODUCER_HEAD=$(git -C "$BLOG_DIR" rev-parse HEAD)
case "$PRODUCER_MODE" in
  grok)
    run_grok_producer || true
    ;;
  claude)
    run_claude_producer || true
    ;;
  minimax)
    run_minimax_producer || true
    ;;
  auto|*)
    if run_claude_producer; then
      :
    elif post_exists_now; then
      log "Claude failed but a post for $YESTERDAY already exists — skipping minimax fallback"
      PRODUCER_USED="${PRODUCER_USED:-claude}"
      PRODUCER_STATUS="OK (post present after claude failure)"
    else
      log "Claude producer failed with no post on disk — attempting MiniMax fallback (Grok Build exhausted)"
      run_minimax_producer || true
    fi
    ;;
esac
if [ "$(git -C "$BLOG_DIR" rev-parse HEAD)" != "$PRODUCER_HEAD" ]; then
  log "FATAL: producer changed Git HEAD; producer/lander boundary was violated. Refusing to land or push additional state."
  exit 1
fi
rm -rf "$PRODUCER_GUARD_DIR"
PRODUCER_GUARD_DIR=""
# Backward-compatible name used in the summary email below.
CLAUDE_STATUS="${PRODUCER_STATUS} [producer=${PRODUCER_USED:-none}]"

# --- Land: deterministic verify → commit → push → publish → OR quarantine ----
# Runs unconditionally (even after a claude -p failure) — landing is also what
# cleans up / quarantines any partial state so tomorrow is unblocked.
log "Invoking blog-land.sh for $YESTERDAY..."
"$LAND_SCRIPT" "$YESTERDAY" >> "$LOG" 2>&1
LAND_RC=$?
LAND_RESULT=$(grep -oE 'LAND-RESULT: .*' "$LOG" | tail -1 | sed 's/LAND-RESULT: //')
log "blog-land.sh returned rc=$LAND_RC (${LAND_RESULT:-unknown})"

# Map land rc + claude status → overall STATUS.
case "$LAND_RC" in
  0)  STATUS="OK" ;;
  3)  STATUS="OK-WITH-WARNING (pushed, not live yet)" ;;
  10) STATUS="FAILED (QUARANTINED — preconditions failed, tree cleaned)" ;;
  11) STATUS="FAILED (land infra — orphaned local commit, manual push needed)" ;;
  12) STATUS="FAILED (land BLOCKED before commit — nothing orphaned; re-run land from a normal shell)" ;;
  20) case "$PRODUCER_STATUS" in
        OK*) STATUS="OK (no post — no activity)" ;;
        *)   STATUS="FAILED (${PRODUCER_STATUS}, no post produced)" ;;
      esac ;;
  21) STATUS="OK (already landed)" ;;
  *)  STATUS="FAILED (land rc=$LAND_RC)" ;;
esac
log "Overall STATUS: $STATUS"

# --- Methodology index rebuild (derived index.db from decisions.jsonl) --------
REBUILD="$BLOG_DIR/.claude/skills/blog-backfill/scripts/rebuild-methodology-index.sh"
if [ -x "$REBUILD" ]; then
  log "Rebuilding methodology index..."
  "$REBUILD" >> "$LOG" 2>&1 || log "WARN: methodology index rebuild failed"
fi

# --- Bounded retention + storage census (this job's own footprint only) ------
# Run logs older than BLOG_BACKFILL_LOG_KEEP_DAYS are the only thing this job
# ever deletes, and only by exact filename. Quarantine is counted, never pruned.
PRUNED=$(prune_run_logs "$LOG_DIR" "${BLOG_BACKFILL_LOG_KEEP_DAYS:-180}" "$LOG")
QUARANTINE_NOTE=""
if ! quarantine_census "$BLOG_DIR/.blog-quarantine" "${BLOG_QUARANTINE_MAX_ENTRIES:-12}" "$LOG"; then
  QUARANTINE_NOTE=" — QUARANTINE OVER LINE (${QUARANTINE_COUNT} entries)"
fi

# --- Consecutive-failure escalation ------------------------------------------
CONSEC_FAILS=$(count_consecutive_failures "$LOG_DIR" "run-*.log" "FATAL|TIMED OUT|FAILED \(" 10)
ESCALATE_PREFIX=""
if [ "$CONSEC_FAILS" -ge 3 ]; then
  log "ESCALATION: ${CONSEC_FAILS} consecutive failed runs detected — elevating alert priority"
  ESCALATE_PREFIX="🚨 ${CONSEC_FAILS}-DAY STREAK: "
fi

# Buzz sys-automation on a hard failure only (reads governed Buzz dispatch).
case "$STATUS" in
  FAILED*) cron_fail "blog-backfill-daily" "${ESCALATE_PREFIX}${YESTERDAY}: ${STATUS} (${CONSEC_FAILS}-day streak). Log: $LOG" ;;
esac

# --- Summary email -----------------------------------------------------------
TAIL=$(tail -50 "$LOG")
BODY="Daily /blog-backfill run for ${YESTERDAY}
Status: ${STATUS}
Land result: ${LAND_RESULT:-n/a} (rc=${LAND_RC})
Producer: ${CLAUDE_STATUS}
Consecutive failures (incl. this run): ${CONSEC_FAILS}
Disk: ${DISK_GUARD_FREE_MB:-?}MiB free on ${DISK_GUARD_MOUNT:-/} (floor ${DISK_MIN_MB}MiB, warn ${DISK_WARN_MB}MiB)${DISK_WARNING:+ — WARNING: under the early-warning line}
Quarantine: ${QUARANTINE_COUNT:-0} entries, ${QUARANTINE_MB:-0}MiB${QUARANTINE_NOTE}
Run-log retention: ${PRUNED:-0} log(s) older than ${BLOG_BACKFILL_LOG_KEEP_DAYS:-180}d removed
Recovery command for a missed day: ${RECOVERY_CMD}

================================================================================
Last 50 log lines (full log: ${LOG}):
================================================================================

${TAIL}
"
DISK_PREFIX=""; [ -n "$DISK_WARNING" ] && DISK_PREFIX="⚠️ DISK ${DISK_GUARD_FREE_MB}MiB: "
SUBJECT="${ESCALATE_PREFIX}${DISK_PREFIX}Daily blog-backfill: ${YESTERDAY} — ${STATUS}${QUARANTINE_NOTE}"
node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io --subject "$SUBJECT" --body "$BODY" >> "$LOG" 2>&1 \
  || log "Email send failed — see log"

# Failure alerting is handled above by cron_fail (#cron-failures) + the summary
# email; success/status is silent now (ntfy retired 2026-06-13).

# Normal notification path completed — disarm the fail-loud trap.
NOTIFIED=1
log "=== Daily blog-backfill end ==="

# Exit truthfully for the liveness trap (review finding on PR #26): a handled
# failure must still exit non-zero so the EXIT trap withholds .ok and the estate
# sweep's running-but-failing signal stays live. NOTIFIED=1 above guarantees the
# trap does NOT double-alert.
case "$STATUS" in OK*) : ;; *) exit 1 ;; esac
