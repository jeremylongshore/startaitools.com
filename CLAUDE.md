# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo static site portfolio and blog using the Hermit v2 theme. The site serves as a professional portfolio for Jeremy Longshore, an AI Engineer & Speed DevOps Specialist, featuring project showcases, work experience, and technical blog posts. The site showcases DiagnosticPro platform work with 254 BigQuery tables, 226+ RSS feeds, and 500K+ processed records.

## Key Commands

### Local Development
```bash
# Start local development server with live reload
hugo server -D  # -D flag includes draft posts

# Start server without drafts
hugo server

# Start server accessible from external devices
hugo server -D --bind 0.0.0.0
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
# Create a new blog post (primary location)
hugo new posts/my-new-post.md

# Create a legacy-format blog post
hugo new content/en/blogs/my-new-post.md

# Create a new page
hugo new about.md
```

### Content Synchronization
```bash
# Sync selected content from Start AI Tools blog
./scripts/sync-startaitools.sh
```

## Project Structure

The site follows Hugo conventions with dual content structure and Hermit v2 theme:

- **content/posts/** - Primary blog posts location (11 published posts)
- **content/en/blogs/** - Legacy blog structure (maintained for compatibility)
- **content/** - Main static pages (about.md, contact.md, resume.md, projects.md, skills.md)
- **themes/hermit-v2/** - Hermit v2 theme (Git submodule, avoid modifying directly)
- **layouts/partials/** - Custom layout overrides for theme customization
- **static/** - Static assets (images, CSS, JS)
- **scripts/** - Utility scripts including content sync from Start AI Tools
- **public/** - Generated static site (auto-generated, never edit directly)
- **hugo.toml** - Site configuration with theme colors, menu structure, social links
- **netlify.toml** - Netlify deployment configuration (Hugo v0.149.1)

## Content Architecture

### Dual Content Structure
The site maintains two content locations for different purposes:
- **content/posts/** - Current primary location for new blog posts
- **content/en/blogs/** - Legacy structure maintained for compatibility

### Front Matter Format
Posts use TOML front matter format:
```toml
+++
title = 'Post Title'
date = 2025-09-06T10:54:30-05:00
draft = false
tags = ["ai", "programming", "startup"]
categories = ["Technology"]
author = "Jeremy Longshore"
+++
```

### Content Sync Integration
The site can sync select content from the sister site "Start AI Tools" using:
- **Script**: `scripts/sync-startaitools.sh`
- **Target directory**: `content/en/blogs/startai/`
- **Automatic attribution**: Adds canonical URLs and series tags
- **Image sync**: Copies images to `static/images/startai/`

## Site Configuration

### Theme Setup (Hermit v2)
- **Colors**: Primary "#494f5c", Accent "#018472"
- **Features**: Related posts, code copy buttons, reading time, social sharing, scroll to top
- **Typography**: Proper code highlighting with Pygments
- **Navigation**: 7-item menu (Home, About, Resume, Projects, Skills, Posts, Contact)

### Professional Portfolio Features
- **Author bio**: Configured in hugo.toml params.author
- **Social links**: GitHub, X/Twitter, LinkedIn, Email
- **SEO**: Meta descriptions, structured data, robots.txt enabled
- **Performance**: Optimized for Lighthouse 98+ scores

### Contact Information
- **Primary email**: jeremy@intentsolutions.io
- **Website**: jeremylongshore.com
- **Social handles**: @asphaltcowb0y (X), @jeremylongshore (GitHub/LinkedIn)

## Deployment & Environment

### Netlify Configuration
- **Build command**: `hugo` (standard build)
- **Publish directory**: `public/`
- **Hugo version**: 0.149.1 (locked in netlify.toml)
- **Environment**: Production with HTTPS redirect
- **Domain**: jeremylongshore.com

### Development Workflow
1. Create content in `content/posts/` for new posts
2. Use `hugo server -D` for local preview with drafts
3. Commit changes triggers automatic Netlify deployment
4. Optional: Sync content from Start AI Tools using sync script

## Theme Customization

### Override Strategy
- **Theme location**: `themes/hermit-v2/` (Git submodule)
- **Custom overrides**: Place in `layouts/` directory to override theme defaults
- **Custom partials**: Currently in `layouts/partials/` for specific customizations
- **Avoid direct theme modification**: Use Hugo's override system instead

### Asset Management
- **Static assets**: Place in `static/` directory
- **Images**: Use `static/images/` for blog images
- **Custom CSS/JS**: Add to `static/css/` or `static/js/`