+++
title = 'Ship Dormant, Wire Later — A Multi-Agent Slack Production Day'
slug = 'ship-dormant-wire-later-multi-agent-slack'
date = 2026-05-20T10:00:00-05:00
draft = false
tags = ["release-engineering", "architecture", "ci-cd", "claude-code", "typescript", "automation"]
categories = ["Technical Deep-Dive"]
description = "Ship infrastructure dormant behind feature flags. The activation day is wiring plus a CLI — eleven PRs, six dormant primitives going live in one day."
+++

Ship infrastructure dormant behind gates. The activation day is wiring plus a CLI, not architecture plus wiring plus a CLI.

That is the whole thesis of `claude-code-slack-channel`'s 2026-05-20 wiring day. Eleven PRs landed in ccsc alone. ~6,800 LOC of insertions across them. The test suite went from 962 to 986. CRAP max stayed at 29, just under the 30 threshold. The reason that volume was even achievable in one day is that the hard problems — HMAC nonce HITL, stream-reply primitives, peer-bot rate limiting, the mute store, the Ed25519 audit signing keypair — had all been built and merged in prior weeks, gated behind feature flags or simply not wired into any inbound path. The day's work was wiring them up and giving operators a CLI to manage the now-live signing key.

The post is about that cadence: what it costs, what it buys, and what the integration day actually looks like when you do it.

## The morning of 2026-05-20: six dormant primitives

