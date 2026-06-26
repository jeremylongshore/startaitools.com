+++
title = 'N Bots in One Slack Channel Loop Forever: Three Gates'
slug = 'bot-loop-circuit-breaker-multi-agent-slack'
date = 2026-06-23T08:00:00-05:00
draft = false
tags = ["multi-agent", "slack", "bots", "rate-limiting", "reliability"]
categories = ["Architecture"]
description = "Put N AI agents in one Slack channel and, left ungated, they answer each other forever. The three moves that make a shared multi-agent channel safe."
+++

Put two AI agents in the same Slack channel and let each one reply to anything it sees, and you have built a perpetual motion machine. A answers a human. B sees A's message and answers it. A sees B's answer and answers *that*. Neither one is wrong. Neither one is broken. They will keep going until you kill a process, because each message is, from Slack's point of view, a legitimately distinct event that deserves a response.

This post is about `claude-code-slack-channel` — the substrate that lets humans, Claude Code sessions, and peer agents share one channel — and the three commits-worth of work it took to make that channel *safe* when more than one bot is in it. The thesis is one sentence: safety for a multi-agent channel is three moves, not one. You gate who gets to speak (mention-to-engage), you trip a breaker when speech runs away (a channel-wide circuit breaker), and you keep the whole thing observable and bounded under load (backpressure plus structured drop reasons). Pull any one and the other two don't save you.

## The problem: bots answer each other forever

The peer-bot feedback loop is the failure that defines the domain. By default a channel ignores other bots entirely; the loop only becomes possible once an operator explicitly opts peer bots in via an `allowBotIds` allowlist. But that opt-in is exactly what you *want* — the whole point of a shared channel is agents collaborating — so "just don't allowlist bots" isn't a fix, it's a refusal to build the feature.

The moment two bots are on the allowlist, A's reply is an inbound event for B, B's reply is an inbound event for A, and the exchange has no natural terminator. Ordinary event-dedup doesn't help: dedup catches the *same* event arriving twice, but A's third message and B's fourth message are genuinely new events. The loop is made of distinct, valid messages. That's what makes it nasty — every individual step looks correct.

The obvious fix is "only respond when you're spoken to" — require an @-mention before a bot engages. And it works, right up until a human tries to actually have a conversation. A mention-gate that demands a fresh `@bot` on *every single message* is too dumb to use: the human mentions the bot, gets an answer, types a follow-up, and gets silence, because the follow-up didn't re-mention. So they re-mention. Every turn. The channel becomes a place where you shout the bot's name before each sentence. Mention-gating that's correct but unusable isn't a fix; it just trades one failure for another.

So the real problem has two halves that have to be solved together: stop bots from talking to bots, without making the channel miserable for the humans. Three moves do it.

## Move one: mention-to-engage, but thread-sticky

The first move makes mention-gating usable. A `requireMention` channel drops any message that doesn't @-mention the bot — *except* once a human has engaged a thread by mentioning the bot, subsequent human messages in that same thread are delivered without a fresh mention. Mention once to open the thread, then converse. The engaged thread is recorded in a set keyed by the session thread, so a top-level mention and its in-thread follow-ups resolve to the same slot.

```ts
// Illustrative — the requireMention branch of the channel gate.
if (policy.requireMention && !isMentioned(ev, botUserId)) {
  // Thread-sticky: a human who already mentioned the bot in this
  // thread keeps the floor without re-mentioning every turn.
  if (!ev.bot_id && opts.engagedThreads !== undefined) {
    const threadTs = (ev.thread_ts ?? ev.ts) as string | undefined
    if (opts.engagedThreads.has(deliveredThreadKey(channel, threadTs))) {
      return { action: 'deliver', access }
    }
  }
  return { action: 'drop', dropReason: 'channel.require_mention' }
}
```

Three details in that branch are load-bearing. **Peer bots are never sticky** — the `!ev.bot_id` guard means an allowlisted bot has to mention the target on *every* message to be delivered, so a bot can't ride a human's engaged thread into a loop. Stickiness is a convenience extended to humans only. **A mention is still required to open a thread** — stickiness lowers the cost of staying in a conversation, never the cost of starting one. And **the engaged set is bounded**: it evicts its oldest entry past a cap, so a busy channel can't grow it without limit. A convenience feature that leaks memory is a slow outage.

