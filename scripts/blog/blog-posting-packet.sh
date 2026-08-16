#!/usr/bin/env bash
# blog-posting-packet.sh — build + email the per-post social "posting packet" to
# Ezekiel (WS2). Replaces blog-social-email.sh.
#
# WHAT IT DOES
#   For each published post that has not yet had a packet sent (tracked by
#   packet_sent in .blog-syndication-ledger.json), it:
#     1. generates the three voice pieces via a bounded `claude -p` — X (raw,
#        punchy), LinkedIn personal (Jeremy, first person), LinkedIn company
#        (Intent Solutions) — plus the title and subtitle for the long-form X
#        article, following references/social-bundle.md. The MODEL writes only
#        the persuasive copy; it never writes the links.
#     2. DETERMINISTICALLY appends the UTM-tagged deep-dive link + GitHub "Code:"
#        links (UTM is the measurement keystone — it must not depend on the model
#        getting a query string right; utm_source = x|linkedin|substack|medium,
#        with utm_content separating the two X and the two LinkedIn surfaces).
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
# The persona authority. voice-system-prompt.md is the canonical master voice and
# voices.md names the facets each surface writes in. Both lived in intent-os being
# cited as paths and never actually read, so the packet was generating copy from
# social-bundle.md alone. These are inlined into the voice prompt now.
PERSONA_DIR="/home/jeremy/000-projects/intent-os/persona"
VOICE_MASTER="$PERSONA_DIR/voice-system-prompt.md"
VOICE_FACETS="$PERSONA_DIR/voices.md"
# The MEASURED fingerprint (persona rung 3, 2026-08-12). Until this existed the
# packet was fitted to a prose description of a voice: voices.md declared five
# facets, two of which were the generic agents content-marketer and
# docs-architect renamed. This file is fitted to 1,430 human-authored turns
# pulled from the Claude Code transcripts, and it separates real Jeremy from our
# own AI blog prose at AUC 0.965. Method + limits: persona/fingerprint-report.md.
VOICE_FINGERPRINT="$PERSONA_DIR/voice-fingerprint.json"
# In-repo enforcement (single source of truth for the banned-phrase list).
VOICE_LINT="$BLOG_DIR/.claude/skills/blog-backfill/scripts/lint-post-voice.py"
VOICE_DENYLIST="$BLOG_DIR/.claude/skills/blog-backfill/scripts/voice-denylist.json"
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

# Shared Intent runtime: a per-run heartbeat for the daily
# liveness sweep + a plain-English #cron-failures alert on any abnormal exit.
# Guarded so a fresh clone without the lib still runs. This is what stops the
# Ezekiel packet from failing SILENTLY — a broken send now pages instead of
# vanishing (the 2026-07-08 "the email never fired" lesson).
if [ -f "$HOME/bin/lib/intent-runtime.sh" ]; then
  # shellcheck disable=SC1091
  source "$HOME/bin/lib/intent-runtime.sh"
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
# Raised from 300s when the Vibe craft skills were wired in (2026-08-09): the run
# now loads two skills before writing, which costs real seconds. Measured at ~100s
# with the skills against ~45s without, so 480 keeps a wide margin. A timeout here
# is not fatal (the packet degrades loudly), but a degraded packet is a bad day for
# Ezekiel, so buy the headroom.
VOICE_TIMEOUT="${PACKET_VOICE_TIMEOUT:-480}"
# Pinned so the packet's register does not drift when the CLI default model moves.
VOICE_MODEL="${PACKET_VOICE_MODEL:-claude-sonnet-5}"
# Where generate_voice leaves the human-readable REASON it failed.
#
# It needs a file rather than a variable because generate_voice is called inside
# $(...), so anything it assigns dies with the subshell. Without this channel the
# caller knows only that voice-gen failed, which is exactly how a three-day auth
# outage (2026-08-14..16) reached Ezekiel as three silent placeholder packets: the
# CLI printed "Not logged in - Please run /login" as ASSISTANT TEXT ON STDOUT with
# exit 0, the script captured only stderr, and the raw stdout was discarded on the
# failure path. Nothing anywhere named the cause. Now the cause lands in the log AND
# in the packet itself, so the next break announces itself.
VOICE_FAIL_FILE="${TMPDIR:-/tmp}/blog-packet-voice-fail.$$"
# The Vibe marketing pack, installed globally 2026-08-09. Supplies PLATFORM CRAFT
# to the syndication copy (never voice, never punctuation). PACKET_USE_CRAFT_SKILLS=0
# falls back to the persona-only prompt.
CRAFT_SKILL_DIR="/home/jeremy/.claude/skills"

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
utm() { # <bare_url> <source> [content]
  # utm_source alone was NOT enough. Both LinkedIn surfaces (Jeremy's personal
  # profile and the Intent Solutions company page) resolve to utm_source=linkedin,
  # so the two links were byte-identical and Umami could not tell which surface
  # sent the traffic. The optional third arg adds utm_content (li_personal |
  # li_company), which is the only thing that separates them. Callers already
  # passed it; the function silently dropped it until 2026-08-09.
  #
  # Keep the tail as short as it can be and still attribute: source always,
  # content only when the caller distinguishes two surfaces on one source.
  local url="$1" src="$2" content="${3:-}"
  local sep="?"; [[ "$url" == *"?"* ]] && sep="&"
  local q="utm_source=${src}"
  [ -n "$content" ] && q="${q}&utm_content=${content}"
  printf '%s%s' "$url$sep" "$q"
}

