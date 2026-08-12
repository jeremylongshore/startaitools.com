#!/usr/bin/env bash
# blog-recommendation-worker.sh — drain ONE auto-ok recommendation bead per run,
# implement it on a feature branch, and open a PR. Never merges. Never touches
# the deploy branch.
#
# WHY THIS EXISTS
#   The analysis layer of this pipeline works and the action layer did not exist.
#   Three times a correct report reached a human and stopped: July's calibration
#   shipped 1 of 7 recommendations, the tier-creep guard suppressed a persistent
#   breach for five weeks by design, and the fork contract lived in prose with no
#   required check. An emailed markdown report is not an action layer.
#
#   So recommendations become beads (labelled auto-ok or owner-gated) and this
#   worker drains the auto-ok half on a cadence.
#
# WHAT IT WILL AND WILL NOT DO
#   auto-ok means deterministic, testable and reversible: add a gate, delete a
#   heuristic, govern a field, build a counter. owner-gated means it changes what
#   gets published or how it reads, and this worker never touches those. The label
#   is the boundary and it is checked here, not assumed.
#
#   It opens a PR and stops. It does not merge, and that is deliberate rather than
#   timid: on 2026-08-11 four lint violations were pushed by an agent across three
#   commits, each passing the checks that were run and failing the ones that were
#   not. A gate-passing change that misses the point is exactly what review is for.
#
# SAFETY PROPERTIES
#   * Runs in a throwaway `git worktree`, never the shared tree. A concurrent
#     session can `git checkout` the primary tree out from under a job; that has
#     already cost uncommitted work once on another repo in this estate.
#   * One bead per run. A bounded blast radius beats a fast queue drain.
#   * The deterministic gate (lint-all.sh) is re-run by THIS script after the
#     agent finishes. The agent's own claim that tests pass is not evidence.
#   * On any failure the bead goes back to open with a note, so the next run
#     retries rather than the work vanishing.
#
# Usage:
#   blog-recommendation-worker.sh              # cron mode: drain one bead
#   blog-recommendation-worker.sh --dry-run    # pick + brief, change nothing
#   blog-recommendation-worker.sh --bead <id>  # target a specific bead

set -uo pipefail

BLOG_DIR=/home/jeremy/000-projects/blog/startaitools
LOG_DIR=/home/jeremy/.local/state/blog-recommendation-worker
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/worker-$(date +%Y-%m-%d).log"
EMAIL_SCRIPT=/home/jeremy/.claude/skills/email/scripts/send-email.cjs
WORKTREE_ROOT=/tmp/blog-worker-worktrees
LABEL_ALLOW="auto-ok"
LABEL_DENY="owner-gated"
AGENT_TIMEOUT="${WORKER_AGENT_TIMEOUT:-2700}"
AGENT_MODEL="${WORKER_AGENT_MODEL:-claude-sonnet-5}"

mkdir -p "$HOME/.local/state/intent-os/liveness" 2>/dev/null || true
: > "$HOME/.local/state/intent-os/liveness/blog-recommendation-worker.beat" 2>/dev/null || true

# shellcheck source=./lib-cron-common.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib-cron-common.sh"
log() { echo "[$(date -Is)] $*" | tee -a "$LOG"; }

NOTIFIED=0
BEAD=""
WORKTREE=""
# shellcheck disable=SC2317  # invoked via `trap ... EXIT` below
cleanup_and_notify() {
  local rc=$?
  liveness_markers "blog-recommendation-worker" "$rc"
  # Always remove the worktree; leaving them accumulates and they are disposable.
  if [ -n "$WORKTREE" ] && [ -d "$WORKTREE" ]; then
    git -C "$BLOG_DIR" worktree remove --force "$WORKTREE" >/dev/null 2>&1 || true
  fi
  [ "$rc" -eq 0 ] && return
  [ "$NOTIFIED" -eq 1 ] && return
  # A claimed bead must never be left in_progress by a crashed run, or the queue
  # silently stalls on a bead nobody is working.
  if [ -n "$BEAD" ]; then
    bd update "$BEAD" --status open >/dev/null 2>&1 || true
    bd export -o "$BLOG_DIR/.beads/issues.jsonl" >/dev/null 2>&1 || true
  fi
  log "ABNORMAL EXIT (rc=$rc) — releasing bead ${BEAD:-none} and alerting"
  cron_fail "blog-recommendation-worker" "rc=${rc} on bead ${BEAD:-none}. Check ${LOG}"
}
trap cleanup_and_notify EXIT

