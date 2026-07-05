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
#   3   OK-WARNING    — landed + pushed, but not live yet (Netlify lag / probe)
#   10  QUARANTINED   — a precondition failed; artifacts quarantined, tree clean
#   11  FAILED        — infra failure (push rejected / orphaned)
#   20  NO-POST       — no post exists for the date; nothing to do
#   21  ALREADY-LANDED— post already committed; queue reprocessed, no new commit

set -uo pipefail

# ---- Configuration ----------------------------------------------------------
BLOG_DIR=/home/jeremy/000-projects/blog/startaitools
POSTS_DIR="$BLOG_DIR/content/posts"
DECISIONS="$BLOG_DIR/.claude/skills/blog-backfill/methodology/decisions.jsonl"
STAGING_DIR="$BLOG_DIR/.blog-staging"
QUARANTINE_DIR="$BLOG_DIR/.blog-quarantine"
QUEUE_FILE="$BLOG_DIR/.crosspost-queue.json"
LEDGER_FILE="$BLOG_DIR/.blog-syndication-ledger.json"
CCP_REPO=/home/jeremy/000-projects/claude-code-plugins
CCP_BLOG_DIR="$CCP_REPO/marketplace/src/content/blog-posts"
ISL_REPO=/home/jeremy/000-projects/intent-solutions-landing/astro-site
SKILL_SCRIPTS="$BLOG_DIR/.claude/skills/blog-backfill/scripts"
EMAIL_SCRIPT=/home/jeremy/.claude/skills/email/scripts/send-email.cjs
CANONICAL_BASE="https://startaitools.com/posts"
LIVENESS_MAX_SECS="${BLOG_LAND_LIVENESS_SECS:-360}"
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

