+++
title = 'GCR to Artifact Registry: Late-Night Deploy Fix'
slug = 'gcr-to-artifact-registry-deploy-workflow-migration'
date = 2025-10-18T10:00:00-05:00
draft = false
tags = ["devops", "gcp", "docker", "ci-cd"]
categories = ["Development Journey"]
description = "Migrating a broken deploy workflow from deprecated Google Container Registry to Artifact Registry, plus cleaning up a phantom Sentry secret."
+++

## The 1 AM Deploy Session

Hustle deploys had been failing. The symptom was a cryptic "retry budget exhausted" error during Docker push in the GitHub Actions workflow. The root cause: Google Container Registry (GCR) at `gcr.io` was deprecated. Google had been routing GCR traffic through Artifact Registry for a while, but the old push endpoints were finally returning errors consistently enough to break CI.

Two commits, four minutes apart, at 1:24 and 1:28 AM. The kind of session where the goal is simple: fix the registry, fix the phantom secret, verify green, go to bed.

## Commit 1: Registry Migration

Created a new `hustle-app` repository in Artifact Registry (`us-central1-docker.pkg.dev`), then rewrote the entire GitHub Actions deploy workflow to point at the new registry.

The core image reference change in `.github/workflows/deploy.yml`:

```yaml
# Before (deprecated, failing)
image: gcr.io/${{ secrets.GCP_PROJECT_ID }}/hustle-app

# After (working)
image: us-central1-docker.pkg.dev/${{ secrets.GCP_PROJECT_ID }}/hustle-app/hustle-app
```

The diff was 133 insertions because it wasn't just the image URL. Artifact Registry uses a different authentication flow than GCR. The Docker login step needed `gcloud auth configure-docker us-central1-docker.pkg.dev` instead of the old `gcloud auth configure-docker` (which defaulted to `gcr.io`). The build, tag, and push steps all needed the new full path.

Both prod and staging environments were updated in the same commit. No reason to do this incrementally when the old registry is dead.

Worth noting: if you're using Workload Identity Federation (recommended for GitHub Actions to GCP), the IAM bindings need the Artifact Registry Writer role (`roles/artifactregistry.writer`) on the new repository. The old GCR-specific roles (`roles/storage.admin` on the `artifacts.PROJECT.appspot.com` bucket) don't carry over. This wasn't an issue here since the workflow uses a service account key, but it's a second gotcha for teams using the newer auth pattern.

## Commit 2: Phantom Secret Cleanup

With the registry fixed, the workflow ran further and hit the next failure: a reference to `${{ secrets.SENTRY_DSN }}` that didn't exist in the repo's GitHub Secrets configuration. Sentry was never actually set up for this project. The reference was copy-paste debt from a workflow template.

GitHub Actions doesn't fail on missing secrets by default — it passes an empty string. But the workflow was using the value in a way that caused a downstream error. Removed the reference from both prod and staging configs. Two lines each.

Deploy went green at 1:28 AM.

This is a pattern worth recognizing: the first fix unblocks the pipeline enough for the *next* failure to surface. Registry migration exposed the secret issue. In longer chains, you can spend an hour peeling back layers. Tonight was only two layers deep.

## The GCR Migration Checklist

If you're still pushing to `gcr.io` and haven't hit this yet, here's the migration path:

1. **Create the Artifact Registry repository** in your preferred region — `gcloud artifacts repositories create REPO --repository-format=docker --location=REGION`
2. **Update image URLs** from `gcr.io/PROJECT/IMAGE` to `REGION-docker.pkg.dev/PROJECT/REPO/IMAGE` — note the extra path segment for the repository name
3. **Update Docker auth** — `gcloud auth configure-docker REGION-docker.pkg.dev` instead of the bare `gcloud auth configure-docker`
4. **Update CI/CD workflows** — every step that references the old registry path
5. **Clean up secrets and env vars** that reference `gcr.io` — this is where phantom references like the Sentry DSN surface

The gotcha that catches most people: the URL structure adds a repository name between the project ID and image name. With GCR it was `gcr.io/PROJECT/IMAGE`. With Artifact Registry it's `REGION-docker.pkg.dev/PROJECT/REPO/IMAGE`. Miss that segment and you get confusing 403 errors.

## Template Debt Lesson

The Sentry secret issue is worth calling out separately. When you scaffold a new project from a deploy workflow template, every secret reference is a future failure waiting to happen. The workflow ran fine for months because GitHub Actions silently passes empty strings for missing secrets. It only broke when the empty value hit a code path that actually validated it.

The fix is boring: audit your workflow secrets after scaffolding. Run `grep -r 'secrets\.' .github/workflows/` and verify every one exists in your repo settings. Five minutes of checking beats debugging at 1 AM.

## Session Stats

| Metric | Value |
|--------|-------|
| **Commits** | 2 |
| **Time span** | 4 minutes (1:24 AM - 1:28 AM) |
| **Repo** | hustle |
| **Files changed** | `.github/workflows/deploy.yml` |
| **Net change** | 133 insertions, 2 deletions |
| **Root cause** | GCR deprecation + template copy-paste debt |

## Related Posts

- [Deploying Next.js 15 to Google Cloud Run](/posts/deploying-nextjs-15-google-cloud-run-custom-domain-ssl/) — The original Cloud Run deployment this workflow serves
- [SSE + Cloud Run: Every Platform Lies](/posts/sse-cloud-run-every-platform-lie/) — Another Cloud Run gotcha discovered the hard way
- [HustleStats Production Auth Debugging](/posts/hustlestats-production-auth-debugging-nextauth-prisma/) — A deeper debugging session on the same project, three days later
