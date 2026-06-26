+++
title = 'A Second Brain You Can Audit Beats One You Must Trust'
slug = 'governed-second-brain-local-first-mcp'
date = 2026-06-16T08:00:00-05:00
draft = false
tags = ["mcp", "ai-engineering", "local-first", "rag", "provenance"]
categories = ["AI Engineering"]
description = "A second brain you can audit beats one you must trust. Local-first, daemon-free, no-egress by default, and an external anchor that detects a silent rewrite."
+++

Most "second brain" products ask for the same thing in the end-user license agreement: trust us. Trust that your notes stay where you put them. Trust that the model only saw what we told you it saw. Trust that the record we keep is the record that happened. None of those are verifiable from the outside — they're promises, backed by a privacy policy and a logo.

The Governed Second Brain plugin shipped this day inverts that contract. It's a local-first, in-process MCP server — read and write, daemon-free — that you install over a folder of your own files and query inside Claude Code.

The whole design is organized around one substitution: replace *trust me* with *check it yourself*. Where a hosted RAG product would say "your data is safe," this says "here is the command that proves what ran, what left, what changed, and what you installed." Four audit questions, four design choices. This post is about why each one is structural and not a feature you could bolt onto a trust-me product after the fact.

## The problem: governed knowledge can't run on faith

Retrieval over a personal or team knowledge base is a solved demo and an unsolved product. The demo is easy: embed some documents, do nearest-neighbor search, stuff the hits into a prompt. The product is hard because the moment the knowledge is *governed* — client material under contract, regulated data, an institutional memory other people rely on — the interesting questions stop being about retrieval quality and start being about provenance.

Second brains attract the trust-me default more than almost any other category, and the reason is a mismatch. The data is the most sensitive a person owns — private notes, half-formed ideas, client material under NDA — while the architecture most products wrap around it is the most opaque: a hosted index, a sync loop, an embedding API, all behind a dashboard. You are asked to put your most guarded material into the system you can see the least of. That trade is fine for a to-do list and unacceptable for governed knowledge.

Three of the questions that follow have no good answer in a hosted, trust-me architecture:

- **What actually ran against my files?** A cloud service runs code you can't see on data you can't withhold. "Local-first" in marketing copy frequently means "we cache locally and sync everything anyway."
- **What left the machine?** RAG pipelines egress document text to an embedding or completion API by default. The user usually finds out which bytes left by reading a SOC 2 report, not by reading their own logs.
- **Did my record of what happened get quietly rewritten?** This is the subtle one. A knowledge store accumulates a history — what was promoted, transitioned, superseded. If that history can be edited after the fact and nobody can tell, then "audit trail" is a decoration.

These three plus a fourth — what did I install — are the questions a governed knowledge store has to answer to be worth governing. The rest of this post is the four answers, each a design choice rather than a disclosure.

The plugin's umbrella repo got renamed this day from *Compile-Then-Govern* to **Governed Second Brain** with an explicit commit note: "Apache-2.0, honest audit claim." That second clause is the thesis in three words. The rename forced the README to stop overstating what the audit does and start stating exactly what it does — because the previous claim turned out to be falsifiable, and an audit feature you can falsify is worse than none.

## Choice 1 — local-first and daemon-free: you can see what runs

The plugin is an in-process MCP server. There is no background daemon, no `:3847` HTTP service to keep alive, no separate process holding your data open. The earlier incarnation of this system split the write path across a long-running curator daemon; folding it in-process removed a whole class of "is the service up, is it the right version, what is it doing while idle" questions.

The full loop runs in one process: capture a fact, govern it through dedupe and policy, promote it, write the hash-chained audit entry, export, index, and answer a query with a `qmd://` citation pointing back at the source. That entire path — capture → govern → promote → audit → index → cited search — executes against local SQLite and a local vector index with no service in the middle. The verification criterion for the first phase was exactly this loop returning a cited hit from local data, with the audit chain verifying intact afterward. No daemon ran; nothing was waiting in the background to be trusted.

