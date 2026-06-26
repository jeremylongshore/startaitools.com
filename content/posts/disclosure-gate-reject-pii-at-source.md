+++
title = 'Reject PII at the Source: A Disclosure Gate at Intake'
slug = 'disclosure-gate-reject-pii-at-source'
date = 2026-06-19T08:00:00-05:00
draft = false
tags = ["governance", "privacy", "knowledge-base", "dolt"]
categories = ["Development Journey"]
description = "The cheapest place to enforce a privacy rule is the front door — a fail-closed disclosure gate that rejects comp data and PII at candidate intake."
+++

June 19, 2026 was a broad day across the governed-knowledge stack — a privacy gate at one project's front door, a new beads plugin shipped at another, a substrate exploration at a third, and a wall of grouped dependency bumps in between. The throughline isn't the breadth. It's where the governance lives: at the source.

## The Thesis

The cheapest place to enforce a rule is the front door, before anything downstream can store, index, or reason over the data. If you reject compensation figures and PII *at candidate intake*, you never have to write the rule again. No retrieval layer has to remember to filter it. No promotion step has to scrub it. No export has to redact it. The data simply never enters the system.

That's what `qmd-team-intent-kb` shipped on the 19th, and it's the part of a wide day worth slowing down for.

## The Disclosure Gate

`qmd-team-intent-kb` is a governed memory store — the knowledge base half of the brain stack. The unit of input is a *candidate*: a piece of text proposed for the store, not yet trusted, not yet promoted to governed memory. Candidates are where untrusted data first touches the system.