# Lint one blob of model-authored copy through the SAME deny-list the article
# prose is held to. Echoes the linter's issue lines on fd1; returns non-zero on
# any violation. Without this the packet was the one unlinted surface in the
# whole pipeline: the article could not ship with an em dash, but the LinkedIn
# post quoting it could, and did.

# The runaway-sentence threshold, read from the measured composed band rather
# than picked. It is the p90 of his composed-band sentence length, so copy only
# trips it when over HALF its sentences are longer than 90% of anything he has
# written. Empty (guard off) if the fingerprint is missing, because a missing
# profile must not start rejecting copy.
#
# This exists because three rounds of prompt wording failed to hold the line: the
# same field came back at a 27-word median, then 20, then 35. Prose instructions
# do not converge, a gate does. It is deliberately NOT a "write short" rule;
# sentence length does not distinguish his writing from AI writing at all.
MAX_MEDIAN_SENTENCE=""
if [ -f "$VOICE_FINGERPRINT" ]; then
  MAX_MEDIAN_SENTENCE=$(jq -r '.bands.composed.sentence_words.p90 // empty' \
    "$VOICE_FINGERPRINT" 2>/dev/null | cut -d. -f1)
fi

lint_copy() { # <label> <text>
  local label="$1" text="$2"
  [ -f "$VOICE_LINT" ] || return 0   # linter absent: do not brick the packet
  # :- guard on purpose. lint_copy is sourced standalone by the test harness and
  # runs under `set -u`, and more importantly a linter must never be the thing
  # that brings the packet down. Unset threshold means guard off, not crash.
  local extra=()
  [ -n "${MAX_MEDIAN_SENTENCE:-}" ] && extra=(--max-median-sentence "$MAX_MEDIAN_SENTENCE")
  # Deliberate: the linter reports issues on STDERR and status lines on stdout, so
  # discard its stdout and hand its stderr back to the caller as this function's
  # stdout. Written as a block so the intent is unambiguous.
  { printf '%s' "$text" | python3 "$VOICE_LINT" --stdin --label "$label" \
      "${extra[@]}" >/dev/null; } 2>&1
}

