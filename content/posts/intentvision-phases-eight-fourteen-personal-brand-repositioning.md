+++
title = 'IntentVision Phases 8-14 and Personal Brand Repositioning'
slug = 'intentvision-phases-eight-fourteen-personal-brand-repositioning'
date = 2026-02-01T10:00:00-06:00
draft = false
tags = ["intentvision", "jeremylongshore", "devops", "terraform", "bounties", "staging"]
categories = ["Development Journey"]
description = "IntentVision powers through seven phases from notifications to DevOps playbook, jeremylongshore.com gets a personal brand repositioning, and bounties adds CODEOWNERS governance."
+++

February opened with an IntentVision sprint. Seven phases in a single day, pushing the product from a working dashboard toward something you could actually sell.

Twenty-eight commits across three repos. Nineteen on IntentVision, eight on jeremylongshore.com, and one on bounties. The IntentVision work was the main event. The jeremylongshore.com repositioning was strategic. The bounties commit was governance.

## IntentVision: Phases 8 Through 14

The first seven phases (covered in a previous post) gave IntentVision its data layer, visualization primitives, and dashboard composition. Phases 8 through 14 are about operational maturity — the difference between a demo and a product.

**Phase 8: Notifications.** The dashboard can now push alerts when metrics cross thresholds. The implementation uses a pub/sub pattern internally so adding new notification channels (Slack, email, PagerDuty) is a config change rather than a code change. For now it's in-app only. The infrastructure is ready for the rest.

The threshold configuration lives in the dashboard UI — no YAML editing required. You pick a metric, set an operator (greater than, less than, equals), and define the value. When the condition fires, the notification includes the metric name, current value, threshold value, and a deep link to the relevant dashboard panel.

The pub/sub approach means the notification system doesn't know about the dashboard and the dashboard doesn't know about the notification system. They communicate through events. This decoupling is deliberate — when Phase 14's DevOps playbook says "add a Slack channel for alerts," the implementation is adding a Slack subscriber to the pub/sub bus, not modifying the notification engine.

**Phase 9: Staging environment.** A separate Cloud Run service running the staging build with its own Firestore database. The staging environment mirrors production configuration but uses synthetic data. This lets you demo features without exposing real usage patterns.

The synthetic data generator creates realistic-looking metrics — not random noise, but patterns that mimic actual team velocity curves and commit frequency distributions. A potential customer looking at the staging demo sees what their dashboard would look like, not what a random number generator looks like.

**Phase 10: Sellable alpha.** The first pass at packaging — a deployment guide, environment variable documentation, and a setup script that takes you from `git clone` to running instance in under 10 minutes. The word "sellable" is doing heavy lifting here. It means someone who isn't me can install and configure it without a phone call.

The setup script validates prerequisites (Node.js version, gcloud CLI, Terraform), creates the GCP project if needed, and runs the initial Terraform apply. It's opinionated — one deployment topology, one region, one set of defaults. Customization comes later.

**Phase 11: Usage metering.** Every API call and dashboard render gets a counter. The metering is lightweight — increment a counter in Firestore, batch-flush every 60 seconds. No Prometheus yet, just raw counts. The counters are namespaced by customer, operation type, and time bucket (hourly granularity).

The goal is to have data for pricing conversations: how much does a typical team actually use? A week of metering data should answer whether per-seat or per-operation pricing makes more sense.

**Phase 12: Terraform.** The GCP infrastructure moved from click-ops and gcloud commands to Terraform modules. Cloud Run service, Firestore database, IAM bindings, and the staging environment all declarative. The modules are parameterized so spinning up a new customer environment is `terraform apply -var="customer=acme"`.

State lives in a GCS backend bucket with versioning enabled, so any Terraform disaster is recoverable. The state bucket itself is the one resource created manually — the chicken-and-egg problem of managing infrastructure-as-code state with infrastructure-as-code. The bucket has a 30-day retention policy on deleted objects, which has already saved one terraform state corruption during development.

**Phase 13: Stabilization.** A dedicated phase for fixing the things that broke during the feature sprint. Two categories of fixes:

