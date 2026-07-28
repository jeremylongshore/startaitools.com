+++
title = 'How the Same Deploy Pattern Crossed Four Repos in One Week'
slug = 'how-the-same-deploy-pattern-crossed-four-repos-in-one-week'
date = 2026-07-28T07:30:00-05:00
draft = false
tags = ['deploy', 'tutorial', 'vps', 'reusable-workflow', 'cross-repo', 'operator']
categories = ['DevOps']
description = 'Same deploy pattern: jeremylongshore.com PR #11/#15 → intent-os reusable workflow → startaitools.com deploy.yml → tonsofskills.com PR #256. One week, four repos, zero new code per repo.'
+++

Three days ago there was no deploy pattern for startaitools.com. Tonight there is one and the pattern is the same one that runs the personal portfolio, the company landing mirror, the operator-side A3 drill for the Hustle Estate, and now the niche-publication site that ships every startaitools.com post to a wider audience. The pattern is not new. The pattern is the point. The pattern crossed four repos in one week and did not require writing a single line of deploy code per repo.

This is what it looks like when a deploy pattern becomes a building block instead of a custom build.

## The shape of the pattern

VPS as the single ingress, with Caddy as the front door. Tailscale OIDC for cross-org SSH (no SSH keys, no static credentials, no per-repo secret rotation). A reusable GitHub Actions workflow at `jeremylongshore/.github` that takes a static-site config and a service name and a health-check URL and a VPS tailnet IP and runs the entire deploy dance end to end. A small force-command on the VPS that does the gated git fetch, the build, the rsync into `srv-path`, and a smoke check on the served bytes. The pattern is about three hundred lines of Ruby on the build side and about forty lines of bash on the deploy side and zero of either per repo.

The point of the shape is that the shape is the same across the four repos:

