# Content Tier Classification System

Four-tier system for classifying daily work journal posts. Tiers 1-3 are auto-classified by the backfill pipeline. Tier 4 is a separate manual workflow (`/blog-research-article`).

**Critical:** Every day's work is covered regardless of tier. Tier determines *treatment* (structure, depth, quality gates), not *scope*.

---

## Tier Definitions

| Tier | Name | Trigger | Lines | Quality Gates |
|------|------|---------|-------|---------------|
| 1 | Field Note | Routine work, known patterns, incremental progress | 80-140 | Hugo build |
| 2 | Technical Deep-Dive | Transferable lesson, debugging journey, design tradeoff | 150-250 | Hugo build + consistency audit |
| 3 | Case Study | Multi-day arc, substantial methodology, system design from first principles | 300-500 | Hugo build + consistency audit + code analysis |
| 4 | Distinguished Paper | Manual trigger — user provides article/topic link | 1200-1800 words | Fact-check + consistency audit + Toulmin structure + user review |

**Expected distribution:** 60-70% Tier 1, 25-35% Tier 2, 5-10% Tier 3

---

## Six Scoring Dimensions (0-5)

### NOV — Novelty

| Score | Anchor |
|-------|--------|
| 0 | Copy-paste from docs or known recipe |
| 1 | Routine application of known pattern to new context |
| 2 | Minor adaptation — tweaked an existing approach for edge case |
| 3 | Synthesized multiple known approaches into something not obvious |
| 4 | Solved a problem with no clear prior art in this stack |
| 5 | Genuinely new technique, framework, or methodology |

### ARC — Architectural Significance

| Score | Anchor |
|-------|--------|
| 0 | Config change, typo fix, dependency bump |
| 1 | Single-file bug fix or feature addition within existing architecture |
| 2 | Multi-file change that follows existing patterns |
| 3 | New module or service boundary introduced |
| 4 | Architectural pattern change affecting multiple systems |
| 5 | New paradigm — fundamentally changes how the system operates |

### NAR — Narrative Richness

| Score | Anchor |
|-------|--------|
| 0 | Linear execution — did X, then Y, then Z, all worked |
| 1 | Minor complication — one thing didn't work, quick fix |
| 2 | Debugging journey with one false lead |
| 3 | Real drama — multiple failed approaches, surprising root cause |
| 4 | Arc with tension, reversal, and insight — the kind of story you'd tell at a meetup |
| 5 | Multi-act narrative with cascading discoveries and paradigm shift |

### TCH — Teaching Potential

| Score | Anchor |
|-------|--------|
| 0 | Project-specific — useful only to someone working on this exact codebase |
| 1 | Transferable within the stack (e.g., Hugo tip useful to Hugo users) |
| 2 | Transferable across stacks (e.g., debugging technique applicable anywhere) |
| 3 | Changes how someone thinks about a category of problems |
| 4 | Mental model shift — reader sees their own work differently after reading |
| 5 | Framework-level insight — reader can apply this to problems you haven't imagined |

### SCP — Scope

| Score | Anchor |
|-------|--------|
| 0 | Single line change |
| 1 | Single file, single concern |
| 2 | Multiple files, single system |
| 3 | Multiple systems, coordinated changes |
| 4 | Cross-project changes with integration points |
| 5 | Greenfield multi-system build from scratch |

### RPR — Reproducibility

| Score | Anchor |
|-------|--------|
| 0 | Entirely project-specific, no transferable artifacts |
| 1 | Pattern could be described but not extracted |
| 2 | Reusable snippet or technique, needs adaptation |
| 3 | Extractable module or template with clear interface |
| 4 | Packageable tool or library others could use directly |
| 5 | Published, documented, versioned artifact |

---

## Classification Algorithm

1. Score all 6 dimensions independently (0-5 each)
2. Apply tier rules:
   - **Tier 3 (Case Study):** max(NOV, TCH) >= 4 AND NAR >= 4 AND 3+ dimensions >= 3
   - **Tier 2 (Deep-Dive):** max(NOV, TCH, NAR) >= 3 AND 2+ dimensions >= 3
   - **Tier 1 (Field Note):** Everything else
