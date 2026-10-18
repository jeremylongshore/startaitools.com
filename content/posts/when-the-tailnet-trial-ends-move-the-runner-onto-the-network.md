+++
title = 'Move the deploy runner onto the tailnet, skip Tailscale OIDC'
slug = 'when-the-tailnet-trial-ends-move-the-runner-onto-the-network'
date = 2026-10-17T10:00:00-06:00
draft = false
tags = ["github-actions", "tailscale", "self-hosted-runners", "vps-deploy", "release-engineering", "ci-cd"]
categories = ["Technical Deep-Dive"]
description = "Move the GitHub Actions deploy runner onto the tailnet, skip the ephemeral Tailscale OIDC handshake. Add join-tailnet and send-revision toggles."
tldr = "When the deploy runner can already be a tailnet member, ephemeral Tailscale key minting is the wrong default for a reusable deploy workflow. Add an opt-in join-tailnet boolean to the workflow, fall back to a plain TCP check of the VPS SSH port over the runner's own tailnet route, and add a send-revision opt-out for callers whose VPS-side deploy script only accepts an empty command. A hosted runner that mints an ephemeral auth key every deploy will 402 the moment the tailnet's free trial ends; a runner that is already on the tailnet reaches the VPS with no new key."
+++

When a deploy needs a fresh login token every run, and the broker that issues those tokens stops being free, the token call returns 402 Payment Required and the rest of the job still reports success. Production stays on the previous build for days. What you have at the end of this post is a GitHub Actions deploy workflow with two settings any caller can flip (join-tailnet: false, and send-revision: false), a mode where the runner is already a member of the private network and so does not need to mint a token at all, and the order in which to migrate each repo that calls this workflow one at a time.

On 2026-10-14, every deploy through one shared VPS deploy workflow failed the same way: a 402 Payment Required from Tailscale on the first call to mint a short-lived network token, because the Tailscale account (the VPN that brokers access to a private mesh network, called a tailnet) had been moved off its free trial the same day. The run summary said `success` on every check. The merged commits landed in GitHub. Production stayed on the previous build until someone read the deploy log line by line, two days later.

This is what a paid-tier expiry looks like when the only path from the runner to the production host is a token-mint handshake. The fix is not renewing the trial. The fix is making network membership the runner's job, not the workflow's.

## What the old deploy job actually did

The old deploy shape, repeated across every consumer of the reusable workflow, looked roughly like this:

1. Mint an ephemeral Tailscale auth key by exchanging a GitHub Actions OIDC token against a federated trust.
2. Use the key to bring the hosted runner onto the tailnet as a node tagged `tag:ci`.
3. SSH to the production host as the deploy user, run the VPS-resident deploy script.
4. The auth key expires. The runner node drops off the tailnet.

Step 1 is a single API call. Step 2 needs the key in hand. Step 3 is the actual deploy. The whole thing runs in roughly a minute.

When step 1 returned 402, step 2 never ran. The runner stayed off the tailnet. Step 3 ran in the wrong context (the runner was never on the tailnet, so it could not reach the VPS over its Tailscale hostname) and the deploy job reported `success` anyway, because the SSH step was wrapped in a way that did not propagate the upstream 402.

(SSH_ORIGINAL_COMMAND is the variable an SSH forced-command script reads for the command the client tried to run.)

## The reusable workflow change

The reusable workflow lives in `.github` (the repo that holds the shared CI assets). Two new inputs declared on `on.workflow_call`:

```yaml
on:
  workflow_call:
    inputs:
      runs-on:
        type: string
        default: 'ubuntu-latest'
      join-tailnet:
        type: boolean
        default: true
```

`runs-on` (string, default `ubuntu-latest`) picks the deploy job's runner. `join-tailnet` (boolean, default `true`) gates the two Tailscale steps. With `join-tailnet: false`, the OIDC trust exchange and the `tailscale up` step are skipped entirely, and a plain TCP check of the VPS SSH port over the runner's own tailnet route replaces them. The two Tailscale inputs (`TS_OIDC_CLIENT_ID`, `TS_AUDIENCE`) become optional in that mode because the mode never uses them.

The default stays `true`. Every caller pins the workflow by SHA, so callers migrate one at a time, each with its own deploy as proof. That is the design choice worth defending below.

## The TCP-only health check

When `join-tailnet` is `false`, the workflow replaces the OIDC exchange and the `tailscale up` step with a single TCP probe of the VPS SSH port over the runner host's own tailnet route. The shape:

