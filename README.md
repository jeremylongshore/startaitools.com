# 🚀 StartAITools.com - AI Development Knowledge Center

[![Hugo](https://img.shields.io/badge/Hugo-v0.150.0-ff4088?logo=hugo)](https://gohugo.io/)
[![Theme](https://img.shields.io/badge/Theme-Hugo%20Book-blue)](https://github.com/alex-shpak/hugo-book)
[![Netlify Status](https://api.netlify.com/api/v1/badges/YOUR-BADGE-ID/deploy-status)](https://app.netlify.com/sites/startaitools/deploys)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> Comprehensive knowledge center documenting the journey from AI experiments to production systems. Learn from real-world implementations, access professional documentation templates, and follow proven development workflows.

🔗 **Live Site:** [startaitools.com](https://startaitools.com)

## ✨ What You'll Find Here

### 📚 Knowledge Center
- **Developer Workflows** - AI-assisted development from PRD to production
- **Architecture Patterns** - System design and workspace organization
- **Project Journey** - Complete timeline from RAG experiments to revenue
- **Security Guides** - Linux, SSH, and security best practices
- **AI/ML Documentation** - Machine learning implementation guides

### 🛠️ Professional Templates
- **22+ Documentation Templates** - PRDs, Tech Specs, ADRs, and more
- **Real PRD Examples** - Actual product requirements using our templates
- **Task Generation System** - Break down PRDs into actionable tasks
- **Workflow Automation** - AI-assisted development patterns

### 📖 Learning Resources
- **Getting Started Guides** - Entry points for different skill levels
- **Technical Glossary** - Comprehensive term definitions
- **Cross-Referenced Content** - Interconnected learning paths
- **Real Project Stories** - Learn from actual implementations

## 🏗️ Technology Stack

- **Static Site Generator:** [Hugo](https://gohugo.io/) v0.150.0 (Extended)
- **Theme:** [Hugo Book](https://github.com/alex-shpak/hugo-book) - Knowledge center layout
- **Hosting:** [Netlify](https://netlify.com/) - Automatic deployment
- **Search:** Built-in Hugo Book search functionality
- **Domain:** startaitools.com
- **Repository:** [github.com/jeremylongshore/startaitools.com](https://github.com/jeremylongshore/startaitools.com)

## 📂 Project Structure

```
startaitools/
├── content/
│   ├── docs/                  # Knowledge center (main content)
│   │   ├── getting-started/   # New user onboarding
│   │   ├── ai-ml/            # AI & ML guides
│   │   ├── architecture/      # System design
│   │   ├── blog/             # Blog archives
│   │   ├── journey/          # Project evolution
│   │   ├── resources/        # External links
│   │   ├── security/         # Security docs
│   │   ├── templates/        # Documentation templates
│   │   └── workflow/         # Dev workflows
│   ├── posts/                 # Blog posts
│   ├── glossary/             # Term definitions
│   └── _index.md             # Homepage
├── tasks/                     # PRDs and task lists
├── ai-dev-tasks/             # Template source files
├── themes/hugo-book/         # Theme (git submodule)
├── static/                   # Static assets
├── public/                   # Generated site (gitignored)
├── hugo.toml                 # Site configuration
└── netlify.toml             # Deployment config
```

## 🚀 Quick Start

### Prerequisites

- [Hugo Extended](https://gohugo.io/installation/) v0.150.0+
- [Git](https://git-scm.com/)
- Text editor (VS Code, Cursor, etc.)

### Local Development

```bash
# Clone the repository
git clone https://github.com/jeremylongshore/startaitools.com.git
cd startaitools

# Initialize theme submodule
git submodule update --init --recursive

# Start development server
hugo server -D --bind 0.0.0.0

# View at http://localhost:1313
```

### Build for Production

```bash
# Build optimized site
hugo --gc --minify --cleanDestinationDir

# Output in ./public directory
```

## 📝 Content Creation

### Create Documentation

```bash
# New documentation page
hugo new docs/section/page-name.md

# Example:
hugo new docs/workflow/my-workflow.md
```

### Create Blog Post

```bash
# New blog post
hugo new posts/my-blog-post.md
```

### Create PRD

```bash
# Use the PRD template
Use @ai-dev-tasks/create-prd.md

# Save in tasks directory
tasks/prd-feature-name.md
```

### Front Matter Examples

**Documentation Page:**
```yaml
---
title: "Page Title"
weight: 10
bookToc: true
bookCollapseSection: false
tags: ["tag1", "tag2"]
description: "SEO description"
---
```

**Blog Post:**
```yaml
---
title: "Post Title"
date: 2025-09-14T10:00:00-06:00
draft: false
tags: ["ai", "development"]
categories: ["Technical"]
author: "Jeremy Longshore"
description: "SEO description"
---
```

## 🎨 Key Features

### Navigation
- **Collapsible Sidebar** - Organized sections that expand/collapse
- **Weighted Ordering** - Logical content arrangement
- **Breadcrumbs** - Clear navigation paths
- **Table of Contents** - Auto-generated for long pages

### Content Features
- **Cross-References** - Interconnected topics
- **Template Library** - 22+ professional templates
- **Real Examples** - Actual PRDs and implementations
- **Glossary Integration** - Technical term definitions

### Development Features
- **Auto-Deploy** - Push to master triggers deployment
- **Hot Reload** - Live preview during development
- **SEO Optimized** - Meta tags and descriptions
- **Mobile Responsive** - Works on all devices

## 🔧 Configuration

### Site Configuration
Edit `hugo.toml` for:
- Site title and metadata
- Menu structure
- Theme settings
- Build options

### Deployment Configuration
Edit `netlify.toml` for:
- Build commands
- Environment variables
- Redirect rules
- Headers

## 🚢 Deployment

The site automatically deploys to Netlify when you push to the master branch:

```bash
git add .
git commit -m "feat: Your changes"
git push origin master
```

**Netlify Settings:**
- Build Command: `hugo --gc --minify --cleanDestinationDir`
- Publish Directory: `public/`
- Hugo Version: 0.150.0

## 📚 Documentation

- **For AI Assistants:** See [CLAUDE.md](CLAUDE.md) for comprehensive guidance
- **Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines
- **Releases:** See [RELEASES.md](RELEASES.md) for version history
- **GitHub Setup:** See [GITHUB_SETUP.md](GITHUB_SETUP.md) for repository config

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Content submission guidelines
- Code contribution process
- Style guide
- Review process

### Ways to Contribute
- 📝 Write documentation or tutorials
- 🐛 Report bugs or issues
- 💡 Suggest new features
- 🔧 Submit pull requests
- ⭐ Star the repository

## 📊 Project Stats

- **Content Pages:** 50+ documentation pages
- **Templates:** 22 professional templates
- **Blog Posts:** 17+ technical articles
- **PRD Examples:** 8 real implementations
- **Monthly Visitors:** Growing!

## 🗺️ Roadmap

### In Progress
- ✅ Knowledge center structure
- ✅ Collapsible navigation
- ✅ Template library
- ✅ Project timeline documentation

### Coming Soon
- [ ] Smart glossary with auto-linking
- [ ] Interactive code examples
- [ ] Video tutorials
- [ ] Newsletter integration
- [ ] Comment system

## 🔗 Related Projects

- **Templates Repository:** [github.com/jeremylongshore/vibe-prd](https://github.com/jeremylongshore/vibe-prd)
- **Company GitHub:** [github.com/jeremylongshore](https://github.com/jeremylongshore)
- **Personal Site:** [jeremylongshore.com](https://jeremylongshore.com)

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- [Hugo](https://gohugo.io/) - Static site generator
- [Hugo Book Theme](https://github.com/alex-shpak/hugo-book) - Knowledge center theme
- [Netlify](https://netlify.com/) - Hosting and deployment
- [stulogy](https://github.com/stulogy) - Original PRD template inspiration
- AI community for continuous feedback

## 💼 About Intent Solutions Inc.

Intent Solutions specializes in rapid AI deployment for businesses. We help companies integrate AI solutions quickly and effectively.

**Services:**
- AI Strategy Consulting
- Custom AI Development
- Tool Selection & Integration
- Training & Support

## 📧 Contact

- **Website:** [startaitools.com](https://startaitools.com)
- **Company:** [Intent Solutions Inc.](https://intentsolutions.io)
- **Email:** hello@startaitools.com
- **GitHub:** [@jeremylongshore](https://github.com/jeremylongshore)

---

<p align="center">
  Built with ❤️ by Jeremy Longshore
</p>

<p align="center">
  <a href="https://startaitools.com">🌐 Visit Site</a> •
  <a href="https://github.com/jeremylongshore/startaitools.com">⭐ Star on GitHub</a> •
  <a href="https://github.com/jeremylongshore/startaitools.com/issues">🐛 Report Issue</a>
</p>