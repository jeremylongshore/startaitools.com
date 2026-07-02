<!--
MEDIUM CANONICAL SETTINGS
When importing to Medium, set the canonical URL (Story settings > Advanced > "Import" or the canonical link field) to:
  https://startaitools.com/posts/coreweave-gpu-ops-field-guide/
This tells search engines startaitools.com is the original source.
-->

*Canonical: https://startaitools.com/posts/coreweave-gpu-ops-field-guide/*

# Surviving CoreWeave: the GPU failures that burn your hours

Your 64-GPU job just threw **Xid 94**. Reschedule, or is the node dead?

It comes down to one bit, and most people get it wrong. They see "memory error," panic, drain the whole node, and lose an hour babysitting a machine that was fine. Or they do the opposite — retry blindly onto a GPU that's quietly returning corrupt gradients.

CoreWeave gives you world-class hardware with very sharp edges. The failure modes aren't exotic — they're just undocumented in the place you're looking when a run dies at 2 a.m. Here are the five that burn the most hours, and how to read them fast.

## Node forensics: read the Xid before you touch anything

When a GPU misbehaves, the driver logs an **Xid** to the kernel ring buffer (`dmesg`). The Xid number is the whole story. Learn three of them and you'll triage most node incidents without a support ticket.

**Xid 79 — "GPU has fallen off the bus."** The driver can't reach the GPU over PCIe anymore. NVIDIA's catalog recommends `RESTART_BM` — restart the bare metal. The card is gone until the node reboots.

**Xid 94 — "Contained memory error."** A memory error the hardware isolated to *one* application. The action is `RESTART_APP`. Every other process on that GPU keeps running. You restart your job and move on. The node is not dead.

**Xid 95 — "Uncontained memory error."** The error escaped the faulting process. Other work on that GPU may have read corrupt data. The action is `RESET_GPU`. Now the GPU is suspect, and everything that touched it is suspect with it.

That's the bit everyone gets wrong. **94 is contained — reschedule. 95 is uncontained — the GPU is out.** Same three words in the log, opposite responses.

The other pair worth memorizing is **Xid 63 / 64** — row remapper events. Ampere and newer GPUs quietly retire bad memory rows. When you suspect a flaky card, read the remap state directly with `nvidia-smi -q -d ROW_REMAPPER`. Two fields decide it: `Pending: Yes` means a remap is scheduled but won't take effect until the GPU is reset (routine), while `Remapping Failure Occurred: Yes` means the remap couldn't be written — the card needs to come out of service.

One CoreWeave-specific rule sits on top of all this: **never manually uncordon a health cordon.** CoreWeave's Node Life Cycle controller cordons nodes automatically on GPU hardware errors and reboots them. Uncordon one by hand and you're scheduling work back onto a known-bad card. Let the controller clear it.

## The fabric lies quietly: RDMA that fell back to TCP

This one doesn't crash. It just makes your training 5x slower and says nothing.

GPUDirect RDMA over InfiniBand is what makes multi-node training fast. When it silently falls back to TCP sockets, your `all_reduce` still completes — over Ethernet, at a fraction of the bandwidth. No error. No log line screaming at you. Just a job that's mysteriously behind schedule.

Three things have to be true, and each fails quietly if you miss it:

1. **Request the InfiniBand resource in both `requests` and `limits`.** It's a boolean scheduling flag (`rdma/ib: 1`), not a count. Miss it in either block and your pod schedules onto a node without IB, and NCCL shrugs and uses TCP.
2. **Point NCCL at the right interfaces:** `NCCL_IB_HCA=ibp` and `NCCL_SOCKET_IFNAME=eth0`.
3. **Confirm it took.** Set `NCCL_DEBUG=INFO` and read one line. `NET/IB` is InfiniBand — good. `NET/Socket` means TCP, and every second of that run is wasted.

CoreWeave's own docs put it plainly: if a multi-node job runs but throughput is far below expectations, NCCL has usually fallen back from InfiniBand to TCP. Prove the fabric with `all_reduce_perf` from CoreWeave's `nccl-tests` and baseline the bus bandwidth against their published manifests — the exact number moves with your NCCL version.

## Launch: MPIJob, not PyTorchJob

The obvious path — Kubeflow's `PyTorchJob` — is not the path CoreWeave paves. Their reference manifests for multi-node NCCL runs use the **MPI Operator (`MPIJob`)**, with SUNK/Slurm as the other supported route. Two traps live here.

