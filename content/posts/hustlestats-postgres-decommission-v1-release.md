+++
title = 'PostgreSQL Decommission, Monitoring Stack, and HustleStats v1.0.0'
slug = 'hustlestats-postgres-decommission-v1-release'
date = 2025-11-18T10:00:00-06:00
draft = false
tags = ["hustlestats", "postgres", "monitoring", "production", "v1-release", "eslint", "vertex-ai"]
categories = ["Development Journey"]
description = "31 commits across HustleStats: decommissioning PostgreSQL, standing up structured logging and GCP alerts, enriching player profiles, and cutting the v1.0.0 release."
+++

31 commits in a single day. Not 31 features -- 31 cleanup, hardening, and shipping tasks that turned a working prototype into a released product. The commit volume sounds dramatic. The reality is unglamorous. This was the grind that makes software real.

## PostgreSQL Decommission

HustleStats started on PostgreSQL with Prisma as the ORM. The data layer migrated to Firestore months ago, but the Prisma dependency lingered -- unused schema files, legacy route handlers, and a healthcheck endpoint that still pinged a Postgres connection string that no longer existed.

Removed Prisma entirely. Deleted the schema files, the migration history, and the client generation step from the build pipeline. Archived the legacy API routes that referenced it. Simplified the healthcheck to verify Firestore connectivity only. Updated the deployment docs to reflect the actual data layer.

The decommission was overdue. Dead dependencies are not harmless. They confuse new contributors, inflate the dependency tree, and create phantom failures in CI when a transitive dependency breaks. In this case, the Prisma dependency pulled in `@prisma/client`, `prisma` CLI, and the PostgreSQL driver -- none of which had any purpose. The healthcheck was the worst offender: it pinged a Postgres connection string that no longer existed in production, timing out after 5 seconds on every check, making the healthcheck report stale data about a database nobody used.

## Monitoring Stack

Production without monitoring is a demo. Three pieces went in today:

**Structured JSON logging.** Every API route now emits structured logs with consistent fields: timestamp, route, user ID, response time, error details. GCP Cloud Logging ingests these directly without custom parsing.

**GCP alert policies.** Error rate threshold alerts, latency P95 alerts, and a dead-man's-switch that fires if the healthcheck stops responding. These route to a PagerDuty channel that forwards to Slack.

**Firebase Performance Monitoring.** Client-side page load metrics, API call latency from the browser's perspective, and custom traces around the Vertex AI inference calls. The Vertex AI telemetry is particularly useful -- it surfaces when model latency spikes independently of application latency.

Smoke tests validate the monitoring pipeline on every deploy. They hit the healthcheck, trigger a test alert, and verify that structured logs appear in Cloud Logging within 30 seconds. The smoke tests also exercise the Vertex AI telemetry path -- they send a synthetic inference request and confirm the custom trace appears in Firebase Performance Monitoring.

## Player Profile Enrichment

HustleStats tracks youth athletes. The player model was anemic -- name, team, and a handful of stats. Today it got real data:

- **13 position codes** covering every position across soccer, basketball, baseball, softball, and volleyball
- **Gender field** with proper enum validation
- **56 league identifiers** spanning recreational, travel, club, and school leagues
- **Zod validation schemas** enforcing all of it at the API boundary

The Zod schemas are the important part. Without them, the enrichment data is just more fields that can hold garbage. With them, the API rejects malformed profiles before they hit Firestore.

## Production Deploy Workflow

The GitHub Actions deploy pipeline got a full overhaul. Build, test, deploy to Cloud Run, run smoke tests, and roll back automatically if smoke tests fail. The rollback uses Cloud Run traffic splitting -- if the new revision fails smoke tests, traffic routes back to the previous revision within 60 seconds.

This is table stakes for production, but HustleStats didn't have it until today. The previous workflow was `git push` and hope. If the deployment failed, the only signal was a customer complaint. Now the pipeline either succeeds with verified smoke tests or rolls back automatically. The rollback has already saved one deployment -- a misconfigured environment variable that passed the build but failed the healthcheck.

## v1.0.0

Cut the first official release. README rewritten from scratch -- not the auto-generated Next.js boilerplate, but an actual project README covering architecture, setup instructions, environment variables, and deployment. CHANGELOG covering every milestone since the initial commit. GitHub Pages site generated from the README.

Tagged `v1.0.0` in git. The version number is a statement: this is no longer experimental. It has monitoring, it has validation, it has automated rollback, and it has documentation that a new developer could follow without asking me questions. That last part is what separates a project from a product.

## jeremylongshore.com Update

Updated the projects page on the personal site to reflect HustleStats reaching v1.0.0. Minor change, but keeping the portfolio current matters when the portfolio is part of the product story.

## ESLint Cleanup

100+ linting warnings resolved. Most were unused imports and missing return types. A few were genuine issues -- unreachable code paths and implicit `any` types that masked potential runtime errors.

ESLint cleanup is never exciting. But a clean lint output means the *next* warning actually gets noticed. When you have 100 warnings, nobody reads them. When you have zero warnings and a new one appears, it gets fixed the same day.

## NWSL Video Pipeline

Separate project, same day. The NWSL highlight video pipeline hit an edge case: Imagen 4 failed to generate a specific thumbnail. The fallback to Imagen 3 kicked in correctly, but the voiceover timing was off by 2 seconds because the fallback image had different dimensions.

Fixed the voiceover timing calculation to normalize against the output aspect ratio regardless of which Imagen version produced the thumbnail. The 90-second assembly pipeline now handles both Imagen versions without manual intervention.

## The Day in Numbers

31 commits. PostgreSQL fully decommissioned. Three-layer monitoring stack operational. Player profiles enriched with position, gender, and league data behind Zod validation. Deploy pipeline with automatic rollback. v1.0.0 tagged and documented.

None of this is novel engineering. All of it is necessary engineering. The gap between "it works on my machine" and "it's a product" is exactly this kind of work.

---

**Related Posts:**

- [HustleStats Production Auth Debugging: NextAuth, PrismaAdapter, and Cascading Failures](/posts/hustlestats-production-auth-debugging-nextauth-prisma/) -- The auth crisis that preceded this stabilization work
- [Deployment Secrets, Missing Columns, and Sitemap Hygiene](/posts/hustlestats-defensive-schema-email-config-sitemap-cleanup/) -- Earlier HustleStats maintenance in the same codebase
- [COPPA Compliance in a Youth Sports App](/posts/coppa-compliance-youth-sports-app-real-implementation-process/) -- The compliance side of building for youth athletes
