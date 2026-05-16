# Writer-Agent Briefing Template

**Purpose:** Turn "briefing 4 writers in parallel is slow" into a mechanical fill-and-dispatch. Copy the template below, fill the slots, make 4 parallel Agent calls in a single tool-use block.

If you find yourself reaching for inline writing because "briefing is expensive," stop. Fill this template. Dispatch. The briefing cost is exactly four copy-paste-and-fill operations.

---

## Template (fill every `{{SLOT}}`, then paste into Agent `prompt`)

```
You are writing a Tier {{TIER}} blog post for startaitools.com. Write the complete markdown file with TOML front matter directly to /home/jeremy/000-projects/blog/startaitools/content/posts/{{SLUG}}.md. Output NOTHING to stdout except a one-line confirmation when done.

=== CLASSIFICATION (from blog-classifier) ===

{{CLASSIFICATION_JSON}}

=== GATHERED MATERIAL ===

--- Git log ({{DATE}}) ---
{{GIT_LOG}}

--- PR bodies (top 5-10 most relevant) ---
{{PR_BODIES}}

--- Beads closed this day ---
{{BEADS_LOG}}

--- Session transcript digest (relevant excerpts only) ---
{{SESSION_DIGEST}}

--- CLAUDE.md excerpts from active repos ---
{{CLAUDE_MD_EXCERPTS}}

=== WRITING STYLE RULES (verbatim) ===

- Lead with the problem or what needed to happen
- Show real code snippets (key logic, not boilerplate)
- Direct, opinionated tone. Short declarative sentences.
- Show failures/debugging journeys when they happened
- State opinions directly, backed by shown work
- Connect to the broader Intent Solutions narrative
- Target audience: builders, Claude Code users, production systems engineers
- End with 2-3 Related Posts cross-links to existing content

FORBIDDEN PHRASES (AI slop):
- "In this blog post"
- "Let's dive in"
- "It's worth noting"
- "diving deep"
- "comprehensive"
- Any mermaid diagrams (site never uses them)
- Generic intros or outros
- Emoji in titles or body (the site voice is plain-direct)

=== TIER-{{TIER}} STRUCTURE RULES ===

{{TIER_STRUCTURE}}

(paste the exact tier block from references/write-post.md — Tier 1 = 80-140 lines Field Note, Tier 2 = 150-250 lines Deep-Dive with problem/approach/result arc, Tier 3 = 300-500 lines thesis-driven case study)

=== FRONT MATTER SHAPE (TOML, no deviation) ===

+++
title = '{{TITLE}}'
slug = '{{SLUG}}'
date = {{DATE}}T{{TIME}}-05:00
draft = false
tags = {{TAGS}}
categories = ["{{CATEGORY}}"]
description = "{{DESCRIPTION}}"
+++

=== RELATED POSTS CONTEXT ===

Candidates for cross-linking (pick 3, prioritize most relevant):
{{RELATED_POST_SLUGS}}

=== OUTPUT CONTRACT ===

1. Write the file to /home/jeremy/000-projects/blog/startaitools/content/posts/{{SLUG}}.md
2. Use ONLY the Write tool — do not print the post to stdout
3. Return exactly one confirmation line: "WROTE: {{SLUG}}.md ({{WORD_COUNT}} words)"
4. Do NOT include the footer signature — the main thread adds that
```

---

## Dispatching 4 writers in parallel

After classifier has produced JSON for all 4 days, make ONE tool-use block with 4 `Agent` calls:

```
Agent(subagent_type="docs-architect",      prompt="<filled template for Tier 3 day>")
Agent(subagent_type="content-marketer",    prompt="<filled template for Tier 2 day A>")
Agent(subagent_type="docs-architect",      prompt="<filled template for Tier 2 day B>")
Agent(subagent_type="content-marketer",    prompt="<filled template for Tier 1 day>")
```

All four run concurrently. The main thread moves on to dispatching quality-gate agents in parallel while the writer agents work.

---

## Slot reference

| Slot | Source | Notes |
|------|--------|-------|
| `{{TIER}}` | classifier.tier | integer 1 / 2 / 3 |
| `{{SLUG}}` | classifier.slug | kebab-case, matches filename |
| `{{CLASSIFICATION_JSON}}` | entire JSON record from classifier | paste verbatim |
| `{{GIT_LOG}}` | output of git log for the day, trimmed to ~2000 lines | drop churn commits |
| `{{PR_BODIES}}` | top 5-10 PR bodies by relevance, first 800 chars each | not all PRs — the ones that matter |
| `{{BEADS_LOG}}` | `bd list --closed-after/--closed-before` output for the day | |
| `{{SESSION_DIGEST}}` | relevant sections from scan-session-transcripts.py output | don't dump the full 60k-line file |
| `{{CLAUDE_MD_EXCERPTS}}` | first 200 lines of CLAUDE.md from each active repo | architectural context |
| `{{TITLE}}` | your title choice (under 60 chars if possible, but voice > char count) | |
| `{{DATE}}` | YYYY-MM-DD | |
| `{{TIME}}` | T08:00:00, T09:00:00, T10:00:00 for stagger | |
| `{{TAGS}}` | array of taxonomy tags from write-post.md § "Tags taxonomy" | |
| `{{CATEGORY}}` | one of the allowed categories (Case Study, Technical Deep-Dive, Development Journey, etc.) | |
| `{{DESCRIPTION}}` | SEO meta under 160 chars | |
| `{{RELATED_POST_SLUGS}}` | 5-8 candidate slugs from grep of content/posts/ + 1-line summary each | let the agent pick 3 |
| `{{TIER_STRUCTURE}}` | Tier-specific block pasted verbatim from write-post.md lines 78-130 | |
| `{{WORD_COUNT}}` | leave empty — agent fills it in the confirmation | |

---

## When the 1M-context main thread has better evidence than the agent will

This is the most common rationalization for inline writing. It is almost always wrong.

- The agent's context is a clean slate brief with the specific evidence you selected as load-bearing. That is a feature, not a bug.
- The main thread's 1M of context is polluted with tool-call noise, prior conversation, and tokens that are not about this post. Polluted context writes polluted posts.
- If the agent writes something wrong, the quality-gate agents in step 5 catch it. That's their job.
- Inline writing bypasses the quality-gate signal loop. Writing mistakes made inline don't show up in the calibration data, which means they never get fixed systematically.

Dispatch the agent. Let the signal loop work.