DRY_RUN=0; TARGET_BEAD=""
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;;
    --bead) TARGET_BEAD="$2"; shift ;;
    *) echo "Unknown arg: $1" >&2; exit 64 ;;
  esac
  shift
done

log "=== recommendation worker start (dry_run=$DRY_RUN) ==="
cd "$BLOG_DIR" || { log "FATAL: cd $BLOG_DIR"; exit 11; }
disk_guard "$BLOG_DIR" 2048 "$LOG" || exit 11

command -v bd >/dev/null 2>&1 || { log "FATAL: bd not on PATH"; exit 11; }
command -v gh >/dev/null 2>&1 || { log "FATAL: gh not on PATH"; exit 11; }

# --- Pick exactly one eligible bead ------------------------------------------
pick_bead() {
  if [ -n "$TARGET_BEAD" ]; then printf '%s' "$TARGET_BEAD"; return; fi
  # bd ready already excludes blocked work. Filter to the allow label, then take
  # the lowest priority number (bd priority 0 is most urgent).
  bd list --label "$LABEL_ALLOW" --status open --json 2>/dev/null \
    | jq -r 'sort_by(.priority) | .[0].id // empty' 2>/dev/null
}
BEAD=$(pick_bead)
if [ -z "$BEAD" ]; then
  log "No open ${LABEL_ALLOW} beads — nothing to do."
  # A quiet queue is a valid outcome, but silence reads as a broken cron, so the
  # positive heartbeat goes out the same way the packet sweep's does.
  if [ "$DRY_RUN" -eq 0 ]; then
    # shellcheck disable=SC2016 # backticks are markdown in the email body
    HEARTBEAT_BODY=$(printf 'The weekly recommendation worker ran clean and found no open %s beads.\n\nThis is a drained queue, NOT a failure. Owner-gated beads are deliberately skipped; run `bd list --label %s` to see what is waiting on you.\n' "$LABEL_ALLOW" "$LABEL_DENY")
    node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io \
      --subject "✓ Recommendation worker: queue empty ($(date +%Y-%m-%d))" \
      --body "$HEARTBEAT_BODY" >/dev/null 2>&1 || log "WARN: heartbeat email failed"
  fi
  NOTIFIED=1
  log "=== worker end (0 beads) ==="
  exit 0
fi

# Re-read the bead and REFUSE if it carries the deny label. The picker filters,
# but a --bead override bypasses the picker, and the label boundary is the whole
# safety model. Check it where the mistake would be made.
BEAD_JSON=$(bd show "$BEAD" --json 2>/dev/null | jq -c 'if type=="array" then .[0] else . end')
if printf '%s' "$BEAD_JSON" | jq -e --arg d "$LABEL_DENY" '.labels // [] | index($d)' >/dev/null 2>&1; then
  log "REFUSING $BEAD: carries the ${LABEL_DENY} label. This worker never implements owner-gated work."
  NOTIFIED=1
  exit 0
fi
if ! printf '%s' "$BEAD_JSON" | jq -e --arg a "$LABEL_ALLOW" '.labels // [] | index($a)' >/dev/null 2>&1; then
  log "REFUSING $BEAD: does not carry the ${LABEL_ALLOW} label."
  NOTIFIED=1
  exit 0
fi

TITLE=$(printf '%s' "$BEAD_JSON" | jq -r '.title // ""')
DESC=$(printf '%s' "$BEAD_JSON" | jq -r '.description // ""')
ACCEPT=$(printf '%s' "$BEAD_JSON" | jq -r '.acceptance_criteria // ""')
log "Selected $BEAD: $TITLE"

if [ "$DRY_RUN" -eq 1 ]; then
  log "DRY-RUN: would claim $BEAD, build a worktree, brief the agent, gate, and open a PR."
  NOTIFIED=1
  log "=== worker end (dry-run) ==="
  exit 0