- Notification edge cases: what happens when a threshold is crossed multiple times in the same batch window? Answer: deduplicate by threshold ID within the batch interval.
- Terraform state drift: the 6 manually-created resources from before Phase 12 needed to be imported into Terraform state. Each import required matching the Terraform resource definition to the existing cloud resource's configuration exactly.

**Phase 14: DevOps playbook.** An operational runbook covering deployment procedures, rollback steps, monitoring checks, and incident response. Written for a future team member, not for me. If I get hit by a bus, someone can operate IntentVision from the playbook. The playbook includes `terraform destroy` instructions for clean customer deprovisioning — a step that's easy to forget but critical for data retention compliance.

Seven phases sounds like a lot for one day. Each phase was 2-4 commits. The phases are scoped tight — "notifications" doesn't mean building a full alerting platform, it means the pub/sub infrastructure and one working channel. "Terraform" doesn't mean every resource in the GCP project, it means the resources IntentVision owns.

The discipline of phase-based development pays off here. Each phase has a clear entry state and exit state. You can stop at any phase boundary and have a coherent product. Phase 8 without Phase 9 still works. Phase 12 without Phase 14 still works. The phases are sequential in the development timeline but independent in the product.

The total at the end of the day: IntentVision has notifications, a staging environment, deployment packaging, usage metering, infrastructure-as-code, a stabilization pass, and an operational runbook. That's the difference between "I have a dashboard" and "I have a product someone else can operate." The code changes are incremental. The product posture change is significant.

## jeremylongshore.com: Brand Repositioning

Eight commits on the personal site, all around repositioning. The site had been a standard developer blog with project links. The repositioning reframes it around organizational transformation — helping companies build internal platforms and AI-assisted workflows.

The changes: updated the site tagline from a technology-focused statement to an outcomes-focused one, rewrote the about page to lead with business impact rather than technical skills, restructured the project showcase to group by business impact rather than technology stack, and added case study summaries for the flagship projects.

This isn't a visual redesign. Same hugo-bearblog theme, same layout, same navigation. It's a content repositioning. The audience shifts from "fellow developers who want to see my code" to "engineering leaders evaluating whether to bring me in for a transformation engagement." Every project description now leads with the business problem, not the technology stack.

The case study summaries follow a consistent format: problem statement, approach, outcome with metrics. IRSB becomes "decentralized bounty resolution protocol reducing dispute resolution time from weeks to hours." git-with-intent becomes "AI-assisted git workflow tool replacing manual code review triage with automated intent classification." The plugin marketplace becomes "open-source plugin ecosystem enabling community-contributed AI developer tools."

The repositioning is deliberate timing. With IntentVision reaching sellable-alpha status, the personal brand needs to reflect "someone who ships products" rather than "someone who writes code." The products are the evidence. The brand just needs to point at them correctly.

## Bounties: CODEOWNERS

One commit. Added a CODEOWNERS file to the bounties repo. The file maps directory paths to required reviewers. `/src/scoring/` requires review from someone with scoring algorithm context. `/src/intelligence/` requires review from someone who understands the maintainer profiling system. `/src/core/` is the most approachable path — the data models and API routes that any JavaScript developer can work with.

For a solo developer, CODEOWNERS seems like overhead. It's actually documentation. The file tells future contributors (or future me after a long break) which parts of the codebase have implicit domain knowledge requirements. Not everything in a repo is equally approachable.

When the first external contributor opens a PR, CODEOWNERS ensures they get a review from someone who actually understands the code they changed. More importantly, it signals to potential contributors which areas of the codebase are welcome to outside work and which areas need careful coordination. The scoring algorithm is complex enough that a well-intentioned change could break the EV calculation without any test failing — the tests check correctness, not optimality.

---

## Related Posts

- [Two Products Bootstrapped from Zero to Release in One Day](/posts/gwi-intentvision-bootstrap-two-products-one-day/) — IntentVision's initial bootstrap from empty repo to v0.1.0
- [IRSB Security Audit Fixes, git-with-intent v0.6.0, and GitHub Profile Overhaul](/posts/irsb-security-audit-fixes-gwi-v060-github-profile-overhaul/) — The day before: security work and release engineering across the portfolio
- [February 2026 State of Affairs: 255 Commits, 12 Projects, and What I Shipped](/posts/february-2026-state-of-affairs-255-commits-12-projects/) — Where this month's work rolled up