3. Apply overrides:
   - **"Year from now" test:** Would this post be useful to a stranger 12 months from now? If no, downgrade one tier.
   - **Source sufficiency check:** Is there enough detail in the gathered material to sustain the tier's target length without padding? If no, downgrade.
4. Tier 4 is never auto-assigned — it is a separate manual workflow via `/blog-research-article`.

---

## Anti-Inflation Rules

1. **Volume is not quality.** 42 commits of PDF extraction is still Tier 1 if the technique is known.
2. **Busy ≠ distinguished.** 3 routine projects in one day = Tier 1. Breadth without depth doesn't escalate.
3. **First-time-for-me ≠ novel.** If it's post #10,001 on the topic in the wider world, NOV stays low.
4. **"Year from now" test.** If this won't be useful to a stranger in 12 months, downgrade.
5. **Tier 3 is rare.** Maximum 5-10% of days qualify. If you're hitting 15%+, you're inflating.
6. **Default down when in doubt.** A well-written Tier 1 beats a padded Tier 2.
7. **High scope alone doesn't escalate.** A large refactor following known patterns (SCP=5, NOV=1) is still Tier 1.

---

## Anchor Enforcement (added 2026-05-16 after May calibration inflation)

The dimension anchors above are **strict floors**, not suggestions. The classifier was scoring TCH at 3.9 mean / SCP at 3.9 mean across May 2026 — which made the Tier 2 gate structurally always-true and eliminated Tier 1 entirely. To prevent recurrence:

### TCH (Teaching Potential) — hard rules

- **TCH ≥ 4 requires an explicit, named, transferable artifact** in the day's work. Acceptable evidence: a pattern with a name ("dual-layer pattern", "three-guards"), a framework, a published methodology document, an extractable rule. Without a named artifact, TCH caps at 3.
- **TCH ≥ 3 requires the work to demonstrably "change how someone thinks about a category of problems."** Bug-fix narratives, CI tweaks, dep bumps, single-PR ship reports do NOT meet this bar. Default TCH for daily ops work is 1-2.
- **TCH = 5 is reserved for framework-level insight** that applies beyond the immediate problem domain. Single-blog-post work almost never qualifies. If you reach for TCH=5, downgrade to 3 unless you can name a non-author audience that will adopt the pattern within 3 months.

### SCP (Scope) — hard rules

- **SCP ≥ 3 requires multiple distinct systems with coordinated changes.** A single-repo, single-PR change is SCP=1-2 regardless of file count. The "multiple files in one repo" case is SCP=2.
- **SCP ≥ 4 requires cross-project integration points.** Touching configs in one repo does not qualify.
- **High SCP alone never escalates tier** (existing rule 7). With the new anchor floor, this rule should rarely need to fire — but it remains a safety net.

### Confidence-gated downgrade

- **If `confidence < 0.85` AND the highest-scoring qualifying dimension is exactly at the tier-gate threshold value** (e.g., TCH=3 fires the Tier 2 gate, NAR=4 fires the Tier 3 gate), **downgrade one tier**. The threshold value is the most over-promoted score; if confidence is also soft, the call is bait.

### 14-day distribution feedback (mandatory pre-classification check)

Before scoring, read the past 14 calendar days of `methodology/decisions.jsonl`. Count tier distribution. If **Tier 1 share is below 50%**, prepend this self-check to your reasoning:

> "Past 14 days show Tier 1 at {N}% (target 60-70%). I am likely inflating. Today's call must explicitly justify why this is NOT a Tier 1, naming the specific dimension that fires the gate and the anchor that supports the score."

If you cannot fill that template honestly, the day is Tier 1.

---

## Calibration Examples

### Example A: Apr 7 — WCAG Color Audit, CSS Variable Bumps

- NOV: 1 (standard accessibility practice)
- ARC: 1 (CSS variable changes)
- NAR: 0 (linear execution, everything worked)
- TCH: 1 (WCAG guidance is well-documented)
- SCP: 2 (multiple files, single concern)
- RPR: 1 (project-specific palette choices)
- **Result: Tier 1 (Field Note)** — routine maintenance, no drama, no transferable insight.