LOG_DIR=/home/jeremy/.local/state/blog-land
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
# Urgent alert (ntfy high + email). Used for quarantine + orphan — always loud,
# regardless of whether a wrapper will also summarize.
urgent_alert() {
  local title="$1" body="$2" prio="${3:-high}"
  local topic; topic=$(cat /home/jeremy/.ntfy-topic 2>/dev/null)
  [ -n "$topic" ] && curl -s -H "Title: $title" -H "Priority: $prio" -H "Tags: rotating_light" \
    -d "$body" "https://ntfy.sh/$topic" >/dev/null 2>&1 || true
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
if [ "$CUR_BRANCH" != "$DEPLOY_BRANCH" ]; then
  log "NOTE: on '$CUR_BRANCH', deploy branch is '$DEPLOY_BRANCH' — not force-switching (staged changes present). Landing on current branch would not deploy; refusing."
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
  # Still make sure any due cross-posts get processed + verify live.
  [ "$DRY_RUN" -eq 0 ] && "$SKILL_SCRIPTS/check-crosspost-queue.sh" >> "$LOG" 2>&1 || true
  rm -f "$STAGING_DIR/${TARGET_DATE}.intent.json" 2>/dev/null || true
  if remote_live_check "$CANONICAL" 60 "$LOG"; then log "LAND-RESULT: ALREADY-LANDED (live)"; else log "LAND-RESULT: ALREADY-LANDED (not live)"; fi
  exit 21
fi

# ---- Precondition gate ------------------------------------------------------
SENTINEL="$STAGING_DIR/${TARGET_DATE}.intent.json"
declare -a REASONS=()

# (1) Readiness sentinel: the skill's explicit "all gates passed, safe to ship".
#     Its absence / ready!=true is the primary catch for a timed-out or
#     fact-check-blocked run.
if validate_json "$SENTINEL"; then
  READY=$(jq -r '.ready // false' "$SENTINEL" 2>/dev/null)
  [ "$READY" = "true" ] || REASONS+=("readiness sentinel present but ready!=true (skill did not attest all gates passed)")
else
  REASONS+=("readiness sentinel missing or invalid at $SENTINEL (skill did not finish — timeout or blocked gate)")
fi

# (2) Classifier record for the date (methodology step 3).
grep -q "\"date\"[[:space:]]*:[[:space:]]*\"$TARGET_DATE\"" "$DECISIONS" 2>/dev/null \
  || REASONS+=("no classifier record for $TARGET_DATE in decisions.jsonl (step 3 skipped)")

# (3) Step-8 agent_audit addendum for the slug.
grep "\"slug\"[[:space:]]*:[[:space:]]*\"$SLUG\"" "$DECISIONS" 2>/dev/null | grep -q 'audit_addendum' \
  || REASONS+=("no agent_audit addendum for $SLUG (step 8 skipped)")

# (4) Hugo build must pass (catches broken front matter / bad shortcodes).
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
  # --- Quarantine: move stranded artifacts out so the tree is clean tomorrow ---
  QDIR="$QUARANTINE_DIR/$(date +%Y%m%dT%H%M%S)-${SLUG}"
  mkdir -p "$QDIR"
  { printf 'Quarantined: %s\nDate: %s\nSlug: %s\n\nReasons:\n' "$(date -Is)" "$TARGET_DATE" "$SLUG"
    for r in "${REASONS[@]}"; do printf '  - %s\n' "$r"; done; } > "$QDIR/REASON.txt"
  # Post file: unstage if staged, then move the working file aside.
  git reset -q HEAD -- "$POST_REL" 2>/dev/null || true
  [ -f "$POST" ] && mv -f "$POST" "$QDIR/" && log "quarantined post → $QDIR/"
  # decisions.jsonl: preserve the uncommitted diff, then restore to HEAD so the
  # tracked tree is clean (decisions.jsonl records PUBLISHED posts only).
  git diff -- "$DECISIONS" > "$QDIR/decisions.diff" 2>/dev/null || true
  git checkout -- "$DECISIONS" 2>/dev/null || true
  # Sentinel: move aside if present.
  [ -f "$SENTINEL" ] && mv -f "$SENTINEL" "$QDIR/" 2>/dev/null || true
  # Verify the tracked blog paths are clean now.
  if [ -z "$(git status --porcelain content/posts .claude/skills/blog-backfill/methodology/decisions.jsonl 2>/dev/null)" ]; then
    log "Tree clean after quarantine — tomorrow's run is unblocked."
  else
    log "WARN: tracked blog paths still show changes after quarantine:"
    git status --porcelain content/posts .claude/skills/blog-backfill/methodology/decisions.jsonl >> "$LOG" 2>&1
  fi
  urgent_alert "🚨 blog post QUARANTINED: ${TARGET_DATE}" "Post '${SLUG}' failed preconditions and was quarantined (NOT published). Reasons: ${REASONS[*]}. Files: ${QDIR}"
  log "LAND-RESULT: QUARANTINED"
  exit 10
fi

log "All preconditions passed."
TITLE=$(fm_title "$POST" "$SLUG")
# Pick the tier from the CLASSIFIER record (the one carrying a .tier), not the
# step-8 audit_addendum line which also matches the date but has no tier.
TIER=$(grep "\"date\"[[:space:]]*:[[:space:]]*\"$TARGET_DATE\"" "$DECISIONS" 2>/dev/null \
  | jq -r 'select(.tier != null) | .tier' 2>/dev/null | tail -1); TIER="${TIER:-1}"
log "Title: $TITLE | Tier: $TIER"

if [ "$DRY_RUN" -eq 1 ]; then
  log "DRY-RUN: would commit '$POST_REL' + decisions, push origin/$DEPLOY_BRANCH, dual-publish, queue (tier=$TIER), verify $CANONICAL."
  log "LAND-RESULT: OK (dry-run)"
  exit 0
fi

# ---- Land: commit + push (canonical) ---------------------------------------
git add "$POST_REL" ".claude/skills/blog-backfill/methodology/decisions.jsonl"
if git commit --no-verify -m "post(${TARGET_DATE}): ${TITLE} — Tier ${TIER}" >> "$LOG" 2>&1; then
  log "Committed $SLUG on $DEPLOY_BRANCH ($(git rev-parse --short HEAD))"
else
  log "commit produced nothing (already committed?) — continuing"
fi
if git push origin "$DEPLOY_BRANCH" >> "$LOG" 2>&1; then
  log "Pushed to origin/$DEPLOY_BRANCH"
else
  log "push rejected — attempting pull --rebase then re-push"
  if git pull --rebase origin "$DEPLOY_BRANCH" >> "$LOG" 2>&1 && git push origin "$DEPLOY_BRANCH" >> "$LOG" 2>&1; then
    log "Re-push succeeded after rebase"
  else
    log "FATAL: could not push $SLUG to origin/$DEPLOY_BRANCH"
    urgent_alert "🚨 blog-land: push FAILED ${TARGET_DATE}" "Committed '${SLUG}' locally but could NOT push to origin/${DEPLOY_BRANCH}. Post is committed but NOT live. Manual push needed."
    log "LAND-RESULT: FAILED (orphaned local commit)"
    exit 11
  fi
fi

# ---- Dual-publish to tonsofskills (best-effort) -----------------------------
if [ -d "$CCP_REPO/.git" ] && [ -x "$SKILL_SCRIPTS/transform-hugo-to-astro.sh" ]; then
  mkdir -p "$CCP_BLOG_DIR"
  if "$SKILL_SCRIPTS/transform-hugo-to-astro.sh" "$POST" "$CCP_BLOG_DIR/$SLUG.md" >> "$LOG" 2>&1; then
    ccp_branch=$(default_branch_of "$CCP_REPO"); ccp_branch="${ccp_branch:-main}"
    if ( cd "$CCP_REPO" \
      && git add "marketplace/src/content/blog-posts/$SLUG.md" \
      && git commit --no-verify -m "content(blog): dual-publish ${SLUG} to tonsofskills.com/blog" >> "$LOG" 2>&1 \
      && git push origin "$ccp_branch" >> "$LOG" 2>&1 ); then
      log "Dual-published to tonsofskills (origin/$ccp_branch)"
    else
      log "WARN: dual-publish to tonsofskills failed (canonical already live) — see log"
    fi
  else
    log "WARN: transform-hugo-to-astro failed — skipping dual-publish"
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
if [ "$SYND_FN" -eq 1 ] && [ -d "$ISL_REPO/.git" ] && [ -x "$SKILL_SCRIPTS/sync-to-intentsolutions.sh" ]; then
  if "$SKILL_SCRIPTS/sync-to-intentsolutions.sh" "$CCP_BLOG_DIR/$SLUG.md" >> "$LOG" 2>&1; then
    isl_branch=$(default_branch_of "$ISL_REPO"); isl_branch="${isl_branch:-main}"
    if ( cd "$ISL_REPO" \
      && git add "src/content/field-notes/$SLUG.md" \
      && git commit --no-verify -m "content(field-notes): add ${SLUG}" >> "$LOG" 2>&1 \
      && git push origin "$isl_branch" >> "$LOG" 2>&1 ); then
      log "Syndicated to intentsolutions.io/field-notes (origin/$isl_branch)"
    else
      log "WARN: field-notes syndication failed — see log"
    fi
  else
    log "WARN: sync-to-intentsolutions failed — skipping field-notes"
  fi
elif [ "$SYND_FN" -eq 1 ]; then
  log "NOTE: field-notes tags matched but ISL repo/script unavailable — skipping"
fi

# ---- Syndication ledger (all tiers) + crosspost queue (tier>=2) -------------
PUBLISHED_AT=$(date -Is)
GH_LINKS=$(grep -oE 'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+' "$POST" 2>/dev/null | sed 's/[.,)]*$//' | sort -u | jq -R . | jq -s . 2>/dev/null)
[ -z "$GH_LINKS" ] && GH_LINKS='[]'

# Syndication ledger: the single home for the per-post "did-he-post" record that
# the Ezekiel packet + weekly rollup read/update. Replaces the vestigial
# substack_emailed/x_thread_emailed booleans (which lived, unused, in the queue).
# Tier gates destinations: T1 → X + LinkedIn only; T2/3 → + Substack + Medium.
subm_status="n/a"; [ "$TIER" -ge 2 ] && subm_status="pending"
LEDGER_ENTRY=$(jq -n \
  --arg date "$TARGET_DATE" --arg slug "$SLUG" --arg title "$TITLE" \
  --arg url "$CANONICAL" --argjson tier "$TIER" --arg pub "$PUBLISHED_AT" \
  --argjson gh "$GH_LINKS" --arg subm "$subm_status" '
  {date:$date, slug:$slug, title:$title, canonical_url:$url, tier:$tier,
   published_at:$pub, github_links:$gh, packet_sent:false,
   syndication:{
     x:           {status:"pending", posted_at:null, url:null, by:null},
     li_personal: {status:"pending", posted_at:null, url:null, by:null},
     li_company:  {status:"pending", posted_at:null, url:null, by:null},
     substack:    {status:$subm,     posted_at:null, url:null, by:null},
     medium:      {status:$subm,     posted_at:null, url:null, by:null}
   }}')
validate_json "$LEDGER_FILE" || echo '[]' > "$LEDGER_FILE"
# De-dupe by slug (re-entrant), then append.
if jq --argjson e "$LEDGER_ENTRY" '[.[] | select(.slug != ($e.slug))] + [$e]' "$LEDGER_FILE" \
  | atomic_json_write "$LEDGER_FILE"; then
  log "Syndication ledger updated for $SLUG"
else
  log "WARN: could not update syndication ledger"
fi

# Crosspost queue (dev.to + hashnode APIs), tier>=2 only.
if [ "$TIER" -ge 2 ]; then
  AFTER_24H=$(date -d "$PUBLISHED_AT + 24 hours" -Is 2>/dev/null || date -Is)
  QUEUE_ENTRY=$(jq -n \
    --arg slug "$SLUG" --arg title "$TITLE" --arg url "$CANONICAL" \
    --arg pub "$PUBLISHED_AT" --arg after "$AFTER_24H" --argjson tier "$TIER" '
    {slug:$slug, title:$title, canonical_url:$url, published_at:$pub, tier:$tier,
     devto:{status:"pending", publish_after:$after},
     hashnode:{status:"pending", publish_after:$after},
     medium:{status:"skipped", error:"No MEDIUM_INTEGRATION_TOKEN; Medium API cross-posting retired."}}')
  validate_json "$QUEUE_FILE" || echo '[]' > "$QUEUE_FILE"
  if jq --argjson e "$QUEUE_ENTRY" '[.[] | select(.slug != ($e.slug))] + [$e]' "$QUEUE_FILE" \
    | atomic_json_write "$QUEUE_FILE"; then
    log "Crosspost queue appended for $SLUG (tier $TIER)"
  else
    log "WARN: could not append crosspost queue"
  fi
else
  log "Tier $TIER — no API cross-post queued (T1 = startaitools + tonsofskills only)."
fi

# Process any due cross-posts now (idempotent; skips those not yet past +24h).
"$SKILL_SCRIPTS/check-crosspost-queue.sh" >> "$LOG" 2>&1 || log "WARN: crosspost queue processor returned non-zero"

# ---- Ezekiel posting packet -------------------------------------------------
# The packet is intentionally NOT built here. It is generated by the separate
# blog-posting-packet.sh --sweep cron (08:30, replacing blog-social-email.sh),
# which reads this ledger entry. Keeping it out of the land step preserves the
# land step's determinism + leanness (the packet generates voice copy via a
# bounded claude -p — an LLM belongs after the publish gate, never inside it) and
# gives Netlify time to make the post live before the packet's link is used.
log "Ledger entry recorded (packet_sent:false) — the 08:30 posting-packet sweep will build + send the Ezekiel packet."

# ---- Consume the sentinel (mark landed) -------------------------------------
rm -f "$SENTINEL" 2>/dev/null || true

# ---- Liveness gate: STATUS=OK requires the live URL to answer 2xx -----------
if remote_live_check "$CANONICAL" "$LIVENESS_MAX_SECS" "$LOG"; then
  log "LAND-RESULT: OK"
  exit 0
else
  log "Pushed successfully but $CANONICAL is not live yet (Netlify build lag or failure)."
  log "LAND-RESULT: OK-WARNING (pushed, not live)"
  exit 3
fi
