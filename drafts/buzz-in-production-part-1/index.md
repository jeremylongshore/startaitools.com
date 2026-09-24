+++
title = 'Buzz in Production, Part 1: We Treated a Preview Chat App Like a Regulated System'
slug = 'buzz-in-production-part-1-regulated-system'
date = 2026-07-30T10:00:00-06:00
draft = true
tags = ["self-hosting", "devops", "security", "release-engineering", "docker", "ai-agents"]
categories = ["Technical Deep-Dive"]
description = "Block shipped Buzz, a Nostr-native team chat for humans and AI agents. This is the hardening substrate a team and its agents can trust: what taking a preview app to a closed, backed-up production surface actually took."
series = "Buzz in Production"
toc = true
tldr = "Block's Buzz is honest preview software: bundled MinIO is eval-only, rate limiting is defined but not enforced, and the best public self-host guide calls its own hardening what the author would build, not what he tested. So adoption stopped being a trust job and became a hardening job. We ran the real thing: closed relay enforcing from first boot, secrets encrypted in git, backups that restore, an updater built to auto-revert, and a merge gate that ran green while GitHub billing was dead. A relay running is not a closed relay enforcing, and the whole job is the distance between them."
+++

Preview software is honest software, if you read it right.

Block shipped Buzz on 2026-07-21. It is a Nostr-native team chat where humans and AI agents are co-members of the same relay, and it got plenty of launch-week attention. It is also, by its authors' own admission, preview software. The bundled MinIO is eval-only. Rate limiting is defined but not enforced. Some workflow features are stubbed. Upstream tells you all of this out loud, which I respect, because it turns adoption into a job you can actually scope.

