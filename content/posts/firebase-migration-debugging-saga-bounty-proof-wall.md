+++
title = 'Firebase Migration Debugging Saga, GWI PR Reviews, and the Bounty Proof Wall'
slug = 'firebase-migration-debugging-saga-bounty-proof-wall'
date = 2026-01-18T10:00:00-06:00
draft = false
tags = ["firebase", "netlify", "ci-cd", "debugging", "git-with-intent", "bounty", "workload-identity-federation"]
categories = ["Technical Deep-Dive"]
description = "Migrating intent-solutions-landing from Netlify to Firebase Hosting with a long CI debugging saga (WIF, IAM, billing API, token issues, infinite recursion), shipping GWI D4.5-D4.6 with PR review fixes, and building the bounty dashboard with CSV import and proof wall."
+++

Thirty-six commits across three repos. The Firebase migration ate most of the day -- not because the migration itself was hard, but because CI kept breaking in new and creative ways. The GWI and bounty work shipped cleanly by comparison.

## Firebase Migration: The Plan

The intent-solutions-landing site was on Netlify. It worked fine, but having the company landing page on a different platform than everything else (Firebase) meant two sets of deployment configs, two DNS management interfaces, two SSL certificate renewal processes. Consolidation to Firebase Hosting was the goal.

The migration plan was straightforward:

1. Add `firebase.json` hosting config
2. Set up GitHub Actions for deploy-on-push
3. Point DNS to Firebase
4. Remove Netlify config

Steps 1 and 4 took five minutes each. Steps 2 and 3 took the rest of the day.

## The CI Debugging Saga

### Workload Identity Federation

Firebase deploys from GitHub Actions need authentication. The recommended approach is Workload Identity Federation (WIF) -- no service account keys stored in GitHub secrets, just a trust relationship between GitHub's OIDC provider and GCP's IAM.

The WIF setup requires:

1. A workload identity pool
2. A workload identity provider linked to GitHub's OIDC
3. A service account with Firebase Hosting deploy permissions
4. An IAM binding that lets the GitHub OIDC token impersonate the service account

I'd done this before for other projects. The pool and provider already existed. The service account was new but straightforward. The IAM binding was where things started breaking.

### IAM Permission Cascade

The first deploy failed with `Permission denied on resource project`. The service account had `roles/firebasehosting.admin`. That should be enough. It wasn't.

Firebase Hosting deploys also need `roles/run.admin` (because Firebase Hosting uses Cloud Run under the hood for certain features), `roles/artifactregistry.reader` (because the deploy process pulls container images), and `roles/iam.serviceAccountUser` (because the deploy impersonates itself during the Cloud Run setup). Four roles for what should be a single operation.

Each missing role produced a different error message, none of which mentioned the actual missing role. The `Permission denied on resource project` error for a missing `artifactregistry.reader` role is particularly unhelpful.

### Billing API Surprise

After fixing the IAM roles, the next deploy failed with `Billing account not found or not enabled`. The GCP project had billing enabled. The Firebase project was linked to the GCP project. The billing API, however, was not enabled.

Firebase Hosting's deploy process makes a call to the Cloud Billing API to verify the project can incur charges (even for the free tier). If the Billing API isn't enabled at the API level (not the billing account -- the API itself), the deploy fails. This is documented nowhere in the Firebase Hosting docs. It's in a Google Cloud troubleshooting guide for Cloud Run deployments, which you'd only find if you knew Firebase Hosting uses Cloud Run internally.

```bash
gcloud services enable cloudbilling.googleapis.com --project=intent-solutions
```

One command. Two hours to find it.

### Token Expiry Race

The next failure was intermittent. About 30% of deploys failed with `Token expired`. The WIF token has a one-hour lifetime. Firebase Hosting deploys for a simple static site take about 90 seconds. The token shouldn't expire.

The issue was in the GitHub Actions workflow. The `google-github-actions/auth` step generates the token, but subsequent steps that install dependencies (npm install for the build) can take variable time. On a cold runner, npm install plus the Hugo build plus the Firebase deploy could push past the token lifetime if the runner was under load.

The fix: move the auth step to immediately before the deploy step, not at the top of the job. The token is fresh when the deploy needs it.

```yaml
# BEFORE: token generated early, might expire
- uses: google-github-actions/auth@v2
- run: npm install && npm run build
- run: firebase deploy

# AFTER: token generated immediately before use
- run: npm install && npm run build
- uses: google-github-actions/auth@v2
- run: firebase deploy
```

This is a pattern worth remembering for any WIF-based deployment. If your CI job has a build step that takes more than a few minutes, generate the auth token as late as possible.

### Infinite Recursion

