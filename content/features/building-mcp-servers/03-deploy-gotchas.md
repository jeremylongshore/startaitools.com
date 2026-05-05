+++
title = 'Four Production-Deploy Gotchas'
weight = 30
date = 2026-05-05T08:00:00-05:00
description = "Chapter three — the four deploy-time bugs that only manifest in production. Why CI green doesn't mean ship-ready, and what to add to your deploy checklist."
+++

**Source post:** [Four production deploy gotchas](/posts/five-releases-fifteen-minutes-mandy-cutover-and-freeze-break/) (companion: VPS-as-the-home Day 1)

Tests pass. CI is green. The merge is clean. You hit deploy and the production logs light up. Welcome to the seam where everything you tested doesn't quite match where you're running.

## The four

1. **Container image is built on a different libc than the host.** Compiles fine, runs fine in CI, segfaults on the host because the prebuilt wheel was linked against musl and the host is glibc. Add an explicit base-image declaration to your Dockerfile and run a smoke test on the production image during CI, not just the host CI image.

2. **Environment variables are loaded from a different source than dev.** Dev: `.env` file. Staging: AWS Secrets Manager. Production: Vault. Each one parses values slightly differently — quoted strings, escaped newlines, trailing whitespace. Have one `loadenv()` function and test it against all three sources.

3. **Filesystem paths assume a writable working directory.** The container runs as a non-root user, the working directory is read-only, and your "temporary" cache file goes nowhere. Always declare your write surfaces explicitly — a `WRITABLE_DIRS` env or config block — and assert them on startup.

4. **Healthcheck endpoint races the readiness probe.** Your service listens on `:8080` after a 4-second warmup. Your healthcheck endpoint returns 200 from the first second. Kubernetes thinks you're ready before your app does, sends real traffic, gets connection refused. Always wire the healthcheck to the same readiness signal your app uses to start serving.

## Why this connects to MCP

MCP servers are deployed exactly like any other long-lived service — and they inherit every one of these traps. The protocol is over stdio or HTTP/SSE; in either case, your server has to be alive and accepting connections before the client tries. None of the four gotchas show up in the protocol layer. All four show up in the operational layer that the protocol runs on top of.

The end of this feature is the start of the next one: how to design an MCP server's tool catalog so v0.2 can ship without breaking v0.1's clients. That's a longer write-up — coming as a standalone feature when the second Guidewire release lands.
