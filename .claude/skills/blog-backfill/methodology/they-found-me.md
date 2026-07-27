# They Found Me — Inbound Credibility Dossier

**Scope:** the consolidated list of inbound credibility that Jeremy can reference in public copy. The list is **publicly verifiable**: each entry either (a) names a specific person / org + a public source for the inbound event, or (b) ties to an artifact (training roster, partner badge, GitHub follow, etc.) that Jeremy has direct evidence of.

**Bead:** startaitools-6ys

**Last refreshed:** 2026-07-27

---

## Master list

| # | Who | What | Source / Evidence | Confidence |
|---|---|---|---|---|
| 1 | **Mudit Gupta** (CISO/CTO Polygon) | Public follow + signal-boost across X and LinkedIn | Public posts on Mudit's X (`@Mudit__Gupta`) and LinkedIn identifying Jeremy + claude-code-plugins. Searchable. | High — verifiable by anyone |
| 2 | **Nixtla** (CEO / co-founder) | Named paid consulting client. Nixtla reached out via inbound email | Invoice record on file (`/home/jeremy/000-projects/intent-solutions/clients/nixtla/` — INTERNAL ONLY). The public attribution is "we work with Nixtla on time-series forecasting infra" or equivalent; specific deal size + scope is NOT public. | Medium — partially public; client-permitted framing only |
| 3 | **Lit Protocol** | Inbound curiosity → partnership conversation | Inbound email + call record; Lit is a public company so the partnership talk itself is public-attributable via blog post / social mention. | Medium-High — public via their blog + Jeremy's CS piece |
| 4 | **Elm** | Inbound conversation | Inbound email + Slack DM record. Elm is part of the Claude Code Slack Channel use case publicly cited. | Medium — Jeremy has the email; customer is OK with private reference for now |
| 5 | **Anthropic Claude Partner Badge** | Issued 2026-07 to Jeremy Longshore | Public Credly record: `https://www.credly.com/badges/ddf22fb4-0aa6-46b3-a93b-0b45b509e471`. Plus the Claude Partner Network program is itself a public Anthropic program. | High — verified; latest addition (yesterday, PR #36/#37/#38/#39 closed this dossier gap) |

## Pending inbound (filed as separate bead: startaitools-dnv)

| Who | Why pending |
|---|---|
| **Kilo AI** (Emilie ??, Title ??) | LinkedIn gist + Kilo AI funding/backing line needed before Jeremy can name them. See `startaitools-dnv`. Until that's filled, Kilo goes in the **excluded pending list** below. |

## Excluded (with reasons)

| Why excluded | What we don't say |
|---|---|
| Anthropic Direct Partner / Investor / Strategic | We are NOT direct partners. Until Anthropic publicly announces Jeremy (or the Enterprise Program cohort rosters him by name), framing is "in the Enterprise Program" + the verifiable partner badge. CLAUDE.md rule: "anthropic partner" is **not** OK until approved. |
| Customer rosters | Names of any client we billed (other than Nixtla) are private. Don't name clients — describe the work as a category. |
| Cohort roster (35 subcontractors) | PII (per CLAUDE.md). NEVER name individually. Refer to the cohort as "the team." |
| Recovery / addiction history | Per CLAUDE.md: never appears in any externally-published artifact. Out. |
| Specific deal sizes, pay rates, hour allocations | Out. |
| Internal team relationships | Out. |

## How to use this dossier

When writing a Tier 1+ post that references inbound credibility:

1. **Pull this file first** (`cat .claude/skills/blog-backfill/methodology/they-found-me.md`).
2. **Cross-check any named person/org** against the master list + the `startaitools-dnv` pending list.
3. **If a name is on neither list**, either find the source / consent trail in your `client/` folder, or refuse to name them.
4. **If a name is in "Excluded"**, do NOT mention them. Use the canonical category framing (e.g., "in the Anthropic Enterprise Program," not "Anthropic partner").

## Copy snippets (when templates are useful)

For headline copy and meta descriptions:

- "Mudit Gupta (CISO/CTO Polygon) called this out publicly — see for yourself." → links Mudit's X or LinkedIn post
- "Nixtla engaged us for time-series forecasting work." → does NOT name a deal size or scope
- "Lit Protocol and Elm both reached out." → uses both names verbatim
- "Anthropic's Claude Partner Network alumnus — verify at the public Credly record." → links the Credly badge directly

## Maintenance protocol

- Add an entry when a new inbound arrives. The source-of-truth for the inbound event lives in `/home/jeremy/000-projects/intent-solutions/clients/<name>/inbound-log.md` (the client folder convention).
- Drop an entry when (a) the person/org publicly retracts or (b) consent is revoked.
- Refresh monthly OR on-PR-merge.
