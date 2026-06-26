+++
title = 'The Merge Is the Trust Boundary: Re-Derive as Untrusted'
slug = 'govern-at-merge-untrusted-union'
date = 2026-06-20T08:00:00-05:00
draft = false
tags = ["distributed-systems", "audit", "cryptography", "knowledge-base", "merge"]
categories = ["Architecture"]
description = "In a multi-writer knowledge store the merge is the trust boundary: re-derive the union as untrusted, re-govern from scratch, and anchor it with a signed DAG."
+++

A single-writer knowledge store with a hash-chained audit log has a clean story: every governance event folds the previous entry's hash into its own, so an in-place edit breaks the chain and `verify` catches it. That story holds right up to the moment a second writer appears.

The instant two clones of the same store can each promote facts independently and later reconcile, the audit chain stops being a single line. Clone A has a chain that verifies clean against itself. Clone B has a chain that verifies clean against itself. Merge them, and you have a question neither green checkmark answers: **is the union governed?**

This post is about the EPIC 1 work in `qmd-team-intent-kb` that took the position that it is not — and that the only honest fix is to treat the merge itself as the trust boundary, re-derive the union as untrusted, and re-govern it from scratch. The thesis underneath is one sentence: in a multi-writer knowledge store, the merge is where trust has to be rebuilt, because it is the one place trust cannot be inherited.

## The problem: audit chains don't compose across a merge

The seductive assumption is that two trustworthy halves make a trustworthy whole. A clone's chain verified; the other clone's chain verified; surely their union is fine. Two independent failures kill that.

**Failure one: a content-level merge runs no policy.** The decisive finding came from a throwaway spike against Dolt's native three-way merge. The spike fed two branches into Dolt's row-union and watched a *secret-bearing row* — one that a governance gate would have rejected — land in the merged database with zero governance applied.

The union operator reconciles rows; it does not re-run your disclosure checks, your dedupe, your tenancy rules. Version control is not governance. Anything either branch promoted (or had slip past a weaker gate) rides into the merged state unchecked, because the merge operator has no concept of a policy to enforce. This is not a Dolt defect — it is true of every content-level merge operator, which is exactly why the fix has to live above the substrate rather than inside it.

**Failure two: the linear verifier breaks at the seam — for an innocent reason.** The store's audit verifier is a linear walker: it sorts rows by `(timestamp ASC, id ASC)` and asserts each row's `prev_entry_hash` matches its predecessor. That contract is exactly right for one clone's own history and exactly wrong for a merge.

```text
# Illustrative — why a linear walk fires a FALSE break at a merge seam.
clone A chain (its wallclock):   a0 → a1 → a2
clone B chain (its wallclock):   b0 → b1
merged, sorted by timestamp:     a0  b0  a1  b1  a2     # interleaved by wallclock
linear walk: a1.prev_entry_hash == a0  but predecessor is now b0  →  PREV_LINK_MISMATCH
```

Two clones evolve on independent wallclocks; concatenating their chains by timestamp interleaves rows that never linked to each other, and the walker fires `PREV_LINK_MISMATCH` at the boundary. So the naive merge produces a chain that *looks* tampered even when nobody tampered — which means a real tamper at the seam would be indistinguishable from the normal noise of merging. A verifier that cries wolf at every merge can't be trusted to catch a wolf.

Put together: the merge admits ungoverned data *and* destroys the signal that would tell you. You cannot patch this by trusting either input chain harder. The trust has to be rebuilt at the merge, not inherited through it.

## The design: re-derive the union as untrusted

The move is to stop treating a row that crossed a clone boundary as "already governed." At merge time the gate (`mergeGovern`) takes the union of both clones' promoted rows and re-runs every one of them through the *same* front-door governance it would apply to a brand-new capture — as if none had ever been trusted.

