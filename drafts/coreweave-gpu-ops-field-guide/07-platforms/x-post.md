Your 64-GPU job on CoreWeave just threw Xid 94 — reschedule, or is the node dead? One bit decides, and most people get it wrong.

The Xid in dmesg is the whole story. Three to memorize:

Xid 79 — GPU fell off the bus. The card is gone until the node reboots.
Xid 94 — CONTAINED memory error. Isolated to one app. Restart your job, the node is fine.
Xid 95 — UNCONTAINED. The error escaped the process, so everything that GPU touched is suspect. The GPU is out.

94 vs 95 is the bit. Same words in the log, opposite responses.

Suspect a flaky card? Read the remap state directly with nvidia-smi -q -d ROW_REMAPPER. "Pending: Yes" is routine — it takes effect on the next reset. "Remapping Failure Occurred: Yes" is terminal, the card is done. And never manually uncordon a node CoreWeave health-cordoned. That is a known-bad GPU.

The failure that doesn't crash — it just makes you 5x slower and says nothing: GPUDirect RDMA silently falling back to TCP. Your all_reduce still completes, over Ethernet, at a fraction of the bandwidth. No error anywhere.

Three things have to be true. rdma/ib: 1 in BOTH requests and limits. NCCL_IB_HCA=ibp and NCCL_SOCKET_IFNAME=eth0. Then set NCCL_DEBUG=INFO and confirm NET/IB, not NET/Socket. See NET/Socket and every second of that run is wasted.

Two more that quietly burn hours:

Storage — CoreWeave object storage is S3-compatible, so the wrong code "just works" at the wrong speed. In-cluster you must hit cwlota.com — LOTA, the local accelerator — not cwobject.com. And LOTA only caches objects over 4MB, so millions of tiny files get zero benefit — pack them into bigger archives.

Cost — there is no cost dashboard and no billing API. You build your spend view yourself in PromQL against their Grafana: billing:instance:total times your rate card (you need the admin or metrics group). Then right-size: for 7B to 30B inference the L40S beats the H100 on cost-per-token (directional — figures move by benchmark and month). Save the H100s for when latency truly matters.

None of this is in one place, which is exactly why it costs people days.

Full field guide — Xid triage, RDMA, MPIJob, LOTA, and cost:
https://startaitools.com/posts/coreweave-gpu-ops-field-guide/

Community field notes — not affiliated with, endorsed by, or sponsored by CoreWeave, Inc.
