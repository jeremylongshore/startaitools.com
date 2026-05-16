# Step 5: SEO Polish Pipeline

Runs AFTER consistency/fact gates pass, BEFORE the first commit. Applies per-tier.

The gates above (classifier, consistency-checker, fact-checker, code-reviewer) protect truth and coherence. This polish pipeline protects discoverability. Both matter — the best post in the world does nothing if readers never find it.

## Per-Tier Pipeline

| Agent | Tier 1 | Tier 2 | Tier 3 |
|-------|:------:|:------:|:------:|
| `seo-meta-optimizer` | ✓ | ✓ | ✓ |
| `seo-structure-architect` | — | ✓ | ✓ |
| `seo-snippet-hunter` | — | ✓ | ✓ |
| `seo-keyword-strategist` | — | ✓ | ✓ |
| `seo-authority-builder` | — | — | ✓ |
| `seo-content-auditor` | — | — | ✓ |

All agents dispatch via `Agent(subagent_type="<name>", prompt=<brief>)`. Each receives the full draft post path and returns structured suggestions. The main thread applies the suggestions to the draft before moving on.

## Agent Briefs

### seo-meta-optimizer

**Input:** draft post path, target keywords (derived from classification's thesis + tags).

**Asks:**
- Is the title under 60 characters? Rewrite if not — keep primary keyword near the front.
- Is the description under 160 characters and keyword-inclusive? Rewrite if not.
- Does the slug follow kebab-case and match the canonical URL pattern `/posts/<slug>/`? Fix if not.

**Applies:** updates `title`, `description`, `slug` in the front matter.

### seo-structure-architect

**Input:** draft post path.

**Asks:**
- Is the header hierarchy sequential (H1 → H2 → H3, no skipping)? Fix.
- Are H2s keyword-anchored rather than cute?
- Does the post have ≥3 internal links to related content on startaitools.com? If not, suggest placements.
- Would BlogPosting JSON-LD schema improve SERP treatment? Emit the schema for the main thread to inject.

**Applies:** heading restructure (if needed), internal-link insertions, optional `<script type="application/ld+json">` block at the end of the body.

### seo-snippet-hunter

**Input:** draft post path.

**Asks:**
- Does the post answer a clear question? If yes, is the first answer a 40–60-word snippet-optimized paragraph directly under a question-shaped H2?
- Are there list/table structures Google is likely to feature?
- If no featured-snippet surface exists, suggest one addition (one tight paragraph or one table) that fits the narrative.

**Applies:** small additive rewrite — never deletes existing content, only proposes insertions.

### seo-keyword-strategist

**Input:** draft post path, primary tags, thesis.

**Asks:**
- Measure density of primary keyword. If >2.5%, suggest de-emphasis (over-optimization risk). If <0.5%, suggest natural insertions.
- Identify LSI / semantic variations missing from the body. Suggest 3–5 natural insertions.
- Flag keyword stuffing or thin sections.

**Applies:** targeted word/phrase swaps in the body, never structural rewrites.

### seo-authority-builder (Tier 3 only)

**Input:** draft post path.

**Asks:**
- Does the post signal E-E-A-T (Experience, Expertise, Authoritativeness, Trust)?
  - Experience: first-person "I/we shipped X" moments?
  - Expertise: concrete technical depth tied to named tools/versions/APIs?
  - Authoritativeness: links out to authoritative sources (docs, RFCs, spec), plus internal links to prior work?
  - Trust: honest tradeoffs, named constraints, explicit caveats?
- Flag any claim that needs a citation (YMYL territory — security, finance, medical, legal).

**Applies:** suggests paragraph-level additions. Main thread decides whether to accept.

### seo-content-auditor (Tier 3 only)

**Input:** draft post path.

**Output:** a 0–100 score with per-dimension breakdown (content depth, originality, E-E-A-T, scannability, source quality). Returns PASS/REVISE/BLOCK.

If BLOCK, fix the flagged issues and re-run. If REVISE, apply high-confidence suggestions and move on.

## Audit Trail

Every agent invocation in this phase is recorded in the post's `agent_audit` block in `decisions.jsonl`:

```json
"agent_audit": {
  "writer": "docs-architect",
  "code_reviewer": "PASS",
  "consistency": { "skill_local": "PASS", "global": "PASS" },
  "fact_check": { "skill_local": "PASS", "global": "PASS" },
  "seo": {
    "meta_optimizer": "applied",
    "structure_architect": "applied",
    "snippet_hunter": "applied",
    "keyword_strategist": "applied",
    "authority_builder": "applied",
    "content_auditor": { "score": 87, "verdict": "PASS" }
  }
}
```

This trail is what `/blog-calibrate` uses to measure whether the deeper pipeline improves outcomes over the inline-fallback path.

## Fallback

If any SEO agent is unavailable, skip it and record `"skipped: unavailable"` in the audit trail. Do not block publication on an unavailable optional polish agent.
