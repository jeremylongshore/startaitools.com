+++
title = "No-Toggle Test: Make 'Not Built Yet' an Enforced Invariant"
slug = 'single-tenant-first-no-toggle-test'
date = 2026-06-22T08:00:00-05:00
draft = false
tags = ["testing", "architecture", "multi-tenancy", "governance"]
categories = ["Development Journey"]
description = "Shipping single-tenant first is sound—but 'we haven't built multi-tenancy yet' rots as a comment. A static no-toggle test makes it an enforced invariant."
+++

June 22 on **agent-governance-plane** was a paperwork day. Eight releases (v0.1.74 through v0.1.81), a stack of architecture decision records, a non-breaking migration test, and a council ruling on conformance. Mostly governance cadence—the kind of day that produces a lot of merged PRs and very little you'd screenshot. But one commit buried in the release train carries a discipline worth pulling out and naming, because it solves a problem every project hits and almost everyone solves with a comment.

## The Thesis

When you deliberately ship the simple version of something first—single-tenant before multi-tenant, one region before many, sync before async—you create a gap between what the code does and what the code is *allowed* to do. The usual way to record that gap is a comment: `// multi-tenant not implemented yet`. Comments rot. The honest move is to make "not built yet" an assertion a test enforces, so the boundary can't quietly erode while nobody's looking.

## The Decision: Single-Tenant First

