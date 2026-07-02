*Originally published at [startaitools.com](https://startaitools.com/posts/coreweave-gpu-ops-field-guide/).*

# Surviving CoreWeave: the GPU failures that burn your hours

If you've moved a training run onto CoreWeave, you already know the deal: the hardware is fast, the network is real InfiniBand, and the edges are sharp. This week I want to hand you the five failure modes that quietly cost people the most time — the ones that aren't in the doc you're staring at when a run dies at 2 a.m.

Let's start with the one that catches everyone.

Your 64-GPU job just threw **Xid 94**. Reschedule, or is the node dead? It comes down to one bit, and most people get it wrong. They see "memory error," panic, drain the whole node, and lose an hour on a machine that was fine. Or they retry blindly onto a GPU that's quietly returning corrupt gradients.

## Node forensics: read the Xid before you touch anything

When a GPU misbehaves, the driver logs an **Xid** to `dmesg`. The number is the whole story. Learn three and you'll triage most node incidents without a support ticket.

- **Xid 79 — "GPU has fallen off the bus."** The driver can't reach the card over PCIe. NVIDIA's catalog says `RESTART_BM` — restart the bare metal. It's gone until the node reboots.
- **Xid 94 — "Contained memory error."** Isolated to *one* application. Action: `RESTART_APP`. Everything else on that GPU keeps running. Restart your job and move on.
- **Xid 95 — "Uncontained memory error."** The error escaped the process. Other work on that GPU may have read corrupt data. Action: `RESET_GPU`. The card is suspect, and so is everything it touched.

That's the bit: **94 is contained — reschedule. 95 is uncontained — the GPU is out.** Same words in the log, opposite responses.

The other pair to know is **Xid 63 / 64**, the row remapper. When you suspect a flaky card, read the remap state directly:

```
nvidia-smi -q -d ROW_REMAPPER
```

`Pending: Yes` means a remap is scheduled and takes effect on the next reset — routine. `Remapping Failure Occurred: Yes` is the one that ends it: the remap couldn't be written, and the card needs to come out.

And one CoreWeave-specific rule: **never manually uncordon a health cordon.** CoreWeave's lifecycle controller cordons nodes automatically on hardware errors. Uncordon one and you're scheduling work back onto a known-bad GPU. Let the controller clear it.

## The fabric lies quietly: RDMA that fell back to TCP

This one doesn't crash. It just makes training 5x slower and says nothing.

GPUDirect RDMA over InfiniBand is what makes multi-node training fast. When it silently falls back to TCP, your `all_reduce` still completes — over Ethernet, at a fraction of the bandwidth. No error. Just a job mysteriously behind schedule.

Three things have to be true. Request the IB resource in **both** requests and limits (it's a boolean, not a count):

```
resources:
  requests: { rdma/ib: 1, nvidia.com/gpu: 8 }
  limits:   { rdma/ib: 1, nvidia.com/gpu: 8 }
```

Point NCCL at the right interfaces:

```
export NCCL_IB_HCA=ibp
export NCCL_SOCKET_IFNAME=eth0
```

Then confirm it took. `export NCCL_DEBUG=INFO` and read one line: `NET/IB` is InfiniBand (good); `NET/Socket` means you're on TCP and wasting every second of the run. CoreWeave's own docs say it: if a multi-node job runs but throughput is far below expectations, NCCL has usually fallen back to TCP. Baseline with `all_reduce_perf` from CoreWeave's `nccl-tests` before you trust the fabric.

## Launch: MPIJob, not PyTorchJob

The obvious path — Kubeflow's `PyTorchJob` — is not the one CoreWeave paves. Their reference manifests use the **MPI Operator (`MPIJob`)**, with SUNK/Slurm as the other route. Two traps:

- **`slotsPerWorker` must equal the GPUs per pod.** One rank per slot. Mismatch it and `mpirun` launches the wrong number of ranks while the job reports "running."
- **Don't use the SUNK pod scheduler to gang-schedule a distributed job.** Its docs are blunt: *"No gang scheduling... Multi-node PodGroups aren't supported."* It's for single-node work. On a multi-pod job you get piecemeal scheduling — some ranks start, the rest stay `Pending`, and the started ranks hang forever at NCCL rendezvous. Use `MPIJob` or a real Slurm allocation, which grab the whole gang at once.

## Storage: the endpoint decides your throughput

CoreWeave AI Object Storage is S3-compatible, so your code "just works" — at the wrong speed if you use the wrong hostname.

**Inside the cluster, hit `http://cwlota.com`.** That's LOTA, the accelerator that caches objects on the GPU nodes' local NVMe. The public `https://cwobject.com` routes you around it. LOTA **only caches objects larger than 4 MB**, so consolidate small samples into archives (WebDataset, TAR, TFRecord) and use **50 MB minimum multipart parts**.

The payoff is real once warm: CoreWeave's benchmark on 160 H200 GPUs went from ~**24 GiB/s cold** to **368 GiB/s warm** (~2.3 GiB/s per GPU). For weights, **Tensorizer** loaded GPT-J-6B in ~8.2 s vs ~15 s for HuggingFace on A40s. For resilience, `torch.distributed.checkpoint.async_save` writes on a background thread, and DCP's load-time **resharding** lets you save on one topology and resume on another — which is exactly what you need when CoreWeave cordons a node mid-run and you come back on a different world size.

## Cost: there is no dashboard — you build it

The surprise for every finance-conscious team: **CoreWeave ships no cost dashboard and no billing API.** You build your spend view in PromQL against their managed Grafana. Start with `billing:instance:total`, multiply by your rate card inside the query (there's no single "dollars" metric), and get into the `admin` or `metrics` group to see it.

Two levers: **reserve only your steady-state floor** — reserved capacity runs 25–60% off but you pay for it idle or not — and **right-size the GPU**. For ~7B–30B inference, third-party 2026 benchmarks put the L40S ahead of the H100 on cost-per-token (directional — the figures swing hard by benchmark and by month); save the H100s for genuinely latency-critical work. Match silicon to format too: FP8 lives on Hopper and Ada, not Ampere.

## The short version

- Read the Xid first. 79 → reboot. 94 → contained, restart app. 95 → uncontained, GPU out. Never uncordon a health cordon.
- Confirm `NET/IB`, not `NET/Socket`. `rdma/ib: 1` in requests *and* limits.
- Launch with `MPIJob`. `slotsPerWorker` = GPUs per pod. SUNK pod scheduler won't gang-schedule.
- Use `cwlota.com` in-cluster. Objects >4 MB, parts >50 MB. `async_save` + DCP resharding survives node loss.
- Build your cost view in PromQL. Reserve only your floor.

None of this is in one place, which is exactly why it costs days. If this saved you one, forward it to whoever's on call this week — and subscribe for the next field guide, where I'll take the same treatment to a different piece of ML infrastructure.

---

*Jeremy Longshore builds Claude Code skills for infrastructure platforms at Intent Solutions — the CoreWeave GPU-ops pack lives in [claude-code-plugins](https://github.com/jeremylongshore/claude-code-plugins-plus-skills). Community-contributed. Not affiliated with, endorsed by, or sponsored by CoreWeave, Inc.*

*Originally published at [startaitools.com](https://startaitools.com/posts/coreweave-gpu-ops-field-guide/).*
