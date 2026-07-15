# Release v0.15.6

**Release Date**: 2026-07-15

## Changes since v0.15.5

- chore: release v0.15.6 [skip ci] (d3467c50)
- chore(beads): append interaction log for voice-lint bead close (08306c37)

---

# Release v0.15.5

**Release Date**: 2026-07-15

## Changes since v0.15.4

- chore: release v0.15.5 [skip ci] (5f3d67b7)
- Merge pull request #27 from jeremylongshore/fix/blog-voice-no-emdash-slop (06dcf972)
- fix(blog-backfill): mask code/URLs in voice slop scan; catch decode errors (90e8a8d9)
- fix(blog-backfill): hard-ban em dashes and AI-slop via voice lint gate (dd1f013e)

---

# Release v0.15.4

**Release Date**: 2026-07-14

## Changes since v0.15.3

- chore: release v0.15.4 [skip ci] (3d8bd251)
- post(2026-07-13): Empty Is Not Clean: Five Fail-Open Bugs in an AI Agent — Tier 2 (8b4cfd3f)

---

# Release v0.15.3

**Release Date**: 2026-07-13

## Changes since v0.15.2

- chore: release v0.15.3 [skip ci] (3f4bdf1a)
- post(2026-07-12): The Kernel Must Not Import Its Agents — Tier 2 (dcc6d5e5)
- chore(methodology): weekly feedback-sweep 2026-07-12 (cdfd5098)

---

# Release v0.15.2

**Release Date**: 2026-07-12

## Changes since v0.15.1

- chore: release v0.15.2 [skip ci] (85b72f91)
- post(2026-07-11): Making a Fire-and-Forget Writer Safe Under Failure — Tier 2 (0c8b0981)

---

# Release v0.15.1

**Release Date**: 2026-07-11

## Changes since v0.15.0

- chore: release v0.15.1 [skip ci] (0cbf4a1f)
- post(2026-07-10): Liveness Without Health Is Theater — Tier 2 (e2973062)

---

# Release v0.15.0

**Release Date**: 2026-07-10

## Changes since v0.14.7

- chore: release v0.15.0 [skip ci] (3ec90d2c)
- Merge pull request #26 from jeremylongshore/feat/blog-fleet-two-marker-arming (d8ac16e3)
- fix(blog-cron): use fall-through OK branch in the final status exits so shellcheck -S style stays green (a15b340a)
- chore(lint): wrap two >100-char lines in tier-creep-guard.py — unblocks the required ruff check (6a59530e)
- fix(blog-cron): exit non-zero on handled payload failures so .ok tells the truth (21e6c039)
- feat(blog-cron): two-marker liveness (.beat + .ok) across the blog cron fleet via lib-cron-common (9186e0da)
- Merge remote-tracking branch 'origin/fix/blog-cron-fail-alerting-hardening' into feat/blog-fleet-two-marker-arming (fda35aed)
- fix(blog-cron): liveness heartbeats for the already-trapped wrappers (aa96c8a1)
- fix(blog-cron): alert on missing-guard FATAL in tier-creep-guard (ab31db04)
- fix(blog-cron): fail-loud EXIT trap for feedback-sweep (5a8869dd)
- fix(blog-cron): fail-loud EXIT trap for monthly calibrate + retro (a91af687)

---

# Release v0.14.7

**Release Date**: 2026-07-10

## Changes since v0.14.6

- chore: release v0.14.7 [skip ci] (176693aa)
- post(2026-07-09): Adversarial Review: The Six Lenses That Halted a Rollout — Tier 3 (0aee62de)

---

# Release v0.14.6

**Release Date**: 2026-07-09

## Changes since v0.14.5

- chore: release v0.14.6 [skip ci] (6d1aabea)
- post(2026-07-08): Fix the Dependabot Pile-Up: Policy Over Patches — Tier 1 (1ce612fe)

---

# Release v0.14.5

**Release Date**: 2026-07-08

## Changes since v0.14.4

