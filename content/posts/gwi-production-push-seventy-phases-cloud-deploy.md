+++
title = 'Production Push: 70 Phases, Cloud Deploy, and the Docker Build Gauntlet'
slug = 'gwi-production-push-seventy-phases-cloud-deploy'
date = 2025-12-18T10:00:00-06:00
draft = false
tags = ["git-with-intent", "opentofu", "gcp", "docker", "ci-cd", "devops"]
categories = ["Development Journey"]
description = "32 commits pushing git-with-intent from phases 32-70: OpenTofu migration, GCP deployment with Workload Identity Federation, and multiple Docker build fix iterations."
+++

The previous three days built the product. December 18th was about making it run somewhere that isn't my laptop.

Thirty-two commits spanning phases 32 through 70. The work falls into three buckets: infrastructure-as-code, cloud deployment, and the surprisingly painful process of getting Docker builds to actually work.

## OpenTofu Migration

git-with-intent's infrastructure was defined in Terraform. On December 18th it moved to OpenTofu.

The migration itself was uneventful. OpenTofu is a fork of Terraform with compatible syntax. Replace `terraform` with `tofu` in your commands, update the CI workflow, done. The state file format is identical. No resource recreation needed.

The reason for migrating was licensing. HashiCorp moved Terraform to BSL 1.1 in August 2023. OpenTofu is the Linux Foundation fork that remains open source under MPL 2.0. For a product that might itself ship under BSL, having the infrastructure tooling on a clear open-source license avoids awkward questions about license compatibility.

The OpenTofu configuration manages:
- GCP project setup and API enablement
- Cloud Run services for each microservice
- Cloud SQL (PostgreSQL) for persistent storage
- Redis (Memorystore) for caching and rate limiting
- IAM bindings with least-privilege service accounts
- Artifact Registry for Docker images

## GCP Deployment with Workload Identity Federation

The deployment pipeline uses GitHub Actions to build, push, and deploy to GCP. The authentication uses Workload Identity Federation instead of service account keys.

WIF lets GitHub Actions authenticate to GCP without storing a JSON key file in GitHub Secrets. Instead, GitHub's OIDC token (which Actions provides automatically) is exchanged for a short-lived GCP access token. No long-lived credentials. No key rotation. No risk of leaked key files.

Setting up WIF requires:
1. A Workload Identity Pool in GCP
2. A Provider configured for GitHub's OIDC issuer
3. A service account with the permissions the workflow needs
4. An IAM binding that maps the GitHub repo to the service account

The IAM binding is the security boundary. It specifies exactly which GitHub repository and branch can assume which service account. A compromised fork can't authenticate because the binding references the canonical repo.

This was straightforward to configure but required four commits to get right. The first attempt had the wrong audience claim in the OIDC configuration. The second attempt had the service account bound to the wrong Workload Identity Pool. The third attempt worked for `docker push` but failed on `gcloud run deploy` because the service account was missing the Cloud Run Admin role. Fourth commit fixed the IAM binding.

Four commits for authentication. Not because it's hard. Because each step requires a deploy-test cycle that takes 3 minutes, and you can't test WIF locally.

## The Docker Build Gauntlet

This was the painful part of the day. Multiple iterations fixing Docker builds that worked locally but failed in CI or in Cloud Run.

**Iteration 1: Base image mismatch.** The Dockerfiles used `node:20-alpine` for the build stage and `node:20-slim` for the production stage. Alpine uses musl libc. Slim uses glibc. Native Node modules compiled in the build stage with musl won't run in the production stage with glibc. Fix: use the same base image for both stages.

**Iteration 2: Missing build arguments.** The API service reads its version from a build-time environment variable. The Dockerfile had `ARG VERSION` but the CI workflow wasn't passing `--build-arg VERSION=$TAG`. The service started but reported version "undefined" in health checks.

**Iteration 3: Package lockfile drift.** `npm ci` in the Docker build was failing because `package-lock.json` was out of sync with `package.json`. This worked locally because my local `node_modules/` had the right versions. Docker builds from scratch, so lockfile inconsistencies become build failures.

**Iteration 4: Prisma binary target.** The database layer uses Prisma. Prisma generates platform-specific query engine binaries. The binary generated on macOS (darwin-arm64) doesn't work in a Linux container (linux-musl). Fix: add `binaryTargets = ["native", "linux-musl-openssl-3.0.x"]` to the Prisma schema so both binaries get generated.

Four separate Docker build issues, each requiring a commit to fix. Each fix required a full CI run to validate because you can't reproduce the CI environment locally (or at least, not quickly enough to be worth it).

## CI Fixes

With the Docker builds working, the CI pipeline needed its own round of fixes:

- **Webhook public access.** The GitHub webhook receiver needs to be publicly accessible for GitHub to deliver events. Cloud Run services default to requiring authentication. Added `--allow-unauthenticated` to the webhook service's deploy command. Every other service stays authenticated.
- **Lint cleanup.** The CI pipeline runs ESLint on every PR. The rapid development of phases 9-70 accumulated lint warnings that didn't block local development but did block CI. One commit cleaned up unused imports, missing return types, and inconsistent spacing across all services.
- **Test timeout.** Integration tests that call real APIs were timing out in CI. The GitHub Actions runner has higher latency to GitHub's API than my local machine. Bumped the test timeout from 30 seconds to 60 seconds.

## DevOps Playbook

One commit created a DevOps playbook document covering:
- How to deploy a new version
- How to roll back a failed deployment
- How to rotate the WIF service account (you don't rotate it — you create a new one and update the binding)
- How to debug a Cloud Run service that won't start
- How to read structured logs in Cloud Logging

This document exists because future-me will forget how WIF works. Every deployment system needs a runbook. Writing it on the day you set it up is when the knowledge is freshest.

## Vertex AI SDK and License

Two final commits. The Vertex AI SDK integration adds the ability to use Google's models for intent analysis alongside OpenAI and Anthropic. It's a new provider in the connector framework — same interface, different backend.

The proprietary license commit added the Intent Solutions license to the repository. This is a separate license from the BSL 1.1 that covers the connector SDK. The core platform is proprietary. The SDK for building connectors is open.

## The Gap Between "Works" and "Runs in Production"

Phases 9-30 were features. Phases 32-70 were operations. The feature work was more interesting. The operations work was more necessary.

A product that runs on localhost and doesn't deploy is a hobby project. The 32 commits on December 18th closed that gap. Not elegantly — four Docker build iterations and four WIF authentication attempts are not elegant. But the end state is a product that deploys from a git push, runs on managed infrastructure, and has a runbook for when things go wrong.

---

## Related Posts

- [Feature Marathon: git-with-intent Phases 9 Through 30](/posts/gwi-feature-marathon-phases-nine-through-thirty/) — The features this deployment infrastructure supports
- [Deploying Next.js 15 to Google Cloud Run with Custom Domain and SSL](/posts/deploying-nextjs-15-google-cloud-run-custom-domain-ssl/) — Similar Cloud Run deployment patterns on a different project
- [Terraform: Complete Learning Guide for Infrastructure as Code](/posts/terraform-complete-learning-guide-infrastructure-as-code/) — Background on the IaC approach that OpenTofu extends
