+++
title = 'Citations'
description = 'Shared citation corpora for the startaitools deep-dive series. Every source verified against Semantic Scholar or a canonical DOI before inclusion.'
date = 2026-05-16T10:00:00-05:00
draft = false
noindex = true
+++

# Citation Corpora

Each ecosystem on this site maintains a shared citation corpus that all deep-dive articles in that series draw from. The corpus is verified once per release: every source has either a Semantic Scholar `paperId` recorded with a match score of at least 0.70, or it is a canonical non-S2-indexed reference (older paper, government standard, vendor specification) with a stable URL or DOI cross-checked manually.

The point of a shared corpus is twofold:
1. **Coherence.** When four articles in the same series cite Saltzer & Schroeder (1975), they cite the same DOI with byte-identical bibliographic formatting.
2. **Auditability.** A reader who wants to check the literature behind an article can read the source list once instead of repeatedly across articles, and a reviewer can verify every reference in one pass.

---

## Wild Ecosystem corpus

**Files:** [`wild-citations.bib`](https://github.com/jeremylongshore/startaitools/blob/main/content/citations/wild-citations.bib) (BibTeX) · [`wild-citations.jsonl`](https://github.com/jeremylongshore/startaitools/blob/main/content/citations/wild-citations.jsonl) (per-source verification metadata with `claim_anchors`)

**Covers:** [Wild Ecosystem](/wild-ecosystem/) hub · [Part 1: Safety Architecture](/posts/wild-deep-dive-1-safety-architecture/) · [Part 2: CLAUDE.md](/posts/wild-deep-dive-2-claude-md/) · [Part 3: Observability Loop](/posts/wild-deep-dive-3-observability/) · [Part 4: Claude Code as Tech Lead](/posts/wild-deep-dive-4-tech-lead/)

**Topics:** capability-based access control, attribute-based access control, audit-log integrity, distributed-systems tracing, supervision trees, session types, two-phase commit, indirect prompt injection, language-model red teaming, long-context attention degradation, sycophancy, agent paradigms, software-engineering automation.

---

## IRSB Ecosystem corpus

**Files:** [`irsb-citations.bib`](https://github.com/jeremylongshore/startaitools/blob/main/content/citations/irsb-citations.bib) (BibTeX) · [`irsb-citations.jsonl`](https://github.com/jeremylongshore/startaitools/blob/main/content/citations/irsb-citations.jsonl) (per-source verification metadata with `claim_anchors`)

**Covers:** [IRSB Ecosystem](/irsb-ecosystem/) hub · [Part 1: On-Chain Enforcement](/posts/irsb-deep-dive-1-on-chain-enforcement/) · [Part 2: Evidence Pipeline](/posts/irsb-deep-dive-2-evidence-pipeline/) · [Part 3: Watchtower Architecture](/posts/irsb-deep-dive-3-watchtower-architecture/) · [Part 4: AI-Agent Pivot](/posts/irsb-deep-dive-4-ai-agent-pivot/) · [Guidewire MCP v0.1.0](/posts/guidewire-mcp-v0-1-0-foundation-ship/)

**Topics:** Ethereum EIP-7702 delegation and ERC-7710 redemption, payment-channel watchtowers (Pisa, Cerberus, Outpost), smart-contract security and formal verification (Z3, Oyente, ZEUS, Hawk), Byzantine consensus and finality (Casper FFG, Tendermint, PBFT), MEV and frontrunning, off-chain computation patterns, cryptographic audit-log integrity, agent paradigms and prompt-injection threats, EU AI Act compliance, and enterprise-integration architecture (Parnas, Brooks).

---

## Methodology

The verification pipeline reactivated for this work is documented at [`~/.claude/skills/deep-research/references/semantic_scholar_api_protocol.md`](https://github.com/jeremylongshore/startaitools) (v4.0, MCP-native). Each candidate source is resolved via `mcp__semantic-scholar__paper_title_search` or `paper_details` with a Levenshtein title-similarity threshold of 0.70 against the cited title; matches scoring above the threshold are recorded with the Semantic Scholar `paperId` and external identifiers (DOI, ArXiv, DBLP, MAG) in the `.jsonl` companion file. References that are not S2-indexed (e.g., older papers, vendor specifications, government standards) are flagged with `verification_method: manual_*` and a stable URL or DOI is recorded in their place.

This corpus does not claim to be a complete bibliography of the topics it covers. It is the working set of sources the deep-dive articles in this series cite. New sources are appended as needed; existing entries are not modified without bumping the entry's verification timestamp.