**`slotsPerWorker` must equal the GPUs per pod.** The MPI Operator launches one rank per slot. Set eight GPUs per worker and four slots, and `mpirun` spins up the wrong number of ranks — half your GPUs sit idle while the job reports "running."

**Don't reach for the SUNK pod scheduler to gang-schedule a distributed job.** Its own docs are blunt: *"No gang scheduling. The scheduler schedules each Pod as a separate Slurm job. Multi-node PodGroups aren't supported."* It's built for single-node work like inference. Point it at a multi-pod training job and you get piecemeal scheduling — some ranks start, the rest stay `Pending`, and the ranks that started block forever at NCCL rendezvous. Use `MPIJob` or a real Slurm allocation, which grab the whole gang at once.

## Storage: the endpoint decides your throughput

CoreWeave AI Object Storage is S3-compatible, so your existing code "just works." That's the trap — it works at the wrong speed if you use the wrong hostname.

**Inside the cluster, hit `http://cwlota.com`.** That's LOTA, the Local Object Transport Accelerator — a proxy that caches objects on the GPU nodes' local NVMe. The public `https://cwobject.com` endpoint works too, and it routes you around the accelerator you're paying for. In-cluster: `cwlota.com`. Full stop.

LOTA **only caches objects larger than 4 MB** — anything smaller bypasses the cache. So the classic "millions of tiny files" dataset gets zero benefit. Consolidate small samples into larger archives (WebDataset, TAR, TFRecord) so your objects clear the 4 MB bar, and use a **minimum 50 MB multipart part size**.

The payoff is real once the cache warms. CoreWeave's own benchmark on 160 H200 GPUs measured about **24 GiB/s aggregate cold** climbing to **368 GiB/s warm** — roughly 2.3 GiB/s per GPU. For weights, **Tensorizer** loaded GPT-J-6B in ~8.2 s median versus ~15 s for HuggingFace on A40s. For resilience, `torch.distributed.checkpoint.async_save` writes checkpoints on a background thread, and DCP's load-time **resharding** lets you save on one topology and resume on another — which is exactly what you need when a node gets cordoned mid-run and you come back on a different world size.

## Cost: there is no dashboard — you build it

Here's the one that surprises every finance-conscious team: **CoreWeave ships no cost dashboard and no billing API.** You want to know what you're spending? You build it yourself, in PromQL, against their managed Grafana.

The usage metrics are there. Start with `billing:instance:total` — running instances by cluster. Multiply usage by your rate card inside the query to synthesize a cost estimate; there's no single "dollars" metric to read. You'll need to be in the `admin`, `metrics`, or `write` group to see them.

Two levers keep the number down. **Reserve carefully** — reserved capacity runs 25–60% off on-demand, but you pay for it whether or not you use it, so reserve only your steady-state floor and burst the rest. And **right-size the GPU to the model** — third-party 2026 benchmarks consistently put the L40S ahead of the H100 on cost-per-token for ~7B–30B inference (directional — the figures swing hard by benchmark and by month); reach for the H100 only when you genuinely need ultra-low latency. Match the silicon to the numeric format too: FP8 lives on Hopper and Ada, not Ampere.

## The short version

- **Read the Xid first.** 79 → node reboot. 94 → contained, restart your app. 95 → uncontained, the GPU is out. Never uncordon a health cordon.
- **Confirm `NET/IB`, not `NET/Socket`.** `rdma/ib: 1` in requests *and* limits.
- **Launch with `MPIJob`.** `slotsPerWorker` = GPUs per pod. The SUNK pod scheduler won't gang-schedule.
- **Use `cwlota.com` in-cluster.** Objects above 4 MB, parts above 50 MB. `async_save` + DCP resharding survives node loss.
- **Build your cost view in PromQL.** No dashboard exists. Reserve only your floor.

None of this is in one place, which is exactly why it costs people days. Now it's in one place.

---

*Jeremy Longshore builds Claude Code skills for infrastructure platforms at Intent Solutions — the CoreWeave GPU-ops pack lives in [claude-code-plugins](https://github.com/jeremylongshore/claude-code-plugins-plus-skills). Community-contributed. Not affiliated with, endorsed by, or sponsored by CoreWeave, Inc.*

*Originally published at [startaitools.com](https://startaitools.com/posts/coreweave-gpu-ops-field-guide/).*
