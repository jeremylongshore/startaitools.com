# Step 3: Verify, Publish, and Dual-Publish

## 3a. Verify and publish to startaitools.com

```bash
# 1. Hugo build check
cd /home/jeremy/000-projects/blog/startaitools
hugo --buildFuture --gc --minify --cleanDestinationDir

# 2. Commit
git add content/posts/SLUG.md
git commit -m "feat: add blog post for YYYY-MM-DD — brief summary

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"

# 3. Push to master (NOT main — Netlify watches master)
git push origin master
```

## 3b. Dual-publish to tonsofskills.com/blog

Transform Hugo frontmatter to Astro YAML and copy:

```bash
/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/scripts/transform-hugo-to-astro.sh \
  /home/jeremy/000-projects/blog/startaitools/content/posts/SLUG.md \
  /home/jeremy/000-projects/claude-code-plugins/marketplace/src/content/blog-posts/SLUG.md
```

Commit to claude-code-plugins:
```bash
cd /home/jeremy/000-projects/claude-code-plugins
git add marketplace/src/content/blog-posts/SLUG.md
git commit -m "feat(blog): add SLUG to tonsofskills.com/blog

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
git push
```

## 3c. Syndicate to intentsolutions.io/field-notes (conditional)

Only if the post's tags include any of: `architecture`, `ai-agents`, `technical-leadership`, `vertex-ai`, `portfolio`, `multi-agent-systems`, `cost-optimization`, `google-cloud`, `infrastructure-as-code`, `cloud-architecture`, `ai-systems`, `infrastructure-automation`, `systems-architecture`, `ai-engineering`, `data-architecture`, `enterprise-automation`, `case-study`, `agent-orchestration`

```bash
/home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/scripts/sync-to-intentsolutions.sh \
  /home/jeremy/000-projects/claude-code-plugins/marketplace/src/content/blog-posts/SLUG.md
```

Commit to intent-solutions-landing:
```bash
cd /home/jeremy/000-projects/intent-solutions-landing/astro-site
git add src/content/field-notes/SLUG.md
git commit -m "feat(field-notes): add SLUG to intentsolutions.io/field-notes

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
git push
```