The single most serious public self-host guide I found is [Rohit Raj's write-up](https://rohitraj.tech/en/notes/block-buzz-agent-collaboration-platform-guide-2026), and it is honest about its own scope. It frames its hardening checklist as "what I'd actually build with it" and "the wiring the launch posts skip": a starting point, offered as aspirational, and the author says so plainly. It tells you, in as many words, to run Buzz as "a small, isolated agent laboratory, not a Slack replacement." For the guide's scope, that is the right call.

This picks up where that guide points. His checklist is the right starting line. What follows is the delta from a lab to a surface a whole team depends on: closed-relay, backed-up, auto-reverting, edge-limited, and proven at each step. Not because calling it a lab was wrong. Because closing the gap between "a lab" and "a team depends on it" is the work worth writing down. Agents are the point of Buzz, and they arrive later in this series. Part 1 is the substrate they land on, because a surface you cannot trust is not one you put a team or an agent on. That gap is this series.

## The one gate that decides everything

I spent twenty years running restaurants before I wrote production code, and the habit that transferred cleanest is the pre-shift line check. You walk the line before service. Every station stocked, every backup pan filled, every temperature logged. A station that fails the check does not close the restaurant. It means that plate does not leave the pass until it is right. The default is not-served, and you earn served by passing the check. That is what fail-closed means on a line.

A chat surface a team is about to live in gets the same rule. And the trap is the one that bites a new manager on their first Friday: "a relay is running" is not "a closed relay is enforcing." A pan with food in it is not a plate that is right. One is a process that answered a health check. The other is a system that will tell an uninvited stranger no. Part 1 is about the difference, and about the setup that lets you prove it instead of hope it.

That is the only operator metaphor I am going to lean on for the whole series. Line check, fail-closed: nothing leaves the pass until it is proven correct. Everything below is either stocking the station or checking it.

## The one property that makes this buildable

If you are reading a hardening writeup about Buzz, you already know what Buzz is, so I will skip the tour. One property of it is load-bearing for everything below: [Buzz](https://github.com/block/buzz) ships a first-class invite-only closed-relay mode with NIP-42 auth. That is the only reason hardening it is a finite job instead of bolting auth onto a public firehose. With that mode, the hard part is never inventing enforcement. It is proving the enforcement is actually on, and keeping it on through updates, restarts, and a backup restore. Add the fact that upstream calls this preview software out loud, and adoption stops being a trust job and becomes a hardening job with a bounded checklist.

Our code lives in a [public fork](https://github.com/intent-solutions-io/buzz). I will come back to why the fork holds code only, and where everything estate-specific actually lives.

## Principle 1: the fork is additive-only, and code-only

GitHub will not let you make a fork of a public repo private. That is a hard constraint, not a preference, and it decides the whole layout. So the fork holds CODE ONLY. Every estate-specific artifact, real hostnames, the deploy runbooks, the decrypted anything, lives in a separate private ops repo that I am not going to link and you do not need.

Inside the public fork, the discipline is additive-only. We add files upstream does not have:

```
000-docs/          our public-safe blueprint and audits
FORK.md            the additive-only contract, in writing
.beads/            our task backlog, tracked as JSONL
TEST_AUDIT.md      the test-layer audit for our changes
```

We never touch upstream-owned files. Not the README, not CONTRIBUTING, not LICENSE. The reason is boring and load-bearing: if you never edit a file upstream also edits, you never get a merge conflict when you rebase. A fast-moving pre-1.0 project will push a lot of commits. You want to ride that upstream without a merge war every week, and additive-only is how you get it.

This is not a promise, it is enforced. Local git hooks run a "must-survive set" check (the upstream-owned files must be byte-identical to upstream), an escape-scan for anything that leaks estate specifics into the public fork, and hash-pinning so a reviewed file cannot drift silently. Same discipline I use on the [Claude Code plugins platform](https://github.com/jeremylongshore/claude-code-plugins) I maintain, where 2,000+ stars means a lot of eyes on every diff. Track a moving upstream, carry your own hardening, keep the two from fighting. That is the whole trick.

The `FORK.md` file is where the contract lives in writing, so the rule survives me. Six months from now, an agent or a teammate rebasing against a fast upstream needs to know, without asking, that touching the README is off limits and that new hardening goes in an added file. A convention that only lives in one person's head is a convention that breaks the first time that person is out. Write the contract down, then have the hook enforce the contract. `TEST_AUDIT.md` does the same job for the test layers: it records what our changes are actually covered by, so "we added hardening" is a claim with a receipt attached, not a vibe.

## Principle 2: separate the failure domains (the reversal)

Here is the design decision I got wrong first, and why the correction is the interesting part.

The original plan put Buzz next to the revenue stacks on a shared VPS. One box, one Caddy, everything co-tenant. It would have worked on day one. Then an external infrastructure review (a private one, separate from the public write-ups) pushed back, and the owner reversed the call: production Buzz moves to a dedicated VPS with its own Caddy ingress.

The argument is plane separation, and it is correct. A pre-1.0 stack that auto-updates should not share a kernel, a disk, an ingress process, or a memory ceiling with workloads that pay the bills. Not during an all-in, whole-team rollout, when the blast radius of a bad update is the highest it will ever be. The alternative, co-tenancy with resource caps, reduces the risk but does not remove the shared-kernel and shared-ingress failure modes. On a preview app you are inviting everyone onto, "reduced" is not the bar.

What we did not do is throw away the stack we already stood up on the shared box. That got re-designated permanent staging. Same compose, same gates. Destructive drills (backup-restore, planted-fault updater tests) run there, forever, and never on prod. Out of that falls a rule I now treat as non-negotiable: fresh prod secrets always, staging keys never promote.

The staging stack is a self-contained compose. Relay, Postgres 17, Redis 7, MinIO as the interim media store, and a one-shot bucket initializer that creates the media bucket and then exits. The initializer runs once, not as a long-lived service, because a bucket needs creating exactly one time and a container that keeps trying to re-create it is just noise in your logs and one more thing that can flap a healthcheck. Small choice, but "runs once and gets out of the way" beats "runs forever doing nothing" every time you are trying to read a startup log at speed. Here is the shape:

```yaml
services:
  buzz-relay:
    image: ghcr.io/block/buzz@sha256:<digest>   # pinned by digest, never :latest
    ports:
      - "127.0.0.1:<port>:<port>"               # loopback only, Caddy is the front door
    environment:
      BUZZ_RELAY_MODE: closed                    # closed from first boot
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "0.50"
          pids: 256                              # a preview toy cannot starve a real surface
```

Three things carry the weight there. The image is pinned by digest, not a floating tag, so "update" is a decision and not an accident. The publish is loopback-only, so the only way in is through the single Caddy front door. And every service has memory, cpu, and pids caps, because co-tenancy without caps is just a slower outage.

The caps are only half of it. Each stack also runs on its own docker bridge network, with no route to any other stack's database:

```yaml
networks:
  buzz-internal:
    driver: bridge          # this stack only; no route to any revenue stack's Postgres
```

Resource caps and network reachability are two separate controls, and you want both. The caps stop a runaway container from starving its neighbors. The private network stops a preview chat toy from ever reaching a revenue stack's Postgres in the first place. One is a throttle. The other is a wall. A starve you can survive and clean up after. A cross-stack database reach is a data-boundary violation you cannot un-ring, so the wall matters more, and it is the cheaper of the two to get right.

The default docker bridge is the trap here. Drop two compose stacks on a box without naming networks and they can land on the same default bridge, which means Buzz's relay container can open a socket to a revenue Postgres by container name. Nothing stops it except the fact that nobody wrote the code to do it, and "nobody wrote it yet" is not a security boundary. Naming the network per stack turns an implicit shared LAN into an explicit, empty one. It is a two-line change that removes an entire class of "how did that even reach that" incident, which is exactly the kind of change worth making before anyone is on the box, not after.

### Bringing the prod box up without locking yourself out

The dedicated prod VPS came up in a deliberate order, because the wrong order is an instant self-lockout. Firewall rules do not care about your good intentions. Flip default-deny before the path you actually use is proven, and you have just fired the rule that strands you.

So the order was: tailnet first, firewall last. Bring the tailnet up and confirm tailnet SSH works before touching the firewall at all. Then create a non-root sudo admin user and log in as that user over the tailnet, and verify it works, before disabling root login and password auth. Only then flip the firewall to default-deny: trust the tailnet interface, expose only public 80 and 443 for Caddy, and let public 22 time out.

```
1. tailnet up      -> ssh over tailnet confirmed working
2. admin user      -> sudo login over tailnet confirmed working
3. disable root + password auth   (tailnet path already proven)
4. firewall default-deny: trust tailnet iface, public 80/443 only, public 22 times out
```

Every destructive step happens only after the replacement path is proven, never before. Get steps 3 and 4 ahead of steps 1 and 2 and you close public SSH while the tailnet path is still a hope, which means you are now locked out of your own production box with no way back in except a provider console. Order is the control.

### A very ordinary bug, diagnosed the right way

On the fresh prod box, Caddy refused to start. Not a cert problem, not a config typo. A log file was owned `root:root` where the identical, happily-running staging box had it owned `caddy:caddy`. A root-context first-start had created the file, and Caddy would not write to something it did not own.

I did not theorize about it. I diffed the fresh box against the known-good staging box, found the single difference in ownership, `chown`ed the file, and moved on. The whole detour was minutes because there was a running reference to diff against. When a fresh box will not do what an identical running one does, diff the two, do not guess. And this is the quiet dividend of keeping staging alive from Principle 2: it is not just a drill target, it is the known-good reference you diff a sick box against.

## Principle 3: secrets are SOPS-encrypted files, committed to git

This one makes people flinch until they see it. The secrets file is committed to git. On purpose. It is deliberately not gitignored.

It is safe because it is SOPS-encrypted with age, and it is decrypted in-process, never to disk. The master file carries 30 `ENC[AES256_GCM]` values and zero plaintext. A committed value looks like this:

```yaml
pg_password: ENC[AES256_GCM,data:c2FtcGxl...,iv:...,tag:...,type:str]
```

You can read the key name. You cannot read the value without the age private key, and that key lives on the host and the dev box, never in the repo. "Committed to git" is safe because the ciphertext is the thing in git, and the plaintext never is. The upside is that secrets version and review like code, and a fresh clone plus the host key is a working deploy.

The prod secrets file is encrypted to the new prod box's age key plus the estate key, and nothing else. That is the enforcement behind "staging keys never promote": the staging box's key is not a recipient on the prod file, so it cannot decrypt prod. That is not a policy you have to remember, it is key scoping. The staging shell has no path to a prod credential even if someone fat-fingers a copy. The honest caveat: the estate key is also a recipient, so whatever holds the estate key can decrypt prod too. That key's custody is the real control, and it lives off both app boxes. The scoping is only as strong as where that one key sleeps.

The reason this matters more on a preview app than on a mature one is the same reason the failure-domain split matters: you are going to touch this stack a lot. Every update, every drill, every planted-fault test is a chance to leak a credential from a lower environment into a higher one by habit. Wire the environments so the wrong key simply does not decrypt, and the habit cannot hurt you.

## Principle 4: a merge gate that does not need GitHub's runners

Then GitHub Actions went dark. Org-level billing was blocked, and every workflow dispatch came back `startup_failure`. No hosted runners, no CI, in the exact window we were trying to land a hardened stack.

So the merge-lock gate does not depend on GitHub-hosted runners. A repo-local script checks out a clean detached git worktree, runs the exact same gates the CI job would, and posts the required commit statuses through the status API, which is not billing-gated. Receipts from the actual merge:

```
Gates (pnpm check)   success   126s   (clean worktree)
Drills               success   207s
Secret-scan          success   (gitleaks)
```

The clean detached worktree is the part that makes this honest rather than theater. If you run the gates in your working tree, you are testing your working tree, uncommitted edits and all, which is not what merges. Checking out the exact merge commit into a throwaway worktree means the gates run against the bytes that will actually land, and the status you post reflects reality. Run gates against a dirty tree and a green check is just a rumor.

I want to be precise about what did and did not get bypassed, because this is the beat people misread. A CI check was never bypassed. The gates ran, in a clean worktree, and passed. The only thing bypassed was the review-approval requirement, because a solo dev cannot approve his own pull request and there was nobody else on the branch. Approval is a human control. Gates are a machine control. I skipped a human control I was the only member of, and I ran every machine control at full strength. Those are not the same thing, and conflating them is how "we have CI" turns into a story you tell yourself. When the team lands and there is a second human on the branch, the approval control comes back on. The machine controls never went off.

## The first proof that matters: a relay that says no

Stocking the station is done. Now the line check.

Staging came up healthy. Four containers, all healthy: `buzz-relay`, `buzz-postgres`, `buzz-redis`, `buzz-minio`. And here is the first operator trap. The path you would guess, `/health`, returns 404 on this image. The real smoke set is the `_readiness` endpoint plus the NIP-11 relay-info document:

```bash
curl -s -o /dev/null -w '%{http_code}\n' "https://buzz.<domain>/health"       # => 404  (the trap)
curl -s -o /dev/null -w '%{http_code}\n' "https://buzz.<domain>/_readiness"    # => 200
curl -s -o /dev/null -w '%{http_code}\n' \
  -H 'Accept: application/nostr+json' "https://buzz.<domain>/"                 # => 200  (NIP-11)
```

Functional probes over liveness guesses. If you probe `/health` and treat the 404 as down, you will chase a ghost for an hour. Worse, if a general agent wires `/health` into a healthcheck or an alerting rule, you ship a monitor that reports permanent failure on a perfectly healthy relay, which is how you train a team to ignore alerts in week one. The gotcha is small. The blast radius of getting it wrong is not.

The relay content-negotiates the same root URL for two different audiences:

```bash
# Machine audience: NIP-11 relay metadata
curl -s -H 'Accept: application/nostr+json' "https://buzz.<domain>/"
# => 200; software "block/buzz", version 0.2.0, supported_nips includes 42

# Human audience: the web client
curl -s -H 'Accept: text/html' "https://buzz.<domain>/"
# => 200; the SPA
```

That `supported_nips` includes 42 is the tell that matters. NIP-42 is the authentication layer, which means the closed-relay auth is present, not just configured in a file somewhere.

Worth being precise about what "installed" had to mean here, because it is not "the container is up." It means a human opens the public HTTPS URL in a browser and gets the working app, zero client install, nothing to download, while a Nostr client hitting the exact same URL gets the relay metadata instead. Same front door, content-negotiated to two audiences. That zero-install-for-a-human property was a hard requirement, not a nicety. You cannot invite a whole team onto a surface that needs a native client install per person on day one. If the browser does not just work, the surface is not ready, no matter how healthy the containers report.

Present is not enforcing, though. So the proof that actually counts ran on prod, live over HTTPS, and it is three assertions in a row:

- The owner key authenticated over NIP-42, published a note, and read it back. Round trip works.
- A freshly generated, un-invited key was REFUSED. The door says no to a stranger.
- The relay logged `member_count:1` on boot. One member, the intended one, nobody smuggled in.

Then the unauthenticated probe matrix, a first pass from the box itself: media PUT, git upload-pack and receive-pack, hook routes, admin routes. All rejected. Only the intended public routes served. That is the difference between a relay running and a closed relay enforcing, and it is the difference you can only see if you send the requests that are supposed to fail and confirm they fail. The exhaustive version, run from outside the tailnet with the edge rate-limit controls in place, is Part 4.

One ownership detail worth stealing. Closed-relay ownership is set to a throwaway bootstrap key at first boot. The real owner is a human's client-side-generated key that swaps in at onboarding. So the owner's actual secret key never touches an operator shell, and by construction there is no path for it to land in a compose file or a log. The most privileged key in the system is the one the operator never holds.

## We folded an external review in as verified beads, not as faith

That same external infrastructure review handed us a list of findings. I did not take them on faith and I did not wave them off. Each one became a bead we could verify against the real running stack, cross-referenced to the upstream issue so the trail is public:

- Desktop join is blocked without Tauri CORS origins the compose does not set: [block/buzz#3490](https://github.com/block/buzz/issues/3490).
- Android pairing needs a sidecar the bundled compose omits entirely: [block/buzz#2734](https://github.com/block/buzz/issues/2734).
- A git-conformance probe can wedge startup, a whole hang class worth designing around: [block/buzz#2723](https://github.com/block/buzz/issues/2723).
- A `buzz-admin` dev-credential fallback that must never survive into a closed prod relay: [block/buzz#2837](https://github.com/block/buzz/issues/2837).

That last one is the kind of thing that separates a lab from a production surface. A dev-credential fallback is a convenience in a laboratory and a back door in production, and the only difference is whether anyone checked. We checked, against the running box, and folded the check into the unauthenticated probe matrix so it stays checked on every future update instead of once.

A finding you have reproduced against your own stack is worth ten you copied off a checklist.

## The tool we decided not to build yet

Mid-build, the owner asked a fair question: does an "ops plugin" earn its place? A general-purpose agent can already read docs and run compose. Why wrap it?

We decided not to pre-spec it. Run the real install-setup-operate cycle first. Capture exactly the non-obvious traps a general agent gets wrong: `/health` is a 404, the closed-relay identity-key ordering, the fact that upstream's "backup command" is a checklist and not a backup. Then scope the tool around that specific gap, once we have earned enough to make the tool non-obvious. The interesting engineering decision was choosing not to build the obvious thing until the knowledge existed to build the right thing. You cannot automate a job you have not done by hand.

## What I am not claiming yet

Credibility comes from the limitations, so here they are, plainly.

Off-site backup is not done. The encrypted local borg archive is real, and we drilled the restore on a different machine, so that half is proven. But the off-site copy rides Backblaze B2 with Object Lock, and B2 is not provisioned yet, because that is an owner gate across the whole estate. Local proven, off-site pending a credential. I am not going to round that up.

While we are here: upstream's "backup" guidance is a checklist, not a backup. It tells you which directories matter and leaves the actual capture, encryption, retention, and restore to you. That is fine for a lab and dangerous if you mistake reading the checklist for having a backup. A backup you have not restored is a hope with a filename. So we restored it, on a different machine, because a restore on the same box proves almost nothing. Part 2 is that drill in full: the exact message present, membership intact, the door still shut, with the RTO measured, not estimated.

The last-mile work that remains is gated future steps: the apex-domain cutover and the owner's desktop-key swap both sit behind explicit gates. Mobile pairing itself is done, a real phone completed the QR handshake against prod, and the how of that (plus the bug that briefly took the relay down getting there) is Part 5.

And one thing did not cleanly reproduce in the headless restore harness: a Nostr client's auth-on-read handshake. We wrote it down as an open item rather than paper over it.

## What this actually cost

Because the point of a writeup like this is to help you decide, not to admire the result, here is the honest bill.

Time: two evenings of focused work. One to stand up staging and fold in the external review, one to bring up the dedicated prod host, prove the backup restore, add the edge controls, and fix the pairing bug.

Money: the marginal infra is one additional small VPS (the dedicated prod host) plus metered object storage for the off-site backup that is not switched on yet. Order of magnitude, this is a low-tens-of-dollars-a-month footprint, not a hundreds one, and staging reuses a box that already exists.

The part that is easy to hide: this assumes tooling I already had. A SOPS-and-age secrets pipeline, the additive-only git hooks, an audit harness, and a repo-local CI lane were all in place before Buzz showed up. If you are starting from zero, budget that setup separately. It is a real, mostly one-time cost, and it is the actual reason the discipline here looks cheap.

And a scope limit worth saying out loud: every proof here is single-operator and single-member. Member onboarding, per-agent keys, and day-to-day key management at team scale are real work this series has not shown yet.

## What's next

This was the setup. The rest of the series is the proof, one hard problem per part.

- Part 2, "A Backup Isn't Real Until It Restores." A named borg recovery point, restored on a different machine, where the exact prod message is physically present, membership is intact, the relay still refuses an un-invited key, and the RTO is about 3 minutes.
- Part 3, "Auto-Updating a Preview App Without Losing the Database." Why naked `:latest` plus auto-migrate on a v0.x event store is a loaded gun, and a wrapped updater that snapshots, pins a digest, hard-timeouts a wedged image, functional-probes, and auto-reverts in order instead of faking a rollback.
- Part 4, "Proving a Closed Relay Actually Says No." The full off-network unauthenticated probe matrix, plus the edge compensating controls (fail2ban and connlimit) we added because upstream rate limiting is defined but unenforced.
- Part 5, "The Mobile Pairing Bug That Briefly Took the Relay Down." The QR 404, the pinned image that shipped no pairing binary, and the sidecar-first fix.

Preview software told us the truth about itself. The only honest response is to do the checking upstream did not claim to have done, and to show the receipts either way. The relay was easy to run and hard to trust, and closing that distance is the entire job. The discipline IS the product.

---

## Series Navigation

**Buzz in Production**

1. **Part 1: We Treated a Preview Chat App Like a Regulated System** (you are here)
2. Part 2: A Backup Isn't Real Until It Restores (coming soon)
3. Part 3: Auto-Updating a Preview App Without Losing the Database (coming soon)
4. Part 4: Proving a Closed Relay Actually Says No (coming soon)
5. Part 5: The Mobile Pairing Bug That Briefly Took the Relay Down (coming soon)

---

## Related Posts

- [A Green Recovery Drill Can Still Be Lying](/posts/a-green-recovery-drill-can-still-be-lying/)
- [Adversarial Review Before Team Rollout](/posts/adversarial-review-before-team-rollout/)
- [58 E2E Tests, One Day, One Slack Channel Launch](/posts/58-e2e-tests-slack-channel-launch-one-day/)
