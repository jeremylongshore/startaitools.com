# Intent Solutions Inc. Blog

This repository contains the source code for the company blog for Intent Solutions Inc., a firm specializing in deploying AI solutions.

### 🌐 Live Site
[startaitools.com](https://startaitools.com)

### 🛠 Tech Stack
- **Static Site Generator:** Hugo
- **Theme:** Archie
- **Hosting:** Netlify

### 📝 Local Development

To run the site locally for development:
```bash
# Start development server
hugo server -D --bind 0.0.0.0
```

To build the site for production:
```bash
# Build for production
hugo --gc --minify --cleanDestinationDir
```

To create a new blog post:
```bash
# Create new blog post
hugo new posts/my-new-post.md
```

### 🏗 Project Structure
```
├── content/        # All site content
│   ├── posts/      # Blog posts
│   └── ...
├── static/         # Static assets (images, etc.)
├── themes/archie/  # Theme files
├── public/         # Generated site (not in git)
└── hugo.toml       # Main configuration
```
