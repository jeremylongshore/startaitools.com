---
title: "Expanding Claude AutoBlog to 5 Platforms: Multi-Platform Blog Automation with Monospace Documentation"
date: 2025-09-27T19:30:00-06:00
draft: false
tags: ["claude-code", "automation", "hugo", "jekyll", "gatsby", "nextjs", "wordpress", "github-pages", "open-source"]
author: "Jeremy Longshore"
description: "How we expanded Claude AutoBlog SlashCommands from Hugo-only to supporting 5 major blogging platforms, added a monospace-themed GitHub Pages site, and learned about platform-agnostic command design."
---

Yesterday we open-sourced Claude AutoBlog SlashCommands - automated blog publishing commands for Claude Code. Today we got a simple request: "can u create this repo to be for multiple popular blog sites not just hugo that users can install and use on their own."

This is the story of expanding from Hugo-only to supporting Jekyll, Gatsby, Next.js, and WordPress - and adding a beautiful monospace documentation site in the process.

## The Challenge

The original commands (`/blog-startaitools` and `/blog-jeremylongshore`) were hardcoded for Hugo:
- Hugo-specific paths (`content/posts/`)
- Hugo build commands (`hugo --gc --minify --cleanDestinationDir`)
- YAML/TOML front matter specific to Hugo conventions
- Hugo deployment workflows (Netlify with Hugo config)

**The problem:** Developers using Jekyll, Gatsby, Next.js, or WordPress couldn't use these commands without significant rewriting.

**The goal:** Create platform-specific command templates that maintain the same core analysis logic but adapt to each platform's requirements.

## Phase 1: Pattern Analysis

First, I analyzed what was platform-agnostic vs. platform-specific in the existing Hugo commands:

**Universal patterns (keep everywhere):**
- Git history analysis since last post
- Complete conversation history review
- Cross-linking to related posts
- Draft review before publishing
- The "show the journey, not just the destination" philosophy

**Platform-specific variations:**
- Content directory structure
- Front matter format
- Build commands
- File naming conventions
- Deployment mechanisms

This became the blueprint: **Same analysis engine, different publishing adapters.**

## Phase 2: Creating Platform Commands

### Jekyll Command

Jekyll uses a date-prefixed naming convention: `_posts/YYYY-MM-DD-slug.md`

**Front matter format (lines 38-46):**
```yaml
---
layout: post
title: "Your Post Title"
date: 2025-MM-DD HH:MM:SS -0600
categories: [category1, category2]
tags: [tag1, tag2]
---
```

**Build command (line 56):**
```bash
bundle exec jekyll build
```

**Key customization:** Jekyll requires the `layout: post` field and uses `categories` instead of just `tags`.

### Gatsby Command

Gatsby supports multiple content patterns depending on setup:
- `gatsby-source-filesystem` with external markdown
- `gatsby-plugin-mdx` for MDX components
- Content layers like Contentlayer

**Content directory (line 6):**
```markdown
- **Git History**: Check commits since the most recent post date in your Gatsby `content/posts/` directory
```
Update to your actual Gatsby content location.

**Build command (line 56):**
```bash
npm run build
# or
gatsby build
```

The command includes notes about checking `gatsby-config.js` to find the actual content path configuration.

### Next.js Command

Next.js has TWO routing patterns:

**App Router (Next.js 13+):**
```
app/blog/[slug]/page.mdx
```

**Pages Router (Next.js 12):**
```
pages/blog/[slug].mdx
```

The command handles both:

```markdown
**Identify your routing style:**
- App Router: `app/blog/[slug]/page.mdx`
- Pages Router: `pages/blog/[slug].mdx`
- External content with next-mdx-remote: `content/posts/slug.md`
```

**Build and test:**
```bash
npm run build
# then test with
npm run start
```

### WordPress Command

WordPress was the most complex because it doesn't use local files - it publishes directly via API.

**Two publishing methods:**

**Option A: WP-CLI**
```bash
wp post create \
  --post_title="Post Title" \
  --post_content="$(cat post-content.md)" \
  --post_status=publish \
  --post_category="category-id" \
  --tags_input="tag1,tag2,tag3"
```

**Option B: REST API**
```bash
curl -X POST "https://yoursite.com/wp-json/wp/v2/posts" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Post Title",
    "content": "Post content",
    "status": "publish"
  }'
```

