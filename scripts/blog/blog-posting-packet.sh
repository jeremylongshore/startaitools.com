#!/usr/bin/env bash
# blog-posting-packet.sh — build + email the per-post social "posting packet" to
# Ezekiel (WS2). Replaces blog-social-email.sh.
#
# WHAT IT DOES
#   For each published post that has not yet had a packet sent (tracked by
#   packet_sent in .blog-syndication-ledger.json), it:
#     1. generates the three voice pieces via a bounded `claude -p` — X (raw,
#        punchy), LinkedIn personal (Jeremy, first person), LinkedIn company
#        (Intent Solutions) — following references/social-bundle.md. The MODEL
#        writes only the persuasive copy; it never writes the links.
#     2. DETERMINISTICALLY appends the UTM-tagged deep-dive link + GitHub "Code:"
#        links (UTM is the measurement keystone — it must not depend on the model
#        getting a query string right; utm_source = x|linkedin|substack|medium).
#     3. selects any required disclaimers from the APPROVED disclaimer-library.json
#        (fails closed → HOLD banner if a governed entity has no approved string).
#     4. renders the v3 HTML (blog-packet-html.cjs) and emails it TO Ezekiel,
#        CC Jeremy.
#     5. marks packet_sent:true in the ledger (send-exactly-once).
#
# Determinism note: this is the ONE place an LLM touches the syndication path, and
# it runs AFTER the post is already published + live — so a flaky/slow model can
# never block a publish. If voice-gen fails, a DEGRADED packet still goes out
# (canonical + UTM links + "write the copy manually") — silence is never valid.
#
# Usage:
#   blog-posting-packet.sh <YYYY-MM-DD>   # build+send the packet for that post
#   blog-posting-packet.sh --sweep        # cron mode: all unpacketed posts (merged
#                                          # into ONE email); heartbeat if none
#   blog-posting-packet.sh <...> --dry-run # build the HTML, print path, send nothing

set -uo pipefail

# Force a UTF-8 locale so every text tool (grep/sed/jq/iconv) treats model output
# as UTF-8, not bytes. Cron/claude-p subprocesses can otherwise inherit C/POSIX.
export LC_ALL="${LC_ALL:-C.UTF-8}" LANG="${LANG:-C.UTF-8}"

BLOG_DIR=/home/jeremy/000-projects/blog/startaitools
POSTS_DIR="$BLOG_DIR/content/posts"
LEDGER_FILE="$BLOG_DIR/.blog-syndication-ledger.json"
# Thread A (2026-07-16): skill INSTRUCTIONS (incl. references/) moved to ~/.claude/skills/.
# Only methodology/ + scripts/ stayed in-repo. SKILL_DIR here is used ONLY for references/
# files, so it points at the global skill dir. (disclaimer-library.json is Jeremy-approved
# governed config that lost repo version-control in the move — flagged for Thread C, which
# re-homes disclaimers into a governed intent-os source of truth.)
SKILL_DIR="/home/jeremy/.claude/skills/blog-backfill"
DISCLAIMER_LIB="$SKILL_DIR/references/disclaimer-library.json"
VOICE_SPEC="$SKILL_DIR/references/social-bundle.md"
HTML_GEN="$(dirname "${BASH_SOURCE[0]}")/blog-packet-html.cjs"
EMAIL_SCRIPT=/home/jeremy/.claude/skills/email/scripts/send-email.cjs
X_DIR=/home/jeremy/000-projects/blog/x-threads
LI_DIR=/home/jeremy/000-projects/blog/linkedin-posts
LOG_DIR=/home/jeremy/.local/state/blog-posting-packet
mkdir -p "$LOG_DIR" "$X_DIR" "$LI_DIR"
LOG="$LOG_DIR/packet-$(date +%Y-%m-%d).log"
# Rolling record of recent LinkedIn openers so consecutive posts never share a first
# line. Without it the model defaults to leading with Jeremy's operator backstory
# every time. generate_voice reads it into the prompt; build_payload appends to it.
RECENT_LI_OPENERS="$LOG_DIR/recent-li-openers.txt"

# shellcheck source=./lib-cron-common.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib-cron-common.sh"
# NOTE: log to STDERR (not stdout) — build_payload/generate_voice are captured via
# $(...) and any log line on stdout would pollute the captured JSON payload.
log() { echo "[$(date -Is)] $*" | tee -a "$LOG" >&2; }