v0.7.0 added a fail-closed disclosure gate at that exact boundary. The commit reads `feat(api): enforce no-comp/no-PII disclosure gate at candidate intake` (PR #201). Two rules, both enforced before the candidate is accepted:

- **No compensation data.** Salary figures, rate cards, offer numbers — rejected at intake.
- **No PII.** Personally identifiable information — rejected at intake.

Fail-closed is the load-bearing word. The gate's default answer is *no*. A candidate is accepted only if it clears the disclosure rules; anything ambiguous is rejected, not waved through. The failure mode of a privacy filter should be over-rejection, never silent acceptance — because a leaked salary or a leaked name can't be un-leaked once it's indexed. A fail-open gate that lets ambiguous text through "to be safe about false positives" has the asymmetry exactly backwards: a false reject costs one re-submission, a false accept costs a permanent disclosure.

The follow-up commit is the honest part: `fix(api): harden the disclosure-gate comp regexes per Gemini review` (PR #202). The first pass at compensation detection had gaps an AI reviewer caught — the kind of edge cases regex-based detection always has. Comp figures show up as bare numbers, as ranges, as "OTE," as hourly rates, as currency-prefixed and currency-suffixed strings. No single pattern covers them. The fix hardened the patterns and shipped. A privacy gate is exactly the place where you take the reviewer's catch seriously rather than arguing the original was "good enough" — because the cost of a missed pattern here isn't a bug ticket, it's a disclosure that already happened.

The bead trail closed the loop: `chore(beads): close 3iu.1 — disclosure gate shipped (PR #201 + #202)`. The gate, the hardening, and the tracked work all landed as one unit. That's the shape governance work should take — the enforcement and the audit trail ship together, so the next session can see not just that a gate exists but why it was built and what review hardened it.

## Why the Source and Not the Sink

The instinct on a privacy requirement is to filter at the read path — scrub PII when you export, redact comp data when you serve a query. That's the sink, and it's the wrong place. The two postures compare like this:

- **Filter at the sink (read path):** the rule has to be re-implemented at every endpoint, every export, every consumer. Each one is a new place to forget it. A single gap exposes every record already in the store. You protect data that's already at risk.
- **Filter at the source (intake):** the rule lives once, at the front door. Downstream code assumes a clean store. A gap rejects one candidate, not the whole corpus. You protect data before it's at risk at all.

Every read path is a new place to forget the rule. Add an endpoint, you re-implement the filter. Add a consumer, you hope it remembers. The rule fragments across every place data leaves the system.

Enforce at the source and the rule lives in exactly one place: the front door. Downstream code gets to assume the store is clean because the only way in already proved it. That assumption is the whole payoff — it's what lets the rest of the stack stay simple.

There's a second reason the source beats the sink: blast radius. A filter at intake protects data that hasn't been written yet, so the worst case of a bug is one rejected candidate. A filter at the read path is the last line before data already in the store reaches a consumer — and if it has a gap, every record that ever entered is exposed through it. The source gate fails small. The sink gate fails large. When you're picking where to spend your one careful implementation, spend it where a mistake is cheapest to recover from.

The same day, `qmd-team-intent-kb` also shipped a one-shot `promote-candidate→governed-memory` endpoint (PR #203) — the path from untrusted candidate to trusted memory. That promotion step is *only* safe to keep simple because the disclosure gate already ran at intake. The clean-source assumption is what the promote endpoint gets to rely on. Source-enforcement and a simple promotion path are the same design decision seen from two ends.

## The Rest of the Stack Widened

The disclosure gate was the deep work. The rest of the day was honest breadth — the governed-knowledge stack getting wider on several fronts at once.

**`beads-dolt` shipped v0.1.0** — a Dolt/DoltHub-aware beads workflow as a plugin (`feat: beads-dolt plugin v0.1.0`). Beads is the task tracker; Dolt is a version-controlled SQL database. The plugin teaches the beads workflow to live on a Dolt substrate. It got dogfooded the same day through the Intent Eval Platform (`test: dogfood beads-dolt through the Intent Eval Platform`) — shipping a plugin and immediately running real work through it is the only test that counts. A follow-up fix reordered the skill docs to `lead with the root-cause AND the two-command fix`, a finding that surfaced from the dogfooding itself.

**`governed-second-brain` explored Dolt-as-substrate** — a documented exploration of using Dolt as the storage substrate with a distributed-remote model (`docs: Dolt-as-substrate + distributed-remote exploration`, PR #7), plus the bead cross-refs to track it as a real epic. This is the wider bet behind `beads-dolt`: if a version-controlled database is the right substrate for tracked work, it might be the right substrate for governed memory too. The exploration is documented, not built — the honest state of a bet still being weighed.

**`intentional-cognition-os` planted the same gate's seed** — a bead to `track ICO ingest-time disclosure enforcement` (epic cze). The disclosure-gate pattern that `qmd-team-intent-kb` just shipped at intake gets tracked for ICO's ingest path too. Same discipline, different front door. When a pattern proves out at one project's source, the move is to plant it at the next project's source — not to bolt a filter onto ICO's read path later.

**A wall of dependency bumps cleared.** `qmd-team-intent-kb` took a grouped dependabot batch — `bump the dev-dependencies group across 1 directory with 10 updates` (#196), a 9-update GitHub Actions group (#195), production-deps, testcontainers, and more. The enabling commit landed first: `chore(dependabot): group routine updates to cut PR noise` (#194). Grouping routine updates is itself a governance-at-the-source move — instead of ten separate PRs each demanding a review, the noise gets collapsed at the dependabot config so the review surface stays small. Same principle as the disclosure gate: fix it at the configuration boundary, not at every downstream PR.

**`jeremylongshore.com` got an operator-editorial redesign** with live API contributions (`feat(site): operator-editorial redesign + live API contributions`) — the portfolio site, unrelated to the brain stack, but part of the day's honest breadth.

## The Takeaway

A broad day is still a day. The breadth here wasn't scatter — it was one principle showing up at several front doors at once.

Enforce governance at the source and the rule lives in one place. The disclosure gate proves it most cleanly: reject compensation data and PII at candidate intake, fail-closed, and nothing downstream has to remember to. The promote endpoint stays simple because the source is clean. The dependabot grouping cuts noise at the config, not at every PR. The ICO bead plants the same gate at the next project's front door.

The knowledge stack got wider on the 19th — `beads-dolt` shipped, Dolt-as-substrate got explored, a dependency wall cleared. But the spine of the day was a single fail-closed gate at one boundary, doing the work so that nothing after it has to.

## Related Posts

- [Honor the Gate When the Verdict Is Inconvenient](/posts/honor-the-gate-when-the-verdict-is-inconvenient/)
- [When Green CI Proves Nothing](/posts/when-green-ci-proves-nothing/)
- [The API Is the Real Boundary](/posts/the-api-is-the-real-boundary/)

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Reject PII at the Source: A Disclosure Gate at Intake",
  "description": "The cheapest place to enforce a privacy rule is the front door — a fail-closed disclosure gate that rejects comp data and PII at candidate intake.",
  "datePublished": "2026-06-19T08:00:00-05:00",
  "dateModified": "2026-06-19T08:00:00-05:00",
  "author": {
    "@type": "Person",
    "name": "Jeremy Longshore"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Start AI Tools"
  },
  "url": "https://startaitools.com/posts/disclosure-gate-reject-pii-at-source/",
  "keywords": "governance at the source, disclosure gate, fail-closed, PII rejection, candidate intake, governed memory, Dolt substrate, beads-dolt, privacy, knowledge base"
}
</script>