The matching gate also has to be careful about what counts as a mention. A human pasting a code snippet or quoting an earlier message that contains `<@bot>` is displaying the token, not addressing the bot. So the matcher prefers Slack's structured `blocks` and prunes the `rich_text_preformatted` (code block) and `rich_text_quote` (blockquote) subtrees before looking for the mention — a `<@bot>` buried in a fenced code block can't falsely engage the channel. It falls back to substring matching only when structured blocks are absent.

Finally, the interaction mode itself is a first-class channel choice, and new channels default to mention-to-engage. The safe posture is the default; opening the floodgates is the thing you opt into, not the thing you forget to turn off.

## Move two: a channel-wide circuit breaker for N-cycle rings

Mention-gating handles the well-behaved case. The breaker handles the runaway one — when something gets past the gate anyway, or when two bots are *supposed* to talk and the conversation goes feral.

The first layer is a per-`(channel, bot_id)` sliding window: track each bot's message timestamps, and once a single bot exceeds the threshold (default 10 messages in 60 seconds) in a channel, drop that bot's messages until the window slides back under. That's tuned well above any plausible legitimate cross-bot rate — humans interleave their messages, loops don't — and it cleanly breaks the *pairwise* A→B→A case.

But the pairwise limit has a blind spot, and it's the kind you only see when you reason about it adversarially. A longer A→B→C→D→E→A *ring* keeps every individual sender under its own per-bot cap. Five bots each posting every seven or eight seconds sit at roughly eight messages a minute apiece — comfortably under the cap of ten — so a counter that only ever watches one bot at a time reports all-clear while their combined velocity runs away. That's the threshold math, and it's worth saying out loud: a two- or three-bot ring is *caught* by the per-bot counter, because for three bots to sum past a 40/60s aggregate at least one has to exceed its own 10/60s cap. The aggregate breaker earns its keep precisely when the ring is large enough — five or more — that every member can hide under the per-bot limit.

So a second counter sits on top: a channel-wide aggregate that sums peer-bot velocity across *all* bots in the channel and trips when the total runs away.

```ts
// Illustrative — two counters, two scopes, checked in order on the inbound gate.
if (!perBotWindow.check(channelId, botId, now, perBotLimit)) {
  return { action: 'drop', dropReason: 'rate.cross_bot_loop' }   // pairwise A→B→A
}
if (!channelWindow.checkChannel(channelId, now, breakerConfig)) {
  return { action: 'drop', dropReason: 'rate.channel_cycle' }    // N-cycle ring A→B→C→D→E→A
}
```

The aggregate default is roughly 4× the per-bot limit (40 messages in 60 seconds), chosen so a legitimate two- or three-bot exchange interleaved with real human work never trips it, but a runaway ring — which fires as fast as the pipeline allows — trips it within seconds.

It helps to trace the ring against both counters to see why the second one earns its place:

```text
# Illustrative — an A→B→C→D→E→A ring under a 10/60s per-bot cap and a 40/60s breaker.
# Five bots, round-robin, one message every ~1.5s.
t=00.0s  A posts   per-bot[A]=1   channel=1
t=01.5s  B posts   per-bot[B]=1   channel=2
t=03.0s  C posts   per-bot[C]=1   channel=3
t=04.5s  D posts   per-bot[D]=1   channel=4
t=06.0s  E posts   per-bot[E]=1   channel=5
t=07.5s  A posts   per-bot[A]=2   channel=6     # each bot only ~ every 7.5s — per-bot stays near 8, never 10
...
t=58.5s  ...        per-bot[*]≈8   channel=40    # every bot under its cap, but the ring trips the AGGREGATE → rate.channel_cycle
```

Each bot paces itself to about eight messages in the window — under its own cap of ten — while the channel total climbs to 40 and the breaker fires. The per-bot counter, watching each bot in isolation, would have let this five-way ring run indefinitely. Three properties keep the aggregate honest:

