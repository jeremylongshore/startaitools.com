# Phase 4: Final Verification

After all posts are published, run through this checklist:

## Build Verification

1. `hugo --buildFuture --gc --minify --cleanDestinationDir` — clean production build for startaitools
2. `cd /home/jeremy/000-projects/claude-code-plugins/marketplace && npm run build` — verify tonsofskills build
3. Verify post count matches expected on both sites
4. Spot-check 3 posts for: correct dates, working code blocks, no AI slop, no em/en dashes
   (for any *new* post in the batch: `python3 ${CLAUDE_SKILL_DIR}/scripts/lint-post-voice.py content/posts/SLUG.md` must exit 0)

## Cross-Post & Social Verification

5. Confirm cross-post queue entries created in `.crosspost-queue.json` with correct staggered timestamps
6. Verify any ready cross-posts were published with correct canonical URLs pointing to startaitools.com
7. Verify Substack drafts exist in `$SUBSTACK_OUTPUT_DIR` with canonical attribution footers
8. Confirm social bundles emailed via Gmail (or bundle files saved to `/tmp` if send failed)

## Methodology & Decision Record Verification

9. **Decision records exist:** Verify every classified day has a corresponding entry in `/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/methodology/decisions.jsonl`. Each record must have: date, slug, tier, confidence, all 6 dimension scores, reasoning, and source signals.

10. **Tier distribution sanity check:** Review the batch's tier distribution. If >40% of days in the batch are Tier 2+, flag for review — this likely indicates classification inflation. Expected: 60-70% Tier 1, 25-35% Tier 2, 5-10% Tier 3.

11. **Anti-inflation audit:** Check that no Tier 3 posts were classified without meeting all three gate conditions (max(NOV,TCH) >= 4 AND NAR >= 4 AND 3+ dimensions >= 3). Read `references/content-tier-classification.md` for the full algorithm.

12. **Quality gate compliance:** Verify each post received the quality gates required by its tier per `SKILL.md` Quality Gates table. Each post's `agent_audit` block in `decisions.jsonl` must record:
    - **Tier 1:** `writer`, Hugo build
    - **Tier 2:** `writer`, `code_reviewer` (if code blocks present), `blog-consistency-checker`, `article-consistency-checker`, SEO polish (meta, structure, snippet, keyword), Hugo build
    - **Tier 3:** everything in Tier 2 plus `blog-fact-checker`, `fact-checker`, `seo-authority-builder`, `seo-content-auditor`, code analysis

    If any required agent is missing from the audit trail, flag the post in the final report. If an agent was unavailable, the trail must record `"skipped: unavailable"` — a missing field is a pipeline failure, not an accepted skip.

13. **Agent audit trail schema:** Every `decisions.jsonl` entry for a tier-2+ post must include an `agent_audit` object following the schema in `references/polish-seo.md`. Example:
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

14. **SQLite methodology index rebuild (every run):** JSONL is the append-only source of truth; the SQLite index is a derived, queryable analytics layer. Rebuild it at the end of every backfill batch so calibration (`/blog-calibrate`), feedback correlation (`/blog-feedback`), and cross-run analytics stay current:
    ```bash
    /home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/scripts/rebuild-methodology-index.sh
    ```
    The script runs `rebuild-index.sql` (schema) then imports all JSONL records via Python (decisions, feedback, patterns) and prints a tier-distribution summary plus the last 10 decisions as verification. Re-running is idempotent — the schema drops and recreates all tables.
