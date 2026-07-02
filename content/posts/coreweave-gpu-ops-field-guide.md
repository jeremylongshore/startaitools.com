+++
title = 'Surviving CoreWeave: the GPU failures that burn your hours'
slug = 'coreweave-gpu-ops-field-guide'
date = 2026-07-02T08:00:00-05:00
draft = false
tags = ["devops", "debugging", "architecture"]
categories = ["DevOps"]
description = "A practitioner field guide to CoreWeave's real GPU failure modes: Xid triage, silent RDMA fallback, MPIJob launch, LOTA storage, and building your own cost view."
toc = true
tldr = "CoreWeave gives you fast GPUs and sharp edges. This guide covers the five things that actually cost you time: reading the Xid before you touch a node, catching RDMA that silently fell back to TCP, launching multi-node jobs with MPIJob instead of PyTorchJob, hitting the right storage endpoint, and building a cost view that doesn't exist out of the box."
+++

Your 64-GPU job just threw **Xid 94**. Reschedule, or is the node dead?

It comes down to one bit, and most people get it wrong. They see "memory error," panic, drain the whole node, and lose an hour babysitting a machine that was fine. Or they do the opposite — retry blindly onto a GPU that's quietly returning corrupt gradients.

CoreWeave gives you world-class hardware with very sharp edges. The failure modes aren't exotic. They're just undocumented in the place you're looking when a run dies at 2 a.m. Here are the five that burn the most hours, and how to read them fast.

## Node forensics: read the Xid before you touch anything

When a GPU misbehaves, the driver logs an **Xid** to `dmesg`. The Xid number is the whole story. Learn three of them and you'll triage 90% of node incidents without a support ticket.

- **Xid 79 — "GPU has fallen off the bus."** The driver can't reach the GPU over PCIe anymore. The NVIDIA catalog's recommended action is `RESTART_BM` — restart the bare metal. The card is gone until the node reboots. Don't fight it; the node needs a power cycle.
- **Xid 94 — "Contained memory error."** A memory error the hardware isolated to *one* application. Action: `RESTART_APP`. Every other process on that GPU keeps running. You restart your job and move on. The node is not dead.
- **Xid 95 — "Uncontained memory error."** The error escaped the faulting process. Other work on that GPU may have read corrupt data. Action: `RESET_GPU`. Now the GPU is suspect and everything that touched it is suspect with it.

That's the bit everyone gets wrong. **94 is contained — reschedule. 95 is uncontained — the GPU is out.** Same three words in the log ("GPU memory error"), opposite responses.

The other pair worth memorizing is **Xid 63 / 64** — row remapper events. Ampere and newer GPUs quietly retire bad memory rows. When you suspect a flaky card, read the remap state directly:

```bash
nvidia-smi -q -d ROW_REMAPPER
```

