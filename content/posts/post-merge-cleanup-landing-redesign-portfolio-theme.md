+++
title = 'Post-Merge Cleanup, Landing Redesign, and Portfolio Theme Overhaul'
slug = 'post-merge-cleanup-landing-redesign-portfolio-theme'
date = 2026-01-19T10:00:00-06:00
draft = false
tags = ["git-with-intent", "intent-solutions-landing", "jeremylongshore", "bounty-tracker", "merge-conflicts", "css"]
categories = ["Development Journey"]
description = "Resolving git-with-intent merge conflicts, adding contact form and Learn/Colab pages to the landing site, overhauling jeremylongshore.com with a charcoal slate theme, and updating bounty tracker status."
+++

Seven commits across four repos. A cleanup day -- resolving merge debt from the previous week's feature branches, filling content gaps on the landing site, and refreshing the personal site's visual identity. None of these changes are individually significant, but collectively they close out a week of parallel development and get everything back to a clean main branch.

The pattern of building features in parallel and then spending a day on merge cleanup is becoming standard for multi-repo work. It's not glamorous, but skipping the cleanup creates compounding confusion.

## git-with-intent: Merge Conflict Resolution

The compliance reports branch (D4.x) and the violation pipeline branch (D5.x) had been developed in parallel. Both touched the event store schema, both modified the tenant configuration format, and both added new API routes.

The merge conflicts were in three categories:

**Schema conflicts** -- both branches added columns to the events table. The resolution was straightforward: keep both sets of columns, reorder to maintain logical grouping (timestamps together, references together, metadata last).

**Config format conflicts** -- D4.x added compliance report scheduling to tenant config. D5.x added violation alert routing to tenant config. Both used the same `notifications` key. The resolution split it into `notifications.compliance` and `notifications.violations`.

**Route conflicts** -- both branches registered routes under `/api/reports`. The resolution namespaced them: `/api/reports/compliance` for D4.x and `/api/reports/violations` for D5.x.

Two commits for the merge itself plus the conflict resolution. No tests broke after the merge, which suggests the test suites were adequately isolated.

## intent-solutions-landing: Contact Form and Content Pages

### Contact Form

The landing site lacked a contact form. Visitors who wanted to reach out had to find the email address buried in the footer -- not exactly a conversion-friendly experience. The new contact form uses Firebase's HTTP callable functions to send an email notification without exposing an email address on the page.

The form collects name, email, company (optional), and message. Validation runs client-side for immediate feedback and server-side in the callable function for safety. Submissions go to a Firestore collection for tracking and trigger an email to the Intent Solutions inbox via SendGrid.

### Learn and Colab Pages

Two new content pages:

**Learn** -- curated links to Intent Solutions' educational content. Blog posts organized by topic, video tutorials (when they exist), and documentation for open-source projects. The page is primarily a navigation hub, not original content.

**Colab** -- the collaboration model page. Describes how Intent Solutions works with clients: discovery call, scoped proposal, iterative delivery, post-delivery support. The page targets potential clients who've already decided they want AI agent help and need to understand the engagement model.

## jeremylongshore.com: Charcoal Slate Theme

The personal site was using the default hugo-bearblog colors. The charcoal slate theme is a dark-mode redesign:

- Background: `#1a1a2e` (deep navy-charcoal)
- Text: `#e0e0e0` (soft white, not pure white)
- Accent: `#4a9eff` (muted blue for links and headings)
- Code blocks: `#0f0f23` background with `#f0f0f0` text

The theme required overriding three CSS files in the hugo-bearblog layouts. The color palette was chosen for readability during long reading sessions -- pure white on pure black causes eye strain, but soft white on dark charcoal doesn't.

The hardest part was getting code blocks to look right. The default syntax highlighting theme clashed with the dark background -- keywords in dark blue were nearly invisible. Switching the highlight style to `monokai` and setting a slightly lighter code block background (`#0f0f23` instead of the page background) fixed the contrast without breaking the overall aesthetic. Inline code uses the accent blue with a subtle background tint.

## Bounty Tracker: Status Updates

The bounty tracker gained a status display in the dashboard. Each bounty now shows one of five states: `discovered`, `qualifying`, `in-progress`, `submitted`, `paid`. State transitions are timestamped and shown in a mini timeline on the bounty detail view.

The status update also fixed a display bug where bounties with no estimated hours showed "Infinity" in the expected value column instead of "N/A". The root cause was a division by zero in the EV calculation -- `bountyAmount / estimatedHours` where `estimatedHours` was `0` instead of `null`. The fix added a guard clause and rendered "N/A" when hours are unknown rather than attempting the calculation.

The status timeline also required a small schema migration. The previous schema stored status as a single string field. The new schema stores an array of `{status, timestamp, actor}` objects so the full history is preserved. Existing bounties got a migration that wrapped the current status into the first timeline entry with the bounty creation date as the timestamp.

## Numbers

| Repo | Commits | Focus |
|------|---------|-------|
| git-with-intent | 2 | Merge conflict resolution |
| intent-solutions-landing | 3 | Contact form, Learn, Colab |
| jeremylongshore.com | 1 | Charcoal slate theme |
| bounty-tracker | 1 | Status display + bug fix |
| **Total** | **7** | |

## Related Posts

- [Firebase Migration Debugging Saga](/posts/firebase-migration-debugging-saga-bounty-proof-wall/) -- the Firebase migration that this landing work builds on
- [Model-Agnostic Positioning and the IAE Branding Back-and-Forth](/posts/intent-solutions-landing-model-agnostic-positioning/) -- earlier landing site iteration
- [git-with-intent v0.9 to v0.10: Docker Upgrades and Strategic Research](/posts/git-with-intent-v090-v0100-docker-upgrades/) -- later GWI work after these branches merged
