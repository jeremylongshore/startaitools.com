# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Server
```bash
# Start local development server with drafts
hugo server -D --bind 0.0.0.0

# Production-like preview (no drafts)
hugo server --bind 0.0.0.0
```

### Build for Production
```bash
# Optimized production build
hugo --gc --minify --cleanDestinationDir
```

### Content Creation
```bash
# New documentation page
hugo new docs/section/page-name.md

# New blog post
hugo new posts/my-blog-post.md

# New glossary entry
hugo new glossary/term-name.md
```

### Testing
```bash
# No automated tests - manual preview required
hugo server -D  # Test locally before deploying
```

## High-Level Architecture

**StartAITools.com** is a professional knowledge center built with Hugo (v0.150.0) and the default Hugo Book theme. It serves as a public learning resource for AI development tools, research, and professional templates, featuring:

- **Company Focus**: Intent Solutions Inc knowledge sharing platform (services at intentsolutions.io)
- **Academic Research Guide**: Comprehensive 2025 guide with AI tools comparison
- **Professional Templates**: 20+ documentation templates for development workflows
- **Smart Glossary System**: 1,855 auto-linking technical terms with hover tooltips
- **Enhanced Navigation**: Expand/collapse functionality with copy code buttons
- **Reorganized Content**: Proper directory structure (guides, reference, research)
- **Search**: Built-in Hugo Book search functionality

### Key Directories

- `content/docs/` - Main knowledge center with 13 sections:
  - `guides/` - AI tools guides (4 guides including Academic Research 2025)
  - `templates/` - Professional templates (20+ templates)
  - `reference/` - Reference sheets and cheatsheets
  - `research/` - Research and analysis content
  - `index/` - Site navigation and index
  - Plus: getting-started, ai-ml, architecture, blog, resources, security, workflow, glossary
- `content/posts/` - Blog articles (17 posts)
- `layouts/partials/docs/inject/` - Custom navigation enhancements
- `static/js/` - Custom JavaScript (tech-glossary-simple.js)
- `static/data/` - Glossary data (glossary.json with 1,855 terms)
- `assets/` - Custom SCSS (_custom.scss with copy buttons and navigation styling)
- `themes/hugo-book/` - Official Hugo Book theme (git submodule)
- `public/` - Generated site (never edit directly)

### Current Configuration (September 2025)

**Theme**: Official Hugo Book v11.0.0 (default/unmodified)
- Creator: Alex Shpak (original theme author)
- Installation: Git submodule (proper method)
- Minimal professional styling only
- Blue hyperlinks (#3b82f6) for readability
- Auto light/dark mode switching maintained

**Content Focus**: Intent Solutions Inc knowledge sharing platform
- Learning resources and research (NOT services - see intentsolutions.io)
- Academic Research Guide 2025 with AI tools comparison
- Professional development templates (20+ templates)
- Enhanced UX: Expand/collapse navigation, copy code buttons
- Zero broken links after reorganization

### Content Structure

Each documentation section has:
- `_index.md` with `bookCollapseSection: true` for collapsible navigation
- Individual content files with front matter (title, weight, tags, description)
- Weighted ordering (1-9) for logical flow

### Deployment Flow

1. Content changes pushed to master branch
2. Netlify webhook triggered
3. Build command: `hugo --gc --minify --cleanDestinationDir`
4. Site deployed to startaitools.com

### Front Matter Formats

**Documentation pages** use YAML:
```yaml
---
title: "Page Title"
weight: 10
bookToc: true
bookCollapseSection: false
tags: ["tag1", "tag2"]
---
```

**Blog posts** use YAML with date:
```yaml
---
title: "Post Title"
date: 2025-09-14T10:00:00-06:00
draft: false
tags: ["ai", "development"]
author: "Jeremy Longshore"
---
```

## Important Notes

1. **Never edit public/** - This directory is auto-generated
2. **Test locally first** - Always run `hugo server -D` before committing
3. **Glossary auto-links** - No manual linking needed for technical terms
4. **Theme is default** - Using Hugo Book default with minimal custom CSS
5. **GA needs setup** - Replace G-XXXXXXXXXX with actual tracking ID