- chore: release v0.14.5 [skip ci] (881f09d2)
- Fix: cross-post scripts sourced a nonexistent .env — Dev.to/Hashnode were silently skipping (#24) (68b501be)

---

# Release v0.14.4

**Release Date**: 2026-07-08

## Changes since v0.14.3

- chore: release v0.14.4 [skip ci] (0df629ec)
- Harden blog cron notifications: sunset ntfy, fail-loud posting-packet, fix Code: link detection (#23) (36ba6042)

---

# Release v0.14.3

**Release Date**: 2026-07-08

## Changes since v0.14.2

- chore: release v0.14.3 [skip ci] (93d8b67c)
- post(2026-07-07): Noise-Robust LLM-Judge Evals: Don't Sign a Coin Flip — Tier 3 (80634314)

---

# Release v0.14.2

**Release Date**: 2026-07-07

## Changes since v0.14.1

- chore: release v0.14.2 [skip ci] (e47f2aea)
- post(2026-07-06): Every Safety Gate Has a Failure Direction — Tier 2 (a06fe703)

---

# Release v0.14.1

**Release Date**: 2026-07-07

## Changes since v0.14.0

- chore: release v0.14.1 [skip ci] (e84e216f)
- docs(claude): make version.txt reference version-agnostic (2ce0369b)

---

# Release v0.14.0

**Release Date**: 2026-07-07

## Changes since v0.13.0

- chore: release v0.14.0 [skip ci] (670bb278)
- fix(ci): stop release workflow failing on 'tag already exists' (1698e207)
- docs(claude): add end-to-end pipeline architecture summary (produce→land→syndicate) (154603b2)
- fix(blog-cron): working-tree-free dual-publish/field-notes push (no more mirror 404) (6d723b1c)
- feat(blog-cron): time-comparison dashboard in the weekly rollup (WoW/MoM/YoY/YTD) (61480cdb)
- fix(blog-cron): emoji in packet + rollup subject lines; fix rollup recipient count (ffe7ef41)
- fix(blog-cron): sanitize packet voice output to valid UTF-8 (kill the � glyph) (6cac4181)
- post(2026-07-05): The Relevance Score That Broke Our Cite-or-Refuse Gate — Tier 2 (c1de3592)
- fix(blog-cron): X is always a single tweet + shorten UTM links (packet) (6dad898f)
- chore(beads): session interaction log — blog pipeline hardening + Ezekiel handoff epic (e634da1c)
- feat(blog-cron): weekly team growth rollup + document the new pipeline (WS2b) (cb4385a5)
- feat(blog-cron): hand social posting to Ezekiel via HTML posting packet (WS2/WS3) (c7e99878)
- feat(blog-cron): invert the commit path — LLM produces, blog-land.sh lands (WS1) (30337f7f)
- feat(blog-cron): daily portfolio web-analytics email to Jeremy (WS0) (588e2261)
- post(2026-07-04): The Moat Is the Trust Layer (NEXUS BYOK RAG) — Tier 3 (99a73e3d)
- fix(blog-cron): bump headless ceiling 1800->2700s for Tier-3 headroom (7008d679)
- feat(blog-cron): add hysteresis to tier-creep guard (no weekly nag) (0209684e)
- chore(methodology): weekly feedback-sweep 2026-07-05 (b1d4c7c2)
- fix(blog-backfill): make the step-8 audit-addendum check order-independent (cc525990)
- chore(blog-methodology): agent audit trail for 2026-07-03 gpt-5.4 post (2a7820c6)
- feat: add blog post for 2026-07-03 — shipping gpt-5.4 as one config line (d2793935)
- feat(blog-cron): self-managing tier-creep tripwire (weekly, deterministic) (f43987f5)
- feat(blog-classifier): Tier-2 narrative-or-standout floor to end T2 creep (148a7799)
- docs(methodology): July 2026 mid-cycle tier-creep calibration check (8e2ec85a)
- chore(methodology): retroactive Tier 2 classification for coreweave field guide (b90bef01)
- post(2026-07-02): Backlog Zero — the estate triage machine (ccbc6a0d)
- fix(blog-skill): Step-0 existing-post check matches unquoted TOML dates (1f3dca75)
- post: CoreWeave GPU-ops field guide — Xid triage, RDMA fallback, MPIJob, LOTA, cost (dd420618)
- post(2026-07-01): Run the Readiness Audit Before You Flip DNS (675d470c)
- fix(blog-cron): calibrate commits+pushes its own output (b878ab57)
- chore(methodology): commit June calibration report + appended pattern (da4b0499)
- fix(blog-cron): detect unquoted TOML dates in daily-backfill post check (5fdc1e6a)
- revert(post): unpublish KPZ paper — move to drafts/ (rough draft, not for publication) (161ee36c)
- post(2026-07-01): The KPZ Universality Class and Tropical Mesoscale Convective Organization (ed4b4662)
- docs(readme): correct post count 37+ → 290+ and drop removed startai/ subdir (1d4de6ce)
- docs(claude): correct CLAUDE.md drift — post count, Hugo version, new sections (14485303)
- chore(beads): close June retro bead startaitools-ccj (61f1dcd5)
- post(2026-06): June 2026 monthly retrospective — first full month under the repaired rubric (265fdae1)
- chore(crosspost): re-enable Hashnode in the pipeline (Pro plan live) (f92b2560)
- feat(home): spotlight 'Rent the Agent, Own the Proof' as the featured hero (5083d312)
- fix(crosspost): Hashnode gql-beta endpoint + Bearer auth + TOML/colon-safe parse (1c11ed17)
- content(drafts): add paste-ready hashnode.md (API paywalled — manual post) (66a632f0)
- content(posts): publish 'Rent the Agent, Own the Proof' (Claude Tag vs CCSC/AGP) (d1376681)
- content(posts): backfill 2026-06-29 — gate the statement, not the tool name (Tier 2) (acf1204b)
- content(posts): backfill 2026-06-28 — coverage vs mutation testing on the rules engine (Tier 2) (09ba6b11)
- chore(methodology): weekly feedback-sweep 2026-06-28 (21deaeb7)
- chore(blog-methodology): agent-audit addendum for 2026-06-27 backfill (e1a76c28)
- content(posts): backfill 2026-06-27 — when LLM output lies instead of crashing (Tier 1) (e1f0bad5)
- content(posts): backfill 2026-06-26 — the LLM should never do the math (Tier 2) (32616971)
- fix(crosspost): TOML/colon-safe Dev.to title parsing + retire dead channels (89ffa50f)
- content(posts): backfill 2026-06-22..06-25 (Batch C) — gap closed (c6b75599)
- content(posts): backfill 2026-06-18..06-21 (Batch B) (0bfcd52f)
- content(posts): backfill 2026-06-14..06-17 (Batch A) (9a74f971)
- fix(hugo): whitelist text/* content types for local 0.163 build gate (e63c4dda)
- chore(beads): close startaitools-74z interaction log (e3178111)
- chore(beads): session interaction log for startaitools-74z (e6a60fc6)
- fix(blog-cron): stop the silent 11-day backfill stall (f7a80281)
- chore(methodology): commit 2026-06-14 feedback-sweep output (570f1cca)
- content(posts): backfill 2026-06-13 — Tier 2 'MCP Server Auth: The API Is the Real Boundary' (ce7a4ad0)
- content(posts): backfill 2026-06-12 — Tier 2 'When --cap-drop ALL Broke the Gate Socket' (2555f4b0)
- content(posts): backfill 2026-06-11 — Tier 2 'Green CI Proves Nothing: Why Your Tests Gate Zero Calls' (bdf4f8c9)
- content(posts): backfill 2026-06-10 — Tier 2 'Honor the Gate When the Verdict Is Inconvenient' (2f836315)
- content(posts): backfill 2026-06-07 (Tier 2 HITL delivery) + 2026-06-08 (Tier 1 uptime monitor) (1c61bc69)
- chore(beads): log canonical-mirror task (966d02dc)
- chore(beads): append bd interaction-log entries (ba18a984)
- content(posts): mirror Kobiton 'Making Agents Reliable' as a canonical-attributed post (f01265f9)
- chore(methodology): append cron feedback-sweep entries + bd interaction log (7a5ec537)
- content(features): add Chapter 2 (Kobiton 'Making Agents Reliable') to Agent-Native Mobile Testing (5c4d249e)
- post(2026-06-06): nine days silent — the blog pipeline that stopped publishing itself (587fa731)
- feat(cron): dormant slack_fail() to #cron-failures on hard cron failures (242b402f)
- chore(methodology): commit stranded agent_audit addendum for 2026-06-05 post (4fdc4268)
- post(2026-06-05): the wrong product, built perfectly — Tier 3 case study on decoupling vs requirements misreads (081515b9)
- Merge pull request #21 from jeremylongshore/feat/cron-hardening-monthly-pty-worktree-escalation (3c299798)
- feat(cron): worktree-aware pre-flight + pty wrap on monthly + consecutive-failure escalation (1a8c8905)
- Merge pull request #20 from jeremylongshore/post/may-2026-monthly-retro (37cf69b4)
- trigger: re-deploy preview after Netlify install-deps transient failure (b7c92989)
- post(2026-06-04): from one adopter to two — discovery-affordance spec just got named (828d3543)
- post(2026-05): May 2026 monthly retrospective — the calibration reckoning (8bf36312)
- Merge pull request #17 from jeremylongshore/feat/cron-preflight-branch-normalize-and-phase-markers (6abd2890)
- fix(cron): lift uncommitted-changes + ff-pull checks outside the branch guard (ea795936)
- feat(cron+skill): eliminate the two largest avoidable costs in the blog pipeline (a23db04b)
- Merge pull request #16 from jeremylongshore/feat/blog-cron-pty-wrap-and-ci-lint (c3b52e3d)
- chore(methodology): append agent audit trail for 2026-05-27 post (052a47bd)
- post(2026-05-27): vite dev server in production — the 871-byte tell (8456cf48)
- fix(hashnode): exit non-zero on 301/302 so caller registers a real failure (c4f1e6e7)
- feat(ci): shellcheck + ruff + Hugo build gates for blog pipeline scripts (c8f55407)
- fix(scripts): clear shellcheck + ruff backlog across blog pipeline helpers (b730c79e)
- fix(cron): pty-wrap claude -p so daily blog-backfill timeouts leave a trail (6469396b)
- fix(cron): raise blog-backfill timeout 1800s → 5400s + log wall time (0330cee0)
- chore(methodology): append agent audit trail for 2026-05-26 post (cbef7022)
- chore: untrack .crosspost-queue.json (untracked per CLAUDE.md) (cac88a0b)
- feat(post): CI gap — shellcheck + ruff caught four findings (2026-05-26) (5f256561)
- feat(post): CodeQL caught the race I dismissed (2026-05-25) (086d5e41)
- feat(post): the Unicode layer your validator can't see — same-day TrapDoor defense (2026-05-24) (1d2e9613)
- fix(methodology): drop stray top-level tier from 2026-05-23 agent_audit record (b16043e6)
- feat(post): self-expiring report-only CI gates — advisory to enforced (2026-05-23) (8655cebb)
- chore(methodology): append agent audit trail for 2026-05-22 post (7a9fb093)
- feat(post): safety model first — 16-tool ops MCP in one day (2026-05-22) (f19948cf)
- feat(post): ICO dogfood zero-to-five FTS fallback (2026-05-21) (52b8e801)
- feat(post): ship dormant, wire later — multi-agent Slack production day (2026-05-20) (f47948d7)
- feat(post): five tags, zero ships — release workflow bug anatomy (2026-05-19) (9d3a8b1b)
- feat(post): v1.0 release gate with conditional GO (2026-05-18) (4d4244b2)
- chore(methodology): append agent audit trail for 2026-05-17 post (9796ea35)
- feat(post): honest perf benchmarks for a paid-API compiler (2026-05-17) (7fbeba09)
- Merge pull request #13 from jeremylongshore/fix/paperback-grid-content (8206fabc)
- fix(paperback): preserve markdown inside HTML grid divs (wild Layer 1/3/4 content) (a30c1abc)
- fix(scripts): handle null was_correct in feedback rebuild (#12) (b480c395)
- fix(scripts): handle null was_correct in feedback.jsonl rebuild (1b1a130c)
- feat(post): five silent failures in one day (2026-05-16) (#11) (87ce5b68)
- feat(post): five silent failures in one day (2026-05-16) (2b035a6a)
- Merge pull request #10 from jeremylongshore/fix/footnote-cluster-spacing (58d7ae17)
- fix(content): comma-separate adjacent footnote markers in wild + IRSB rewrites (5d47cf72)
- Merge pull request #9 from jeremylongshore/redesign/dispatch-aesthetic (41a99060)
- Merge pull request #8 from jeremylongshore/feat/academic-rewrite-wild (d089a278)
- feat(content): academic-grade rewrite of IRSB cluster (6 docs + corpus + 2 paperback PDFs) (818b9def)
- feat(content): academic-grade rewrite of wild ecosystem cluster (5 docs + shared corpus) (8c06302a)
- bd init: initialize beads issue tracking (ff7634e4)
- docs(CLAUDE.md): reflect in-repo blog pipeline layout (ba95f8ee)
- feat(skills): move blog pipeline in-repo — enforcement travels with the code (6ac16a49)
- feat(posts): add 2026-05-15 Tier 2 — deterministic-first LLM advisory CI (940916ce)
- feat(posts): add 2026-05-14 Tier 2 — self-improving skills schema cascade (b56d785a)
- feat(posts): add 2026-05-13 Tier 2 — transitive CVE dual-layer pattern (ad531463)
- feat(posts): add 2026-05-12 Tier 3 — three guards against shipping slop (310c1ca7)
- feat(posts): add 2026-05-11 Tier 2 — monitoring assumptions silently break under load (95fbd580)
- Merge remote-tracking branch 'origin/master' into redesign/dispatch-aesthetic (5300024a)
- fix(seo): emit rel=canonical from .Params.canonicalURL (9c49a0f5)
- docs(posts/agents-md): set Kobiton as canonical (rel=canonical mirror) (9b9226b9)
- feat(posts): add 2026-05-09 Tier 3 case study — spec graduation, engagement-architecture inversion (ac4f9569)
- content(about+research): refresh bio + repair dead post links (23b7eda9)
- feat(posts+features): launch Agent-Native Mobile Testing feature with Kobiton M2 Blog 1 (127356c4)
- feat(posts): add 2026-05-08 Tier 2 deep-dive — coherence as a deliverable on multi-surface engagements (0812c754)
- feat(posts): add 2026-05-07 Tier 3 case study — forge dogfood ships Grade-A Plane plugin, JRig loop closes (19e54815)
- feat(analytics): add Umami tracker for self-hosted analytics (9913112d)
- fix(subscribe): replace broken Netlify form with VPS forms-api proxy + Slack hook (b62d60d6)
- content(2026-05-06): Tier 3 case study — Guidewire MCP v0.1.0 → v0.1.1 in 76 minutes (3c400d34)
- ops(cron): add monthly retrospective cron + document autonomous pipeline (77de5342)
- content(monthly-recap): April 2026 retrospective (ff3a18da)
- feat(posts): add 2026-05-05 Tier 3 case study — Postgres ApprovalSink + 2 bugs (8a03c0ac)
- fix(list): use paginator slice + h1 title — drops /posts/ page weight 92% (51004ec7)
- fix(homepage): drop misleading "365 days/year" stat, replace with retrospective count (1e023969)
- content(contact): rewrite — fix stale references, tighten editorial tone (503bc273)
- content(about,projects): factual updates + recent project list (371343da)
- feat(design): full visual redesign — Dispatch aesthetic (b6288674)
- feat(posts): add 2026-05-04 Tier 3 case study — Guidewire MCP v0.1.0 ship (4717f906)
- feat(posts): add 2026-05-03 Tier 3 case study — anti-slop framework finds three bugs inside itself (114bc90a)
- feat(posts): add 2026-05-02 Tier 3 case study — four production deploy gotchas (9746d532)
- feat(posts): add 2026-05-01 Tier 3 case study — VPS-as-the-Home Day 1 (38c3bf29)
- feat(posts): add 2026-04-30 Tier 3 case study — propagation day (514d26bc)
- docs(posts): rebrand bounties → contributions in irsb post (8ac4d683)
- feat(posts): backfill 2026-04-23 through 2026-04-29 (6 posts) (929a7045)
- feat(posts): backfill 2026-04-19 through 2026-04-22 (9bdb08b6)
- chore(seo): apply SEO polish to braves-postgame Tier 2 post (9d37236c)
- feat(posts): add 2026-04-17 Tier 1 + 2026-04-18 Tier 2 (fc84a296)
- feat(posts): add collaboratively-shaped-roadmap case study (27b66cf0)
- feat: add AI code review blind test post (585b228a)
- chore: remove duplicate April 14-15 posts (a8501bde)
- feat: add blog posts for April 14-15 via full agent pipeline (9dfff63b)
- feat: add blog posts for April 14-15 (Tier 2 + Tier 3) + CLAUDE.md refresh (15b8eb75)
- chore(deps): bump actions/checkout from 4 to 6 (#5) (fd255911)
- build(deps): bump actions/setup-python from 5 to 6 (#3) (13632858)
- fix: expand QCSS research corpus post to full Tier 2 depth (d0d811e7)
- feat: add blog posts for April 10-13 (2 field notes, 2 deep-dives) (c2c40309)
- feat: add 6 monthly retrospectives (Oct 2025 - Mar 2026) (94090354)
- feat: backfill final 18 posts (Feb-Apr 2026) — gap fully closed (19bab589)
- feat: backfill 30 Jan 2026 posts with tier classification (d04f116e)
- feat: backfill 24 Dec 2025 posts with tier classification (733610ba)
- feat: backfill 16 Nov 2025 posts with tier classification (d0780efa)
- feat: backfill 6 Oct 2025 posts + fix consistency issues across all Tier 2 posts (8b694856)
- feat: add monthly-recaps section + backfill 5 Oct 2025 posts with tier classification (66e4e598)
- feat: apply tier classification system to Apr 6-8 posts (f5259d8d)
- feat: add blog posts for Apr 6-8 — knowledge OS epics, Braves polish, render/promote (66e75465)
- fix: add subscribe form success page — form POST was 404ing (a2d4148b)
- fix: expand legal toolkit and canary CI sections in Apr 5 post (d458849e)
- feat: add blog posts for Apr 3-5 — Braves dashboard refactor, v1.0.0 release, legal toolkit + epic planning (7b486780)
- fix: footer layout — stack subscribe above copyright, fix double-year bug (52a8330c)
- feat: add RSS subscribe link, Netlify signup form, and OG image (594906af)
- fix: fact-check corrections to supply chain security article (74162b9f)
- feat: add blog post — software supply chain security after axios (7cd1a7e0)
- fix: mobile overflow — constrain code blocks, tighten margins (78c6cdcb)
- fix: mobile rendering — stack TOC sidebar, fix table wrapping (6cefa7a9)
- feat: add blog post for 2026-03-28 — IntentCAD viewer DWG FastView parity (3b9045c3)
- docs: update CLAUDE.md with buildFuture requirement, date guidance, ecosystem pages (e0c48d82)
- fix: add --buildFuture to Netlify build for same-day posts (f8dc0b5d)
- fix: mobile rendering for grid layouts and tables, add ecosystem sections to homepage (757c192a)
- post: IRSB Ecosystem Deep Dive series (hub + 4 posts) (f1f02e17)
- feat: add 14 missing projects, update stale info, reorder newest first (e484ebbe)
- fix: add explicit slug fields to wild-deep-dive posts (939b77e2)
- feat: add blog posts for 2026-03-24 and 2026-03-25 (1e7af9d5)
- post: Wild Deep Dive Part 4 — Claude Code as Tech Lead (fc518436)
- post: Wild Deep Dive Part 3 — The Observability Loop (7ab56bad)
- post: Wild Deep Dive Part 2 — CLAUDE.md collaboration pattern (9e357094)
- post: Wild Deep Dive Part 1 — Safety Architecture (5a602a35)
- feat: replace stale IAMS section with Wild Ecosystem page (4de1f157)
- feat: add blog post for 2026-03-21 — nuclear option day validator rewrite 414 plugins (4304b190)
- feat(blog): add March 23 post — X Bug Triage Plugin zero to v0.4.3 (b324bd6e)
- feat: add blog post for 2026-03-22 — ninety skills three packs one day (77b3f5ca)
- feat: add blog post for 2026-03-20 — 58 E2E tests and slack channel launch (c3162f75)

---

# Release v0.12.0

**Release Date**: 2026-03-20

## Changes since v0.11.2

- chore: release v0.12.0 [skip ci] (fc84adaf)
- feat: add blog posts for 2026-03-14 through 03-18 (48eed589)
- feat: add blog posts for 2026-03-10 through 03-13 (cb70a504)
- feat: add blog posts for 2026-03-06 through 03-09 (8c900b72)
- feat: add blog posts for 2026-03-02 through 03-05 (3dda8a5b)
- feat: add blog posts for 2026-02-27, 02-28, 03-01 (4e31d7c6)
- feat: add blog post for 2026-02-26 — deterministic DXF comparison engine (c09e6a7f)

---

# Release v0.11.2

**Release Date**: 2026-02-26

## Changes since v0.11.1

- chore: release v0.11.2 [skip ci] (550c44fd)
- fix: use current date to avoid Hugo skipping future-dated post (f042c875)

---

# Release v0.11.1

**Release Date**: 2026-02-26

## Changes since v0.11.0

- chore: release v0.11.1 [skip ci] (a5d6d8a4)
- fix: convert front matter to TOML format for Hugo compatibility (13412053)

---

# Release v0.11.0

**Release Date**: 2026-02-26

## Changes since v0.10.0

- chore: release v0.11.0 [skip ci] (42b6ed8b)
- feat: add blog post - The Silent Killer: How Bare catch {} Blocks Hide Failures (452eabf1)

---

# Release v0.10.0

**Release Date**: 2026-02-23

## Changes since v0.9.0

- chore: release v0.10.0 [skip ci] (2f1ccd67)
- feat: add 8 blog posts covering Feb 4-22 work (255 commits, 12 projects) (85e0a6b9)
- docs: update CLAUDE.md with accurate deploy branch, architecture, and content details (3da78f0c)

---

# Release v0.9.0

**Release Date**: 2026-02-04

## Changes since v0.8.2

- chore: release v0.9.0 [skip ci] (6d72e4fc)
- feat: add blog post - Fixing Claude Code Hooks: The New Matcher Format (00d414cb)

---

# Release v0.8.2

**Release Date**: 2026-01-27

## Changes since v0.8.1

- chore: release v0.8.2 [skip ci] (a7377fd7)
- chore: clean up root directory clutter (3d687b17)

---

# Release v0.8.1

**Release Date**: 2026-01-27

## Changes since v0.8.0

- chore: release v0.8.1 [skip ci] (e9ab3eda)
- docs: streamline CLAUDE.md for clarity and accuracy (d3f6ff8d)

---

# Release v0.8.0

**Release Date**: 2026-01-04

## Changes since v0.7.0

- chore: release v0.8.0 [skip ci] (fbc2f0ef)
- feat: add blog post - Production Release Engineering v4.5.0 (e46709e0)

---

# Release v0.7.0

**Release Date**: 2026-01-03

## Changes since v0.6.0

- chore: release v0.7.0 [skip ci] (4f4b1932)
- feat: add blog post - Building External Plugin Sync (3a34f3e0)

---

# Release v0.6.0

**Release Date**: 2025-12-29

## Changes since v0.5.3

- chore: release v0.6.0 [skip ci] (4a601874)
- feat: add blog post - Building Post-Compaction Recovery for AI Agent Workflows with Beads (de6aeb36)

---

# Release v0.5.3

**Release Date**: 2025-12-20

## Changes since v0.5.2

- chore: release v0.5.3 [skip ci] (ad85fad8)
- docs: add Beads upgrade note (whats-new + hooks) (3504c4dc)
- chore: add Beads (bd) workflow + ignore beads source clone (59c4c447)

---

# Release v0.5.1

**Release Date**: 2025-12-12

## Changes since v0.5.0

- chore: release v0.5.1 [skip ci] (5a20d5de)
- Add: Python class identity mismatch CI debugging guide (da108834)

---

# Release v0.5.0

**Release Date**: 2025-12-11

## Changes since v0.4.0

- chore: release v0.5.0 [skip ci] (dedf9f62)
- feat: add blog post - How to Get ADK Agent into Google Community Showcase (5e6a8631)

---

# Release v0.4.0

**Release Date**: 2025-12-02

## Changes since v0.3.0

- chore: release v0.4.0 [skip ci] (38ebd19e)
- Merge remote-tracking branch 'origin/master' (59fff928)
- feat: add blog post - Implementing Brand Consistency with CSS Variables (bce884ad)

---

# Release v0.3.0

**Release Date**: 2025-11-18

## Changes since v0.2.0

- chore: release v0.3.0 [skip ci] (f14de8d6)
- feat: add blog post - Building an Idempotent Stripe Billing Enforcement Engine for Firestore (e9f95986)

---

# Release v0.2.0

**Release Date**: 2025-11-09

## Changes since v0.1.1

- chore: release v0.2.0 [skip ci] (d15d8943)
- feat: add blog post - Fine-Tuning IAM1: Building a Hierarchical Multi-Agent System on Vertex AI (a6050be2)

---

# Release v0.1.1

**Release Date**: 2025-11-02

## Changes since v0.1.0

- chore: release v0.1.1 [skip ci] (c96479a2)
- refactor: rename iaems to iams directory structure (4d34d6cf)

---

# Release v0.1.0

**Release Date**: 2025-10-30

## Changes since v0.0.1

- chore: release v0.1.0 [skip ci] (06cbd08e)
- feat: add BrightStream multi-agent platform case study (dc9bec17)

---

# Release v0.0.1

**Release Date**: 2025-10-30

## Changes since v0.0.0

- chore: release v0.0.1 [skip ci] (2d04f117)
- fix: handle missing previous tag in changelog generation (6082f214)
- fix: add NEO and PokeeResearch posts to research landing page (af32000f)
- chore: force Netlify rebuild for research posts (effb5c64)
- feat: add blog post - Building Production Multi-Agent AI: BrightStream on Vertex AI (eefbd5cd)
- Add Foundation section and first converted doc (db22a9e5)
- Add IAEMS documentation workspace (b445a159)
- fix: move research posts to content/research/ directory (782dac1b)
- feat: add comprehensive NEO vision-language model guide (8c4b2d67)
- feat: add PokeeResearch-7B analysis - RLAIF training without K annotations (3638bd3c)
- fix: correct URL for Coasean Singularity article (cc5d6d11)
- feat: add NBER Coasean Singularity research analysis (b9fd46d4)
- fix: remove 11 duplicate posts, keep most technical versions (0ace7cc8)
- fix: remove ALL truncated RSS-synced posts, keep only comprehensive archive versions (e20c6a8b)
- docs: update content audit with restoration results (6a87a0c5)
- fix: disable automatic RSS sync to prevent content overwriting (9fce5b4d)
- fix: restore comprehensive content from archive (RSS sync overwrote posts) (1e0846e6)
- fix: remove 9 duplicate posts (48d68dbb)
- chore(sync): import Start AI Tools posts (6bb6d98a)
- feat: restore comprehensive content from jeremylongshore.com + fix research page links (f11620f3)
- feat: restore comprehensive content to 30+ blog posts from archive (e53c4042)
- fix: repair 3 broken links on research page (2725a79b)
- feat: add hustlestats.io links to Hustle project (89923ae6)
- fix: remove duplicate posts with truncated filenames (1c01276e)
- fix: remove duplicate portfolio post and false revenue claims (4ec61aae)
- feat: add blog post - Fixing Claude Code EACCES Multi-User Linux Permissions🤖 Generated with [Claude Code](https://claude.com/claude-code)Co-Authored-By: Claude <noreply@anthropic.com> (5dd1cc8c)
- chore(sync): import Start AI Tools posts (195311c7)
- fix: remove all non-English MCP translations - MASSIVE SEO improvement (5beafd5a)
- fix: resolve Google Search Console indexing issues (partial fix) (aac10337)
- chore(sync): import Start AI Tools posts (ec4ec303)
- feat: add blog post - Intent Solutions Portfolio 2025: Five Production Platforms and 4-Day Deployment Architecture (e74ebdc8)
- feat: add blog post - Building a Better PubMed Research Tool: 10 MCP Tools, Zero Compromises (78618dbf)
- feat: publish scaling AI batch processing blog post (566b42e8)
- chore(sync): import Start AI Tools posts (cdefab17)
- fix: repair broken internal links and remove invalid external link (e5b9a496)
- style: add spacing between list items in research and curriculum page (241a6ef0)
- feat: rebrand about page to focus on Intent Solutions company (b5b69796)
- feat: update projects page with current focus and remove revenue claims (780c9196)
- fix: remove duplicate posts and add spacing between post items (20a4b319)
- style: reduce link underline thickness from 3px to 1px (ac0739cb)
- fix: update date to CDT timezone to fix future-date issue (ad6e4e73)
- fix: correct publish date to avoid future-date issue (bf421c95)
- feat: add blog post - Scaling AI Batch Processing with Vertex AI Gemini (061217de)
- chore(sync): import Start AI Tools posts (14330d40)
- chore(sync): import Start AI Tools posts (f2f0b57f)
- feat: add blog post - Debugging a Critical Marketplace Schema Validation Failure (38996292)
- fix(workflows): resolve permissions and YAML syntax errors (998d6c03)
- feat: add comprehensive CLAUDE.md and NLWeb research article (897e943d)
- feat: add blog post - Debugging Slack Integration: 6 Duplicate Responses Fix (2430c3f8)
- feat: add Playwright testing suite implementation guide (777cb17c)
- feat: add blog post - Applying Universal Directory Standards to Prompt Repository (d0c0d51b)
- feat: add blog post - Making a Youth Sports App COPPA-Compliant: The Real Process (45f06faa)
- chore: enable automatic releases on every push (43622c8b)
- chore: add global release workflow (e26bf29a)
- fix: Make curriculum module links functional and remove duplicate titles (ee4d9fc3)
- fix: Enable content rendering for MCP and TRM curriculum sections (fd6dd891)
- feat: Add Samsung Tiny Recursive Models research to StartAITools (cb4b1886)
- feat: Add Microsoft MCP for Beginners curriculum to StartAITools (d0bd7836)
- feat: Content nuke - From GitHub Repos to Published Education (cd319352)
- feat: Add comprehensive Hybrid AI Stack and Terraform educational guides (cc30ac12)
- fix: Rebrand homepage as educational platform, not commercial site (1a0e7e05)
- feat: Rebrand homepage as 'Start AI Tools by Intent Solutions' (a0dfa57a)
- fix: Force Netlify cache bust for homepage - timestamp 2025-10-07 20:52 (dbf6cec4)
- fix: Add cache control headers to prevent CDN caching issues (cf38b71f)
- feat: Complete projects page overhaul (c2bd5d26)
- feat: Update branding and fix research page links (96aa8c57)
- feat: add blog post - Self-Hosting n8n on Contabo VPS: Enterprise Automation for $0/Month (8055b2a8)
- chore: cleanup and add new blog post (b7f39228)
- fix: remove markdown # symbols and incorrect dates from headers (ad12d6e0)
- feat: add blog post - GitHub Release Workflow: When Yesterday's Updates Aren't Public (bf55ed79)
- fix: restore missing Research and Projects pages and menu items (691506a1)
- feat: add blog post - Debugging Claude Code Slash Commands: When Your Blog Automation Silently Fails (e62056f6)
- feat: add blog post - Repository Transformation: From Chaos to Professional Prompt Engineering Toolkit (f0f97945)
- fix: cleanup StartAITools - remove duplicate theme, cache issues, and unnecessary directories (aec8f988)
- feat: add blog post - DevOps Onboarding at Scale: Creating Comprehensive System Analysis with Universal Templates (c615e692)
- feat: Enterprise Documentation Transformation - Git-Native TaskWarrior Workflows (3f76cc77)
- 🚀 ADD: AI-Assisted Technical Writing Automation Workflows Guide (9f8033b1)
- fix: resolve timezone issue preventing Waygate MCP post from displaying (ed7d77e7)
- fix: restore correct Archie theme and StartAITools configuration (7195274e)
- fix: remove broken archie theme submodule and restore hugo-bearblog theme (16e7b995)
- fix: correct netlify.toml redirects from jeremylongshore.com to startaitools.com (7b898b3b)
- feat: add Waygate MCP v2.1.0 forensic analysis technical deep-dive (1e36fad5)
- feat: add blog post - Building AI-Friendly Codebase Documentation: A Real-Time CLAUDE.md Creation Journey (a156ba69)
- force: clear Netlify cache - add --ignoreCache flag to build command (d03c53c9)
- feat: add 3 blog posts from jeremylongshore - security audit, N8N transformation, and debugging journey (69cd4bee)
- feat: add enterprise MCP security architecture blog post (f7ccc96a)
- fix: force Netlify cache clear - switch to Bear theme (ed988dd9)
- feat: add 4-part AI-Dev Transformation blog series (b90c4b0f)
- chore: remove Hermit v2 theme completely - Bear migration complete (10bd2b2c)
- fix: complete Bear theme configuration with proper params and markup settings (8b4c1a11)
- fix: force clean build with --cleanDestinationDir to clear Netlify cache (75a182bc)
- chore: trigger Netlify rebuild with cache clear (5f41b3c8)
- Build: pin Hugo v0.150.0, optimize Netlify build with --gc --minify (d970d773)
- Optimize Bear theme: move config to _default dir, fix pagination deprecation warning (4efa3ada)
- remove: delete incorrect medical DiagnosticPro post (e849a8cb)
- chore: clean up Hugo build cache and resources (d10f9cb6)
- Merge pull request #1 from jeremylongshore/feat/bearblog-startai (20c07d73)
- feat: switch to hugo-bearblog and import Start AI Tools posts with auto-sync (643d9f3a)
- Add comprehensive Ubuntu development journey timeline post (5df5e42a)
- Add blog post about AI documentation toolkit journey (65616696)
- Remove redundant GitHub Actions workflow - Netlify handles auto-deployment (b9b0ba3a)
- Add complete GitHub repository configuration and automation (eb28a5d8)
- Enhanced repository with professional documentation and Start AI Tools integration (3ec91d0a)
- Correct blog post: market research not personal challenges (55bdd5b8)
- Add marketing automation project pricing exploration post (083bccb1)
- Fix blog post date - was in future preventing Hugo build (23f8f565)
- Add DiagnosticPro feature rollouts blog post and update CLAUDE.md (367273e5)
- Add new blog post (da57bca2)
- Fix Netlify build error - remove startaitools submodule (d051ef46)
- Rebalance portfolio content - reduce data obsession, add automation focus (30d4fb75)
- Transform blog into professional portfolio/resume site (3f8b84b5)
- Major cleanup: Remove public from tracking, add gitignore, remove old theme assets (62e6c4a4)
- Change site title back to Jeremy Longshore (ff80bcbc)
- Switch theme from Hugo Noir to Hermit-V2 for better readability (7c0bf3fb)
- Fix: Add custom CSS to ensure text is visible in light mode (4aa2de70)
- Fix: Complete content formatting overhaul - professional markdown for all pages and blog posts (e1e69340)
- Merge ; commit '05d0da0dda598ddb3f9a4236a2c65d64646ad559' (f41a7956)
- Update Format MD on About me Page (fc6bff0c)
- CRITICAL FIX: Use exact markdown formatting provided for About page (05d0da0d)
- Force rebuild: Add timezone to trigger Netlify deploy (35e14a89)
- Fix: Add proper spacing between headers and links in Contact page, create Experience and Projects pages (8c44df06)
- Update: Professional Contact page formatting with sections and emojis (87387f94)
- Perfect: Implement professional About page design with proper hierarchy and formatting (09656934)
- Enhance: Professional formatting for About page with better spacing and structure (03bb6f01)
- Fix: Update About page content, remove duplicate heading, change footer to LinkedIn (83d77ede)
- Enhance: Expand bio description and add website preview images for projects (86032f8e)
- Force rebuild: Add NODE_VERSION to trigger fresh Netlify deploy (b0ba912d)
- Fix: Change Start AI Tools project box to link to intentsolutions.io (875a4ed6)
- Change portfolio link from jeremylongshore.com to intentsolutions.io (98d6d2a8)
- Change site title from Jeremy Longshore to Intent Solutions Inc (fb18ddd4)
- Fix: Add description field in params - theme uses this for tagline display (2cb1bab1)
- Fix: Add tagline display and restore Projects page with external links (4f3b710f)
- Replace Projects menu with direct links to DiagnosticPro and Intent Solutions (2f3e19d4)
- Update tagline: Speed DevOps | AI Specialist | Deploy in days (86be54ca)
- Fix: Add bio field for subtitle display (950380f5)
- Fix: Add correct netlify.toml to override npm build command (f09e7e70)
- Add README with Netlify deployment badge (ff040b3b)
- Hugo site with Noir theme ready for deployment - AI Development Specialist portfolio (9cc3f7d2)
- first post (1d920bcd)
- Fix: Add PaperMod as proper submodule (ddb7b949)
- Initial blog setup (2885d01c)
