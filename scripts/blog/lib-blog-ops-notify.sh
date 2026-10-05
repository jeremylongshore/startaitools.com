# lib-blog-ops-notify.sh: the owner's status digest in the Buzz `blog-ops` channel.
#
# Sourced by blog-backfill-daily.sh, blog-posting-packet.sh, blog-team-rollup.sh and
# blog-recommendation-worker.sh. Defines functions only; nothing runs at source time.
#
# WHY: the owner asked to hear about the blog in Buzz, not only by email. Failures
# already page through cron_fail -> sys-automation and the emails stay exactly as
# they are. This adds ONE short status card per run to `blog-ops`.
#
# THE RULE THAT MATTERS: a Buzz post can never change a run. Every function here
# returns 0, never exits, never touches STATUS, NOTIFIED or the liveness markers,
# and logs what happened. The post runs in a child process under a hard timeout,
# so a hung relay cannot hold the pipeline lock either.
#
# Delivery goes through the estate runtime's buzz_post (governed alert floor ->
# signed notifier transport). The card is routine, so it is sent at `info` with the
# floor lowered for this one call, the model rewrite off (the card is already
# deterministic), the email floor off and the dead-man ping off: a digest that
# cannot reach Buzz is logged, not escalated.
#
# Env: BLOG_OPS_BUZZ=0 disables posting, BLOG_OPS_TIMEOUT (seconds, default 120),
#      BLOG_OPS_RUNTIME (defaults to INTENT_RUNTIME, then ~/bin/lib/intent-runtime.sh).

# blog_ops_post <text> [source-name]
# Prints one BLOG-OPS: line describing the outcome. Always returns 0.
blog_ops_post() {
  local text="${1-}" source="${2:-blog-ops}" runtime rc
  if [ -z "$text" ]; then echo "BLOG-OPS: nothing to post"; return 0; fi
  if [ "${BLOG_OPS_BUZZ:-1}" != "1" ]; then echo "BLOG-OPS: disabled (BLOG_OPS_BUZZ=${BLOG_OPS_BUZZ:-})"; return 0; fi
  runtime="${BLOG_OPS_RUNTIME:-${INTENT_RUNTIME:-$HOME/bin/lib/intent-runtime.sh}}"
  if [ ! -r "$runtime" ]; then echo "BLOG-OPS: runtime unavailable; card not posted (run unaffected)"; return 0; fi
  # shellcheck disable=SC2016 # $1/$2 expand inside the child shell, by design
  timeout --kill-after=10 "${BLOG_OPS_TIMEOUT:-120}" \
    env AF_MIN_SEVERITY=info AF_LLM_NORMALIZE=0 AF_EMAIL_FLOOR=0 AF_HC_URL= AF_SKIP_DEDUP=1 \
        AF_SOURCE="$source" \
    bash -c '. "$1" >/dev/null 2>&1 || exit 97
             command -v buzz_post >/dev/null 2>&1 || exit 98
             buzz_post "$2" blog-ops info' _ "$runtime" "$text" >/dev/null 2>&1
  rc=$?
  case "$rc" in
    0)       echo "BLOG-OPS: card handed to buzz_post (topic blog-ops)" ;;
    97|98)   echo "BLOG-OPS: buzz_post unavailable (rc=$rc); card not posted (run unaffected)" ;;
    124|137) echo "BLOG-OPS: post timed out after ${BLOG_OPS_TIMEOUT:-120}s; card not posted (run unaffected)" ;;
    *)       echo "BLOG-OPS: post failed (rc=$rc); card not posted (run unaffected)" ;;
  esac
  return 0
}

# Strip anything that looks like a local path or a credential-shaped token, and
# cap the line length, so a status string can never leak box internals.
_blog_ops_clean() {
  printf '%s' "${1-}" | tr '\n' ' ' \
    | sed -E 's#(/home|/tmp|/srv|/etc|/var|~)/[^ )]*#[local]#g; s#[A-Za-z0-9_-]{40,}#[redacted]#g; s/[[:space:]]+/ /g; s/^ //; s/ $//' \
    | cut -c1-160
}