The final bug was the most confusing. After the deploy succeeded, the site loaded but every page redirected to itself infinitely. The browser showed ERR_TOO_MANY_REDIRECTS.

The cause: the `firebase.json` had a rewrite rule that sent all requests to the index, which is correct for a single-page app but wrong for a static site. The Hugo build produces actual HTML files at each path. The rewrite rule was intercepting requests for those files and redirecting them to root, which hit the rewrite rule again.

```json
// WRONG - SPA rewrite catches everything
"rewrites": [{ "source": "**", "destination": "/index.html" }]

// RIGHT - no rewrites needed for static sites
// just remove the rewrites section entirely
```

Removing the entire `rewrites` block fixed it. Firebase Hosting serves static files by default -- the rewrite rule was actively harmful.

## GWI: D4.5-D4.6 and PR Review Fixes

### D4.5: Report Distribution

Compliance reports now distribute automatically to configured recipients. Distribution supports email (via SendGrid) and webhook (for Slack/Teams integration). Each recipient can subscribe to specific report types -- the security team gets violation summaries, management gets the monthly compliance overview.

### D4.6: Report Archival

Completed reports archive to a Cloud Storage bucket with lifecycle policies. Reports older than 12 months move to Nearline storage. Reports older than 7 years (the typical regulatory retention period) get flagged for review before deletion.

### PR Review Fixes

Three PRs from Gemini code review had accumulated. The fixes were mechanical:

- Unused import cleanup in the compliance module
- Error message standardization (switching from string interpolation to template literals)
- Missing `await` on an async report generation call that was silently succeeding but not waiting for completion

The missing `await` was the most interesting. The report generation function returned a Promise, and the calling code didn't await it. In development this was invisible -- the report generated fast enough that it completed before anyone checked for it. In CI with slower I/O, the report generation was still running when the test checked for the output file, causing intermittent test failures. The Gemini review flagged it as a potential race condition, which was exactly right.

## Bounty Dashboard

The bounty tracker gained a proper dashboard.

### CSV Import

Bounty data comes from multiple sources: Algora, GitHub Sponsors, and manual entries from Discord bounty boards. The CSV importer normalizes all three formats into the unified bounty schema. Column mapping is configurable per source, so adding a new bounty platform is a config change, not a code change.

The tricky part was date parsing. Algora uses ISO 8601. GitHub Sponsors uses a custom format with timezone abbreviations ("PST", "EST") instead of offsets. Discord entries use whatever the poster felt like typing. The importer chains three date parsers with fallback: ISO 8601 first, then a format-string parser for known platform formats, then a fuzzy natural language parser for the Discord chaos. Unparseable dates get flagged for manual review rather than silently defaulted.

### Proof Wall

The proof wall is the public-facing record of completed bounties. Each entry shows the bounty description, the solution approach (one paragraph), the PR link, and the payout amount. The wall serves two purposes: accountability (proving work was actually done) and marketing (showing the range of problems solved).

Entries are submitted through a form that requires the PR URL, a brief description, and a screenshot of the merged PR. The form validates that the PR URL exists and is merged before accepting the submission.

### Notifications

Bounty state changes trigger notifications. New bounties matching the developer's language preferences get a daily digest email. Bounties approaching deadline get a 48-hour warning. Completed bounties trigger a confirmation to both the hunter and the bounty poster.

The notification system uses a preference store so each developer can tune their alerts. Some want real-time notifications for high-value bounties. Others want a single daily digest. The default is conservative -- daily digest only, no real-time pings -- because notification fatigue is the fastest way to get people to ignore the system entirely.

## Day Summary

| Workstream | Commits | Key Outcome |
|------------|---------|-------------|
| Firebase migration | 18 | Site live on Firebase Hosting |
| CI debugging | (included above) | 5 distinct issues resolved |
| GWI D4.5-D4.6 | 8 | Report distribution + archival |
| GWI PR fixes | 4 | Code review cleanup |
| Bounty dashboard | 6 | CSV import, proof wall, notifications |

The Firebase migration should have taken an hour. It took most of the day. The lesson, as always with CI: the hard part is never the migration itself. It's the authentication chain, the undocumented API dependencies, and the config assumptions that only surface in a clean CI environment.

## Related Posts

- [HustleStats Firebase Migration Days 2-7](/posts/hustlestats-firebase-migration-days-two-through-seven/) -- a previous Firebase migration with its own set of surprises
- [Bounty Scoring Algorithm, GWI Compliance Reports, and Kilo Image Support](/posts/bounty-scoring-algorithm-gwi-compliance-reports/) -- the scoring algorithm that feeds this dashboard
- [GCR to Artifact Registry Deploy Workflow Migration](/posts/gcr-to-artifact-registry-deploy-workflow-migration/) -- another deploy infrastructure migration with similar IAM headaches