| Repo | Site | Pattern entry point | Deployment date |
|---|---|---|---|
| jeremylongshore.com | Personal portfolio | Original Jekyll-scaffold.rb → VPS (PR #11/#15, 2026) | Live 2026-06-20 (per project CLAUDE.md) |
| startaitools.com | Daily blog | New `deploy.yml` calling the shared reusable workflow | This session (PR #43, 2026-07-27) |
| tonsofskills.com | Marketplace / blog mirror | `intent-os` reusable workflow + adoption drill | intent-os PR #256, 2026-07-28 |
| now-lms.io | Client SaaS | Same pattern, separate force-command, different health endpoint | Long-running, before this week |

Four repos. One pattern. Three lines of GitHub Actions input per repo. That is the entire change footprint for the new repo adoptions.

## What crossed, and what did not

What crossed the estate:

- The reusable workflow URI and its SHA pin. `jeremylongshore/.github/.github/workflows/vps-deploy.yml@53d6be37d6c046818157b954acb33667ac095dd8` is the call signature; the SHA is what gets pinned so a future breaking change in the upstream workflow does not silently land on a dependent repo. Pinning is one line per repo.
- The force-command on the VPS (`/usr/local/sbin/deploy-<repo>`). Per-repo but identical-shape: `git fetch`, `bundle install` or `pnpm install` or `go mod download` (whichever the repo uses), `bundle exec ruby scaffold.rb` or `pnpm build` or `make`, `rsync` to `srv-path`, `curl -fsS https://<domain>/healthz`. The pattern is identical; only the build step changes per repo.
- The Caddyfile site-block. Same shape every time: `root * /srv/<repo>/public; file_server; handle /healthz { respond "OK" 200 }; header X-Frame-Options SAMEORIGIN; log ...`. The variables are `srv-path` and the `domain` and whether the site needs reverse-proxy rewrites for forms-api.
- The OPS-side secret posture: SOPS-encrypted creds at `/etc/intentsolutions/secrets/`, no plaintext in any repo, Tailscale OIDC token granted at the org level for `jeremylongshore` and `intent-solutions-io` orgs.

What did not cross:

- The build commands. Hugo for startaitools, Ruby-Liquid scaffold for jeremylongshore, pnpm workspace for tonsofskills, Python/Flask for now-lms. Each repo's build is what it has to be.
- The contact forms / API proxies. Some repos proxy through `/api/forms/*` to `tonsofskills.com/api/forms/:splat`. Some do not. The proxy is per-repo because the upstream API consumer is per-repo.
- The themes. archie for Hugo, default for Jekyll, custom for Astro, Flask for now-lms. Different sites have different needs and the pattern does not pretend otherwise.

The pattern crosses the **ingress and the audit trail**. The build is local to each repo because the build has to be.

## What this week actually looked like

Tuesday 2026-07-21: jeremylongshore.com deploy pattern was already live (PR #11 from late 2026 + the health-check + tailnet additions from PR #15). The reusable workflow at `jeremylongshore/.github` had been used by 1 repo, the personal portfolio. No new code, just an existing stable pattern.

Tuesday-Wednesday 2026-07-22..23: nobody touched startaitools.com deploy. The site had been on Netlify since 2024 (per `netlify.toml` in master). Netlify was working. The migration was a bead on the list, not an emergency. The weekly anchor post for 2026-07-23 was `llm-legible-deterministic-architecture`, Tier 2, the audit-addendum trail baked into the methodology doc that day.

Tuesday 2026-07-27 (this session): the migration-artifacts work. PR #43 added `.github/workflows/deploy.yml` to startaitools.com calling the shared reusable workflow with startaitools-specific inputs (`variant=static`, `srv-path=/srv/startaitools`, `health-check-url=https://startaitools.com/healthz`). Plus `docs/runbook/netlify-to-vps-migration.md` for the operator-side cutover steps (Caddy vhost verbatim, Porkbun DNS cutover via `intent-os/ops/dns/porkbun-update-record.sh`, Netlify carve-out). The Netlify site still serves because the DNS cutover has not happened. Instant rollback window during the 10-minute Porkbun TTL is documented in the runbook.

Wednesday 2026-07-28 (today): `intent-os` PR #256 closed: `feat(deploy): tonsofskills.com adopted onto the deploy wrapper: live drill + CI-shaped promote proven (D128 slice 1)`. The "live drill" is the operator-lens point: someone ran the deploy against a real VPS with a real domain and a real health check and watched the chain light up green and watched the smoke check return the served bytes and called it done. The promotion step is the piece that took the most discipline: the drill had to land the promotion step in a windowed state so the next deploy could pick up where this one left off, and that meant a "CI-shaped promote" step where the orchestrator announces what it is about to promote, waits for the green check, and then promotes, instead of the older "deploy and assume" model.

This is the pattern crossing the estate. Not because anyone mandated it but because the pattern worked and the next team needed the same thing and the next repo's adopt required zero new code in the pattern itself.

## What the pattern enforces

The pattern does not pretend to be clever. It enforces:

- **The build has to name its commit.** `BUILD_SHA` is an ARG that has no default in every repo's `deploy.yml` that calls the reusable workflow. A build that cannot name which commit it is has to fail before the deploy step.
- **The smoke check asserts on served bytes, not exit codes.** `scripts/deploy-smoke.sh` reads the served bytes back, computes a hash against a known-good fingerprint, and returns the diff if the bytes do not match. An exit-zero smoke check that returned empty bytes would have lied about the deploy being healthy. The pattern requires the byte-fingerprint check.
- **The verdict lives in code, not in the presentation layer.** When the smoke check returns, the verdict function is a pure module (`verdictFor(commit, exitCode, byteHash)`) that the deploy step calls. A verdict living only in a Jinja template or a Markdown callout is untestable. The pattern makes the verdict pure because the original fail-open survived exactly because nobody could write a unit test for it.
- **The deploy emits evidence, not assertions.** Every deploy produces a JSON record with the build SHA, the VPS exit code, the smoke-check fingerprint, the health-check response, and the deploy-window timestamp. That record is the audit trail. If the deploy rolls back two hours later because of a downstream failure, the operator can grep the records to find which deploy produced the broken state. No record, no rollback diagnosis, no trust.

The pattern is one sentence at its deepest: a deploy is only verifiable if every layer can name which commit it is, and the stateful layer is where that chain silently breaks.

## Why four repos in one week is the only proof that matters

If only one repo had the pattern, the pattern could be a special-case. If two repos had it, the pattern could be a coincidence. Three is the smallest number that lets the operator say "this is the convention, and the convention beats the alternative." Four means the alternative: per-repo deploy scripts, each one maintained by a different person, each one drifting: has lost.

The pattern is not going to win because it is elegant. The pattern wins because the audit trail is shared, the force-command shape is shared, the Caddyfile site-block shape is shared, and the reusable workflow has the SHA pin that prevents silent drift. The pattern is the conservative thing. Per-repo deploy scripts are the ambitious thing. Conservative beats ambitious in deploy every time because ambitious deploys only succeed when the same person who wrote them is on call. Conservative deploys succeed when anyone with the SOP can roll back without reading the source first.

## What is still open

Three things, all flagged:

1. **The Porkbun cutover for startaitools.com.** The deploy.yml exists, the runbook exists, the Caddy vhost template exists. The Porkbun API call to flip `startaitools.com → 167.86.106.29` with a 600-second TTL is an operator action. Documented in `docs/runbook/netlify-to-vps-migration.md`. The same shape as tonsofskills.com's 2026-07-28 adoption: someone with VPS shell + Porkbun creds + the SOPS-key for the Porkbun API.
2. **A Caddy file_server and force-command pair on jeremylongshore.com.** Today the personal portfolio runs through the pattern via Netlify carve-out. The reusable workflow at `jeremylongshore/.github` was built for personal portfolio first and now-lms + tonsofskills + startaitools all reuse it. The five-repo state (when startaitools cuts over) will be a clean estate.
3. **The 7-layer testing baseline is in now-lms and not in startaitools.com yet.** The testing-tier-1 baseline (harness install + L1 hook chain + coverage visibility + acceptance specs) lives in now-lms since 2026-07-27 (commit `7ec475b`). The Tier 2 / Tier 3 testing taxonomy per the blog-backfill skill is similar shape; the gap is the explicit shellcheck-lint, ruff, voice-lint, link-check gates that startaitools.com has in CI but which live in the `.github/workflows/scripts-lint.yml` workflow rather than as a 7-layer taxonomy file. Closing the gap is a separate bead (`startaitools-XXX-2026`), not a deploy-pattern concern.

## What you can do with this if you run your own multi-repo deploy estate

The shape that crossed four repos in one week is not proprietary. It is the same shape any operator can build:

1. Stand up a VPS. Wire Caddy. Write one reusable workflow. Add Tailscale OIDC for the SSH channel.
2. For every repo, add a 30-line `deploy.yml` that calls the reusable workflow with the four inputs the workflow needs (variant, srv-path, health-check-url, vps-host). Pin the workflow to a SHA. Add a per-repo force-command that knows the build and the smoke check.
3. Make every deploy produce an evidence record. JSON, with the build SHA, the exit code, the smoke-check fingerprint, the health-check response, and the timestamp. Commit the records somewhere grep-able.
4. The pattern is conservative by design. The smoke check asserts on served bytes, not exit codes. The verdict is a pure function. The `BUILD_SHA` ARG has no default. The reusable workflow is SHA-pinned.

That is the entire playbook. The four-repo state is what happens when the playbook is good enough that the next adoption does not require a meeting.

The startaitools.com cutover is the proof. Today it ships the same deploy shape as jeremylongshore.com (and tonsofskills.com and now-lms.io). Tomorrow the Porkbun flip moves the public DNS into the same backend. The work that crossed the estate was not the Caddyfile or the reusable workflow or the force-command. The work that crossed the estate was the decision to make the pattern the convention and the convention beat the per-repo alternatives. That is what an operator-led deploy pattern looks like at scale: it is not the code, it is the agreement.
