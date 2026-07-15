# Step 3: Write the Post

Dispatch a **tier-specific writer agent** via the Agent tool. The agent writes the post directly to disk at `/home/jeremy/000-projects/blog/startaitools/content/posts/SLUG.md`.

## Writer Agent Selection (by tier)

| Tier | Agent | Why |
|------|-------|-----|
| 1 (Field Note) | `content-marketer` | Best for concise narrative logs, conversational voice |
| 2 (Deep-Dive) | `content-marketer` OR `docs-architect` — pick by subject | `docs-architect` if the post is architecture/system-design focused; `content-marketer` if it's a debugging-journey or shipping-narrative |
| 3 (Case Study) | `docs-architect` | Long-form, thesis-driven, deep technical analysis |

All tiers: dispatch via `Agent(subagent_type="<agent-name>", prompt="<full brief>")`. The brief must include:
- The full classification result JSON from Phase 2 step 2
- All gathered source material (git logs, PR bodies, session-transcript digest, CLAUDE.md excerpts, beads history)
- The writing style rules below (paste verbatim)
- The tier-specific structure rules (paste from this file)
- The absolute path where the post must be written
- Instruction to output NOTHING except a confirmation line — the post goes to disk, not stdout

## Post-Writer: Code Snippet Review (all tiers that include code)

If the draft contains any code blocks, dispatch `code-reviewer` in parallel with the first quality gate. Its job is narrow: are the snippets syntactically correct, do the variable names match the narrative, do the types/calls resolve? Returns PASS / REVISE / BLOCK. Fix BLOCKs before running consistency/fact gates.

## Inline-Writer Fallback — EMERGENCY USE ONLY

**Inline writing is the fallback path. The default is the Agent call.**

Only use this fallback when the Agent tool itself returns a hard error AFTER at least one dispatch attempt. The `agent_audit.writer_agent.fallback_reason` field must contain the literal error message from the failed Agent call.

These reasons **do not qualify** and are actively prohibited:

- "I already have the context in this thread" — dispatch anyway; the agent will use what you brief it with
- "Rate limits hit, agents will have less info than me" — brief the agent with what you have; partial context is normal
- "Dispatching 4 agents in parallel feels slow" — it is faster than writing 4 Tier-2+ posts inline; dispatch
- "The task is urgent and the user said don't skimp" — the user saying "don't skimp" is the strongest argument to use the agent, not skip it
- "Efficiency" / "pragmatism" / "simpler path" — not reasons, rationalizations

If you write inline without an Agent-tool error message to cite, you violated the skill. Record it honestly: `"writer_agent": "inline-fallback:violated-skill-due-to-<honest-reason>"`. The /blog-calibrate skill counts these.

### The briefing cost is the excuse — use the template

If briefing feels too expensive to bother dispatching, use `references/writer-briefing-template.md`. Fill slots, dispatch 4 agents in parallel, done.

---

## Writer Instructions

Output a complete markdown file with TOML front matter. Write directly to `/home/jeremy/000-projects/blog/startaitools/content/posts/SLUG.md`.

### Front matter template (TOML only)

```toml
+++
title = 'Descriptive Title Based on Primary Work'
slug = 'kebab-case-matching-filename'
date = YYYY-MM-DDT10:00:00-06:00
draft = false
tags = ["relevant", "tags"]
categories = ["Technical Deep-Dive"]
description = "SEO description under 160 chars"
+++
```

**Filename**: `slug.md` (NO date prefix — dates are in front matter only)

### Writing style rules

- Lead with the problem or what needed to happen
- Show real code snippets (key logic, not boilerplate)
- Direct, opinionated tone. Short declarative sentences.
- Show failures/debugging journeys when they happened
- State opinions directly, backed by shown work
- Connect to the broader Intent Solutions narrative
- Target audience: builders, Claude Code users, production systems engineers
- End with 2-3 Related Posts cross-links to existing content
- Prefer period, comma, colon, or parentheses for asides. Never a dash run-on.

### Absolutely forbidden (AI slop + voice fingerprint)

