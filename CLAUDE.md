# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo-based marketing website for Start AI Tools, a business focused on AI implementation and consulting services. The site uses the Bigspring theme and is deployed on Netlify.

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
- **Parameters**: `config/_default/params.toml` - Site-wide parameters, social links, form actions
- **Netlify config**: `netlify.toml` - Build commands, redirects, headers, cache control

### Content Organization
- **Content**: `content/english/` - All English content (German disabled in config)
  - Homepage sections
  - Blog posts
  - Static pages (privacy, terms, etc.)
- **Theme**: `themes/bigspring/` - Bigspring theme files (Git submodule)
- **Assets**: `assets/` - Custom CSS/JS overrides
- **Static**: `static/` - Static files served directly

### Key Integration Points
- **Contact Form**: Formspree integration (configured in params.toml)
- **Analytics**: Google Analytics ready (ID in hugo.toml)
- **Deployment**: Netlify with automatic HTTPS redirects and cache headers

### Theme Customization
- Color scheme and fonts configured in `hugo.toml` under `[params.variables]`
- Primary color: `#4F46E5` (Indigo)
- Secondary color: `#7C3AED` (Purple)
- Font: Lato (Google Fonts)
- Dark/light mode switcher enabled

### Build & Deployment
- Hugo version: 0.149.1 (extended)
- Automatic deployment via Netlify on git push
- Cache busting configured for CSS/JS files
- Image optimization with Hugo pipes (quality: 90)