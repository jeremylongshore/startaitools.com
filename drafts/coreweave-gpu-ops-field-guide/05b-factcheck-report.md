# Fact-Check + Consistency Report — CoreWeave GPU Ops Field Guide

Applied: blog-fact-checker discipline (verify every external claim against an authoritative
source) + blog-consistency-checker discipline (thesis drift, contradictions, tone).
All load-bearing URLs were fetched/verified via WebFetch or WebSearch on 2026-07-02.

## Fact-Check

### Claims assessed: 18 | HIGH: 11 | MEDIUM: 5 | LOW: 2
### Recommendation: PASS (0 HIGH-priority INACCURATE claims after reframes below)

### VERIFIED (source confirms claim)

| # | Claim | Source | Status |
|---|---|---|---|
| 1 | Xid 79 = "GPU has fallen off the bus", action RESTART_BM | docs.nvidia.com/deploy/xid-errors/analyzing-xid-catalog.html | VERIFIED |
| 2 | Xid 94 = "Contained memory error", action RESTART_APP, isolated to one app | same NVIDIA catalog | VERIFIED |
| 3 | Xid 95 = "Uncontained memory error", action RESET_GPU, affects multiple apps | same NVIDIA catalog | VERIFIED |
| 4 | Xid 63 = remap event, Xid 64 = remap failure (RESET_GPU) | same NVIDIA catalog | VERIFIED |
| 5 | nvidia-smi -q -d ROW_REMAPPER shows "Pending" + "Remapping Failure Occurred" | docs.nvidia.com/deploy/nvidia-smi + GPU Memory Error Mgmt row-remapping doc | VERIFIED |
| 6 | CoreWeave auto-cordons on GPU hardware errors; node conditions are internal-use; don't manually uncordon | docs.coreweave.com/products/cks/nodes/cordon | VERIFIED |
| 7 | rdma/ib: 1 required in BOTH requests and limits (boolean flag) | docs.coreweave.com/.../use-gpudirect-rdma | VERIFIED (exact YAML matched) |
| 8 | NCCL_IB_HCA=ibp, NCCL_SOCKET_IFNAME=eth0 | same CoreWeave RDMA doc | VERIFIED |
| 9 | Check NET/IB vs NET/Socket in NCCL_DEBUG=INFO; TCP fallback warning verbatim | same CoreWeave RDMA doc | VERIFIED (quote used) |
| 10 | CoreWeave reference path = MPIJob (MPI Operator) + SUNK/Slurm; manifests exist | github.com/coreweave/nccl-tests (mpi-operator/ + slurm/) | VERIFIED |
| 11 | SUNK pod scheduler: "No gang scheduling... Multi-node PodGroups aren't supported"; best for single-node/inference | docs.coreweave.com/docs/products/sunk/run_workloads/schedule-kubernetes-pods | VERIFIED (quote used) |
| 12 | In-cluster hit http://cwlota.com; outside https://cwobject.com | docs.coreweave.com/.../object-storage/lota/about | VERIFIED |
| 13 | LOTA only caches objects > 4 MB; smaller bypass cache | same LOTA doc + best-practices | VERIFIED |
| 14 | Consolidate small files (WebDataset/TAR/TFRecord); minimum 50 MB multipart parts | docs.coreweave.com/.../object-storage/concepts/best-practices | VERIFIED |
| 15 | LOTA benchmark ~24 GiB/s cold → 368 GiB/s warm, ~2.3 GiB/s/GPU | coreweave.com/blog benchmark-results-...-2-gb-s-per-gpu | VERIFIED (measured on 160 H200 GPUs — see reframe) |
| 16 | Tensorizer GPT-J-6B ~8.2 s vs HuggingFace ~15 s | coreweave.com/blog/coreweaves-tensorizer-... (8.22 vs 15.02 median, A40) | VERIFIED |
| 17 | torch.distributed.checkpoint.async_save exists; DCP supports load-time resharding across topologies | docs.pytorch.org DCP async recipe + DCP getting-started recipe | VERIFIED |
| 18 | Cost: no billing API/dashboard; build in PromQL; metric billing:instance:total; admin/metrics/write group needed | docs.coreweave.com/docs/observability/usage-monitoring | VERIFIED (exact metric name + group confirmed) |
| 19 | Reserved capacity 25–60% off, deepest on multi-year H100/H200, paid when idle | coreweave.com/pricing + Thunder Compute pricing guide (3rd-party) | VERIFIED (directional) |

