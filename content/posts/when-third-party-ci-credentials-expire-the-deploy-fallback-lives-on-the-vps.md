+++
title = 'When a Third-Party CI Credential Expires, the Deploy Fallback Has to Already Live on the VPS'
slug = 'when-third-party-ci-credentials-expire-the-deploy-fallback-lives-on-the-vps'
date = 2026-10-16T08:00:00-06:00
draft = false
tags = ["github-actions", "ci-deploy", "deploy-fallback", "tailscale-oidc", "vps-deploy", "manual-deploy", "release-engineering", "third-party-credentials"]
categories = ["DevOps"]
description = "A VPS-resident deploy script plus a SHA-pin guard turns any third-party CI credential expiry into a one-line SSH recovery."
tldr = "GitHub Actions deploys that depend on Tailscale OIDC, custom OIDC issuers, or GitHub Apps silently 402 mid-job when those credentials expire, leaving PRs merged but production stale for hours or days. A VPS-resident deploy script that needs no third-party key, plus a SHA-pin guard that refuses anything other than the merged PR's HEAD, turns the next outage into a non-event. Install the script before the first CI deploy depends on it; renewal alone does not remove this class of failure."
+++

GitHub Actions deploys that depend on a third-party OIDC identity silently 402 deep in the run when that identity's plan ends, and the run summary still turns green while production stays stale. What you have at the end of this post is a VPS-resident deploy script that needs no third-party key, plus a SHA-pin guard that proves the manual path can't ship content that diverged from the merged PR, so the next expiry becomes a one-line recovery instead of a multi-day outage.

On 2026-10-14, two static-site changes shipped their merges; the CI run turned green on every check, and production stayed on the previous build. Nobody noticed for two days. The actual failure (a 402 payment-required from a third-party identity provider) was buried inside the first few seconds of a multi-minute deploy job, in a place the run summary had no reason to glance.

This is what a third-party CI credential expiry actually looks like. The fix is not "renew the credential." The fix is having a deploy script that lives on the production host, needs no third-party key, and is verified against the same content hash the merged PR introduced. With that in place, the next outage is a one-line SSH invocation; without it, the next outage is a multi-day production gap.

(OIDC issues short-lived tokens for machine identity, replacing stored secrets.) GitHub Actions steps that need to talk to a private API usually authenticate by exchanging a workload identity token for a short-lived key from the vendor's issuer. Tailscale OIDC is one example; a custom OIDC issuer pointed at your cloud, a GitHub App installation token behind an OIDC handshake, and any number of cloud IAM trust policies follow the same shape. Renewal cycles on any of those can outrun a developer who is not actively staring at the deploy log.

(VPS-resident means a deploy script on the host itself, run over SSH.) The whole point is that the fallback must not depend on the same vendor handshake that just broke. After the vendor is gone, the only credential you still have is your SSH key. The fallback has to need only that.

The day-of incident is a useful case study, but the more useful find is the pattern: every deploy script that exists on a host today was installed by hand before the first CI run that depended on it. That ordering (manual install first, CI adoption second) is what makes the recovery a one-liner whenever the third party goes away.

## What the VPS-resident script actually executes

The script's structure looks like this. The real one (under `ops/deploy/force-commands` in the ops repo) is longer; this is the contract.

```bash
#!/usr/bin/env bash
# VPS-resident deploy fallback.
# Same build/smoke/revert shape as the GH Actions deploy job.
set -euo pipefail

SHA="${1:?usage: deploy-repo.sh <merged-pr-head-sha>}"
LOGDIR="/var/log/deploy-fallback"
mkdir -p "$LOGDIR"

# 1. Pull the merged PR's exact commit; the deploy must equal the merge.
git -C /srv/repo fetch --no-tags origin "$SHA"
git -C /srv/repo checkout --quiet "$SHA"

# 2. Build; on failure, leave the live tree untouched.
if ! ./scripts/build.sh; then
  git -C /srv/repo checkout --quiet -
  exit 1
fi

# 3. Atomic symlink swap + smoke; revert-on-failure.
ln -sfn /srv/repo/dist.new /srv/repo/dist.live
systemctl reload caddy
curl -fsS https://example.com/healthz || {
  ln -sfn /srv/repo/dist /srv/repo/dist.live
  systemctl reload caddy
  exit 2
}
```

