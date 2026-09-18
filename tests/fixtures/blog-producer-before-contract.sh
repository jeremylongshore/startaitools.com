# Historical regression fixture, exact function from70e7feda. Never run as a cron.
run_claude_producer() {
  local t0 exitc wall command_prefix=claude provider=claude
  if [ "${PRODUCER_MODE:-auto}" = "auto" ]; then
    # Same MiniMax Anthropic-compatible Claude path already used by the governed
    # compiler. The full Agent/Skill tools remain available; only child env changes.
    command_prefix="python3 '$BLOG_DIR/scripts/blog/claude-minimax-producer.py'"
    provider=claude-minimax
  fi
  log "Invoking: $provider /blog-backfill $YESTERDAY $YESTERDAY (timeout ${TIMEOUT_SECS}s, pty-wrapped)"
  t0=$(date +%s)
  # script(1) gives claude -p a pty so its CLI flushes incrementally instead of
  # buffering until SIGKILL — the precondition for diagnosing wall-time creep.
  if env PATH="$PRODUCER_GUARD_DIR:$PATH" /usr/bin/timeout "$TIMEOUT_SECS" script -e -q -a -c \
      "$command_prefix -p '/blog-backfill $YESTERDAY $YESTERDAY' --dangerously-skip-permissions" "$LOG" >/dev/null 2>&1; then
    wall=$(( $(date +%s) - t0 ))
    log "claude -p exited cleanly after ${wall}s ($((wall/60))m $((wall%60))s)"
    PRODUCER_USED="$provider"
    PRODUCER_STATUS="OK ($provider)"
    return 0
  else
    exitc=$?
  fi
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
