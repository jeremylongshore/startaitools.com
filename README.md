# StartAITools.com

Professional knowledge center for AI development and implementation with smart glossary auto-linking.

## Overview

StartAITools.com is a comprehensive documentation hub built with Hugo and the Hugo Book theme. The site provides structured learning paths, templates, and resources for AI development teams. Features an intelligent glossary system that automatically links technical terms throughout the documentation.

## Tech Stack

- **Static Site Generator**: Hugo v0.150.0
- **Theme**: Hugo Book (git submodule) - Default theme with custom enhancements
- **Deployment**: Netlify (auto-deploy on push to master)
- **Domain**: startaitools.com
- **Analytics**: Google Analytics 4 (configured, needs tracking ID)

## Project Structure

```
startaitools/
├── content/          # Markdown content files
│   ├── docs/        # Main documentation (9 sections, 491 pages)
│   │   ├── ai-ml/
│   │   ├── architecture/
│   │   ├── blog/
│   │   ├── getting-started/
│   │   ├── glossary/
│   │   ├── resources/
│   │   ├── security/
│   │   ├── templates/
│   │   └── workflow/
│   ├── posts/       # Blog posts
│   └── _index.md    # Homepage
├── themes/          # Hugo themes
│   └── hugo-book/   # Book theme (submodule)
├── static/          # Static assets
│   ├── js/         # Custom JavaScript
│   │   ├── tech-glossary-simple.js  # Auto-linking glossary
│   │   └── layout-selector.js
│   └── data/       # Glossary data
│       └── glossary.json (400+ terms)
├── assets/          # SCSS customizations
│   └── _custom.scss # Theme overrides
├── ai-dev-tasks/    # 22+ documentation templates
├── tasks/           # Example PRDs and task lists
├── public/          # Generated site (gitignored)
└── netlify.toml     # Netlify configuration
```

## Key Features

### Smart Glossary System
- **Auto-linking**: Automatically detects and links 400+ technical terms
- **Hover tooltips**: Clean, professional tooltips with definitions
- **No manual tagging**: Works across all content without markup
- **Performance optimized**: Lightweight JavaScript implementation

### Content Organization
- **9 main sections** with hierarchical structure
- **22+ professional templates** for documentation
- **491 pages** of technical content
- **Collapsible navigation** for easy browsing
- **Full-text search** functionality

### Theme & Styling
- **Default Hugo Book theme** with minimal customization
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

## Recent Updates (September 14, 2025)

- ✅ Implemented smart glossary with 400+ terms
- ✅ Fixed hyperlink colors for readability
- ✅ Rolled back to default Hugo Book theme
- ✅ Configured Google Analytics
- ✅ Optimized build process
- ✅ Updated to Hugo 0.150.0

## Performance Metrics

- **Build time**: ~2.5 seconds
- **Pages**: 491
- **Static files**: 78
- **Aliases**: 192
- **Glossary terms**: 400+

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

© 2025 Intent Solutions Inc. All rights reserved.

## Support

For issues or questions, contact Jeremy Longshore or submit an issue to the GitHub repository.