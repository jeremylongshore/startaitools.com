+++
title = 'Your System-Map Is Fiction Until You Diff It Against Live Infra'
slug = 'verify-system-map-against-live-infra'
date = 2026-06-14T08:00:00-05:00
draft = false
tags = ["devops", "documentation", "infrastructure"]
categories = ["DevOps"]
description = "A system-map that isn't verified against live infrastructure is fiction. The day you decommission a service is the day to reconcile the docs against the live Caddyfile."
+++

A system-map is a document that claims to describe live infrastructure. The
moment those two things disagree, the document is no longer documentation — it's
a story about a system that used to exist. On June 14, 2026, the Intent Solutions
fleet decommissioned its `ntfy` notification service. The interesting work wasn't
the teardown. It was the reconciliation pass that followed: walking the
system-map across several repos and diffing every claim against what was actually
running.

## The Thesis

A system-map that isn't verified against live infrastructure is fiction. Not
"slightly stale," not "mostly right" — fiction, because a reader can't tell which
lines are true. The discipline that fixes this is cheap and unglamorous: the day
you change infrastructure is the day you reconcile the docs, and you reconcile
against the live config, not against memory. Memory is the thing that wrote the
wrong number in the first place.

## What Decommissioning ntfy Exposed

`ntfy` was the push-notification relay for the fleet. Pulling it should have been
a one-line change in one place. It wasn't, because the service was named in
multiple system-map documents across multiple repos — and those documents had
already drifted from each other before ntfy ever left.

The reconciliation touched two source-of-truth documents:

- **intent-os** — the system-map was synced to the ntfy decommission, and in the
  same pass the container and stack counts were corrected to **34 containers
  across 6 stacks**. The commit that mattered most wasn't the ntfy edit; it was
  the one titled "verify vs live Caddyfile" — the counts and timers weren't
  retyped from recollection, they were checked against the running ingress
  config.
- **intentsolutions-vps-runbook** — the same 34/6 correction landed here, plus
  every `ntfy-relay` mention was dropped. Two documents, same fleet, and they had
  to be brought into agreement with each other *and* with the live box.

The number is the tell. Two repos independently described the same
infrastructure, and both had the container/stack count wrong until someone
counted. If the count was wrong, what else was? That's the whole argument for
reconciling on change: drift is invisible until you diff, and the only honest
diff is against the live system.

## Verify Against the Caddyfile, Not Memory

The load-bearing phrase in the day's commits is "verify vs live Caddyfile." Caddy
is the single ingress for the fleet — every public route, every reverse-proxy
target, every active service passes through one config file. That file is not a
description of the system; it *is* the system's routing truth. So it's the right
oracle.

The wrong way to update a system-map is to read the old system-map, edit the
lines you remember changing, and commit. That propagates yesterday's errors
forward and adds today's. The right way is to treat the live config as ground
truth and the document as the thing under test: open the Caddyfile, count what's
actually routed, list the timers that actually fire, and make the document match.
The document is downstream of reality, never the other way around.

This is the same instinct as a test that asserts against real behavior instead of
a mock of the behavior you assumed. A system-map verified against memory asserts
against a mock of your own infrastructure.

## Drift Hides in the Corners

Reconciliation isn't only about the headline service. Once you're diffing
documents against reality, the small dead facts surface too:

- A **Porkbun default-MX quirk** got documented in the runbook — the kind of
  provider-specific gotcha that's invisible until mail silently misroutes, and
  worth writing down the moment you understand it. It shipped alongside a
  `plane-email-setup` runbook covering the SMTP fix and onboarding gotchas.
- **dixieroad.org** was marked released — the domain had expired on 2026-05-13
  and was still listed in active state a month later. A system-map that lists a
  domain you no longer own is the same failure as one that lists a service you no
  longer run: a confident claim that happens to be false.

Neither of these is dramatic. That's the point. Drift accumulates in the corners
nobody re-reads, and the only way it gets caught is a deliberate pass that
questions every line, not just the ones you touched today.

## The Cleanup Was Real Work, Not Just Docs

Two other commits from the day make clear the reconciliation wasn't paperwork
sitting on top of a static system — the infrastructure genuinely moved:

- A bead closed because a **persistent brain store** was stood up — new
  infrastructure that itself becomes a line the system-map now has to track
  truthfully.
- A **partner pilot reschedule** was logged — the three-week window pushed back
  to a Jul 6–Oct 4 run. Operational state, captured in the document of record so
  the next reader doesn't reconstruct it from a chat scroll.

A system-map only stays true if every change to the system writes back to it on
the same day. The decommission was the forcing function; the discipline is doing
it every time, not just when something big leaves.

## The Transferable Rule

You don't need a fancy tool for this. You need a habit: when infrastructure
changes, reconcile the docs in the same change, and reconcile against the live
config rather than the previous version of the docs. The live Caddyfile, the
running container list, the actual DNS records — those are your oracles. The
system-map is the thing being tested against them.

A document that agrees with reality on the day you write it and is never checked
again will be wrong within a month. dixieroad.org was wrong for exactly that
long. The fix isn't writing better docs once. It's diffing them against the live
system every time the system moves — because a system-map you haven't verified is
just a story you're telling yourself about a box you're not looking at.

---

**Related posts:**

- [MCP Server Auth: The API Is the Real Boundary](/posts/the-api-is-the-real-boundary/)
- [Honor the Gate When the Verdict Is Inconvenient](/posts/honor-the-gate-when-the-verdict-is-inconvenient/)
