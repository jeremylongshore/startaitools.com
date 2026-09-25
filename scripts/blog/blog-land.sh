#!/usr/bin/env bash
# blog-land.sh — the deterministic "land" step for the blog pipeline.
#
# WHY THIS EXISTS (the inversion):
# The old pipeline put the LLM (`/blog-backfill`) in the git commit/push path: it
# wrote the post AND committed AND pushed AND dual-published, all inside a
# fixed-time headless `claude -p`. A timeout mid-gates left a dirty tree and a
# half-published post; the next day's clean-tree preflight then refused to run,
# and the whole cadence silently stalled. Worse, a fact-check-failed post could
# still get committed by a rushed run.
#
# The fix: the LLM now only PRODUCES artifacts (post + decisions record + a
# readiness sentinel) and does NO git. THIS script — pure bash, no LLM — decides
# whether those artifacts are safe to publish, and only then commits/pushes/
# dual-publishes/queues. If the preconditions fail, it QUARANTINES the stranded
# files (moving them out of the tree so tomorrow is unblocked) and alerts loudly.
# "Unbrick tomorrow" is never allowed to mean "publish something broken today."
#
# It is re-entrant (safe to re-run), idempotent (a landed post is a no-op), and
# does its own urgent alerting on quarantine/orphan regardless of caller.
#
# Usage:
#   blog-land.sh [YYYY-MM-DD] [--dry-run]
#     date       target date; defaults to yesterday
#     --dry-run  run every check + log intent, but touch nothing (no git, no move)
#
# Exit codes (the daily wrapper maps these to STATUS + notifications):
#   0   OK            — landed and verified live
#   10  QUARANTINED   — a precondition failed; artifacts quarantined, tree clean
#   11  FAILED        — infra failure with a REAL stranded local commit (push
#                       rejected while ahead of origin — manual push recovers it)
#   12  BLOCKED       — commit/push was refused and NO local commit exists
#                       (nothing orphaned, nothing to push; classic cause: the
#                       producer git guard active in this environment — the
#                       2026-08-03 mislabeled "orphaned local commit" incident)
#   13  NOT-LIVE      — committed post is unavailable at its public URL
#   14  DELIVERY      — source published, but required ledger/queue work remains pending
#   20  NO-POST       — no post exists for the date; nothing to do
#   21  ALREADY-LANDED— committed post verified live (canary checks source only)

set -uo pipefail

# ---- Configuration ----------------------------------------------------------
BLOG_DIR=${BLOG_REPO_DIR:-/home/jeremy/000-projects/blog/startaitools}
POSTS_DIR="$BLOG_DIR/content/posts"
DECISIONS="$BLOG_DIR/.claude/skills/blog-backfill/methodology/decisions.jsonl"
STAGING_DIR="$BLOG_DIR/.blog-staging"
QUARANTINE_DIR="$BLOG_DIR/.blog-quarantine"
CCP_REPO=/home/jeremy/000-projects/claude-code-plugins
CCP_BLOG_DIR="$CCP_REPO/marketplace/src/content/blog-posts"
ISL_REPO=/home/jeremy/000-projects/intent-solutions-landing/astro-site
SKILL_SCRIPTS="$BLOG_DIR/.claude/skills/blog-backfill/scripts"
EMAIL_SCRIPT=/home/jeremy/.claude/skills/email/scripts/send-email.cjs
CANONICAL_BASE="https://startaitools.com/posts"
# Deploy patience (startaitools-bhn.7): a post that is committed and pushed is published;
# the page going live is the release+deploy pipeline's job and normally takes ~3-4 minutes
# for a content-only push. 360s turned every slow deploy into a FAILED night. 25 minutes
# covers a slow runner; past that the wrapper records the date as PENDING, not FAILED.
LIVENESS_MAX_SECS="${BLOG_LAND_LIVENESS_SECS:-1500}"
PUBLICATION_HELPER="$(dirname "${BASH_SOURCE[0]}")/blog_publication_state.py"
DISK_MIN_MB="${BLOG_LAND_DISK_MIN_MB:-500}"

# Tags that also syndicate to intentsolutions.io/field-notes.
FIELD_NOTE_TAGS="architecture ai-agents technical-leadership vertex-ai portfolio multi-agent-systems cost-optimization google-cloud infrastructure-as-code cloud-architecture ai-systems infrastructure-automation systems-architecture ai-engineering data-architecture enterprise-automation case-study agent-orchestration"

# ---- Args -------------------------------------------------------------------
DRY_RUN=0
TARGET_DATE=""
for a in "$@"; do
  case "$a" in
    --dry-run) DRY_RUN=1 ;;
    [0-9]*-[0-9]*-[0-9]*) TARGET_DATE="$a" ;;
    *) echo "Unknown arg: $a" >&2; exit 64 ;;
  esac
done
[ -z "$TARGET_DATE" ] && TARGET_DATE=$(date -d "yesterday" +%Y-%m-%d)

LOG_DIR="${BLOG_LAND_LOG_DIR:-$HOME/.local/state/blog-land}"
mkdir -p "$LOG_DIR" "$STAGING_DIR" "$QUARANTINE_DIR"
LOG="$LOG_DIR/land-${TARGET_DATE}.log"

# shellcheck source=./lib-cron-common.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib-cron-common.sh"
log() { echo "[$(date -Is)] $*" | tee -a "$LOG"; }

log "=== blog-land start (date=$TARGET_DATE dry_run=$DRY_RUN) ==="

# ---- Concurrency lock (skip if the parent wrapper already holds it) ---------
if [ "${BLOG_PIPELINE_LOCK_HELD:-0}" != "1" ]; then
  acquire_pipeline_lock "/tmp/blog-pipeline.lock" "$LOG"; rc=$?
  [ "$rc" -eq 2 ] && exit 0     # another run holds it — benign
  [ "$rc" -eq 1 ] && exit 11
