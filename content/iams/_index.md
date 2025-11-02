---
title: "IAMS"
date: 2025-10-29
menu:
  main:
    name: "IAMS"
    weight: 25
bookToc: true
bookFlatSection: false
---

# Building Google A2A Agent Systems
## Claude Code + Jeremy - Technical Workspace

Real documentation of building production-ready agent systems using Google Cloud's Agent Development Kit and Vertex AI.

**Status:** Day 2 | Active Development
**Total Docs:** 34 planning + 4 infrastructure = 38 documents
**Progress:** Foundation complete → Implementation starting

---

## Quick Stats

```
┌─────────────────────────────────┐
│ CURRENT SPRINT (Oct 28 - Nov 3)│
├─────────────────────────────────┤
│ ✅ Python dependencies          │
│ ✅ API client boilerplate       │
│ ✅ Firebase structure           │
│ 🔄 Documentation site           │
│ ⏳ First agent deployment       │
└─────────────────────────────────┘

┌──────────────────────┐
│  DOCUMENT BREAKDOWN  │
├──────────────────────┤
│ Foundation:    15    │
│ System:        13    │
│ Agents:         6    │
│ Progress:       2    │
│ Infrastructure: 4    │
├──────────────────────┤
│ TOTAL:         38    │
└──────────────────────┘
```

---

## Navigation

### [Daily Journal](/iams/journal/)
Real-time log of what we're building, how we're building it, problems hit, solutions found.

**Latest:** [Day 2: Oct 29, 2025](/iams/journal/2025-10-29/) - Infrastructure setup & plugin system debug

### [Foundation](/iams/foundation/) (15 docs)
Core architecture decisions - Agent Marketplace, A2A Framework, IAE Platform

**Start here:** [001] Agent marketplace implementation plan

### [System](/iams/system/) (13 docs)
Complete platform documentation - Analysis, architecture, planning, transformation

**Key doc:** [018] Complete implementation blueprint

### [Agents](/iams/agents/) (6 docs)
SDR automation, manager platform, tool-enabled agents

**Latest:** [033] SDR + Manager workflows specification

### [Progress](/iams/progress/) (2 docs)
Status reports, dashboards, what's done/not done

### [Infrastructure](/iams/infrastructure/)
Technical setup - Python, Firebase, APIs, deployment

### [Reference](/iams/reference/)
Quick links, standards, tools, official documentation

### [Challenges](/iams/challenges/)
Real problems we hit and how we solved them

---

## What We're Building

### Intent Agent Models (IAMS)
A production-ready agent platform combining:
- **Agent Offerings:** Containerized AI agent marketplace
- **A2A Framework:** Agent-to-Agent communication
- **IAE:** Intelligence Agent Engine core
- **Tool-Enabled Agents:** Function-calling for real actions
- **SDR Manager Automation:** Sales effectiveness platform

### Technical Stack
- Google Vertex AI Agent Engine
- Firebase Functions & Firestore
- Cloud Run containerized deployment
- Python + Google ADK
- Real API integrations (Salesforce, Apollo, ZoomInfo)

---

## Latest Updates

**2025-10-29:**
- Infrastructure setup complete (dependencies, API clients, Firebase)
- Plugin system debugged and documented
- Documentation site structure planned
- Day 2 journal entry published

**2025-10-28:**
- SDR + Manager workflows added ([033], [034])
- Documentation renumbering (058-096 → 001-034)
- All 34 planning documents organized

---

## Start Here

**New to this project?**
1. Read [018-PP-EXEC-iams-complete-implementation-blueprint](/iams/system/architecture/018-complete-blueprint/)
2. Check [Today's Journal](/iams/journal/2025-10-29/)
3. Review [Tool-Enabled Implementation Guide](/iams/agents/tool-enabled/implementation-guide/)

**Ready to build?**
1. Follow [022-PM-TASK-iams-implementation-checklist](/iams/system/planning/022-implementation-checklist/)
2. Review [Infrastructure Setup](/iams/infrastructure/)
3. Check [Latest Progress](/iams/progress/)

---

## External Links

- [Claude Code Plugins](https://claudecodeplugins.io) - Jeremy's 227-plugin marketplace
- [Google ADK Docs](https://google.github.io/adk-docs/)
- [Agent Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack)
- [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview)

---

## Why This Site Exists

This is **our workspace** - a transparent, living record of building Google A2A systems.

It's both:
- **A learning resource** - Others can see how real agent systems get built
- **A study guide** - Jeremy can review what we built and why

No marketing. No fluff. Just real work, real code, real problems, real solutions.

---

**Last Updated:** 2025-10-29
**Next Review:** Daily at 5 PM EST

*Built with Claude Code. Documented in real-time.*