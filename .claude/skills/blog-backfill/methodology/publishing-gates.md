# GC Verifiability Pass — publishing gate for /blog-backfill

**Owner:** the writer agent (whether Claude Code, Grok, or human) is responsible for running this pass before publishing any Tier 1/2/3 post that makes a verifiable claim about Jeremy Longshore, Intent Solutions, the OSS portfolio, or a named third party.

**Bead:** startaitools-0yk

The pass is non-negotiable. Every claim that fails the rules below must be either (a) replaced with a verified source, (b) caveated as a rough estimate with a date, or (c) cut.

---

## The rules (canonical, last revised 2026-07-27)

1. **Verifiable-or-caveated-or-cut.** No claim that the reader can disprove with a single fact-check. If it can't be verified against a public source as-of a known date, the claim must be caveated or cut.

2. **Named third parties only with consent.** Naming a specific person, company, or partner (Mudit Gupta, Nixtla, Kilo AI, Lit Protocol, Anthropic, etc.) requires either (a) Jeremy's explicit written consent for the specific claim, or (b) a public, attributable source that has already named them in the same context. The bead description: "anthropic partner" is **not** OK until approved; "training toward Claude certifications / Enterprise Program" is OK because it's already a public program descriptor.

3. **PII red lines.** The cohort roster (35 subcontractors), private Anthropic-program friction, partner-relationship dynamics, dollar amounts, pay info, internal team relationships — all PII; OUT of any public artifact.

4. **Metrics: dated + rounded + live-linked.**
   - Star counts: "2,500+ GitHub stars (as of 2026-07-27, verify: github.com/jeremylongshore/claude-code-plugins-plus-skills)"
   - Downloads: only with a live link to a verifiable source. Examples:
     - NPM: link to `https://api.npmjs.org/downloads/point/last-year/@intentsolutionsio/ccpi`
     - GitHub clones: link to `https://github.com/jeremylongshore/claude-code-plugins-plus-skills` (use the Insights tab to source)
   - Never round up a count that you can't verify as-of a date.

5. **NPM downloads specifically.**
   - Verified 2026-07-27: `@intentsolutionsio/ccpi` averaged ~2,000 downloads/year (`last-year` range). The canonical 45,000+ claim previously circulating on `startaitools.com/about/` and `intent-os/persona/master.md` is **unverified** and should be replaced with the live count + a `verify:` link. (Update applied to `content/about.md` 2026-07-27.)

6. **Anthropic framing.** Until explicit partner-program approval, write "training toward Claude certifications / in the Enterprise Program" — not "Anthropic partner." Jeremy's Claude Partner Badge (issued 2026-07) is verifiable at `https://www.credly.com/badges/ddf22fb4-...`; refer to it as "Claude Partner Network alumnus" or "credentialed Claude consultant" rather than "partner."

7. **Nixtla, Mudit, Kilo, Lit, Elm** (per CLAUDE.md inbound-credibility list) may be named **with a source**. The source must be Jeremy's credibility dossier (this list), not invented. Each still requires per-claim consent.

---

## How to run the pass

Before publishing a Tier 1+ post:

```bash
# 1. Pull current canonical persona
less /home/jeremy/000-projects/intent-os/persona/master.md

# 2. Pull current live metrics (any "2,500+ stars" claims need an as-of-date)
gh repo view jeremylongshore/claude-code-plugins-plus-skills --json stargazerCount,forkCount,updatedAt
curl -s https://api.npmjs.org/downloads/point/last-year/@intentsolutionsio/ccpi | jq .

# 3. For every metric in the draft, the post must say:
#    - "X units (as of YYYY-MM-DD, verify: live-link)"
#    - OR be cut / replaced with a qualitative claim

# 4. For every named third party, append a Verification line:
#    - "Named: <name>. Source: <URL> or Jeremy's consent (per persona/master.md)."
#    - If the named entity is Anthropic and the claim is "partner" — STOP and use the Enterprise-Program framing instead.

# 5. For every PII risk: red line check (rule 3 above). If in doubt, cut.
```

A post that fails the pass returns to the writer with explicit fix-up notes rather than publishing in degraded state.

---

## Why this exists

The 2026-07-16 persona audit found that 11 different Jeremy Longshore sites/posts had drifted apart on factual claims; the canonical answer lived in `persona/master.md` but the on-site copy hadn't been reconciled. That drift was both embarrassing (the same fact had four different versions on the same page in some cases) and reputationally fragile (a reader could fact-check a single number and conclude the entire site overclaimed). The GC verifiability pass is the publishing-side fix: every new post goes through this checklist before merge so drift stops accumulating.

The bead stays in the queue as a recurring gate — every `/blog-backfill` run for a Tier 1+ post implicitly re-runs this pass. New entries in the decision log (`methodology/decisions.jsonl`) record the rule updates, e.g.:

```
# 2026-07-27 — bead startaitools-0yk closed with PR #TBD:
#   - about.md: replaced unverifiable "45,000+ NPM downloads" with verified
#     "~2,000 NPM downloads/year (as of 2026-07-27, verify: api.npmjs.org/...)"
#   - companion fix to persona/master.md is a separate bead (the persona
#     canonical claim format line was the source of the drift)
```

---

## Pass-signing-off

When the writer signs off the pass, append to `methodology/decisions.jsonl`:

```
{"ts": "<ISO8601>", "post": "<slug>", "pass": "gc-verifiability", "verifier": "<agent>", "result": "pass|fix|cut", "n_fixes": <int>}
```

This append becomes part of the audit log that future agents can grep.
