+++
title = 'Verify Audit Evidence with a Signed Payload, Not by Format'
slug = 'verify-audit-evidence-with-signed-payload-not-by-format'
date = 2026-10-12T08:00:00-06:00
draft = false
tags = ["audit", "evidence", "supply-chain", "signed-payload", "in-toto"]
categories = ["Technical Deep-Dive"]
description = "When eight audit-evidence publishers each emit a different format, one canonical signed payload gives one verifier a tampering signal without erasing history."
tldr = "An audit pipeline that lets each publisher pick its own evidence format cannot tell tampering from a legitimate format evolution, so the consumer has nowhere to anchor 'last good.' The fix is one canonical signed statement payload, one consumer that verifies by signature, and a preserved last-verified snapshot whenever a mutation is rejected. Eight publishers on intent-eval-platform migrated to that pattern; six tampering checks are now rejected without losing history."
+++

When many audit-evidence publishers (the systems that produce signed rows of evidence) each emit a different shape and the consumer checks signatures case by case, a tampered row is indistinguishable from a legitimate format change. The consumer has no place to anchor "last good state," so any verification failure either erases history or silently keeps going.

A reader running an audit trail or evidence pipeline across multiple publishers and one consumer can adopt a different shape this week. One canonical signed statement payload (a fixed envelope of kernel version plus payload plus signature that every publisher fills in identically), one verifier that checks by signature, a preserved snapshot on every rejection. That is what cut this pipeline's tampering failures from "ambiguous" to "rejected with history preserved."

## How do you verify audit evidence from multiple publishers?

Adopt one canonical signed statement payload: a fixed envelope of kernel version plus payload plus signature that every publisher fills in identically. One verifier parses the envelope, recomputes the digest over the canonical predicate bytes, and checks the signature against the public key named in the envelope. Format evolution shows up as a signature failure; tampering shows up as a signature failure; the two are no longer distinguishable to a silent verifier. A preserved last-verified snapshot rides with every rejection so the dashboard can answer what the system believed yesterday without needing yesterday's process to be alive.

## The format-evolution trap

The natural reflex is to keep adapting the verifier. Each publisher says its evidence grew up: a new field, a renamed key, a moved nested block. The verifier grows a new branch for each, and the test matrix grows with it. The signed-payload approach is to stop growing the verifier at all and stop asking the verifier to know any individual publisher's shape. The signature binds to the digest of the full payload bytes; the verifier either trusts that digest matches the signed payload or it does not.

What makes this load bearing is that the failure mode is silent. A coerced signature over a slightly different payload passes a content check and fails a signature check. Both look like progress on a glance: the row got bigger, a field appeared, the count went up. The dashboard in this case was logging "verified" against a local witness and "rejected" against the kernel-signed digest, and the two tables had been drifting apart for three nights before anyone noticed.

The audit-harness (the in-repo package of deterministic test-quality checks) release carried a verified registry signature and provenance attestation on 2026-10-12, and that is what made the change carry weight. The pipeline was not adopting a new idea; it was adopting a long-standing in-toto-style attestation pattern that the harness had already shipped.

## The one canonical statement payload

Every publisher now emits the same shape: a kernel-versioned envelope with a typed statement, a predicate payload under it, a digest over the canonical predicate bytes, and a signature bound to that digest. The kernel version is part of the bytes that get signed, so a version bump cannot pass as the same payload. The payload bytes follow; the digest covers them; the signature covers the envelope plus the digest.

```text
statement:
  kernel: "audit-payload/v1"
  subject:
    - name: "publisher-name"
      digest: { sha256: "<hex>" }
  predicate:
    type: "https://intent-eval-platform.io/predicate/<kind>"
    payload:
      <canonical JSON: keys sorted, no whitespace, RFC 8785>
  metadata:
    build_at: "2026-10-12T13:45:00Z"
    source: "<publisher repo>"
envelope:
  digest: { sha256: "<hex of canonical predicate bytes>" }
  signature:
    pub_key_id: "<fingerprint>"
    value: "<base64>"
```

The kernel is the only component the verifier needs to know. Below the kernel, payloads are opaque to the verifier; their shape belongs to the publisher that emits them. Above the kernel, signatures travel with rows. The witness table only needs three columns: `subject`, `digest`, `signature`.

This is the reverse of how multi-publisher audits usually grow. The usual pressure is "the consumer has to understand the publisher," which pushes every format decision into the consumer. Inverting that pressure means every format decision lives with the publisher; the consumer only verifies that the signature covers the kernel and the digest.

## One consumer, verification by signature

