+++
title = 'Rent the Agent, Own the Proof'
slug = 'rent-the-agent-own-the-proof'
date = 2026-06-30T08:00:00-05:00
draft = false
tags = ["ai-agents", "claude-code", "security", "mcp", "governance", "slack", "audit", "architecture"]
categories = ["Technical Deep-Dive"]
description = "Anthropic's Claude Tag is the best agentic teammate you can rent. The question it doesn't answer: who owns the memory, and who can verify the audit log? Here's what customer-owned, verifiable agent governance looks like in code."
tldr = "Claude Tag ships a genuinely strong agent into Slack with a sandbox, credential proxy, deny-by-default egress, central admin governance, and compounding memory, all with zero infrastructure. The trade is ownership: the substrate, memory, and audit log are Anthropic's. CCSC and AGP make the opposite trade with fine-grained deterministic policy, per-tool-call human approval, and an offline-verifiable audit you check with your own public key."
+++

On June 23, 2026, Anthropic [shipped Claude Tag](https://www.anthropic.com/news/introducing-claude-tag): tag `@Claude` in a Slack channel and it works as an agentic teammate: running tool calls, following threads, building memory, acting under your org's identity. The legacy "Claude in Slack" chat app [retires August 3, 2026](https://www.techtimes.com/articles/319206/20260627/claude-tag-brings-ambient-ai-slack-admins-have-until-august-3-migrate.htm); admins get 30 days to migrate. It is, by a distance, the best agentic teammate you can *rent*.

I want to be honest about that up front, because the interesting question isn't whether Claude Tag is good. It's good. The interesting question is the one it doesn't answer: **when an agent has admin-scoped tools in your workspace, who owns the memory it builds, and who can verify the log of what it did?**

## Give Claude Tag its due

A hit piece would be easy and wrong. Claude Tag's engineering is strong, and the honest version of this argument starts by saying so:

- **Zero infrastructure.** No servers, no deploy, no on-call. Tag the bot, it works. Nothing self-hosted competes on setup cost.
- **Multiplayer shared context.** "One Claude that interacts with everyone" in a channel: anyone can see what it's working on and pick up where the last person left off.
- **Compounding memory.** It "learns over time… builds more context about the work," and can learn across channels with permission.
- **Central governance.** Admins specify which tools and data the model can touch, per channel. Usage is billed to the org. Admins can set **token-spend caps** per org and per channel.
- **A genuinely good security model.** Work runs in an **isolated sandbox on Anthropic's infrastructure**. When it needs an external system, requests cross an **Agent Proxy** where, per launch coverage, credentials "stay in a store and are injected at the network boundary without the model receiving raw keys," with a **default policy of deny** for un-allowlisted hosts.

That last point deserves emphasis, because it's the part people underrate: keeping raw credentials out of the model and defaulting egress to deny is *exactly* the posture a security-minded self-hosted stack would build. Anthropic did the hard, correct thing. If you want an agent in Slack tomorrow with no infrastructure, Claude Tag is an excellent product and you should use it.

So this is not "their thing is insecure." It's a different question entirely.

## The trade you're actually making

Every one of those benefits shares a root: **the substrate is Anthropic's.** The sandbox is on their infrastructure. So is the memory. As [AlphaSignal argues](https://alphasignalai.substack.com/p/the-real-claude-tag-question-is-context), the real Claude Tag question is context ownership. The organizational knowledge Claude builds becomes the vendor's proprietary state, not an exportable dataset your next vendor can ingest. The principle is simple: rent the agent, but own the memory. Claude Tag inverts it because you rent the agent *and* the memory lives with the vendor. Critics have named the deeper trap the same way: [not model lock-in but *context* lock-in](https://ksingh7.medium.com/everyones-worried-about-model-lock-in-but-the-real-trap-is-context-lock-in-af04c16167b0). The concern is not that Anthropic is doing anything wrong. The incentives are simply obvious.

Two more things live on that substrate, and they matter more than memory portability:

1. **Governance is coarse.** Admin control means *which channels*, *which tools/data*, and *spend caps*. That is scope plus budget. It is not a documented, mandatory human approval **before each consequential tool call executes**.
2. **The audit log is the vendor's.** Admins "can view a log of everything that @Claude has done." You can *view* Anthropic's record. You cannot *verify* it, independently, with your own key, with no vendor in the trust path.

For a lot of teams, none of that is a dealbreaker, and they should use Claude Tag. But for a regulated shop, a security vendor, or anyone whose answer to "prove what your agent did" has to survive an adversary who controls the log's storage, coarse governance and a vendor-shown record aren't enough. That's the gap two open-source projects were built to fill.

## Why filters were never the boundary

Before the alternative, the premise: for a tool-using agent reading untrusted text, every Slack message is untrusted input. **Content filtering is not a security boundary.** This is true of *any* Slack-connected agent, CCSC and AGP included, not Claude Tag in particular. The answer is not a better filter; it is a different architecture. The literature is blunt about this. [InjecAgent](https://arxiv.org/abs/2403.02691) (Findings of ACL 2024) found ReAct-prompted GPT-4 vulnerable to indirect prompt injection 24% of the time, with private-data exfiltration a primary attack class. Worse, [Adaptive Attacks Break Defenses Against Indirect Prompt Injection](https://arxiv.org/abs/2503.00061) (NAACL 2025) bypassed **all eight** evaluated defenses, keeping attack success above 50%. And because tools reached over MCP are "first-class, composable objects with natural-language metadata," [MCP Security Bench](https://arxiv.org/abs/2510.15994) shows the standard *enlarges* the attack surface through name-collision, tool-description injection, and out-of-scope parameters.

The takeaway isn't "add a better filter." It's that a probabilistic model cannot be the thing that decides whether a destructive action runs. You need **a deterministic gate the model can't talk its way past, a human in the loop for the consequential calls, and a record of what actually ran that you can trust without trusting the runtime.** That's three properties, and they're the three pillars of what I'll call customer-owned, verifiable governance.

Two reference implementations: **[CCSC](https://github.com/jeremylongshore/claude-code-slack-channel)** (Claude Code Slack Channel), a small auditable governance kernel that puts Claude Code in Slack behind exactly these gates; and **[AGP](https://github.com/jeremylongshore/agent-governance-plane)** (Agent Governance Plane), which reimplements-and-hardens that kernel with sandboxed execution across multiple agent harnesses. AGP doesn't vendor CCSC or depend on it: it's an independent reimplementation ("adapt-and-harden") pinned to CCSC's v0.10.0 design. Both are open source; you run them on your own infrastructure.

### Pillar 1: Deterministic, fine-grained policy (not a probabilistic scope)

The oversight literature lays out a [spectrum](https://arxiv.org/abs/2507.14034), from human-out-of-the-loop through human-on-the-loop. Claude Tag's channel scope sits low on it: a coarse boundary set once, per channel. Fine-grained governance sits higher, and it looks like capability-based security: [Miller's object-capability model](https://en.wikipedia.org/wiki/Object-capability_model) and the principle of least authority, where authority is granted per *operation*, not per *door*. Established capability-security work is explicit that coarse role/scope access [over-privileges by construction](https://arxiv.org/abs/1909.12279) and that fine-grained capabilities are how you get least authority at scale.

In CCSC, that's a pure decision procedure: `evaluate(call, rules, now)` maps a tool call to `allow | deny | require` with no side effects, same inputs, same verdict, every time. Tiered rules resolve strictest-wins, then first-applicable. Out of the box, one tool, `upload_file`, defaults to fail-closed (denied unless a rule allows it); every other tool follows the policy *you* author, so making the actions that matter in your workspace fail-closed is a rule you write, not a default you inherit. AGP takes the harder line and bakes it in: its engine is **default-deny with deny > require > allow**, so a call that matches no rule fails closed to deny, not allow. That's precisely what "AGP hardens the kernel" means. Neither ships an `if (model === "claude")` branch anywhere near the decision; the gate is data, evaluated before execution.

The difference from a spend cap is the whole point. A token budget limits *how much* the agent can do. A policy engine decides *whether this specific action* is allowed, and can force a human into the loop for the ones that matter.

### Pillar 2: Human-in-command approval, per tool call

On the oversight spectrum, the mode that matters for consequential actions is **human-in-command**: the action does not execute until a human approves it. Not "review the log afterward." Not "set a budget." A blocking approval on *this* call, *before* it runs.

CCSC's `require` verdict routes to a human approver: approval is a reply-code the gate recognizes, with quorum counted by distinct user IDs, and because permission-reply messages from peer bots are dropped at the inbound gate, an injected message can't cast an approving vote. A separate, stronger handshake guards the admin command path (`!restart`): a single-use 64-bit nonce DM'd out of band, TTL-bounded, checked against wrong-channel replay, built specifically to defeat a same-channel-approval attack, an [EchoLeak](https://arxiv.org/abs/2509.10540)-class injection where the request *and* the approval both originate in a compromised channel. AGP renders the per-call approval as Slack Block-Kit Approve/Deny buttons whose nonce is bound to `(messageId, sessionId)`, and crucially, **a bot can never approve, and a bot's click doesn't even burn the nonce.**

This is the pillar Claude Tag most visibly doesn't have. Admin scope decides what tools are reachable; there's no public evidence of a mandatory per-action human approval before each consequential call. For a broad class of "summarize the thread" work you don't want one. For "open this PR," "message this customer," "run this migration," a lot of orgs very much do.

### Pillar 3: A signed audit you can verify without trusting the runtime

This is the sharpest line between renting and owning, so be precise about what "verifiable" means. Claude Tag gives admins a log they can *view*. CCSC and AGP produce a log you can *verify*: a different verb.

CCSC's journal is a hash chain: each entry commits `sha256(prevHash ‖ canonicalJson)`, so any reordering or edit breaks every downstream link. Each entry is then **Ed25519-signed over RFC 8785 JSON Canonicalization**, and carries a `policy_attestation` digest recording exactly which rules were in force when the decision was made. You verify the whole thing offline, `bun server.ts --verify-audit-log <path>`, with **only the public key**. No vendor. No live service. Key rotation is supported, so the verifier still works across a rotation. This follows the [Certificate Transparency](https://datatracker.ietf.org/doc/html/rfc6962) design lineage: append-only logs a third party can check without trusting the operator. It is the same lineage as verifiable ledger databases like [GlassDB](https://doi.org/10.14778/3583140.3583152) and recent work on [Certificate-Transparency-style provenance for agent action chains](https://arxiv.org/abs/2509.18415), where external verifiers cryptographically validate what an agent did without access to the runtime.

And here's the honest, load-bearing detail most "verifiable log" claims skip: **a bare hash chain does not stop truncation.** If an attacker drops the last N entries, the remaining chain still verifies clean. CCSC documents this as threat T8, out loud, in its threat model. AGP closes exactly that hole: it writes a **signed HEAD checkpoint**, a `<journal>.head` file pinning `{seq, hash}`, so the offline verifier catches a truncated tail a chain alone cannot. `agp verify` checks the chain, the signatures, *and* the signed head, offline, with only the public key. That's what owning the proof buys you: not "trust our log," but "here is a record, check it yourself, and check that none of it was quietly cut off."

### The fourth property AGP adds: a sandbox that *proves* egress is off

Claude Tag's sandbox is on Anthropic's infrastructure. AGP's runs on yours, and it does not *assume* isolation. It *proves* it. Containers launch with `--network none`, `--cap-drop ALL`, `no-new-privileges`, and pid/memory limits, with **no silent fallback to the host** if hardened flags fail. Then a **network preflight** actually runs an egress probe to a TEST-NET-1 address and **fails closed**, tearing the container down, if traffic is *not* isolated. Images are pinned by digest, or at minimum a specific version tag, never `latest`, and host secrets are mounted through a deny-list. The credential posture matches Claude Tag's Agent Proxy: gate, do not impersonate. AGP holds no model credentials, and `{{secret:NAME}}` is resolved only *after* the gate, at the exec boundary. The journal records secret *names*, never values.

## The part where I don't oversell it

The reason to trust any of this is that both projects are relentless about their own limits, and I'm not going to break that streak here.

CCSC does **not** protect you against a compromised host OS, a same-UID process, a supply-chain attack, or a socially-engineered operator at their own terminal. Its threat model says so explicitly. Its manifest *consumer* doesn't ship yet, so cross-bot identity is still just `bot_id`. T8 truncation is also a real gap in CCSC alone. *AGP* fixes it, which is the whole reason AGP exists.

AGP's sandbox is namespace/cgroup isolation, **not** a VM. A kernel exploit or container escape defeats it, and the code comments say exactly that. Its multi-harness claim rests on a deterministic reference contract and a conformance test that drives Claude Code and Codex through identical governance; **live Codex interception is provisional and not yet CI-validated.** AGP's own docs rate the current test suite a B-minus (78/100). And its marketing-claims scanner *bans* the words "tamper-proof," "forensic-grade," and "compliance-grade" in CI, which is why I've said **signed and offline-verifiable** throughout, and not one of those. A log can be signed and still be stolen wholesale if your host is owned. Verifiability is a property of the record, not a force field around your infrastructure.

That discipline is the point. A governance layer that oversells itself is worse than none, because it manufactures the exact false confidence it was supposed to remove.

## So: rent, or own?

Both stacks share one architectural signature, **prove-don't-trust: a deterministic gate, a human-in-command approval, and a signed record you can check.** AGP takes it furthest and makes fail-closed the *default*: default-deny, no-decision-means-deny, egress *runtime-verified* off rather than assumed, an unresolved secret throws, an unpinned image throws. CCSC brings the deterministic policy, the human-in-command gate, and the signed record, and leaves which operations fail closed to the policy you author. Put together, it's one posture: don't trust the runtime, make it prove itself, and keep a record you can check. The single sharpest thing they do that a rented, vendor-logged agent doesn't is produce **a publicly verifiable, offline audit**, and AGP's signed-HEAD checkpoint closes the exact truncation hole CCSC documents. That's the difference between a log you're shown and a proof you hold.

Claude Tag is the best agent you can rent, and for most teams that is the right answer. Take the zero-setup, the multiplayer memory, the strong sandbox, and go. But if your governance model needs the agent, its memory, and its audit trail to be **yours**, on **your** infrastructure, and **verifiable with your own key**, then you host it. You give up the free memory and the zero-ops UX; you get a substrate no vendor can revoke, relocate, or rewrite.

Both are legitimate engineering positions. The question was never which agent is smarter. It's who has to own the substrate, and who has to be able to prove what happened.

---

*CCSC and AGP are open source: [claude-code-slack-channel](https://github.com/jeremylongshore/claude-code-slack-channel) (the governance kernel) and [agent-governance-plane](https://github.com/jeremylongshore/agent-governance-plane) (sandboxed, multi-harness). A companion post, [Gate the Statement, Not the Tool Name](/posts/gate-the-statement-not-the-tool-name/), walks through the capability-based gate at the statement level.*

## References

- Anthropic (2026). *Introducing Claude Tag.* anthropic.com/news/introducing-claude-tag
- Wulf, J., Meierhofer, J., & Hannich, F. (2025). *Architecting Human-AI Cocreation for Technical Services.* arXiv:2507.14034: the human-in-command / human-on-the-loop oversight spectrum.
- Zhan, Q., Liang, Z., Ying, Z., & Kang, D. (2024). *InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated LLM Agents.* Findings of ACL 2024. arXiv:2403.02691.
- Zhan, Q., Fang, R., Panchal, H., & Kang, D. (2025). *Adaptive Attacks Break Defenses Against Indirect Prompt Injection Attacks on LLM Agents.* NAACL 2025. arXiv:2503.00061.
- Zhang, D., et al. (2025). *MCP Security Bench (MSB).* arXiv:2510.15994.
- Reddy, P. & Gujral, A. S. (2025). *EchoLeak: Zero-Click Indirect Prompt Injection in Microsoft 365 Copilot (CVE-2025-32711).* arXiv:2509.10540.
- Zigmond, E., Chong, S., Dimoulas, C., & Moore, S. (2019). *Fine-Grained, Language-Based Access Control for Database-Backed Applications (ShillDB).* arXiv:1909.12279.
- Yue, C., et al. (2023). *GlassDB: An Efficient Verifiable Ledger Database System Through Transparency.* PVLDB. doi:10.14778/3583140.3583152.
- Malkapuram, S., Gangavarapu, S., Kavalakuntla, K. R., & Gangavarapu, A. (2025). *Context Lineage Assurance for Non-Human Identities in Critical Multi-Agent Systems.* arXiv:2509.18415.
- Laurie, B., Langley, A., & Kasper, E. (2013). *Certificate Transparency.* RFC 6962, IETF.
- AlphaSignal (2026). *The Real Claude Tag Question Is Context Ownership.* alphasignalai.substack.com
