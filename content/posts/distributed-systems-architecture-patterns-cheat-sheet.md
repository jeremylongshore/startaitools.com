---
title: "Distributed Systems Architecture Patterns Cheat Sheet"
date: 2025-01-13T15:45:00-06:00
draft: false
tags: ["architecture", "distributed-systems", "scalability", "microservices", "system-design"]
categories: ["Architecture", "Engineering"]
author: "Jeremy Longshore"
description: "Comprehensive reference guide for distributed systems architecture patterns - when to use them and what problems they solve"
toc: true
---

A quick reference guide for distributed systems architecture patterns, covering when to use each pattern and the classic problems they solve.

## Distributed Systems Architecture Patterns Cheat Sheet

|Pattern                                           |Core Idea                                       |When to Use                                            |Classic Problems                                     |
|--------------------------------------------------|------------------------------------------------|-------------------------------------------------------|-----------------------------------------------------|
|Caching (cache-aside / write-through / write-back)|Keep hot data close to the app                  |Read-heavy workloads, expensive queries, slow upstreams|Speed up product pages, session stores, ranking feeds|
|CDN                                               |Push static/streamable assets to edge           |Global users, large media, static bundles              |Image/CSS delivery, video streaming, downloads       |
|Load Balancing (L4/L7)                            |Spread traffic across instances                 |Scale stateless services, HA                           |Web/API tier scaling, zero-downtime deploys          |
|Rate Limiting & Throttling                        |Control request volume per key/client           |Protect downstream services, fair usage                |Public APIs, login abuse protection                  |
|Circuit Breaker                                   |Fail fast when a dependency is unhealthy        |Prevent cascades, degrade gracefully                   |Payment gateway outage, flaky search backend         |
|Backpressure                                      |Signal producers to slow down                   |Spiky traffic, limited consumers                       |Upload pipelines, stream processing stability        |
|Retry + Idempotency                               |Safe replays of failed ops                      |Unreliable networks, async workflows                   |Order creation, webhook delivery                     |
|Read Replicas                                     |Offload reads from primary DB                   |Read-heavy, reporting, geo-reads                       |Analytics pages, timelines, leaderboards             |
|Sharding (Hash/Range/Geo)                         |Split data across nodes                         |Data > single node, parallelism                        |Multi-TB user tables, geo data stores                |
|Replication (Sync/Async)                          |Keep copies for HA & reads                      |Availability, DR, low-latency reads                    |Active-passive failover, follower reads              |
|CQRS                                              |Separate read/write models                      |Complex reads + high write throughput                  |Event feeds, denormalized dashboards                 |
|Event Sourcing                                    |State = log of events                           |Full audit, rebuild state, temporal queries            |Ledger systems, order state timelines                |
|Message Queue / Stream (SQS/Kafka)                |Async decoupling via durable logs               |Spikes, fan-out, ordered pipelines                     |Email/SMS, ETL, clickstream processing               |
|Saga (Orchestration/Choreography)                 |Distributed transaction via steps + compensation|Cross-service workflows without 2PC                    |Book-pay-reserve flows, refunds                      |
|Search Index (ES/OpenSearch)                      |Inverted index for fast text/filters            |Full-text, aggregations, relevance                     |Product search, logs explorer                        |
|Time-Series DB                                    |Append-heavy metrics optimized by time          |Monitoring, IoT, financial ticks                       |Prometheus/TSDB, sensor data                         |
|Write-Optimized Stores (LSM)                      |Fast writes, compaction later                   |High ingest, occasional reads                          |Audit/event logs, analytics ingest                   |
|Geo-Replication / Geo-Sharding                    |Place data near users                           |Low latency, data residency                            |Multi-region apps, GDPR residency                    |
|Consistency Models (Strong/Eventual)              |Pick latency vs guarantees                      |Cross-region apps, offline tolerance                   |Cart totals vs likes counters                        |
|API Gateway                                       |Central entry: auth, routing, limits            |Many services, uniform policies                        |Public API front door, mTLS termination              |
|Webhooks & Outboxes                               |Reliable external notifications                 |Integrations, third-party callbacks                    |Payment status updates, CRM sync                     |
|Blob/Object Storage                               |Cheap infinite files                            |Media, backups, exports                                |User uploads, data lakes                             |
|Workflow Orchestrator (Airflow/Temporal)          |Durable, reliable step with state               |Long-running jobs, SLAs                                |Report generation, video pipelines                   |
|Blue-Green / Canary Deploys                       |Shift traffic gradually                         |Safer releases, quick rollback                         |API rollout, config changes                          |
|Feature Flags                                     |Runtime on/off % rollouts                       |Experimentation, kill-switches                         |A/B tests, dark launches                             |
|Schema Migration Strategy                         |Backward-/forward-compatible changes            |Zero-downtime DB upgrades                              |Expand-migrate-contract patterns                     |
|Distributed Locks / Leader Election               |Coordinate one active worker                    |Cron uniqueness, shared ownership                      |Single consumer, partition leader                    |
|Observability (Logs/Metrics/Traces)               |See what the system is doing                    |SLOs, debugging, capacity planning                     |P99 latency, error budgets, trace trees              |
|Security: AuthN/AuthZ                             |Verify identity and permissions                 |Multi-tenant products, external APIs                   |OAuth2/OIDC, RBAC/ABAC                               |
|Multi-Tenancy (Pool/Bridge/Isolated)              |Resource & data isolation levels                |SaaS with many customers                               |Per-tenant DBs vs shared schema                      |
|Edge Compute / Functions                          |Run logic near the user                         |Latency-sensitive, light workloads                     |Personalization at edge, AB tests                    |
|Rate-Aware DB Patterns                            |Batch, queue, throttle at DB edge               |Hot partitions, lock contention                        |Bulk imports, ID sequence hot-spot                   |
|Pagination Strategies                             |Keyset + Offset for big data                    |Infinite scroll, large tables                          |Feed pagination, admin lists                         |

## How to Use This Cheat Sheet

1. **Problem First**: Start with your problem in the "Classic Problems" column
2. **Match Pattern**: Find patterns that address similar challenges
3. **Validate Fit**: Check if "When to Use" matches your context
4. **Combine Patterns**: Most systems use multiple patterns together

## Key Considerations

- **No Silver Bullets**: Each pattern has trade-offs
- **Start Simple**: Don't over-engineer; add patterns as you scale
- **Measure First**: Use metrics to justify architectural changes
- **Team Knowledge**: Consider your team's expertise with each pattern

## Related Resources

- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Designing Data-Intensive Applications](https://dataintensive.net/)
- [AWS Architecture Best Practices](https://aws.amazon.com/architecture/well-architected/)

---

*This cheat sheet is a living document. As distributed systems evolve, new patterns emerge and existing ones adapt. Use it as a starting point for deeper exploration.*