The first PR in the train (#104) was `feat(tenants): single-tenant model + fail-closed guard + static no-toggle test`. The project chose to ship a single-tenant model now and defer multi-tenancy. That's a normal, defensible call—you don't build tenant isolation before you have a second tenant, and premature multi-tenancy is a great way to ship a slow, leaky system for users you don't have yet.

But deferring multi-tenancy creates a hazard. The data model has to *anticipate* it—the journal carries a `tenant_id` so the migration later is non-breaking (that's what PR #105's `non-breaking tenant_id round-trip migration test` proves). And once the column exists, the temptation exists: some future change flips on a code path that reads or branches on `tenant_id`, and now you have a half-built multi-tenant system with none of the isolation guarantees. The gap between "the schema is ready" and "the isolation is enforced" is exactly where a silent regression lives.

## The No-Toggle Test

Two guards shipped against that hazard. The first is a **fail-closed guard**—if anything tries to operate in a multi-tenant mode that doesn't exist yet, the system refuses rather than guessing. Standard fail-closed posture.

The second is the interesting one: a **static no-toggle test**. It asserts that the multi-tenant toggle is *not reachable yet*. Not "the toggle is off"—a toggle that's off can be flipped on. The test asserts the toggle doesn't exist as a live path at all. "We haven't built multi-tenancy" stops being a fact you have to remember and becomes an invariant the suite enforces on every run.

The difference between those two framings is the whole point:

- A **comment** (`// TODO: multi-tenant`) is a hope. It documents intent and enforces nothing. The first person who wires up a `tenant_id` branch sails right past it, green build and all.
- A **runtime flag set to false** is better, but it's still a switch. It invites someone to flip it "just to test something" and forget. The off-state is one config change from on.
- A **static test asserting the toggle isn't reachable** is a tripwire. The moment someone adds the code path that makes multi-tenancy live, the no-toggle test goes red. They have to *consciously* delete the assertion—which means consciously acknowledging they're now on the hook for tenant isolation.

That last property is what makes it governance and not just a test. It converts an architectural intention ("single-tenant first, multi-tenant later, deliberately") into something that fails loudly the instant reality diverges from the plan. You can't accidentally become multi-tenant. You have to mean it, in a commit that deletes a named assertion, which shows up in review.

## Why This Beats the Comment

The standard objection: "isn't a no-toggle test just testing that we didn't write code?" Yes—and that's the value. Most tests verify behavior you built. This one verifies the *absence* of behavior you deliberately chose not to build. The cost of writing it is near zero. The thing it buys you is that the absence is now load-bearing and monitored, instead of an assumption that survives only as long as everyone remembers the meeting where you decided it.

There's a second-order benefit, too. A no-toggle test documents the deferral better than any ADR can, because it lives next to the code and runs constantly. A new contributor doesn't have to find the readiness ADR to learn that multi-tenancy is intentionally absent—the failing assertion tells them the moment they reach for it. The test is both the guard and the explanation, and unlike a doc, it can't silently fall out of sync with the implementation.

Pair it with the round-trip migration test (#105) and the readiness ADR (#106, `multi-tenant readiness ARCH + single-tenant gate ADR`) and you get a complete, honest picture: the schema is ready for multi-tenancy, the migration is proven non-breaking, the design is written down—*and* a test stands guard asserting none of it is live yet. Ready, documented, and provably not-yet-enabled, all at once.

## The Other Durable Idea: Model-Only Egress

The same day's ADR work produced a second concept worth keeping. PR #109, `docs(adr): Topology C model-only egress-allowlist design`, sketches a topology where the *only* permitted egress is to the model endpoint. Not "egress is restricted." Not "we allowlist a set of domains." The allowlist has exactly one entry: the model the agent is allowed to call. Everything else is denied by default.

It's the same shape of thinking as the no-toggle test—define the boundary as a single explicit permission and let everything outside it be a hard denial, rather than enumerating things to block and hoping the list stays complete. A blocklist rots the same way a comment does; the model-only allowlist makes "data can leave here and nowhere else" an enforced invariant instead of a policy nobody re-checks. (It's the egress-side cousin of [rejecting PII at the source](/posts/disclosure-gate-reject-pii-at-source/) and of treating [the API as the real boundary](/posts/the-api-is-the-real-boundary/).)

## The Rest of the Paperwork

The day closed with a council ruling—PR #110, `docs(decr): ISEDC council ruling on ACS conformance + the Q5 revisit`—recording a conformance decision and flagging a question to revisit. That's the unglamorous half of governance: writing down what was decided and what stays open, so the next session doesn't relitigate it from memory. Releases v0.1.77 and v0.1.78 carried dogfood-budget scoping and a deferred HITL-convergence evaluation. None of it is dramatic. All of it is the cost of keeping a governance layer honest.

Elsewhere in the portfolio, the GCP exodus advanced quietly: the `bigo-portfolio` and `cost-plus-db` projects were deleted (recorded as Stage E in the VPS runbook), and CostPlusDB was reframed on the portfolio site as a retired demo rather than a live service. Same theme—make the real state of things explicit instead of letting a dead service look alive.

## The Takeaway

Shipping the simple version first is good engineering. The mistake is recording the deferral as a hope—a comment, a TODO, a flag you trust people to leave alone. The no-toggle test is the cheap fix: assert the thing you haven't built isn't reachable, so the day someone builds it, they have to say so out loud by deleting your assertion. Make "not built yet" an invariant, not a wish. The model-only egress allowlist is the same move pointed at data flow. Both turn an intention into something that fails loudly when reality drifts—which is the only kind of intention a governance layer can actually keep.

## Related Posts

- [Honor the Gate When the Verdict Is Inconvenient](/posts/honor-the-gate-when-the-verdict-is-inconvenient/)
- [When --cap-drop ALL Broke the Gate Socket](/posts/cap-drop-all-broke-the-gate-socket/)
- [The Disclosure Gate: Reject PII at the Source](/posts/disclosure-gate-reject-pii-at-source/)

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "No-Toggle Test: Make 'Not Built Yet' an Enforced Invariant",
  "description": "Shipping single-tenant first is sound—but 'we haven't built multi-tenancy yet' rots as a comment. A static no-toggle test makes it an enforced invariant.",
  "datePublished": "2026-06-22T08:00:00-05:00",
  "dateModified": "2026-06-22T08:00:00-05:00",
  "author": {
    "@type": "Person",
    "name": "Jeremy Longshore"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Start AI Tools"
  },
  "url": "https://startaitools.com/posts/single-tenant-first-no-toggle-test/",
  "keywords": "no-toggle test, single-tenant first, multi-tenancy, fail-closed, egress allowlist, invariant, testing, architecture, governance"
}
</script>
