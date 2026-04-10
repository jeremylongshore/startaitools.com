+++
title = 'Deployment Secrets, Missing Columns, and Sitemap Hygiene'
slug = 'hustlestats-defensive-schema-email-config-sitemap-cleanup'
date = 2025-10-22T10:00:00-05:00
draft = false
tags = ["hustlestats", "prisma", "deployment", "seo", "maintenance"]
categories = ["Development Journey"]
description = "Three unrelated fixes across two projects: wiring email secrets for password reset, patching a Prisma schema gap that crashed every dashboard page, and cleaning duplicate content from Google Search Console."
+++

Three commits across two repos today. No theme, no arc -- just the kind of maintenance work that keeps production systems from embarrassing you.

## HustleStats: Email Configuration

Password reset was broken in production. Users clicking "Forgot Password" got nothing -- no email, no error message on the frontend, just silence. The Resend API integration was wired up correctly in the application code, the email templates existed, and everything worked in local development. The problem was upstream in the deployment pipeline.

Two changes to the GitHub Actions workflow:

- Added `RESEND_API_KEY` as a repository secret passed to the deployment
- Added `EMAIL_FROM` as an environment variable so the sender address resolved correctly

Two insertions, three deletions. The fix was trivial once identified.

The pattern here is one I keep running into: local dev uses a `.env` file with all the secrets pre-loaded, so the feature works perfectly on your machine. Production uses a completely different secret injection mechanism -- GitHub Actions secrets, Cloud Run environment variables, Kubernetes secrets -- and if you forget to wire one up, the failure is silent. The application code does not crash. It just quietly fails to send the email.

Practical takeaway: if your app sends transactional email, add a health check that verifies the email provider credentials are present at startup. A loud failure on deploy beats a silent failure when a customer needs to reset their password.

A simple guard in your startup code:

```typescript
if (!process.env.RESEND_API_KEY) {
  throw new Error('RESEND_API_KEY is not set — email will not work');
}
```

This costs nothing and saves you from shipping a broken auth flow to production.

## HustleStats: Defensive Stats Schema Migration

Every single dashboard page was crashing with a Prisma error:

```
P2022: The column `Game.tackles` does not exist in the current database
```

The application code referenced five defensive statistics columns -- tackles, interceptions, clearances, blocks, and aerialDuelsWon -- that had been added to the Prisma schema file but never migrated to the actual database. The schema said the columns existed. The database disagreed.

This is a specific failure mode with Prisma that is worth understanding. When you add columns to your `schema.prisma` file and run `prisma generate`, the client gets updated with the new types. Your TypeScript code compiles. Your IDE provides autocomplete. Everything looks correct. But unless you also run `prisma migrate dev` (local) or `prisma migrate deploy` (production) to actually alter the database tables, those columns only exist in the ORM layer.

The fix was seven insertions to the migration file -- all five columns defined as optional integers with sensible defaults. After applying the migration, every dashboard page recovered immediately.

If you use Prisma in any project with CI/CD, add `prisma migrate status` as a pipeline check. It returns a non-zero exit code when there are pending migrations. That one line in your CI config would have caught this before deployment.

In a GitHub Actions workflow, it looks like this:

```yaml
- name: Check for pending Prisma migrations
  run: npx prisma migrate status
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

Fails the build if any migration has not been applied. Cheap insurance.

## jeremylongshore.com: Search Console Cleanup

Google Search Console was flagging duplicate content and crawl budget waste. After investigating, three distinct sources of the problem:

**Legacy `/en/` directory.** An old internationalization experiment had left a complete mirror of the site content under `/en/`. Every page had a duplicate at a `/en/` path. Google was indexing both versions and flagging them as duplicates, which dilutes page authority and wastes crawl budget.

**RSS sync duplicates.** The automated content sync from startaitools.com (via RSS) had created eight posts in the `startai/` subdirectory that were copies of posts already published elsewhere on the site. The sync script creates files but has no logic to detect or remove files when the source changes.

**Placeholder navigation pages.** Seven pages that existed only to populate navigation menus -- no real content, just titles and empty bodies. Google was crawling and indexing them, then flagging them as thin content.

Deleted 16 files totaling 3,085 lines. The sitemap cleaned up immediately. Google typically takes one to two crawl cycles to reflect removals, so the Search Console warnings should clear within a week or two.

The broader lesson for anyone running a static site with automated content pipelines: schedule periodic audits of your output directory. Automated processes excel at creating files and have zero awareness of when those files become redundant. A quarterly check of your sitemap against Search Console will catch drift before it accumulates.

A quick way to spot problems: compare the number of URLs in your sitemap against the number of pages Google reports as indexed. If indexed pages significantly exceeds your sitemap count, you have orphan or duplicate content that Google found but you did not intend to publish. That gap is what flagged this cleanup.

---

**Related Posts:**
- [HustleStats Production Auth Debugging](/posts/hustlestats-production-auth-debugging-nextauth-prisma/) -- yesterday's cascading auth failures in the same codebase
- [Deploying Next.js 15 to Google Cloud Run](/posts/deploying-nextjs-15-google-cloud-run-custom-domain-ssl/) -- the original HustleStats deployment
- [Building Production CI/CD](/posts/building-production-ci-cd-documentation-to-deployment/) -- CI/CD pipeline patterns for catching issues like missing migrations
