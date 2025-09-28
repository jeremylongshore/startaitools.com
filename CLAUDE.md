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
# New blog post
hugo new posts/my-blog-post.md

# Create pages in content root (avoid if possible - prefer editing existing)
hugo new about.md
hugo new contact.md

# Test content with drafts
hugo server -D --bind 0.0.0.0
```

### Testing & Validation
```bash
# No automated tests - manual preview required
hugo server -D  # Test locally before deploying

# Validate HTML and check for broken links
hugo --gc --minify --cleanDestinationDir  # Production build check

# Test with Netlify dev environment
netlify dev  # Simulates production environment locally
```

### Git Workflow with Submodules
```bash
# Clone with submodules (required for Archie theme)
git clone --recursive https://github.com/jeremylongshore/startaitools.com.git

# Update theme submodule when needed
git submodule update --remote --merge

# Standard commit flow
git add .
git commit -m "feat: Description of changes"
git push origin master
```

## High-Level Architecture

**StartAITools.com** is a professional blog and knowledge center built with Hugo (v0.150.0) and the Archie theme. It serves as intent solutions io's content platform focused on AI development insights and technical expertise.

### Site Configuration

**Theme**: Archie theme (minimalist blog theme)
- Located at `themes/archie/` (git submodule)
- Auto light/dark mode switching
- Clean, professional blog layout
- Custom CSS in `static/css/custom.css`

**Content Focus**: intent solutions io blog platform
- Tagline: "Deploy AI solutions in days, not months"
- Business blog with technical content
- AI development insights and guides
- Professional project showcases

### Smart Glossary System
**Key Feature**: Auto-linking 1,855+ technical terms without manual markup
- **Location**: `/static/data/glossary.json` (glossary data)
- **Implementation**: `/static/js/tech-glossary-simple.js` (auto-detection)
- **Functionality**: Automatically detects and links technical terms across all content
- **UI**: Clean hover tooltips with definitions
- **Performance**: Lightweight JavaScript, no impact on page speed

### Key Directories

- `content/posts/` - Blog articles (28+ posts covering AI development, tech evolution, architecture patterns)
- `content/` - Static pages (about.md, contact.md, projects.md, research.md, resume.md, _index.md)
- `themes/archie/` - Archie theme (git submodule)
- `static/css/` - Custom CSS (main.css, custom.css)
- `static/js/` - Custom JavaScript (theme-toggle.js, layout-selector.js)
- `public/` - Generated site (never edit directly)

### Navigation Structure

Main menu configured in `hugo.toml`:
1. Home (/)
2. Posts (/posts) - Main blog content
3. About (/about) - Company information
4. Research (/research) - Research content
5. Projects (/projects) - Project showcases
6. Contact (/contact) - Contact information

### Deployment Flow

1. Content changes pushed to master branch
2. Netlify webhook triggered
3. Build command: `hugo --gc --minify --cleanDestinationDir`
4. Site deployed to startaitools.com

### Front Matter Format

All content uses YAML front matter:
```yaml
---
title: "Post Title"
date: 2025-09-18T10:00:00-06:00
draft: false
tags: ["ai", "development"]
author: "Jeremy Longshore"
---
```

**Static pages** (about, contact, etc.):
```yaml
---
title: "Page Title"
description: "Page description for SEO"
---
```

## Content Management

### Blog Posts
- Located in `content/posts/`
- 28+ comprehensive posts covering technical topics: AI development, architecture patterns, system evolution
- Professional tone with technical depth and real-world metrics
- Front matter format: YAML with title, date, draft, tags, author
- Recent additions (September 2025): Hugo operations guide, Speed DevOps methodology, DiagnosticPro platform architecture, career transition stories, glossary management systems
- Examples: AI engineering curriculum, transformer deployment, multi-agent architecture, $500K revenue case studies

### Static Pages
- About page: Company information and mission
- Contact page: Professional contact information
- Projects page: Portfolio of work and case studies
- Research page: Research content and findings
- Resume page: Professional background

## Netlify Configuration

Advanced deployment setup in `netlify.toml`:
- **Hugo Version**: 0.150.0 (production), 0.149.1 (previews)
- **Build optimizations**: `--gc --minify --cleanDestinationDir`
- **Security headers**: X-Frame-Options, X-XSS-Protection, CSP
- **Caching**: Aggressive caching for static assets (1 year)
- **Redirects**: HTTP to HTTPS, www to non-www
- **Preview builds**: Include future posts for testing

## Recent Updates (September 2025)

### Content Expansion
- **6 new comprehensive blog posts** added (32,000+ words total)
- **Hugo Site Operations Guide** - Production management workflows
- **Career Journey Post** - Marine Corps to AI founder transition
- **DiagnosticPro Architecture** - $500K+ revenue platform case study
- **Speed DevOps Methodology** - 48-72 hour deployment framework
- **Glossary Management** - Auto-linking 1,855+ technical terms
- **Founder's Log Continuation** - Mobile-first development workflows

### Technical Improvements
- **Theme Migration** - Completed switch to Archie theme from Hugo Book
- **Documentation Updates** - All references updated to reflect Archie theme
- **Content Structure** - Improved organization and cross-linking
- **SEO Optimization** - Enhanced meta descriptions and tagging

## Common Issues & Fixes

### Date Display Issue
Static pages (about, contact, projects, research, resume) show "Posted on Jan 1, 1" due to missing date in front matter.

**Fix**: Add proper date to static pages:
```yaml
---
title: "Page Title"
date: 2025-01-01T00:00:00-06:00
description: "Page description for SEO"
---
```

### Analytics Setup
Replace placeholder tracking ID in `hugo.toml` line 8:
```toml
googleAnalytics = "G-XXXXXXXXXX"  # Replace with actual GA4 tracking ID
```

### Updating Glossary Terms
Edit `/static/data/glossary.json` to add or modify technical terms:
```json
{
  "terms": [
    {
      "term": "your-term",
      "definition": "Clear explanation of the technical concept",
      "category": "AI/ML"
    }
  ]
}
```
Changes take effect immediately on next site build.

### Build Performance
Hugo build is optimized for production deployment:
- Build time: ~2.5 seconds (despite 28+ posts)
- Optimization flags: `--gc --minify --cleanDestinationDir`
- No package.json or npm dependencies required
- Static asset caching: 1 year via Netlify headers

## Important Notes

1. **Never edit public/** - This directory is auto-generated by Hugo
2. **Test locally first** - Always run `hugo server -D` before committing
3. **Theme is Archie** - Minimalist blog theme with auto light/dark mode
4. **SEO configured** - Meta descriptions, Open Graph, structured data
5. **Analytics ready** - GA4 configured, needs tracking ID (replace G-XXXXXXXXXX)
6. **Mobile responsive** - Archie theme includes responsive design
7. **Content Focus** - Technical depth with real business metrics and case studies
8. **No automated testing** - Manual preview and validation required
9. **Auto-deployment** - All pushes to master trigger Netlify build
10. **Custom styling** - Theme customizations in `/assets/_custom.scss`