```bash
# Inside the deploy job, when inputs.join-tailnet is false.
nc -z "$VPS_HOST" 22 || {
  echo "::error::cannot reach $VPS_HOST:22 over tailnet"
  exit 1
}
```

The probe is intentionally minimal. It mints nothing, authenticates nothing, logs into nothing. It only proves the runner can reach the VPS SSH port over its own tailnet route, which is exactly the precondition step 3 needs.

This is the no-join fallback. The self-hosted runner is already a tailnet member because it lives on the runner host, which has been a tailnet member since before this workflow existed. The runner reaches the VPS over the same Tailscale hostname the hosted runner would have reached after a successful `tailscale up`. The TCP probe is the gate that proves the route exists, then the deploy SSH step runs the same way it always has.

## The send-revision toggle

A second caller-facing boolean landed the same day, also declared on `on.workflow_call`:

```yaml
on:
  workflow_call:
    inputs:
      send-revision:
        type: boolean
        default: true
```

Default `true`. When `true`, the deploy step passes the merged PR's HEAD SHA to the VPS-side script as `github.sha`. When `false`, the deploy step connects with no remote command, so `SSH_ORIGINAL_COMMAND` is empty.

Why: at least one consumer's VPS-resident deploy script is a hardened forced command that accepts only an empty command. It captures current main itself, preflights the live site, and deploys that exact commit with a database backup and rollback path. The first deploy on the self-hosted runner exited 64 because the reusable workflow always sends `github.sha`. The exit code propagated up; the run summary finally showed red.

The opt-out preserves the hardening. The VPS-side script is owned by its own repo's release process and refuses arguments on purpose. Changing it to accept an argument would weaken the contract that the manual-install path depends on. Changing the workflow to send nothing when a caller asks for nothing is the smaller change.

## The opt-in, not the flip

The deploy workflow change is two inputs, both default to the old behaviour, both opt-in per caller. That is the load-bearing design choice, and it is worth stating the alternatives.

Flipping the default would migrate every caller at once. That is also the change that hides failures: a caller who skipped the changelog would see a deploy run on an unexpected runner, and the next time a real bug shows up, no one can tell which runner ran it. Every caller pins the workflow by SHA. They are the unit of migration. Each caller flips `join-tailnet` on its own deploy, watches its own run, and only then does the next caller move.

Keeping the default at `true` also keeps the change self-documenting in caller repos. A `with: join-tailnet: false` line in a caller workflow is the visible signal that this caller is on the new mode. A blanket default flip would erase that signal.

## The first consumer: startaitools.com

The first consumer to flip was startaitools.com itself. Its deploy workflow already called the shared `.github` reusable deploy, so flipping was a single workflow-input change plus the consumer-side runner label so GitHub knew where to dispatch the job. The merged change shipped the same day, the deploy landed on the self-hosted runner, and the run summary finally showed a deploy that did not require a working Tailscale account to even start.

That is the proof pattern. One caller migrates, one deploy proves the mode works for that caller, and only then does the next caller move. The runner host is the existing self-hosted runner platform and is already a tailnet member, so the change at the runner side was zero new code.

## Why not just renew the trial

Renewing the Tailscale plan restores this single outage. The reason to still install the opt-in is that "renew this one credential" is not a class-of-failure fix.

Every OIDC handshake that mints a short-lived credential is a vendor handshake. Tailscale OIDC is one example. A custom OIDC issuer pointed at your cloud rotates every 90 days. A GitHub App installation token can be revoked by an org admin who never thinks about your deploy. An IAM trust policy edit on the cloud side breaks the handshake the same way: 403, 401, or 402, deep in the run summary, with the rest of the deploy job looking fine. Any of these would have cost the same two days of stale production.

Moving the runner onto the network removes the handshake from the deploy path. The deploy becomes a TCP probe plus an SSH. The TCP probe depends on the runner host still being a tailnet member, which is a runner-host lifecycle question, not a vendor question. The SSH depends on the deploy user's SSH key, which the operator has regardless of vendor state.

## Why not edit the VPS-side script instead

The send-revision toggle exists because at least one VPS-resident deploy script is a hardened forced command that only accepts an empty command. The natural reflex is to relax it: "accept an optional argument, ignore it if empty, run the deploy with whatever revision the runner sends." That is the wrong direction.

