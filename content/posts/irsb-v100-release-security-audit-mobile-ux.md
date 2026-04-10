+++
title = 'IRSB v1.0.0 Release Prep: Security Audit Scaffold and Mobile UX'
slug = 'irsb-v100-release-security-audit-mobile-ux'
date = 2026-01-28T10:00:00-06:00
draft = false
tags = ["irsb", "release-engineering", "security-audit", "mobile-ux", "solidity", "erc-8004", "x402"]
categories = ["Development Journey"]
description = "Eleven commits toward IRSB v1.0.0: README rewrite, ERC-8004/x402 standards integration, mobile UX improvements, legal pages, and a 15-item security audit scaffold with validation tooling."
+++

Eleven commits, all in the IRSB monorepo. This was v1.0.0 release prep — the gap between "it works" and "it's ready."

## README Rewrite

The old README was a developer's scratchpad. Bullet points about what each package did, a quickstart that assumed you already knew the architecture, and a diagram made in ASCII that didn't match the current package structure.

The rewrite targets three audiences in order: evaluators (what is this and why should I care), operators (how do I deploy and run it), and contributors (how do I develop against it). Each audience hits the section they need within 10 seconds of landing on the page.

The architecture diagram moved from ASCII to a Mermaid flowchart embedded in the README. GitHub renders it natively. The diagram shows the four-layer stack: chain contracts, subgraph indexing, API gateway, and dashboard frontend.

## CLAUDE.md Update

The CLAUDE.md got updated to reflect the current monorepo structure. Package boundaries, build commands per package, test commands, and the deployment pipeline. This matters because Claude Code reads CLAUDE.md first when entering the repo, and outdated guidance means wasted context on every session.

## ERC-8004 and x402 Standards

IRSB adopted two emerging standards:

**ERC-8004** defines a standard interface for on-chain agent registries. IRSB's operator registry already did most of what ERC-8004 specifies, but the function signatures and event names were different. The refactor aligned them. Now any tooling built for ERC-8004 works with IRSB's registry out of the box.

**x402** is a payment protocol for agent-to-agent transactions. IRSB's bounty resolution already handles payments, but x402 adds a standard envelope format that other protocols can interoperate with. The integration was additive — the existing payment flow still works, and x402-formatted requests get parsed and routed through the same settlement logic.

Neither standard is finalized. The implementation is behind a feature flag (`ENABLE_ERC8004=true`, `ENABLE_X402=true`) so the protocol can track spec changes without breaking the stable codepath.

## Mobile UX Improvements

The dashboard was built desktop-first. Three specific mobile issues got fixed:

**Table overflow.** The operator list table had 8 columns. On mobile, the rightmost columns were clipped with no scroll affordance. Added horizontal scroll with a fade gradient on the right edge to signal more content.

**Touch targets.** Action buttons were 24px square — fine for mouse, too small for fingers. Bumped to 44px minimum per Apple's HIG. The visual size stays at 24px; the touch target is a transparent 44px hit area around it.

**Bottom nav collision.** On iOS Safari, the bottom navigation bar overlaps fixed-position elements. Added `env(safe-area-inset-bottom)` padding to the footer and any bottom-anchored modals.

## Legal Pages

Added Terms of Service, Privacy Policy, and a Disclaimer page. These aren't boilerplate — the Terms specifically address the protocol's limitation of liability for on-chain enforcement actions, the Privacy Policy documents what the subgraph indexes (public chain data, not PII), and the Disclaimer clarifies that IRSB is infrastructure, not financial advice.

The legal pages are Markdown rendered by the same Next.js pipeline as the docs. Version-controlled, diffable, and dated with a "Last Updated" field.

## Security Audit Scaffold

This is the infrastructure for the formal audit, not the audit itself.

### IRSB-SEC-001 Through IRSB-SEC-015

Fifteen security items cataloged with severity (CRITICAL, HIGH, MEDIUM, LOW), status (OPEN, IN_PROGRESS, RESOLVED, WONT_FIX), and a description of the attack vector.

The critical items: reentrancy in the bounty settlement function, unchecked return values on token transfers, and missing access control on the operator registry's `deactivate` function.

The high-severity items: frontrunning on bounty claims, oracle manipulation in the evidence verification step, and gas griefing on the resolver callback.

Each item has a template: attack vector description, proof-of-concept sketch, proposed mitigation, and a checkbox for "verified by test." The template exists so the eventual auditor can see the team already identified these vectors and evaluate the mitigations.

### security.sh Validation

A shell script that runs the security checklist against the codebase. It checks:

- Slither static analysis passes with no HIGH or CRITICAL findings
- All `IRSB-SEC-*` items with status RESOLVED have a corresponding test file
- No `selfdestruct` or `delegatecall` in production contracts
- All external calls use the checks-effects-interactions pattern

The script exits 0 if everything passes, exits 1 with a report of failures if not. It's meant to run in CI as a pre-merge gate.

### PR Template Updates

The PR template now includes a security section: "Does this PR modify contract logic? If yes, list affected IRSB-SEC items." This forces contributors to think about the security surface of every contract change.

## Forge Formatting

Ran `forge fmt` across all Solidity files. Twenty-three files reformatted. The formatting was inconsistent because different contributors had different Prettier configs. Forge's built-in formatter is now the standard, enforced by a CI check.

---

Eleven commits. v1.0.0 isn't shipped yet, but the scaffolding is in place: the README explains the project, the security audit has structure, and the mobile experience doesn't embarrass us.

### Related Posts

- [IRSB Public Site Redesign and git-with-intent v0.5.0 Release](/posts/irsb-public-site-redesign-gwi-v050-release/)
- [Deep Dive Part 1: Five On-Chain Enforcers That Make AI Agent Wallets Structurally Safe](/posts/irsb-deep-dive-1-on-chain-enforcement/)
- [Lumera-Emanuel Launch and git-with-intent Open-Source Release](/posts/lumera-emanuel-launch-gwi-open-source-release/)
