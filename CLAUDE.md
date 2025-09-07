# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo static site blog using the Beautiful Hugo theme. The blog is configured to showcase technology, AI, and software development content.

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
# Create a new post
hugo new posts/my-new-post.md

# Create a new page
hugo new about.md
```

## Project Structure

The blog follows standard Hugo conventions with the Beautiful Hugo theme:

- **content/posts/** - Blog posts in Markdown format with Hugo front matter
- **public/** - Generated static site (do not edit directly, regenerated on build)
- **themes/beautifulhugo/** - Theme files (avoid modifying directly)
- **hugo.toml** - Main configuration file with site settings, menu structure, and social links
- **static/** - Static assets that will be copied as-is to public/
- **layouts/** - Custom layout overrides (currently empty, theme defaults used)

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

## Theme Customization

The Beautiful Hugo theme is installed as a Git submodule. To customize:
1. Override theme files by creating matching paths in the root layouts/ directory
2. Modify hugo.toml for configuration changes
3. Add custom CSS/JS in static/ directory

## Deployment Notes

The site builds to the `public/` directory. The current setup includes multiple social links and professional profiles configured in hugo.toml under `[[Params.social]]` sections.