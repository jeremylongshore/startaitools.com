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

**StartAITools.com** is a professional knowledge center built with Hugo (v0.150.0) and the default Hugo Book theme. It serves as a public resource for AI development tools and guides, featuring:

- **Academic Research Guide**: Comprehensive 2025 guide with AI tools comparison
- **Professional Templates**: Documentation templates for development workflows
- **Smart Glossary System**: 1,855 auto-linking technical terms with hover tooltips
- **Simplified Navigation**: Clean index page for easy content discovery
- **Search**: Built-in Hugo Book search functionality
- **Auto-deployment**: Pushes to master automatically deploy via Netlify

### Key Directories

- `content/docs/` - Main knowledge center with 11 sections (getting-started, ai-ml, architecture, blog, resources, security, templates, workflow, glossary, guides, index)
- `content/posts/` - Blog articles
- `static/js/` - Custom JavaScript (tech-glossary-simple.js, layout-selector.js)
- `static/data/` - Glossary data (glossary.json with 1,855 terms)
- `assets/` - Custom SCSS (_custom.scss for theme overrides)
- `tasks/` - PRDs and task lists using the templates
- `ai-dev-tasks/` - Documentation template source files
- `themes/hugo-book/` - Theme (git submodule)
- `public/` - Generated site (never edit directly)

### Current Configuration (September 2025)

**Theme**: Official Hugo Book v11.0.0 (default/unmodified)
- Creator: Alex Shpak (original theme author)
- Installation: Git submodule (proper method)
- Minimal professional styling only
- Blue hyperlinks (#3b82f6) for readability
- Auto light/dark mode switching maintained

**Content Focus**: Public knowledge resources
- Academic Research Guide 2025 with AI tools comparison
- Professional development templates
- No project documentation (users directed to GitHub)

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