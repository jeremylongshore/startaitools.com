---
title: "[001] Agent Offerings Implementation Plan"
date: 2025-10-26
weight: 1
bookToc: true
doc_number: "001"
category: "PP"
type: "PLAN"
tags: ["agent-marketplace", "planning", "pricing", "product"]
related: ["002", "003", "004"]
---

# [001] AI Agent Offerings - Implementation Plan

**Date:** 2025-10-26
**Category:** Product & Planning
**Type:** Implementation Plan
**Status:** Foundation Complete

---

## Quick Summary

Research-backed plan to add 3 containerized AI agent products to intentsolutions.io. Based on comprehensive market research, validated ROI metrics, and competitive analysis.

**Key Decision:** Focus on 3 core agents (LinkedIn, Meeting, Support) with 2-tier pricing and fact-based positioning.

---

## Executive Summary

### Recommendations
- ✅ **3 core agents** - LinkedIn, Meeting, Support (NOT 5)
- ✅ **2-tier pricing** - Self-serve + Managed (with Custom option)
- ✅ **Remove unverifiable claims** - Use ONLY validated ROI metrics
- ✅ **Position 40-60th percentile** - Above average, below premium
- ✅ **Technical, no-BS tone** - Maintain authenticity

---

## Product Lineup

### Agent 1: LinkedIn Outbound Agent

**Market Position:** 40th percentile
`Dux-Soup $41 < YOU $59-79 < PhantomBuster $99 < Expandi $99`

#### Validated Claims
- ✅ **"Replaces 3-5 SDRs"** - TRUE (SDR avg: $75K/yr = $6,250/mo)
- ✅ **"Books meetings autonomously"** - TRUE (verified competitors)
- ✅ **"Processes 1,000+ leads/day"** - TRUE (PhantomBuster benchmark)
- ❌ **"3x higher response rates"** - UNVERIFIED (ideal scenario only)

#### Pricing
| Tier | Price | What You Get |
|------|-------|--------------|
| **Self-serve** | $197/mo | You deploy on AWS/GCP |
| **Managed** | $797/mo | I host, manage, monitor |
| **Custom** | $5K-15K + $297/mo | Enterprise customization |

#### What It Actually Does
1. Finds prospects matching ICP on LinkedIn
2. Enriches data via Apollo.io / Clay.com APIs
3. Generates personalized messages (GPT-4 templates)
4. Sends connection requests + follow-ups
5. Books qualified meetings to calendar
6. Updates HubSpot/CRM with activity

#### Real Integrations
- LinkedIn Sales Navigator API
- Apollo.io enrichment
- Instantly.ai / Lemlist (email)
- HubSpot / Salesforce CRM
- Calendly / Cal.com booking

---

### Agent 2: Meeting Intelligence Agent

**Market Position:** 55th percentile
`Sembly $10-20 < YOU $97-297 < Grain $29 < Fireflies $39`

#### Validated Claims
- ✅ **"Saves 5+ hours/week"** - TRUE (Nielsen Norman verified)
- ✅ **"98% transcription accuracy"** - TRUE (Otter.ai benchmark)
- ✅ **"Extracts action items"** - TRUE (standard feature)
- ❌ **"Replaces executive assistant"** - TOO BOLD (30% task completion)

#### Pricing
| Tier | Price | What You Get |
|------|-------|--------------|
| **Self-serve** | $97/mo | Containerized, you host |
| **Managed** | $297/mo | I host + support |
| **Custom** | $5K-15K + $297/mo | Enterprise features |

#### What It Actually Does
1. Joins Google Meet / Zoom calls (bot participant)
2. Transcribes with 90-98% accuracy (Whisper API)
3. Generates structured summary (agenda, decisions, actions)
4. Extracts action items with assignees
5. Sends follow-up emails with summary
6. Updates Notion / HubSpot with meeting notes

#### Real Integrations
- Google Meet / Zoom webhook
- OpenAI Whisper (transcription)
- GPT-4 (summarization)
- Notion / Confluence
- Slack (notifications)
- HubSpot (CRM update)

---

### Agent 3: Customer Support Triage Agent

**Market Position:** 60th percentile
`Intercom Fin $74 < YOU $147-497 < Zendesk $125`

