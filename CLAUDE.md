# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo-based marketing website for Intent Solutions Inc., a business focused on deploying AI solutions. The site uses the Archie theme and is deployed on Netlify.

## Commands

### Development
```bash
# Start local development server
hugo server -D

# Start server with drafts disabled (production-like)
hugo server

# Build the site
hugo --gc --minify

# Build with cache clearing (for Netlify deployments)
hugo --gc --minify --cleanDestinationDir
```

### Testing & Preview
```bash
# Build for production preview
hugo --gc --minify --enableGitInfo

# Build with future-dated content visible
hugo --gc --minify --buildFuture
```

## Architecture & Structure

### Configuration
- **Main config**: `hugo.toml` - Core Hugo settings, theme configuration, build settings
- **Social & Menu**: Social links and navigation menu configured in hugo.toml
- **Netlify config**: `netlify.toml` - Build commands, redirects, headers, cache control

### Content Organization
- **Content**: `content/` - All site content
  - Blog posts in `posts/`
  - Static pages (about, contact, projects)
- **Theme**: `themes/archie/` - Archie theme files (Git submodule)
- **Assets**: `assets/` - Custom CSS/JS overrides
- **Static**: `static/` - Static files served directly

### Key Integration Points
- **Social Links**: GitHub, Twitter, LinkedIn, Email configured in hugo.toml
- **Menu Structure**: Home, Blog, Projects, About, Contact
- **Deployment**: Netlify with automatic deployments

### Theme Configuration
- **Theme**: Archie - minimal, clean blog theme
- **Mode**: Auto (supports dark/light mode switching)
- **Site Title**: Intent Solutions Inc
- **Subtitle**: "Deploy AI solutions in days, not months"
- **CDN**: Disabled (useCDN = false)

### Build & Deployment
- Hugo version: Latest (configured in netlify.toml)
- Automatic deployment via Netlify on git push
- Build commands: `hugo --gc --minify --cleanDestinationDir`
- Pagination: 10 posts per page