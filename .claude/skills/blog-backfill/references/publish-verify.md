# Step 7: Verify the build + write the readiness sentinel (NO git)

## Read this first — the inversion (in force 2026-07-05)

**The skill no longer commits, pushes, dual-publishes, or syndicates.** A separate
deterministic land step — `scripts/blog/blog-land.sh`, pure bash, no LLM — does
all of that *after* it independently verifies the post is complete. Your job in
step 7 is only to:

1. prove the post builds, and
2. drop a **readiness sentinel** that attests "all gates passed, safe to publish."

If you `git commit`/`git push` here you re-introduce the exact failure this design
removes: a timeout mid-gates that leaves a half-published post and a dirty tree
that bricks the next day's run. **Do not run git in this step.**

Why this is safe: `blog-land.sh` re-checks the build, the classifier record, the
step-8 audit addendum, and this sentinel. If any are missing or the sentinel says
`ready:false`, it **quarantines** the post (moves it aside, restores a clean tree)
and alerts — it never publishes something half-baked.

## 7a. Verify the Hugo build

```bash
cd /home/jeremy/000-projects/blog/startaitools
hugo --buildFuture --gc --minify --cleanDestinationDir
```

Must exit 0. If it fails, **fix the post and rebuild**. Do not write the sentinel
until the build is green.

## 7b. Leave the post + decision record as UNCOMMITTED changes

The post lives at `content/posts/SLUG.md`; the classification + audit records are
appended to `methodology/decisions.jsonl`. Both stay **uncommitted** — the land
step `git add`s exactly those two paths and commits them atomically once verified.
Do not touch git.

## 7c. Write the readiness sentinel — LAST action, only if every gate passed

Write this **only if**: the Hugo build is green **AND** every required quality gate
for the tier returned `PASS` with no unresolved `BLOCK` (consistency for Tier 2+,
fact-check for Tier 3). If a gate `BLOCK`ed and you could not resolve it, write
`"ready": false` (or do not write the sentinel at all) — that tells the land step
to quarantine rather than publish. **A sentinel with `ready:true` is your explicit
attestation that this post is safe to ship.**

```bash
mkdir -p .blog-staging
cat > .blog-staging/DATE.intent.json <<'JSON'
{
  "date": "DATE",
  "slug": "SLUG",
  "ready": true,
  "tier": N,
  "generated_at": "ISO8601_NOW",
  "gates": { "build": "pass", "consistency": "pass|n/a", "fact_check": "pass|n/a" }
}
JSON
```

Replace `DATE`, `SLUG`, `N`, `ISO8601_NOW`, and the gate verdicts with real values.
The land step keys off `.ready`; the rest is audit context.

## What you do NOT do (the land step owns these)

- ❌ `git add` / `git commit` / `git push` to startaitools
- ❌ dual-publish to tonsofskills.com (`transform-hugo-to-astro.sh` + commit)
- ❌ syndicate to intentsolutions.io/field-notes
- ❌ append to `.crosspost-queue.json` or run `check-crosspost-queue.sh`
- ❌ email the social bundle / build the Ezekiel packet

All of the above run in `blog-land.sh` after a verified publish, tier-gated from
the tier recorded in `decisions.jsonl`. See `scripts/blog/blog-land.sh`.