fi

# ---- Disk guard -------------------------------------------------------------
if ! disk_guard "$BLOG_DIR" "$DISK_MIN_MB" "$LOG"; then exit 11; fi

# ---- Helpers ----------------------------------------------------------------
# Urgent alert (Buzz sys-automation + email). Used for quarantine + orphan —
# always loud, regardless of whether a wrapper will also summarize.
urgent_alert() {
  local title="[blog-daily-${TARGET_DATE}] $1" body="$2; incident=blog-daily-${TARGET_DATE} run=${BLOG_RUN_ID:-unbound}"
  cron_fail "blog-land" "${title}: ${body}"
  node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io --subject "$title" \
    --body "$(printf '%s\n\nDate: %s\nLog: %s\n\nLast 40 log lines:\n%s\n' "$body" "$TARGET_DATE" "$LOG" "$(tail -40 "$LOG" 2>/dev/null)")" \
    >/dev/null 2>&1 || true
}

# Extract a front-matter scalar (title) from a TOML or YAML post.
fm_title() {
  local f="$1" t
  t=$(sed -n "s/^title = ['\"]\(.*\)['\"] *$/\1/p" "$f" | head -1)
  [ -z "$t" ] && t=$(sed -n 's/^title: *["'\'']\{0,1\}\(.*\)/\1/p' "$f" | head -1 | sed 's/["'\'']*$//')
  echo "${t:-$2}"
}

# Extract tags (space-separated) from TOML `tags = [...]` or YAML list-ish.
fm_tags() {
  local f="$1"
  sed -n 's/^tags = \[\(.*\)\].*/\1/p' "$f" | head -1 | tr -d '"'\''' | tr ',' ' '
}

# ---- Locate the post --------------------------------------------------------
cd "$BLOG_DIR" || { log "FATAL: cd $BLOG_DIR"; exit 11; }
# Best-effort: be on the deploy branch and up to date. We do NOT require a clean
# tree — the staged post is an expected uncommitted change.
DEPLOY_BRANCH=$(default_branch_of "$BLOG_DIR"); DEPLOY_BRANCH="${DEPLOY_BRANCH:-master}"
CUR_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
WORKSPACE_HELPER="$(dirname "${BASH_SOURCE[0]}")/blog-run-workspace.py"
if [ -z "${BLOG_RUN_MANIFEST:-}" ]; then
  log "LAND-RESULT: BLOCKED (bound isolated run manifest required; owner checkout preserved)"
  exit 12
fi
RUN_BRANCH=$(jq -r '.branch' "$BLOG_RUN_MANIFEST")
RUN_WORKSPACE=$(jq -r '.workspace' "$BLOG_RUN_MANIFEST")
CLASSIFIER_RUN_ID=$(jq -r '.run_id // empty' "$BLOG_RUN_MANIFEST")
if [ "$RUN_WORKSPACE" != "$BLOG_DIR" ] || [ "$RUN_BRANCH" != "$CUR_BRANCH" ]; then
  log "LAND-RESULT: BLOCKED (workspace identity mismatch; no mutation)"
  exit 12
fi
if [ "$CUR_BRANCH" != "$RUN_BRANCH" ]; then
  log "NOTE: on '$CUR_BRANCH', deploy branch is '$DEPLOY_BRANCH' — not force-switching (staged changes present). Landing on current branch would not deploy; refusing."
  # A dry-run must never page: this path fired a real urgent alert when a
  # --dry-run was exercised from a feature branch on 2026-08-04 (AAR intent-os
  # 000-docs/145). The refusal itself still logs and exits nonzero.
  if [ "$DRY_RUN" -eq 1 ]; then
    log "DRY-RUN: would urgent-alert wrong-branch and exit 11."
    log "LAND-RESULT: FAILED (wrong branch, dry-run)"
    exit 11
  fi
  # If we're not on the deploy branch we cannot safely commit the post to it
  # without risking the staged file. Treat as infra failure so a human looks.
  urgent_alert "🚨 blog-land: wrong branch for ${TARGET_DATE}" "Working tree is on '$CUR_BRANCH' but the deploy branch is '$DEPLOY_BRANCH'. Not landing."
  exit 11
fi

POST=$(post_exists_for_date "$POSTS_DIR" "$TARGET_DATE" || true)
if [ -z "$POST" ]; then
  log "No post found for $TARGET_DATE — nothing to land (no-op)."
  log "LAND-RESULT: NO-POST"
  exit 20
fi
SLUG=$(basename "$POST" .md)
CANONICAL="$CANONICAL_BASE/$SLUG/"
log "Post: $POST (slug=$SLUG)"

# ---- Idempotency: already committed? ---------------------------------------
POST_REL="${POST#"$BLOG_DIR"/}"
if git ls-files --error-unmatch "$POST_REL" >/dev/null 2>&1 && git diff --quiet HEAD -- "$POST_REL" 2>/dev/null; then
  log "Post already committed (tracked, no diff) — this is a re-entrant no-op for the commit."
  if [ "${BLOG_CANARY:-0}" = "1" ]; then
    log "LAND-RESULT: ALREADY-LANDED (canary source only; public/cross-post checks omitted)"
    exit 21
  fi
  if ! remote_live_check "$CANONICAL" 60 "$LOG"; then
    log "LAND-RESULT: FAILED (existing committed post not live)"
    if [ "$DRY_RUN" -eq 0 ]; then
      urgent_alert "🚨 blog-land: public post unavailable ${TARGET_DATE}" "Existing committed post '$SLUG' is unavailable at $CANONICAL. Source presence does not prove publication; inspect the deployment."
    fi
    exit 13
  fi
  if [ "$DRY_RUN" -eq 0 ]; then
    python3 "$PUBLICATION_HELPER" recover --manifest "$BLOG_RUN_MANIFEST" >> "$LOG" 2>&1 || {
      log "LAND-RESULT: FAILED (published run delivery recovery remains pending)"; exit 14;
    }
  fi
  python3 "$PUBLICATION_HELPER" check-existing --manifest "$BLOG_RUN_MANIFEST" \
    --slug "$SLUG" >> "$LOG" 2>&1 || {
    log "LAND-RESULT: FAILED (existing public post has incomplete delivery state)"; exit 14;
  }
  if [ "$DRY_RUN" -eq 0 ]; then
    "$SKILL_SCRIPTS/check-crosspost-queue.sh" >> "$LOG" 2>&1 || true
    rm -f "$STAGING_DIR/${TARGET_DATE}.intent.json" 2>/dev/null || true
  fi
  log "LAND-RESULT: ALREADY-LANDED (live)"
  exit 21
fi

# ---- Precondition gate ------------------------------------------------------
SENTINEL="$STAGING_DIR/${TARGET_DATE}.intent.json"
declare -a REASONS=()
if ! python3 "$WORKSPACE_HELPER" validate --manifest "$BLOG_RUN_MANIFEST" >> "$LOG" 2>&1; then
  REASONS+=("isolated run write-set integrity failed")
fi
# Shared semantic contract is authoritative; the fallback below cannot erase
# failed production or invent readiness/agent receipts.
if ! python3 "$BLOG_DIR/scripts/blog/blog-producer-contract.py" verify \
    --repo "$BLOG_DIR" --date "$TARGET_DATE" --run-id "${BLOG_RUN_ID:-missing}" \
    --transcript "${BLOG_PRODUCER_TRANSCRIPT:-}" >> "$LOG" 2>&1; then
  REASONS+=("producer artifact contract incomplete/invalid; see precise contract error above")
fi

# (1) Readiness sentinel: the skill's explicit "all gates passed, safe to ship".
#     Its absence / ready!=true is the primary catch for a timed-out or
#     fact-check-blocked run.
if validate_json "$SENTINEL"; then
  READY=$(jq -r '.ready // false' "$SENTINEL" 2>/dev/null)
  [ "$READY" = "true" ] || REASONS+=("readiness sentinel present but ready!=true (skill did not attest all gates passed)")
else
  REASONS+=("readiness sentinel missing or invalid at $SENTINEL (skill did not finish — timeout or blocked gate)")
fi

# (2) Classifier record for this exact date and slug (methodology step 3).
jq -e --arg d "$TARGET_DATE" --arg s "$SLUG" --arg run "$CLASSIFIER_RUN_ID" \
  'select(.date == $d and .slug == $s and .tier != null and (.audit_addendum == null or .audit_addendum == false) and ($run == "" or .run_id == $run))' "$DECISIONS" >/dev/null 2>&1 \
  || REASONS+=("no classifier record for $TARGET_DATE/$SLUG in decisions.jsonl (step 3 skipped or wrong target)")

# (3) Step-8 agent_audit addendum for the slug.
jq -e --arg d "$TARGET_DATE" --arg s "$SLUG" --arg run "$CLASSIFIER_RUN_ID" \
  'select(.date == $d and .slug == $s and .audit_addendum == true and ($run == "" or .run_id == $run))' "$DECISIONS" >/dev/null 2>&1 \
  || REASONS+=("no agent_audit addendum for $SLUG (step 8 skipped)")

# (3b) The learned-pattern engine must have actually RUN for this slug.
#
# Three months of records carried an `applied_patterns` key while v_pattern_usage
# stayed empty across the entire corpus, because an empty list is what the engine
# emits when nothing matched AND what a writing agent that skipped step 2b emits
# when it fills the field in by hand. Those two were byte-identical, so the field
# proved nothing. SKILL.md INSTRUCTED the agent to run the engine and nothing
# verified it, which is the same shape as the fork contract that lived in prose
# with no required check behind it.
#
# The check is the ruleset digest, not the key: apply-patterns.py stamps a digest
# over the applicable ruleset, and we recompute it here and compare. An agent
# cannot produce that value without running the engine against the current
# patterns.jsonl. It also catches a second failure the old field could not, a
# record classified against a since-changed ruleset.
#
# WARN-ONLY until PATTERN_GATE_ENFORCE_FROM, then blocking. The flip is a DATE,
# not a human's memory, because "remember to turn this on later" is the exact
# failure mode this gate exists to close.
PATTERN_GATE_ENFORCE_FROM="2026-08-18"
PATTERN_ENGINE="$SKILL_SCRIPTS/apply-patterns.py"

# SELF-HEAL (2026-09-03, the root fix for the receipt bug). The producer is an
# LLM following a checklist, and twice in three weeks (2026-08-19, 2026-09-02)
# it skipped step 2b — the classifier record landed without a pattern_engine
# receipt and the gate below quarantined a perfectly good post, costing a
# manual recovery each time. The engine is DETERMINISTIC: running it here over
# the record produces byte-identical results to the producer running it, so
# there is nothing to trust the LLM about. Heal, log loudly, then let the gate
# verify the healed record like any other.
#
# Bound runs already validated this immutable authority against staged/native
# evidence. Never rewrite it here, even while uncommitted. Missing/stale receipt
# must fail the gate. Retain the legacy unbound heal only for explicit standalone
# use of this block; the normal lander requires an isolated manifest above.
# A committed legacy record is never rewritten (append-only would see deletion).
if [ -f "$PATTERN_ENGINE" ]; then
  if ! python3 - "$DECISIONS" "$TARGET_DATE" "$SLUG" "$PATTERN_ENGINE" "${BLOG_RUN_MANIFEST:-}" "$CLASSIFIER_RUN_ID" <<'HEAL' >> "$LOG" 2>&1; then
import json, subprocess, sys, tempfile, os
dec, date, slug, engine = sys.argv[1:5]
manifest = sys.argv[5] if len(sys.argv) > 5 else ""
run_id = sys.argv[6] if len(sys.argv) > 6 else ""
lines = open(dec, encoding="utf-8").readlines()
idx = None
for i, l in enumerate(lines):
    try:
        d = json.loads(l)
    except ValueError:
        continue
    if (d.get("date") == date and d.get("slug") == slug and d.get("tier") is not None
            and not d.get("audit_addendum") and (not run_id or d.get("run_id") == run_id)):
        idx = i; rec = d
if idx is None:
    sys.exit(0)  # no record; the no-classifier gate handles it
probe = subprocess.run(["python3", engine, "digest"], capture_output=True, text=True)
if probe.returncode != 0 or not probe.stdout.strip():
    sys.stderr.write(probe.stderr)
    raise RuntimeError(f"pattern engine digest failed or empty (exit {probe.returncode})")
want = probe.stdout.strip()
got = (rec.get("pattern_engine") or {}).get("ruleset_digest", "")
if got == want and got:
    sys.exit(0)  # receipt present and fresh
if manifest:
    print(f"PATTERN-GATE: bound classifier for {slug} has missing/stale receipt; authority unchanged")
    sys.exit(0)  # the gate below refuses it; never fabricate bound authority
# committed already? healing would create a git deletion; decline.
diff = subprocess.run(["git", "diff", "HEAD", "--", dec], capture_output=True, text=True).stdout
if ("+" + lines[idx].rstrip("\n")) not in diff:
    print(f"PATTERN-HEAL: record for {slug} lacks a receipt but is already committed; leaving it for the gate")
    sys.exit(0)
out = subprocess.run(["python3", engine, "apply"], input=json.dumps(rec), capture_output=True, text=True)
if out.returncode != 0 or not out.stdout.strip():
    print(f"PATTERN-HEAL: engine failed ({out.stderr.strip()[:120]}); leaving the record for the gate")
    sys.exit(0)
healed = json.loads(out.stdout)
old_tier, new_tier = rec.get("tier"), healed.get("tier")
lines[idx] = json.dumps(healed, ensure_ascii=False, separators=(", ", ": ")) + "\n"
fd, tmp = tempfile.mkstemp(dir=os.path.dirname(dec))
with os.fdopen(fd, "w", encoding="utf-8") as f:
    f.writelines(lines)
os.replace(tmp, dec)
note = f" (tier {old_tier} -> {new_tier})" if old_tier != new_tier else ""
print(f"PATTERN-HEAL: producer skipped step 2b for {slug}; ran the engine here and stamped the receipt{note}. The producer bug still exists; this stops it costing a publish day.")
HEAL
    REASONS+=("pattern preparation/validation failed; see logged engine error")
  fi
  # The current invocation already wrote its own result above. Never replay a
  # prior run's PATTERN-HEAL warning from this append-only target-date log.
fi

if [ -f "$PATTERN_ENGINE" ]; then
  if ! _want_digest=$(python3 "$PATTERN_ENGINE" digest 2>> "$LOG"); then
    REASONS+=("pattern engine digest failed; see logged engine error")
  elif [ -z "$_want_digest" ]; then
    REASONS+=("pattern engine digest returned empty output")
  fi
  _got_digest=$(jq -r --arg d "$TARGET_DATE" --arg s "$SLUG" --arg run "$CLASSIFIER_RUN_ID" \
    'select(.date==$d and .slug==$s and .tier!=null and (.audit_addendum == null or .audit_addendum == false) and ($run == "" or .run_id == $run)) | .pattern_engine.ruleset_digest // ""' \
    "$DECISIONS" 2>/dev/null | head -1)
  _gate_msg=""
  if [ -z "$_got_digest" ]; then
    _gate_msg="classifier record for $SLUG carries no pattern_engine receipt (step 2b was skipped; the tier was never checked against the learned patterns)"
  elif [ -n "$_want_digest" ] && [ "$_got_digest" != "$_want_digest" ]; then
    _gate_msg="pattern_engine receipt for $SLUG was stamped against ruleset $_got_digest but the live ruleset is $_want_digest (record classified against a stale pattern set)"
  fi
  if [ -n "$_gate_msg" ]; then
    if [[ "$(date +%F)" < "$PATTERN_GATE_ENFORCE_FROM" ]]; then
      log "WARN (pattern gate, not blocking until $PATTERN_GATE_ENFORCE_FROM): $_gate_msg"
    else
      REASONS+=("$_gate_msg")
    fi
  else
    log "Pattern engine receipt OK (ruleset $_got_digest)"
  fi
fi

# (4) decisions.jsonl is append-only, and every newly appended line must belong
# to the target post. This prevents a two-day producer run from landing another
# date's classifier/audit records with the requested post.
if git diff --no-color -- "$DECISIONS" | grep -qE '^-[^-]'; then
  REASONS+=("decisions.jsonl contains deletions; the audit log is append-only")
fi
while IFS= read -r decision_line; do
  [ -n "$decision_line" ] || continue
  if ! printf '%s\n' "$decision_line" | jq -e --arg d "$TARGET_DATE" --arg s "$SLUG" --arg run "$CLASSIFIER_RUN_ID" \
      'select(.date == $d and .slug == $s and ($run == "" or .run_id == $run))' >/dev/null 2>&1; then
    REASONS+=("decisions.jsonl contains an appended record outside target $TARGET_DATE/$SLUG")
    break
  fi
done < <(git diff --no-color -- "$DECISIONS" | sed -n '/^+++ /d; s/^+//p')

# (5) Voice lint: hard no em/en dash + banned AI-slop phrases (new posts only).
# Historical posts are not bulk-rewritten; this gates the post being landed.
VOICE_LINT="$BLOG_DIR/.claude/skills/blog-backfill/scripts/lint-post-voice.py"
if [ -f "$VOICE_LINT" ] && [ -f "$POST" ]; then
  if python3 "$VOICE_LINT" "$POST" >> "$LOG" 2>&1; then
    log "Voice lint OK"
  else
    REASONS+=("voice lint failed (em/en dash or AI-slop phrase in $POST_REL; see log)")
  fi
else
  log "WARN: voice lint script or post missing; skipping voice gate"
fi

# (6) Hugo build must pass (catches broken front matter / bad shortcodes).
if hugo --buildFuture --gc --minify --cleanDestinationDir --quiet >> "$LOG" 2>&1; then
  log "Hugo build OK"
else
  REASONS+=("hugo build failed")
fi

if [ "${#REASONS[@]}" -gt 0 ]; then
  log "PRECONDITIONS FAILED for $SLUG:"
  for r in "${REASONS[@]}"; do log "  - $r"; done
  if [ "$DRY_RUN" -eq 1 ]; then
    log "DRY-RUN: would quarantine now."
    log "LAND-RESULT: QUARANTINED (dry-run)"
    exit 10
  fi
  # Snapshot only this isolated run; owner checkout and all original evidence stay intact.
  if ! QUARANTINE_RESULT=$(python3 "$WORKSPACE_HELPER" quarantine \
      --manifest "$BLOG_RUN_MANIFEST" --reason "${REASONS[*]}"); then
    log "LAND-RESULT: FAILED (quarantine could not preserve run evidence)"
    exit 11
  fi
  QDIR=$(printf '%s' "$QUARANTINE_RESULT" | jq -r '.quarantine')
  log "Run quarantined at $QDIR; workspace retained; owner work preserved."
  urgent_alert "🚨 blog post QUARANTINED: ${TARGET_DATE}" "Post '${SLUG}' failed preconditions and was quarantined (NOT published). Reasons: ${REASONS[*]}. Files: ${QDIR}"
  log "LAND-RESULT: QUARANTINED"
  exit 10
fi

log "All preconditions passed."
TITLE=$(fm_title "$POST" "$SLUG")
# Audit addenda can also carry a tier. Select only the real classifier for this
# exact run, consistently with the pattern and classifier-presence gates.
CLASSIFIER_TIER=$(jq -r --arg d "$TARGET_DATE" --arg s "$SLUG" --arg run "$CLASSIFIER_RUN_ID" \
  'select(.date == $d and .slug == $s and .tier != null and (.audit_addendum == null or .audit_addendum == false) and ($run == "" or .run_id == $run)) | .tier' "$DECISIONS" 2>/dev/null | tail -1)
CLASSIFIER_TIER="${CLASSIFIER_TIER:-1}"

# --- Deterministic tier-and-length gate (2026-09-01) -------------------------
#
# WHY. For four months the classifier has inflated: TCH/SCP floored at 3, then
# NAR/TCH drifted to award a "4" to over half the corpus, so ~65% of posts were
# labelled Tier 2 against a 25-35% band. Three score-keyed "cap rule" patches
# were each defeated within a month because the drift is in the anchors the rule
# reads (August retro: catch rate 31%->4%->0% while flags fired on 100% of posts).
#
# A post's LENGTH is not a soft score and cannot drift. A Deep-Dive that is 105
# lines long is not a Deep-Dive whatever the LLM scored it. This gate caps the
# EFFECTIVE tier at what the length supports. It only ever DOWNGRADES (never
# invents an escalation), so a genuinely short Field Note is untouched, and it is
# immune to the anchor drift that killed every previous patch.
#
# Thresholds are the SAME ones the grader uses (feedback-sweep.py
# TIER1_MAX_LINES=145, TIER2_MAX_LINES=260). A CI test asserts they stay equal,
# so the gate and the grader can never disagree by construction.
LAND_TIER1_MAX_LINES=145
LAND_TIER2_MAX_LINES=260

# Body line count: strip the first frontmatter block (+++ or ---), count the
# rest, matching how the grader counts (newlines in the body).
BODY_LINES=$(awk '
  NR==1 && ($0=="+++"||$0=="---") { fence=$0; infm=1; next }
  infm && $0==fence { infm=0; next }
  !infm { n++ }
  END { print n+0 }
' "$POST" 2>/dev/null); BODY_LINES="${BODY_LINES:-0}"

if [ "$BODY_LINES" -le "$LAND_TIER1_MAX_LINES" ]; then
  STRUCTURAL_TIER=1
elif [ "$BODY_LINES" -le "$LAND_TIER2_MAX_LINES" ]; then
  STRUCTURAL_TIER=2
else
  STRUCTURAL_TIER=3
fi

TIER="$CLASSIFIER_TIER"
if [ "$CLASSIFIER_TIER" -gt "$STRUCTURAL_TIER" ]; then
  TIER="$STRUCTURAL_TIER"
  log "TIER-LENGTH GATE: classifier said Tier $CLASSIFIER_TIER but the post is $BODY_LINES lines (structural Tier $STRUCTURAL_TIER). Capping to Tier $TIER — a shorter post cannot be a higher tier, regardless of the score."
  # Record the correction as a deterministic feedback record. This is the honest
  # adjudication the loop has never had (zero human verdicts in four months): the
  # calibration report reads feedback.jsonl and now sees where length overruled
  # the classifier, which is the exact inflation signal the score-keyed rules
  # could not surface. Append-only, tracked, one line; never blocks the publish.
  _fb="$BLOG_DIR/.claude/skills/blog-backfill/methodology/feedback.jsonl"
  if [ -f "$_fb" ]; then
    if jq -cn --arg s "$SLUG" --arg d "$(date +%Y-%m-%d)" \
      --arg run "${BLOG_RUN_ID:-missing}" --argjson orig "$CLASSIFIER_TIER" --argjson corr "$STRUCTURAL_TIER" --argjson ln "$BODY_LINES" \
      '{slug:$s, run_id:$run, date_assessed:$d, original_tier:$orig, correct_tier:$corr, was_correct:0,
        reasoning:("Tier-length gate: classifier said tier \($orig) but the post is \($ln) lines (structural tier \($corr), thresholds 145/260). Length overrules an inflated score; shipped as tier \($corr)."),
        year_from_now_useful:null, engagement_data:null, source:"length_gate_downgrade",
        metadata:{lines:$ln, structural_tier:$corr, classifier_tier:$orig}}' >> "$_fb" 2>/dev/null; then
      log "  recorded length-gate downgrade to feedback.jsonl"
    fi
  fi
fi
log "Title: $TITLE | Tier: $TIER (classifier $CLASSIFIER_TIER, $BODY_LINES lines)"

# tldr is the LLM-citation surface (ChatGPT/Perplexity/Kagi cite pages that state
# their answer near the top). Mandatory in the writer brief since 2026-09-01;
# WARN here rather than quarantine so a missed tldr is visible without costing a
# publish day. The weekly feedback sweep can trend this line.
if ! /usr/bin/grep -qE '^tldr\s*=' "$POST" 2>/dev/null; then
  log "WARN: post has no tldr front-matter param (the LLM-citation surface) — brief requires one since 2026-09-01"
fi

if [ "$DRY_RUN" -eq 1 ]; then
  log "DRY-RUN: would commit '$POST_REL' + decisions, push origin/$DEPLOY_BRANCH, dual-publish, queue (tier=$TIER), verify $CANONICAL."
  log "LAND-RESULT: OK (dry-run)"
  exit 0
fi

# ---- Land: commit + push (canonical) ---------------------------------------
python3 "$PUBLICATION_HELPER" seal --manifest "$BLOG_RUN_MANIFEST" \
  --transcript "${BLOG_PRODUCER_TRANSCRIPT:-}" >> "$LOG" 2>&1 || {
  log "LAND-RESULT: BLOCKED (independent precommit quality seal failed)"; exit 12;
}
# feedback.jsonl is staged too: the tier-length gate may have appended a
# downgrade record above, and committing it with the post keeps the tree clean.
# When the gate did not fire it is unchanged and `git add` is a no-op.
PUBLISH_RESULT=$(python3 "$WORKSPACE_HELPER" validate --manifest "$BLOG_RUN_MANIFEST") || {
  log "LAND-RESULT: BLOCKED (write-set changed before commit)"; exit 12;
}
mapfile -t PUBLISH_PATHS < <(printf '%s' "$PUBLISH_RESULT" | jq -r '.publish_paths[]')
git add -- "${PUBLISH_PATHS[@]}" >> "$LOG" 2>&1 || {
  log "LAND-RESULT: BLOCKED (staging failed; no commit)"; exit 12;
}
if git commit -m "post(${TARGET_DATE}): ${TITLE} (Tier ${TIER})" >> "$LOG" 2>&1; then
  log "Committed $SLUG on $DEPLOY_BRANCH ($(git rev-parse --short HEAD))"
elif [ -z "$(git status --porcelain -- "$POST_REL" 2>/dev/null)" ]; then
  log "commit produced nothing (post already committed) — continuing"
else
  # Commit refused AND the post is still uncommitted: nothing exists to push, so
  # this is NOT an orphaned commit. The classic cause is the producer git guard
  # leaking into this environment (2026-08-03: guard rejected commit/push/pull
  # and the run mislabeled itself "orphaned local commit").
  log "FATAL: commit refused and '$POST_REL' remains uncommitted — nothing to push (is the producer git guard active in this environment?)"
  urgent_alert "🚨 blog-land: commit BLOCKED ${TARGET_DATE}" "git commit for '${SLUG}' was refused and the post remains uncommitted. No push was attempted; nothing is orphaned. Likely cause: blog-land invoked inside the producer-guarded environment. Re-run blog-land.sh ${TARGET_DATE} from a normal shell."
  log "LAND-RESULT: BLOCKED (commit refused — nothing committed, nothing to push)"
  exit 12
fi
if python3 "$WORKSPACE_HELPER" publication-check --manifest "$BLOG_RUN_MANIFEST" >> "$LOG" 2>&1 \
    && git push origin "HEAD:refs/heads/$DEPLOY_BRANCH" >> "$LOG" 2>&1; then
  log "Pushed to origin/$DEPLOY_BRANCH"
else
  {
    # Distinguish a real stranded commit from a push refused with nothing to
    # push: only the former is an "orphaned local commit" needing manual push.
    AHEAD=$(git rev-list --count "origin/${DEPLOY_BRANCH}..HEAD" 2>/dev/null || echo "unknown")
    if [ "$AHEAD" = "0" ]; then
      log "FATAL: push refused but HEAD is not ahead of origin/${DEPLOY_BRANCH} — no local commit is stranded (is the producer git guard active in this environment?)"
      urgent_alert "🚨 blog-land: push BLOCKED ${TARGET_DATE}" "Push for '${SLUG}' was refused but no local commit exists ahead of origin/${DEPLOY_BRANCH} — nothing is orphaned. Likely cause: blog-land invoked inside the producer-guarded environment. Re-run blog-land.sh ${TARGET_DATE} from a normal shell."
      log "LAND-RESULT: BLOCKED (push refused — nothing committed, nothing to push)"
      exit 12
    fi
    log "FATAL: could not push $SLUG to origin/$DEPLOY_BRANCH (${AHEAD} local commit(s) stranded)"
    urgent_alert "🚨 blog-land: push FAILED ${TARGET_DATE}" "Committed '${SLUG}' locally but could NOT push to origin/${DEPLOY_BRANCH} (${AHEAD} commit(s) ahead). Post is committed but NOT live. Manual push needed."
    log "LAND-RESULT: FAILED (orphaned local commit)"
    exit 11
  }
fi

python3 "$WORKSPACE_HELPER" complete --manifest "$BLOG_RUN_MANIFEST" >> "$LOG" 2>&1 || {
  log "LAND-RESULT: FAILED (remote publication receipt could not be verified)"; exit 11;
}

# Source publication and delivery completion are separate durable facts. Wait
# for the public route before creating packet/API work; a restart retries the
# retained quality-sealed handoff without generating another post.
if ! remote_live_check "$CANONICAL" "$LIVENESS_MAX_SECS" "$LOG"; then
  log "LAND-RESULT: FAILED (source published; public article unavailable; delivery pending)"
  exit 13
fi
python3 "$PUBLICATION_HELPER" reconcile --manifest "$BLOG_RUN_MANIFEST" >> "$LOG" 2>&1 || {
  log "LAND-RESULT: FAILED (source published; required delivery state remains pending)"; exit 14;
}

# ---- Dual-publish to tonsofskills + field-notes (working-tree-free) ----------
# Both use publish_file_to_repo (git plumbing): commit is built on the FRESH
# origin tip and pushed WITHOUT checking anything out — so a shared repo that's
# dirty or behind can't cause the non-fast-forward mirror-404 that bit us
# 2026-07-06. The post is transformed once to a tmp file named <slug>.md (the
# field-notes sync derives its slug from the basename).
ASTRO=""; ASTRO_TMPD=""
if git -C "$CCP_REPO" rev-parse --git-dir >/dev/null 2>&1 && [ -x "$SKILL_SCRIPTS/transform-hugo-to-astro.sh" ]; then
  ASTRO_TMPD=$(mktemp -d); ASTRO="$ASTRO_TMPD/$SLUG.md"
  if "$SKILL_SCRIPTS/transform-hugo-to-astro.sh" "$POST" "$ASTRO" >> "$LOG" 2>&1; then
    ccp_branch=$(default_branch_of "$CCP_REPO"); ccp_branch="${ccp_branch:-main}"
    if publish_file_to_repo "$CCP_REPO" "$ccp_branch" "$ASTRO" "$CCP_BLOG_DIR/$SLUG.md" \
        "content(blog): dual-publish ${SLUG} to tonsofskills.com/blog" "$LOG"; then
      log "Dual-published to tonsofskills (origin/$ccp_branch)"
    else
      log "WARN: dual-publish to tonsofskills failed after retries (canonical already live) — see log"
    fi
  else
    log "WARN: transform-hugo-to-astro failed — skipping dual-publish"; ASTRO=""
  fi
else
  log "NOTE: tonsofskills repo/script unavailable — skipping dual-publish"
fi

# ---- Conditional syndicate to intentsolutions.io/field-notes ----------------
POST_TAGS=$(fm_tags "$POST")
SYND_FN=0
for t in $POST_TAGS; do
  case " $FIELD_NOTE_TAGS " in *" $t "*) SYND_FN=1; break;; esac
done
if [ "$SYND_FN" -eq 1 ] && [ -n "$ASTRO" ] && [ -f "$ASTRO" ] \
   && git -C "$ISL_REPO" rev-parse --git-dir >/dev/null 2>&1 \
   && [ -x "$SKILL_SCRIPTS/sync-to-intentsolutions.sh" ]; then
  FN_FILE="$ISL_REPO/src/content/field-notes/$SLUG.md"
  if "$SKILL_SCRIPTS/sync-to-intentsolutions.sh" "$ASTRO" >> "$LOG" 2>&1 && [ -f "$FN_FILE" ]; then
    isl_branch=$(default_branch_of "$ISL_REPO"); isl_branch="${isl_branch:-main}"
    if publish_file_to_repo "$ISL_REPO" "$isl_branch" "$FN_FILE" "$FN_FILE" \
        "content(field-notes): add ${SLUG}" "$LOG"; then
      log "Syndicated to intentsolutions.io/field-notes (origin/$isl_branch)"
    else
      log "WARN: field-notes syndication push failed after retries — see log"
    fi
    rm -f "$FN_FILE"   # leave the ISL working tree clean (we pushed via plumbing)
  else
    log "WARN: sync-to-intentsolutions failed — skipping field-notes"
  fi
elif [ "$SYND_FN" -eq 1 ]; then
  log "NOTE: field-notes tags matched but ISL repo/script/astro unavailable — skipping"
fi
[ -n "$ASTRO_TMPD" ] && rm -rf "$ASTRO_TMPD"

# Ledger and queue were durably reconciled before optional image/syndication work.

# ---- Per-post image (runs AFTER the ledger entry exists) --------------------
# Ezekiel posts image plus text; a bare post gets materially less reach. This
# writes an `image` block into the ledger entry the packet reads an hour later.
#
# Deliberately placed AFTER publish and NEVER allowed to fail the land: the post
# is already live and committed by this point, so a vendor having a bad minute
# must not turn a good publish into a quarantine. make-post-image.py falls back
# to the deterministic PIL card on its own, so the worst case here is a card
# instead of generated art, and the packet says so out loud.
#
# BLOG_IMAGE_GEN=0 turns generation off entirely (cards only, no spend).
#
# --outdir/--repo-root MUST name this run's workspace ($BLOG_DIR). The script
# lives in the live checkout, so its defaults point there; without these flags
# the assets landed in the live checkout, the `git add` below found nothing in
# the workspace, and every packet since the 2026-09-15 workspace cutover sent
# Ezekiel image URLs that 404 (found in the 2026-09-24 estate sweep).
if [ "${BLOG_IMAGE_GEN:-1}" = "1" ]; then
  log "Generating post image for $SLUG ..."
  if timeout "${BLOG_IMAGE_TIMEOUT:-420}" python3 "$(dirname "${BASH_SOURCE[0]}")/make-post-image.py" \
      --post "$POST" --outdir "$BLOG_DIR/static/images/posts" --repo-root "$BLOG_DIR" \
      --ledger >> "$LOG" 2>&1; then
    log "  image step complete (see ledger .image for provider, model, and prompt)"
  else
    log "  WARN: image step failed outright; the packet will note the missing image"
  fi
else
  log "Image generation disabled (BLOG_IMAGE_GEN=0); rendering cards only"
  timeout 120 python3 "$(dirname "${BASH_SOURCE[0]}")/make-social-card.py" \
    --post "$POST" --outdir "$BLOG_DIR/static/images/posts/cards" >> "$LOG" 2>&1 || true
fi

# Ship the image assets in their OWN commit. Ezekiel is remote, so a path on this
# box is useless to him: the images have to be deployed and referenced by public
# URL. A second commit (rather than folding them into the post commit) keeps the
# vendor call out of the publish path entirely. If this push fails the post is
# already live and the packet degrades to naming the local file, which is a
# cosmetic loss rather than a failed publish.
#
# push_with_rebase, NOT bare git push. The post push a few seconds earlier
# triggers release.yml, whose bot pushes a changelog commit back to master —
# so by the time this commit is ready, the remote has ALREADY moved and a bare
# push loses the race close to every night. Worse than the cosmetic miss: the
# unpushed commit strands local master AHEAD of origin, the release bot keeps
# moving origin, and the NEXT morning's preflight `git pull --ff-only` refuses
# the diverged state and aborts the producer — no post, no packet. One lost
# race here cost the whole 2026-08-18 publish day (found 2026-08-19).
if git -C "$BLOG_DIR" add static/images/posts >> "$LOG" 2>&1 &&
   ! git -C "$BLOG_DIR" diff --cached --quiet -- static/images/posts; then
  if git -C "$BLOG_DIR" commit \
      -m "assets(${TARGET_DATE}): social image and cards for ${SLUG}" >> "$LOG" 2>&1 &&
     push_with_rebase "$DEPLOY_BRANCH" "$LOG"; then
    log "Image assets committed and pushed"
  else
    # A conflicted `pull --rebase` inside push_with_rebase stops MID-REBASE and
    # leaves the repo in rebase state; everything after this point (crosspost
    # queue, ledger write) would then run against a half-rebased tree. Abort it.
    if [ -d "$BLOG_DIR/.git/rebase-merge" ] || [ -d "$BLOG_DIR/.git/rebase-apply" ]; then
      git -C "$BLOG_DIR" rebase --abort >> "$LOG" 2>&1 || true
      log "aborted a half-finished rebase left by the failed image push"
    fi
    log "WARN: image assets did not push; isolated run evidence retained; canonical publication verified independently"
    # Page, don't just log. A stranded commit here is not cosmetic: it diverges
    # master and the NEXT morning's ff-only preflight aborts the whole producer
    # (2026-08-18 lost its publish day to exactly this, and the only trace was
    # a WARN nobody read). Same pattern as the post-push failure above.
    urgent_alert "⚠ blog-land: image assets commit STRANDED ${TARGET_DATE}" "The image-assets commit for '${SLUG}' could not be pushed after isolated remote-race reconciliation. Canonical source publication is verified; image artifacts and unpublished commit remain in ${BLOG_DIR}. Next-day generation uses a fresh isolated remote baseline and is unaffected. Diagnose the retained run, not the owner's checkout."
  fi
else
  log "No new image assets to commit"
fi

# Process any due cross-posts now (idempotent; skips those not yet past +24h).
"$SKILL_SCRIPTS/check-crosspost-queue.sh" >> "$LOG" 2>&1 || log "WARN: crosspost queue processor returned non-zero"

# ---- Ezekiel posting packet -------------------------------------------------
# The packet is intentionally NOT built here. It is generated by the separate
# blog-posting-packet.sh --sweep cron (05:00 daily),
# which reads this ledger entry. Keeping it out of the land step preserves the
# land step's determinism + leanness (the packet generates voice copy via a
# bounded claude -p — an LLM belongs after the publish gate, never inside it) and
# gives Netlify time to make the post live before the packet's link is used.
log "Ledger entry recorded (packet_sent:false) — the 08:30 posting-packet sweep will build + send the Ezekiel packet."

# ---- Consume the sentinel (mark landed) -------------------------------------
rm -f "$SENTINEL" 2>/dev/null || true

# ---- Liveness gate: STATUS=OK requires the canonical article to answer 200 ---
if remote_live_check "$CANONICAL" "$LIVENESS_MAX_SECS" "$LOG"; then
  log "LAND-RESULT: OK"
  exit 0
else
  log "Source and delivery state are complete, but $CANONICAL is unavailable."
  log "LAND-RESULT: FAILED (source published; public article unavailable)"
  # The wrapper owns the verdict on a slow deploy (PENDING, re-checked at the next run);
  # it sets this so a published post does not page from here as well.
  [ "${BLOG_LAND_QUIET_UNAVAILABLE:-0}" = "1" ] || urgent_alert "blog-land PUBLIC UNAVAILABLE ($TARGET_DATE)" "Source and delivery state are complete; public verification failed. Inspect publication/deployment. Log: $LOG"
  exit 13
fi