# Shared notify spine (~/bin/lib/notify-lib.sh): a per-run heartbeat for the daily
# liveness sweep + a plain-English #cron-failures alert on any abnormal exit.
# Guarded so a fresh clone without the lib still runs. This is what stops the
# Ezekiel packet from failing SILENTLY — a broken send now pages instead of
# vanishing (the 2026-07-08 "the email never fired" lesson).
if [ -f "$HOME/bin/lib/notify-lib.sh" ]; then
  # shellcheck disable=SC1091
  source "$HOME/bin/lib/notify-lib.sh"
  arm_fail_trap "blog-posting-packet" "$LOG"
fi

# --- Config: recipients ------------------------------------------------------
# Packet goes TO Ezekiel only (the team gets the weekly rollup, not per-post CC).
# CC Jeremy for oversight. EZEKIEL_EMAIL / PACKET_CC come from blog/.env (or env,
# or repeatable --to/--cc). Sourcing .env lets Jeremy re-point recipients without
# editing the script.
# Recipients (EZEKIEL_EMAIL/PACKET_CC) come from the PARENT blog/.env (where the
# blog secrets actually live); $BLOG_DIR/.env (startaitools/.env) doesn't exist.
# Defaults below cover the missing-file case, so this only matters for overrides.
for _envf in "$(dirname "$BLOG_DIR")/.env" "$BLOG_DIR/.env"; do
  if [ -f "$_envf" ]; then set -a; # shellcheck disable=SC1090,SC1091
    source "$_envf"; set +a; break; fi
done
EZEKIEL_EMAIL="${EZEKIEL_EMAIL:-ezekiel@intentsolutions.io}"
PACKET_CC="${PACKET_CC:-jeremy@intentsolutions.io}"
VOICE_TIMEOUT="${PACKET_VOICE_TIMEOUT:-300}"

# --- Args --------------------------------------------------------------------
MODE=""; TARGET_DATE=""; DRY_RUN=0
declare -a EXTRA_TO=(); declare -a EXTRA_CC=()
while [ $# -gt 0 ]; do
  case "$1" in
    --sweep) MODE="sweep" ;;
    --dry-run) DRY_RUN=1 ;;
    --to) EXTRA_TO+=("$2"); shift ;;
    --cc) EXTRA_CC+=("$2"); shift ;;
    [0-9]*-[0-9]*-[0-9]*) MODE="date"; TARGET_DATE="$1" ;;
    *) echo "Unknown arg: $1" >&2; exit 64 ;;
  esac
  shift
done
[ -z "$MODE" ] && { echo "Usage: blog-posting-packet.sh <YYYY-MM-DD> | --sweep [--dry-run]" >&2; exit 64; }

# --- Helpers -----------------------------------------------------------------
utm() { # <bare_url> <source>
  # Minimal UTM — just utm_source (x|linkedin|substack|medium). That's all the
  # weekly rollup's utm_source breakdown needs; the extra utm_medium/campaign/
  # content tail only made the pasted links long and ugly. Keep links short.
  local url="$1" src="$2"
  local sep="?"; [[ "$url" == *"?"* ]] && sep="&"
  printf '%sutm_source=%s' "$url$sep" "$src"
}

fm_title() { sed -n "s/^title = ['\"]\(.*\)['\"] *$/\1/p" "$1" | head -1; }

# Body text without front matter (for voice-gen + entity matching).
post_body() { awk 'f{print} /^\+\+\+|^---/{c++} c==2 && !f {f=1}' "$1"; }

# First ~12 words of a LinkedIn opener on one line — the fingerprint kept in
# RECENT_LI_OPENERS so back-to-back posts can't share a first sentence.
li_opener() {
  printf '%s' "$1" | tr '\n' ' ' | sed 's/  */ /g; s/^ *//' \
    | cut -d. -f1 | awk '{n=(NF<12?NF:12); for(i=1;i<=n;i++) printf "%s%s", $i, (i<n?" ":""); print ""}'
}

