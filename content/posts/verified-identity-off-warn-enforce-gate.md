+++
title = 'Verified Identity for AI Agents: Off, Warn, Enforce'
slug = 'verified-identity-off-warn-enforce-gate'
date = 2026-06-21T08:00:00-05:00
draft = false
tags = ["ai-agents", "identity", "cryptography", "governance"]
categories = ["Development Journey"]
description = "Give AI agents an Ed25519 verified identity, then roll out an off/warn/enforce daemon gate that refuses to act on an unverified one — like an unsigned commit."
+++

June 21 was a build day on **agent-governance-plane**. Twenty commits, ten releases — v0.1.64 through v0.1.73 — and a release-bot churning out version tags faster than the changelog could keep a thought. On a day like that it's easy to lose the throughline in the noise. There was exactly one: **no unverified intendant acts.**

## The Thesis

An "intendant" is the AI agent acting *through* the governance plane — the thing that opens a session, runs a command, posts to a channel. Until June 21, the daemon knew an intendant existed. It did not know *who* it was, and it had no way to prove the answer. That's the same posture as a git history full of unsigned commits: the work is there, the authorship is a shrug.

The fix is the one git already settled years ago. Give every actor a cryptographic identity, mint a verifiable name for it, and gate the system on whether that name checks out — rolled out the only safe way a gate ever rolls out: **off, then warn, then enforce.** Treat an unverified agent exactly like an unsigned commit. By end of day the daemon could refuse to act on one.

## Build the gate from the inside out

The interesting part isn't that the feature shipped. It's the *order* it shipped in — four PRs that each only make sense because the one before it landed first.

**1. Record who ran, before you can verify it (agp-z26.1, #93).** The first commit added an `intendant_identity_uri` to the journal — every recorded action now carries a field for *which* intendant produced it. This is deliberately the cheapest possible step: you can't enforce identity you've never written down, and you can't debug a gate that has no audit trail. Start by making the system *able to name* the actor, even before the name means anything.

**2. Make verification a seam, not a hardcode (agp-z26.2, #94).** Next came a pluggable `Verifier` interface plus an `IntendantManifest` contract — the shape an intendant must present to be checked. Crucially, this PR shipped *no* real crypto. It shipped the hole where crypto goes. That ordering is the whole discipline: define the contract before the implementation so the implementation can never quietly become the contract.

**3. Drop in a real backend (agp-z26.3, #95).** Only now does Ed25519 arrive — a v0 verification backend that mints the verified identity URI. It satisfies the seam from step 2 and populates the journal field from step 1. Because the seam already existed, the crypto is just *one* implementation of `Verifier`, swappable the day a better scheme shows up. Nothing downstream knows or cares that it's Ed25519.

**4. Turn the key — slowly (agp-z26.4, #96).** The last piece is the gate itself: an **off / warn / enforce** identity gate in the daemon.

- **off** — verification runs, nobody is blocked. You're collecting signal.
- **warn** — unverified intendants are flagged loudly but still act. You find out what's actually in your system before you break it.
- **enforce** — the daemon *refuses* to act on an unverified intendant. The unsigned commit gets rejected at the door.

Anyone who has rolled out a Content-Security-Policy `report-only` header before flipping it live, or run a new lint rule as a warning for a sprint before making it a hard error, knows this shape. A gate you flip straight to enforce is a gate you flip straight to an incident. The three-position switch is what lets you turn identity enforcement on in a *running* system without a flag day.

## Prove the contract is generic, not Claude-shaped

A governance plane that only governs one harness isn't a governance plane — it's a wrapper. So the day's capstone (agp-cln.1, #97) was a `CodexIntendant` plus a deterministic reference implementation, proving the identity contract holds for a second harness. Claude and Codex both present an `IntendantManifest`, both get verified through the same seam, both land an `intendant_identity_uri` in the same journal. The follow-on work that same day pushed it further: a live Codex interception path (agp-cln.2, #99), a test proving two concurrent harness sessions share one channel without echo loops (agp-cln.3, #98), and finally unlocking the multi-harness claim itself — *gated on the green contract and the concurrent tests passing* (agp-cln.4, #101).

That last detail is the tell. The claim "we support multiple harnesses" wasn't allowed to be a marketing sentence. It was wired to depend on a passing contract and real concurrency tests — a claim that can only be made when the evidence is green. (A later commit, agp-g68 / #103, even broadened the banned-claim regex to catch repudiation variants the scanner had missed.)

## The transferable point

A verified identity is a claim, and "verified" has to *mean* the signature checked out — same as a green CI check has to mean the tests ran. The four-PR sequence is what makes the claim trustworthy:

1. **Name the actor first** (journal field) — you can't govern what you can't reference.
2. **Define the contract before the implementation** (the `Verifier` seam) — so the crypto can never silently *become* the spec.
3. **Make the backend swappable** (Ed25519 as one `Verifier`) — v0 today, something stronger later, nothing downstream rewritten.
4. **Roll the gate off → warn → enforce** — so you can turn it on in production without a flag day.

Skip step 2 and your verification *is* whatever the first backend happened to do. Skip the off/warn/enforce ramp and enforcement day is an outage. The order isn't ceremony; each step exists to keep the next one honest.

## Also shipped

Same day, the same "build it so it can't lie" instinct showed up across the portfolio:

- **agent-governance-plane** also landed a transactional outbox for at-least-once channel delivery (agp-4na.3, #92) — durable message hand-off, not fire-and-forget.
- **qmd-team-intent-kb** did EPIC 0/1 residual hardening: an N-way merge fold with a commutativity/associativity proof, a fail-loud check at the merge gate on non-content-derived row IDs, and a cross-repo golden-vector drift guard pinning ICO's UUID vector inside INTKB (#209, #210).
- **governed-second-brain** brought its brain API live on the tailnet and filed the deploy-hardening follow-up rather than calling it done.
- **intent-outreach** cleared its dependency debt — zod v3 → v4 and the Vercel AI SDK v4 → v6, the latter clearing every open npm-audit vuln (#22, #23).

## Why the boring order is the whole post

Ten releases in a day looks like velocity. What it actually was: a single capability — verified agent identity — disassembled into four steps small enough that each could ship green and none could ship a lie. Name, then contract, then backend, then a gate you ease into. By the time `enforce` is available, every piece under it has already been proven in isolation.

That's the move worth stealing. When you give your AI agents an identity, don't ship "we verify agents now" as one heroic PR. Ship the journal field. Ship the empty seam. Ship the backend that fills it. Ship the three-position switch. Then, and only then, turn the key — and treat the unverified agent exactly like the unsigned commit it is.

## Related Posts

- [Honor the Gate When the Verdict Is Inconvenient](/posts/honor-the-gate-when-the-verdict-is-inconvenient/)
- [The API Is the Real Boundary](/posts/the-api-is-the-real-boundary/)
- [When Green CI Proves Nothing](/posts/when-green-ci-proves-nothing/)

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Verified Identity for AI Agents: Off, Warn, Enforce",
  "description": "Give AI agents an Ed25519 verified identity, then roll out an off/warn/enforce daemon gate that refuses to act on an unverified one — like an unsigned commit.",
  "datePublished": "2026-06-21T08:00:00-05:00",
  "dateModified": "2026-06-21T08:00:00-05:00",
  "author": {
    "@type": "Person",
    "name": "Jeremy Longshore"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Start AI Tools"
  },
  "url": "https://startaitools.com/posts/verified-identity-off-warn-enforce-gate/",
  "keywords": "AI agent identity, Ed25519, cryptographic identity, off warn enforce, agent governance, verified identity URI, ai-agents, cryptography"
}
</script>