fi

# --- Isolated worktree off a FRESH origin tip --------------------------------
git fetch -q origin || { log "FATAL: fetch failed"; exit 11; }
DEPLOY_BRANCH=$(default_branch_of "$BLOG_DIR"); DEPLOY_BRANCH="${DEPLOY_BRANCH:-master}"
BRANCH="auto/${BEAD}-$(date +%Y%m%d)"
mkdir -p "$WORKTREE_ROOT"
WORKTREE="$WORKTREE_ROOT/$BEAD"
git worktree remove --force "$WORKTREE" >/dev/null 2>&1 || true
git branch -D "$BRANCH" >/dev/null 2>&1 || true
if ! git worktree add -q -b "$BRANCH" "$WORKTREE" "origin/$DEPLOY_BRANCH" >>"$LOG" 2>&1; then
  log "FATAL: could not create worktree at $WORKTREE"
  exit 11
fi
log "Worktree $WORKTREE on $BRANCH (from origin/$DEPLOY_BRANCH)"

bd update "$BEAD" --status in_progress >/dev/null 2>&1 || true
bd export -o "$BLOG_DIR/.beads/issues.jsonl" >/dev/null 2>&1 || true

# --- Brief the agent ----------------------------------------------------------
PROMPT="You are implementing ONE tracked task in the startaitools blog repo. You are
working in an isolated git worktree at ${WORKTREE}, on branch ${BRANCH}. Do all work there.

TASK (bead ${BEAD}): ${TITLE}

DESCRIPTION:
${DESC}

ACCEPTANCE CRITERIA:
${ACCEPT}

HARD RULES, in order of precedence:
1. NEVER checkout, commit to, push to, or merge into '${DEPLOY_BRANCH}'. You are on a
   feature branch and it stays that way. Do not run 'git merge', 'git push origin
   ${DEPLOY_BRANCH}', or any force push.
2. Read ${WORKTREE}/CLAUDE.md before you touch anything. It is the authority on this
   repo's conventions and it overrides your instincts.
3. Implement ONLY this bead. If you find other problems, note them in your summary;
   do not fix them. Scope creep in an unattended agent is how a small PR becomes
   unreviewable.
4. Every behaviour change needs a test, and the test must have TEETH: verify it by
   deliberately breaking the thing it guards and confirming the test fails, then
   restore. A test that passes before and after your change guards nothing.
5. Run 'bash scripts/blog/lint-all.sh' until it is fully green. It runs shellcheck,
   ruff, the pipeline invariants and pytest, which is exactly what CI runs. A missing
   tool is reported as a FAILURE, not a pass; do not work around that.
6. Commit with the repo's commit standard: 'type(scope): imperative subject', then a
   body covering WHAT changed, WHY (including 'chose X over Y because Z' where a real
   alternative existed), HOW it was verified with the evidence, RISK, and UNFINISHED.
   Never use an em dash or an en dash anywhere.
7. Do NOT open the pull request. The calling script does that. Do NOT merge anything.

When you are done, print a short summary of what you changed and what you verified.
If you cannot complete the task safely, STOP, explain why, and leave the tree clean.
Do not guess at an acceptance criterion you cannot meet."

log "Invoking the agent (timeout ${AGENT_TIMEOUT}s, model ${AGENT_MODEL})..."
T0=$(date +%s)
if /usr/bin/timeout "$AGENT_TIMEOUT" claude -p "$PROMPT" --model "$AGENT_MODEL" \
     --add-dir "$WORKTREE" >>"$LOG" 2>&1; then
  log "agent exited cleanly after $(( $(date +%s) - T0 ))s"
else
  rc=$?
  log "agent exited non-zero ($rc) after $(( $(date +%s) - T0 ))s"
fi

# --- The gate. The agent's word is not evidence. ------------------------------
cd "$WORKTREE" || { log "FATAL: cd $WORKTREE"; exit 11; }
if [ -z "$(git status --porcelain)" ] && \
   [ -z "$(git log --oneline "origin/${DEPLOY_BRANCH}..HEAD" 2>/dev/null)" ]; then
  log "Agent produced NO changes. Releasing $BEAD back to open."
  bd update "$BEAD" --status open >/dev/null 2>&1 || true
  bd-sync note "$BEAD" "Worker run produced no changes; released back to open. Log: $LOG" >/dev/null 2>&1 || true
  NOTIFIED=1
  cron_fail "blog-recommendation-worker" "Bead ${BEAD} produced no changes. Check ${LOG}"
  exit 12