# Disclaimer selection. Echoes approved notes (one per line) on fd1; if a governed
# entity matches but has NO approved string, prints "HOLD:<entity>" and returns 1.
select_disclaimers() { # <body_file>
  local body_file="$1" body ent match n
  [ -f "$DISCLAIMER_LIB" ] || return 0
  body=$(tr '[:upper:]' '[:lower:]' < "$body_file")
  local hold=0
  for ent in $(jq -r '.entities | keys[]' "$DISCLAIMER_LIB" 2>/dev/null); do
    local matched=0
    while IFS= read -r match; do
      [ -z "$match" ] && continue
      case "$body" in *"$(printf '%s' "$match" | tr '[:upper:]' '[:lower:]')"*) matched=1; break;; esac
    done < <(jq -r --arg e "$ent" '.entities[$e].match[]?' "$DISCLAIMER_LIB" 2>/dev/null)
    [ "$matched" -eq 0 ] && continue
    n=$(jq -r --arg e "$ent" '.entities[$e].approved | length' "$DISCLAIMER_LIB" 2>/dev/null)
    if [ "${n:-0}" -eq 0 ]; then
      echo "HOLD:${ent}"
      hold=1
    else
      jq -r --arg e "$ent" '.entities[$e].approved[]' "$DISCLAIMER_LIB" 2>/dev/null
    fi
  done
  return "$hold"
}

# Generate voice copy via a bounded claude -p. Echoes a JSON object on success,
# nothing on failure. NEVER writes links (bash appends those deterministically).
generate_voice() { # <post_file> <title> <tier>
  local post_file="$1" title="$2" tier="$3" body prompt raw json
  body=$(post_body "$post_file" | head -400)
  local spec=""
  [ -f "$VOICE_SPEC" ] && spec=$(cat "$VOICE_SPEC")
  # Test hook: skip the LLM entirely when PACKET_VOICE_STUB=1 (structural testing).
  if [ "${PACKET_VOICE_STUB:-0}" = "1" ]; then
    printf '{"x_post":"STUB x copy — punchy raw voice.","x_is_thread":false,"li_personal":"STUB LinkedIn personal copy in Jeremy first person.","li_company":"STUB Intent Solutions company copy, third person.","substack_subtitle":"STUB subtitle."}'
    return 0
  fi
  # ALWAYS a single tweet — the account has an extended character limit, so one
  # long post is preferred and threads are never used.
  local thread_hint="a SINGLE tweet — ALWAYS one post, NEVER a thread. The account pays for the extended character limit, so a longer single tweet is fine and preferred. Set x_is_thread false."
  # Recent LinkedIn openers to steer away from (cross-post variety).
  local recent="" avoid_block=""
  [ -s "$RECENT_LI_OPENERS" ] && recent=$(tail -12 "$RECENT_LI_OPENERS")
  if [ -n "$recent" ]; then
    avoid_block="
=== RECENT LINKEDIN OPENERS — DO NOT REUSE OR PARAPHRASE ===
Recent LinkedIn posts opened with the lines below. li_personal AND li_company must
each open with a DIFFERENT first sentence — different structure, different hook,
different first five words. Do not echo or paraphrase any of these:
${recent}
=== END RECENT OPENERS ==="
  fi
  prompt=$(cat <<PROMPT
You are writing social copy to syndicate a blog post. Follow this voice spec EXACTLY:

=== VOICE SPEC ===
${spec}
=== END SPEC ===

POST TITLE: ${title}
TIER: ${tier}

POST BODY (context — do not copy verbatim):
${body}

Produce copy for three DISTINCT voices. Hard rules:
- Write ONLY the persuasive copy. Do NOT include any URLs, "Deep-dive:", "Code:",
  "Read:", or hash(link) lines — those are appended automatically. (Hashtags are fine.)
- X, li_personal, and li_company must EACH open with a DISTINCT first sentence — no
  two may share an opener, and none may reuse a recent opener listed below.
- Banned phrases (never use): "excited to share", "thrilled to", "dive into",
  "in today's fast-paced", "game-changer", "unlock", "delve".
- x_post: casual, punchy, unfiltered "raw" voice. ${thread_hint}.
- li_personal: Jeremy's first-person professional voice. VARY THE ENTRY POINT every
  time — lead with a specific detail from THIS post, a question, a number, or a claim.
  His operator background (20 yrs restaurants + trucking before software) is available
  as an OCCASIONAL angle, but do NOT open with it by default — most posts should open
  on the technical substance, not the backstory. End with a line like "Deep-dive +
  code in the comments." (no actual link).
- li_company: Intent Solutions brand voice, third person, serious/professional — with a
  distinctly different opening from li_personal.
- substack_subtitle: one-line subtitle for the Substack long-form.
${avoid_block}

Output ONLY a single minified JSON object, no markdown fences, with keys:
x_post, x_is_thread (boolean), li_personal, li_company, substack_subtitle
PROMPT
)
  raw=$(timeout "$VOICE_TIMEOUT" claude -p "$prompt" --dangerously-skip-permissions 2>>"$LOG")
  # Sanitize: drop any truly-invalid byte sequences (iconv -c) AND strip literal
  # U+FFFD replacement chars (0xEF 0xBF 0xBD) that the model/CLI may have emitted
  # mid-word (this is what produced "allowed<?>lse" in an early packet). No <?>
  # glyph can reach Ezekiel after this; a fresh regen won't have it at all.
  if printf '%s' "$raw" | grep -q $'\xEF\xBF\xBD'; then
    log "  WARN: U+FFFD replacement char in model output — stripping (regen recommended)"
  fi
  raw=$(printf '%s' "$raw" | iconv -f UTF-8 -t UTF-8 -c 2>/dev/null | sed $'s/\xEF\xBF\xBD//g')
  # Extract the JSON object: flatten to one line, greedily grab first { … last }.
  json=$(printf '%s' "$raw" | tr '\n' ' ' | grep -o '{.*}' | head -1)
  if printf '%s' "$json" | jq -e . >/dev/null 2>&1; then
    printf '%s' "$json"
    return 0
  fi
  return 1
}

