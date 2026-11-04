+++
title = 'Pin the Eval Dataset With a SHA-256 Digest From the Caller'
slug = 'pin-the-eval-dataset-sha256-digest-from-the-caller'
date = 2026-11-03T08:00:00-06:00
draft = false
tags = ["testing", "ai-agents", "architecture", "typescript"]
categories = ["AI Engineering"]
description = "An eval score is a claim about the bytes it scored. Pin the eval dataset with a SHA-256 digest from the caller, and freeze what an approved revision held."
tldr = "A passing eval score describes only the exact bytes that were scored, so the review-agent-eval runner takes the dataset's SHA-256 from the caller instead of reading a digest out of the dataset's own manifest. Every later revision pins the previous manifest's digest, and the caller supplies the previous manifest itself. The runner refuses any change to an already approved case, label, stratum or threshold. Every summary still reports humanAuthorizationVerified as false, because a digest proves bytes and not a person."
+++

A green evaluation score reads like a claim about the model's behavior, but the expected answers, the inputs and the score a run has to reach can all change under you, and the run stays green across the change. This post covers the fix: the runner (the program that verifies the dataset and scores supplied predictions) takes a SHA-256 digest (a fingerprint of the exact bytes) of the evaluation dataset from the caller (whatever invokes the runner, a person or a CI job), not from the dataset itself.

Scoring the expected answers that ship with a dataset cannot detect a changed dataset. A digest stored inside the dataset is not a sign-off either. It is more data inside the thing being judged.

Approval has to live outside the dataset. A version of it counts as approved when whoever runs the evaluation holds a digest of that version's exact bytes. That digest covers the manifest (the index file listing every case and the hash of that case's bytes), and every later version has to keep every case an approved version already contained.

## Where the digest comes from

The caller passes the expected digest as an option on the runner, with a comment saying it is supplied independently of the dataset and not read from its own manifest. The runner hashes the manifest bytes and compares them against the value it was handed:

```typescript
function parseManifest(bytes: Buffer, expected: string) {
  Hash.parse(expected);
  if (sha256(bytes) !== expected) refuse();
  const manifest = Manifest.parse(json(bytes));
  if (new Set(manifest.cases.map((item) => item.id)).size !== manifest.cases.length) refuse();
  if ((manifest.revision === 1) !== (manifest.previousManifestSha256 === null)) refuse();
  return manifest;
}
```

The digest is a statement about bytes, so a dataset cannot vouch for itself. The manifest is still parsed as a schema, so a file with the right bytes and the wrong shape is refused.

Approval of a revision and approval of the labels inside it are two different things. The approval a revision carries is the digest held outside the dataset, and whoever holds it approved that revision. The runner confers no approval of its own, and it never claims a human approved the labels.

Every selected case gets the same treatment. A case is an id, one input, the label it should get, the stratum (the group it belongs to), and a marker recording where the label came from. Reads are bounded to 1 MiB per file and 64 MiB for the manifest plus its selected cases. The runner opens with `O_NOFOLLOW` and `O_NONBLOCK`, refuses a link count other than one, refuses a symlink, a redirected ancestor or a non-regular file, and rechecks the manifest and the selected cases at the end of the capture.

## Freezing the cases an earlier revision covered

Adding cases is allowed. Changing anything an earlier approved revision already contained is not.

The manifest counts each version of the dataset as a revision. Revision one has a null predecessor and refuses a supplied prior checkpoint. Every later revision needs both the previous manifest file and an independently trusted digest for it, matching the predecessor the manifest declares. The prior manifest is schema and hash checked on its own. Then the new revision has to advance by exactly one, keep the same dataset id, the same kind and the same recall floors, keep every prior case in order, and add at least one case.

```typescript
  if (
    prior.revision + 1 !== manifest.revision ||
    prior.datasetId !== manifest.datasetId ||
    prior.kind !== manifest.kind ||
    JSON.stringify(prior.recallFloors) !== JSON.stringify(manifest.recallFloors) ||
    prior.cases.length >= manifest.cases.length
  )
    refuse();
  for (const [index, item] of prior.cases.entries()) {
    const next = manifest.cases[index];
    if (!next || item.id !== next.id || item.sha256 !== next.sha256) refuse();
  }
```

