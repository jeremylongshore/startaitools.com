# SEO grounding for startaitools.com

**What this file is.** The ten `~/.claude/agents/seo-*.md` agents are generic. They
are shared by every repo on this box, so they cannot be edited to fit one blog, and
they were written with no knowledge of this one. This file is the grounding that
makes their advice apply here. Every `polish-seo.md` brief points at this file by
absolute path, the same way `write-post.md` points at `voice-denylist.json`.

**Where it lives and why.** In the repo, under version control, next to the other
enforcement data. The SEO briefs are instructions and live globally; this is the
grounding data those instructions read, and it is a git diff when it changes.

Absolute path for briefs:

```
/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/references/seo-grounding.md
```

---

## Part 1: corrections to the generic agents

Paste the relevant rows into any SEO agent brief. Where a generic agent and this
file disagree, **this file wins**. The agent does not know what it is looking at.

| Generic agent says | Reality here | What to do instead |
|---|---|---|
| `seo-meta-optimizer:39`: "Include special characters for visibility (✓ → ★)" | The site voice bans emoji in titles and body, and the article linter treats decorative punctuation as a voice violation. This instruction ran on posts shipped this week. | **Ignore it.** No checkmarks, arrows, stars, or emoji in `title` or `description`. Ever. |
| `seo-meta-optimizer:65,69`: "WordPress SEO plugin settings (Yoast/RankMath)" | This is Hugo. There is no plugin layer. | Meta is TOML front matter: `title`, `description`, `slug`. Change those fields, nothing else. |
| `seo-structure-architect:77`: "WordPress: TOC plugin config" | Hugo. The TOC is a front-matter flag. | Set `toc = true` in front matter. It renders through `layouts/_default/single.html`. |
| `seo-snippet-hunter:90`: "WordPress: FAQ block setup" | Hugo, Goldmark, `unsafe = true`. | Write the FAQ as plain markdown headings, or inline a `<script type="application/ld+json">` block. No block editor exists. |
| `seo-authority-builder:112`: "WordPress: Author box plugins, schema" | Hugo, single author, Archie theme. | Authority is carried by the receipts in Part 2, not by an author-box widget. |
| `seo-content-refresher:61,64`: "Update statistics from 2023 to 2025" and "Update meta title with 2025" | Hardcoded years that were already stale when written. | Never put a year in a title unless the post is genuinely about that year. A dated title ages the post the day it publishes. |
| Any agent suggesting a dash in a title or heading | Em dash and en dash are hard-banned everywhere by `lint-post-voice.py`, which gates the land path. | Use a colon, a period, or parentheses. A suggestion containing a dash is rejected, not fixed. |
| Any agent suggesting a hype verb or a stock opener | The 26-entry deny-list at `scripts/voice-denylist.json` is enforced on the article and now on the syndication copy too. | Read the deny-list before accepting a rewrite. A "punchier" title that trips it is not punchier, it is a build failure. |

**Structural constraint the agents do not know:** post URLs are
`/posts/<slug>/` and `slug` is set explicitly in front matter. An agent that
"improves" the title without touching `slug` is correct and safe. An agent that
changes `slug` on an already-published post breaks the canonical URL, the
syndication ledger entry, and every cross-post that points at it. **Slug changes are
allowed on unpublished drafts only.**

---

## Part 2: E-E-A-T expressed as our receipts