fi

log "Running the deterministic gate in the worktree..."
if bash scripts/blog/lint-all.sh >>"$LOG" 2>&1; then
  log "Gate PASSED"
else
  log "Gate FAILED — not opening a PR. Branch $BRANCH is left in place for inspection."
  bd update "$BEAD" --status open >/dev/null 2>&1 || true
  bd-sync note "$BEAD" "Worker implemented this but lint-all.sh failed; branch ${BRANCH} left for inspection. Log: $LOG" >/dev/null 2>&1 || true
  bd export -o "$BLOG_DIR/.beads/issues.jsonl" >/dev/null 2>&1 || true
  NOTIFIED=1
  cron_fail "blog-recommendation-worker" "Bead ${BEAD}: gate FAILED, no PR opened. Branch ${BRANCH}. Check ${LOG}"
  exit 13
fi

# Commit anything the agent left uncommitted, so the branch is self-contained.
if [ -n "$(git status --porcelain)" ]; then
  git add -A >>"$LOG" 2>&1
  git commit -q -m "chore(${BEAD}): worker-staged remainder for '${TITLE}'" >>"$LOG" 2>&1 || true
fi

git push -q -u origin "$BRANCH" >>"$LOG" 2>&1 || { log "FATAL: could not push $BRANCH"; exit 11; }
log "Pushed $BRANCH"

# shellcheck disable=SC2016 # backticks are markdown in the PR body
PR_BODY=$(printf 'Implements bead \x60%s\x60: %s\n\n## What\n\nAutomated by `scripts/blog/blog-recommendation-worker.sh`, which drains one `%s` recommendation bead per week.\n\n## Acceptance criteria (from the bead)\n\n%s\n\n## Verification\n\n`scripts/blog/lint-all.sh` passed in an isolated worktree before this PR was opened. That runs shellcheck, ruff, the pipeline invariants and pytest, which is exactly what CI runs. The worker re-runs the gate itself rather than trusting the agent to report on its own work.\n\n## Review notes\n\nThis branch was written unattended. Read it as you would any contributor PR, not as a rubber stamp. The worker deliberately does not merge: on 2026-08-11 four lint violations were pushed by an agent across three commits, each passing the checks that were run and failing the ones that were not.\n\nRefs %s\n' \
  "$BEAD" "$TITLE" "$LABEL_ALLOW" "${ACCEPT:-none recorded}" "$BEAD")

if PR_URL=$(gh pr create --repo jeremylongshore/startaitools.com \
    --base "$DEPLOY_BRANCH" --head "$BRANCH" \
    --title "${TITLE}" --body "$PR_BODY" 2>>"$LOG"); then
  log "PR opened: $PR_URL"
  bd-sync note "$BEAD" "Worker opened PR: ${PR_URL} (branch ${BRANCH}). NOT merged; awaiting review." >/dev/null 2>&1 || true
  bd export -o "$BLOG_DIR/.beads/issues.jsonl" >/dev/null 2>&1 || true
  node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io \
    --subject "🤖 Worker opened a PR: ${TITLE}" \
    --body "$(printf 'The weekly recommendation worker implemented bead %s and opened a PR.\n\n  %s\n\nIt did NOT merge. Gate (shellcheck + ruff + invariants + pytest) passed in an isolated worktree before the PR was opened, but this branch was written unattended: review it like a contributor PR.\n\nLog: %s\n' "$BEAD" "$PR_URL" "$LOG")" \
    >/dev/null 2>&1 || log "WARN: PR notification email failed"
  NOTIFIED=1
else
  log "FATAL: gh pr create failed; branch $BRANCH is pushed but has no PR"
  bd update "$BEAD" --status open >/dev/null 2>&1 || true
  exit 14
fi

log "=== worker end (1 bead, PR opened, nothing merged) ==="
exit 0
