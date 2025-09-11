# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo static site portfolio and blog using the Hermit v2 theme. The site serves as a professional portfolio for an AI Engineer & Speed DevOps Specialist, featuring project showcases, work experience, and technical blog posts.

## Key Commands

### Local Development
```bash
# Start local development server with live reload
hugo server -D  # -D flag includes draft posts

# Start server without drafts
hugo server
```

### Building the Site
```bash
# Build static site to public/ directory
hugo

# Build including drafts
hugo -D
```

### Content Management
```bash
# Create a new blog post
hugo new content/en/blogs/my-new-post.md

# Create a new page
hugo new about.md
```

## Project Structure

The site follows standard Hugo conventions with the Hermit v2 theme:

- **content/en/blogs/** - Blog posts in Markdown format
- **content/en/** - Main content pages (about.md, contact.md, etc.)
- **data/en/** - Data files for dynamic content (author.toml, experience.toml, projects.toml)
- **public/** - Generated static site (do not edit directly, regenerated on build)
- **themes/hermit-v2/** - Theme files (avoid modifying directly)
- **hugo.toml** - Main configuration file with site settings, menu structure, and social links
- **static/** - Static assets that will be copied as-is to public/
- **layouts/** - Custom layout overrides (currently empty, theme defaults used)
- **netlify.toml** - Netlify deployment configuration

## Working with Content

Posts use Hugo front matter format:
```markdown
+++
title = 'Post Title'
date = 2025-09-06T10:54:30-05:00
draft = false
+++
```

The blog is configured with:
- Reading time and word count display
- Syntax highlighting with highlight.js
- Social sharing buttons
- Related posts functionality

## Site Configuration

The site uses Hermit v2 theme with professional portfolio features:
- **Theme colors**: themeColor = "#494f5c", accentColor = "#018472"
- **Features enabled**: Related posts, code copy button, reading time, social sharing, scroll to top
- **Social links**: GitHub, X (Twitter), LinkedIn, Email configured in hugo.toml
- **Menu structure**: Home, About, Resume, Projects, Skills, Posts, Contact

## Theme Customization

The Hermit v2 theme is installed in themes/hermit-v2/. To customize:
1. Override theme files by creating matching paths in the root layouts/ directory
2. Modify hugo.toml for configuration changes
3. Add custom CSS/JS in static/ directory
4. Update data files in data/en/ for portfolio content

## Deployment

The site deploys automatically to Netlify:
- **Build command**: `hugo` (defined in netlify.toml)
- **Publish directory**: `public/`
- **Hugo version**: 0.149.1
- **Domain**: jeremylongshore.com with HTTPS redirect
- **Live URL**: https://jeremylongshore.com