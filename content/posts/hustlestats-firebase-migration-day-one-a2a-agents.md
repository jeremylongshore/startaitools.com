+++
title = 'HustleStats Firebase Migration: 5-Agent A2A Architecture on Day One'
slug = 'hustlestats-firebase-migration-day-one-a2a-agents'
date = 2025-11-10T10:00:00-06:00
draft = false
tags = ["hustlestats", "firebase", "a2a", "vertex-ai", "coppa", "cloud-functions", "firestore"]
categories = ["Development Journey"]
description = "Day one of migrating HustleStats to Firebase with a 5-agent A2A architecture, COPPA-compliant security rules, and a 72% cost reduction target. Also committed node_modules."
+++

Four commits to kick off the HustleStats Firebase migration. The previous stack -- Next.js on Cloud Run with Prisma and PostgreSQL -- worked but cost $72/month for a youth sports app with minimal traffic. Firebase brings that down to an estimated $20/month. The tradeoff is a complete backend rewrite.

## The 5-Agent A2A Architecture

HustleStats is a youth soccer statistics tracker. Parents log games, coaches review performance, kids see their highlights. The new backend uses Google's Agent-to-Agent (A2A) protocol with five agents:

1. **Orchestrator** -- Gemini 2.0 Flash, routes requests to specialist agents
2. **Validation Agent** -- schema validation, input sanitization, age-appropriate content filtering
3. **User Creation Agent** -- Firebase Auth user provisioning, role assignment (parent/coach/player)
4. **Onboarding Agent** -- guided setup flow, team creation, roster import
5. **Analytics Agent** -- game stat aggregation, player trend calculations, team comparisons

The orchestrator handles intent classification and routing. When a parent submits a game log, the orchestrator sends it to Validation first (check for required fields, sanitize free-text comments), then to Analytics (calculate per-player stats, update season aggregates).

Each agent is a Cloud Function triggered by Firestore document writes. The A2A communication happens through Firestore documents in a `tasks/` collection. The orchestrator writes a task document, the target agent picks it up via a Firestore trigger, processes it, and writes the result back. No HTTP calls between agents. No message queue. Just shared state in Firestore.

This pattern is simple but effective for low-throughput applications. HustleStats processes maybe 50 game logs per weekend during peak season. The Firestore trigger latency (typically 1-2 seconds) is invisible to users.

## COPPA Compliance from Day One

HustleStats tracks children under 13. COPPA compliance is not optional. The Firestore security rules enforce three things:

**Parental consent gate.** No player profile is visible until a parent account has completed the consent flow. The security rule checks a `consentCompleted` boolean on the parent document before allowing reads on any child player document.

**Data minimization.** Player documents store first name and jersey number only. No last name, no photo, no location data. The security rules reject writes that include restricted fields.

**Deletion on demand.** Parents can delete all data for a child player with a single action. The Cloud Function cascades the delete through game logs, stats aggregates, and team roster entries. The security rule allows parents to delete their children's data but not other families' data.

These rules are in the Firestore security rules file, not in application code. A bug in the Cloud Function cannot bypass them. The rules are the enforcement layer; the application code is the convenience layer.

## CI/CD with Workload Identity Federation

The deployment pipeline uses GitHub Actions with Workload Identity Federation. No service account key files stored in GitHub. The WIF configuration:

- GitHub OIDC provider registered in GCP
- Service account with Firebase Admin and Cloud Functions Developer roles
- Attribute mapping from GitHub repository to GCP principal

Every push to the deploy branch triggers: lint, test, security rules validation, then `firebase deploy`. The security rules validation step runs `firebase emulators:exec` with a test suite that verifies the COPPA rules reject unauthorized access patterns.

## The node_modules Commit

Commit three was a mistake. Committed `node_modules/` to the repository. 3.9 million lines of insertions. The `.gitignore` was missing the entry.

Reverted in the next commit, added `node_modules/` to `.gitignore`, and force-pushed to clean the history. The git log still shows the spike -- 3.9M insertions followed by 3.9M deletions. A reminder to always verify `.gitignore` before the first commit in a new project.

## Cost Projection

The $72/month Cloud Run + PostgreSQL stack breaks down as: $25 Cloud Run (minimum instance), $30 Cloud SQL (smallest PostgreSQL), $12 networking, $5 misc. Most of that cost is floor pricing -- the minimum you pay regardless of traffic.

Firebase pricing for HustleStats' usage pattern:

- **Firestore:** ~$2/month (50 game logs/weekend, small documents)
- **Cloud Functions:** ~$3/month (invocations well within free tier, small compute per call)
- **Firebase Auth:** free tier (under 10K monthly active users)
- **Hosting:** free tier (static assets, minimal bandwidth)
- **Gemini API:** ~$10/month (agent inference, mostly Flash tier)
- **Buffer:** $5/month

Estimated total: $20/month. A 72% reduction. The biggest savings come from eliminating the always-on Cloud SQL instance and Cloud Run minimum.

## What Day One Sets Up

The scaffolding is in place. Five agents defined, security rules written, CI/CD pipeline deployed, cost model validated. Nothing interesting broke. Nothing required a clever workaround. It was a linear execution day -- setup, configure, deploy, verify.

The interesting work starts when real game data flows through the agent pipeline and the edge cases surface. Partial game logs. Duplicate submissions. Coaches editing stats that parents already submitted. The A2A routing will need refinement as those patterns emerge.

For now, the foundation is solid and the cost target is realistic.

---

**Related Posts:**
- [COPPA Compliance for Youth Sports Apps](/posts/coppa-compliance-youth-sports-app-real-implementation-process/) -- The full COPPA implementation guide from the previous HustleStats version
- [HustleStats Production Auth Debugging](/posts/hustlestats-production-auth-debugging-nextauth-prisma/) -- The auth cascade that motivated moving away from NextAuth
- [IAE Product Architecture: A2A Framework with Modular Pricing](/posts/iae-product-architecture-a2a-framework-modular-pricing/) -- The A2A architecture pattern used across Intent Solutions products