```text
# Illustrative — the merge gate, in five moves.
union = dedupe_by_content_id(cloneA.promoted ++ cloneB.promoted)
union = sort_by_content_id(union)              # makes A∪B and B∪A byte-identical
for index, row in enumerate(union):
    cand = project_to_untrusted(row)           # strip governance metadata; trustLevel = untrusted
    if not disclosure_clean(cand):  quarantine(row); continue   # fail-closed secret/PII choke point
    if not policy_pipeline(cand):   quarantine(row); continue   # dedupe, sensitivity, tenancy, ...
    promote(cand, clock = merge_clock(index))  # canonical promotion path, deterministic timestamp
```

The load-bearing detail is `project_to_untrusted`. A promoted row carries governance metadata — its lifecycle, its prior policy evaluations, its `trustLevel`. The gate strips all of that, keeps only the source content and provenance, and forces `trustLevel = untrusted`, so the `source_trust` rule evaluates the row as if it had no standing. The merge trusts *nothing* that came across a boundary. Survivors get promoted through the canonical path; a secret that rode in on a clone is quarantined, never written. The merged state is, by construction, indistinguishable from one assembled by feeding every row through the front door one at a time.

Quarantine has its own non-leak contract, and it matters more than it looks. A rejected row is recorded as a `QuarantinedRow` carrying the offending memory's content-derived id, a category (`disclosure` or `policy`), and a human-readable reason — the disclosure category, or the id of the rule that rejected it. What it never carries is the matched secret or PII value.

The whole point of the disclosure choke point is to keep secrets out of the governed store; a quarantine record that quoted the secret back in its `reason` field would re-leak exactly what it just blocked, into the very audit trail meant to be safe to share. So the gate reports *that* a row was turned away and *why category*, never *what* the offending value was. Refusing to leak on the rejection path is as much a part of the design as refusing to admit on the success path.

The gate also fails loud, and atomically, on a row it cannot reason about. Before any promotion runs, it pre-passes the entire union and checks that every row's id reproduces under re-derivation — that `id == deriveMemoryId(candidateId, contentHash)`. A row whose id does *not* reproduce did not come from the canonical promotion path; it carries a stray, non-content-derived id (a `crypto.randomUUID()` v4 from some out-of-band code path), and that id is poison: it would survive de-dup as its own twin and sort to a per-clone position, breaking both de-dup and commutativity.

Rather than corrupt the merge quietly, the gate throws at entry — before a single row is written — so one bad row aborts the whole merge instead of silently skewing it. Walking the already-sorted union makes the first reported offender deterministic across clones, too: even the *failure* is reproducible. The error carries the offending id and the id it should have been — both already-public identifiers — but never the row's content, the same non-leak discipline the quarantine path follows.

Critically, the gate invents no new governance primitive. It re-runs the existing disclosure choke point and the existing policy pipeline. That is a deliberate honesty constraint, and it sets a ceiling I'll name later: re-governing the union is exactly as strong as the governance you already had, and not one bit stronger.

That "front door" is itself worth a sentence, because it's what makes re-running it meaningful. The same day this merge gate landed, the store's EPIC 0 hardening put real teeth on the intake path: a fail-closed PII/secret/comp choke point at `CandidateRepository.insert()` that rejects on detection rather than flagging-and-continuing, token-bound tenancy so a row can't claim a tenant its caller isn't scoped to, and token hashing plus revocation so a leaked credential can be killed.

The merge gate's whole value proposition — "re-derive the union through the front door" — only pays off because the front door is fail-closed. Re-running a permissive gate over the union would launder bad rows, not catch them. The order of operations matters: harden intake first (EPIC 0), then point the merge at it (EPIC 1).

### Why content-derived ids make the re-derivation reproducible

Re-running policy is necessary but not sufficient. For the result to mean anything across clones, two clones re-deriving the *same* union have to land on the *same* answer — same ids, same hashes, same verdict. That reproducibility is bought by three deterministic choices.

**Content-derived UUID v5.** Every memory and audit-event id is derived from its content (`deriveMemoryId(candidateId, contentHash)`) under a locked namespace, not minted from `crypto.randomUUID()`. So the same logical memory produces the *same* id in every clone. That makes the union's de-dup a real set operation — two clones holding the same fact collapse to one row — and it makes a sort-by-id traversal deterministic. The gate even refuses, loudly, any row whose id does not reproduce under re-derivation: a stray v4 id would survive de-dup twice and sort to a per-clone position, so the gate aborts the whole merge atomically rather than corrupt it silently.