Daemon-free is an auditability choice before it's an operability one. A background service is a thing that runs when you aren't looking. An in-process tool runs only when a tool call invokes it, inside a session you initiated, and stops when the call returns. The surface you have to reason about is the tool list, not a process tree. "What runs against my files" collapses to "what tools did this session call" — which is a question the transcript already answers, without you having to take anyone's word for it.

This is the difference between "local-first" as an architecture and "local-first" as a marketing word. Plenty of products that wear the label cache locally and sync everything to a server anyway; the local copy is a convenience, not a boundary. Here the local copy *is* the system — there is no server-side index to drift out of sync with, because there is no server. The data plane and the trust plane are the same machine.

## Choice 2 — no egress by default: you can see what leaves

Building the brain has two modes, and the default is the conservative one:

```bash
# Build a governed brain from a folder — zero LLM egress.
npx governed-second-brain init ./notes --index-only

# Opt into the full compile (document text egresses to the model).
npx governed-second-brain init ./notes        # pre-flight consent first
```

`init <folder> --index-only` builds the entire brain — index, governance, cited retrieval — with **zero egress**. No document text leaves the machine; the index is built locally and queries resolve locally. This is the mode for regulated or client data, and it is the default precisely so that "local-first" cannot quietly imply "nothing leaves" while a compile step ships your files to an API behind your back.

The richer mode is the full ICO (Intentional Cognition OS) compile, which runs on DeepSeek as an opt-in egress path. That mode genuinely sends document text to a model — and the design's honesty rule is that this fact is loud, not buried. The egress mode is gated behind a pre-flight consent step that names what it does on the tin: it reads every file under the target folder, runs local tooling, and — in this mode only — sends document text to the model. Consent is a step you pass through, not a flag you forget you set.

This is also why the default is index-only rather than full-compile. Defaults are the decisions users don't make, so the default has to be the one that's safe to not think about. The README is correspondingly forbidden from letting "local-first" do the work of implying "air-gapped." Two modes, one honest sentence each: index-only sends nothing; full-compile sends document text to the model, and asks first.

The pre-flight summary is itself an auditable artifact. It is a printed contract — these are the files I will read, these are the tools I will run, this is what I will send and to whom — presented before you approve, not logged after you've already lost the choice. A consent screen you can't decline is a notification; a consent screen that gates the action is a decision point. This one gates.

The point isn't that egress is bad. It's that egress should be a decision the user makes with the facts in front of them, not a default they discover later in someone else's compliance document. Auditability of *what leaves* means the answer is knowable before the bytes move, not reconstructable after.

## Choice 3 — the external audit-chain anchor: you can see what changed

This is the design choice that earned the "honest audit claim" rebrand, because the original claim was wrong in an instructive way.

The knowledge store keeps a hash-chained audit log: every governance event (a memory promoted, transitioned, superseded) is an entry whose hash folds in the hash of the previous entry. The intuition is the familiar one — change any record and the chain breaks, so the log is tamper-evident. That intuition is half right, and the missing half is the whole problem:

```text
# Illustrative — what a self-contained hash chain does and does not catch.
chain:  e0 → e1 → e2 → e3      entry_hash = H(row || prev_entry_hash)

# Edit e1 in place but DON'T re-hash e2, e3  →  chain breaks  →  caught. Good.
# Silently REWRITE the whole chain (recompute every hash)    →  internally
#   consistent again  →  self-verify still passes.            →  NOT caught.
```

A self-contained chain only proves *internal* consistency. It catches a sloppy edit that doesn't recompute everything downstream. It does **not** catch a wholesale rewrite, because a rewrite recomputes every hash and produces a new chain that is perfectly consistent with itself. A local writer can throw away the history, fabricate a clean replacement, and `verify` returns green. Calling that "tamper-proof" was the overstatement the rebrand corrected; the accurate word is tamper-*detection*, and only against in-place edits.

The external anchor closes the rewrite gap. The mechanism is two commits working as a pair: **`govern` commits the chain head to an external anchor log**, and **`brain_audit_verify` checks the live chain head against that anchored value.** The companion store change in `qmd-team-intent-kb` is described exactly this way — "external anchor log for the audit chain (detect silent full rewrites)."