# Build ONE post's payload JSON (echoed on fd1). Uses the ledger entry $1 (JSON).
build_payload() { # <ledger_entry_json>
  local entry="$1"
  local slug title canonical tier gh_json
  slug=$(printf '%s' "$entry" | jq -r '.slug')
  title=$(printf '%s' "$entry" | jq -r '.title')
  canonical=$(printf '%s' "$entry" | jq -r '.canonical_url')
  tier=$(printf '%s' "$entry" | jq -r '.tier // 1')
  gh_json=$(printf '%s' "$entry" | jq -c '.github_links // []')
  local post_file="$POSTS_DIR/$slug.md"

  # Destinations by tier.
  local -a dests=("x" "li_personal" "li_company")
  [ "$tier" -ge 2 ] && dests+=("substack" "medium")
  local dests_json; dests_json=$(printf '%s\n' "${dests[@]}" | jq -R . | jq -sc .)

  # Disclaimers (fail-closed).
  local body_tmp; body_tmp=$(mktemp); post_body "$post_file" > "$body_tmp"
  local notes hold=0 hold_reason=""
  notes=$(select_disclaimers "$body_tmp")
  local -a note_arr=()
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    if [[ "$line" == HOLD:* ]]; then hold=1; hold_reason="Post mentions a governed entity ('${line#HOLD:}') with no Jeremy-approved disclaimer. Approve wording in disclaimer-library.json before posting."; else note_arr+=("$line"); fi
  done <<< "$notes"
  rm -f "$body_tmp"
  local notes_json; notes_json=$(printf '%s\n' "${note_arr[@]:-}" | jq -R . | jq -sc '[.[] | select(length>0)]')

  # UTM links.
  local link_x link_li_p link_li_c
  link_x=$(utm "$canonical" "x")
  link_li_p=$(utm "$canonical" "linkedin" "personal")
  link_li_c=$(utm "$canonical" "linkedin" "company")

  # GitHub "Code:" line.
  local gh_line=""
  local gh_count; gh_count=$(printf '%s' "$gh_json" | jq 'length')
  if [ "${gh_count:-0}" -gt 0 ]; then
    gh_line=$(printf '%s' "$gh_json" | jq -r 'join(" · ")')
  fi
  # Quality gate: repo-centric post with no github link → warn note.
  if [ "${gh_count:-0}" -eq 0 ] && grep -qiE 'github\.com|open source|open-source|repo\b' "$post_file" 2>/dev/null; then
    note_arr+=("⚠ No GitHub link was auto-detected but this post looks repo-related — add the Code: link manually if it has one.")
    notes_json=$(printf '%s\n' "${note_arr[@]:-}" | jq -R . | jq -sc '[.[] | select(length>0)]')
  fi

  # Voice content.
  local voice x_post x_thread li_p li_c subtitle
  if voice=$(generate_voice "$post_file" "$title" "$tier"); then
    x_post=$(printf '%s' "$voice" | jq -r '.x_post // ""')
    x_thread=false   # never a thread — single tweet always (extended char limit)
    li_p=$(printf '%s' "$voice" | jq -r '.li_personal // ""')
    li_c=$(printf '%s' "$voice" | jq -r '.li_company // ""')
    subtitle=$(printf '%s' "$voice" | jq -r '.substack_subtitle // ""')
    log "  voice generated for $slug"
    # Remember these openers so the NEXT post won't repeat them (real sends only;
    # a dry-run must not poison the history). Cap at the last 24 lines.
    if [ "$DRY_RUN" -eq 0 ]; then
      { li_opener "$li_p"; li_opener "$li_c"; } >> "$RECENT_LI_OPENERS" 2>/dev/null || true
      if tail -n 24 "$RECENT_LI_OPENERS" > "${RECENT_LI_OPENERS}.tmp" 2>/dev/null; then
        mv -f "${RECENT_LI_OPENERS}.tmp" "$RECENT_LI_OPENERS" 2>/dev/null || true
      fi
    fi
  else
    log "  WARN: voice-gen failed for $slug — degraded packet"
    x_post="[voice copy failed to generate — write the X post manually]"
    x_thread=false
    li_p="[write the LinkedIn personal post manually]"
    li_c="[write the LinkedIn company post manually]"
    subtitle=""
    note_arr+=("⚠ Automated copy generation failed for this post — the X/LinkedIn boxes are placeholders. Write the copy from the article, or ping Jeremy.")
    notes_json=$(printf '%s\n' "${note_arr[@]:-}" | jq -R . | jq -sc '[.[] | select(length>0)]')
  fi

  # Deterministically append links.
  local x_final li_p_comment li_c_comment
  x_final="$x_post"$'\n\n'"Deep-dive: $link_x"
  [ -n "$gh_line" ] && x_final="$x_final"$'\n'"Code: $gh_line"
  li_p_comment="Deep-dive: $link_li_p"
  [ -n "$gh_line" ] && li_p_comment="$li_p_comment"$'\n'"Code: $gh_line"
  li_c_comment="Read: $link_li_c"
  [ -n "$gh_line" ] && li_c_comment="$li_c_comment"$'\n'"Code: $gh_line"

  local footer; footer=$(jq -r '.default_footer' "$DISCLAIMER_LIB" 2>/dev/null)

  jq -n \
    --arg title "$title" --arg canonical "$canonical" --argjson tier "$tier" \
    --argjson dests "$dests_json" --argjson notes "$notes_json" \
    --arg lx "$link_x" --arg lsc "$canonical" --arg lmc "$canonical" \
    --arg xp "$x_final" --argjson xt "$x_thread" \
    --arg lip "$li_p" --arg lipc "$li_p_comment" \
    --arg lic "$li_c" --arg licc "$li_c_comment" \
    --arg sub "$subtitle" --arg footer "$footer" \
    --argjson hold "$hold" --arg hr "$hold_reason" '
    {post_title:$title, canonical_url:$canonical, tier:$tier, destinations:$dests,
     before_notes:$notes,
     links:{x:$lx, substack_canonical:$lsc, medium_canonical:$lmc},
     x_post:$xp, x_is_thread:$xt,
     li_personal:$lip, li_personal_comment:$lipc,
     li_company:$lic, li_company_comment:$licc,
     substack_subtitle:$sub, footer:$footer,
     hold:($hold==1), hold_reason:$hr}'
}