**An entry hash that excludes the wallclock.** The audit chain's `entry_hash` was split into versions: v2 canonicalizes the row body *without* its `timestamp`, so the same logical event hashes identically no matter when each clone happened to write it. (v1 rows are deliberately frozen, never rehashed — their original hashes are their tamper-evidence; v1 and v2 coexist and verify in one pass.) Determinism here is a deliberate substitution: the timestamp leaves the hash body so two clones agree, and a separate deterministic merge clock puts ordering back.

**A deterministic merge clock.** Promotion still needs to write *some* timestamp. Sourcing it from `new Date()` would make the merged DB differ run-to-run. Instead `merge_clock(index)` derives a strictly-monotonic timestamp from the row's position in the id-sorted traversal. Because the sort is content-stable, a given memory lands at the same index — and gets the same timestamp — on every clone. This is what makes `mergeGovern(A, B)` and `mergeGovern(B, A)` produce byte-identical durable state *and* an identical audit chain. The merge is commutative, by construction, not by luck.

### Three clones, one pass, same answer

Two-way commutativity is the property you can demo. The one you actually need in a team is that it doesn't matter *how* the merge was assembled — three people's clones reconciled in any grouping, any order, must land on the same governed state. The N-way path (`mergeGovernFold`) gets this almost for free, and the "almost" is instructive.

The obvious implementation is an iterated reduce: govern A and B, then re-govern those survivors against C, writing the running database each pass. That is rejected for a concrete reason. The deterministic merge clock restarts at its epoch on every call, so a second pass would mint audit timestamps that collide with or precede the first pass's — and the verifier re-walks the chain by `(timestamp ASC, id ASC)` while the store anchors each new row to the most-recent by `(timestamp DESC, id DESC)`. Colliding per-pass clocks desynchronize insertion order from chronological order, and the chain breaks.

So the fold instead concatenates every clone's rows into the *inputs of a single* `mergeGovern` call: one union, one id-sorted traversal, one strictly-monotonic clock over the whole thing. Because the first step is a set union and the traversal erases input order, `fold([X, Y, Z])`, `fold([Z, Y, X])`, and either grouping of the pairwise merges all produce byte-identical durable state and an identical audit chain. Associative and commutative, proven by a fold-of-three test that asserts every ordering verifies with zero breaks. The reduction shape is the only new code; the governance is reused verbatim.

### The signed DAG anchor: binding the merge to who made it

Determinism gives reproducibility. It does not give attribution. A wholesale rewrite that recomputes every hash is internally consistent and self-verifies clean — the same gap a single-writer external anchor closes for a linear chain. A merge needs more, because a merged head has *two* parents and the question "who reconciled these two histories?" has no answer in the hashes alone.

So each merge appends a **per-actor Ed25519-signed anchor record** (`SignedMergeAnchorRecord`). It binds the merged chain head to a `parents` *set* — the two pre-merge clone heads, sorted so the set canonicalizes identically regardless of input order — a per-actor Lamport clock, the signer's public key embedded inline, and a detached Ed25519 signature over the canonical body. Two independent guards then ride every record: the existing SHA-256 integrity hash (the bytes weren't accidentally corrupted) *and* the signature (a forger who edits the merged chain and re-hashes it forward still cannot produce a valid signature without the actor's private key).

```text
# Illustrative — what the merge-aware verifier checks, and what each catches.
per-clone linear walk        →  tamper inside one clone's own history
id-sorted merged re-walk     →  merged DB NOT produced by mergeGovern (or reordered after)
Ed25519 signature verifies   →  WHO anchored this merge — not just that the bytes agree
parents == {headA, headB}    →  the anchor attests to the correct two chains
chainHead == merged head     →  the anchor describes THIS merged head, not a different one
```

The `parents` field is what makes this a DAG anchor rather than a fancier linear one. A merged head has two ancestors, and the anchor records them as a *set*, not a tuple — sorted before the body is serialized — so the same two clone heads canonicalize to identical signable bytes no matter which clone was passed to `mergeGovern` first. The Lamport clock alongside it is a per-actor monotonic counter the caller owns and bumps before each signed anchor, so an auditor can order one actor's anchors causally even when wallclocks across machines disagree. And an optional `commitHash` records the Dolt or git SHA the merge landed on, giving an external auditor a thread back into version-control history. None of these are required to verify a single merge; all of them are what let a *sequence* of merges across actors be reconstructed after the fact.

The merge-aware verifier owns the canonical id-based ordering as a first-class contract — it re-walks the union by content-derived event id and checks `prev_entry_hash` against the *id-sorted* predecessor, not the wallclock one. It validates each clone's chain linearly first (a break there is tamper in that clone's own history, surfaced before any merge-level reasoning), then re-walks the merged union, then cross-checks the signed anchor. That ordering cures the false `PREV_LINK_MISMATCH` from earlier: a clean merge re-walks to byte-identical hashes and reports zero breaks, so a real reorder or tamper now stands out instead of drowning in merge noise. Against a keyless adversary, the skeptic harness that gated this work reported 20,000 brute-force signature attempts with zero accepted, and a tamper-then-rehash trips `HISTORY_REWRITTEN` or `DAG_HEAD_MISMATCH`.