Two fields decide the verdict. **`Pending: Yes`** means a remap is scheduled but won't take effect until the GPU is reset — the repair is durably recorded, just not live. **`Remapping Failure Occurred: Yes`** is the one that ends the conversation: the remap couldn't be written (that's the Xid 64 case), and the card needs to come out of service. Pending is routine. Failure is terminal.

One CoreWeave-specific rule sits on top of all this: **never manually uncordon a health cordon.** CoreWeave's Node Life Cycle controller cordons nodes automatically on GPU hardware errors and reboots them. Those node conditions are internal machinery, not a knob for your automation. If you `kubectl uncordon` a node CoreWeave cordoned for a hardware fault, you're scheduling work back onto a known-bad card. Let the controller clear it.

## The fabric lies quietly: RDMA that fell back to TCP

This one doesn't crash. It just makes your training 5x slower and says nothing.

GPUDirect RDMA over InfiniBand is what makes multi-node training fast. When it silently falls back to TCP sockets, your `all_reduce` still completes — over Ethernet, at a fraction of the bandwidth. No error. No log line screaming at you. Just a job that's mysteriously behind schedule.

Three things have to be true, and all three fail quietly if you miss one.

**Request the InfiniBand resource in both requests and limits.** It's a boolean scheduling flag, not a count:

```yaml
resources:
  requests:
    rdma/ib: 1
    nvidia.com/gpu: 8
  limits:
    rdma/ib: 1
    nvidia.com/gpu: 8
```

Miss it in either block and your pod schedules onto a node without IB, and NCCL shrugs and uses TCP.

**Point NCCL at the right interfaces.** On CoreWeave that's:

```bash
export NCCL_IB_HCA=ibp
export NCCL_SOCKET_IFNAME=eth0
```

**Then confirm it actually took.** Turn on debug output and read one line:

```bash
export NCCL_DEBUG=INFO
```

Look for `NET/IB`. That's InfiniBand — good. If you see `NET/Socket`, you're on TCP and every second of that run is wasted. CoreWeave's own docs put it plainly: if a multi-node job runs but throughput is far below expectations, NCCL has usually fallen back from InfiniBand to TCP.

Prove the fabric before you trust it. Run `all_reduce_perf` from CoreWeave's `nccl-tests` and check the reported bus bandwidth. On a 64-GPU H100 run over InfiniBand you should see hundreds of GB/s — the exact number moves with your NCCL version, so baseline against CoreWeave's published manifests, not a screenshot from someone's blog. If your busbw is an order of magnitude low, you already know why: go back and read the `NET/` line.

## Launch: MPIJob, not PyTorchJob

The obvious path — Kubeflow's `PyTorchJob` — is not the path CoreWeave paves. Their reference manifests for multi-node NCCL runs use the **MPI Operator (`MPIJob`)**, with SUNK/Slurm as the other supported route. Follow the paved road; the sharp edges are already sanded off it.

Two traps live here.

**`slotsPerWorker` must equal the GPUs per pod.** The MPI Operator launches one rank per slot. Set eight GPUs per worker and four slots, and `mpirun` spins up the wrong number of ranks — half your GPUs sit idle while the job reports "running."

**Don't reach for the SUNK pod scheduler to gang-schedule a distributed job.** Its own docs are blunt: *"No gang scheduling. The scheduler schedules each Pod as a separate Slurm job. Multi-node PodGroups aren't supported."* It's built for single-node work like inference. Point it at a multi-pod training job and you get piecemeal scheduling — some ranks start, the rest stay `Pending`, and the ranks that started block forever at NCCL rendezvous waiting for peers that were never scheduled. Your job hangs at init with no error. Use `MPIJob` or a real Slurm allocation, which grab the whole gang at once.

## Storage: the endpoint decides your throughput

CoreWeave AI Object Storage is S3-compatible, so your existing code "just works." That's the trap — it works at the wrong speed if you use the wrong hostname.

**Inside the cluster, hit `http://cwlota.com`.** That's LOTA, the Local Object Transport Accelerator — a proxy that caches objects on the GPU nodes' local NVMe. The public `https://cwobject.com` endpoint works too, and it'll route you around the accelerator you're paying for. In-cluster: `cwlota.com`. Full stop.

LOTA has rules. **It only caches objects larger than 4 MB** — anything smaller bypasses the cache entirely. So the classic "millions of tiny files" dataset gets zero benefit. Consolidate small samples into larger archives (WebDataset, TAR, TFRecord) so your objects clear the 4 MB bar, and use a **minimum 50 MB multipart part size** to cut request overhead.

The payoff is real once the cache warms. CoreWeave's own benchmark on 160 H200 GPUs measured about **24 GiB/s aggregate cold** (first minute, cache empty) climbing to **368 GiB/s warm** — roughly 2.3 GiB/s per GPU. Cold reads are network-bound; warm reads come off local NVMe. Structure your data loader to warm the cache early.

For weights, **Tensorizer** loads faster than the standard path — CoreWeave clocked GPT-J-6B at ~8.2 s median versus ~15 s for HuggingFace on A40s, by streaming tensors at wire speed instead of deserializing a checkpoint blob.

For resilience, use **PyTorch Distributed Checkpoint**. `torch.distributed.checkpoint.async_save` writes checkpoints on a background thread so training barely stalls, and DCP's load-time **resharding** lets you save on one topology and resume on another. That last part matters here: when CoreWeave cordons a node mid-run and you come back on a different world size, a DCP checkpoint loads anyway. A rigidly-sharded one doesn't.

## Cost: there is no dashboard — you build it

Here's the one that surprises every finance-conscious team: **CoreWeave ships no cost dashboard and no billing API.** You want to know what you're spending? You build it yourself, in PromQL, against their managed Grafana.

The usage metrics are there. The one you start with is `billing:instance:total` — running instances by cluster — alongside `billing:object_storage_used_bytes:total` and friends. Multiply usage by your rate card inside the query to synthesize a cost estimate; there's no single "dollars" metric to read. You'll need to be in the `admin`, `metrics`, or `write` group to see them.

Two levers keep the number down.

**Reserve carefully.** Reserved capacity runs 25–60% off on-demand, with the deepest cuts on multi-year H100/H200 commitments. But reserved means *paid whether or not you use it* — an idle reservation is worse than on-demand. Reserve only your steady-state floor; burst the rest.

**Right-size the GPU to the model.** An H100 is wasted on small-model inference. Third-party 2026 benchmarks consistently put the L40S ahead of the H100 on cost-per-token for models in the ~7B–30B range — reach for the H100 only when you genuinely need ultra-low latency. (Treat the exact dollar figures as directional; they swing hard by benchmark and by month.) And remember the hardware line: **FP8 lives on Hopper and Ada, not Ampere** — if your inference plan is FP8, an A100 can't run it, so match the silicon to the numeric format before you commit.

## The short version

- **Read the Xid first.** 79 → node reboot. 94 → contained, restart your app. 95 → uncontained, the GPU is out. `nvidia-smi -q -d ROW_REMAPPER`: Pending is fine, Remapping Failure is terminal. Never uncordon a health cordon.
- **Confirm `NET/IB`, not `NET/Socket`.** RDMA fails silent and slow. `rdma/ib: 1` in requests *and* limits.
- **Launch with `MPIJob`.** `slotsPerWorker` = GPUs per pod. The SUNK pod scheduler won't gang-schedule — your job will hang at rendezvous.
- **Use `cwlota.com` in-cluster.** Keep objects above 4 MB, parts above 50 MB. `async_save` + DCP resharding survives node loss.
- **Build your cost view in PromQL.** No dashboard exists. Reserve only your floor; put small-model inference on cheaper silicon.

None of this is in one place, which is exactly why it costs people days. Now it's in one place.

---

*Jeremy Longshore builds Claude Code skills for infrastructure platforms at Intent Solutions — the CoreWeave GPU-ops pack lives in [claude-code-plugins](https://github.com/jeremylongshore/claude-code-plugins-plus-skills). Community-contributed. Not affiliated with, endorsed by, or sponsored by CoreWeave, Inc.*