# blog_ops_daily_digest <date> <status> <land-result> <log> [brief-urgent]
# Prints the card text (at most 11 lines; the transport adds one provenance line).
# Reads only the current run's part of <log>: everything after the last start
# marker, which also covers a failover child that wrote into the same log.
blog_ops_daily_digest() {
  local date="${1-}" status="${2-}" land="${3-}" log_file="${4-}" urgent="${5:-0}"
  local run title_line title shipped classifier url contract brief schema dual
  local caught gave_up needs=""
  run=$(awk '/=== Daily blog-backfill start/{buf=""} {buf=buf $0 "\n"} END{printf "%s", buf}' "$log_file" 2>/dev/null)

  title_line=$(printf '%s' "$run" | grep -oE 'Title: .* \| Tier: [0-9]+ \(classifier [0-9]+' | tail -1)
  if [ -n "$title_line" ]; then
    title=$(printf '%s' "$title_line" | sed -E 's/^Title: (.*) \| Tier: [0-9]+ \(classifier [0-9]+$/\1/')
    shipped=$(printf '%s' "$title_line" | sed -E 's/.*\| Tier: ([0-9]+) .*/\1/')
    classifier=$(printf '%s' "$title_line" | sed -E 's/.*\(classifier ([0-9]+)$/\1/')
  fi
  url=$(printf '%s' "$run" | grep -oE 'Liveness OK: https://[^ ]+' | tail -1 | sed 's/^Liveness OK: //')

  contract=$(printf '%s' "$run" | grep -oE 'PRODUCER-CONTRACT: [A-Za-z-]+' | grep -v 'ADVISORY' | tail -1 | sed 's/^PRODUCER-CONTRACT: //')
  brief=$(printf '%s' "$run" | grep -oE 'ADVISORY: amended contract \([^)]*\): .*' | tail -1 | sed -E 's/^ADVISORY: amended contract //')
  schema=$(printf '%s' "$run" | grep -oE 'ADVISORY: record schema \([^)]*\): .*' | tail -1 | sed -E 's/^ADVISORY: record schema //')

  if printf '%s' "$run" | grep -q 'Dual-published to tonsofskills'; then dual="yes"
  elif printf '%s' "$run" | grep -q 'dual-publish to tonsofskills failed'; then dual="no (failed after retries)"
  elif printf '%s' "$run" | grep -qE 'skipping dual-publish'; then dual="no (skipped)"
  else dual="no (nothing landed)"; fi

  caught=$(printf '%s' "$run" | grep -cE 'CATCH-UP: [0-9-]+ recovered')
  gave_up=$(printf '%s' "$run" | grep -oE 'CATCH-UP: GAVE UP on [0-9-]+' | sed 's/.* on //' | paste -sd, -)

  case "$status" in
    FAILED*|DEGRADED*) needs="the run did not finish clean; the alert is in sys-automation" ;;
  esac
  [ -n "$gave_up" ] && needs="${needs:+$needs; }catch-up gave up on ${gave_up}"
  [ "$urgent" = "1" ] && needs="${needs:+$needs; }a contract switch is close with too few clean runs"

  printf 'Blog daily: %s\n' "$date"
  if [ -n "${title:-}" ]; then
    printf 'Post: %s\n' "$(_blog_ops_clean "$title")"
    printf 'Live: %s\n' "${url:-not confirmed live yet}"
    printf 'Tier: classifier %s -> shipped %s\n' "$classifier" "$shipped"
  else
    case "$land:$status" in
      ALREADY-LANDED*) printf 'Post: already published earlier\n' ;;
      *:FAILED*)       printf 'Post: none landed (the run failed)\n' ;;
      *)               printf 'Post: nothing to publish\n' ;;
    esac
  fi
  printf 'Land: %s | Status: %s\n' "$(_blog_ops_clean "${land:-n/a}")" "$(_blog_ops_clean "$status")"
  printf 'Producer contract: %s\n' "${contract:-not run}"
  printf 'Brief switch %s\n' "$(_blog_ops_clean "${brief:-(enforces 2026-10-14): not reported}")"
  printf 'Record schema switch %s\n' "$(_blog_ops_clean "${schema:-(enforces 2026-10-17): not reported}")"
  printf 'Catch-up: %s published, gave up on %s\n' "$caught" "${gave_up:-none}"
  printf 'Dual-publish to tonsofskills: %s\n' "$dual"
  [ -n "$needs" ] && printf 'needs you: %s\n' "$(_blog_ops_clean "$needs")"
  return 0
}