```text
# Illustrative — the anchor is an outside witness to the chain head.
govern:               anchor.log  ←  head_hash(e3) = "9f66…"   (committed externally)
brain_audit_verify:   live_head == anchored_head ?  intact  :  SILENT REWRITE DETECTED
```

A wholesale rewrite is internally consistent, but it produces a *different head hash* than the one already committed to the anchor. The anchor is an outside witness: it remembers what the head was, so a fresh chain that disagrees with it is caught even though the fresh chain agrees with itself.

The trust model then gets stated honestly per mode rather than as one blanket claim. A local single-writer install gets integrity, ordering, and rewrite-detection — that is genuinely what the chain plus anchor deliver, and it's a real guarantee worth having. Non-repudiation across multiple distrusting actors is a different, stronger property that needs keyed signatures and a tamper-resistant anchor, and the local mode does not pretend to it. Stating the weaker-but-true claim for the common case, and naming where the stronger claim would require more machinery, is the honesty the rebrand was about. The forbidden-words list is short and deliberate: tamper-proof, immutable, blockchain. The feature is real; the claim is now sized to it.

## Choice 4 — reproducible, provenanced install: you can see what you installed

Auditability that stops at runtime leaves the biggest hole open: the install itself. A second brain you can audit, delivered by a supply chain you can't, is still trust-me — you've just moved the trust from the data plane to the package manager.

So the install is pinned and provenanced end to end:

- **`gsb.lock.json`** pins the exact version tuple — the plugin runtime, the ICO compiler, and qmd (pinned to the canonical `2.5.3`). The spool contract between compile and govern is a versioned wire format, so the lockfile owns a single known-good combination rather than letting three components drift independently.
- **A hermetic full-chain CI smoke** runs the entire capture-to-cited-search loop against that pinned tuple before any release, with a real corpus and a real audit verify. The reproducible build is *tested as a whole*, not asserted component by component.
- **npm provenance** is generated by the CI release workflow, so the published package carries a verifiable link back to the commit and workflow that built it.
- **The package ships only `plugin-runtime/governed-brain.cjs`**, not a vendored `node_modules`. A stripped, self-contained runtime artifact is one file you can inspect, not a dependency forest you have to take on faith. (An early publish accidentally externalized dependencies that weren't bundled — an inert package — which is exactly the failure a single self-contained artifact prevents.)

The tuple matters more than a normal lockfile because the three components talk to each other over a versioned wire format. The compile stage produces a spool that the govern stage consumes; that spool contract can change shape between versions. Pinning the plugin runtime, the compiler, and qmd as a single tuple — rather than letting each float to its own latest — is what keeps the contract coherent. The lockfile owns a combination that was proven to work together, not three independently-blessed versions that happen to be installed at the same time.

These read like packaging chores. They're the fourth audit axis. "What did I install" has a verifiable answer — a provenanced package, a pinned tuple, one inspectable runtime file, a CI smoke that proves the whole chain works at those versions — instead of "whatever npm resolved today."

## The result

By end of day the plugin was live as `npx governed-second-brain init`, version strings aligned at `0.1.4` (a finding the `validate-plugin` gate surfaced), the MCP server auto-registering with Claude Code so a fresh install can `/brain "..."` against its own data without manual config. The umbrella repo carries the productization epic and its phased child work; the audit-chain anchor moved from "on the roadmap" to "implemented" in the same pass that shipped it.

The auto-registration is a small thing that matters for the thesis. The installer doesn't hand you a block of `.mcp.json` to paste and hope you got right — it registers the server with Claude Code itself, prints a first `/brain` query and a capture example, and the loop is live. An honest, checkable system that's also annoying to wire up loses to a trust-me product that just works; closing the setup gap is what lets the auditable option win on convenience too, not only on principle.

The honest summary is the four audit questions, each with a command behind it rather than a promise:

| Audit question | Design choice | How you check it |
|---|---|---|
| What runs against my files? | Local-first, daemon-free in-process MCP | The session transcript — no background process |
| What leaves the machine? | No-egress `--index-only` default; opt-in compile with consent | The mode you chose, stated before bytes move |
| Did my history get rewritten? | External audit-chain anchor | `brain_audit_verify` vs. the committed head |
| What did I install? | `gsb.lock.json` pin + npm provenance + single `.cjs` | The lockfile, the provenance, one inspectable file |

## The principle: replace the promise with the command

Strip away the specifics and the design is one move applied four times. Every place a hosted product would hand you a promise, this hands you a command.

"Your data stays local" is a promise. "There is no daemon and the loop runs in-process" is a fact you can confirm from the tool list. "We only access what you authorize" is a promise. "Index-only egresses nothing; the other mode asks first" is a behavior you can observe before any bytes move. "We keep an immutable audit log" is a promise — and, as it turned out, a falsifiable one. "`brain_audit_verify` checks the live chain head against an externally committed anchor" is a command that returns a verdict. "Our package is trustworthy" is a promise. "Here is the provenance, the pinned tuple, and the one file we ship" is a manifest you can read.

The pattern generalizes past second brains. Any system that touches data you don't fully control faces the same fork: it can ask you to trust an unobservable property, or it can expose an artifact that makes the property checkable. The first is cheaper to build and ages into a liability the day someone asks you to prove it. The second costs more up front — an anchor log, a consent gate, a lockfile, a provenance step — and the cost buys you a claim that survives scrutiny.

The discipline that made this honest was the willingness to *shrink* a claim to fit its mechanism. The original "tamper-proof" language was aspirational; the mechanism underneath only delivered tamper-detection, and only against careless edits. Rather than build toward the bigger claim or quietly keep the wrong word, the rebrand sized the words to the substrate — tamper-detection where the chain earns it, rewrite-detection where the anchor earns it, and a short list of words the system is forbidden from using because it hasn't earned them. A claim you can defend is worth more than a claim that sounds better, and the gap between the two is exactly where trust-me products live.

## Tradeoffs

None of this is free, and the costs are worth naming. The external anchor adds a write on every govern and a check on every verify — cheap, but it means the anchor log is now load-bearing state the system has to keep somewhere durable. And it raises an honest recursion: where do you anchor the anchor? An anchor log that lives next to the chain it witnesses is no witness at all — a rewriter who can touch one can touch both. The substrate that makes it real is an external, append-only, shared history that the local writer doesn't unilaterally control — committing the head into git history is the cheap version, a timestamping service the stronger one. The anchor is only as trustworthy as the place it's committed to, and naming that ceiling is part of the honest claim.

Index-only mode trades retrieval richness for zero egress; the fuller compile is genuinely better at some queries, which is why it exists, which is why the consent prompt has to be honest rather than discouraging. The in-process design has its own ceiling: there's no shared service, so a brain that a whole team queries at once wants the hosted path — and that path is deliberately out of scope here, a client opt-in rather than the default, because hosting reintroduces exactly the trust surface this version removed. A single pinned tuple in `gsb.lock.json` buys reproducibility at the cost of staleness — the known-good combination is known-good until a security fix lands upstream and the pin has to move deliberately. Each trade leans the same direction: a little more ceremony in exchange for a claim you can actually back.

## Also shipped

**contributing-clanker** cut its v0.2.0 release with new contribution-quality gates and a versioned product-landing README. **intent-outreach** got a ground-up rebuild — provider-pluggable LLM seam, a deterministic pipeline behind an MCP server, the GCP stack retired — and reached marketplace grade B on `validate-skillmd`. Both are their own posts; here they're context for a busy day whose lead story was making a knowledge store you can check instead of one you have to believe.

---

**Related posts:**

- [MCP Server Auth: The API Is the Real Boundary](/posts/the-api-is-the-real-boundary/) — the same knowledge system, and why the governance audit trail must stay pure for verification to mean anything.
- [Governed Knowledge: Two Releases, a Freshness Daemon, and Export Gating](/posts/governed-knowledge-two-releases-freshness-daemon/) — earlier groundwork on governing a knowledge corpus rather than just retrieving from it.
- [Green CI Proves Nothing: Why Your Tests Gate Zero Calls](/posts/when-green-ci-proves-nothing/) — the same instinct applied to tests: a green check that verifies nothing is worse than no check.
