+++
title = 'The LLM Should Never Do the Math'
slug = 'llm-never-does-the-math'
date = 2026-06-26T08:00:00-05:00
draft = false
tags = ["ai-agents", "claude-code", "architecture", "finops", "databricks"]
categories = ["Technical Deep-Dive"]
description = "A Claude Code skill that hunts Databricks cost leaks and reports confirmed dollars from the customer's own billing tables — never LLM estimates."
+++

A CFO will not act on a number an LLM eyeballed. They will not act on a number the model "estimated" by reasoning over a usage dump. And they should not — because the moment a language model emits a dollar figure it computed itself, that figure is a guess wearing the costume of a fact.

This is the design constraint behind `databricks-cost-leak-hunter`, the pilot skill of the databricks-pack v2 rebuild shipped in the claude-code-plugins marketplace ([PR #906](https://github.com/jeremylongshore/claude-code-plugins)). Given a live, authenticated Databricks workspace, it surfaces real cost leaks across four named categories, ranks them by monthly dollar impact, and emits a report a finance reader can act on. The marketplace validator graded it B (88/100, zero errors). The SKILL.md is 329 lines. The single most important thing in it is a rule the model is structurally prevented from breaking: **the LLM never does the dollar arithmetic.**

## Why not just let the agent read the bill and summarize it?

Because that is exactly how you ship a confidently wrong cost report.

Hand a model a few thousand rows of `system.billing.usage` and ask it for the top cost leaks, and it will give you a fluent answer. It will add DBUs. It will multiply by a price it half-remembers. It will round. Every one of those steps is a place the model can be plausibly, invisibly wrong — and the output reads identically whether the math is right or hallucinated. The failure mode of an LLM doing FinOps is not a crash. It is a clean, well-formatted, wrong number.

The fix is architectural, not prompt-engineering. The model is allowed to decide *what to look for* and *how to explain it*. It is never allowed to be the calculator.

## The dollar primitive: confirmed, never estimated

Every confirmed figure comes from the customer's own billing tables — `system.billing.usage` joined to `system.billing.list_prices`. Not a model estimate. Not a public price list. The number Databricks actually billed.

That join is defined once, as a `priced` CTE, and reused by every category query. Usage is multiplied by `list_prices.pricing.default`, matched on both `sku_name` and `usage_unit`, inside the price-effective window, filtered to `currency_code = 'USD'`. Define the dollar primitive once; every downstream query inherits it. There is exactly one place where a DBU becomes a dollar, and it is a SQL join against the source of truth.

Before any of that runs, Step 1 is a fail-fast grant check. `system.billing.usage` sits behind a metastore-admin grant chain, so the skill probes it first:

```sql
SELECT 1 FROM system.billing.usage LIMIT 1;
```

If that errors, the skill reports the exact missing `GRANT USE CATALOG / USE SCHEMA / SELECT` chain verbatim and stops — rather than limping forward and failing mid-analysis with a half-built report. It also requires `DATABRICKS_WAREHOUSE_ID`, a running SQL warehouse to execute against. Fail at the door, with the precise remediation, or not at all.

## Two data planes: dollars and evidence

The skill reads from two MCPs, and the split is the whole architecture.

**Dollars** come from the Databricks CLI Statement Execution API — `databricks api post /api/2.0/sql/statements` — reading the `system.*` tables. Auth is the CLI's own `DATABRICKS_HOST` + `DATABRICKS_TOKEN` (or `databricks auth login`), and Unity Catalog enforces the metastore-admin grant chain on every read. This plane answers *how much*.

**Evidence** — the live config that explains *why* a leak exists — comes from a custom `databricks-workspace-mcp` control-plane server. It reads the live REST API for the auto-termination setting, the node type, the autoscale floor, the pool's `min_idle`. It has its own PAT / U2M / M2M auth and needs no system-table grants, because it never touches billing data.

The line that captures the division of labor: **the SQL produces the number; the workspace MCP turns it into a verified, single-config-change fix.** "$8,400/month on a cluster that never auto-terminates" is the SQL's job. "Set `autotermination_minutes = 15`" is the MCP's. And the degradation path matters: if the workspace MCP is absent, the skill still produces every dollar figure and falls back to accepting pasted config — it never fails silently mid-flow because one plane is missing.

## Four leak categories, each labeled with what it actually is

The leaks are not a flat list. Each category carries an explicit confidence *kind*, and that label travels with the dollars all the way to the report.

**1. Clusters that never auto-terminate — `confirmed`.** Join priced ALL_PURPOSE usage to `system.compute.clusters`, flag `auto_termination_minutes = 0`, rank by 30-day idle spend. This is money actually billed for compute that sat idle:

```sql
SELECT p.usage_metadata.cluster_id AS cluster_id,
       COALESCE(c.cluster_name, 'unknown') AS cluster_name,
       c.auto_termination_minutes,
       ROUND(SUM(p.usd), 2) AS spend_30d_usd
FROM priced p
JOIN cluster_cfg c ON p.usage_metadata.cluster_id = c.cluster_id
WHERE p.billing_origin_product = 'ALL_PURPOSE'
  AND c.auto_termination_minutes = 0
GROUP BY p.usage_metadata.cluster_id, c.cluster_name, c.auto_termination_minutes
HAVING SUM(p.usd) > 0
ORDER BY spend_30d_usd DESC;
```

**2. Scheduled jobs on All-Purpose compute — `confirmed`.** A usage row with a `job_id` and `billing_origin_product = 'ALL_PURPOSE'` (~$0.55/DBU) instead of `JOBS_COMPUTE` (~$0.15/DBU). Re-price the exact same DBUs at the Jobs rate; the delta is the savings. Deterministic re-pricing, not a model's guess at "roughly 3x cheaper."

**3. Overprovisioned clusters idling below floor — `estimated`.** Mean CPU from `system.compute.node_timeline`, flag clusters under 25% utilization, `est_overprovision = spend × (1 − CPU%)`. This is the one *arithmetically modeled* number in the skill — the at-risk Photon figure below is flagged for review, not model-computed — and it is labeled `est_*` everywhere it appears, so no one mistakes a model for a bill.

**4. Photon premium without the speedup — `at-risk`.** Photon is not a column. It is billing-visible via the SKU. Surface the ~2× premium portion as money to review against actual runtime gain — not confirmed waste:

```sql
SELECT p.usage_metadata.cluster_id AS cluster_id,
       ROUND(SUM(p.usd), 2)        AS photon_spend_30d_usd,
       ROUND(SUM(p.usd) / 2.0, 2)  AS photon_premium_at_risk_30d_usd
FROM priced p
WHERE p.sku_name ILIKE '%PHOTON%'
  AND p.billing_origin_product IN ('ALL_PURPOSE','JOBS_COMPUTE')
  AND p.usage_metadata.cluster_id IS NOT NULL
GROUP BY p.usage_metadata.cluster_id
HAVING SUM(p.usd) > 0
ORDER BY photon_premium_at_risk_30d_usd DESC;
```

Three kinds — confirmed, estimated, at-risk — and a report that never blurs them together:

| Confidence kind | What it means |
|---|---|
| **Confirmed** | Money actually billed, from `system.billing.usage` joined to `system.billing.list_prices` |
| **Estimated** | A modeled figure from utilization data (CPU %), labeled `est_*` so no one reads it as a bill |
| **At-risk** | Spend flagged for business review (the Photon premium) before it counts as recoverable waste |

## The ranker that the model cannot fudge

The pipeline is **detect → compute → rank → report**. The detect and report stages are the model's. The compute and rank stages live in `scripts/rank-and-report.py`, whose docstring opens with the thesis:

> The LLM does NOT do the dollar arithmetic.

The script ingests per-category JSON — each item `{category, root_cause, fix, waste_30d_usd, kind}` — converts 30-day spend to monthly, ranks descending, and renders the report. And it enforces the invariant the whole skill is built on: **never sum confirmed and unconfirmed dollars under one verb.**

```python
UNCONFIRMED = ("estimated", "at-risk")

# Split sum — confirmed and unconfirmed dollars are NEVER added under one verb.
confirmed_monthly   = sum(c["monthly"] for c in ranked if c.get("kind") == "confirmed")
unconfirmed_monthly = sum(c["monthly"] for c in ranked if c.get("kind") in UNCONFIRMED)
```

That split is why the headline reads honestly. For a $100K/month workspace it renders something like: *"burning **~$19,000/month** (confirmed), plus up to **~$8,000/month** pending review"* — with a trailing-30-day window stamp, and a ranked table whose `Confidence` column is load-bearing:

| # | Where it's leaking | $/month | Confidence | The fix |
|---|---|---|---|---|

Root-cause cells use plain business language. No raw `DBU` in any CFO-visible text — that translation happens before the number reaches finance, not in the reader's head.

## Why not let the model add the numbers?

Because a model that can add can also mis-add, and you cannot tell which run you got. Deterministic arithmetic outside the LLM is not a performance optimization. It is the difference between a report and a guess. The model's strengths — pattern-matching, explanation, ranking by business relevance — are real and used here. Its weakness — silent numerical confabulation — is engineered out by never giving it a calculator in the first place.

This is the same instinct that runs through the rest of the skill-marketplace work: deterministic math outside the model, every figure labeled with its confidence, and the model confined to the parts of the job where being articulate is an asset rather than a liability.

## The adversarial review that caught the LLM inventing a schema

The skill was built through a 10-agent workflow: research → author → **four adversarial review lenses** → revise. That review stage is not polish. It is load-bearing — and here is why.

The review caught a **hallucinated `system.compute.clusters.runtime_engine` column.** The model had confidently written its first Photon-detection query against a column that does not exist. Left unreviewed, the skill would have shipped a cost report built on a fictional schema — and it would have looked completely plausible doing it. The fix is the Photon query above: detect via `sku_name ILIKE '%PHOTON%'` on the priced billing row, because Photon is billing-visible by SKU and never a system-table column.

That is the entire argument for adversarial review of LLM-authored systems in one bug. The failure mode is not a stack trace. It is *confident plausibility* — output that looks right, reads right, and is wrong.

Two more from the same pass:

- A **non-deterministic jobs-rate join fan-out.** The jobs-rate CTE could match multiple price rows per usage unit, multiplying rows and inflating savings — the kind of un-deduped join a model reaches for because the simpler version reads correctly to anyone skimming it. Fix: dedupe to one USD rate per `usage_unit` so the join can't fan out.
- CFO-clarity gaps in the narrative cells.

Then a follow-up Gemini code review caught three more. Two worth naming:

- **CRITICAL:** `spend-baseline.sql.json` had `${DATABRICKS_WAREHOUSE_ID}` inside a `--json @file` template. The Databricks CLI does *not* expand env vars inside a JSON file, so the call would fail with an invalid warehouse id. Fix: jq-inject the id at call time — `jq --arg wh "$DATABRICKS_WAREHOUSE_ID" '. + {warehouse_id: $wh}' template.json`.
- **HIGH:** the renderer, at one point, summed confirmed and estimated/at-risk dollars under a single total with no Confidence column — violating the exact invariant the skill exists to enforce. The model regressed against its own design rule. Review caught it.

That last one is the lesson stated cleanly: even a system explicitly designed around "never sum confirmed with modeled" will, under LLM authorship, drift back toward doing it — because summing everything into one big number is the locally fluent move. Adversarial review is the gate that catches the regression. A hallucinated column and a silently-fanned-out join both produce output that looks right; only a hostile second read finds them.

## The same instinct, elsewhere

Precision over blunt tooling ran through the rest of that day's work too. A dependency-vuln triage in a Node mail service refused a blind `npm audit fix --force` — which would have major-bumped googleapis and typescript-eslint — and instead cleared 17 of 22 advisories via npm `overrides` and targeted direct bumps, documenting the 5 accepted residual install-time-only vulns in `tests/TESTING.md`. The destructive automatic fix is rarely the right one, in dependency graphs or in cost reports. A version-controlled document-store initiative got consolidated into a single synthesis hub, and partner FinOps research moved a step forward.

## The transferable rule

If you want a number a decision-maker will act on, the model is not allowed to compute it. Join the source-of-truth tables for confirmed figures. Label every output with its confidence kind and never blur the kinds together. Run the arithmetic in deterministic code the model cannot reach. And put the whole thing through adversarial review before it ships — because the LLM's most dangerous output is the one that looks exactly right.

## Related Posts

- [Govern at the Merge: The Untrusted Union](/posts/govern-at-merge-untrusted-union/) — where governance belongs in a pipeline, and why the merge point is the gate. Same argument as the grant check and the confidence split: enforce at the boundary, not after.
- [The Bot Loop Circuit Breaker for Multi-Agent Slack](/posts/bot-loop-circuit-breaker-multi-agent-slack/) — multi-agent review and the failure modes that only show up when agents check each other's work, the way the four review lenses caught the hallucinated column.
- [The API Is the Real Boundary](/posts/the-api-is-the-real-boundary/) — the two-MCP split is exactly this: dollars on one data plane, config evidence on another, each with its own auth and its own job.

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "The LLM Should Never Do the Math",
  "description": "A Claude Code skill that hunts Databricks cost leaks and reports confirmed dollars from the customer's own billing tables — never LLM estimates.",
  "datePublished": "2026-06-26T08:00:00-05:00",
  "dateModified": "2026-06-26T08:00:00-05:00",
  "author": {
    "@type": "Person",
    "name": "Jeremy Longshore"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Start AI Tools"
  },
  "url": "https://startaitools.com/posts/llm-never-does-the-math/",
  "keywords": "LLM cost report, Databricks cost leaks, deterministic math, confirmed dollars, FinOps, Claude Code skill, AI agent reliability, adversarial review, hallucination"
}
</script>
