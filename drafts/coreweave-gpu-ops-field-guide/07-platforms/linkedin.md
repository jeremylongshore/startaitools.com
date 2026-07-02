CoreWeave gives you world-class GPUs and no cost dashboard. Here's how to see what you're actually spending.

Most teams don't find out until the invoice lands: CoreWeave ships no cost dashboard and no billing API. If you want to know your spend before month-end, you build the view yourself.

The usage metrics are there — you just query them in PromQL against CoreWeave's managed Grafana. Start with:

  billing:instance:total

That's running instances by cluster. Multiply it by your rate card inside the query to synthesize a cost estimate — there's no single "dollars" metric to read, so you construct it. (You'll need to be in the admin or metrics group to see it.)

Once you can see the number, two levers move it:

1. Reserve only your steady-state floor. Reserved capacity runs 25–60% off on-demand — but you pay for it whether or not you use it. An idle reservation is worse than on-demand. Reserve the baseline, burst the rest.

2. Right-size the GPU to the model. An H100 is wasted on small-model inference. Third-party 2026 benchmarks consistently put the L40S ahead of the H100 on cost-per-token for models in the ~7B–30B range (directional — the exact figures move by benchmark and by month). Save the H100s for workloads that genuinely need ultra-low latency. And match silicon to numeric format first — FP8 lives on Hopper and Ada, not Ampere, so an A100 can't run an FP8 plan at all.

The cost angle is just one of five failure modes that quietly burn hours on CoreWeave — the others being Xid triage, silent RDMA-to-TCP fallback, multi-node launch, and storage endpoints. I wrote the full practitioner field guide here:

https://startaitools.com/posts/coreweave-gpu-ops-field-guide/

Community field notes — not affiliated with, endorsed by, or sponsored by CoreWeave, Inc.

#GPU #MLInfrastructure #DevOps #CoreWeave #MLOps
