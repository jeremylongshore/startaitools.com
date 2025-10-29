---
title: "Foundation"
date: 2025-10-28
weight: 2
bookToc: true
bookCollapseSection: false
---

# Foundation Documents

Core architecture decisions that shape the IAEMS platform. These 15 documents establish:
- Agent Marketplace architecture
- A2A (Agent-to-Agent) Framework
- IAE (Intelligence Agent Engine) Platform

---

## Agent Marketplace (4 docs)

Containerized AI agent marketplace with Docker-based isolation and n8n orchestration.

- **[001]** [Agent Offerings Implementation Plan](agent-marketplace/001-implementation-plan/)
- **[002]** [Market Research & Competitive Analysis](agent-marketplace/002-research-analysis/)
- **[003]** [Container-Based Agent Architecture](agent-marketplace/003-container-architecture/)
- **[004]** [Final Implementation Decision](agent-marketplace/004-architecture-decision/)

**Key Decisions:**
- Docker containers for agent isolation
- n8n for workflow orchestration
- Scalable microservices architecture

---

## A2A Framework (6 docs)

Agent-to-Agent communication using native Vertex AI Agent Engine capabilities.

- **[005]** [A2A Framework Executive Summary](a2a-framework/005-executive-summary/)
- **[006]** [A2A Technical Architecture](a2a-framework/006-technical-architecture/)
- **[007]** [Intelligence Layer Specification](a2a-framework/007-intelligence-layer/)
- **[008]** [ICP Scoring Algorithm](a2a-framework/008-icp-scoring/)
- **[009]** [A2A Implementation Roadmap](a2a-framework/009-implementation-roadmap/)
- **[010]** [A2A Documentation Index](a2a-framework/010-documentation-index/)

**Key Decisions:**
- Native Vertex AI A2A support (no custom protocol)
- Event-driven agent communication
- State management and coordination

---

## IAE Platform (2 docs)

Intelligence Agent Engine - the core platform powering agent operations.

- **[011]** [IAE Demo Strategy](iae-platform/011-demo-strategy/)
- **[012]** [IAE Product Plan](iae-platform/012-product-plan/)

**Key Decisions:**
- Vertex AI as primary infrastructure
- Demo-first approach for validation
- Product roadmap aligned with capabilities

---

## Reading Order

**For newcomers:**
1. Start with [004] Final Implementation Decision
2. Read [006] A2A Technical Architecture
3. Review [001] Agent Offerings Implementation

**For implementers:**
1. Follow [009] A2A Implementation Roadmap
2. Reference [007] Intelligence Layer Specification
3. Use [010] Documentation Index for navigation

---

**Documents:** 15 total (4 marketplace + 6 A2A + 2 IAE + 3 other)
**Status:** Complete architectural foundation
**Next:** System-level documentation (13 docs)