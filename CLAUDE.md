# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**StartAITools.com** - A comprehensive knowledge center and learning platform built with Hugo Book theme. This site serves as both a business presence for Intent Solutions Inc. and a technical knowledge repository documenting the AI development journey from experiments to production systems.

## Architecture

### Technology Stack
- **Static Site Generator**: Hugo v0.150.0 (Extended)
- **Theme**: Hugo Book (knowledge center layout)
- **Hosting**: Netlify (automatic deployment on push)
- **Search**: Built-in Hugo Book search
- **Domain**: startaitools.com
- **Repository**: github.com/jeremylongshore/startaitools.com

### Directory Structure
```
startaitools/
├── content/                    # All site content
│   ├── docs/                  # Knowledge center (main content)
│   │   ├── getting-started/   # Entry point for new users
│   │   ├── ai-ml/            # AI & machine learning guides
│   │   ├── architecture/      # System design patterns
│   │   ├── blog/             # Blog archives (founder logs)
│   │   ├── journey/          # Project evolution timeline
│   │   ├── resources/        # External resources & links
│   │   ├── security/         # Linux security guides
│   │   ├── templates/        # AI dev task templates
│   │   └── workflow/         # Development workflows
│   ├── posts/                 # Blog posts (main blog)
│   ├── glossary/             # Technical term definitions
│   └── [static pages]        # about.md, contact.md, etc.
├── tasks/                     # PRDs and task lists
├── ai-dev-tasks/             # Template source files
├── themes/hugo-book/         # Theme files (submodule)
├── static/                   # Static assets
├── public/                   # Generated site (DO NOT EDIT)
└── hugo.toml                 # Site configuration
```

## Common Commands

### Development
```bash
# Start local development server
hugo server -D --bind 0.0.0.0

# Start without drafts (production-like)
hugo server --bind 0.0.0.0

# Build for production
hugo --gc --minify --cleanDestinationDir
```

### Content Creation
```bash
# Create new documentation page
hugo new docs/section-name/page-title.md

# Create new blog post
hugo new posts/my-blog-post.md

# Create new glossary entry
hugo new glossary/term-name.md

# Create new PRD
Create manually in tasks/prd-feature-name.md
```

### Deployment
```bash
# Site auto-deploys on push to master
git add .
git commit -m "feat: Description of changes"
git push origin master

# Netlify will automatically build and deploy
```

## Content Organization

### Knowledge Center Structure (/docs/)

Each section has:
- `_index.md` - Section overview and navigation
- Individual content files - Detailed guides and documentation
- `bookCollapseSection: true` - Makes sidebar collapsible

**Current Sections:**
1. **Getting Started** (weight: 1) - New user onboarding
2. **AI & ML** (weight: 2) - Machine learning guides
3. **Architecture** (weight: 3) - System design patterns
4. **Blog Archives** (weight: 4) - Historical blog posts
5. **Journey** (weight: 5) - Project evolution story
6. **Resources** (weight: 6) - External links and tools
7. **Security** (weight: 7) - Linux security documentation
8. **Templates** (weight: 8) - AI dev task templates
9. **Workflow** (weight: 9) - Development workflows

### Blog Posts (/posts/)
- Technical articles and tutorials
- Project announcements
- Industry insights
- Personal journey posts

### PRDs and Tasks (/tasks/)
- Product Requirements Documents
- Task breakdowns from PRDs
- Architecture Decision Records (ADRs)
- Active development planning

## Key Features Implemented

### Navigation
- **Collapsible sidebar** - Each section expands/collapses independently
- **Weighted ordering** - Sections appear in logical order
- **Breadcrumbs** - Easy navigation path tracking
- **Table of contents** - Auto-generated for long pages

### Content Features
- **Cross-references** - Links between related content
- **Glossary integration** - Technical terms linked to definitions
- **Template library** - 22+ AI dev task templates
- **Real PRD examples** - Actual PRDs using the templates

### Search & Discovery
- **Full-text search** - Built into Hugo Book theme
- **Tag system** - Content categorization
- **Related content** - Suggested reading links

## Writing Guidelines

### Documentation Pages
```markdown
---
title: "Page Title"
weight: 10
bookToc: true
bookCollapseSection: false
tags: ["tag1", "tag2"]
description: "Brief description for SEO"
---

# Main Heading

Content here...

## Subheadings

More content...
```

### Blog Posts
```markdown
---
title: "Post Title"
date: 2025-09-14T10:00:00-06:00
draft: false
tags: ["ai", "development"]
categories: ["Technical", "Journey"]
author: "Jeremy Longshore"
description: "SEO description"
---

Post content...
```

### PRDs
Follow templates in `/ai-dev-tasks/create-prd.md`

## Important Files

### Configuration
- `hugo.toml` - Main site configuration
- `netlify.toml` - Deployment settings
- `.gitmodules` - Theme submodule reference

### Documentation
- `CLAUDE.md` - This file (AI assistant guidance)
- `README.md` - Public repository documentation
- `RELEASES.md` - Version history
- `CONTRIBUTING.md` - Contribution guidelines

### Templates
- `/ai-dev-tasks/*.md` - All documentation templates
- `/tasks/prd-*.md` - Example PRDs using templates

## Development Workflow

### Adding New Content
1. Choose appropriate section in `/content/docs/`
2. Create markdown file with proper front matter
3. Add cross-references to related content
4. Update section `_index.md` if needed
5. Test locally with `hugo server`
6. Commit and push to deploy

### Creating PRDs
1. Use template: `@ai-dev-tasks/create-prd.md`
2. Save in `/tasks/prd-feature-name.md`
3. Generate tasks: `@ai-dev-tasks/generate-tasks.md`
4. Track progress in task list

### Updating Navigation
1. Edit section `_index.md` files
2. Adjust `weight` for ordering
3. Set `bookCollapseSection` for collapsible behavior
4. Update `title` for sidebar display

## External Integrations

### GitHub Repositories
- **Main Site**: github.com/jeremylongshore/startaitools.com
- **Templates**: github.com/jeremylongshore/vibe-prd
- **Company**: github.com/jeremylongshore

### Deployment
- **Netlify**: Automatic deployment on push
- **Domain**: startaitools.com (configured in Netlify)
- **Build Command**: `hugo --gc --minify --cleanDestinationDir`
- **Publish Directory**: `public/`

## Best Practices

### Content Quality
- Write for learning - include definitions and context
- Cross-reference related topics
- Provide real examples and code
- Include "next steps" sections

### SEO Optimization
- Use descriptive titles and descriptions
- Include relevant tags
- Create comprehensive content
- Internal linking strategy

### Maintenance
- Regular content updates
- Fix broken links
- Update outdated information
- Archive old content appropriately

## Common Issues & Solutions

### Build Warnings
- "Reference not found" - Page doesn't exist yet (usually OK)
- "Image not found" - Missing image file in static/
- "No layout for json" - Expected for search index

### Local Development
- Use `--bind 0.0.0.0` for network access
- Clear `public/` if seeing stale content
- Check `hugo.toml` for configuration issues

## Future Enhancements

### Planned Features
- Smart glossary with auto-linking
- Interactive code examples
- Video tutorials section
- Newsletter integration
- User comments system

### Content Roadmap
- Complete all template documentation
- Add more project case studies
- Create video walkthroughs
- Expand glossary coverage
- Add more real PRD examples

---

**Last Updated**: September 14, 2025
**Maintained By**: Jeremy Longshore / Claude Code
**Purpose**: Comprehensive AI development knowledge center and learning platform