# Lint every model-authored field of a voice JSON blob. Echoes the issue lines
# (each prefixed "<field>:") on fd1 and returns non-zero if ANY field failed.
lint_voice_fields() { # <voice_json>
  local voice="$1" field val issues rc=0
  for field in x_post li_personal li_company substack_subtitle \
               x_article_title x_article_subtitle bmc_note; do
    val=$(printf '%s' "$voice" | jq -r --arg f "$field" '.[$f] // ""')
    [ -z "$val" ] && continue
    if ! issues=$(lint_copy "$field" "$val"); then
      rc=1
      printf '%s\n' "$issues" | sed '/^ *$/d; s/^ *//'
    fi
  done
  return "$rc"
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
#
# FAIL-CLOSED. A missing or unreadable library used to `return 0`, which reads as
# "no governed entity matched" and lets a post about a governed partner go out with
# no disclaimer at all. The library not being there is not evidence that the post is
# clean; it is evidence that we cannot tell. That is a HOLD, not an all-clear.
select_disclaimers() { # <body_file>
  local body_file="$1" body ent match n
  if [ ! -f "$DISCLAIMER_LIB" ]; then
    echo "HOLD:disclaimer-library-unavailable"
    return 1
  fi
  if ! jq -e '.entities' "$DISCLAIMER_LIB" >/dev/null 2>&1; then
    echo "HOLD:disclaimer-library-unreadable"
    return 1
  fi
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
  # Clear last call's reason so a stale one can never be attributed to this post.
  : > "$VOICE_FAIL_FILE" 2>/dev/null || true
  body=$(post_body "$post_file" | head -400)
  local spec=""
  [ -f "$VOICE_SPEC" ] && spec=$(cat "$VOICE_SPEC")
  # Test hook: skip the LLM entirely when PACKET_VOICE_STUB=1 (structural testing).
  if [ "${PACKET_VOICE_STUB:-0}" = "1" ]; then
    printf '{"x_post":"STUB x copy, punchy raw voice.","x_is_thread":false,"li_personal":"STUB LinkedIn personal copy in Jeremy first person.","li_company":"STUB Intent Solutions company copy, third person.","substack_subtitle":"STUB subtitle.","x_article_title":"STUB X article title.","x_article_subtitle":"STUB X article subtitle.","bmc_note":"STUB supporter note."}'
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
  # The persona authority, inlined. voice-system-prompt.md is the canonical master
  # voice; voices.md names the facets and their dial settings. Both were cited by
  # path in social-bundle.md and never read, so every packet was written from the
  # surface spec with no master voice underneath it.
  local master="" facets=""
  [ -f "$VOICE_MASTER" ] && master=$(cat "$VOICE_MASTER")
  [ -f "$VOICE_FACETS" ] && facets=$(cat "$VOICE_FACETS")
  # The measured fingerprint, rendered as targets rather than pasted as raw JSON.
  #
  # This block deliberately does NOT hand the model a sentence-length target, and
  # that is a correction of a real defect rather than an omission. The corpus is
  # 90% one-line commands, so its blended median (9 words) describes the command
  # band and nothing else; an earlier version of this wiring shipped that median
  # as a universal target and pushed LinkedIn copy toward a register Jeremy only
  # uses when barking at an agent. Measured against our own posts, length turns
  # out to carry no signal at all: our AI prose runs p50 11 words per sentence
  # and his composed writing runs p50 10. The AI is not the one writing long.
  #
  # What DOES separate him, in the composed band as well as the command band, is
  # the habit cluster: lowercase sentence starts, absent terminal punctuation,
  # comma sparsity, zero dashes. Those are the AUC 0.965 signals, so those are
  # what the prompt carries.
  local fingerprint=""
  if [ -f "$VOICE_FINGERPRINT" ]; then
    fingerprint=$(jq -r '
      "Fitted to \(.provenance.corpus_turns) human-authored turns (\(.provenance.date_range[0]) to \(.provenance.date_range[1])).",
      "It separates real Jeremy from our own AI-written blog prose at AUC \(.provenance.discrimination.auc).",
      "",
      "DO NOT TARGET A SENTENCE LENGTH. This is measured, not a style preference:",
      "  \(.what_actually_discriminates.sentence_length_does_not_discriminate)",
      "Writing short does not make copy sound like him. It makes it sound clipped.",
      "",
      "WHAT ACTUALLY SEPARATES HIM FROM AI PROSE. These are the signals the AUC",
      "\(.provenance.discrimination.auc) test runs on, so these are what to hit:",
      (.what_actually_discriminates.signals_used_by_the_auc_test[] | "  - \(.)"),
      "",
      "He keeps those habits even when composing, which is the surprising part and",
      "the part worth using. In the composed band (\(.bands.composed.turns) turns, \(.bands.composed.definition)):",
      "  - starts a sentence lowercase \(.bands.composed.habits.lowercase_start_rate) of the time",
      "  - ends with terminal punctuation only \(.bands.composed.habits.terminal_punctuation_rate) of the time",
      "  - uses a comma in \(.bands.composed.habits.comma_rate) of turns",
      "  - sentence words p50 \(.bands.composed.sentence_words.p50), p75 \(.bands.composed.sentence_words.p75), p90 \(.bands.composed.sentence_words.p90). Reference only, NOT a target.",
      "Let that pull the copy toward plain and unfussy. Do not mechanically lowercase",
      "everything: brand copy on the company surface can capitalize normally.",
      "",
      "DICTATION NOISE (typo rate \(.dictation_noise_do_not_reproduce.typo_rate)). NEVER REPRODUCE:",
      "  \(.dictation_noise_do_not_reproduce.note)",
      "",
      "NOT DERIVABLE from this corpus, do not pretend otherwise:",
      (.not_derivable_from_this_corpus[] | "  - \(.)")
    ' "$VOICE_FINGERPRINT" 2>/dev/null) || fingerprint=""
  fi
  if [ -n "$fingerprint" ]; then
    fingerprint=$(printf '\n=== MEASURED VOICE FINGERPRINT (persona/voice-fingerprint.json) ===\n%s\n=== END FINGERPRINT ===\n' "$fingerprint")
  fi
  # The banned-phrase list, injected from the single source of truth. This prompt
  # used to restate a hand-picked 7-item subset, which drifted from the 26-entry
  # deny-list the linter actually enforces. The model was being told one rule and
  # graded against another.
  local denylist=""
  if [ -f "$VOICE_DENYLIST" ]; then
    denylist=$(jq -r '.slop_phrases[].label' "$VOICE_DENYLIST" 2>/dev/null | sed 's/^/  - /')
  fi
  # Platform craft comes from the Vibe marketing skills; VOICE still comes from
  # persona. That division is the whole point: content-atomizer knows LinkedIn
  # truncates at the "see more" fold and what an X post has to do in its first
  # line, which persona has no opinion about. Persona knows what that hook sounds
  # like in Jeremy's voice, which the skill has no opinion about. Neither one
  # replaces the other, and the skill NEVER supplies register or punctuation:
  # its own reference prose carries hundreds of em dashes, which our linter bans.
  local craft_block=""
  if [ "${PACKET_USE_CRAFT_SKILLS:-1}" = "1" ] && [ -d "$CRAFT_SKILL_DIR/content-atomizer" ]; then
    craft_block=$(cat <<'CRAFT'

=== PLATFORM CRAFT (do this FIRST) ===
Before writing anything, invoke the "content-atomizer" skill with the Skill tool and
read its platform guidance for X/Twitter and LinkedIn. Then invoke
"direct-response-copy" and use its hook guidance to sharpen your opening lines.

Use those skills for PLATFORM MECHANICS ONLY:
  - what each platform's format rewards (line length, the LinkedIn "see more" fold,
    what an opening line has to accomplish, whitespace and scannability)
  - hook construction and specificity
  - what suppresses reach on each surface

Do NOT take from those skills:
  - voice, register, or personality (that is persona, above, and it wins)
  - punctuation style (our dash ban below wins, absolutely and without exception,
    and those skills' own prose violates it constantly)
  - any phrasing lifted from their examples (write our words about our work)
  - marketing claims the article does not support

Work only from what the skills already contain. Do NOT run web searches, and do not
fetch anything: this call is time-bounded and offline.
=== END PLATFORM CRAFT ===
CRAFT
)
  fi
  prompt=$(cat <<PROMPT
You are writing SYNDICATION copy for a blog post that is already published and live.
${craft_block}

This is the marketing register. It is NOT the register the article itself is written
in. The article is a work journal: what got built, what broke, what it cost. The
syndication copy below is allowed to persuade someone to go read it. Do not carry the
persuasive register back into how you characterize the work, and never claim more than
the article does.

=== CANONICAL MASTER VOICE (persona/voice-system-prompt.md) ===
${master}
=== END MASTER VOICE ===

=== NAMED VOICE FACETS (persona/voices.md) ===
${facets}
=== END FACETS ===
${fingerprint}
=== SURFACE VOICE SPEC (social-bundle.md) ===
${spec}
=== END SPEC ===

POST TITLE: ${title}
TIER: ${tier}

POST BODY (context — do not copy verbatim):
${body}

Produce copy for three DISTINCT voices, plus the framing for one long-form repost. Each
maps to a NAMED FACET from the selector in the facets doc above. Use that facet's dial
settings, do not invent a facet that is not in the selector:

  x_post      -> the Raw facet     (snark 4, depth 2, operator lens light, first person)
                 MEASURED. Raw is the one facet fitted to real data, and the corpus
                 IS this register. Lean hardest here on the habit cluster above:
                 lowercase starts, sparse terminal punctuation, few commas, plain
                 words. Note that "snark 4" is NOT measured (only 8 reactive turns
                 survived filtering), so treat it as a soft guess, not a target.
  li_personal -> the Personal facet (snark 2, depth 3, operator lens on, first person)
                 DECLARED register, no corpus behind the STANCE. Do not compensate
                 by writing short: his composed writing is not short, and clipped
                 LinkedIn copy reads as a different kind of fake.
                 The closest measured thing is the "deciding" register: when Jeremy
                 actually reasons out loud he does not lead with a hook, he states
                 the situation and works through it in complete sentences (fragment
                 rate 0.07 against a 0.24 baseline). Let that pull this surface
                 toward substance and away from a pitch.
  li_company  -> the House facet   (snark 1, depth 3, operator lens as company DNA,
                                    Intent Solutions brand third person)
                 DECLARED and undecidable REGISTER. Jeremy has never written as the
                 company in any corpus, so the stance is convention, not evidence.
                 This is the one surface where the measured lowercase habit should
                 NOT be copied: a company post capitalizes normally. What still
                 carries over is the plainness and the dash ban. Declared speaker,
                 measured plainness.
  x_article_title / x_article_subtitle
              -> the Field facet   (snark 2, depth 3, operator lens on, first person)
                 NOT Raw. The tweet is a hook someone scrolls past; the article is a
                 page someone opened on purpose, and they arrived for the substance.
  bmc_note    -> the Personal facet (snark 2, depth 3, operator lens on, first person)
                 The warmest room on the list. These are people who already chose to
                 support the work, so this is one or two sentences TO them, not an
                 advertisement AT them. Say why this particular piece was worth the
                 week. No pitch, no thanks-for-subscribing boilerplate, no ask.

PRECEDENCE, when any two of these disagree (highest wins):
  1. The hard rules below (dash ban, deny-list, no links, JSON shape)
  2. The MEASURED fingerprint above, where it applies (sentence shape)
  3. The persona voice and facet dials above
  4. Platform craft from the skills
Measured beats declared, but only inside what was actually measured. Where the
fingerprint gives a habit rate and a facet gives an adjective, the habit wins.
Where the fingerprint says "not derivable" or "reference only" (post-level length,
sentence length, brand register), fall through to craft and the facet dials. Never
promote a reference-only number into a target.
A craft skill suggesting a punchier line that trips rule 1 is WRONG here. Rewrite it
in our voice, inside our punctuation rules. Never the other way around.

Hard rules:
- Write ONLY the persuasive copy. Do NOT include any URLs, "Deep-dive:", "Code:",
  "Read:", or hash(link) lines — those are appended automatically. (Hashtags are fine.)
- X, li_personal, and li_company must EACH open with a DISTINCT first sentence — no
  two may share an opener, and none may reuse a recent opener listed below.
- HARD BAN: em dash (U+2014) and en dash (U+2013), anywhere in any field, including
  HTML entities. Use a period, comma, colon, or parentheses. This is checked by a
  linter after you write; a violation costs a regeneration.
- NEVER reproduce the dictation typos. The corpus this voice was fitted to carries a
  13.7% typo rate because most of it was voice-dictated on the move. Lowercase starts
  and fragments are VOICE and belong in the copy. Misspellings are transcription
  NOISE and do not. Write his shape in correct spelling.
- BANNED PHRASES (the canonical deny-list, enforced by the same linter that gates the
  article prose). Do not use any of these, in any field:
${denylist}
- x_post: ${thread_hint}
- li_personal: VARY THE ENTRY POINT every time — lead with a specific detail from THIS
  post, a question, a number, or a claim. Jeremy's operator background is available as
  an OCCASIONAL angle, but do NOT open with it by default; most posts should open on
  the technical substance, not the backstory. End with a line like "Deep-dive + code in
  the comments." (no actual link).
- li_company: the House facet. Brand third person ("Intent Solutions built…", "the team
  found…"), measured and professional, still blunt and concrete, with the same honesty
  about tradeoffs that earns trust in the first-person facets. Distinctly different
  opening from li_personal.
- substack_subtitle: one line. The editorial hook that makes someone open the long-form.
- x_article_title / x_article_subtitle: the framing for reposting the WHOLE article as a
  long-form X article. The body is the published article verbatim, so you write only these
  two. The title may differ from the blog title (X readers are a different room) but must
  describe the same piece honestly. The subtitle is one line, the Field facet, and says
  what the reader gets. Do not write a hook that promises more than the article delivers.
${avoid_block}

- bmc_note: one or two sentences for the Buy Me a Coffee supporters feed, which
  reposts the whole article. Written TO people who already back the work. Say what
  this piece cost or what it changed, in plain terms. Never thank them for
  supporting, never ask for anything, never mention coffee.

Output ONLY a single minified JSON object, no markdown fences, with keys:
x_post, x_is_thread (boolean), li_personal, li_company, substack_subtitle,
x_article_title, x_article_subtitle, bmc_note
PROMPT
)
  # Model is PINNED so packet copy does not silently change register when the CLI
  # default moves. --dangerously-skip-permissions is gone; instead the tool set is
  # ALLOWLISTED, which is both safer and more predictable in cron:
  #   Skill  - load content-atomizer / direct-response-copy
  #   Read/Glob/Grep - read those skills' reference files
  # Everything else is denied, which matters because content-atomizer's own
  # description says it web-searches for algorithm changes before generating. On a
  # cron path a network call is latency we cannot afford and an approval prompt we
  # can never answer, so it is denied at the harness rather than merely discouraged
  # in the prompt.
  local -a claude_args=(-p "$prompt" --model "$VOICE_MODEL")
  if [ "${PACKET_USE_CRAFT_SKILLS:-1}" = "1" ]; then
    claude_args+=(--allowedTools "Skill" "Read" "Glob" "Grep")
  fi
  local rc=0
  raw=$(timeout "$VOICE_TIMEOUT" claude "${claude_args[@]}" 2>>"$LOG") || rc=$?
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

  # FAILURE PATH. Say WHY, in the log and in the reason channel, and keep enough of
  # the raw output to identify a cause we have not seen before. Everything here is
  # diagnosis of a run that already failed; it never changes what gets published.
  local reason
  if [ "$rc" -eq 124 ]; then
    reason="timed out after ${VOICE_TIMEOUT}s"
  elif printf '%s' "$raw" | grep -qiE 'not logged in|run /login|OAuth session expired|could not be refreshed|Failed to authenticate|Invalid API key|authentication_error'; then
    # The recurring one. Named explicitly because the fix (re-auth the headless CLI)
    # is nothing like the fix for any other failure here, and because this exact
    # string is what three days of degraded packets looked like from the inside.
    reason="NOT AUTHENTICATED - the headless CLI has no valid session, run 'claude setup-token'"
  elif [ -z "$raw" ]; then
    reason="empty stdout (claude exit $rc) - see the stderr lines above in this log"
  elif [ "$rc" -ne 0 ]; then
    reason="claude exited $rc without valid JSON"
  else
    reason="claude exited 0 but produced no JSON object"
  fi
  printf '%s' "$reason" > "$VOICE_FAIL_FILE" 2>/dev/null || true

  log "  voice-gen FAILED: $reason"
  log "    claude exit=$rc, stdout bytes=$(printf '%s' "$raw" | wc -c)"
  if [ -n "$raw" ]; then
    # Flattened and byte-capped: this is a log line, not a transcript. The raw text
    # has already been through the iconv/U+FFFD sanitizer above, so it is safe to
    # print. 500 bytes is enough to read an error banner and far short of dumping
    # a full model response into the log every time a lint-adjacent failure lands.
    log "    raw stdout (first 500 bytes): $(printf '%s' "$raw" | tr '\n\t' '  ' | head -c 500)"
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

  # Destinations by tier. The tweet is unconditional; the long-form REPOSTS
  # (Substack, Medium, and the X article) only earn their place on a post with
  # enough body to be worth reading somewhere else.
  #
  # Buy Me a Coffee is deliberately NOT in that group, and used to be. The tier
  # gate exists to ration PUBLIC syndication reach: do not push a thin field note
  # at Medium. The supporters' feed is the opposite situation. Those are people
  # who already chose to fund the work, and gating them by tier meant the readers
  # paying for it saw the least of it: every Tier 1 day, they got nothing while
  # the public surfaces got the post. Found 2026-08-13 when a Tier 1 post shipped
  # with the supporters' section silently absent from the packet.
  #
  # This is about to matter much more than the ledger suggests. The ledger is
  # 31 Tier 2 against 5 Tier 1 today, but the tier bands the creep guard enforces
  # are 60-70% Tier 1, so correcting the inflation would have hidden MOST posts
  # from supporters.
  local -a dests=("x" "li_personal" "li_company" "buymeacoffee")
  [ "$tier" -ge 2 ] && dests+=("substack" "medium" "x_article")
  local dests_json; dests_json=$(printf '%s\n' "${dests[@]}" | jq -R . | jq -sc .)

  # Disclaimers (fail-closed).
  local body_tmp; body_tmp=$(mktemp); post_body "$post_file" > "$body_tmp"
  local notes hold=0 hold_reason=""
  notes=$(select_disclaimers "$body_tmp")
  local -a note_arr=()
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    if [[ "$line" == HOLD:* ]]; then
      hold=1
      case "${line#HOLD:}" in
        disclaimer-library-unavailable)
          hold_reason="The approved disclaimer library is missing at $DISCLAIMER_LIB, so we cannot tell whether this post needs a governed disclaimer. Restore the library and re-run before posting." ;;
        disclaimer-library-unreadable)
          hold_reason="The approved disclaimer library at $DISCLAIMER_LIB is present but has no readable .entities map. Fix the JSON and re-run before posting." ;;
        *)
          hold_reason="Post mentions a governed entity ('${line#HOLD:}') with no Jeremy-approved disclaimer. Approve wording in disclaimer-library.json before posting." ;;
      esac
    else note_arr+=("$line"); fi
  done <<< "$notes"
  rm -f "$body_tmp"
  local notes_json; notes_json=$(printf '%s\n' "${note_arr[@]:-}" | jq -R . | jq -sc '[.[] | select(length>0)]')

  # UTM links. utm_content is what separates the two LinkedIn surfaces, which
  # otherwise collapse to the same utm_source=linkedin link. The names match the
  # payload field names (li_personal / li_company) so a row in the Umami utm_content
  # breakdown maps straight back to a box in this packet.
  # X now has two surfaces for the same reason LinkedIn does: the tweet and the long-form
  # article both resolve to utm_source=x, so without utm_content they would collapse into
  # one row and neither could be attributed. The tweet stays bare and the article carries
  # utm_content=x_article, which is the only thing separating them.
  local link_x link_x_article link_bmc link_li_p link_li_c
  link_x=$(utm "$canonical" "x")
  link_x_article=$(utm "$canonical" "x" "x_article")
  link_bmc=$(utm "$canonical" "buymeacoffee")
  link_li_p=$(utm "$canonical" "linkedin" "li_personal")
  link_li_c=$(utm "$canonical" "linkedin" "li_company")

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

  # Voice content, gated by the same voice linter the article prose runs through.
  # Generate, lint, regenerate ONCE on a violation, then degrade loudly. The copy is
  # never silently shipped dirty and never silently dropped: a field that cannot pass
  # the lint is replaced by a visible placeholder naming what failed, so Ezekiel sees
  # a box he must write himself instead of a box with an em dash in it.
  local voice="" lint_report="" attempt
  for attempt in 1 2; do
    if ! voice=$(generate_voice "$post_file" "$title" "$tier"); then
      voice=""; break
    fi
    if lint_report=$(lint_voice_fields "$voice"); then
      lint_report=""; break
    fi
    log "  voice lint FAILED for $slug (attempt $attempt):"
    while IFS= read -r l; do [ -n "$l" ] && log "    $l"; done <<< "$lint_report"
    [ "$attempt" -eq 2 ] && break
    log "  regenerating voice copy once"
  done

  local x_post x_thread li_p li_c subtitle xa_title xa_subtitle bmc_note
  if [ -n "$voice" ]; then
    x_post=$(printf '%s' "$voice" | jq -r '.x_post // ""')
    x_thread=false   # never a thread — single tweet always (extended char limit)
    li_p=$(printf '%s' "$voice" | jq -r '.li_personal // ""')
    li_c=$(printf '%s' "$voice" | jq -r '.li_company // ""')
    subtitle=$(printf '%s' "$voice" | jq -r '.substack_subtitle // ""')
    xa_title=$(printf '%s' "$voice" | jq -r '.x_article_title // ""')
    xa_subtitle=$(printf '%s' "$voice" | jq -r '.x_article_subtitle // ""')
    bmc_note=$(printf '%s' "$voice" | jq -r '.bmc_note // ""')

    # Degrade the specific fields that still fail, leave the clean ones alone.
    if [ -n "$lint_report" ]; then
      local bad bad_list
      bad_list=$(printf '%s\n' "$lint_report" | sed -n 's/^\([a-z_]*\):.*/\1/p' | sort -u)
      while IFS= read -r bad; do
        [ -z "$bad" ] && continue
        case "$bad" in
          x_post)     x_post="[voice lint failed twice on this field. Write the X post manually from the article.]" ;;
          li_personal) li_p="[voice lint failed twice on this field. Write the LinkedIn personal post manually from the article.]" ;;
          li_company)  li_c="[voice lint failed twice on this field. Write the LinkedIn company post manually from the article.]" ;;
          substack_subtitle) subtitle="" ;;
          # Emptied rather than replaced with a placeholder string: the renderer keys the
          # X-article degraded box on a missing title, so "" is what makes the loud box
          # appear. A placeholder here would render as if it were the title.
          x_article_title) xa_title="" ;;
          x_article_subtitle) xa_subtitle="" ;;
          bmc_note) bmc_note="" ;;
        esac
      done <<< "$bad_list"
      note_arr+=("⚠ Voice lint failed twice on: $(printf '%s' "$bad_list" | tr '\n' ' '). Those boxes are placeholders, not copy. Offending output is in $LOG.")
      notes_json=$(printf '%s\n' "${note_arr[@]:-}" | jq -R . | jq -sc '[.[] | select(length>0)]')
    fi
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
    # The reason generate_voice recorded, if it got far enough to record one. This
    # rides into the packet note as well as the log, because the person who needs to
    # act on "NOT AUTHENTICATED" is on the CC line of the email, not reading the log.
    local fail_reason=""
    [ -s "$VOICE_FAIL_FILE" ] && fail_reason=$(cat "$VOICE_FAIL_FILE" 2>/dev/null)
    log "  WARN: voice-gen failed for $slug — degraded packet${fail_reason:+ ($fail_reason)}"
    x_post="[voice copy failed to generate — write the X post manually]"
    x_thread=false
    li_p="[write the LinkedIn personal post manually]"
    li_c="[write the LinkedIn company post manually]"
    subtitle=""
    xa_title=""
    xa_subtitle=""
    bmc_note=""
    note_arr+=("⚠ Automated copy generation failed for this post — the X/LinkedIn boxes are placeholders. Write the copy from the article, or ping Jeremy.${fail_reason:+ Cause: $fail_reason}")
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

  # Image attachments. make-post-image.py writes this block into the ledger entry
  # (generated art when the provider answered, the deterministic card either way).
  # Ezekiel posts image plus text, so the packet has to name the files; without
  # this the packet was text-only and every post went out bare.
  local image_json; image_json=$(printf '%s' "$entry" | jq -c '.image // null')
  local img_abs card_og card_sq
  img_abs=$(printf '%s' "$image_json" | jq -r '.image // ""')
  card_og=$(printf '%s' "$image_json" | jq -r '.cards.og // ""')
  card_sq=$(printf '%s' "$image_json" | jq -r '.cards.square // ""')
  # Ezekiel is REMOTE. A path on this box is useless to him, so anything under
  # static/ becomes the public URL Hugo serves it at. Only a file outside static/
  # (which should not happen on the land path) falls back to a local path, and
  # then at least Jeremy can find it.
  to_url() { # <repo-relative-or-absolute path>
    local p="$1"
    [ -z "$p" ] && { printf ''; return; }
    case "$p" in
      static/*) printf 'https://startaitools.com/%s' "${p#static/}" ;;
      /*)       printf '%s' "$p" ;;
      *)        printf '%s/%s' "$BLOG_DIR" "$p" ;;
    esac
  }
  img_abs=$(to_url "$img_abs")
  card_og=$(to_url "$card_og")
  card_sq=$(to_url "$card_sq")
  local media_json
  media_json=$(jq -n --arg i "$img_abs" --arg og "$card_og" --arg sq "$card_sq" \
    --argjson fb "$(printf '%s' "$image_json" | jq '.fallback // false')" \
    '{generated:(if $i=="" then null else $i end),
      card_og:(if $og=="" then null else $og end),
      card_square:(if $sq=="" then null else $sq end),
      generated_failed:$fb}')
  if [ -z "$img_abs" ] && [ -z "$card_og" ]; then
    note_arr+=("⚠ No image was produced for this post. Post the text on its own, or ask Jeremy for a graphic.")
    notes_json=$(printf '%s\n' "${note_arr[@]:-}" | jq -R . | jq -sc '[.[] | select(length>0)]')
  fi

  jq -n \
    --arg title "$title" --arg canonical "$canonical" --argjson tier "$tier" \
    --argjson dests "$dests_json" --argjson notes "$notes_json" \
    --arg lx "$link_x" --arg lxa "$link_x_article" \
    --arg lsc "$canonical" --arg lmc "$canonical" \
    --arg xp "$x_final" --argjson xt "$x_thread" \
    --arg lip "$li_p" --arg lipc "$li_p_comment" \
    --arg lic "$li_c" --arg licc "$li_c_comment" \
    --arg sub "$subtitle" --arg footer "$footer" \
    --arg xat "$xa_title" --arg xas "$xa_subtitle" --arg bmn "$bmc_note" \
    --arg lbmc "$link_bmc" \
    --argjson media "$media_json" \
    --argjson hold "$hold" --arg hr "$hold_reason" '
    {post_title:$title, canonical_url:$canonical, tier:$tier, destinations:$dests,
     before_notes:$notes, media:$media,
     links:{x:$lx, x_article:$lxa, buymeacoffee:$lbmc,
            substack_canonical:$lsc, medium_canonical:$lmc},
     x_post:$xp, x_is_thread:$xt,
     li_personal:$lip, li_personal_comment:$lipc,
     li_company:$lic, li_company_comment:$licc,
     substack_subtitle:$sub, footer:$footer,
     x_article_title:$xat, x_article_subtitle:$xas, bmc_note:$bmn,
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
    # A no-packet morning is a valid no-op, but SILENCE reads as failure
    # (incident 2026-07-17: no way to tell a quiet morning from a broken pipeline
    # — the ntfy NO-PACKET heartbeat was retired 2026-06-13 and never replaced).
    # Send a short POSITIVE heartbeat so every morning produces a visible signal.
    # The liveness beat + daily sweep still cover the "cron stopped firing" case.
    log "No unpacketed posts — nothing to send; sending positive heartbeat email."
    _latest=$(jq -r 'sort_by(.date) | last | "\(.date)  \(.slug)"' "$LEDGER_FILE" 2>/dev/null)
    if node "$EMAIL_SCRIPT" --to jeremy@intentsolutions.io \
      --subject "✓ Blog pipeline healthy — nothing new to syndicate ($(date +%Y-%m-%d))" \
      --body "$(printf 'The blog syndication sweep ran clean and found nothing new to send Ezekiel. This is a normal quiet day, NOT a failure.\n\nWhy no Ezekiel packet: every post in the syndication ledger is already marked packet_sent. A fresh packet goes out the morning after a NEW post lands.\n\nMost recent post in the ledger:\n  %s\n\nIf you expected a new post: the daily backfill produces the PRIOR day post; if that day already had one, it no-ops. See ~/.local/state/blog-backfill-daily/ for todays run.\n' "${_latest:-unknown}")" \
      >/dev/null 2>&1; then
      log "heartbeat email sent to jeremy@intentsolutions.io"
    else
      log "WARN: heartbeat email failed"
    fi
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
