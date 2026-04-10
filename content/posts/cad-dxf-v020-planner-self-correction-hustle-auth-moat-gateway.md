+++
title = 'CAD Agent v0.2.0: Planner Self-Correction, Hustle Auth Consolidation, and Moat Dual-Mode Gateway'
slug = 'cad-dxf-v020-planner-self-correction-hustle-auth-moat-gateway'
date = 2026-02-24T10:00:00-06:00
draft = false
tags = ["ai-agents", "cad", "authentication", "security", "mcp", "blockchain", "testing", "python"]
categories = ["Development Journey"]
description = "Eight commits ship a validation feedback loop for the CAD planner, a single-cookie auth consolidation kills an XSS vector in Hustle, and Moat gets a dual-mode MCP/Web3 gateway."
+++

Three projects, twelve commits, and the most interesting one is a feedback loop that teaches the planner to fix its own mistakes.

## CAD Agent v0.2.0: Validation Feedback Loop

The CAD agent's planner takes a natural language prompt and returns a structured changeset. The validator checks whether that changeset is safe to apply. In v0.1.0, a validation failure meant the user got an error message and had to rephrase their prompt.

That's a bad user experience. The planner knows the drawing context. It knows what it tried. If the validator says "entity X doesn't exist on layer Y," the planner has enough information to try again with the correct layer. It shouldn't need the user to mediate.

v0.2.0 adds a feedback loop. When validation fails, the error gets fed back to the planner as additional context, and the planner generates a corrected changeset. Up to 3 retry attempts before giving up and surfacing the error to the user.

The implementation is straightforward:

```python
def plan_with_feedback(prompt, drawing_context, max_retries=3):
    changeset = planner.plan(prompt, drawing_context)

    for attempt in range(max_retries):
        errors = validator.validate(changeset, drawing_context)
        if not errors:
            return changeset

        feedback = format_validation_errors(errors)
        changeset = planner.plan(
            prompt,
            drawing_context,
            correction_context=feedback
        )

    return PlanResult(errors=errors, exhausted_retries=True)
```

The `correction_context` parameter is the key. It tells the planner what went wrong without changing the original prompt. The planner sees: "You tried to move entity handle 3A on layer 'COLUMNS' but that handle is on layer 'GRID'. Available entities on 'COLUMNS': [3B, 3C, 3D]."

In testing against the mock provider, the feedback loop resolves ~60% of validation failures on the first retry. The remaining failures are genuine ambiguity in the user's prompt that no amount of retrying will fix.

**Live PDF-to-edit journey tests.** End-to-end tests that start from a PDF structural drawing, extract a DXF (via an external converter), parse it, apply edits through the full pipeline, and verify the output. These caught a real bug: the DXF writer was dropping block attribute overrides during serialization. The attributes existed in memory but didn't survive the write-to-disk path.

**Backend dependency fix.** A version pin conflict between `ezdxf` and `matplotlib` that only manifested on clean installs. CI was passing because the cache had a compatible combination. Fresh `pip install` from `requirements.txt` failed. Pinned `matplotlib<3.9` to resolve it.

**DevOps playbook.** A runbook covering local dev setup, CI configuration, release tagging, and the manual test checklist. The kind of document you write after the third time someone asks "how do I run this."

## Hustle: Single Cookie Auth Consolidation

Hustle (hustlestats.io) had an auth problem that wasn't a bug but was a security risk.

The auth system used two cookies: `__session` (the Firebase session cookie, HttpOnly, server-verified) and a fallback `firebase-auth-token` cookie that was set client-side. The fallback existed because early development had client components that needed auth state before the server middleware ran.

The fallback cookie was not HttpOnly. It was readable by JavaScript. Which means any XSS vulnerability anywhere in the app could steal the auth token.

The consolidation was two changes:

1. Remove the fallback cookie entirely. All auth flows now go through the single `__session` cookie.
2. Update every client component that was reading the fallback cookie to instead call a server action that checks the session cookie and returns the auth state.

The second part was the real work. Seven components were reading the fallback cookie directly. Each one needed a server action wrapper. But the tradeoff is clear: a small performance hit from the additional server roundtrip versus an XSS vector that could compromise any authenticated user.

## Moat: Dual-Mode MCP/Web3 Gateway

Moat's gateway got a significant upgrade: it now speaks both MCP (Model Context Protocol) and Web3 protocols through a single entry point.

**MCP mode** handles AI agent requests. An agent calls a Moat tool through the MCP server, and the gateway evaluates the request against the policy engine, executes it through the appropriate adapter, and returns the result with a receipt.

**Web3 mode** handles on-chain operations. EIP-712 typed data signing for structured on-chain messages. When an agent needs to submit an on-chain transaction (like recording a receipt on Sepolia), the gateway constructs the EIP-712 payload, signs it with the agent's delegated key, and submits it.

The dual-mode design means the same gateway handles both off-chain API calls and on-chain transactions. A single policy engine evaluates both. A single receipt system logs both. The agent doesn't need to know whether its action is going to an API or a blockchain — it calls the same Moat tool either way.

**Testing patterns and error hierarchy.** Two commits built the test infrastructure for the dual-mode gateway. The error hierarchy separates policy violations (denied by rule), execution failures (adapter crashed), and receipt failures (on-chain submission failed). Each error type carries different context and triggers different retry behavior. Policy violations are terminal. Execution failures are retryable. Receipt failures queue for async retry.

The test patterns use a builder for policy fixtures:

```python
policy = PolicyBuilder() \
    .allow("http.proxy", domains=["api.github.com"]) \
    .deny("http.proxy", domains=["*.internal"]) \
    .require_receipt("eth.transfer", chain="sepolia") \
    .build()
```

Clean enough to read as documentation. Specific enough to catch edge cases in policy evaluation order.

## The Day in Numbers

| Project | Commits | Key Outcome |
|---------|---------|-------------|
| cad-dxf-agent | 8 | v0.2.0 — planner self-correction, PDF-to-edit tests |
| hustle | 2 | Single-cookie auth, XSS vector eliminated |
| moat | 2 | Dual-mode MCP/Web3 gateway with EIP-712 |

Twelve commits. The planner feedback loop is the most architecturally significant — it's the difference between a tool that errors and a tool that tries harder. The Hustle auth consolidation is the most important for users, even though they'll never know it happened. The Moat gateway is the most forward-looking: a single policy surface for both off-chain and on-chain agent actions.

---

## Related Posts

- [Shipping a CAD Agent from Zero: DXF Parsing, Edit Engines, and LLM Planner Interfaces](/posts/building-cad-dxf-agent-from-zero-to-v010/) — The v0.1.0 that v0.2.0 builds on
- [Building Moat: Auth, On-Chain Receipts, and 117 Tests](/posts/building-moat-auth-persistence-onchain-receipts-117-tests/) — Moat's original architecture before the dual-mode upgrade
- [Session Cookie Auth, Forgot-Password Timeouts, and Killing Flaky E2E Tests](/posts/session-cookies-forgot-password-flaky-e2e-tests/) — The earlier Hustle auth work that created the fallback cookie this post removes
