+++
title = 'Lumera-Emanuel Launch and git-with-intent Open-Source Release'
slug = 'lumera-emanuel-launch-gwi-open-source-release'
date = 2025-12-20T10:00:00-06:00
draft = false
tags = ["encryption", "sqlite", "mcp", "ci-cd", "open-source", "security"]
categories = ["Development Journey"]
description = "Full Lumera-Emanuel bootstrap: AES-256-GCM encryption, SQLite storage, CASS memory, 4 MCP tools, 35+ tests, and CI/CD. Plus git-with-intent goes MIT with a responsible disclosure policy."
+++

Two projects shipped on December 20th. One was brand new. The other opened its doors.

## Lumera-Emanuel: Privacy-First Agent Memory

Lumera-Emanuel went from empty repo to working system in 11 commits. The goal: a privacy-first memory layer for AI agents that encrypts everything at rest and gives the agent structured recall without leaking user data to the host.

### Encryption Layer

The core storage is SQLite with AES-256-GCM encryption. Every memory entry gets encrypted before it touches disk. The encryption key derives from a user-provided passphrase via PBKDF2 with a unique salt per entry. No plaintext ever persists.

```python
def store_memory(key: str, value: str, passphrase: str) -> None:
    salt = os.urandom(16)
    derived_key = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    ).derive(passphrase.encode())

    aesgcm = AESGCM(derived_key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, value.encode(), None)
    # Store salt + nonce + ciphertext in SQLite
```

480,000 PBKDF2 iterations is the OWASP recommendation for SHA-256. About 200ms to derive the key on modern hardware — imperceptible to a user, painful for a brute-force attacker. Each entry gets its own random salt and nonce, so identical plaintext produces different ciphertext every time. If someone copies the database file, they get noise.

### CASS Memory Model

On top of SQLite sits CASS — Contextual Associative Structured Storage. Memories aren't flat key-value pairs. Each entry has a context tag, an association graph linking related memories, and a structured metadata envelope.

When an agent recalls a memory, it gets the associated context too. Ask for "last deployment failure" and the recall includes the fix that resolved it, the team member who helped, and the config change that prevented recurrence.

The association graph is bidirectional. Store a memory about a deployment failure and link it to the rollback procedure. Later, when the agent retrieves the rollback procedure for a different reason, the linked deployment failure surfaces as context. The agent builds a web of related experiences instead of a flat list of isolated facts.

### MCP Tools and Test Suite

Four MCP tools expose the memory system: `store`, `recall`, `search`, and `forget`. The `forget` tool is deliberate — privacy-first means users can delete their data, and the agent respects that without caching deleted entries. Forget cascades through the association graph.

35 tests cover the encryption round-trip, association graph traversal, concurrent access patterns, and the MCP tool interface.

The encryption tests verify that changing a single byte in the passphrase produces a decryption failure, that the same plaintext encrypted twice produces different ciphertext, and that the salt/nonce are never reused.

The concurrency tests matter because agents run async. Ten concurrent writers, each storing and linking memories simultaneously, then verify the graph is consistent after all writes complete. SQLite's WAL mode handles the concurrent writes, but the association graph updates needed explicit transaction boundaries to prevent partial link states.

CI/CD runs the full suite on every push with GitHub Actions. The entire bootstrap from empty repo to green CI took a single day.

## git-with-intent Goes MIT

Five commits on git-with-intent, and the biggest one changed a file most developers never read: the license.

The project moved to MIT. Full open-source, no restrictions, no conversion timeline. The previous BSL-1.1 license was defensible for a pre-GA product, but with the security posture stable, the restriction period was creating friction for potential contributors without providing real protection.

### Responsible Disclosure

Alongside the license change, a responsible disclosure policy went live. Security vulnerabilities get reported through a dedicated channel with a 90-day coordinated disclosure window.

The policy includes specifics: which components are in scope (all MCP tools, the encryption layer, the SQLite storage engine), what counts as a valid vulnerability (anything that bypasses encryption, leaks plaintext, or allows unauthorized memory access), and expected response times (acknowledgment within 48 hours, triage within 7 days).

### Security Posture Document

The security posture document covers the threat model for the whole platform: tenant isolation, API authentication, and the trust boundary between agents and the git-with-intent runtime.

The threat model is organized by attack surface: network-facing APIs, agent-to-tool communication, inter-tenant data boundaries, and the CI/CD pipeline itself. Each surface has documented mitigations and residual risks. Not marketing copy — actual threat modeling that a security reviewer can audit.

The remaining commits were housekeeping: dependency pinning to SHA digests for the CI workflows and a README section linking to the new security policy. Small details that signal maturity to anyone evaluating whether to depend on the project.

---

A launch and a release on the same day. Lumera-Emanuel starts encrypted. git-with-intent starts open.

### Related Posts

- [git-with-intent v0.9 to v0.10: Docker Upgrades, README Rewrites, and Strategic Research](/posts/git-with-intent-v090-v0100-docker-upgrades/)
- [Fixing Provider Registry Mutations and Sandbox Permissions](/posts/fixing-provider-registry-mutations-sandbox-permissions/)
- [Software Supply Chain Security](/posts/software-supply-chain-security/)