- **Humans always post freely.** Both counters only apply to events where `bot_id` is set. A human in a melting-down channel is never rate-limited; the throttle is aimed exclusively at the machines.
- **It's disablable, with one coherent semantic.** Setting the config to `{ count: 0, windowMs: 0 }` short-circuits to "always allow" in both the store and the gate. (That non-positive-config path was a follow-up fix — the original code had a dead branch where a zero config didn't actually disable cleanly. To deny *all* peer-bot delivery you don't zero the limit; you set `allowBotIds: []`. Two intentions, two switches.)
- **It's deliberately not persisted.** A process restart resets every counter. Same posture as the channel's nonce store: a fresh process means no stale state for a misbehaving bot to game, and the breaker re-derives from live traffic in one window.

| Counter | Scope | Catches | Default |
|---|---|---|---|
| Per-bot sliding window | one `(channel, bot_id)` | pairwise A→B→A loops | 10 / 60s |
| Channel circuit breaker | all bots in a channel | N-cycle A→B→C→A rings | 40 / 60s |

Neither counter alone is sufficient. The per-bot limit can't see a ring; the aggregate limit can't tell you *which* bot is the offender. Layered, they cover both the pair and the ring.

## Move three: backpressure and observability

The third move is what turns a channel you've *gated* into one you can actually *operate*. Loops aren't the only way a multi-agent channel hurts you — a burst of legitimate new conversations can exhaust resources just as effectively, and a channel where you can't see *why* a bot went quiet is one you can't debug.

**A global backpressure cap.** The session supervisor takes a `maxConcurrentSessions` limit; once live plus in-flight activations hit the cap, a genuinely *new* session is refused rather than spun up. The load-shed decision is both logged to the operator and written to the audit journal — a refusal is a governance event, not a silent drop. One subtle correctness note: the cap counts *distinct* in-progress sessions, because a session that just finished activating is briefly present in both the "live" set and the "activating" set, and naively summing the two would double-count it and reject sessions spuriously near the cap.

```ts
// Illustrative — refuse a NEW session at the cap; count distinct in-flight keys.
let inFlightNew = 0
for (const k of activating.keys()) if (!live.has(k)) inFlightNew++
if (live.size + inFlightNew >= maxConcurrentSessions) {
  journalWrite({ kind: 'session.activate_rejected', outcome: 'deny', /* ... */ })
  return Promise.reject(new Error('at maxConcurrentSessions cap'))
}
```

**A structured drop reason on every gate drop.** Every inbound message the gate turns away now carries a typed `dropReason`, and that reason lands in the journal. The reasons are grouped by the gate stage that produced them — which is itself a readable map of how an inbound event is evaluated, in order:

- **bot-event stage** — `self.echo` (our own message), `bot.not_allowlisted`, `admin.muted`, `rate.cross_bot_loop`, `rate.channel_cycle`, `bot.permission_relay`.
- **top-level stage** — `subtype.filtered` (an edited or deleted message, intentionally ignored), `event.no_user`.
- **DM stage** — `dm.policy_closed`, `dm.pairing_cap`, `dm.pending_full`.
- **channel stage** — `channel.not_opted`, `channel.allowfrom_miss`, `channel.require_mention`.

The payoff is operational: when a bot stays silent, you can always answer "why didn't it respond?" by reading one field instead of guessing. Silence stops being ambiguous. An enum beats a free-text string here because the reasons are a closed set you want to count, filter, and alert on — `rate.channel_cycle` spiking is a signal you can build a dashboard on; a string blob isn't.

**Read-only admin verbs from Slack.** Operators can ask the channel about itself without changing anything: `!mute-status` lists active peer-bot mutes and their remaining TTL, `!rate-limit` shows the effective thresholds, `!agents` lists the peer bots seen active recently. The `!agents` view is derived from the per-`(channel, bot)` activity the rate limiter already tracks — the same timestamps that feed the breaker double as an "agents online" read-out, no separate bookkeeping. These are pure observation verbs — no argument, no state change — sitting alongside the destructive `!clear`/`!restart` commands but carrying none of their risk. You shouldn't have to SSH into a box to find out which bots are live in a channel.