`claude-code-slack-channel` (ccsc) is a multi-agent Slack bridge. Humans and N Claude agents share a channel. Bots can talk to bots. Destructive admin verbs require a human in the loop via cross-channel HMAC nonce challenges. Every event flows through an [Ed25519](https://ed25519.cr.yp.to/)-signed audit journal stored as an [age-encrypted SOPS file](https://github.com/getsops/sops).

**What "ship dormant" means here.** A primitive ships complete and unit-tested but unwired — no production path calls it, no MCP tool exposes it, no feature flag in any channel turns it on. The diff lands in `main`. Production behavior is unchanged. The dormant interval is the gap between merge and activation. The pattern is a sibling of [dark launching](https://martinfowler.com/bliki/DarkLaunching.html) and [feature-flag deployment](https://martinfowler.com/articles/feature-toggles.html): build the artifact in production code, defer its activation as a separate, smaller change.

By the morning of 2026-05-20, six primitives sat in `main` exactly that way and none of them were active.

| Bead    | PR    | Shipped (dormant)                                                              |
| ------- | ----- | ------------------------------------------------------------------------------ |
| ccsc-ofn | #179 | HMAC nonce HITL primitives for destructive admin verbs (798 LOC)               |
| ccsc-3w0 | #180 | Admin commands hardened — !clear / !restart through full pipeline (1401 LOC)   |
| ccsc-ele | #181 | Stream-reply via progressive `chat.update` — 14 unit tests (839 LOC)           |
| ccsc-gyt | #182 | Peer-bot rate limit — per-(channel, bot_id) sliding-window cap (513 LOC)       |
| ccsc-gjm | #183 | `!mute` / `!unmute` operator verbs + mute store (806 LOC)                      |
| ccsc-22l | prior | Journal v2 with Ed25519 audit-signing keypair as first-class type              |

Each of those PRs shipped with its own unit tests, its own boundary, and its own integration story laid out in the description. None of them affected production behavior — which is the entire point. The dispatcher had no admin verbs wired in. The gate had no rate-limit store. The reply tool had no `stream` field on its input schema. The journal had no key to sign with. Bugs in any of them — and there were bugs, as the wiring PRs would later show — could not reach users until the wiring day.

PR #184 also landed that morning, separately from the wiring sequence: the `multi-agent` setup recipe doc covering humans plus N agents in one Slack channel. It made the multi-agent epic eligible to close once the wiring PRs landed.

You either find that posture sensible or terrifying. The cost is real and I will get to it. The payoff is what the wiring day looked like.

## Wiring day, in order

Six PRs activated the primitives. A seventh shipped the operator CLI.

### PR #185 — load the signing key at boot (ccsc-uge, 465 LOC)

The signing keypair lives in an age-encrypted SOPS file. On boot, ccsc has to decrypt it, parse it, and hand it to the journal writer — and refuse to start if anything is ambiguous.

The loader spawns `sops -d <path>` via `execFile`, pipes the plaintext to `crypto.ts:parseKeyPairYaml`, and returns an `AuditSigningResolution`:

```ts
// audit-key-loader.ts — actual discriminated union
type AuditSigningResolution =
  | { kind: 'loaded'; keypair: Ed25519KeyPair; staleWarning: boolean; source: string }
  | { kind: 'disabled'; reason: string }   // --no-audit-signing graceful v1 fallback
  | { kind: 'error'; reason: string };
```

The boot path is the load-bearing detail (simplified):

```ts
const noAuditSigning = parseNoAuditSigningFlag(process.argv.slice(2));
const resolution = await loadSigningKey({ noAuditSigning });
if (resolution.kind === 'error') {
  console.error(resolution.reason);
  process.exit(2);                 // refuse to start ambiguously
}
const signingKey = resolution.kind === 'loaded' ? resolution.keypair : undefined;
const initialPolicyDigest = signingKey ? policyDigest(policyRules) : undefined;
await JournalWriter.open({ path: journalPath, signingKey, policyDigest: initialPolicyDigest });
```

That ordering — load the key *before* the journal opens — is what makes the resolution meaningful. If we opened the journal first and tried to attach the key later, every event between open and attach would be unsigned, and the chain would already be invalid. Decrypted YAML lives in process memory only. Nothing touches disk.

The PR added 11 unit tests covering positional flag parsing, `~/` HOME expansion, decrypt failure, malformed YAML, tamper-checked public-key mismatch, the >90-day stale-key warning, and an end-to-end happy path where the loaded key signs an event that `verifyJournal` later accepts. 952 → 962 tests.

### PR #186 — wire the dispatcher into the inbound path (ccsc-0jj, 175 LOC)

Small PR. Big consequence. `tryDispatchAdminVerb(ev, access)` runs *before* `deliverEvent` in `handleMessage`. If a message parses as a recognized admin verb, the dispatcher handles it and we never send the text to Claude. If it does not parse as a verb, the dispatcher returns `false` and the normal chat path takes over.

The wiring is plumbing — `journalWrite → journal.writeEvent`, `sendTmuxKeys → createTmuxSendKeys(SLACK_TMUX_SESSION)` lazily, `issueChallenge → mintNonce + DM via web.chat.postMessage to user_id` (verb is in channel C, the nonce is delivered in a DM — that's the cross-channel HITL design from ccsc-ofn), `verifyChallenge → verifyNonce against adminNonceStore`, `muteStore → adminMuteStore`.

The interesting part is **boot guard R14**:

```ts
const hasAdminChannels = Object.values(bootAccess.channels).some(
  c => (c.adminCommands?.allowFrom ?? []).length > 0
);
if (hasAdminChannels && !process.env.SLACK_TMUX_SESSION) {
  console.error(
    'R14: channels declare adminCommands.allowFrom but SLACK_TMUX_SESSION is unset. ' +
    '!clear / !restart would silently no-op. Refusing to start.'
  );
  process.exit(1);
}
```

If any channel allows admin verbs and the tmux session env var is unset, the bridge refuses to boot. Half-wired admin paths are worse than no admin paths. Verbs would be recognized, journaled, the nonce challenge would send — and then the action would silently do nothing because there is no tmux session to send keys to.

Gemini caught a real bug in this PR. The runtime refusal on unset env was returning `false`, which meant the verb text fell through to Claude as ordinary chat content. That broke the ccsc-3w0 invariant that Claude never sees admin verbs as chat. The fix:

```ts
if (!tmuxSession) {
  // verb-specific kind: admin.clear.denied / admin.restart.denied
  await journalWrite({ kind: `admin.${verb}.denied`, reason: 'tmux_session_unset', ... });
  return true;   // verb was recognized, we just couldn't execute it
}
```

Return `true` because the verb was recognized. Journal a `.denied` event for forensics. The chat path doesn't get the text either way.

### PR #187 — wire the mute and rate-limit stores into the gate (ccsc-00f, 39 LOC)

Thirty-nine lines of code. Three weeks of dormant primitives going live.

After this PR, the peer-bot rate limit fires automatically the moment two bots start a loop in the same channel. Operator `!mute` actually silences a peer bot at the gate. The dispatcher (PR #186) and the gate (PR #187) share the **same** `adminMuteStore` instance — so when an operator mutes a bot, the next inbound message from that bot in that channel drops at the gate immediately.

A 60-second reaper interval prunes mute store on TTL, rate-limit store on all-timestamps-older-than-window, and nonce store on expiry. Gemini caught a HIGH-priority bug here. The reaper used a hardcoded 60-second prune window for `peerBotRateLimitStore`. An operator who configured `peerBotRateLimit.windowMs: 300_000` (a 5-minute sliding window) would have their timestamps destroyed every minute. The counter would reset constantly. The rate limit would never fire.

The fix is small and the reasoning is what matters:

```ts
// The reaper is for memory hygiene on idle buckets. The per-call check()
// does in-line pruning against each rule's actual windowMs. So the reaper
// only needs to use a window safely larger than any realistic custom window.
const RATE_LIMIT_REAP_WINDOW_MS = 60 * 60 * 1000;  // 1 hour
```

That comment is the lesson. The reaper is hygiene, not enforcement. Enforcement happens in `check()` on every call.

### PR #188 — wire stream-reply into the `reply` MCP tool (ccsc-h1h, 134 LOC)

The stream-reply primitive (ccsc-ele) had shipped weeks earlier with 14 unit tests pinning its cached-`ts` invariant: a long message becomes ONE growing Slack message via N-1 [`chat.update`](https://api.slack.com/methods/chat.update) calls on a cached `ts`, instead of N separate `postMessage` calls. None of the MCP tools called it.

The wire-up is a single optional field on the `reply` tool's input schema:

```ts
const ReplyInput = z.object({
  chat_id: z.string().min(1),
  text: z.string().min(1),
  thread_ts: z.string().optional(),
  stream: z.boolean().optional(),       // ← new
  // ...file_uploads, etc.
});
```

Backward compatible. Callers that don't pass `stream` get the unchanged multi-postMessage path. Callers that pass `stream: true` AND have text exceeding the chunk limit get delegated to `executeReplyStreamingPath()`. `streamReply` emits its own `gate.outbound.allow` event with a pre-committed full-text hash and a `system.stream_finalize` event when the cached-`ts` message is finalized. No per-chunk audit events — the design choice from ccsc-ele was that a stream is one logical reply, not N events.

Gemini surfaced three findings on this PR — one HIGH, two MEDIUM:

1. **HIGH.** `streamReply` events were missing `toolName` attribution. `streamReply` is a generic primitive — it doesn't know it's being called from `reply` versus some future tool. The fix was injecting `toolName: 'reply'` at the wire-up site so the audit log matches the non-streaming path's attribution.
2. **MEDIUM.** `postMessage` was not validating the returned `ts`. Slack returns one in the normal case, but rate-limit edge cases and malformed channels can return undefined. The fix throws cleanly so the init-failure path runs instead of cascading into N `chat.update` calls with `ts === undefined`.
3. **MEDIUM.** File-upload logic was duplicated between the streaming and non-streaming branches of `executeReply`. Extracted into `executeReplyFileUploads`. As a side effect, this dropped `executeReply`'s CRAP score from 33 (over the threshold) back under 30.

All three were real. None of them would have shown up in unit tests of `streamReply` in isolation — they only surface at the wiring boundary, where the generic primitive meets the production caller and its audit-log expectations.

### PR #189 — `ccsc audit-key {init, rotate}` operator CLI (ccsc-l1f, 1362 LOC, 24 unit tests, 962 → 986)

The signing key is now live in production. Operators need a way to manage it. PR #189 ships that surface.

Architecture: a pure module `audit-key-cli.ts` that holds all the logic, plus a thin runner `scripts/audit-key.ts` that wires real deps. All side-effecting deps — the `sops` subprocess, `fs`, `JournalWriter` — are injected. That is what makes 24 unit tests possible without ever invoking real SOPS or writing real keypairs.

The `init` pipeline:

1. Refuse overwrite — `init` is one-shot per state dir. Use `rotate` to replace.
2. Generate Ed25519 keypair via `crypto.ts:generateKeyPair`.
3. Serialize YAML via `serializeKeyPairYaml`.
4. Write `${keyPath}.tmp` with mode `0o600`.
5. `sops --encrypt --in-place ${keyPath}.tmp`.
6. Atomic rename `${keyPath}.tmp` → `${keyPath}`.
7. Print the public key for stashing in `pass` and gisting externally.

The `rotate` pipeline is gated by `--confirm-bridge-stopped` to prevent cross-process journal corruption:

1. Load and parse the current keypair via SOPS subprocess.
2. Generate the new keypair.
3. Open `JournalWriter` under the OLD signing key.
4. Write ONE `system.key_rotation` event carrying `input.old_public_key`, `input.new_public_key`, `input.rotation_reason` (enum).
5. Close the writer.
6. Encrypt and stage the new keypair as `${keyPath}.new.tmp` via `sops --encrypt`.
7. Archive: rename `${keyPath}` → `${keyPath}.${unix-ms}.archived`.
8. Install: rename `${keyPath}.new.tmp` → `${keyPath}`.
9. Print the new public key plus the archive path.

The ordering is the safety property. The rotation event is written under the OLD key, *before* the NEW key is installed. After install, every event from that point forward is signed by the NEW key. `verifyJournal` walks the chain, sees the rotation event signed by OLD, picks up the new public key from its payload, and verifies the rest of the chain with NEW. The rotation is auditable end-to-end without trusting any out-of-band notification.

Safety invariants enforced inline:

- `init` refuses to overwrite an existing key file. No silent clobber.
- Both verbs refuse on stale `.tmp` or `.new.tmp`. Those could be plaintext key material from an interrupted prior run. An operator has to verify and clean up manually — the CLI will not just delete them.
- `rotate` refuses without `--confirm-bridge-stopped`. The `ACTIVE_PATHS` lock only protects against same-process collision. Cross-process writers would interleave bytes and corrupt the journal hash chain. Out-of-band coordination is required.
- On encrypt failure during `init` or the new-key write in `rotate`, the plaintext `.tmp` is unlinked in the catch block. Plaintext key material never survives the CLI process.
- On final-install failure during `rotate`, the archive is restored. The operator is never left with no key file.
- On encrypt-new failure during `rotate`, the error message tells the operator that the rotation event WAS written under the OLD key, the audit log now expects NEW key signatures, and how to recover. That is the worst-case message and it has to be specific.

The happy-path rotate test is the one I keep going back to. It uses the real `JournalWriter` and real `verifyJournal`. It asserts that the rotation event verifies under the OLD key AND that subsequent events verify under the NEW key. That is acceptance criteria #3 and #4 for the bead, end-to-end, in a unit test, because all the side-effecting deps are injected.

> Every v0.10 primitive that had been shipped-but-dormant is now active in production with an operator-facing surface.

That is the commit body of PR #189. It is the whole point.

## Day stats

| Metric                | Value                                  |
| --------------------- | -------------------------------------- |
| PRs merged (ccsc)     | 11 (#179–#189)                         |
| Insertions            | ~6,800 LOC                             |
| Tests                 | 962 → 986 (+24, all in PR #189)        |
| CRAP max              | 29 (threshold 30)                      |
| depcruise             | 17 modules / 52 deps, 0 violations     |
| Coverage (post-#185)  | 96.94% line / 97.75% func              |

## What this cadence costs

Ship-dormant is not free. Three real costs:

**Surface area without exercise.** A primitive that exists but is not called by any production path is, by definition, only as well-tested as its unit suite. The integration story is on paper until the wiring day arrives. PR #186's boot-guard bug and PR #187's reaper-window bug are both examples of assumptions that held in unit tests and broke at the integration boundary. The multi-week dormant interval was deliberate — wiring six primitives in one coherent activation was the goal, not a one-primitive-per-day stagger that would have left the bridge in half-wired states for weeks. But that decision is the cost: an earlier wire-in would have caught these bugs earlier. The honest read is that the cadence trades early bug discovery for activation coherence.

**Dead-code anxiety.** While ccsc-ele was dormant, you could have read the codebase and asked: why does this stream-reply path exist if nothing calls it? The honest answer is "we are going to wire it in soon" and "soon" sometimes means three weeks. That is real cognitive load on anyone reading the code who is not the author. The mitigation is the bead system — every dormant primitive has a bead ID, a status, and a description of its activation plan — but the mitigation only works if you actually read the beads.

**Trust the tests, without an end-to-end loop.** Between merging a dormant primitive and wiring it in, you are trusting the unit suite to be a faithful proxy for production behavior. That trust held here — every primitive worked when activated, modulo the wiring-boundary bugs that Gemini caught and we fixed in the wiring PRs themselves. It will not always hold. The discipline that makes it hold is writing the unit tests against the interface the wiring will use, not the interface the primitive author finds convenient. PR #181's 14 cached-`ts`-invariant tests are the canonical example. They pinned a contract that PR #188 then relied on, and the contract held.

## What this cadence buys

The wiring day itself. Eleven PRs in one day is achievable because every PR is doing one thing — flipping one switch, wiring one store, adding one optional schema field. None of those PRs had to *design* the thing they wired in. The design conversation happened weeks ago. The wiring PR is `+39 LOC`. The CLI PR is bigger because the CLI is the new surface, but even there the *primitives* it composes — `generateKeyPair`, `serializeKeyPairYaml`, `JournalWriter.open`, the SOPS subprocess pattern — were all already there.

This is the same posture as the audit-harness staged install pattern used across Intent Solutions repos: ship the enforcement scaffold first, then activate. It is also the pattern behind every mature feature-flag deployment and every progressive-delivery rollout — defer the activation switch from the architectural change so each step is independently reviewable. The activation PR is small because the scaffold did the heavy lifting. The reviewer can hold the whole activation in their head. Gemini can catch real bugs in it because the diff is comprehensible. The risk of any single activation PR is bounded.

## Also shipped

The 2026-05-20 day was not just ccsc. Five other repos moved.

- **intentional-cognition-os**: five npm releases in one day (v1.1.1 → v1.2.2). The release pipeline itself was being debugged in production. PR #76 fixed a release-ordering bug — `build before tests, sync workspace versions, publish to npm`. PR #78 fixed a race condition in release-after-publish flows by polling for npm propagation up to 120s instead of `sleep 5`. PR #77 scaffolded the dogfood trail and the `/ico-your-internals` skill. PR #79 authored the intent-eval-core-v1 question bank.
- **claude-code-plugins** (the marketplace): 5 PRs — homepage "Heat check" editorial picks card replaced the static starter pack (#755), the Level Up Upwork-only card replaced with a contact form (#756), the ga4-pack 5-skill starter pack landed (#754), the kobiton readme badge plus per-partner `logoHeight` sizing (#753), and a CI script-quality close.
- **hustle**: Phase 4 db starter — 5 core schemas + a Firestore → Drizzle mapping (PR #42), test cleanup (4 obsolete Phase-3-orphan suites deleted, Resend mock fix), and a CI fix (vitest devDeps + strip GCP/Firebase wiring from branch-protection).
- **intentsolutions-vps-runbook**: Caddy access logging wired for redirect domains (PR #22).
- **partner-portals**: Kobiton blog 3 editorial revision (soften overclaims, fix factual errors, correct hook names and behavior verified against PR #70).

That spread is what a day looks like when most of the architectural work happened on prior days. Most of the activity is activation, wiring, polish, and CI hygiene. None of it is "now let's design X."

## Related Posts

- [Five Tags, Zero Ships — Release Workflow Bug Anatomy](/posts/five-tags-zero-ships/) — 2026-05-19, the inverse: five tags shipped, zero actual ships.
- [V1 Release Gate — Conditional GO](/posts/v1-release-gate-conditional-go/) — 2026-05-18, the same theme of *when* to flip the activation switch on infrastructure that has been built up.
- [Forge Dogfood — Plane Plugin, Grade A, JRig-Verified Loop](/posts/forge-dogfood-plane-plugin-grade-a-and-jrig-verified-loop/) — 2026-05-07, integration tests catching what unit tests can't.
