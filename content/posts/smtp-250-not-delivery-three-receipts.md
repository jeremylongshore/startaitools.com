+++
title = 'SMTP 250 is not delivery: three receipts that fix transactional mail'
slug = 'smtp-250-not-delivery-three-receipts'
date = 2026-10-11T08:00:00-06:00
draft = false
tags = ["email", "smtp", "transactional-mail", "delivery-receipts", "phase-classification", "evidence-before-resend", "design-rationale"]
categories = ["DevOps"]
description = "SMTP 250 is not delivery. Three receipts fix transactional mail: a frozen ApprovedMessage, phase-classified outcomes (RFC 5321 §4.2.1), and reconciliation before any resend."
tldr = "SMTP says 250, but the relay may still lose the message. The three receipts that fix this: a frozen ApprovedMessage at enqueue, phase-classified SMTP outcomes per RFC 5321 §4.2.1, and reconciliation against admissible evidence before any resend."
+++

SMTP returns "accepted" for a message the relay may still lose ten minutes later, and APPEND is not delivery. After this, an engineer auditing a transactional mail system can name the three receipts (machine-written records proving each step really ran) that recover the truth, explain why each is non-negotiable, and check their own system against them.

The receipts come from a recent design pass on Catalyst's correspondence subsystem, but the problem belongs to any system that sends mail through a hostile network. SMTP is honest about the protocol. It is silent about what happens after.

## The first receipt: a frozen ApprovedMessage

The first receipt is a record of intent, frozen at the moment of enqueue. In Catalyst's design, every outgoing message becomes an ApprovedMessage row at insert: authorized then, and only its disposition is updatable afterward. The template that produced it is owner-approved, and the text is fixed by grant.

That single rule kills an entire class of drift. A message enqueued at 10:00 cannot be quietly edited at 10:05 by a retry path, a config push, or a fix-up migration. The bytes that leave the wire are the bytes that were approved. Reconciliation later has a fixed target to compare evidence against.

The temptation is to skip this and rely on the template alone. That breaks the first time a template changes between the moment of approval and the moment of send. The frozen message is the receipt that says "this is what was sent, and we said so before it went." A row that was right at insert is the cheapest receipt a system can keep.

## The second receipt: phase-classified SMTP outcomes

A 250 after DATA is not delivery. It is "the server accepted the message into its queue." The relay may still lose it. RFC 5321 §4.2.1 defines six classes of outcome that a faithful worker must keep separate:

- transport_blocked: the connection never opened, or opened and was killed before DATA
- rejected_temporary: a 4xx response, retriable
- retries_exhausted: 4xx that survived the retry budget
- rejected_permanent: a 5xx response, never retriable
- accepted_by_server: a 250 after the end-of-data marker (the byte sequence that ends the DATA payload)
- unknown: a failure after the end-of-data marker, where the server may or may not have the message

A phase-aware wrapper maps protocol phases to these classes:

```python
def classify_smtp_outcome(phase, code, after_end_of_data, retries_remaining=0):
    if phase == "channel":
        return "transport_blocked"
    if phase == "message":
        if 400 <= code < 500:
            return "retries_exhausted" if retries_remaining <= 0 else "rejected_temporary"
        return "rejected_permanent"
    if code == 250 and after_end_of_data:
        return "accepted_by_server"
    return "unknown"
```

The split matters because each class implies a different next action. accepted_by_server does not imply "delivered." It implies "the relay said yes, and we have no further signal." retries_exhausted implies "stop, surface to staff." unknown implies "we will never know from SMTP alone; reconciliation has to settle this." Treating unknown as accepted is how duplicate sends start. Treating unknown as rejected is how silent loss starts.

The obvious alternative is to treat the SMTP response as a boolean: success or failure. That collapses rejected_permanent and retries_exhausted into "no," which destroys the audit trail. It collapses accepted_by_server and unknown into "yes," which is how workers start resending messages the server already accepted. A boolean log is the most expensive kind of audit, because the next person to read it has to guess what was lost.

