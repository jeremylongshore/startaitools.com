# Broken Links Priority Fix List

Generated: 2025-10-20
Total URLs tested: 767
Working links: 555
Broken links: 212

## Priority 1: Critical Broken Links (User-Facing Content)

### 1. Broken GitHub Repository Link
- **URL**: `https://github.com/jeremylongshore/prompts-intent-solutions`
- **Status**: 404 (Repository not public or doesn't exist)
- **Location**: `content/projects.md`
- **Fix**: Remove this section or update to correct URL

### 2. Broken Prompts Intent Solutions GitHub Pages
- **URL**: `https://jeremylongshore.github.io/prompts-intent-solutions/`
- **Status**: 404 (GitHub Pages not configured or repo not public)
- **Location**: `content/projects.md`
- **Fix**: Remove link or publish GitHub Pages if repo exists locally

### 3. Broken ArXiv Paper Link
- **URL**: `https://arxiv.org/abs/2510.04618)**`
- **Location**: `content/research.md`
- **Fix**: Verify correct ArXiv paper ID (may be incorrect number)

## Priority 2: Broken Internal Blog Post Links

These are cross-references to blog posts that may have been moved or removed:

### Posts with Wrong Slugs (need slug correction):
1. `https://startaitools.com/posts/ssh-deb-grep-comprehensive-guide/` → 404
2. `https://startaitools.com/posts/advanced-linux-security-ssh-debian-text-processing/` → 404
3. `https://startaitools.com/posts/hybrid-ai-stack-reduce-costs-60-80-percent-intelligent-routing/` → 404
4. `https://startaitools.com/posts/building-254-table-bigquery-schema-72-hours/` → 404
5. `https://startaitools.com/posts/diagnosticpro-complete-evolution-analysis/` → 404
6. `https://startaitools.com/posts/diagnosticpro-case-study/` → 404
7. `https://startaitools.com/posts/terraform-complete-learning-guide-infrastructure-as-code/` → 404

### Posts in /startai/ subdirectory (need full path):
Multiple links like `https://startaitools.com/posts/startai/[post-name]/` → 404

These posts exist but URLs in cross-references are incorrect.

## Priority 3: LinkedIn Blocking (False Positives)

- **URL**: `https://linkedin.com/in/jeremylongshore`
- **Status**: 999 (LinkedIn bot protection, not actually broken)
- **No Action Required**: These are working links that LinkedIn blocks from automated checkers

## Priority 4: Microsoft Docs 404s (Low Priority)

Multiple Microsoft Learn URLs returning 404:
- Azure AI Services Content Safety docs
- Security best practices docs

**Note**: Microsoft frequently reorganizes docs. These may need manual verification if they're important.

## Priority 5: False Positives (Regex Issues)

The link checker incorrectly flagged these due to markdown syntax:
- `https://claudecodeplugins.io)**` (actually: `**[text](https://claudecodeplugins.io)**`)
- `https://github.com/jeremylongshore)**` (actually: `**[GitHub →](https://github.com/jeremylongshore)**`)

**No Fix Needed**: These links are working, just extracted incorrectly.

## Recommended Actions

### Immediate Fixes:
1. **projects.md**: Remove or update Prompts Intent Solutions section (broken GitHub links)
2. **research.md**: Verify ArXiv paper ID and fix
3. **Internal blog posts**: Audit cross-references and update URLs to match actual post slugs

### Audit Required:
1. Review all internal post cross-references
2. Check if moved/renamed posts have redirect rules in Netlify
3. Consider removing references to posts that no longer exist

### Low Priority:
1. Microsoft docs links (check manually if needed)
2. Example URLs in documentation (these are intentionally fake)
3. LinkedIn links (working despite 999 status)
