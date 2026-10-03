#!/usr/bin/env bash
# blog-feedback-sweep.sh — weekly cron wrapper for feedback-sweep.py
#
# Runs the deterministic retrospective grader against every classifier record
# without a feedback.jsonl entry and persists the new rows to origin/master.
# Emails the digest. No LLM in the loop.
#
# Schedule: weekly, Sunday 10:00 local (cron line in $HOME crontab).
#
# Usage:
#   blog-feedback-sweep.sh                    # cron: grade, then persist
#   blog-feedback-sweep.sh --publish-pending  # recovery: push queued rows only
#
# OUTCOME CONTRACT (2026-10-03, startaitools-8oc.15)
# ---------------------------------------------------------------------------
#  Stage             Mandatory?        Failure means
#  1 grade           yes               FAILED  (exit 1)
#  2 persist-local   yes               FAILED  (exit 1)
#  3 persist-remote  deferrable, capped DEFERRED (exit 75) while deferred runs
#                                      < BLOG_FEEDBACK_MAX_DEFERRED_RUNS (3);
#                                      FAILED (exit 1) at the cap, on a record
#                                      conflict, or on a corrupt origin file
#  4 notify (email)  yes               DEGRADED (exit 2) if everything else was OK
#
#  STATUS  exit  .beat  .ok   Buzz cron_fail  email subject
#  OK      0     yes    yes   no              "— OK"
#  DEFERRED 75   yes    no    yes (high)      "— DEFERRED"
#  DEGRADED 2    yes    no    yes (high)      (email failed; Buzz carries it)
#  FAILED  1     yes    no    yes (high)      "— FAILED"
#
# The status/exit mapping is computed in exactly one place
# (blog-feedback-records.py `outcome`) and is unit-tested there.
#
# WHY IT NO LONGER COMMITS IN THE SHARED CHECKOUT
# ---------------------------------------------------------------------------
# Until 2026-10 this script committed feedback.jsonl on master in the primary
# checkout and pushed via push_with_rebase. The daily lander appends
# length_gate_downgrade rows to the same file from its isolated workspace, so a
# rebase met two end-of-file appends and conflicted. On 2026-09-27 that left the
# shared checkout mid-rebase for six days (failing both monthly jobs on 10-01)
# while this script logged a WARN, reported "OK" and wrote .ok.
#
# Now:
#   * grading runs on a `git archive` snapshot of fresh origin/master in the
#     state dir, so it sees the lander's rows and never touches the shared
#     working tree, index, HEAD or stash;
#   * new rows go to a durable pending queue OUTSIDE the repo
#     ($STATE/pending-feedback.jsonl) — that is "local persistence";
#   * the queue is published by blog-feedback-records.py: fresh origin content
#     + pending rows, merged at RECORD level (identical rows dedupe, distinct rows
#     both survive, same key with different content is a CONFLICT, never
#     silently dropped), committed with git plumbing on that exact origin tip
#     and pushed with bounded retries. No rebase, so no mid-rebase checkout.
#
# RECOVERY: a DEFERRED run keeps its rows in the queue and the next run (or
# `blog-feedback-sweep.sh --publish-pending`) retries them before grading. The
# queue and its deferred-run counter are visible at $STATE/pending-feedback.jsonl
# and $STATE/pending-meta.json. A CONFLICT needs a human: inspect the queue
# against origin, edit or remove the offending queued row, then --publish-pending.

set -uo pipefail
export PATH="${HOME}/.local/bin:${HOME}/bin:/usr/local/bin:/usr/bin:/bin:${PATH:-}"

JOB=blog-feedback-sweep
LOG_DIR="${BLOG_FEEDBACK_STATE_DIR:-$HOME/.local/state/blog-feedback-sweep}"
mkdir -p "$LOG_DIR"

# Liveness heartbeat: drop a per-run beat so the estate dead-man's-switch
# (~/bin/automation-liveness-sweep.sh) can tell this schedule still fires. The
# beat marks "the cron ran"; .ok (written by the EXIT trap iff rc==0) marks
# "and it succeeded".
mkdir -p "$HOME/.local/state/intent-os/liveness" 2>/dev/null || true
: > "$HOME/.local/state/intent-os/liveness/${JOB}.beat" 2>/dev/null || true