The generic authority agent asks abstract questions ("does the post signal
expertise?"). Abstract questions get abstract answers, and abstract answers are how
a post ends up padded with credential language instead of evidence. Here the four
E-E-A-T dimensions have concrete, checkable forms. Grade against these.

### Experience: was the writer actually there

The strongest signal this blog has, and the one no competitor can copy, is that
every post is a record of work that happened on a specific day.

**Present when:**

- First person about work actually done. "I shipped", "we found", "it broke at 4am".
- A specific date, a specific commit, a specific run. Not "recently".
- The failure is in the post. What was tried first and why it lost.
- Concrete numbers with units and a source. "40s to 6s on the CI runner", not "much faster".

**Absent when:**

- The post explains a technology in general rather than reporting its use here.
- Second person instructional voice ("you should configure...") with no evidence the
  writer configured it.
- Outcomes with no measurement behind them.

**How to fix a weak Experience signal:** do not add adjectives. Add a receipt. Pull
the actual number, name the actual file, link the actual run.

### Expertise: is the mechanism named precisely

**Present when:**

- Tools named with versions. `Hugo 0.150.0`, not "our static site generator".
- Models named by exact full name. `Claude Opus 4.8`, `Grok 4.5`, `GPT-5.6 Sol`. Never
  the bare vendor.
- The actual mechanism is described, not a metaphor for it. Which gate, which check,
  which boundary between the deterministic path and the model path.
- Real code from the real repo. Not illustrative pseudocode.
- A "why not the obvious approach" passage that names the alternative and why it lost.

**Absent when:**

- Vague nouns doing the work of specific ones: "the system", "the pipeline", "the tool".
- Code that could not run.
- A tradeoff asserted without stating what was given up.

### Authoritativeness: does it connect to a body of work

**Present when:**

- Links out to primary sources: the vendor's own docs, an RFC, a spec, a released
  changelog. Not a summary blog of the primary source.
- Links in to prior posts here that carry the earlier stage of the same work. This is
  the topical cluster, and it is built by cross-linking honestly rather than by
  keyword adjacency.
- Public artifacts where they exist: the PR, the commit, the CI run, the released
  package, the repository.

**Absent when:**

- Zero outbound links, or outbound links only to aggregators.
- Cross-links chosen because the slug shares a keyword rather than because the post
  is genuinely the prior chapter.

**The specific ask:** every post ends with 2 to 3 Related Posts. Those are the
authority graph. Pick them for continuity of the actual work, not for keyword overlap.

### Trust: does it admit what it does not know

This dimension is where a work journal beats a marketing blog, and it is the one a
generic SEO agent will quietly optimize away, because hedges look like weak copy to a
conversion-oriented reader. They are not weak here. They are the product.

**Present when:**

- Named constraints. What this does not handle, what it was not tested against.
- An honest scope statement. "This works on one box. It has not run on a second."
- The cost stated. What it took, what it still costs to run.
- Corrections carried forward when a later post reverses an earlier one.

**Absent when:**

- Every result is clean.
- No limitation appears anywhere.
- A hedge got edited out to make a sentence land harder.

**Hard rule for SEO polish:** a polish agent may never remove a caveat, a limitation,
or a stated cost to improve readability or keyword density. Those sentences are the
Trust signal. If an agent proposes cutting one, reject it and record the rejection.

---

## Part 3: what the polish pass may and may not touch

The SEO pass runs after the truth gates (consistency, fact check, code review) and
before the first commit. By then the post is true. The polish pass protects
discoverability without putting truth back at risk.

**May change:**

- `title` and `description` in front matter, within the voice rules.
- Heading wording, when the heading is vague and a precise one exists.
- Heading hierarchy, when a level is skipped.
- Added internal links where a genuine prior post exists.
- Added JSON-LD.
- Word choice, where the replacement is equally accurate.

**May never change:**

- `slug` on a published post.
- Any number, date, version, model name, or file path. Those came from the gates.
- Any caveat, limitation, tradeoff, or stated cost.
- The failure narrative.
- Anything that would make the post claim more than the day's work supports.

**A polish suggestion that trips the voice linter is not a suggestion.** Reject it
without a counter-proposal round; the deny-list and the dash ban are not negotiable
against a keyword-density target.

---

## Part 4: the honest position on keyword targeting

This blog does not chase keywords. It publishes a daily record and the record ranks
on long-tail specificity, because the exact error string, the exact version pair, and
the exact failure mode are what a searching engineer actually types.

Practical consequences for the SEO agents:

- **Keyword density targets are advisory here, not a gate.** A post about one narrow
  failure will naturally repeat the failing component's name. That is the long tail
  working, not stuffing.
- **Do not add a keyword the post did not earn.** If the post does not discuss the
  thing, no density target justifies mentioning it.
- **Titles are specific over broad.** "The day the green checks were lying" beats
  "CI best practices" here, because the person who needs it is searching for their
  symptom.
- **The front-of-funnel queue is the real keyword input.** `next-topics.py` ranks
  candidates from actual Umami content performance. That data beats a volume estimate
  from a generic agent, because it is this site's readers rather than a global average.

---

## Part 5: grading checklist

Score a draft against this before accepting any SEO agent's verdict.

| Check | Pass condition |
|---|---|
| Experience | At least one first person account of specific work, with a date, commit, or run behind it |
| Expertise | Every tool and model named exactly, with versions where they matter |
| Authority | At least one primary source outbound, 2 to 3 honest Related Posts inbound |
| Trust | At least one named limitation, constraint, or cost |
| Voice | `lint-post-voice.py` exits 0 |
| Meta | Title under 60 characters where the voice allows, description under 160, no emoji, no dash, no year |
| Structure | No skipped heading levels, slug matches filename |
| Register | Reports rather than persuades (see `write-post.md`, "This is a work journal") |

A post failing Trust or Voice does not ship, regardless of its SEO score. A post
failing Meta or Structure gets fixed in place. A post failing Experience is usually
not a polish problem; it is a draft written about a topic rather than about a day.

## Part 6 : What actually wins, measured (added 2026-09-01, refresh quarterly)

90-day Umami channel + UTM attribution, pulled 2026-09-01. This is the evidence
behind the title-as-search-query rule and the PAA/FAQ step. Cite these numbers in
briefs instead of generic SEO theory.

**Channels (real human visits; the ~3.7k "direct" is bots/monitors, ignore it):**

| Channel | Visits/quarter |
|---|---|
| Organic search | 34 (the largest real channel) |
| Referral (GitHub, own sites) | 28 |
| Organic social (the whole syndication machine) | 23 |
| LLM answer engines (ChatGPT, Perplexity, Kagi) | 6 (small, growing, already citing us) |

**Search detail:** Bing + DuckDuckGo out-refer Google roughly 3:1 (24 vs 7).
Optimize for the Bing family too, not Google alone. BlogPosting JSON-LD is now
emitted deterministically by `layouts/partials/schema.html` on every dated page.

**The shape that wins:** searchable, named-tool, how-to posts. Top performers:
a vision-language model guide (65 visitors), "Building a CAD-DXF Agent from Zero
to v0.1.0" (45), "Fixing Claude Code Hooks: the New Matcher Format" (37).
Introspective/governance daily posts cluster at 10-17 regardless of quality.
A title that names the tool, the error, or the version is the single most valuable discoverability edit this phase can make.

**The LLM channel:** posts get cited inside AI answers when they contain a
clean, quotable, direct answer near the top. The mandatory `tldr` front-matter
param is that answer. Protect it: one paragraph, states the finding plainly,
no dashes, quotable out of context.