#### Validated Claims
- ✅ **"4 hours → 4 minutes"** - TRUE (McKinsey 74% reduction)
- ✅ **"Handles 45-50% of queries"** - TRUE (retail/travel benchmark)
- ✅ **"Human approval required"** - GOOD DISCLAIMER
- ❌ **"Replaces support team"** - FALSE (45-50% deflection, not 100%)

#### Pricing
| Tier | Price | What You Get |
|------|-------|--------------|
| **Self-serve** | $147/mo | Docker container |
| **Managed** | $497/mo | I host + manage |
| **Custom** | $5K-15K + $297/mo | Enterprise integration |

#### What It Actually Does
1. Monitors Zendesk / Intercom ticket queue
2. Categorizes by urgency/department (ML)
3. Drafts responses using knowledge base (RAG)
4. **Requires human approval** before sending
5. Escalates complex/sensitive issues
6. Learns from approved/edited responses

#### Real Integrations
- Zendesk / Intercom API
- Notion / Confluence (knowledge base)
- OpenAI GPT-4 (responses)
- Slack (escalation)

---

## What We're NOT Adding

### ❌ Research Agent
**Why:** Too broad, unclear value prop. Data enrichment already covered in LinkedIn agent.

### ❌ Security Agent
**Why:** Wrong audience. Selling to operators/founders, not CISOs. Enterprise sales cycle.

### ❌ "AI Agent Suite" Bundle
**Why:** Only 3 agents. Bundle makes sense at 4-5+ products. Offer multi-agent discount instead.

---

## Pricing Strategy

### Market Positioning: 40-60th Percentile

**Why This Works:**
- **Not budget tier** ($10-20/mo) - signals quality
- **Not premium** ($4K+/mo) - accessible to SMBs
- **"Above average" psychology** - worth paying for
- **Room for growth** - 10-15% annual increases

### Complete Pricing Matrix

| Agent | Self-Serve | Managed | Custom |
|-------|-----------|---------|--------|
| LinkedIn | $197/mo | $797/mo | $5-15K + $297/mo |
| Meeting | $97/mo | $297/mo | $5-15K + $297/mo |
| Support | $147/mo | $497/mo | $5-15K + $297/mo |
| **ALL 3** | $441/mo | $1,591/mo | $15-45K + $891/mo |
| **Multi-agent discount** | **$397/mo** (save $44) | **$1,497/mo** (save $94) | Custom quote |

### Why Monthly Fees for Self-Serve?

**Research Finding:** Per-seat-only pricing = 2.3x higher churn

**Benefits:**
- **For You:** Recurring revenue, ongoing relationship
- **For Customer:** Predictable costs, includes updates
- **What's Included:** Docker updates, bug fixes, email support

---

## Content Audit

### ❌ Remove These Claims

**Too Grandiose:**
- "creating industries that don't exist"
  → **Replace:** "ai systems that ship to production"

**Unverified:**
- "AI transformation for your business"
- "Revolutionize" or "disrupt"
- "Save 80%+ of time"
- "Replace entire teams"
- "Deploy in minutes"

### ✅ Use Factual Statements

| Instead of... | Use... |
|---------------|--------|
| "AI transformation" | "3 containerized AI agents for outreach, meetings, support" |
| "Save 80% of time" | "Saves 5+ hours/week (Nielsen Norman verified)" |
| "Deploy in minutes" | "Deploy in 1-2 hours (self-serve) or instant (managed)" |
| "Replace entire team" | "Replaces 3-5 SDRs at $6,250/mo each (self-serve at $197/mo)" |

---

## Implementation Status

### ✅ Completed
- Market research and competitive analysis
- Pricing strategy validation
- Product positioning defined
- Content audit complete

### 🔄 In Progress
- Technical architecture design (see [003])
- Container implementation
- API integrations

### ⏳ Planned
- Product page design
- Demo videos
- Customer onboarding flows

---

## Related Documents

- **[002]** Market Research & Competitive Analysis - Full data
- **[003]** Container-Based Agent Architecture - Technical design
- **[004]** Final Implementation Decision - Architecture choice

---

## Key Takeaways

1. **Focus beats breadth** - 3 well-defined agents > 5 vague ones
2. **Facts over hype** - Validated ROI metrics build trust
3. **Tier pricing** - Self-serve accessibility + managed convenience
4. **Market positioning** - 40-60th percentile = "worth it" psychology
5. **No BS tone** - Technical authenticity differentiates

---

**Next Steps:** Review competitive analysis ([002]) → Design architecture ([003]) → Finalize decision ([004])