### Example B: Apr 6 — 7 Epics Bootstrapping a Knowledge OS

- NOV: 3 (synthesizing epic planning methodology across disparate systems)
- ARC: 4 (new system boundaries, epic structure across repos)
- NAR: 3 (design decisions with tradeoffs, but linear progression)
- TCH: 4 (epic planning methodology is transferable)
- SCP: 5 (cross-project, greenfield planning)
- RPR: 3 (epic template is extractable)
- max(NOV, TCH) = 4, NAR = 3 (not >= 4) — Tier 3 test fails
- max(NOV, TCH, NAR) = 4 >= 3, dims >= 3: NOV(3), ARC(4), TCH(4), SCP(5), RPR(3) = 5 dims — Tier 2 passes
- **Result: Tier 2 (Technical Deep-Dive)** — substantial but narrative is linear, not dramatic enough for Case Study.

### Example D (2026-05-13 — inflation correction): Transitive CVE Clearance

**Input summary:** Single repo, single PR. Bumped a transitive dep to clear two CVEs using `overrides` field in package.json. 99-line blog post. Clear pattern explanation, single artifact (the overrides snippet).

**Classifier's original (inflated) call:** Tier 2, TCH=4, SCP=4, confidence 0.82.

**Corrected call under enforced anchors:**
- NOV: 1 (overrides field is documented; CVE clearance pattern is widely known)
- ARC: 1 (single-file change)
- NAR: 1 (linear — found CVE, applied overrides, verified)
- TCH: 2 (transferable within Node ecosystem; no named framework — fails the "named artifact" requirement for TCH≥3)
- SCP: 1 (single file, single concern — definitionally SCP=1 per anchor)
- RPR: 2 (overrides snippet is reusable but project-specific)
- max(NOV,TCH,NAR)=2, fails Tier 2 gate
- **Result: Tier 1 (Field Note)** — short, transferable-but-bounded fix-it post. The original Tier 2 inflated TCH and SCP past their anchors.

**Lesson:** Even when the post is genuinely useful, "useful" is the Tier 1 default. The Tier 2 bar is *transferable lesson*, which requires more than "here's a pattern" — it requires the named, packageable thing.

### Example E (2026-05-12 — inflation correction): Three Guards Against Shipping Slop

**Input summary:** 114-line post about three pre-ship review process patterns. Named patterns ("three guards") but no extraction beyond the post itself. Single conversation/PR retrospective.

**Classifier's original (inflated) call:** Tier 3, confidence 0.86.

**Corrected call under enforced anchors:**
- NOV: 2 (synthesizing three review tactics in one frame)
- ARC: 1 (process change, not architectural)
- NAR: 2 (modest — three vignettes, no reversal or surprise)
- TCH: 3 (passes named-artifact test — "three guards" is the named frame)
- SCP: 1 (single review process, single repo)
- RPR: 2 (the three-guards pattern is extractable but not packageable)
- Tier 3 gate: max(NOV,TCH)=3 (need ≥4), NAR=2 (need ≥4) — **fails both Tier 3 requirements**
- Tier 2 gate: max(NOV,TCH,NAR)=3, 2+ dims ≥ 3? Only TCH=3 — fails
- **Result: Tier 1 (Field Note)** with consideration for Tier 2 if the post had hit 150+ lines with deeper extraction.

**Lesson:** Length is signal. A 114-line post cannot carry a Tier 3 case study. If the classifier wants Tier 3 but the writer naturally produces 114 lines, the classifier was wrong, not the writer.

### Example C: Multi-Day Debugging Journey with Architecture Reversal

- NOV: 4 (discovered undocumented API behavior, built workaround)
- ARC: 4 (had to redesign integration layer)
- NAR: 5 (three failed approaches, surprising root cause, architecture reversal)
- TCH: 4 (debugging methodology and API gotcha are widely applicable)
- SCP: 3 (multiple systems)
- RPR: 3 (diagnostic pattern is extractable)
- max(NOV, TCH) = 4 >= 4, NAR = 5 >= 4, dims >= 3: all 6 >= 3 — Tier 3 passes
- **Result: Tier 3 (Case Study)** — genuine drama, transferable insight, worth a lightning talk.