## The third receipt: reconciliation against admissible evidence

The third receipt is the one that closes the loop. Before any resend, the worker reconciles against admissible evidence. Admissible evidence, in this design, has four required fields: origin (the From: identity on the wire), Message-ID, recipient, and a canonical digest of the original bytes. All four must match. The worker's reconcile step, ReconcileSend, refuses anything that lacks all four.

```python
REQUIRED_FIELDS = ("origin", "message_id", "recipient", "canonical_digest")

def is_admissible(evidence):
    return all(evidence.get(k) for k in REQUIRED_FIELDS)
```

That last sentence is the part that takes the longest to internalize. A copy Catalyst filed itself is not evidence. APPEND proves the IMAP server received the bytes, not that the recipient did, per RFC 9051 §6.3.12. Without admissible evidence, the worker will resend. Internal state alone resends too. Admissible evidence is the only thing that breaks the loop.

The remaining case is unknown. An unknown stays unknown and goes to staff via decide_uncertain_send, the staff action that records an immutable resolution to a send with unknown outcome. The three resolutions are abandon (close the item, do not resend), authorize_resend (open a new series that cancels the held one), and revise (publish a superseding message that replaces the held one). No code path resends on the network's word.

## Why not just trust the SMTP response

Three concrete failures fall out of trusting the SMTP response as a boolean.

1. The server returns 250, the message vanishes in the relay, the worker reports success, and the recipient never gets it. There is no signal to retry against.
2. The server returns 250, the worker never sees the response because of a network drop on the response channel, the worker retries, and the recipient gets the message twice.
3. The server returns a failure after the end-of-data marker. The worker cannot tell whether the server accepted the message and lost the response, or whether the server rejected it. Either way, resending risks a duplicate. Not resending risks a loss.

The three receipts answer each of these. The frozen ApprovedMessage gives the worker a target. Phase classification tells the worker what kind of failure it is. Admissible evidence is the only thing the worker trusts to break the tie. The worker's reconcile step then collapses the ambiguity into a single recorded decision.

```python
def reconcile(approved, evidence):
    if not is_admissible(evidence):
        return escalate_to_staff(approved, reason="no_admissible_evidence")
    if not matches(approved, evidence):
        return escalate_to_staff(approved, reason="evidence_mismatch")
    return resolve(approved, code="accepted_by_evidence")
```

## What the build looked like

The implementation landed in three passes. The first was the design: a 1,012-line specification covering nine corrections and decisions D-27 through D-32, owner-approved at v0.3.2. Independent QA found 2 BLOCKER, 4 HIGH, 10 MEDIUM, and 6 LOW. The re-check verified 18 of 22 as resolved; v0.3.2 closed the remaining 4.

The second pass was the foundation: 2,700 lines across 25 files, 401 tests in 330.73 seconds. The phase-classification wrapper, the frozen ApprovedMessage model, and the ReconcileSend worker landed together. The worker ledger, a row-based attempt tracker, gained finish(due_in=...) for scheduled deferrals at the database clock plus an offset, finish(status=held) for non-terminal holds, refund_attempt to release any status, and fence(claim) to extend a lease inside a transaction. None of those primitives touch the wire; they exist to keep the worker honest about when it has, and has not, made a real attempt.

The third pass was the review. 329 additions across 10 files, 240 of them in the test suite, taking the total to 424 tests in 434.34 seconds. The re-check found no BLOCKER or HIGH; one new MEDIUM and three LOW remained. A follow-up fix tightened one detail: when ReconcileSend records accepted_by_evidence, it resolves the message's open send items with the same code, and a system actor writes the immutable resolution. Before that, a stuck open send item could keep the uncertain-sends health gate (G3) alarming even after evidence arrived. The reconcile-key path now reports reconcile_key_malformed instead of crashing on a missing ApprovedMessage.

## What stays in the audit