mark_sent() { # <slug>
  local slug="$1"
  validate_json "$LEDGER_FILE" || return 1
  jq --arg s "$slug" 'map(if .slug==$s then .packet_sent=true else . end)' "$LEDGER_FILE" \
    | atomic_json_write "$LEDGER_FILE"
}

send_packet() { # <html_file> <subject>
  local html="$1" subject="$2"
  local -a to_args=(--to "$EZEKIEL_EMAIL")
  for t in "${EXTRA_TO[@]:-}"; do [ -n "$t" ] && to_args+=(--to "$t"); done
  [ -n "$PACKET_CC" ] && to_args+=(--cc "$PACKET_CC")
  for c in "${EXTRA_CC[@]:-}"; do [ -n "$c" ] && to_args+=(--cc "$c"); done
  if [ "$DRY_RUN" -eq 1 ]; then
    log "DRY-RUN: would email '$subject' to $EZEKIEL_EMAIL (cc $PACKET_CC). HTML: $html"
    return 0
  fi
  node "$EMAIL_SCRIPT" "${to_args[@]}" --subject "$subject" --html "$html"
}

# --- Main --------------------------------------------------------------------
log "=== posting-packet start (mode=$MODE date=${TARGET_DATE:-} dry_run=$DRY_RUN) ==="