The WordPress command includes complete setup instructions for both methods, including how to generate application passwords and get category/tag IDs.

## Phase 3: Comprehensive Documentation

Created `docs/PLATFORM_SETUP.md` - a 400+ line guide covering:

**For each platform:**
- Prerequisites and installation
- Blog directory structure
- Command customization steps
- Front matter format examples
- Build command variations
- Deployment options
- Troubleshooting tips

**Example: Hugo Setup section**
```markdown
### Prerequisites
```bash
# Install Hugo (macOS)
brew install hugo

# Verify installation
hugo version  # Should be v0.100+
```

### Blog Structure
```
your-hugo-blog/
├── config.toml or hugo.toml
├── content/
│   └── posts/
├── themes/
└── public/
```
```

Each platform section follows the same structure - making it easy to find what you need.

## Phase 4: The Monospace Aesthetic

While working on multi-platform support, I cloned The Monospace Web framework by Oskar Wickström to improve the README visual design.

**The request:** "is there a way to make that page look better without flooding it with emojis"

**The solution:** Create a GitHub Pages site with monospace grid aesthetic.

### Cloning and Integrating

```bash
cd /home/jeremy/projects/repos
git clone https://github.com/owickstrom/the-monospace-web.git

# Copy CSS and JS to our repo
cp the-monospace-web/src/reset.css claude-AutoBlog-SlashCommands/docs/assets/css/
cp the-monospace-web/src/index.css claude-AutoBlog-SlashCommands/docs/assets/css/
cp the-monospace-web/src/index.js claude-AutoBlog-SlashCommands/docs/assets/js/
```

### Creating the GitHub Pages Site

Built `docs/index.html` with:

**Professional header table:**
```html
<table class="header">
  <tr>
    <td colspan="2" rowspan="2" class="width-auto">
      <h1 class="title">Claude AutoBlog Slash Commands</h1>
      <span class="subtitle">Automated blog publishing for developers</span>
    </td>
    <th>Version</th>
    <td class="width-min">v1.1.0</td>
  </tr>
  <tr>
    <th>Updated</th>
    <td class="width-min"><time>2025-09-27</time></td>
  </tr>
</table>
```

**ASCII art workflow diagram:**
```
┌─────────────────────────────────────────────────────────┐
│  1. Work on project                                     │
│     └─ Write code, solve problems, iterate              │
│                                                          │
│  2. Run command:  /blog-myblog                          │
│     └─ Claude analyzes git + conversation + files       │
│                                                          │
│  3. Review generated draft                              │
│     └─ Complete post with cross-links and SEO           │
│                                                          │
│  4. Approve                                             │
│     └─ Auto-publish: build, commit, push, deploy        │
│                                                          │
│  5. Live in 2 minutes                                   │
│     └─ Professional blog post on your site              │
└─────────────────────────────────────────────────────────┘
```

**Platform comparison table** with monospace-friendly styling.

**Tree view** of installed commands using the framework's tree class.

### The Monospace Grid

The framework uses a character-based grid system:
- Responsive in character-sized steps
- Maintains perfect alignment
- Tables auto-adjust to monospace
- Forms align to grid
- ASCII art integrates seamlessly

**Why it works for developer documentation:**
- Clean, distraction-free aesthetic
- Familiar to terminal users
- Semantic HTML
- Accessible and fast
- No JavaScript required for core functionality

## Phase 5: GitHub Repository Enhancements

### Badges and Shields

Added shields.io badges to README:
```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]
[![Claude Code](https://img.shields.io/badge/Claude_Code-v1.0.123+-blue.svg)]
[![Platform Support](https://img.shields.io/badge/Platforms-5-orange.svg)]
```

### One-Command Install

Created a copy-paste one-liner:
```bash
cd /tmp && git clone https://github.com/jeremylongshore/Claude-AutoBlog-SlashCommands.git && cp Claude-AutoBlog-SlashCommands/commands/*.md ~/.claude/commands/ && echo "✅ Installed! Choose a command to customize:" && ls -1 ~/.claude/commands/blog-*.md
```

Users can install all platform commands in 30 seconds.

### CONTRIBUTING.md

Created comprehensive contribution guidelines covering:
- How to report issues
- How to request features
- How to add new platform support
- Pull request process
- Testing requirements
- Code style guidelines
- Recognition for contributors

## What We Learned