TS=$(date +%Y-%m-%d)
LOG="$LOG_DIR/sweep-${TS}.log"
REPO="${BLOG_FEEDBACK_REPO:-/home/jeremy/000-projects/blog/startaitools}"
EMAIL_SCRIPT="${BLOG_FEEDBACK_EMAIL_SCRIPT:-/home/jeremy/.claude/skills/email/scripts/send-email.cjs}"
EMAIL_TO="${BLOG_FEEDBACK_EMAIL_TO:-jeremy@intentsolutions.io}"
MAX_DEFERRED_RUNS="${BLOG_FEEDBACK_MAX_DEFERRED_RUNS:-3}"
PUSH_ATTEMPTS="${BLOG_FEEDBACK_PUSH_ATTEMPTS:-3}"
PENDING="$LOG_DIR/pending-feedback.jsonl"
META="$LOG_DIR/pending-meta.json"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HELPER="$HERE/blog-feedback-records.py"
FEEDBACK_REL=.claude/skills/blog-backfill/methodology/feedback.jsonl
SWEEP_REL=.claude/skills/blog-backfill/scripts/feedback-sweep.py
DECISIONS_REL=.claude/skills/blog-backfill/methodology/decisions.jsonl

# shellcheck source=./lib-cron-common.sh
source "$HERE/lib-cron-common.sh"

log() { echo "[$(date -Is)] $*" | tee -a "$LOG"; }

MODE=sweep
case "${1:-}" in
  "") ;;
  --publish-pending) MODE=publish-pending ;;
  *) echo "Unknown arg: $1" >&2; exit 64 ;;
esac
log "=== feedback-sweep start (mode=$MODE) ==="

# --- Fail-loud guard: an early exit must never be silent ----------------------
NOTIFIED=0
SNAP=""
# shellcheck disable=SC2317  # invoked via `trap ... EXIT` below
notify_unexpected_exit() {
  local rc=$?
  [ -n "$SNAP" ] && rm -rf "$SNAP"
  liveness_markers "$JOB" "$rc"   # .beat every run; .ok iff rc==0
  [ "$rc" -eq 0 ] && return
  [ "$NOTIFIED" -eq 1 ] && return
  log "ABNORMAL EXIT (rc=$rc) before normal notification — sending fail-loud alert"
  cron_fail "$JOB" "${TS}: early exit rc=${rc} — sweep did not complete. Check ${LOG}"
  node "$EMAIL_SCRIPT" --to "$EMAIL_TO" \
    --subject "🚨 blog-feedback-sweep aborted early: ${TS} (rc=${rc})" \
    --body "$(printf 'Weekly blog feedback-sweep exited abnormally (rc=%s) BEFORE its normal summary email.\n\nNo digest was sent for %s.\n\nLast 30 log lines:\n--------------------------------------------------------------------------------\n%s\n' "$rc" "$TS" "$(tail -30 "$LOG" 2>/dev/null)")" \
    >/dev/null 2>&1 || true
}
trap notify_unexpected_exit EXIT

# One sweep at a time: the pending queue has a single owner.
exec 8>"$LOG_DIR/sweep.lock" || { log "FATAL: cannot open lock"; exit 1; }
if ! flock -n 8; then
  log "LOCKED: another feedback-sweep run holds $LOG_DIR/sweep.lock — not running (no .ok)"
  NOTIFIED=1
  exit 75
fi

[ -f "$HELPER" ] || { log "FATAL: $HELPER missing"; exit 1; }
BRANCH=$(default_branch_of "$REPO"); BRANCH="${BRANCH:-master}"

ST_GRADE=skipped; ST_LOCAL=skipped; ST_REMOTE=skipped; ST_NOTIFY=ok
DIGEST="(grading not run in --publish-pending mode)"
DEFERRED_RUNS=0

# --- Stage 1+2: grade on a fresh-origin snapshot, queue new rows locally -------
if [ "$MODE" = sweep ]; then
  ST_GRADE=failed
  if ! git -C "$REPO" fetch -q origin "+refs/heads/${BRANCH}:refs/remotes/origin/${BRANCH}" >> "$LOG" 2>&1; then
    log "grade: FAILED — could not fetch origin/$BRANCH (grading stale data would mint conflicting rows)"
    DIGEST="(not graded: fetch of origin/$BRANCH failed)"
  else
    TIP=$(git -C "$REPO" rev-parse "refs/remotes/origin/${BRANCH}")
    SNAP=$(mktemp -d "$LOG_DIR/snapshot.XXXXXX")
    if git -C "$REPO" archive "$TIP" -- "$SWEEP_REL" "$DECISIONS_REL" "$FEEDBACK_REL" content/posts \
         | tar -x -C "$SNAP" 2>> "$LOG" \
       && SEED_OUT=$(python3 "$HELPER" seed --feedback "$SNAP/$FEEDBACK_REL" \
            --pending "$PENDING" --seed-copy "$SNAP/feedback.seed") ; then
      log "grade: snapshot of origin/$BRANCH @ ${TIP:0:9}; seeded pending rows: $SEED_OUT"
      if DIGEST=$(python3 "$SNAP/$SWEEP_REL" 2>&1); then
        ST_GRADE=ok
        printf '%s\n' "$DIGEST" >> "$LOG"
        ST_LOCAL=failed
        if STAGE_OUT=$(python3 "$HELPER" stage --seeded "$SNAP/feedback.seed" \
             --graded "$SNAP/$FEEDBACK_REL" --pending "$PENDING"); then
          ST_LOCAL=ok
          log "persist-local: $STAGE_OUT (queue: $PENDING)"
        else
          log "persist-local: FAILED — $STAGE_OUT"
        fi
      else
        printf '%s\n' "$DIGEST" >> "$LOG"
        log "grade: FAILED — feedback-sweep.py exited non-zero"
      fi
    else
      log "grade: FAILED — snapshot or seed failed (${SEED_OUT:-archive error}); pending queue untouched"
      DIGEST="(not graded: ${SEED_OUT:-snapshot failed})"
    fi
    rm -rf "$SNAP"; SNAP=""
  fi