# Collect target ledger entries.
validate_json "$LEDGER_FILE" || log "No/invalid ledger at $LEDGER_FILE — nothing to do."
declare -a ENTRIES=()
if [ "$MODE" = "date" ]; then
  entry=$(jq -c --arg d "$TARGET_DATE" '.[] | select(.date==$d)' "$LEDGER_FILE" 2>/dev/null | head -1)
  [ -n "$entry" ] && ENTRIES+=("$entry")
else # sweep: all unpacketed
  while IFS= read -r e; do [ -n "$e" ] && ENTRIES+=("$e"); done < <(jq -c '.[] | select(.packet_sent != true)' "$LEDGER_FILE" 2>/dev/null)
fi

if [ "${#ENTRIES[@]}" -eq 0 ]; then
  # Heartbeat: silence is never valid on the sweep cron.
  if [ "$MODE" = "sweep" ]; then
    # No packet today is a valid no-op — it warrants no ping. The per-run
    # heartbeat (notify-lib arm_fail_trap) records that the sweep ran, and the
    # daily liveness sweep is what catches this cron if it ever stops firing.
    # (ntfy retired 2026-06-13 — the old NO-PACKET heartbeat went nowhere.)
    log "No unpacketed posts — nothing to send (heartbeat records the run)."
  else
    log "No ledger entry for $TARGET_DATE — nothing to build."
  fi
  log "=== posting-packet end (0 packets) ==="
  exit 0
fi

# Build each post's HTML fragment; merge into ONE email (never N emails).
TMP_HTML=$(mktemp --suffix=.html)
{
  echo '<div style="font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;font-size:15px;line-height:1.55;color:#1a1a1a;max-width:720px">'
  if [ "${#ENTRIES[@]}" -gt 1 ]; then
    echo "<p>Ezekiel — <strong>${#ENTRIES[@]} posts</strong> are live; packets below.</p>"
  else
    echo "<p>Ezekiel —</p>"
  fi
} > "$TMP_HTML"

declare -a SENT_SLUGS=(); SUBJECT_BITS=""
first=1
for entry in "${ENTRIES[@]}"; do
  slug=$(printf '%s' "$entry" | jq -r '.slug')
  title=$(printf '%s' "$entry" | jq -r '.title')
  log "Building packet for $slug ..."
  payload=$(build_payload "$entry") || { log "  build_payload failed for $slug — skipping"; continue; }
  frag=$(printf '%s' "$payload" | node "$HTML_GEN" --fragment) || { log "  html gen failed for $slug"; continue; }
  [ "$first" -eq 0 ] && echo '<hr style="border:0;border-top:3px double #d0d7de;margin:28px 0">' >> "$TMP_HTML"
  printf '%s\n' "$frag" >> "$TMP_HTML"
  first=0
  SENT_SLUGS+=("$slug")
  SUBJECT_BITS="${SUBJECT_BITS:+$SUBJECT_BITS · }$title"
done
echo '</div>' >> "$TMP_HTML"

if [ "${#SENT_SLUGS[@]}" -eq 0 ]; then
  log "No packets built successfully."
  rm -f "$TMP_HTML"; exit 1
fi

# Lead with an emoji so the packet is instantly recognizable in Ezekiel's inbox
# ("📣 = my posting packet") — a consistent marker, not a per-day siren.
SUBJECT="📣 POST THIS — X + LinkedIn"
[ "${#SENT_SLUGS[@]}" -gt 1 ] && SUBJECT="📣 POST THESE — ${#SENT_SLUGS[@]} articles"
SUBJECT="$SUBJECT — $(printf '%s' "$SUBJECT_BITS" | cut -c1-80)"

if send_packet "$TMP_HTML" "$SUBJECT"; then
  log "Packet emailed to $EZEKIEL_EMAIL (${#SENT_SLUGS[@]} post(s))"
  if [ "$DRY_RUN" -eq 0 ]; then
    for slug in "${SENT_SLUGS[@]}"; do mark_sent "$slug" && log "  marked packet_sent for $slug"; done
  fi
else
  log "ERROR: packet email failed — packet_sent NOT marked (will retry next sweep)"
  rm -f "$TMP_HTML"; exit 1
fi

if [ "$DRY_RUN" -eq 1 ]; then log "DRY-RUN html preserved at $TMP_HTML"; else rm -f "$TMP_HTML"; fi
log "=== posting-packet end (${#SENT_SLUGS[@]} packet(s)) ==="