Three things in that shape are load-bearing and easy to miss.

First, the script reads a SHA argument. It does not pull from `main` and hope. Production ends up running the merged PR's exact commit, byte-identical to what the merge step produced on GitHub.

Second, the build failure path is a checkout rollback, not a half-deployed tree. If `build.sh` fails, the script leaves the live tree pointing at the previous commit. There is no "almost deployed" state.

Third, the healthz smoke gates the symlink swap. A bad build never goes live. A failing smoke flips the symlink back before Caddy notices anything is wrong.

## The receipt that keeps the manual path honest

The missing piece for any VPS-resident fallback is the receipt (a machine-written record proving a step really ran) that proves the manual path is not a content-divergence loophole. The safe-merge guard (under `ops/merge-guard` in the same ops repo) refuses a manual deploy unless the SHA you intend to ship is the exact HEAD of the merged PR. Receipt shape:

```
SAFE-MERGE: PR #1648 SHA=7cff13d48... status=ok
SAFE-MERGE: manual-deploy-allowed sha=7cff13d48... matches PR #1648 head
```

If you typed a different SHA, the guard would refuse the run before the build even started. The recovery is execution-divergence (CI is down, manual is up) while the artifact stays identical. Curl-able probe shape:

```
GET /merge-guard/deploy/v1/tonsofskills?pr=1648 -> { allowed: true, sha: "7cff13d48..." }
```

No safe-merge pass, no `deploy-repo.sh`. The OIDC outage does not turn into "well, we just shipped whatever was on disk."

## The silent failure shape

A normal failed deploy stops the run summary in red and pings. An OIDC 402 looks like this inside the GitHub Actions run log:

```text
2026-10-14T04:55:11Z ::group::Step Tailscale OIDC
2026-10-14T04:55:11Z POST https://api.tailscale.com/api/v2/oauth/token
2026-10-14T04:55:12Z <- 402 Payment Required
2026-10-14T04:55:12Z body: "your Tailscale trial has ended; choose a plan to create or change keys"
2026-10-14T04:55:12Z ::endgroup::
# (later steps continue; the 402 never propagates upward)
2026-10-14T04:55:30Z Set up job
2026-10-14T04:55:31Z Complete job
Result: success
```

The deploy job's overall result is `success` because the failure happened inside a sub-step the run summary never propagates. The merged commit lands in GitHub; the live site stays on the previous build. The 402 is the only signal that production is stale, and the 402 is buried in a `::group::` block inside the first few seconds of a multi-minute job.

## Why not just fix CI?

Renewing the Tailscale plan restores this single outage. The reason to still install the fallback is that "renew this one credential" is not a class-of-failure fix.

A custom OIDC issuer pointed at your cloud rotates every 90 days. A GitHub App installation token can be revoked by an org admin who never thinks about your deploy. An IAM trust policy edit on the cloud side breaks the handshake the same way: 403, 401, or 402, deep in the run summary, with the rest of the deploy job looking fine. Any of these would have cost the same two days of stale production.

CI runs on credentials. A VPS-resident deploy script that needs only an SSH key (which the operator has regardless of vendor state) does not. Reducing CI from "the only deploy path" to "one of two" means the next expiry is a frictionless recovery instead of an outage.

You do not have to migrate the whole pipeline. The shape that works:

1. Build the GH Actions deploy job so its build/smoke/revert shape is one bash file plus a few `cp` and `systemctl reload`s.
2. Drop that script on the host at `/usr/local/sbin/<repo>-deploy`, gated by a manual-install checklist that requires the script to land before any CI deploy depends on it.
3. Add a safe-merge-style SHA guard so the manual path can only ship the merged PR's HEAD.

The manual-install gate is the load-bearing piece. It means no CI deploy is the first deploy. Every deploy script on a host today was installed by hand before the first CI run that depended on it; that ordering is what makes the next expiry a one-liner SSH invocation instead of a multi-day production gap.

## Also shipped