### REFRAMED (claim adjusted to stay accurate — no false statements shipped)

- **H100 all_reduce_perf busbw "~356–373 GB/s" (from the task brief):** NOT verifiable. CoreWeave's
  current nccl-tests README shows GB200 numbers (e.g. 745 GB/s single rack), not a labelled H100
  64-GPU figure. **Reframe shipped:** "you should see hundreds of GB/s — the exact number moves with
  your NCCL version, so baseline against CoreWeave's published manifests." No specific unverified
  number is asserted. [flagged]
- **L40S ~$0.31/M-tok vs H100 ~$0.67/M-tok (from the task brief):** NOT verifiable — third-party
  sources disagree by an order of magnitude ($0.023 vs $0.026; $0.15–0.25; others). **Reframe
  shipped:** directional only — "L40S ahead of H100 on cost-per-token for ~7B–30B inference; treat
  exact dollar figures as directional, they swing by benchmark and month," cited to Spheron
  (spheron.network/blog/l40s-vs-h100) and flagged third-party/2026. [flagged]
- **LOTA benchmark hardware:** the 24→368 GiB/s numbers were measured on **160 H200 GPUs** (20 nodes ×
  8 H200), not H100. Article states "160 H200 GPUs" explicitly — corrected from any H100 implication.

### CORRECTED vs the task brief (would have been INACCURATE if shipped as-worded)

- Brief said "**shard** small files"; CoreWeave best-practices actually says the opposite —
  **consolidate** small files into larger archives (WebDataset/TAR/TFRecord) so objects clear the
  4 MB LOTA threshold. Article ships the correct guidance.

### PRACTITIONER-KNOWLEDGE (true, but not a direct CoreWeave quote — framed as general behavior)

- **slotsPerWorker = GPUs per pod:** standard MPI Operator behavior (one rank per slot). Not lifted
  from a CoreWeave sentence; framed as MPI Operator convention. LOW risk — this is how the operator works.
- **"5x slower" on TCP fallback:** order-of-magnitude illustration of IB-vs-TCP, not a measured CoreWeave
  figure. Framed as directional ("a fraction of the bandwidth"), which the CoreWeave doc supports.
- **FP8 on Hopper/Ada not Ampere:** general NVIDIA hardware fact (FP8 tensor cores introduced with
  Hopper/Ada; Ampere A100 has none). Accurate.

## Consistency Audit

**Identified thesis:** "CoreWeave gives you fast GPUs with sharp edges — here are the five failure
modes that burn hours and how to read each one fast." **Thesis holds: YES** — intro promises "five that
burn the most hours," the five sections deliver in order, and the "short version" recaps all five.
Closing line ("none of this is in one place... now it's in one place") lands the intro's promise.

- **Contradiction scan:** none. The 94-contained / 95-uncontained distinction is stated identically in
  Section 1 and the recap. No claim reversed later.
- **Tone:** consistent practitioner/direct voice throughout (second person + imperative). No academic
  drift, no unexplained hedging. Matches startaitools writing-guide.
- **Editorial-rule compliance (AIMED content, not a work journal):** PASS. No first-person "here's what
  I built." Skills/Intent Solutions confined to a single byline line at the bottom. No CoreWeave
  trademark/legal-email mention anywhere.
- **Anti-slop scan:** PASS — grep for the writing-guide forbidden list ("comprehensive", "deep dive",
  "let's dive in", "it's worth noting", "diving deep", etc.) returns clean. No mermaid diagrams.
- **Code-narrative alignment:** every code block is set up before and explained after; the YAML, env
  vars, and nvidia-smi command each match their surrounding claim.

**Consistency recommendation: PASS** (0 high-severity issues).

## Net verdict: PASS — safe to review/publish. Two figures reframed to directional (busbw, $/token),
one brief instruction corrected (consolidate not shard), LOTA benchmark hardware stated as H200.