The dashboard verifier does three things in order, and only those three. It parses the envelope, recomputes the digest over the canonical predicate bytes, and checks the signature against the public key named in the envelope. A rejection at any step moves the row into a holding area; a pass moves it into the witness table under the subject digest.

```python
def verify(envelope: dict, keyring: Keyring) -> Verdict:
    kernel = envelope["statement"]["kernel"]
    if kernel != SUPPORTED_KERNEL:
        return Verdict.reject(kernel_unsupported=kernel)

    predicate_bytes = canonicalize(envelope["statement"]["predicate"])
    expected = sha256(predicate_bytes).hexdigest()
    declared = envelope["envelope"]["digest"]["sha256"]
    if expected != declared:
        return Verdict.reject(digest_mismatch={
            "declared": declared, "recomputed": expected})

    pub = keyring.lookup(envelope["envelope"]["signature"]["pub_key_id"])
    if pub is None:
        return Verdict.reject(unknown_key=...)

    if not pub.verify(predicate_bytes, envelope["envelope"]["signature"]["value"]):
        return Verdict.reject(bad_signature=True)

    return Verdict.accept(subject=envelope["statement"]["subject"],
                          digest=expected,
                          signature=envelope["envelope"]["signature"])
```

The verifier does not branch on predicate type, publisher, or layout. If a publisher adds a field, the canonicalizer's output changes, the digest changes, and the signature has to follow or verification fails. Format evolution shows up as a signature failure; that is the design, not a defect.

## When verification fails, hold the last good snapshot

A rejection is supposed to be an event the system keeps, not one it papers over. The tamper-evident holding area preserves the rejected envelope verbatim; the witness table keeps the last accepted row for that subject. A mutation that does not pass is a mutation the consumer has not yet agreed on, and the right answer is to surface that without erasing what already passed.

```python
def apply(verdict: Verdict, store: Store, snapshot: Snapshot) -> ApplyResult:
    if verdict.kind == "reject":
        store.rejections.append({
            "envelope": verdict.envelope,
            "reason": verdict.reason,
            "received_at": utcnow(),
        })
        store.rejections.prune(keep_last=REJECTION_WINDOW)
        return ApplyResult.held(
            last_known=store.witnesses.get(verdict.subject),
            rejection=verdict.reason)

    store.witnesses[verdict.subject] = verdict.digest
    snapshot.persist(verdict.subject, verdict.digest, verdict.signature)
    return ApplyResult.accepted(
        subject=verdict.subject, digest=verdict.digest)
```

The snapshot sits alongside the witness table for the same reason the witness table is keyed by subject digest. The dashboard can answer "what did the system believe yesterday?" without needing yesterday's process to be alive. That is the property that broke before, when a forced schema migration overwrote the witness table with a partially-verified copy.

## What got shipped

Six rejections in cross-repository tests covered the cases the old verifier could not tell apart: a single-byte payload mutation, a canonicalization difference on whitespace, a key id not in the ring, a signature over a tampered digest, a kernel version one off, and a payload reordered against an older row. Each rejection kept the witness for its subject. None of them caused history loss.

J-Rig (an internal governed evidence publisher) emitted fourteen canonical rows from the merged commit on the night of 2026-10-12. All fourteen verify against the dashboard signature path on the same day. J-Rig's twenty-four payload contracts pass across kernel versions 0.10.0 and 0.11.0; a stricter type check is now in CI for the test-only mismatch between the branded types in those versions.

A second finding came out of the same session: the trace-intelligence program's dependency graph needed 438 edges added to align final review and production-adoption with their prerequisites. The graph was repaired without changing ownership, acceptance criteria, or completion states. The collision between the two is the one to surface: a missing migration record and a missing dependency edge are both evidence the system was lying to itself about state; the same cross-repo fix path surfaced both, and neither was visible from the dashboard before it landed.

A real failure worth keeping. The scanner adapter had been treating gitleaks's exit-1 as a policy finding, conflating scanner crashes with findings. A contract-test surface reproduces this now, and required-missing-tool behavior stays advisory instead of silently raising real findings. The adapter is no longer a place where the verifier has to second-guess the publisher's report.

## Why not the obvious approach?

Two alternatives were on the table. The first was a richer schema with publisher-specific extensions and a per-publisher verifier; the second was a content-addressed store that names files by their hash and trusts whoever can read them.

The richer schema pushes the format-decision pressure the wrong way. Every new field forces the consumer to learn a shape it does not own, and a tampered field reads as a new field until someone diffs the schema. The cross-repository tests in this pipeline had eight publisher schemas to maintain, and three of them were already a quarter behind. A per-publisher verifier is the natural extension of that path; it does not survive the next publisher.