The hardening is owned by the repo whose deploy path it is. That repo's release process depends on the script knowing it always runs an empty command, because the script's whole behaviour (capture main, preflight, deploy, back up the database, roll back on smoke failure) assumes the caller is not in control of what gets shipped. Letting a caller pass a revision would re-introduce the divergence loophole the script was built to close. The VPS-resident script is the manual fallback path, and the manual fallback path needs to be the thing that decides what it deploys.

The reusable workflow is the shared asset that every caller already pins by SHA. Adding an opt-out is the smaller change, and it puts the decision at the right layer.

## Also shipped

- Four new tests cover the runner-mode change; the reusable workflow's suite now reports 10 passing.
- A `send-revision` boolean for callers whose VPS-side deploy script only accepts an empty command; default unchanged.
- startaitools.com is the first consumer to migrate, in the same day's release v1.33.24.

## Use this

- Add a `join-tailnet` boolean to your reusable deploy workflow, default `true`, with a TCP-only health check on the runner's own tailnet route as the no-join fallback.
- Add a `send-revision` boolean for callers whose VPS-side deploy script only accepts an empty command, default `true`, so the workflow can connect without sending `github.sha` when a caller asks.
- Migrate consumers one at a time, each with its own deploy as proof; never flip the default for every caller in one change.

Reference: the reusable workflow at `https://github.com/jeremylongshore/.github/blob/main/.github/workflows/vps-deploy.yml`.

## FAQ

### What does a hosted runner's Tailscale OIDC 402 look like inside a GitHub Actions deploy?

The OIDC step POSTs to the Tailscale issuer and receives a 402 Payment Required. The failure happens inside a sub-step that the run summary does not propagate. The rest of the deploy job continues, the job result still reports `success`, the merged commit lands in GitHub, and production stays on the previous build until the run log is read end to end.

### Why is the opt-in design safer than flipping the default for every caller at once?

Every caller pins the reusable workflow by SHA, and the unit of migration is the caller. Each caller flips the toggle on its own deploy, watches its own run, and only then does the next caller move. A blanket default flip hides which caller is on which mode; the visible `with: join-tailnet: false` line per caller is what keeps the migration self-documenting.

### What is a self-hosted runner that is already a tailnet member?

A runner whose host machine has joined the Tailscale network as a long-lived node. The runner reaches other tailnet nodes over their Tailscale hostnames without any per-deploy handshake. The runner host used for this change is already configured this way, which is why no Tailscale account is needed for the new mode.

## Related Posts

- [When a Third-Party CI Credential Expires, the Deploy Fallback Has to Already Live on the VPS](/posts/when-third-party-ci-credentials-expire-the-deploy-fallback-lives-on-the-vps/): the doctrinal predecessor; VPS-resident deploy script plus SHA-pin guard for the day a third-party CI credential expires.
- [Tailscale Federated Trust: Scope to Auth Keys, Not All](/posts/scope-federated-tailscale-trust-to-auth-keys/): narrows every deploy federated trust to `auth_keys` scope, the trust posture this change assumes is still in force.
- [VPS-as-the-Home Day 1: Eight Deploy Iterations](/posts/vps-as-the-home-day-1-eight-deploy-iterations/): the original reusable VPS deploy workflow plus Tailscale OIDC, eight iterations to land, the architecture this change extends.

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What does a hosted runner's Tailscale OIDC 402 look like inside a GitHub Actions deploy?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The OIDC step POSTs to the Tailscale issuer and receives a 402 Payment Required. The failure happens inside a sub-step that the run summary does not propagate. The rest of the deploy job continues, the job result still reports success, the merged commit lands in GitHub, and production stays on the previous build until the run log is read end to end."
      }
    },
    {
      "@type": "Question",
      "name": "Why is the opt-in design safer than flipping the default for every caller at once?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Every caller pins the reusable workflow by SHA, and the unit of migration is the caller. Each caller flips the toggle on its own deploy, watches its own run, and only then does the next caller move. A blanket default flip hides which caller is on which mode; the visible with: join-tailnet: false line per caller is what keeps the migration self-documenting."
      }
    },
    {
      "@type": "Question",
      "name": "What is a self-hosted runner that is already a tailnet member?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A runner whose host machine has joined the Tailscale network as a long-lived node. The runner reaches other tailnet nodes over their Tailscale hostnames without any per-deploy handshake. The runner host used for this change is already configured this way, which is why no Tailscale account is needed for the new mode."
      }
    }
  ]
}
</script>