**Hard ban: em dash and en dash.** Zero tolerance, everywhere in the file:
title, description, headings, body, code comments you invent, Related Posts lines.
Do not use `—` (U+2014), `–` (U+2013), or HTML `&mdash;` / `&ndash;`.
Section titles: use a colon or a plain title (`## Disguise 1: empty args…`), never
`## Title — subtitle`. Subtitles and meta description: same rule.

If you are about to write an em dash, rewrite as two sentences or use parens.

**Banned phrases** (case-insensitive; if any appear, rewrite before saving):

- "In this blog post" / "In this article" / "In this post"
- "Let's dive in" / "dive into" / "diving deep"
- "It's worth noting" / "worth noting that"
- "delve" / "delving"
- "comprehensive"
- "in today's fast-paced"
- "game-changer" / "game changer"
- "revolutionize" / "seamless" / "supercharge"
- "excited to share" / "thrilled to"
- "unlock the" / "leverage" (hype verb)
- "at its core" / "in conclusion"
- "the landscape of" / "navigate the"
- "without further ado" / "it goes without saying"
- Any mermaid diagrams (site never uses them)
- Generic intros or outros
- Emoji in titles or body

**Enforcement:** after the draft is on disk, the main thread runs
`${CLAUDE_SKILL_DIR}/scripts/lint-post-voice.py content/posts/SLUG.md`.
Non-zero exit = rewrite until clean. `blog-land.sh` re-runs the same lint and
**quarantines** (does not publish) on failure. CI lints changed posts on PRs.

---

## Tier-Specific Writer Instructions

The classification result determines the post's structure, depth, and quality gates. **All tiers cover every repo that had activity that day** — tier determines *treatment*, not *scope*.

### Tier 1: Field Note (80-140 lines)

**Structure:** Concise narrative log. Thematic grouping or chronological flow.

**Approach:**
- Lead with what needed to happen and what got done
- Cover all active repos — one paragraph each for minor work, two for primary repos
- Code snippets only for non-obvious logic (1-2 max)
- No deep analysis — state what was done and move on
- Narrative thread connects the day's work, but don't force a grand theme

**Quality bar:** "Would someone scanning this in an RSS reader get the gist in 60 seconds?"

**Quality gates:** Hugo build passes.

### Tier 2: Technical Deep-Dive (150-250 lines)

**Structure:** Problem/approach/result arc. Use the rhetorical structure from the classifier (problem-solution, before-after, or debugging-journey).

**Approach:**
- Open with the problem or decision that made this day interesting
- Show the approach with code and commentary (3-5 code blocks)
- Include at least one "why not the obvious approach?" section
- Cover secondary repos in a brief "Also shipped" section at the end
- Consistency audit required (run `blog-consistency-checker` agent)

**Quality bar:** "Would a senior engineer at a different company bookmark this?"

**Quality gates:** Hugo build + consistency audit passes.

### Tier 3: Case Study (300-500 lines)

**Structure:** Thesis-driven. Use the rhetorical structure from the classifier (thesis-driven, comparative-analysis, or design-rationale).

**Approach:**
- Open with a thesis statement (from classifier's `thesis_candidate`)
- Before/after analysis with concrete metrics or comparisons
- Design decision rationale — show alternatives considered and why they lost
- Explicit tradeoffs section: what did you give up?
- External context — how does this relate to the broader ecosystem?
- Code with deep commentary (5-8 code blocks)
- Cover secondary repos in a brief "Also shipped" section at the end
- Both consistency audit and code analysis required

**Quality bar:** "Would this be worth a conference lightning talk?"

**Quality gates:** Hugo build + consistency audit + deeper code analysis.

### Tier 4: Distinguished Paper (1200-1800 words)

**Not used in the backfill pipeline.** This tier is handled exclusively by `/blog-research-article`.

See `~/.claude/skills/blog-research-article/SKILL.md` for the full Toulmin-structured workflow.

---

## Tags taxonomy (use these, don't invent new)

**High-frequency:** ai-agents, typescript, python, testing, ci-cd, architecture, claude-code, debugging, automation, docker, authentication, release-engineering, devops, full-stack, web-development, fastapi, react, monorepo

**Categories:** Technical Deep-Dive (default), Development Journey, AI Engineering, DevOps, Architecture, Weekly Recap, Monthly Retrospective

**Cadence tags (auto-added):** weekly-recap, monthly-retro
