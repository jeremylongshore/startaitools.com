+++
title = 'Nixtla BSL License Pivot'
slug = 'nixtla-bsl-license-pivot'
date = 2026-01-06T10:00:00-06:00
draft = false
tags = ["licensing", "open-source", "governance", "documentation"]
categories = ["Development Journey"]
description = "Two commits, one decision: pivoting Nixtla's licensing from MIT to Business Source License 1.1 and generating the DOCX for legal review."
+++

Two commits. One governance decision. The thinnest day of the month so far.

## Why BSL 1.1

Nixtla's baseline lab has been MIT-licensed since inception. MIT is the default choice for developer tools — maximum adoption, zero friction, everyone can use it however they want.

The problem with MIT for a commercial product: competitors can take your code, wrap a paid service around it, and sell it back to the same market you're trying to serve. You built it. They profit from it. Your only competitive advantage is moving faster, which is not a sustainable moat when someone with a bigger team can fork and iterate.

Business Source License 1.1 changes the equation. The code is source-available — anyone can read it, study it, and use it for non-production purposes. But production use requires a commercial license during the protection period. After the protection period expires (typically 3-4 years), the code converts to a fully permissive open-source license.

BSL 1.1 has precedent. HashiCorp moved Terraform to BSL. MariaDB uses BSL for MaxScale. CockroachDB uses a BSL variant. The pattern: build in the open, protect commercial viability, and eventually release everything to the commons.

## The Implementation

Two commits:

1. **LICENSE file swap** — Replace MIT license text with BSL 1.1 template, customized with Nixtla-specific parameters: change date, change license (Apache 2.0 after the protection period), and the production use definition.

2. **DOCX generation prompt** — A structured prompt for generating the license in DOCX format for legal review. The legal team doesn't review markdown files. They review Word documents with tracked changes. The prompt produces a properly formatted DOCX with all the standard legal document sections: definitions, grant of rights, conditions, limitation of liability, and the time-based conversion clause.

That's it. Two commits. No code changes. No feature work. Pure governance.

## The Tradeoff

The honest risk: BSL reduces adoption. Developers see "non-MIT" and move on. Some won't read past the license name. Some will read the terms and decide the production restriction doesn't work for their use case. The contributor pool shrinks because external contributors are wary of contributing to code they can't freely use.

The honest upside: the code stays commercially viable. If Nixtla's baseline lab becomes the standard tool for time-series forecasting validation, BSL ensures that commercial value flows back to the people who built it. MIT doesn't guarantee that. MIT doesn't even try.

Whether this is the right call depends on where Nixtla sits on the adoption-vs-revenue curve. Early stage, you want maximum adoption — MIT wins. Growth stage with a clear market and competitors emerging — BSL protects the business. Nixtla is at the inflection point where the question shifts from "will anyone use this?" to "who's going to profit from this?"

## Two-Commit Days

Some days produce 87 commits across 11 repos. Other days produce 2 commits in one repo. The governance work matters as much as the code work. Probably more. A licensing decision affects every line of code in the repository, past and future. It's the kind of thing you get right once and never touch again.

The DOCX generation prompt is a small detail worth noting. Legal teams have their own tooling expectations. Meeting them where they are — Word docs with standard formatting — removes friction from the review process. Don't make lawyers use GitHub to review a LICENSE file. Export it to their format and let them do their job.

Two commits. One decision that changes the commercial trajectory of the entire project.

---

## Related Posts

- [Nixtla Enterprise Docs Restructure and v1.0.0 Release](/posts/nixtla-enterprise-docs-restructure-v100-release/) — The enterprise positioning that prompted the licensing conversation
- [Nixtla Security Hardening, Docs Redesign, v1.7.0](/posts/nixtla-security-hardening-docs-redesign-v170/) — Governance and documentation maturation in the same repo
- [Nixtla BSL, CI Cost Optimization, Code Quality v1.5.0](/posts/nixtla-ci-cost-optimization-code-quality-v150/) — Earlier governance and quality work on the Nixtla baseline lab