Five layers stack into the property, and it helps to see them as a unit — each earns one specific guarantee, and none is load-bearing alone:

| Layer | Mechanism | What it earns |
|---|---|---|
| Content-derived UUID v5 | same content derives the same id in every clone | union de-dup is a real set op; id-sorted traversal is reproducible |
| Deterministic entry hash (v2) | canonical hash body excludes the wallclock timestamp | the same logical event hashes identically across clones |
| Govern-at-merge gate | re-derive the union as untrusted through the front door | ungoverned rows are quarantined, never admitted |
| Signed DAG anchor (Ed25519) | parents *set* + signature over the merged head | *which key* reconciled the histories — identity needs a trusted key roster on top |
| Merge-aware verifier | per-clone walk + id-sorted re-walk + anchor cross-check | a real reorder or tamper stands out instead of drowning in merge noise |

Pull any row and the property degrades: without content-derived ids the merge isn't commutative; without the deterministic hash the merged chain won't re-walk clean; without the gate the union is ungoverned; without the signature you can't attribute the merge; without the merge-aware verifier you can't tell a clean merge from a tampered one. They were built and merged as one epic for that reason.

## Why it matters: verification that travels with the content

The payoff is that verification is no longer tied to a place or a trusted party. Any clone, anywhere, that re-derives the same content reproduces the same ids, the same `entry_hash`, the same merged chain, and the same quarantine-or-promote verdict. "Is this merged store governed?" becomes a question you answer by recomputation, not by trusting the machine that produced it. The signed anchor adds the one thing recomputation can't: evidence that a specific *key* performed the reconciliation. The signature is self-contained — verifiable against the public key embedded in the record, with no key server in the loop — but that earns integrity plus "one keyholder signed this," not identity. Attributing that key to a named actor still needs a trusted roster of which public key belongs to whom: the anchor proves a key signed; the roster says whose key it is. That roster is the out-of-band trust this design still leans on, and naming it is the honest version of the claim.

Determinism also makes the merge safe to *preview*. The gate takes a `dryRun` flag that runs the entire pipeline — validation, de-dup, disclosure check, policy, audit-event construction — and writes nothing. Because the result is byte-identical to what a real run would produce, a dry run is a faithful forecast, not an approximation: you can see exactly which rows would promote and which would quarantine before committing the merge. A non-deterministic gate couldn't offer that; its preview and its real run could disagree.

That is the whole shape of the thing. Where a version-control merge says "I reconciled the rows," this says "I re-governed the union from scratch as untrusted, here is the deterministic result you can reproduce, and here is my signature over the head." The merge stops being a place where trust is silently inherited and becomes a place where it is explicitly rebuilt.

## The ceiling, named honestly

The discipline this work inherited from its single-writer predecessor is sizing the claim to the mechanism. So, plainly:

```text
# Illustrative — the ceiling.
forger WITHOUT the actor's private key   →  cannot mint an accepted anchor   (caught)
the key-holder edits a row and RE-SIGNS  →  a self-consistent signed anchor  (NOT caught here)
```

This is **tamper-evident, not tamper-proof.** A legitimate key-holder — or an exfiltrated key — can still edit a row, recompute the chain, and produce a fresh signed anchor that verifies perfectly. The signature proves the edit was made by the key, not that the edit was honest.

That gap is *mitigated, not eliminated*, by two things outside the cryptography. First, key custody: the Ed25519 private key lives only in a SOPS/age-encrypted file, mode 600, loaded at sign time and never written to disk in plaintext. Second, committing the anchor log somewhere append-only that the local writer cannot quietly rewrite — a `git push`, an OpenTimestamps proof. The anchor is only as trustworthy as the place it is committed to; an anchor that lives next to the chain it witnesses is no witness at all. Naming where the stronger claim would need more machinery is part of the claim — the same recursion the single-writer version faced: where do you anchor the anchor?

Two more ceilings worth stating. The re-derivation is only as strong as the detectors it re-runs — the disclosure choke point inherits whatever recall ceiling its secret/PII pattern set has, and re-governing the union doesn't improve that; expanding the detectors is the only lever. And the content-derived ids use UUID v5, which is SHA-1 under the hood per RFC 4122 — that is deterministic namespacing, *not* a security primitive (the static analyzer's weak-crypto alert on it is a dismissed false positive); the audit integrity that actually matters runs on SHA-256. Calling the namespacing "cryptographic integrity" would be the kind of overstatement this whole design exists to avoid.

One more piece of honesty belongs in the same breath, about the substrate. The clone-and-merge story sounds like it demands a distributed database, and the Dolt spike that exposed the ungoverned-merge problem made Dolt the obvious destination. The decision recorded the opposite: the store of record stays SQLite, and the merge gate operates on the store's *types*, not on any one engine's merge — so it is substrate-agnostic, and adopting Dolt later is a swap, not a rewrite.

Migrating the brain onto a distributed substrate is explicitly demand-gated: not built until a real multiplayer need is logged — two people actually blocked on a shared brain, or a real cross-person recall miss. Provisioning a distributed control plane before that signal is exactly the premature optimization the de-risked plan exists to prevent. The merge gate is the part you need *first*, because the governance gap is real the moment two clones exist; the distributed plumbing is the part you can defer until someone is genuinely blocked without it.

The forbidden-words list is short and load-bearing: tamper-proof, immutable, blockchain, and — for the local single-actor case — non-repudiation. What the merge gate earns is real and worth having: governance that survives a merge, deterministic and commutative re-derivation, and cross-actor attribution of the merge event once the anchor is externally committed. Sized to that, the claim holds. Inflated past it, it would be the falsifiable kind that ages into a liability the day someone asks you to prove it.

## The principle

A merge is the one operation where two trust domains touch, and the reflex everywhere — version control, caches, replicas — is to assume the operation preserves whatever properties the inputs had. For data you actually govern, that reflex is the bug. Properties don't compose across a reconciliation you didn't perform yourself.

The fix is not a stronger merge operator; it's refusing to inherit trust at all — re-deriving the union as untrusted, re-running the governance you already trust, anchoring the deterministic result with a signature, and being honest that the signature proves authorship, not virtue. The merge is the trust boundary. Treat it like one.

---

**Related posts:**

- [A Second Brain You Can Audit Beats One You Must Trust](/posts/governed-second-brain-local-first-mcp/) — the single-writer half of this system, where one external anchor closes the silent-rewrite gap for a linear chain. This post is what happens when a second writer arrives.
- [Governed Knowledge: Two Releases, a Freshness Daemon, and Export Gating](/posts/governed-knowledge-two-releases-freshness-daemon/) — earlier groundwork on governing a knowledge corpus rather than just retrieving from it.
- [MCP Server Auth: The API Is the Real Boundary](/posts/the-api-is-the-real-boundary/) — the same knowledge system, and why the governance audit trail must stay pure for verification to mean anything.