**A targeted mute, between the allowlist and the breaker.** The allowlist is all-or-nothing per bot; the breaker is all-or-nothing per channel. Between them sits `!mute @bot`, which silences one specific peer bot in one channel for a TTL — its messages drop with `dropReason: 'admin.muted'` until the mute expires. That's the surgical option: when exactly one bot is misbehaving, you don't have to choose between de-allowlisting it everywhere or tripping the whole channel's breaker. You mute the one offender and leave the rest of the conversation running.

**Per-user session isolation, opt-in.** A channel can opt into keying sessions by `(channel, thread, userId)` instead of the shared `(channel, thread)`, so two humans working in the same thread get independent sessions that don't observe each other's state. It's default-off and default-safe: no flag means the legacy shared key, behavior unchanged. The guard validates the sender id is a non-empty string before keying on it, so a malformed event falls back to the shared session rather than constructing a broken key.

## Why the three compose

It's tempting to ship one of these and call the channel safe. Each one alone leaves a hole the other two close.

Mention-gating without a breaker assumes every actor honors the gate. The moment a bot is *meant* to be in the conversation — allowlisted, mentioning correctly — the gate waves it through, and two such bots can still loop. The breaker is the backstop for actors the gate legitimately admits.

A breaker without mention-gating is all backstop and no front door. You'd let every bot respond to everything and rely on rate limits to clean up the mess — which means the channel is constantly tripping its own breaker, and the humans are drowning in bot chatter below the trip threshold. Gating keeps the normal case quiet so the breaker only fires on genuine runaways.

And both of those without observability is a system that's safe but unoperatable. When a bot goes quiet you can't tell whether it hit the mention gate, tripped the breaker, got muted, or crashed — so you can't tune any of it. The structured drop reasons and the read-only verbs are what let you see which gate is firing and adjust the thresholds with evidence instead of superstition.

## The ceiling, named honestly

What this earns is bounded, and worth stating plainly so nobody oversells it.

The breaker is **velocity control, not intent control.** It stops a *fast* loop — the kind that fires as fast as the pipeline allows. Two bots having a slow, wrong conversation at one message every ten seconds stay under every threshold and will happily waste tokens all afternoon. The defense against *that* is the mention gate and the allowlist, not the rate limit; the breaker is specifically the runaway-velocity backstop, and calling it a general "bad conversation detector" would be a lie.

The counters are **in-memory and per-process.** A restart resets them — deliberately, but it means a multi-process deployment doesn't share a breaker, and the cap is per-supervisor, not global across a fleet. At single-channel, single-process scale that's the right amount of machinery; the day this runs as a horizontally-scaled service, the counters need a shared backing store, and that's a real piece of work, not a config flag.

And the thresholds are heuristics. 10-per-60s and 40-per-60s are tuned for the realistic loop shape, but they're operator-tunable for exactly the reason that the right number depends on your channel's legitimate traffic. The defaults are a safe starting point, not a proof.

## The principle

A shared channel is a place where independent actors — human and machine — touch the same surface, and the reflex is to assume each actor will behave. For humans that's mostly true. For bots it is exactly false: a bot does precisely what it's told, forever, including answer another bot that's answering it.

So you don't make a multi-agent channel safe with one clever gate. You gate who may speak, you trip a breaker when speech runs away, and you keep the whole thing observable so you can see which defense is doing the work. Mention-to-engage keeps the normal case calm. The circuit breaker catches the loops the gate admits. Backpressure and structured drop reasons keep it bounded and debuggable under load. Three moves, each covering the other two's blind spot. Anyone putting more than one bot in one room needs all three.

---

**Related posts:**

- [MCP Server Auth: The API Is the Real Boundary](/posts/the-api-is-the-real-boundary/) — the same instinct applied to auth: knowing which layer is the actual boundary and which is just UX.
- [Honor the Gate When the Verdict Is Inconvenient](/posts/honor-the-gate-when-the-verdict-is-inconvenient/) — a gate is only worth building if you respect its drops.
- [The Merge Is the Trust Boundary: Re-Derive as Untrusted](/posts/govern-at-merge-untrusted-union/) — properties don't compose across a boundary you didn't enforce yourself.
