# Bob's Brain evolution — research timeline (evidence-backed)

Sources: repo READMEs, git history, ADRs. Do not invent dates not listed here.

| When | Artifact | Repo / path | Thesis of that era |
|------|----------|-------------|--------------------|
| **2025-08-09** | Earliest Bob lineage commit | `iams/bobs-brain`, `99-archived/bobs-brain-ref` | "Bob Unified Agent v2 — Professional Business Partner" |
| **2025-09** | Restructure + "Bob's Brain" identity | same | Specialist team under global orchestrator Bob; iam-* ADK/Vertex compliance dept |
| **~2025–2026** | **Bob's Brain v1 (ADK era)** | `jeremylongshore/iam-bobs-brain` / local `iams/bobs-brain` | Google ADK + Vertex Agent Engine; Hard Mode R1–R8; Slack; Mission Spec; Foreman + 8 specialists; risk tiers; evidence bundles. **Frozen 2026-06-28** as honest ADK-era artifact |
| **Archive docs** | Spec snapshot | `contributing-clanker/99-archived-system-docs/006-AT-SPEC-bobs-brain-overview.md` | Enterprise multi-agent orchestrator narrative (v2.0.0 labeling in doc; points at iams path) |
| **2026-06-01** | **Bob's Big Brain** umbrella landing | `governed-second-brain` | "Compile, then govern"; receipts > raw recall; competitive teardown |
| **2026-06-16** | **Bob's Big Brain plugin** v0 | `governed-second-brain-plugin` → branded **bobs-big-brain-plugin** | Local-first Claude Code plugin: `brain_search` / `brain_capture` / hash-chained audit; ICO + INTKB + qmd stack |
| **2026-06-28** | **bobs-brain-v2** greenfield | `iams/bobs-brain-v2` / GH `bobs-brain-v2` | BYOK any provider; Pydantic AI + LiteLLM; zero-Google-by-default; consumes IEP attestation kernel; thin agent + tools (not 8-specialist department) |
| **2026-07-11** | Intendants scaffold (pre-rename) | `bob-the-intendant` | Governed background agents composing AGP |
| **2026-07-12** | **Bob the Intendant** extraction | ADR `agp/059`, rename from intendants | Watcher/composition leaves AGP; leaf → kernel only; "kernel must not import its agents"; Public-Flip Gate (`109-AT-DECR`) |
| **2026-07-13** | Public product front + judge | `bob-the-intendant` v0.0.4 | Governed watcher + `bob judge` Layer-1 judgment; builds in public |

## Lineage shape (not one linear product)

Three **related but distinct** product lines under the "Bob" brand:

1. **Orchestrator Bob (v1 → v2)** — multi-agent / Slack agent that *does work* (ADK department → BYOK governed agent)
2. **Big Brain** — *memory* stack + plugin (compile → govern → cited recall + receipts)
3. **Bob the Intendant** — *background governed agent* leaf on AGP kernel (trigger → policy → HITL → signed journal)

The article must not collapse these into one repo history without saying so.

## Related posts already on startaitools

- `the-kernel-must-not-import-its-agents` (2026-07-12) — Intendant extraction doctrine
- Other posts mention Bob only in passing (portfolio, ADK community, etc.)

## Gaps / confirm with Jeremy

- Exact public GH names vs local path names (`iam-bobs-brain` vs `bobs-brain`)
- Whether "Bob's Brain plugin" = only Big Brain plugin or also older artifacts
- How much of v2 is shipped vs scaffolded (README still program-shaped)
- Whether n8n / early Slack "send_to_bob" era belongs in the arc