The pattern is the audit, not the spec. Every disposition change to an ApprovedMessage is an immutable row. Every reconcile step writes its inputs and its decision. Every staff action through decide_uncertain_send is recorded. A reader three months from now can ask "did this message get sent, and how do we know," and the system can answer with rows, not with someone's recollection.

The full specification (1,012 lines, decisions D-27 through D-32, the nine corrections) lives in 000-docs (each repo's numbered folder of dated records) at the [correspondence specification](https://github.com/intent-solutions-io/catalyst-onboarding-v2/blob/main/000-docs/016-AT-DSGN-p2-correspondence-specification.md).

## Use this

- Freeze the bytes that go on the wire at the moment of enqueue, not the moment of template change.
- Classify SMTP outcomes by protocol phase (RFC 5321 §4.2.1), not by a single success/failure boolean.
- Reconcile against admissible evidence (origin, Message-ID, recipient, canonical digest) before any resend, and route everything else to staff.

## FAQ

### What does an SMTP 250 actually mean?

A 250 after the end-of-data marker is the relay saying the server accepted the message into its queue. It is not delivery. The relay may still lose the message, and the worker has no further protocol signal to confirm the intended recipient received it.

### Why is APPEND not delivery?

APPEND proves the IMAP server received the bytes the worker handed it, per RFC 9051 §6.3.12. It does not prove the recipient saw or fetched the message. Treating APPEND as delivery is how reconciliation starts trusting its own writes instead of admissible evidence.

### What counts as admissible evidence?

Four required fields must all match the ApprovedMessage: origin (the From: identity on the wire), Message-ID, recipient, and a canonical digest of the original bytes. ReconcileSend refuses any evidence missing one of those four. A retry that consults only internal state will resend. A retry that consults admissible evidence will not.

### What happens when a send outcome is unknown?

The unknown stays unknown and goes to staff through decide_uncertain_send, which records an immutable resolution. Three resolutions exist: abandon (close the item, do not resend), authorize_resend (open a new series that cancels the held one), and revise (publish a superseding message that replaces the held one). No code path resends on the network word alone.

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {"@type": "Question", "name": "What does an SMTP 250 actually mean?", "acceptedAnswer": {"@type": "Answer", "text": "A 250 after the end-of-data marker is the relay saying the server accepted the message into its queue. It is not delivery. The relay may still lose the message, and the worker has no further protocol signal to confirm the intended recipient received it."}},
    {"@type": "Question", "name": "Why is APPEND not delivery?", "acceptedAnswer": {"@type": "Answer", "text": "APPEND proves the IMAP server received the bytes the worker handed it, per RFC 9051 Section 6.3.12. It does not prove the recipient saw or fetched the message. Treating APPEND as delivery is how reconciliation starts trusting its own writes instead of admissible evidence."}},
    {"@type": "Question", "name": "What counts as admissible evidence?", "acceptedAnswer": {"@type": "Answer", "text": "Four required fields must all match the ApprovedMessage: origin (the From: identity on the wire), Message-ID, recipient, and a canonical digest of the original bytes. ReconcileSend refuses any evidence missing one of those four. A retry that consults only internal state will resend. A retry that consults admissible evidence will not."}},
    {"@type": "Question", "name": "What happens when a send outcome is unknown?", "acceptedAnswer": {"@type": "Answer", "text": "The unknown stays unknown and goes to staff through decide_uncertain_send, which records an immutable resolution. Three resolutions exist: abandon (close the item, do not resend), authorize_resend (open a new series that cancels the held one), and revise (publish a superseding message that replaces the held one). No code path resends on the network word alone."}}
  ]
}
</script>

## Related Posts

- [Propagation day: when the spec becomes the migration plan]({{< ref "propagation-day-when-the-spec-becomes-the-migration-plan.md" >}})
- [Parked refactor: five receipts]({{< ref "parked-refactor-five-receipts.md" >}})
- [Park the cutover, keep the work]({{< ref "park-the-cutover-keep-the-work.md" >}})