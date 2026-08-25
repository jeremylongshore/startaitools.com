# 🚀 Start AI Tools - AI Implementation Platform

[![Hugo](https://img.shields.io/badge/Hugo-Extended-ff4088?logo=hugo)](https://gohugo.io/)
[![Deploy](https://github.com/jeremylongshore/startaitools.com/actions/workflows/deploy.yml/badge.svg)](https://github.com/jeremylongshore/startaitools.com/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/U5S225PTME)

> Business blog and knowledge center for AI deployment, technical guides, and real-world implementation case studies. Built with Hugo and presented by Intent Solutions.

🔗 **Live Site:** [startaitools.com](https://startaitools.com)

## ✨ Features

- 📝 **Technical Blog** - 325+ posts on AI deployment, data engineering, and DevOps
- 🛠️ **Real-World Case Studies** - DiagnosticPro platform, BigQuery schemas, RSS validation
- 📊 **AI Engineering Resources** - Comprehensive curriculum and research materials
- 🎨 **Professional Design** - Clean, fast, business-focused with Archie theme
- 🔍 **SEO Optimized** - Structured data, meta tags, sitemap
- ⚡ **Lightning Fast** - Static site with optimized builds and aggressive caching
- 📱 **Responsive** - Mobile-first design with excellent UX

## 🏗️ Tech Stack

- **Static Site Generator:** [Hugo](https://gohugo.io/) v0.150.0 in production
- **Theme:** [Archie](https://github.com/athul/archie) (Professional business theme)
- **Hosting:** Self-hosted VPS (Caddy) via GitHub Actions deploy
- **Domain:** startaitools.com
- **Build Process:** Minified, optimized, cache-controlled
- **Features:** Syntax highlighting, code copy buttons, table of contents

## 📂 Content Structure

```
content/
├── posts/              # Blog posts (290+ technical articles, flat)
│   └── *.md           # Individual blog posts
├── _index.md          # Homepage
├── about.md           # About page
├── contact.md         # Contact page
├── projects.md        # Projects showcase
├── research.md        # Research & curriculum
├── en/                # Legacy English content structure
├── agentic-design-patterns/  # Design pattern documentation
├── mcp-for-beginners/        # MCP tutorial series
└── tiny-recursive-models/    # ML model documentation
```

## 🚀 Quick Start

### Prerequisites

- [Hugo](https://gohugo.io/installation/) v0.150.0+
- [Git](https://git-scm.com/)
- [Node.js](https://nodejs.org/) v18+ (for build environment)

### Local Development

```bash
# Clone the repository (or navigate to existing directory)
cd /home/jeremy/projects/blog/startaitools

# Start development server with drafts
hugo server -D

# Start server without drafts (production preview)
hugo server

# Start server accessible from external devices
hugo server -D --bind 0.0.0.0

# View at http://localhost:1313
```

### Build for Production

```bash
# Build optimized static site
hugo --gc --minify --cleanDestinationDir

# Output will be in ./public directory
```

## 📝 Writing Content

### Create New Post

```bash
# Create a new blog post
hugo new posts/my-new-post.md

# Create a project page
hugo new projects/my-project.md
```

### Front Matter Template

Posts use **YAML format** (not TOML):

```yaml
---
title: "Your Post Title"
date: 2025-10-09T10:00:00-06:00
draft: false
tags: ["ai", "programming", "deployment"]
author: "Jeremy Longshore"
description: "Brief description for SEO and social media"
---
```

**Important:** This project uses YAML front matter (delimited by `---`), not TOML format.

## 🎨 Customization

### Site Configuration

Edit `config/_default/config.toml` for site-wide settings:

```toml
baseURL = "https://startaitools.com/"
title = "Start AI Tools - Presented by Intent Solutions"
theme = "archie"
author = "Jeremy Longshore"

[params]
description = "Deploy AI solutions in days, not months"
```

### Navigation Menu

The site has a 6-item navigation menu:
1. Home
2. Posts
3. About
4. Research & Curriculum
5. Projects
6. Contact

Edit menu items in `config/_default/config.toml` under `[menu]` section.

### Custom Styling

The Archie theme provides professional business styling. To customize:

1. Override theme layouts in `layouts/` directory
2. Add custom CSS in `static/css/custom.css`
3. Modify theme parameters in `config.toml`

## 🔗 Featured Content

### Major Blog Post Topics

1. **Data Engineering** - BigQuery 254-table schema, data pipelines, RSS validation (226+ feeds)
2. **AI Platforms** - DiagnosticPro case studies, AI integration workflows
3. **DevOps Automation** - N8N workflows, GitHub Actions, Terraform guides
4. **Documentation Systems** - Claude.md, directory standards, AI-assisted writing
5. **Real-World Debugging** - Slack integration, COPPA compliance, testing suites

### Related Projects

1. **[DiagnosticPro](https://diagnosticpro.io)** - AI-powered diagnostic platform for repair professionals
2. **[Intent Solutions](https://intentsolutions.io)** - AI deployment and consulting services
3. **[AI Engineering Curriculum](https://jeremylongshore.github.io/ai-engineering-curriculum/)** - Comprehensive learning path
4. **[Jeremy Longshore Blog](https://jeremylongshore.com)** - Personal portfolio and tech blog

## 🚢 Deployment

### VPS via GitHub Actions (Current Setup)

Push to `master` runs a Hugo build gate, then deploys to the production VPS over
Tailscale workload-identity federation and a command-restricted SSH key. The VPS
rebuilds from `origin/master` with pinned Hugo 0.150.0 and serves the output
through Caddy.

- **Build command:** `hugo --buildFuture --gc --minify --cleanDestinationDir`
- **Hugo version:** 0.150.0 (pinned on the VPS and in the CI gate)
- **Smoke test:** `https://startaitools.com/healthz` must return `{"status":"ok"}`
- **Domain:** startaitools.com with HTTPS (Caddy-managed certificates)
- **Timezone:** America/Chicago

Netlify remains configured (`netlify.toml`) only as a temporary rollback target
from the hosting cutover; it is not the production host.

### Cache Control Strategy

Aggressive cache-busting served by Caddy:
- HTML pages: `no-cache, no-store, must-revalidate`
- Static assets (css/js/fonts/images): short-lived public cache

This ensures fresh content on every visit while maintaining performance.

### Manual Deployment

```bash
# Build the site
hugo --gc --minify --cleanDestinationDir

# Deploy public/ directory to any static host
rsync -avz public/ user@server:/var/www/html/
```

## 📈 Performance Metrics

- **Lighthouse Score:** 95+/100
- **Page Load:** < 2s
- **First Contentful Paint:** < 800ms
- **Time to Interactive:** < 1.5s
- **Total Page Size:** Optimized with minification and compression

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository (if external contributor)
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Test locally with `hugo server -D`
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open Pull Request

### Content Guidelines

- Use YAML front matter (not TOML)
- Include meaningful tags and descriptions
- Test locally before pushing
- Follow existing content structure
- Optimize images before adding

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Hugo](https://gohugo.io/) - Blazing fast static site generator
- [Archie Theme](https://github.com/athul/archie) - Clean, professional business theme
- [Netlify](https://netlify.com/) - Seamless hosting and deployment
- Open source community

## 📧 Contact

- **Website:** [startaitools.com](https://startaitools.com)
- **Business:** [Intent Solutions](https://intentsolutions.io)
- **Email:** jeremy@intentsolutions.io
- **GitHub:** [@jeremylongshore](https://github.com/jeremylongshore)
- **LinkedIn:** [Jeremy Longshore](https://linkedin.com/in/jeremylongshore)
- **X/Twitter:** [@asphaltcowb0y](https://x.com/asphaltcowb0y)

---

<p align="center">
  <strong>Deploy AI solutions in days, not months</strong><br>
  Presented by Intent Solutions
</p>

<p align="center">
  <a href="https://github.com/jeremylongshore/startaitools">⭐ Star this project</a> •
  <a href="https://startaitools.com">🌐 Visit the site</a> •
  <a href="https://github.com/jeremylongshore/startaitools/issues">🐛 Report an issue</a>
</p>
