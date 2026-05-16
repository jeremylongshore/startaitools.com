# Step 1: Gather ALL Source Material

Run these in parallel where possible for each day being backfilled.

## Git logs across ALL repos

```bash
for dir in /home/jeremy/000-projects/*/; do
  if [ -d "$dir/.git" ]; then
    commits=$(git -C "$dir" log --oneline --after="$PREV_DAY_T23:59:59-06:00" --before="$DAY_T23:59:59-06:00" 2>/dev/null)
    [ -n "$commits" ] && echo "=== $(basename $dir) ===" && echo "$commits"
  fi
done
```

## Detailed git logs for top 2-3 repos (by commit count)

```bash
git -C /home/jeremy/000-projects/REPO log --after="..." --before="..." --stat --format="%h %s%n%b"
```

## Merged PRs (richest signal — include bodies with before/after tables)

```bash
gh pr list --repo jeremylongshore/REPO --state merged --json title,body,mergedAt,number
```

## PR review bot comments (CodeRabbit, Gemini, Greptile)

```bash
gh api repos/jeremylongshore/REPO/pulls/N/reviews
gh api repos/jeremylongshore/REPO/pulls/N/comments
```

## Beads task history across registered workspaces

```bash
for ws in claude-code-plugins git-with-intent irsb irsb/solver irsb/watchtower irsb-monorepo kilo iams/bobs-brain; do
  cd /home/jeremy/000-projects/$ws 2>/dev/null
  bd list --closed-after "$DATE" --closed-before "$NEXT_DATE" --all --flat 2>/dev/null
done
```

## Claude Code session transcripts (user messages, assistant responses, debugging journeys)

```bash
python3 /home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/scripts/scan-session-transcripts.py \
  --start "$DATE" --end "$NEXT_DATE" \
  --output /tmp/session-context-$DATE.txt
```

This captures what was discussed, debugged, and decided during Claude Code sessions —
richer context than git logs alone (rationale, false starts, user intent). Scans all
`~/.claude/projects/*/*.jsonl` files. Skips tool results, thinking blocks, and
null-timestamp metadata. Output groups by project and day with timestamps.

Optional: `--project SUBSTRING` to filter to a single project.

## Project CLAUDE.md for architecture context

```bash
cat /home/jeremy/000-projects/REPO/CLAUDE.md
```

Read CLAUDE.md from the primary repos that had activity that day to understand architecture context for the blog post.

## Email signals (optional)

Scan Gmail for relevant threads from the day. This is a low-cost optional signal — skip gracefully if no relevant threads found.

### Guardrails

**DO NOT scan all email.** Use targeted queries with date range + sender/subject filters. Each backfill day should make at most 3-4 search queries, not a broad inbox scan. If no relevant signals found in the first pass, record `"email": "absent"` and move on.

**Time budget:** Email scan should take < 30 seconds per day. If it's taking longer, the queries are too broad.

**What to search for (allowlist — only these categories):**
- Bounty notifications (Algora, GitHub Sponsors)
- PR review requests from external contributors
- Community feedback or collaboration threads
- Whop/marketplace notifications
- Deployment alerts or incident notifications

**What to SKIP (never scan these):**
- Personal email
- Marketing/promotional emails
- Mailing list digests
- Calendar invitations
- Anything not directly related to the day's development work

### Tool Options (in order of preference)

**Option A: IntentMail MCP tools (preferred — local, fast, privacy-first)**

IntentMail is the local email platform at `/home/jeremy/000-projects/intent-mail/`. If the MCP server is running (`./bin/intentmail.js serve`), use its search tools — they query a local SQLite+FTS5 index, no network calls after initial sync.

```
intentmail search --after YYYY-MM-DD --before YYYY-MM-DD --from "notifications@github.com OR algora.io"
intentmail search --after YYYY-MM-DD --before YYYY-MM-DD --subject "review requested"
```

**Option B: Gmail MCP tools (Claude.ai — works without local setup)**

```
mcp__claude_ai_Gmail__search_threads — search by date range and keywords
mcp__claude_ai_Gmail__get_thread — read specific thread content
```

**Option C: gogcli (steipete's CLI — fast, JSON-first, script-friendly)**

If installed (`brew install gogcli` or build from source):
```bash
gogcli gmail search "after:YYYY/MM/DD before:YYYY/MM/DD from:notifications@github.com" --json
gogcli gmail search "after:YYYY/MM/DD before:YYYY/MM/DD subject:review requested" --json
```

### Search queries (all tools — adapt syntax per tool)

```
# Bounty/sponsorship notifications
after:YYYY/MM/DD before:YYYY/MM/DD (from:notifications@github.com OR from:algora.io OR from:whop.com)

# PR review requests
after:YYYY/MM/DD before:YYYY/MM/DD subject:"review requested" OR subject:"pull request"

# Deployment/CI notifications
after:YYYY/MM/DD before:YYYY/MM/DD (from:netlify.com OR from:github.com) subject:"deploy" OR subject:"build"
```

### Output

If relevant threads found, summarize key signals (1-2 sentences each). If nothing relevant, record `"email": "absent"` in source signals. Do not fabricate email content.

### Privacy

Only extract factual signals (notification type, sender, subject). Do not include email body content verbatim in blog posts. Email is a signal source for context, not a content source.

### Future: msgvault integration

[msgvault](https://github.com/wesm/msgvault) by Wes McKinney uses DuckDB + Parquet for fast offline email analytics. Once set up, it could replace live Gmail queries with instant local search — zero network latency, full offline capability. Has an MCP server for Claude Desktop integration. Consider adopting after initial sync of Gmail archive.