- tons-of-skills-marketplace PR #1661 bundled Fuse.js and dropped `cdn.jsdelivr.net` from `script-src`, with a 15-page live crawl showing zero CSP violations (Claude Opus 5 5 and Claude Fable 5 1 in the review lanes).
- Landing page flagship card (landing#79 + an intent-os (the internal ops + docs repo) PR covering the Tons-of-Skills flagship) added the Tons-of-Skills card; merge-guard added `landing` to its repo list and let both settle via safe-merge.
- Catalyst-onboarding-v2 P3 closed (3B.3, 3B.4, 3C GATE-P3) under a parallel MiniMax M3 lane with primary QA and scoped interpreter-boundary reviews.
- Same-day PR #1648 (remove Google Analytics, Umami only) shipped two days late because of the Tailscale 402; GPT 6 Astra redrafted the leadership briefing later in the day.
- The CI failure was found by reading the cross-session log entry mid-deploy, not by alert.

## Use this

- Install the VPS-resident deploy script before the first CI deploy depends on it, and gate the install behind a manual checklist that asks "is the manual fallback on disk?".
- Couple the manual path to a SHA-pin guard (safe-merge or equivalent) so the fallback cannot ship content that diverges from the merged PR's HEAD.
- Treat "renew the trial" as recovery, not remediation; the fix is reducing CI from sole deploy path to one of two, so the next third-party OIDC expiry is a non-event.

Reference: the `ops/deploy` tree at `https://github.com/intent-solutions-io/intent-os/tree/main/ops/deploy`.

## FAQ

### What does GitHub Actions do when a third-party OIDC trial expires?

The deploy job's overall result stays `success` because the 402 lands inside a `::group::` sub-step that the run summary never propagates. The merged commit is on GitHub, the run summary is green, and production stays on the previous build until someone reads the raw log line by line.

### Why is the manual VPS fallback safer than running the deploy by hand?

A bare `ssh` plus `git checkout` against `main` can ship whatever sits on disk, which is exactly the failure mode the recovery is built to prevent. That guard refuses any manual run whose SHA isn't the merged PR's HEAD, so artifact identity survives even when CI itself is unreachable.

### What is a SHA-pin guard?

It is a small pre-flight check that compares the revision you intend to deploy against what the merged PR actually recorded, and refuses the run if the two diverge. In this stack it lives at `ops/merge-guard/safe-merge`; its only authorisation (`SAFE-MERGE: PR #1648 SHA=... status=ok`) is what lets the VPS-resident `deploy-repo.sh` actually execute.

## Related Posts

- [highest-existing-tag-beats-git-describe](highest-existing-tag-beats-git-describe): when a bot commit re-uses a tag the release workflow expects to own, `git describe` traps the version bump and the version stops moving. `git tag --list 'v*' --sort=-v:refname | head -n1` and the noise goes away.
- [smtp-250-not-delivery-three-receipts](smtp-250-not-delivery-three-receipts): SMTP 250 only confirms that the relay accepted the message; to prove delivery you need a frozen ApprovedMessage at enqueue, phase-classified SMTP outcomes per RFC 5321, and reconciliation against admissible evidence before any resend.
- [rank-only-reporting-keeps-the-eval-honest](rank-only-reporting-keeps-the-eval-honest): when a retrieval evaluation drives its own corpus cleanup, the cleanup should not be in the scored set; report the rank of each gap-filler doc instead.

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What does a Tailscale OIDC trial expiry look like inside a GitHub Actions deploy?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The OIDC step POSTs to the Tailscale issuer and receives a 402 Payment Required inside a ::group:: block early in the run log; later deploy steps continue, the job result still reports success, the merged commit lands in GitHub, and production stays on the previous build until the run log is read end to end."
      }
    },
    {
      "@type": "Question",
      "name": "How does a VPS-resident deploy script recover a deploy when third-party CI authentication is broken?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A bash script on the host checks out the merged PR's exact commit SHA, runs the same build and smoke and revert shape the GH Actions deploy job uses, and is gated by a content-hash guard that refuses any commit other than the merged PR's HEAD. The recovery is one SSH invocation and needs no third-party credential."
      }
    },
    {
      "@type": "Question",
      "name": "Is renewing a single third-party CI credential enough to fix a deploy outage?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Renewing the credential restores the single outage but does not remove the class of failure. Tailscale OIDC, custom OIDC issuers, GitHub App installation tokens, and IAM trust policies all run on credentials that can expire or be revoked. Reducing CI from the sole deploy path to one of two turns the next expiry into a frictionless recovery instead of a multi-day production gap."
      }
    }
  ]
}
</script>