A changed case id, a changed case hash, a deleted case, a reordered case, a replaced label, a replaced input, a replaced stratum or a moved floor all refuse. The current case bytes still have to match the hashes the earlier approved revision covered, so an editor who re-hashes the modified case and re-hashes the manifest on top of it still gets refused. A new approved digest is still required for the addition. The check never grants approval. It only refuses to lose the approval that already exists.

## What the summary refuses to say

Here is where I would push back on the word verified. The summary always carries `humanAuthorizationVerified: false`, even when the manifest declares its kind as human reviewed. The digest binds the labels by case hash, the input bytes, the thresholds, the provenance declaration and the revision metadata. That proves which bytes were scored. It does not prove who approved them, when, or which genuine human dispositions back a human-reviewed dataset. A disposition marker or a hash of a reviewer record does not authenticate a person.

The prediction file has to name the same manifest digest, and a case with no prediction row stays a scored miss. The exit codes carry the same restraint. Exit 0 means verified evidence or a passing score. Exit 1 means a recall or support failure. Exit 2 means invalid usage or evidence. Neither exit 0 nor the word verified establishes human approval or production readiness.

## Breaking the check on purpose

The self-test starts real runner processes and checks their JSON responses and exit statuses. Nine child checks run, each expecting a specific exit status.

- manifest integrity (exit 0)
- perfect predictions (exit 0)
- constant HOLD misses (exit 1)
- missing predictions counted as misses (exit 1)
- perfect observed classes unable to mask missing HOLD support (exit 1)
- case mutation (exit 2)
- independent pin mismatch (exit 2)
- an approved checkpoint preserved on an addition (exit 0)
- a re-pin attempt unable to erase an approved label (exit 2)

The last check edits an already approved case, re-hashes it, re-hashes the manifest, supplies the new digest, and the runner still refuses. That check matters more than the others, because the design rests on it.

Removing the final case recheck, the pass that re-stamps every selected case once the capture is done, made the late-case mutation control fail. That control changes a case file after the runner has already read it, and expects the runner to refuse. Restoring the check made it pass again. That is a local mutation observation, not a failing historical CI run. It is still the evidence that the control bites.

A second failure came out of the same pull request. The root TypeScript build had been leaving out the eval package, so the compiled CLI never existed to be tested. Adding a subprocess check for the compiled runner exposed the missing output. Both failures were found by the shape of the change rather than caused by it: one a deliberately planted defect, the other a pre-existing omission in the root build that this change repaired.

Final verification on the frozen source: 4,419 tests passed with five optional skips, 288 test files passing and two skipped, and ten repository verification gates exited zero. Coverage came out at 89.03% statements, 84.50% branches, 91.46% functions and 90.12% lines. There are 71 new controls, including source and compiled subprocess self-tests, each exercising the nine child checks.

## Running it

The runner is `review-agent-eval`. It takes `--verify-manifest` or `--score PREDICTIONS.json`, along with `--eval-root DIR` and `--manifest-sha256 SHA`. A revision also takes `--previous-manifest FILE` and `--previous-sha256 SHA`. There is a `--self-test` mode that runs the nine child checks. The package script is `pnpm --filter @qmd-team-intent-kb/eval-surface review:eval`, and after a build the same flags work against `node packages/eval-surface/dist/review-agent-eval-cli.js`. Digest approval and human label provenance belong to the caller, and no operational qualification is implied.

The change itself is in [pull request 446](https://github.com/jeremylongshore/bobs-big-brain-registrar/pull/446), merged November 3, 2026.

## Use this

- Pass the expected dataset digest from outside the dataset. A dataset that supplies its own approval has approved nothing.
- Keep the previous manifest and its digest with every revision, and treat a refusal to preserve an approved case as a genuine failure rather than a formatting nit.
- Read a passing score as a claim about bytes. If the report has to say a person approved the labels, that has to come from somewhere other than the dataset.

## Related Posts

- [Every Verdict Carries the Scope It Actually Ran](/posts/a-green-result-only-covers-what-it-ran/)
- [A Path Is Not Proof of Identity](/posts/a-path-is-not-proof-of-identity/)
- [Verify Audit Evidence with a Signed Payload, Not by Format](/posts/verify-audit-evidence-with-signed-payload-not-by-format/)
