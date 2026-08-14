+++
title = 'Dictated From a Phone'
slug = 'dictated-from-a-phone'
description = 'The operator is often not at a desk. The loop is talk, agents build, deterministic gates check, receipts land in the repo. Here are the exact tools, the concurrency, and the part that makes voice a workable interface to a 191-repo estate.'
date = 2026-08-13T09:00:00-05:00
draft = false
weight = 20
tags = ["agents", "llm", "workflow", "tailscale", "voice"]
categories = ["AI Engineering"]
toc = true
+++

The most common question about this setup is where the desk is. Frequently there isn't one. A
large share of the work that produced 598 commits was dictated by voice from a phone, over a
private network, to a machine that then ran the actual build.

The tailnet on 2026-08-13 shows the shape of it. Alongside the dev box, the production VPS and
the relay host sit an iPad, active on a New York relay with 11.5 MB sent and 2.5 MB received, and
an iPhone. Those two are not spare screens. On a lot of days they are the office.

## The loop

Four steps, and only the second one involves a language model.

1. **Talk.** Dictate intent into a terminal session over the tailnet. Not commands, intent.
2. **Agents build.** One or more models take the intent and produce code, docs, schemas, beads.
3. **Deterministic gates check.** Bash and Python, no model, refuse anything that fails.
4. **Receipts land.** Beads, evidence bundles, decision records and a CHANGELOG entry commit
   alongside the work.

Step three is what makes step one survivable. Dictating to an agent is only reasonable if
something other than your attention is checking the result, because the thing you cannot do from
a phone while moving is careful review. So the review is mechanical, and it is the same review
whether you dictated the task or typed it.

## What is actually running

The transport is Tailscale, and SSH is reachable only over the tailnet. The firewall allows port
22 on the `tailscale0` interface and nowhere else, which is what makes the rest of the posture
safe. The clients are Termius and Moshi, both of which survive a network change without dropping
the session, and that property is the difference between usable and not. A connection that dies
every time the phone switches towers is not a workstation.

On the dev box, sessions are tmux, and there are more of them than people expect. Measured on
2026-08-13:

```
$ ps -eo comm= | grep -c '^claude$'
14
$ tmux ls | wc -l
12
```

Fourteen concurrent agent processes across twelve sessions, on one machine, with one human. They
are not all working on the same thing. That is the actual parallelism: not one agent going fast,
but a dozen going at once on separate repositories, each in its own working tree.

## The models, by exact version

Naming these vaguely is how people end up unable to reproduce anything, so:

| Model | Where it runs |
|---|---|
| Claude Opus 5 | Primary interactive and agent work |
| Claude Fable 5 | Secondary interactive sessions |
| MiniMax-M3 | Headless cron agent harness, and the blog producer fallback |
| DeepSeek | Provider in the eval and refine stack |
| Grok | Default headless agent for two nightly jobs |

The MiniMax-M3 harness is worth describing because it shows what a cron-side agent looks like
when it is built rather than bought. It is a single Python file that speaks chat completions with
a tool-use loop, and it exposes exactly one tool to the model: `shell_exec(command, timeout)`.
The harness runs the command as `/bin/bash -c` in a given working directory and hands back
`{exit_code, output}` as JSON. The loop ends on the first assistant message with no tool calls.
Exit 0 means it finished, 2 means it hit the turn limit, 3 means timeout.

That is the entire agent. The interesting engineering is not in the harness, it is in what the
harness is allowed to touch and what checks its output afterward.

It exists because the previous provider started returning HTTP 402 on 2026-07-23, mid-pipeline.
The replacement was written the same day, keyed off a SOPS-encrypted secrets file, and left
behind the default rather than in front of it: the nightly jobs still run the original agent, and
the new one is opt-in by environment variable until it has proven itself over consecutive nights.
A fallback you switched to in a panic is not yet a fallback you trust.

## Beads, or why compaction stopped mattering

The failure mode specific to long agent sessions is context loss. You work for three hours, the
context window compacts, and the agent no longer knows why it was doing any of this.

The fix is that the task state was never in the context window. It is in beads, a local
issue tracker with a Dolt database underneath, one atomic commit per operation. Every claim,
note, dependency and close is a row with history. After a compaction, the recovery command
reloads the state from disk, and the work continues.

The estate on the 2026-08-12 snapshot held 1,125 open issues across 49 databases, with 46 in
progress or blocked at that moment. The intent-os database alone holds 497 issues, of which 280
are closed. That closed count is the useful one: it is a record of finished work that no context
window ever had to hold.

Beads also carries the memory that outlives sessions. A durable fact gets written once and
resurfaces in every future session in that repository, which means the same correction does not
have to be dictated twice. Dictating a correction is expensive. Dictating it repeatedly is how
people give up on voice.

## What voice is bad at

It should be said plainly, because the honest version is more useful than the pitch.

Voice is poor at anything positional. Naming a file is fine. Naming a line range, a column, or
which of three similar functions you meant is slow and error-prone, and homophones make
identifiers worse: model names, flags and repo slugs come through mangled and have to be
resolved from context rather than heard.

So the work that gets dictated skews toward intent, review and direction, and away from precise
edits. "The ownership page should never report a percentage over an empty governed population" is
a good dictated sentence. "Change line 41 to `>=`" is not; by the time you have said it
unambiguously you could have typed it.

The compensating move is that agents are good at exactly the thing voice is bad at. You supply
the intent and the judgment, which are hard to type and easy to say. They supply the positional
precision, which is easy to type and miserable to say. The gates then check the result, because
neither of you should be trusted with that part.
