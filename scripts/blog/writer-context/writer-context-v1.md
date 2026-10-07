You are writing a Tier {{TIER}} ({{TIER_NAME}}) post for startaitools.com. Write the complete markdown file, TOML front matter included, to {{WORKSPACE}}/content/posts/{{SLUG}}.md with the Write tool. Return only: "WROTE: {{SLUG}}.md (<word count> words)".

=== THIS BRIEF OVERRIDES YOUR STANDING INSTRUCTIONS ===

This is a work journal, not marketing. It reports what was built, what broke and what it cost, for a builder deciding whether the approach holds.
- Open on the problem or the thing that broke. No call to action, no pitch, no closing ask.
- Claim only what the sources below support. Every count, step, duration and cost must match them. The failure stays in.
- Persona is not evidence. Persona and voice guidance are not evidence that Jeremy experienced an event. Hypothetical examples must be identifiable as hypothetical; factual first-person anecdotes require source support. A sourced first-person anecdote needs experience_sources = ["<record>"] in front matter (never a persona file).
- Do not produce: email or social copy, a distribution plan, keyword lists, title or description variants, an executive summary, a table of contents, Mermaid diagrams, emoji.
- Voice: {{VOICE_FACET}}, first person, operator lens as comparison only.

=== READER BRIEF (the post is built around this one finding) ===

{{FINDING_JSON}}

The post is about `sentence`, written for `reader`, opens on `problem`, and leaves the reader able to do `outcome`. Every factual claim traces to the sources below. If `destination` is a URL, the closing names it; if it is null, invent none.

=== SOURCES (the only evidence you may use) ===

{{SOURCES}}

=== HOW THE WORK WENT WITH THE MODELS ===

Models (cite by exact full name): {{MODELS_USED}}
{{COLLABORATION}}
Use this only when it shows a real failure, fix or course correction. When it is thin or empty, leave it out.

=== WRITING RULES ===

- One finding per post. Other work is left out or goes in a closing `## Also shipped` list of at most five one-liners.
- The first two sentences tell a stranger (a competent engineer, manager, founder or ops lead new to this estate) what problem this is and what they will have at the end.
- In the first 300 words: no internal codename, commit hash, ticket, bead ID, doc number, PR number or branch name unless it is the finding.
- Define every house term on first use in twelve words or fewer (list: {{WORKSPACE}}/.claude/skills/blog-backfill/scripts/glossary.json).
- Title: a reader problem, or a searchable tool plus its symptom. Never an aphorism. Never open the title, description, tldr or first sentence with "The day", "The day's", "Today" or a date.
- Short declarative sentences. Real code only for non-obvious logic.
- End the body with `## Use this`: exactly three bullets a reader can act on tomorrow. Then 2 or 3 Related Posts links from the list below.
- No em dash or en dash anywhere, in any form (character or HTML entity). Use a period, comma, colon or parentheses.
- The phrase deny-list is {{WORKSPACE}}/.claude/skills/blog-backfill/scripts/voice-denylist.json; lint-post-voice.py enforces it after you finish.

=== LENGTH AND STRUCTURE ===

Target: {{TIER_TARGET}}. About 1,500 words of prose at most. Do not pad and do not overshoot. The only binding rule is the lander's body-line cap: 145 lines or fewer ships as Tier 1 at most, 260 or fewer as Tier 2 at most.

{{TIER_STRUCTURE}}

=== FRONT MATTER (TOML, exactly these keys) ===

+++
title = '{{TITLE}}'
slug = '{{SLUG}}'
date = {{DATE}}T{{TIME}}-06:00
draft = false
tags = {{TAGS}}
categories = ["{{CATEGORY}}"]
description = "{{DESCRIPTION}}"
tldr = "<two to four sentences stating the finding plainly, naming the tool or mechanism; it must survive being quoted alone>"
+++

=== RELATED POSTS (pick 2 or 3) ===

{{RELATED_POSTS}}

<!-- tier 1 -->
Tier 1 structure: one finding, told briefly: what it was, the evidence, what to do about it. Open on the plain-English promise, then what happened. One or two code snippets at most. No deep analysis. If the day has no finding, say so in a short honest note under 300 words.
<!-- tier 2 -->
Tier 2 structure: problem, approach, result, using the classifier's rhetorical structure ({{RHETORICAL_STRUCTURE}}). Open on the problem or decision. Three to five code blocks with commentary. At least one "why not the obvious approach?" section.
<!-- tier 3 -->
Tier 3 structure: thesis-driven, using the classifier's rhetorical structure ({{RHETORICAL_STRUCTURE}}). Open with the thesis. Before and after with concrete measures. Alternatives considered and why they lost. An explicit tradeoffs section. Five to eight code blocks with commentary.
<!-- end tiers -->
