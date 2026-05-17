# Content Strategy Reference

Research-backed guidance for cadence, distribution, community building, and content mix. Sources: Orbit Media's annual blogging survey, HubSpot cadence research, Google E-E-A-T framework, 90-9-1 participation inequality model, ACM evaluation criteria.

---

## Cadence Research

**Orbit Media (2024):** Bloggers who publish 2-6x/week are 2.5x more likely to report "strong results" than those publishing weekly or less. But quality gates matter — the correlation breaks down when posts are thin.

**HubSpot:** Companies publishing 16+ posts/month get 3.5x more traffic than those publishing 0-4. Diminishing returns kick in above daily frequency unless each post has a distinct audience segment.

**Our model:** Daily field notes (Tier 1) + weekly recaps + monthly retros. The daily cadence works because Tier 1 posts are lean and honest — they don't pretend to be more than what happened. The weekly and monthly posts provide aggregation layers that reward return visitors.

---

## Content Mix: Cluster / Pillar / Flagship

| Type | Tier | % of Posts | SEO Role | Reader Value |
|------|------|-----------|----------|-------------|
| Cluster | Tier 1 (Field Note) | 60-70% | Long-tail keywords, fresh content signals | Daily proof-of-work, real-time learning |
| Pillar | Tier 2 (Deep-Dive) | 25-35% | Medium-tail keywords, topical authority | Transferable lessons, bookmark-worthy |
| Flagship | Tier 3-4 (Case Study / Distinguished) | 5-10% | Head terms, backlink magnets | Reference material, citation-worthy |

**Research backing:** HubSpot's topic cluster model shows cluster content ranks 2.5x longer and drives +30% organic traffic when properly interlinked to pillar pages. Our tier system maps directly to this model.

**Internal linking pattern:**
- Tier 1 posts link to their week's recap and relevant Tier 2/3 posts
- Tier 2 posts link to the specific Tier 1 posts that covered the same work at daily granularity
- Tier 3 posts link to the full chain of daily posts that built up to the case study
- Weekly recaps link to all daily posts from that week
- Monthly retros link to weekly recaps and top-performing posts

---

## Distribution Strategy

### Stagger Pattern

| Platform | Timing | Purpose |
|----------|--------|---------|
| startaitools.com (canonical) | Day 0 | SEO authority, canonical URL |
| tonsofskills.com (mirror) | Day 0 | Portfolio visibility |
| Dev.to | Day 0 + 24-48h | Developer community reach |
| Hashnode | Day 0 + 24-48h | Developer community reach |
| Medium | Day 0 + 48-72h | General audience reach |
| Substack | Day 0 + 48-72h | Newsletter subscribers |

**Why stagger:** Google needs time to index the canonical URL before syndicated copies appear. Publishing everywhere simultaneously risks Google choosing the wrong canonical. 24-48h buffer is sufficient for indexing.

**Canonical attribution:** Every cross-posted version must include a canonical URL pointing to startaitools.com. This is non-negotiable for SEO.

### Tier-Specific Distribution

| Tier | Platforms | Social |
|------|-----------|--------|
| 1 (Field Note) | startaitools + tonsofskills only | Optional X post |
| 2 (Deep-Dive) | All platforms | X thread + LinkedIn post |
| 3 (Case Study) | All platforms | X thread + LinkedIn post + targeted outreach |
| 4 (Distinguished) | All platforms | Full social campaign |
| Weekly Recap | startaitools + tonsofskills | LinkedIn post |
| Monthly Retro | All platforms | X thread + LinkedIn post |

**Rationale:** Tier 1 posts are work journals — valuable for the archive and daily cadence but not worth cross-posting. Tier 2+ posts have transferable value worth distributing.

---

## Google E-E-A-T Alignment

| Signal | How We Demonstrate It |
|--------|-----------------------|
| **Experience** | Daily work journals show real hands-on work with code, commits, PRs |
| **Expertise** | Tier 2-3 posts demonstrate deep technical knowledge and methodology |
| **Authoritativeness** | Consistent publishing cadence, cross-post presence, methodology tracking |
| **Trustworthiness** | Auditable decision records, fact-checked Tier 3-4 content, transparent methodology |

The tier system inherently serves E-E-A-T: Tier 1 proves Experience, Tier 2 proves Expertise, Tier 3 proves Authoritativeness, and the methodology tracking system proves Trustworthiness.

---

## Community Building: 90-9-1 Model

| Segment | % of Audience | Behavior | What They Need |
|---------|--------------|----------|----------------|
| Lurkers | 90% | Read, don't engage | Scannable posts, clear takeaways, code snippets to copy |
| Contributors | 9% | Comment, share, apply | Deeper context, tradeoff discussions, reusable patterns |
| Creators | 1% | Build on your work, cite you | Methodology, frameworks, extractable tools |

**Write for all three:**
- Tier 1 serves lurkers (daily, scannable, proof-of-work)
- Tier 2 serves contributors (transferable lessons they can apply)
- Tier 3-4 serves creators (frameworks and methodology they can build on)

---

## Metrics That Matter

**Primary (track these):**
- Time-on-page per tier (Tier 2+ should be 2x+ Tier 1)
- Return visitor rate (weekly recap readers should return)
- Cross-post engagement (Dev.to reactions, Hashnode bookmarks)

**Secondary (useful context):**
- Raw pageviews (vanity but useful for trend)
- Subscriber growth (Substack, RSS)
- Backlinks to Tier 3-4 posts

**Anti-metrics (don't optimize for):**
- Post count (already covered by daily cadence)
- Word count (tier system handles this)
- Social media followers (lagging indicator)

---

## Seasonal Patterns

- **Conference seasons** (spring/fall): Increase Tier 3 output if presenting
- **Release weeks**: Tier 2+ natural — releases have narrative arc
- **Holiday periods**: Tier 1 only, shorter posts, maintain cadence
- **Hackathon/sprint weeks**: High commit volume, likely still Tier 1 (volume ≠ quality)
