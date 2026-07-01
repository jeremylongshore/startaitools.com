1/ Anthropic shipped Claude Tag on June 23 — the best agentic teammate you can rent. Tag @Claude in Slack and it works: zero setup, a strong managed sandbox, compounding memory, central governance. If you want an agent in Slack tomorrow with no infra, it's excellent. Use it. #ai

2/ But honestly assessing an agent means naming what you accept in exchange. Claude Tag runs on Anthropic's substrate: sandbox, memory, audit log all on their infra, under their control. The organizational knowledge Claude builds stays theirs. Not exportable. Vendor lock-in is real.

3/ For most teams, that's fine. Zero-ops and compounding memory beat owning the infrastructure. But regulated shops, security vendors, and teams whose answer to "prove what your agent did" must survive an adversary who controls the log — those teams can't afford vendor-shown records.

4/ Here's the hard part the security literature spells out: filters aren't a boundary. InjecAgent (ACL 2024) found GPT-4 vulnerable to indirect injection 24% of the time. Adaptive Attacks (NAACL 2025) broke ALL EIGHT evaluated defenses, >50% ASR. Probabilistic models can't be the decider.

5/ You need three things: (1) a deterministic gate the model can't talk past, (2) human-in-command approval BEFORE consequential actions run, and (3) a record you can verify yourself, with your own key, no vendor in the trust path. Three pillars of owning the substrate.

6/ CCSC (Claude Code Slack Channel) and AGP (Agent Governance Plane) build exactly those three pillars. CCSC is the governance kernel — pure `evaluate(call, rules, now)` logic, deterministic policy, per-action approval. AGP hardens it into default-deny + sandboxed multi-harness execution + signed-HEAD checkpoints.

7/ The verifiable audit is the sharpest line. Claude Tag: you view Anthropic's log. CCSC/AGP: you verify a hash-chained, Ed25519-signed journal offline with only a public key. AGP adds a signed HEAD checkpoint — so the verifier catches truncation even if the chain is technically clean.

8/ The honest limits: CCSC doesn't stop a host-OS compromise or same-UID process. AGP's sandbox is namespace/cgroup, not VM — a kernel exploit defeats it. Live Codex interception isn't yet CI-validated. Verifiability is a property of the record, not a force field around your infra.

9/ Both legitimate tradeoffs. Claude Tag: zero setup, free memory, multiplayer UX. CCSC/AGP: you host, you build the memory, you own the substrate and hold a proof no vendor can erase. Pick by who must own what. [LINK: startaitools post]

10/ Open source: github.com/jeremylongshore/claude-code-slack-channel (governance kernel) and github.com/jeremylongshore/agent-governance-plane (sandboxed multi-harness). Both ready to run on your infrastructure. Same prove-don't-trust discipline.