fi

# --- Stage 3: publish the pending queue to origin ------------------------------
# Runs in --publish-pending mode, and in sweep mode only after grading and local
# persistence succeeded (a failed grade leaves any older queue for next run).
if [ "$MODE" = publish-pending ] || { [ "$ST_GRADE" = ok ] && [ "$ST_LOCAL" = ok ]; }; then
  PUB_OUT=$(python3 "$HELPER" publish --repo "$REPO" --branch "$BRANCH" \
    --pending "$PENDING" --meta "$META" --attempts "$PUSH_ATTEMPTS" \
    --max-deferred-runs "$MAX_DEFERRED_RUNS" \
    --message "chore(methodology): weekly feedback-sweep ${TS}")
  log "persist-remote: $PUB_OUT"
  ST_REMOTE=$(printf '%s' "$PUB_OUT" | jq -r '.status // "error"' 2>/dev/null)
  ST_REMOTE="${ST_REMOTE:-error}"
  DEFERRED_RUNS=$(printf '%s' "$PUB_OUT" | jq -r '.deferred_runs // 0' 2>/dev/null)
  [ "$MODE" = publish-pending ] && ST_LOCAL=ok
fi
PENDING_COUNT=0
[ -s "$PENDING" ] && PENDING_COUNT=$(/usr/bin/grep -c . "$PENDING" 2>/dev/null || echo 0)

outcome_of() {
  python3 "$HELPER" outcome --grade "$ST_GRADE" --local "$ST_LOCAL" --remote "$ST_REMOTE" \
    --notify "$ST_NOTIFY" --deferred-runs "${DEFERRED_RUNS:-0}" --max-deferred-runs "$MAX_DEFERRED_RUNS"
}
OUTCOME=$(outcome_of)
STATUS=$(printf '%s' "$OUTCOME" | jq -r .status)
REASONS=$(printf '%s' "$OUTCOME" | jq -r '.reasons | join("; ")')

# --- Stage 4: notify -----------------------------------------------------------
BODY="Weekly feedback sweep for ${TS}
Status: ${STATUS}${REASONS:+ — ${REASONS}}

Stages: grade=${ST_GRADE}  persist-local=${ST_LOCAL}  persist-remote=${ST_REMOTE}
Pending rows not yet on origin/${BRANCH}: ${PENDING_COUNT} (${PENDING})
Recovery: scripts/blog/blog-feedback-sweep.sh --publish-pending

================================================================================

${DIGEST}

================================================================================
Full log: ${LOG}
Source-of-truth: origin/${BRANCH}:${FEEDBACK_REL}

Mismatches above are where the structural rubric disagrees with the classifier.
Review with:  /blog-feedback <slug> --correct        (rubric was right)
              /blog-feedback <slug> --wrong N        (override rubric)
"
SUBJECT="Weekly blog feedback-sweep: ${TS} — ${STATUS}"
if ! node "$EMAIL_SCRIPT" --to "$EMAIL_TO" --subject "$SUBJECT" --body "$BODY" >> "$LOG" 2>&1; then
  ST_NOTIFY=failed
  log "notify: email send FAILED — digest preserved in log"
  OUTCOME=$(outcome_of)
  STATUS=$(printf '%s' "$OUTCOME" | jq -r .status)
  REASONS=$(printf '%s' "$OUTCOME" | jq -r '.reasons | join("; ")')
fi
RC=$(printf '%s' "$OUTCOME" | jq -r .rc 2>/dev/null)
RC="${RC:-1}"

if [ "$RC" -ne 0 ]; then
  cron_fail "$JOB" "${TS}: ${STATUS} — ${REASONS}. Pending rows: ${PENDING_COUNT}. Recovery: blog-feedback-sweep.sh --publish-pending. Log: ${LOG}"
fi

# Normal notification path completed — disarm the fail-loud trap.
NOTIFIED=1
log "STATUS: ${STATUS} (rc=${RC}) stages: grade=${ST_GRADE} local=${ST_LOCAL} remote=${ST_REMOTE} notify=${ST_NOTIFY}"
log "=== feedback-sweep end ==="
exit "$RC"
