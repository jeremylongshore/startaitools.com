# StartAITools.com

Professional knowledge center for AI development and implementation with smart glossary auto-linking.

## Overview

StartAITools.com is a comprehensive documentation hub built with Hugo and the Archie theme. The site provides structured learning paths, templates, and resources for AI development teams. Features an intelligent glossary system that automatically links technical terms throughout the documentation.

## Tech Stack

- **Static Site Generator**: Hugo v0.150.0
- **Theme**: Archie (git submodule) - Minimalist blog theme with custom enhancements
- **Deployment**: Netlify (auto-deploy on push to master)
- **Domain**: startaitools.com
- **Analytics**: Google Analytics 4 (configured, needs tracking ID)

## Project Structure

```
startaitools/
├── content/          # Markdown content files (100+ total)
│   ├── docs/        # Main documentation (13 sections)
│   │   ├── ai-ml/
│   │   ├── architecture/
│   │   ├── blog/
│   │   ├── getting-started/
│   │   ├── glossary/
│   │   ├── guides/      # AI tools & guides (4 guides)
│   │   ├── index/       # Site navigation
│   │   ├── reference/   # Reference sheets & cheatsheets
│   │   ├── research/    # Research & analysis
│   │   ├── resources/
│   │   ├── security/
│   │   ├── templates/   # Professional templates (20+ templates)
│   │   └── workflow/
│   ├── posts/       # Blog posts (17 articles)
│   ├── glossary/    # Glossary content
│   ├── learning/    # Learning resources
│   ├── library/     # Resource library
│   └── _index.md    # Homepage
├── themes/          # Hugo themes
│   └── hugo-book/   # Book theme (submodule)
├── static/          # Static assets
│   ├── js/         # Custom JavaScript
│   │   ├── tech-glossary-simple.js  # Auto-linking glossary
│   │   └── layout-selector.js
│   └── data/       # Glossary data
│       └── glossary.json (1,855 terms)
├── assets/          # SCSS customizations
│   └── _custom.scss # Theme overrides
├── ai-dev-tasks/    # 22+ documentation templates
├── tasks/           # Example PRDs and task lists
├── public/          # Generated site (gitignored)
└── netlify.toml     # Netlify configuration
```

## Key Features

### Smart Glossary System
- **Auto-linking**: Automatically detects and links 1,855 technical terms
- **Hover tooltips**: Clean, professional tooltips with definitions
- **No manual tagging**: Works across all content without markup
- **Performance optimized**: Lightweight JavaScript implementation

### Content Organization
- **13 documentation sections** with hierarchical structure
- **20+ professional templates** for development workflows
- **100+ pages** of technical content including reorganized guides
- **Simplified navigation** with expand/collapse functionality
- **Copy buttons** on all code blocks for easy use
- **Full-text search** functionality

### Theme & Styling
- **Archie theme** with minimal customization
- **Readable blue hyperlinks** (#3b82f6)
- **Clean tooltip styling** matching theme
- **Auto light/dark mode** switching
- **Responsive design** for all devices

## Development

### Local Development

```bash
# Start development server with drafts
hugo server -D --bind 0.0.0.0

# Production preview (no drafts)
hugo server --bind 0.0.0.0

# Build for production
hugo --gc --minify --cleanDestinationDir
```

### Creating Content

```bash
# Create a new documentation page
hugo new docs/section-name/page-name.md

# Create a new blog post
hugo new posts/my-post.md

# Create a new glossary term
hugo new glossary/term-name.md
```

### Git Workflow

```bash
# Clone with submodules
git clone --recursive https://github.com/jeremylongshore/startaitools.com.git

# Update theme submodule
git submodule update --remote --merge

# Standard commit flow
git add .
git commit -m "feat: Description of changes"
git push origin master
```

## Deployment

The site automatically deploys to Netlify when changes are pushed to the master branch.

### Netlify Configuration

- **Build Command**: `hugo --gc --minify --cleanDestinationDir`
- **Publish Directory**: `public`
- **Hugo Version**: 0.150.0
- **Auto-deploy**: Enabled on master branch

### Google Analytics Setup

Analytics is configured but needs a tracking ID:
1. Get your GA4 tracking ID (format: G-XXXXXXXXXX)
2. Update in `hugo.toml` line 8
3. Push changes to deploy

## Recent Updates (September 18, 2025)

### Major Content Expansion
- ✅ **6 new comprehensive blog posts** added (32,000+ words total)
- ✅ **Complete Hugo Site Operations Guide** - Production management workflows
- ✅ **Marine to AI Founder Journey** - Career transition story with business lessons
- ✅ **DiagnosticPro Platform Architecture** - $500K+ revenue case study with technical details
- ✅ **Speed DevOps Methodology** - 48-72 hour deployment framework
- ✅ **Glossary Management at Scale** - Auto-linking 1,855+ technical terms
- ✅ **Founder's Log: Mobile Development** - Mobile-first workflow innovations

### Technical Improvements
- ✅ **Theme Migration**: Completed switch from Hugo Book to Archie theme
- ✅ **Documentation Updates**: All references updated to reflect current architecture
- ✅ **Content Organization**: Enhanced structure with cross-linking
- ✅ **SEO Optimization**: Improved meta descriptions and tagging

## Performance Metrics

- **Build time**: ~2.5 seconds (maintained despite 32K+ word content addition)
- **Total pages**: 125+ (25+ blog posts, 100+ static pages)
- **Recent content**: 6 comprehensive blog posts (September 2025)
- **Content focus**: AI development, platform architecture, operations guides, career stories
- **Theme**: Archie (minimalist blog theme with auto light/dark mode)
- **SEO**: Optimized with structured data and cross-linking

## Common Tasks

### Update Glossary Terms
Edit `/static/data/glossary.json` to add or modify terms:
```json
{
  "terms": [
    {
      "term": "your-term",
      "definition": "Clear explanation",
      "category": "AI/ML"
    }
  ]
}
```

### Change Link Colors
Edit `/assets/_custom.scss` to modify styling:
```scss
a {
  color: #3b82f6; // Your color
}
```

## License

© 2025 intent solutions io. All rights reserved.

## Support

For issues or questions, contact Jeremy Longshore or submit an issue to the GitHub repository.# Cache bust: Wed Sep 17 09:10:00 CDT 2025