The content-addressed store is closer to the working shape, but it answers the wrong question. A digest proves the bytes are intact; it does not prove the publisher had the right to issue them. A row whose digest matches but whose signing key is not in the ring still passes. The signed envelope binds the digest to a key id, and the verifier's second step is the only place that check lives.

A real reversal surfaced in the J-Rig kernel compatibility work. The earlier verifier accepted a "legacy fallback" branch so older J-Rig rows would not be lost on the cutover; that branch was a place a tampered payload could land without the witness table noticing. Removing the fallback is what makes the dashboard reject every J-Rig row that comes through the tampering or fallback branch today; the fourteen nightly rows verify on the canonical path. Keeping the old rows was the wrong kind of compatibility. The right kind is keeping the witness for the same subject, not the same shape.

## Use this

- Pick one canonical signed payload shape for every publisher in the pipeline. Kernel version plus payload digest plus signature. Anything below the kernel is the publisher's choice; anything above is the signature's. Format evolution shows up as a signature failure, not as a silent accept.
- Move verification out of every publisher-specific verifier. One consumer, one supported kernel, one signature check. Rejections are a feature. Cross-repo tests should treat new publishers as an unknown key id, not as a new branch.
- Preserve the last good witness for every subject on every rejection. The dashboard answers "what did we believe yesterday?" by reading the witness table, which means the witness table has to survive the rejection that pointed at a tampered payload.

The full migration is live on [intent-eval-platform.io](https://intent-eval-platform.io): eight publishers, one verifier, the J-Rig nightly run, and audit-harness 1.5.1 on the registry with verified provenance.

## FAQ

### How do you verify audit evidence from multiple publishers?

Adopt one canonical signed statement payload: a fixed envelope of kernel version plus payload plus signature that every publisher fills in identically. One verifier parses the envelope, recomputes the digest over the canonical predicate bytes, and checks the signature against the public key named in the envelope. Format evolution shows up as a signature failure; tampering shows up as a signature failure; the two are no longer distinguishable to a silent verifier.

### What is a signed statement payload in an audit pipeline?

A fixed envelope containing a typed statement, a payload digest, and a signature bound to that digest. Every publisher fills in the same envelope; payloads below the kernel can be any shape the publisher chooses. The signature covers the digest plus the envelope, so a single-byte payload mutation or a canonicalization difference on whitespace fails the check while legitimate history still verifies.

### What should a verifier do when an audit row fails verification?

Move the rejected envelope verbatim into a holding area; keep the last accepted row for that subject in the witness table; persist the last-known-good snapshot so the dashboard can answer what the system believed yesterday without needing yesterday's process to be alive. A rejection is an event the system keeps, not one it papers over.

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How do you verify audit evidence from multiple publishers?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Adopt one canonical signed statement payload: a fixed envelope of kernel version plus payload plus signature that every publisher fills in identically. One verifier parses the envelope, recomputes the digest over the canonical predicate bytes, and checks the signature against the public key named in the envelope. Format evolution shows up as a signature failure; tampering shows up as a signature failure; the two are no longer distinguishable to a silent verifier."
      }
    },
    {
      "@type": "Question",
      "name": "What is a signed statement payload in an audit pipeline?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A fixed envelope containing a typed statement, a payload digest, and a signature bound to that digest. Every publisher fills in the same envelope; payloads below the kernel can be any shape the publisher chooses. The signature covers the digest plus the envelope, so a single-byte payload mutation or a canonicalization difference on whitespace fails the check while legitimate history still verifies."
      }
    },
    {
      "@type": "Question",
      "name": "What should a verifier do when an audit row fails verification?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Move the rejected envelope verbatim into a holding area; keep the last accepted row for that subject in the witness table; persist the last-known-good snapshot so the dashboard can answer what the system believed yesterday without needing yesterday's process to be alive. A rejection is an event the system keeps, not one it papers over."
      }
    }
  ]
}
</script>

## Related Posts

- [Name the Single Authority in a Daily Pipeline]({{< ref "name-the-single-authority-in-a-daily-pipeline.md" >}}) - Why one named owner per concern beats committee routing in a daily pipeline
- [Three-Pass Settlement for a Recurring AI Pipeline Contract]({{< ref "three-pass-settlement-recurring-ai-pipeline-contract.md" >}}) - How three passes (producer, settlement, audit) settle a recurring AI pipeline contract
- [Exit Zero Is Not Push OK]({{< ref "exit-zero-is-not-push-ok.md" >}}) - A cron that reports OK after a failed git rebase is a load-bearing lie
