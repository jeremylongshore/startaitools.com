+++
title = 'First Slice in One Day: Eight PRs, One Sign-Off'
slug = 'first-slice-eight-pr-one-day'
date = 2026-10-10T10:00:00-06:00
draft = false
tags = ["devops", "deployment", "refactoring", "decision-records", "publish-and-park"]
categories = ["DevOps"]
description = "Split a first slice into one PR per layer, capped by a governance PR with the sign-off. Each layer, the merge-guard hiccup, and the day the slice landed."
tldr = "Eight merged PRs closed the catalyst-onboarding-v2 first slice in one day, each carrying its own hand-traceable handoff label. The final PR was a governance record with no code, just the owner's explicit sign-off on the slice. One cost: a stale merge-guard pin that took a single config line to fix."
experience_sources = ["catalyst-onboarding-v2 PRs #9, #11-#17", "~/000-projects/CROSS-SESSION-LOG.md 2026-10-10 23:06 entry"]
+++

A parked refactor (a code rewrite that someone deliberately stopped short of
merging, with a dated record of what was kept) sits there until somebody
pushes the first new code on the successor repo (a fresh, empty git
repository opened to carry the rewrite). That is the stretch where most
rewrites die.

The story for this day is eight merged PRs on the catalyst-onboarding-v2
first slice, each carrying its own hand-traceable handoff label (a short ID
like S1-T2 that ties the PR back to the parking plan), capped by one
governance PR (a pull request with no code change, only a dated sign-off in
the commit body) that recorded a single explicit owner sign-off (the named
reviewer's documented approval). If you shelved a clean rewrite yesterday
and have been staring at an empty branch this morning, this is what day one
looks like when it lands.

The hard part of starting is not the code. The new repo is unverified: the
test infrastructure is empty, no recorded check yet passes (the acceptance
baseline), and nothing in the commit history ties back to the spec the
parking bundle (the dated record preserving the original state) was
supposed to preserve. So when the first PR lands, it has nothing to lean
on, and the energy to push a second one is usually gone before lunch.

The pattern that worked was treating each layer of the first slice as its
own PR with its own hand-traceable handoff ID, then closing the day with one
governance PR that recorded an explicit sign-off. Eight PRs landed in a
single day: seven per-layer handoff IDs (S1-T2 through S1-T8) and one
governance label (GATE-S1) recorded in the final, code-empty PR. One
sign-off. That is the shape of the day.

What "first slice" means in this context: the smallest end-to-end vertical
that proves the architecture works, not a complete product. Public intake
form posts to the system, a verified message goes back to the requester, a
staff-visible copy lands in the dossier, all on top of a working data model
and a worker that recovers from crashes. Every PR was a layer in that
vertical: skeleton, data model, intake form, worker, confirmation, staff
dossier, acceptance tests, then a final governance record.

Each PR opened its own draft the moment the previous one merged, which kept
the work honest because every push was a push of a single, isolated layer,
not a kitchen-sink commit. A few details that mattered:

- The skeleton PR had PostgreSQL-only start-up guards written into it, not
  patched in later. A clean-DB check fired before the app started, which
  catches the "I forgot to run migrations" failure before it bites in CI.
- The data model PR came with ADR-14 baked in: roles and an append-only
  history table for the audit trail. Decisions go in dated records, not in
  PR comments that later disappear.
- The intake form used a one-transaction write so a double-submit became a
  race-safe duplicate row instead of a torn record. The duplicate check ran
  inside the same transaction.
- The worker used a lease fence for recovery. A row was claimed for a fixed
  window, and any worker that came back after losing a crash saw the lease
  and skipped the row. That kept the worker crash-safe without a queue
  service.
- The confirmation message adopted only the explicitly named version of the
  contact. No "latest" reference, no loose link. The named version is the
  one in the PR.
- The staff dossier was read-only Django Admin, with owner-created accounts
  and a view-only group. Staff sees the data. Nobody edits from the admin
  panel.
- The acceptance tests mapped every first-slice case to its tests and gated
  the full run on all PASS. The gate was not advisory.
- The final PR was the only one with no code in it. It recorded the owner's
  GATE-S1 sign-off (the "yes, this slice shipped the spec" record) and the
  POL-01 confirmation (the "yes, the parking contract held" record),
  referenced by dated decision documents D-25 and D-26. Two decision records,
  one merge, end of day.

Only one thing broke the rhythm: a merge-guard hiccup, and the lesson comes
from the fix itself. The merge-guard script that gates merges on required CI
was pinned to a branch name pattern that did not match the first few PRs.
The fix was a one-line config edit, but eight PRs plus one config tweak is
the honest count. Without a merge-guard, any of those eight could have
merged without the safe-merge contract. With a stale guard, the slot gets
wasted on a false block. The guard is the right shape. The pin is the bug.

The other point matters too: a single epic (a parent task that groups related
work items) had one open child bead (a tracked task record in the repo's
issue database) at end of day (catalyst-v2-6hl.10). Closing the whole epic
before the final governance PR would have been a lie. The git history is
the audit trail, not the bead state, so the bead stays open until the
governance PR is what closes the epic. One carry-over, all sign-offs
recorded on the rest.

If you are staring at an empty successor branch tomorrow, the lesson is: do
not write the whole refactor in one PR. Write the layers. Each layer is
small enough to review in one sitting, each layer has a hand-traceable label
that ties it back to the parking bundle, and the final layer is the sign-off.
Eight PRs, eight labels, one sign-off, in
[catalyst-onboarding-v2](https://github.com/intent-solutions-io/catalyst-onboarding-v2).
That is the day.

## Use this

- Treat each layer of your first slice as its own PR with a hand-traceable
  handoff label that maps to the original spec. The PR is the proof. The
  label is the audit trail.
- Bake the start-up guards, the data model decisions, and the role split
  into the layer where they belong. Patching in the boring parts later is
  where the day gets eaten.
- Close with a governance PR that records the explicit owner sign-off and
  the parking-contract confirmation. Code PRs prove code. The governance PR
  proves the slice.

## Related Posts

- [parked-refactor-five-receipts](/posts/parked-refactor-five-receipts/) -
  the five named artifacts that make a parked refactor recoverable
- [park-the-cutover-keep-the-work](/posts/park-the-cutover-keep-the-work/) -
  the publish-and-park pattern, with five invariants