### 1. Platform-Agnostic Design

The key insight: **Separate analysis logic from publishing mechanics.**

All platforms need:
- Context gathering (git, conversation, files)
- Content generation (title, body, cross-links)
- Quality control (review before publishing)

But each platform has unique:
- File structure
- Metadata format
- Build process
- Deployment flow

Designing commands this way means 80% of the code is shared conceptually, with 20% platform-specific adapters.

### 2. Documentation as Product

The monospace GitHub Pages site isn't just documentation - it's a product experience.

**Before:** Wall of text README with instructions buried.
**After:** Visual, navigable site with clear sections, examples, and aesthetic appeal.

This matters for open-source adoption. People judge repos in seconds.

### 3. The Power of Templates

By creating command templates rather than hardcoded commands, we made the project:
- **Extensible:** Anyone can add a new platform
- **Customizable:** Users adapt to their specific setup
- **Educational:** Templates teach command structure
- **Maintainable:** One fix applies to all platforms conceptually

### 4. Monospace for Developer UX

The Monospace Web framework taught us something: **Constraint breeds creativity.**

By constraining to a character grid:
- Designs become cleaner
- Content becomes more focused
- Accessibility improves naturally
- Maintenance becomes simpler

Perfect for developer documentation.

### 5. Command Discovery Quirks

We hit an interesting Claude Code behavior: **commands register dynamically during sessions.**

Created `/blog-both-sites` command but got "Unknown slash command" error. Solution: Restart Claude Code completely.

This is important for users: **After installing commands, restart Claude Code.**

## The Results

**Repository now includes:**
- 6 command templates (2 Hugo examples + 4 platform templates)
- 400+ line platform setup guide
- Monospace GitHub Pages site (904 lines across 5 files)
- Comprehensive CONTRIBUTING.md
- One-command install script
- Platform comparison table
- Multiple deployment options documented

**Commits today:**
```
2cfb80c feat: add monospace-themed GitHub Pages site
d5c3633 feat: add multi-platform support for Jekyll, Gatsby, Next.js, and WordPress
5fb6d23 fix: correct broken documentation links in README
```

**New capabilities:**
- Jekyll users can automate blog posts
- Gatsby developers can use the same workflow
- Next.js projects (both routing styles) supported
- WordPress sites via WP-CLI or REST API
- Beautiful documentation site live on GitHub Pages

## What's Next

**Potential additions:**
- **Astro** support (growing static site generator)
- **11ty** template (popular among JAMstack devs)
- **Ghost** integration (headless CMS)
- **Medium** cross-posting (via API)
- **Dev.to** syndication support

**Community contributions:**
- Platform-specific customizations
- Theme-specific adaptations
- Deployment workflow variations
- Testing frameworks

## Try It Yourself

**Install in 30 seconds:**
```bash
cd /tmp && git clone https://github.com/jeremylongshore/Claude-AutoBlog-SlashCommands.git && cp Claude-AutoBlog-SlashCommands/commands/*.md ~/.claude/commands/ && echo "✅ Installed!" && ls -1 ~/.claude/commands/blog-*.md
```

**Choose your platform:**
- Hugo: `blog-hugo-technical.md`
- Jekyll: `blog-jekyll-technical.md`
- Gatsby: `blog-gatsby-technical.md`
- Next.js: `blog-nextjs-technical.md`
- WordPress: `blog-wordpress-technical.md`

**Customize for your blog, then:**
```bash
cd ~/projects/your-project
/blog-yoursite
```

**View the monospace docs:**
https://jeremylongshore.github.io/Claude-AutoBlog-SlashCommands/

## Related Posts

- [Building Custom Claude Code Slash Commands: The Complete Implementation Journey](/posts/building-custom-claude-code-slash-commands-complete-journey/) - Original implementation
- [Open-Sourcing the Blog Automation System: Claude-AutoBlog-SlashCommands Repository](/posts/open-sourcing-claude-autoblog-slashcommands-repository/) - Initial release announcement
- [Complete Hugo Site Operations Guide: From Content to Production](/posts/complete-hugo-site-operations-guide/) - Hugo-specific workflows

---

**Repository:** https://github.com/jeremylongshore/Claude-AutoBlog-SlashCommands
**License:** MIT
**Credits:** Monospace theme by [Oskar Wickström](https://github.com/owickstrom/the-monospace-web)