+++
title = 'Intent Catalog: Six Phases from Empty Repo to Production Control Plane'
slug = 'intent-catalog-six-phases-control-plane'
date = 2026-01-15T10:00:00-06:00
draft = false
tags = ["intent-catalog", "airtable", "github-api", "control-plane", "ccpi", "quality-scoring"]
categories = ["Development Journey"]
description = "Building the intent-catalog control plane through six phases: catalog structure, Airtable schema, GitHub-to-Airtable sync, multi-repo config, doc linkage with quality scoring, and production hardening. Plus CCPI 100-point scoring integration."
+++

Sixteen commits, all in the intent-catalog repo. The project went from an empty directory to a production control plane in a single day, built through six deliberate phases.

## Why a Catalog

Intent Solutions runs a dozen active repositories. Each has its own conventions, its own deployment pipeline, its own documentation style. The intent-catalog is the central registry that knows what exists, where it lives, how healthy it is, and what documentation covers it.

Without it, answering "which repos have stale CI?" or "which projects lack a CLAUDE.md?" required manually checking each one. The catalog makes those questions queryable.

## Phase 1: Catalog Structure

The foundation is a YAML-based catalog format. Each entry describes a repository with structured metadata:

```yaml
- name: git-with-intent
  repo: intentsolutions/git-with-intent
  status: active
  tier: core
  stack: [typescript, docker, github-actions]
  docs: [CLAUDE.md, README.md, CONTRIBUTING.md]
```

The schema enforces required fields (name, repo, status) and validates optional fields against known enums. A JSON Schema file provides IDE autocomplete and CI validation.

## Phase 2: Airtable Schema

The Airtable base mirrors the YAML catalog with linked tables:

- **Repositories** -- one row per repo, all metadata fields
- **Documentation** -- one row per doc file, linked to its repo
- **CI Status** -- latest pipeline results, linked to its repo
- **Quality Scores** -- CCPI scoring results, linked to its repo

The schema uses Airtable's linked record fields so that a single repo view shows all its docs, CI status, and quality scores inline.

## Phase 3: GitHub-to-Airtable Sync

A Node.js sync script pulls repository metadata from the GitHub API and upserts it into Airtable. The sync handles:

- Repository creation/archival detection
- Branch protection status
- Latest commit date and author
- Open PR and issue counts
- CI workflow status (passing/failing/none)

The sync runs idempotently -- running it twice produces the same state. Airtable records use the GitHub repo full name as a natural key, so upserts work without tracking internal IDs.

## Phase 4: Multi-Repo Config

The catalog needed to work across repos with different config patterns. Some repos use `package.json` scripts. Some use Makefiles. Some use `netlify.toml`. Some use all three.

The config discovery module scans each repo for known config files and normalizes them into a common schema. The output answers: "what build command does this repo use?" and "what deployment target does this repo use?" regardless of how the repo is structured.

## Phase 5: Doc Linkage and Quality Scoring

This is where the CCPI 100-point scoring system plugs in. Each repository gets scored across ten dimensions:

- Documentation completeness (CLAUDE.md, README, CONTRIBUTING, LICENSE)
- CI/CD presence and green status
- Dependency freshness (latest vs. current versions)
- Test coverage indicators
- Security scanning presence
- Branch protection rules
- Release tagging discipline
- Code review enforcement
- Issue tracking usage
- Deployment automation

Each dimension scores 0-10. The composite CCPI score gives a single number for "how production-ready is this repo?" The scoring runs as part of the sync pipeline, so scores update automatically.

## Phase 6: Production Hardening

The final phase added error handling, retry logic, rate limiting for the GitHub API (5,000 requests/hour for authenticated calls), and structured logging. The sync script gained a `--dry-run` mode that shows what would change without touching Airtable.

A GitHub Actions workflow runs the sync daily at 06:00 UTC. Failures post to a Slack webhook.

## Operations Hub CRM Integration

The catalog feeds into the Operations Hub, which is the CRM layer for Intent Solutions. When a repo's CCPI score drops below 70, it creates a task in the CRM. When a repo hasn't had a commit in 30 days, it flags it for review. The catalog is the data source; the CRM is the action layer.

## What Shipped

| Phase | Deliverable |
|-------|-------------|
| 1 | YAML catalog format + JSON Schema |
| 2 | Airtable base with 4 linked tables |
| 3 | GitHub-to-Airtable sync script |
| 4 | Multi-repo config discovery |
| 5 | CCPI 100-point quality scoring |
| 6 | Error handling, retries, daily cron |

Sixteen commits for a complete control plane. The catalog now tracks 14 repositories with automated health scoring.

## Related Posts

- [Beads Rollout: Twenty-Two Repos and Org Governance](/posts/beads-rollout-twenty-two-repos-org-governance/) -- the org-wide governance initiative that the catalog supports
- [git-with-intent v0.9 to v0.10: Docker Upgrades and Strategic Research](/posts/git-with-intent-v090-v0100-docker-upgrades/) -- one of the repos tracked by this catalog
- [Enterprise Documentation Transformation](/posts/enterprise-documentation-transformation-git-native-taskwarrior-workflows/) -- earlier documentation standardization work across repos
