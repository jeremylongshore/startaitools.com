# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo-based learning center and technical blog that Jeremy uses for personal education and knowledge building. The site serves as both a business presence for Intent Solutions Inc. and a comprehensive learning repository with interconnected technical guides. Content should be educational, with cross-references between related topics to facilitate learning.

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
- **Netlify config**: `netlify.toml` - Build commands (includes Pagefind indexing), redirects, headers, cache control

### Content Organization
- **Content**: `content/` - All site content
  - Blog posts in `posts/` (12 posts with comprehensive tags)
  - Static pages (about, contact, projects)
- **Theme**: `themes/archie/` - Archie theme files (Git submodule)
- **Assets**: `assets/` - Custom CSS/JS overrides (includes search.css)
- **Static**: `static/` - Static files served directly
- **Layouts**: `layouts/` - Custom template overrides (head.html for search, footer.html)

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
- Hugo version: 0.149.1 (configured in netlify.toml)
- Automatic deployment via Netlify on git push
- Build commands: `hugo --gc --minify --cleanDestinationDir && npx -y pagefind --site public`
- Pagination: 10 posts per page
- Search: Pagefind full-text search integrated (Ctrl+K to open)

### Features
- **Full-text search**: Pagefind indexes all content, accessible via Search link or Ctrl+K
- **Dark/Light mode**: Auto-switching based on user preference
- **Responsive design**: Mobile-friendly Archie theme
- **SEO optimized**: Comprehensive tags and meta descriptions on all posts

## Content Guidelines for Learning

### Educational Content Structure
When creating posts for Jeremy's learning:
- **Include definitions**: Define technical terms inline or create glossary sections
- **Cross-reference posts**: Link between related topics to build knowledge connections
- **Progressive complexity**: Start with fundamentals, link to advanced topics
- **Code examples**: Include real-world, runnable code examples
- **Visual aids**: Use diagrams and flowcharts where helpful
- **Exercises**: Add practice problems or challenges at the end of posts

### Recommended Learning Resources
For technical definitions and open-source textbooks:
- **The Linux Documentation Project** (TLDP): Comprehensive Linux guides and HOWTOs
- **GNU Manuals**: Official documentation for GNU tools (grep, bash, etc.)
- **NIST Glossary**: Computer security terms and definitions
- **RFC Editor**: Internet standards and protocol specifications
- **Open Textbook Library**: Free academic textbooks on computer science
- **GeeksforGeeks**: Programming concepts with examples and definitions
- **MDN Web Docs**: Web technology references and tutorials

### Creating Interconnected Learning Paths
When writing new content:
1. Link to prerequisite posts with phrases like "building on our [fundamental concepts](/link/)"
2. Create "See also" sections linking to related topics
3. Use consistent terminology across posts
4. Build glossary posts that define key terms
5. Create index/hub posts that organize topics by learning path
6. Add "Next steps" sections pointing to more advanced topics