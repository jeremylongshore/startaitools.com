# StartAITools.com Complete Implementation Plan
## Technological Dependency Order

**Date:** September 14, 2025
**Purpose:** Clean separation of internal business content (/blog/) from educational resources (/docs/)

---

## Phase 1: INFRASTRUCTURE FOUNDATION
*Dependencies: None*
*Duration: 1 day*

### 1.1 Hugo Configuration Fixes

#### Fix Deprecation Warnings
```toml
# hugo.toml - Update these sections

# Change deprecated Twitter to X
[privacy.x]
  disable = true

# Remove deprecated privacy.twitter section
# [privacy.twitter] <- DELETE THIS

# Update Hugo version in netlify.toml
[build.environment]
  HUGO_VERSION = "0.150.0"  # Was 0.149.1
```

#### Add SEO Configuration
```toml
# hugo.toml - Add to [params] section

[params]
  description = "Learn AI implementation with real-world guides and templates"
  keywords = ["AI development", "machine learning", "technical guides", "automation"]
  author = "Intent Solutions Inc"

  # Open Graph defaults
  images = ["/images/og-default.png"]

  # Hide internal content from search engines
  robotsNoIndex = ["/blog/", "/tasks/", "/internal/"]

[params.seo]
  canonicalURL = true
  enableRobotsTXT = true

  # Schema.org for educational content
  schemaType = "LearningResource"
  educationalLevel = "Professional"

# Security - disable unsafe rendering for public content
[markup.goldmark.renderer]
  unsafe = false
```

#### Create robots.txt Template
```bash
# layouts/robots.txt
User-agent: *
Disallow: /blog/
Disallow: /tasks/
Disallow: /internal/
Disallow: /ai-dev-tasks/
Allow: /docs/
Allow: /resources/
Allow: /glossary/

Sitemap: {{ .Site.BaseURL }}sitemap.xml
```

### 1.2 Build Process Optimization

#### Update Netlify Configuration
```toml
# netlify.toml

[build]
  command = "hugo --gc --minify --cleanDestinationDir && npm run postbuild"
  publish = "public"

[build.environment]
  HUGO_VERSION = "0.150.0"
  HUGO_ENV = "production"
  HUGO_ENABLEGITINFO = "true"
  NODE_VERSION = "18"

# Add build plugin for broken link checking
[[plugins]]
  package = "netlify-plugin-checklinks"

  [plugins.inputs]
    entryPoints = ["public/index.html"]
    recursive = true
    pretty = true
    skipPatterns = ["/blog/", "/internal/"]

# Security headers for internal content
[[headers]]
  for = "/blog/*"
  [headers.values]
    X-Robots-Tag = "noindex, nofollow"
    Cache-Control = "private, no-cache"

[[headers]]
  for = "/tasks/*"
  [headers.values]
    X-Robots-Tag = "noindex, nofollow"
    Cache-Control = "private, no-cache"
```

#### Create Post-Build Script
```json
// package.json (create this file)
{
  "name": "startaitools",
  "version": "1.0.0",
  "scripts": {
    "postbuild": "node scripts/postbuild.js",
    "validate": "node scripts/validate-structure.js"
  },
  "devDependencies": {
    "glob": "^8.0.3"
  }
}
```

```javascript
// scripts/postbuild.js
const fs = require('fs');
const path = require('path');

// Add noindex meta tag to internal content
const internalPaths = ['public/blog', 'public/tasks', 'public/internal'];

internalPaths.forEach(dir => {
  if (fs.existsSync(dir)) {
    const files = fs.readdirSync(dir, { recursive: true })
      .filter(f => f.endsWith('.html'));

    files.forEach(file => {
      const filepath = path.join(dir, file);
      let content = fs.readFileSync(filepath, 'utf8');

      // Add noindex if not present
      if (!content.includes('noindex')) {
        content = content.replace(
          '</head>',
          '<meta name="robots" content="noindex, nofollow">\n</head>'
        );
        fs.writeFileSync(filepath, content);
      }
    });
  }
});
```

### 1.3 Performance Baseline

#### Create Performance Monitoring Script
```bash
#!/bin/bash
# scripts/performance-baseline.sh

echo "=== Performance Baseline ==="

# Check build time
time hugo --gc --minify --cleanDestinationDir

# Check output size
echo "Public directory size:"
du -sh public/

# Count pages
echo "Total pages:"
find public -name "*.html" | wc -l

# Check for large assets
echo "Large files (>1MB):"
find public -type f -size +1M -exec ls -lh {} \;

# Generate baseline report
cat > performance-baseline.txt << EOF
Date: $(date)
Build Time: $(time hugo --gc --minify 2>&1 | grep real)
Output Size: $(du -sh public/)
Total Pages: $(find public -name "*.html" | wc -l)
Large Files: $(find public -type f -size +1M | wc -l)
EOF
```

### Verification Steps - Phase 1
```bash
# 1. Check Hugo version
hugo version  # Should show 0.150.0+

# 2. Validate configuration
hugo config | grep -E "privacy|seo|robots"

# 3. Test build
hugo --gc --minify --cleanDestinationDir

# 4. Check for warnings
hugo --gc --minify 2>&1 | grep -i "warn"

# 5. Verify robots.txt
cat public/robots.txt | grep Disallow
```

---

## Phase 2: CORE STRUCTURE REORGANIZATION
*Dependencies: Phase 1 complete*
*Duration: 2 days*

### 2.1 Content Directory Restructuring

#### New Directory Structure
```bash
#!/bin/bash
# scripts/restructure-directories.sh

# Create new structure
mkdir -p content/{docs,blog,resources,glossary,internal}
mkdir -p content/docs/{guides,reference,getting-started}
mkdir -p content/docs/guides/{ai-ml,architecture,development,operations}
mkdir -p content/docs/reference/{api,templates,specifications}
mkdir -p content/internal/{tasks,prds,adrs}

# Create section indexes with proper metadata
cat > content/blog/_index.md << 'EOF'
---
title: "Blog"
weight: 40
bookToc: false
bookCollapseSection: false
description: "Personal projects and internal development notes"
robotsNoIndex: true
cascade:
  robotsNoIndex: true
---

# Blog

Personal workspace for projects, development notes, and internal documentation.

> **Note:** This section contains internal business content and personal projects.
EOF

cat > content/docs/_index.md << 'EOF'
---
title: "Documentation"
weight: 10
bookToc: true
bookCollapseSection: true
description: "Educational resources for AI development and implementation"
---

# Documentation

Learn AI implementation with real-world guides, templates, and best practices.

## Categories

- [Getting Started](/docs/getting-started/) - Begin your AI journey
- [Technical Guides](/docs/guides/) - In-depth tutorials and how-tos
- [Reference](/docs/reference/) - Templates and specifications
EOF

cat > content/internal/_index.md << 'EOF'
---
title: "Internal"
weight: 100
bookHidden: true
robotsNoIndex: true
cascade:
  robotsNoIndex: true
  bookHidden: true
---

# Internal Resources

This section is not publicly accessible.
EOF
```

### 2.2 URL Scheme Standardization

#### Hugo Alias Configuration
```yaml
# Template for content migration with aliases

# For moved content, add to front matter:
---
title: "Page Title"
aliases:
  - "/old/path/"
  - "/another/old/path/"
---
```

#### Bulk Alias Addition Script
```bash
#!/bin/bash
# scripts/add-aliases.sh

# Add aliases to all moved content
add_alias() {
  local file=$1
  local old_path=$2

  # Insert alias after title in front matter
  sed -i "/^title:/a aliases:\n  - \"$old_path\"" "$file"
}

# Journey content → Blog
for file in content/docs/journey/*.md; do
  if [ -f "$file" ]; then
    filename=$(basename "$file")
    cp "$file" "content/blog/$filename"
    add_alias "content/blog/$filename" "/docs/journey/$(basename $file .md)/"
  fi
done

# Tasks → Internal
for file in tasks/*.md; do
  if [ -f "$file" ]; then
    filename=$(basename "$file")
    cp "$file" "content/internal/tasks/$filename"
    add_alias "content/internal/tasks/$filename" "/tasks/$(basename $file .md)/"
  fi
done
```

### 2.3 Navigation Weight Implementation

#### Standard Weight System
```yaml
# Weight allocation strategy

# Top-level sections
10 - Getting Started (public education)
20 - Guides (public education)
30 - Reference (public education)
40 - Blog (internal/personal)
50 - Resources (public)
60 - Glossary (public)
100 - Internal (hidden)

# Within sections (increment by 10)
10 - Overview/Introduction
20 - Core concepts
30 - Implementation
40 - Advanced topics
50 - Examples
60 - FAQ
70 - Related resources
```

#### Batch Weight Assignment Script
```python
#!/usr/bin/env python3
# scripts/assign-weights.py

import os
import re
import frontmatter

def assign_weight(filepath, weight_map):
    """Assign weight based on file path and name."""
    with open(filepath, 'r') as f:
        post = frontmatter.load(f)

    # Determine weight based on path
    rel_path = os.path.relpath(filepath, 'content')

    for pattern, weight in weight_map.items():
        if pattern in rel_path:
            post['weight'] = weight
            break

    # Write back
    with open(filepath, 'w') as f:
        f.write(frontmatter.dumps(post))

# Weight mapping
weight_map = {
    'getting-started/_index': 10,
    'guides/_index': 20,
    'reference/_index': 30,
    'blog/_index': 40,
    'resources/_index': 50,
    'glossary/_index': 60,
    'internal/_index': 100,
}

# Apply weights
for root, dirs, files in os.walk('content'):
    for file in files:
        if file.endswith('.md'):
            filepath = os.path.join(root, file)
            assign_weight(filepath, weight_map)
```

### 2.4 Internal Linking Architecture

#### Link Validation Script
```bash
#!/bin/bash
# scripts/validate-links.sh

echo "=== Internal Link Validation ==="

# Find all internal links
grep -r '\[.*\](/[^)]*' content/ --include="*.md" | while read -r line; do
  file=$(echo "$line" | cut -d: -f1)
  link=$(echo "$line" | grep -o '](/[^)]*' | sed 's|](||')

  # Check if target exists
  target="content${link}"
  target="${target%.md}.md"
  target="${target%/}.md"

  if [ ! -f "$target" ] && [ ! -f "${target/_index.md}" ]; then
    echo "BROKEN: $file -> $link"
  fi
done > broken-links.txt

echo "Broken links saved to broken-links.txt"
```

### Verification Steps - Phase 2
```bash
# 1. Verify directory structure
tree -L 3 content/

# 2. Check all indexes have weights
grep -r "^weight:" content/**/_index.md

# 3. Validate internal links
./scripts/validate-links.sh

# 4. Test Hugo build with new structure
hugo server -D

# 5. Check URL aliases work
curl -I http://localhost:1313/docs/journey/ # Should redirect
```

---

## Phase 3: CONTENT MIGRATION & CLEANUP
*Dependencies: Phase 2 complete*
*Duration: 2 days*

### 3.1 Broken Link Identification

#### Comprehensive Link Audit
```bash
#!/bin/bash
# scripts/link-audit.sh

echo "=== Comprehensive Link Audit ==="

# Create audit report
cat > link-audit-report.md << 'EOF'
# Link Audit Report
Date: $(date)

## Broken Internal Links
EOF

# Find all broken patterns
echo "### Journey Links (to be moved to /blog/)" >> link-audit-report.md
grep -r "](/docs/journey" content/ --include="*.md" >> link-audit-report.md || echo "None found" >> link-audit-report.md

echo "### Task Links (to be made internal)" >> link-audit-report.md
grep -r "](/tasks/" content/ --include="*.md" >> link-audit-report.md || echo "None found" >> link-audit-report.md

echo "### Library Links (to be moved to /resources/)" >> link-audit-report.md
grep -r "](/library" content/ --include="*.md" >> link-audit-report.md || echo "None found" >> link-audit-report.md

# Generate fix commands
echo "## Fix Commands" >> link-audit-report.md
echo '```bash' >> link-audit-report.md
echo 'find content -name "*.md" -exec sed -i "s|](/docs/journey|](/blog|g" {} \;' >> link-audit-report.md
echo 'find content -name "*.md" -exec sed -i "s|](/tasks/|](/internal/tasks/|g" {} \;' >> link-audit-report.md
echo 'find content -name "*.md" -exec sed -i "s|](/library|](/resources|g" {} \;' >> link-audit-report.md
echo '```' >> link-audit-report.md
```

### 3.2 Content Categorization

#### Content Classification Script
```python
#!/usr/bin/env python3
# scripts/classify-content.py

import os
import frontmatter
import shutil

def classify_content(filepath):
    """Classify content as internal or public."""
    with open(filepath, 'r') as f:
        post = frontmatter.load(f)
        content = post.content.lower()

    # Internal indicators
    internal_keywords = [
        'prd', 'adr', 'internal', 'task list', 'diagnosticpro',
        'personal project', 'my project', 'client work'
    ]

    # Check for internal indicators
    is_internal = any(keyword in content for keyword in internal_keywords)

    # Check front matter
    if post.get('internal', False) or post.get('draft', False):
        is_internal = True

    return 'internal' if is_internal else 'public'

# Classification mapping
classification = {
    'internal': [],
    'public': []
}

# Classify all content
for root, dirs, files in os.walk('content'):
    for file in files:
        if file.endswith('.md'):
            filepath = os.path.join(root, file)
            category = classify_content(filepath)
            classification[category].append(filepath)

# Generate report
with open('content-classification.md', 'w') as f:
    f.write('# Content Classification Report\n\n')
    f.write(f'## Internal Content ({len(classification["internal"])} files)\n')
    for file in classification['internal']:
        f.write(f'- {file}\n')
    f.write(f'\n## Public Content ({len(classification["public"])} files)\n')
    for file in classification['public']:
        f.write(f'- {file}\n')

print(f"Classification complete: {len(classification['internal'])} internal, {len(classification['public'])} public")
```

### 3.3 Migration Execution

#### Master Migration Script
```bash
#!/bin/bash
# scripts/migrate-content.sh

echo "=== Content Migration Script ==="

# Backup everything first
BACKUP_DIR="backup-$(date +%Y%m%d-%H%M%S)"
cp -r content "$BACKUP_DIR"
echo "Backup created: $BACKUP_DIR"

# 1. Move journey content to blog
echo "Moving journey content to blog..."
if [ -d "content/docs/journey" ]; then
  for file in content/docs/journey/*.md; do
    if [ -f "$file" ]; then
      filename=$(basename "$file")
      # Skip _index.md
      if [ "$filename" != "_index.md" ]; then
        cp "$file" "content/blog/project-$(basename $file)"
        # Add redirect alias
        sed -i "2a aliases:\n  - \"/docs/journey/$(basename $file .md)/\"" \
          "content/blog/project-$(basename $file)"
      fi
    fi
  done
  rm -rf content/docs/journey
fi

# 2. Move tasks to internal
echo "Moving tasks to internal..."
if [ -d "tasks" ]; then
  mkdir -p content/internal/tasks
  for file in tasks/*.md; do
    if [ -f "$file" ]; then
      cp "$file" "content/internal/tasks/"
      # Add redirect alias
      sed -i "2a aliases:\n  - \"/tasks/$(basename $file .md)/\"" \
        "content/internal/tasks/$(basename $file)"
    fi
  done
fi

# 3. Move ai-dev-tasks to internal
echo "Moving ai-dev-tasks to internal..."
if [ -d "ai-dev-tasks" ]; then
  mkdir -p content/internal/ai-dev-tasks
  cp -r ai-dev-tasks/* content/internal/ai-dev-tasks/
fi

# 4. Remove 'archive' references
echo "Updating archive references..."
find content -name "*.md" -exec sed -i 's/Blog Archive/Blog/g' {} \;
find content -name "*.md" -exec sed -i 's/blog archive/blog/g' {} \;

# 5. Update all internal links
echo "Updating internal links..."
find content -name "*.md" -exec sed -i \
  -e 's|](/docs/journey/|](/blog/project-|g' \
  -e 's|](/tasks/|](/internal/tasks/|g' \
  -e 's|](/ai-dev-tasks/|](/internal/ai-dev-tasks/|g' \
  -e 's|](/library/|](/resources/|g' \
  {} \;

echo "Migration complete!"
```

### 3.4 Duplicate Content Resolution

#### Deduplication Script
```python
#!/usr/bin/env python3
# scripts/deduplicate.py

import os
import hashlib
import frontmatter
from collections import defaultdict

def get_content_hash(filepath):
    """Get hash of content (excluding front matter)."""
    with open(filepath, 'r') as f:
        post = frontmatter.load(f)
        content = post.content.strip()
        return hashlib.md5(content.encode()).hexdigest()

# Find duplicates
duplicates = defaultdict(list)

for root, dirs, files in os.walk('content'):
    for file in files:
        if file.endswith('.md'):
            filepath = os.path.join(root, file)
            content_hash = get_content_hash(filepath)
            duplicates[content_hash].append(filepath)

# Report duplicates
with open('duplicate-report.md', 'w') as f:
    f.write('# Duplicate Content Report\n\n')

    for content_hash, files in duplicates.items():
        if len(files) > 1:
            f.write(f'## Duplicate Set (hash: {content_hash[:8]})\n')
            for filepath in files:
                f.write(f'- {filepath}\n')
            f.write('\n')

print(f"Found {sum(1 for f in duplicates.values() if len(f) > 1)} sets of duplicates")
```

### Verification Steps - Phase 3
```bash
# 1. Verify no journey directory exists
[ ! -d "content/docs/journey" ] && echo "✓ Journey removed" || echo "✗ Journey still exists"

# 2. Check internal content is marked
grep -r "robotsNoIndex: true" content/internal/

# 3. Verify all links updated
! grep -r "](/docs/journey" content/ && echo "✓ Journey links updated"

# 4. Check for duplicates
./scripts/deduplicate.py

# 5. Validate structure
hugo --gc --minify && echo "✓ Build successful"
```

---

## Phase 4: TEMPLATE SYSTEM OVERHAUL
*Dependencies: Phase 3 complete*
*Duration: 1 day*

### 4.1 Template Categorization

#### Move Templates to Appropriate Locations
```bash
#!/bin/bash
# scripts/reorganize-templates.sh

# Public educational templates → docs/reference/templates/
mkdir -p content/docs/reference/templates/{development,operations,documentation}

# Internal business templates → internal/templates/
mkdir -p content/internal/templates/{prds,adrs,tasks}

# Categorize and move templates
for template in ai-dev-tasks/*.md; do
  name=$(basename "$template")

  case "$name" in
    # Internal business templates
    *prd*|*adr*|*task*)
      cp "$template" "content/internal/templates/"
      ;;
    # Public educational templates
    *api*|*spec*|*guide*)
      cp "$template" "content/docs/reference/templates/development/"
      ;;
    *runbook*|*sop*|*post-mortem*)
      cp "$template" "content/docs/reference/templates/operations/"
      ;;
    *)
      cp "$template" "content/docs/reference/templates/documentation/"
      ;;
  esac
done
```

### 4.2 Hub-and-Spoke Implementation

#### Create Template Hub
```markdown
# content/docs/reference/templates/_index.md
---
title: "Template Library"
weight: 30
bookToc: true
bookCollapseSection: true
description: "Professional templates for AI development and documentation"
---

# Template Library

Professional templates to accelerate your AI development workflow.

## Categories

### Development Templates
Templates for technical documentation and specifications:
- [API Specification](/docs/reference/templates/development/api-spec/)
- [Technical Design Doc](/docs/reference/templates/development/design-doc/)
- [Database Schema](/docs/reference/templates/development/database-schema/)

### Operations Templates
Templates for operational excellence:
- [Runbook Template](/docs/reference/templates/operations/runbook/)
- [SOP Template](/docs/reference/templates/operations/sop/)
- [Post-Mortem Template](/docs/reference/templates/operations/post-mortem/)

### Documentation Templates
Templates for project documentation:
- [User Guide](/docs/reference/templates/documentation/user-guide/)
- [README Template](/docs/reference/templates/documentation/readme/)
- [Contributing Guide](/docs/reference/templates/documentation/contributing/)

## Quick Start

1. Choose a template category above
2. Select the specific template you need
3. Copy the template to your project
4. Follow the inline instructions

> **Note:** Internal business templates (PRDs, ADRs) are available in the [internal section](/internal/templates/) for authorized users only.
```

#### Create Discovery Spokes
```markdown
# content/docs/getting-started/templates.md
---
title: "Essential Templates"
weight: 50
description: "Start with these 5 essential templates"
---

# Essential Templates for New Projects

Get started quickly with these commonly-used templates:

## 1. API Specification
**When to use:** Designing a new API or service
**[View Template →](/docs/reference/templates/development/api-spec/)**

## 2. Runbook
**When to use:** Documenting operational procedures
**[View Template →](/docs/reference/templates/operations/runbook/)**

## 3. Technical Design
**When to use:** Planning system architecture
**[View Template →](/docs/reference/templates/development/design-doc/)**

## 4. User Guide
**When to use:** Creating end-user documentation
**[View Template →](/docs/reference/templates/documentation/user-guide/)**

## 5. Post-Mortem
**When to use:** Learning from incidents
**[View Template →](/docs/reference/templates/operations/post-mortem/)**

[Browse All Templates →](/docs/reference/templates/)
```

### 4.3 Template Access Control

#### Configure Template Visibility
```toml
# hugo.toml - Add template configuration

[params.templates]
  # Public templates location
  publicTemplates = "/docs/reference/templates/"

  # Internal templates (not indexed)
  internalTemplates = "/internal/templates/"

  # Template download tracking
  enableAnalytics = true
```

#### Create Template Access Script
```javascript
// static/js/template-access.js

// Track template usage (for analytics)
document.addEventListener('DOMContentLoaded', function() {
  const templateLinks = document.querySelectorAll('a[href*="/templates/"]');

  templateLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      const templatePath = this.getAttribute('href');

      // Check if internal template
      if (templatePath.includes('/internal/')) {
        // Require authentication for internal templates
        if (!isAuthenticated()) {
          e.preventDefault();
          alert('Internal templates require authentication');
          return false;
        }
      }

      // Track usage
      if (typeof gtag !== 'undefined') {
        gtag('event', 'template_view', {
          'template_path': templatePath
        });
      }
    });
  });
});

function isAuthenticated() {
  // Simple check - implement your auth logic
  return document.cookie.includes('internal_access=true');
}
```

### Verification Steps - Phase 4
```bash
# 1. Verify template organization
tree content/docs/reference/templates/
tree content/internal/templates/

# 2. Check public templates don't contain internal info
! grep -r "PRD\|ADR\|internal" content/docs/reference/templates/

# 3. Verify internal templates are hidden
grep "bookHidden: true" content/internal/templates/_index.md

# 4. Test template links
grep -r "](/.*templates" content/docs/

# 5. Build and verify
hugo server -D && curl http://localhost:1313/docs/reference/templates/
```

---

## Phase 5: USER EXPERIENCE LAYER
*Dependencies: Phase 4 complete*
*Duration: 2 days*

### 5.1 Navigation Menu Restructuring

#### Update Menu Configuration
```toml
# hugo.toml - Clear separation of content types

[menu]
  # Public educational content
  [[menu.before]]
    identifier = "docs"
    name = "📚 Learn"
    url = "/docs/"
    weight = 10

  [[menu.before]]
    identifier = "resources"
    name = "🔧 Resources"
    url = "/resources/"
    weight = 20

  [[menu.before]]
    identifier = "glossary"
    name = "📖 Glossary"
    url = "/glossary/"
    weight = 30

  # Separator (visual only)
  [[menu.before]]
    identifier = "separator"
    name = "—————"
    url = "#"
    weight = 40

  # Internal/Personal content
  [[menu.after]]
    identifier = "blog"
    name = "✍️ Blog"
    url = "/blog/"
    weight = 50

  # External links
  [[menu.after]]
    identifier = "github"
    name = "GitHub"
    url = "https://github.com/jeremylongshore"
    weight = 90
    params = { external = true }
```

#### Custom Menu Template
```html
<!-- layouts/partials/docs/menu.html -->
<nav class="book-menu">
  <h3>Educational Resources</h3>
  <ul>
    {{ range .Site.Menus.before }}
      {{ if ne .Identifier "separator" }}
        <li>
          <a href="{{ .URL }}" {{ if .Params.external }}target="_blank"{{ end }}>
            {{ .Name }}
          </a>
        </li>
      {{ else }}
        <li class="menu-separator">{{ .Name }}</li>
      {{ end }}
    {{ end }}
  </ul>

  {{ if .Site.Params.ShowInternalMenu }}
    <h3>Internal Resources</h3>
    <ul>
      {{ range .Site.Menus.after }}
        <li>
          <a href="{{ .URL }}" {{ if .Params.external }}target="_blank"{{ end }}>
            {{ .Name }}
          </a>
        </li>
      {{ end }}
    </ul>
  {{ end }}
</nav>
```

### 5.2 Search Configuration

#### Configure Search Filtering
```javascript
// static/js/search-config.js

window.addEventListener('DOMContentLoaded', function() {
  // Initialize search with filters
  if (window.pagefind) {
    window.pagefind.init({
      // Exclude internal content from search
      excludeSelectors: [
        '[data-pagefind-ignore]',
        '.internal-content',
        '#blog-section'
      ],

      // Filter by content type
      filters: {
        section: {
          default: ['docs', 'resources', 'glossary'],
          options: {
            'docs': 'Documentation',
            'resources': 'Resources',
            'glossary': 'Glossary',
            'blog': 'Blog (Internal)'
          }
        }
      },

      // Search result processing
      processResult: function(result) {
        // Hide internal results for non-authenticated users
        if (result.url.includes('/internal/') || result.url.includes('/blog/')) {
          if (!isUserAuthenticated()) {
            return null; // Hide result
          }
          // Mark as internal
          result.internal = true;
        }
        return result;
      }
    });
  }
});
```

#### Search Index Configuration
```toml
# config/_default/params.toml

[search]
  # Enable search
  enable = true

  # Search index settings
  indexing = true

  # Exclude from search index
  excludePaths = [
    "/blog/*",
    "/internal/*",
    "/tasks/*",
    "/ai-dev-tasks/*"
  ]

  # Search placeholder
  placeholder = "Search documentation..."

  # Results per page
  resultsPerPage = 10
```

### 5.3 Mobile Responsiveness

#### Mobile Navigation CSS
```css
/* static/css/mobile-nav.css */

/* Mobile menu toggle */
.mobile-menu-toggle {
  display: none;
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 1001;
  background: var(--body-background);
  border: 2px solid var(--color-link);
  border-radius: 4px;
  padding: 0.5rem;
}

@media (max-width: 768px) {
  .mobile-menu-toggle {
    display: block;
  }

  .book-menu {
    position: fixed;
    top: 0;
    left: -100%;
    width: 80%;
    max-width: 300px;
    height: 100vh;
    background: var(--body-background);
    box-shadow: 2px 0 10px rgba(0,0,0,0.1);
    transition: left 0.3s ease;
    overflow-y: auto;
    z-index: 1000;
  }

  .book-menu.active {
    left: 0;
  }

  /* Improve touch targets */
  .book-menu a {
    display: block;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--border-color);
  }

  /* Content shift when menu opens */
  .book-page.menu-open {
    transform: translateX(80%);
  }

  /* Overlay when menu is open */
  .menu-overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    z-index: 999;
  }

  .menu-overlay.active {
    display: block;
  }
}

/* Tablet adjustments */
@media (min-width: 769px) and (max-width: 1024px) {
  .book-menu {
    width: 250px;
  }

  .book-page {
    margin-left: 250px;
  }
}
```

#### Mobile Menu JavaScript
```javascript
// static/js/mobile-menu.js

document.addEventListener('DOMContentLoaded', function() {
  // Create mobile menu toggle
  const toggle = document.createElement('button');
  toggle.className = 'mobile-menu-toggle';
  toggle.innerHTML = '☰';
  toggle.setAttribute('aria-label', 'Toggle menu');
  document.body.appendChild(toggle);

  // Create overlay
  const overlay = document.createElement('div');
  overlay.className = 'menu-overlay';
  document.body.appendChild(overlay);

  const menu = document.querySelector('.book-menu');
  const page = document.querySelector('.book-page');

  // Toggle menu
  toggle.addEventListener('click', function() {
    menu.classList.toggle('active');
    overlay.classList.toggle('active');
    page.classList.toggle('menu-open');

    // Update ARIA
    const isOpen = menu.classList.contains('active');
    toggle.setAttribute('aria-expanded', isOpen);
    toggle.innerHTML = isOpen ? '✕' : '☰';
  });

  // Close on overlay click
  overlay.addEventListener('click', function() {
    menu.classList.remove('active');
    overlay.classList.remove('active');
    page.classList.remove('menu-open');
    toggle.innerHTML = '☰';
  });

  // Close on escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && menu.classList.contains('active')) {
      menu.classList.remove('active');
      overlay.classList.remove('active');
      page.classList.remove('menu-open');
      toggle.innerHTML = '☰';
    }
  });
});
```

### 5.4 Accessibility Implementation

#### ARIA Labels and Semantic HTML
```html
<!-- layouts/_default/baseof.html -->
<!DOCTYPE html>
<html lang="{{ .Site.Language.Lang }}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ .Title }} | {{ .Site.Title }}</title>

  <!-- Skip to content link -->
  <a class="skip-link" href="#main-content">Skip to main content</a>
</head>
<body>
  <!-- Main navigation -->
  <nav class="site-nav" role="navigation" aria-label="Main navigation">
    {{ partial "docs/menu" . }}
  </nav>

  <!-- Main content -->
  <main id="main-content" role="main" aria-label="Main content">
    {{ block "main" . }}{{ end }}
  </main>

  <!-- Search -->
  <div class="search-container" role="search" aria-label="Site search">
    <input type="search"
           id="search-input"
           aria-label="Search documentation"
           placeholder="{{ .Site.Params.search.placeholder }}">
    <div id="search-results" aria-live="polite" aria-atomic="true"></div>
  </div>
</body>
</html>
```

#### Accessibility CSS
```css
/* static/css/accessibility.css */

/* Skip link */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--color-link);
  color: white;
  padding: 8px;
  text-decoration: none;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}

/* Focus indicators */
a:focus,
button:focus,
input:focus,
textarea:focus,
select:focus {
  outline: 3px solid var(--color-link);
  outline-offset: 2px;
}

/* Screen reader only text */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0,0,0,0);
  white-space: nowrap;
  border-width: 0;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .book-menu {
    border: 2px solid currentColor;
  }

  a {
    text-decoration: underline;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Verification Steps - Phase 5
```bash
# 1. Test navigation menu
hugo server -D
# Navigate to http://localhost:1313 and check menu separation

# 2. Test search filtering
# Search for "internal" - should not show blog/internal content

# 3. Test mobile responsiveness
# Use browser dev tools to test at 375px, 768px, 1024px widths

# 4. Test accessibility
# Use axe DevTools or WAVE to check accessibility

# 5. Keyboard navigation test
# Tab through entire page without mouse
```

---

## Phase 6: TECHNICAL OPTIMIZATION
*Dependencies: Phase 5 complete*
*Duration: 1 day*

### 6.1 Asset Optimization

#### Image Processing Configuration
```toml
# config/_default/imaging.toml

[imaging]
  quality = 85
  resampleFilter = "lanczos"

  # Responsive image sizes
  sizes = ["480", "768", "1024", "1366", "1920"]

  # WebP conversion
  format = "webp"

  # Processing hints
  hint = "photo"

  # Background color for transparent images
  bgColor = "#ffffff"
```

#### Image Optimization Script
```bash
#!/bin/bash
# scripts/optimize-images.sh

echo "=== Image Optimization ==="

# Find all images
find static/images -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) | while read img; do
  filename=$(basename "$img")
  dirname=$(dirname "$img")

  # Convert to WebP
  cwebp -q 85 "$img" -o "$dirname/${filename%.*}.webp"

  # Create responsive versions
  for width in 480 768 1024 1366 1920; do
    convert "$img" -resize "${width}x>" "$dirname/${filename%.*}-${width}.${filename##*.}"
  done
done

echo "Images optimized!"
```

#### Lazy Loading Implementation
```html
<!-- layouts/shortcodes/image.html -->
{{ $src := .Get "src" }}
{{ $alt := .Get "alt" }}
{{ $caption := .Get "caption" }}

<figure class="image-container">
  <picture>
    <!-- WebP version -->
    <source type="image/webp"
            srcset="{{ $src | replaceRE "\\.[^.]+$" ".webp" }}"
            media="(min-width: 768px)">

    <!-- Responsive images -->
    <source srcset="{{ $src | replaceRE "\\.[^.]+$" "-480.$1" }}"
            media="(max-width: 480px)">
    <source srcset="{{ $src | replaceRE "\\.[^.]+$" "-768.$1" }}"
            media="(max-width: 768px)">

    <!-- Fallback -->
    <img src="{{ $src }}"
         alt="{{ $alt }}"
         loading="lazy"
         decoding="async">
  </picture>

  {{ if $caption }}
    <figcaption>{{ $caption }}</figcaption>
  {{ end }}
</figure>
```

### 6.2 SEO Configuration

#### SEO Meta Tags
```html
<!-- layouts/partials/seo.html -->
{{ $isInternal := or (hasPrefix .RelPermalink "/blog/") (hasPrefix .RelPermalink "/internal/") }}

<!-- Basic meta tags -->
<meta name="description" content="{{ .Description | default .Site.Params.description }}">
<meta name="author" content="{{ .Params.author | default .Site.Params.author }}">

{{ if $isInternal }}
  <!-- Block internal content from search engines -->
  <meta name="robots" content="noindex, nofollow, noarchive">
  <meta name="googlebot" content="noindex, nofollow">
{{ else }}
  <!-- Public content SEO -->
  <meta name="robots" content="index, follow">

  <!-- Open Graph -->
  <meta property="og:title" content="{{ .Title }}">
  <meta property="og:description" content="{{ .Description | default .Site.Params.description }}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{{ .Permalink }}">
  <meta property="og:image" content="{{ .Params.image | default .Site.Params.images }}">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{{ .Title }}">
  <meta name="twitter:description" content="{{ .Description | default .Site.Params.description }}">
  <meta name="twitter:image" content="{{ .Params.image | default .Site.Params.images }}">

  <!-- JSON-LD Schema -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LearningResource",
    "name": "{{ .Title }}",
    "description": "{{ .Description }}",
    "educationalLevel": "Professional",
    "learningResourceType": "{{ .Params.resourceType | default "Documentation" }}",
    "inLanguage": "{{ .Site.Language.Lang }}",
    "url": "{{ .Permalink }}",
    "datePublished": "{{ .Date.Format "2006-01-02" }}",
    "dateModified": "{{ .Lastmod.Format "2006-01-02" }}",
    "author": {
      "@type": "Organization",
      "name": "{{ .Site.Title }}"
    }
  }
  </script>
{{ end }}

<!-- Canonical URL -->
<link rel="canonical" href="{{ .Permalink }}">
```

#### Sitemap Configuration
```toml
# config/_default/config.toml

[sitemap]
  changefreq = "weekly"
  filename = "sitemap.xml"
  priority = 0.5

# Exclude internal content from sitemap
[params.sitemap]
  exclude = [
    "/blog/**",
    "/internal/**",
    "/tasks/**",
    "/ai-dev-tasks/**"
  ]
```

### 6.3 Performance Monitoring

#### Performance Budget Configuration
```javascript
// scripts/performance-budget.js

const performanceBudget = {
  // Page weight budgets (in KB)
  html: 20,
  css: 50,
  js: 100,
  images: 500,
  fonts: 100,
  total: 800,

  // Timing budgets (in ms)
  firstContentfulPaint: 1500,
  largestContentfulPaint: 2500,
  timeToInteractive: 3500,
  cumulativeLayoutShift: 0.1,
  firstInputDelay: 100
};

// Check performance budget
async function checkPerformanceBudget() {
  const metrics = {
    html: document.documentElement.outerHTML.length / 1024,
    css: Array.from(document.styleSheets).reduce((acc, sheet) => {
      try {
        return acc + Array.from(sheet.cssRules).join('').length / 1024;
      } catch (e) {
        return acc;
      }
    }, 0),
    js: performance.getEntriesByType('resource')
      .filter(r => r.name.endsWith('.js'))
      .reduce((acc, r) => acc + r.transferSize / 1024, 0),
    images: performance.getEntriesByType('resource')
      .filter(r => r.initiatorType === 'img')
      .reduce((acc, r) => acc + r.transferSize / 1024, 0)
  };

  // Generate report
  console.table(metrics);

  // Check against budget
  for (const [key, value] of Object.entries(metrics)) {
    if (value > performanceBudget[key]) {
      console.warn(`⚠️ ${key} exceeds budget: ${value.toFixed(2)}KB > ${performanceBudget[key]}KB`);
    }
  }
}

// Run check on load
window.addEventListener('load', checkPerformanceBudget);
```

#### Monitoring Script
```bash
#!/bin/bash
# scripts/monitor-performance.sh

echo "=== Performance Monitoring ==="

# Build site
hugo --gc --minify --cleanDestinationDir

# Check build size
echo "Build Statistics:"
echo "Total size: $(du -sh public/)"
echo "HTML files: $(find public -name "*.html" | wc -l)"
echo "CSS size: $(find public -name "*.css" -exec du -ch {} + | grep total)"
echo "JS size: $(find public -name "*.js" -exec du -ch {} + | grep total)"

# Run Lighthouse CI
if command -v lighthouse &> /dev/null; then
  lighthouse https://startaitools.com \
    --output=json \
    --output-path=./lighthouse-report.json \
    --only-categories=performance,accessibility,seo

  # Extract scores
  echo "Lighthouse Scores:"
  cat lighthouse-report.json | jq '.categories | {
    performance: .performance.score,
    accessibility: .accessibility.score,
    seo: .seo.score
  }'
fi

# Generate performance report
cat > performance-report.md << EOF
# Performance Report
Date: $(date)

## Build Metrics
- Total Size: $(du -sh public/)
- HTML Files: $(find public -name "*.html" | wc -l)
- Load Time: [Run speed test]

## Recommendations
- Optimize images larger than 100KB
- Minify CSS/JS if not already done
- Enable caching headers
- Consider CDN for static assets
EOF
```

### 6.4 Security Hardening

#### Security Headers
```toml
# netlify.toml - Security headers

[[headers]]
  for = "/*"
  [headers.values]
    # Security headers
    X-Frame-Options = "SAMEORIGIN"
    X-Content-Type-Options = "nosniff"
    X-XSS-Protection = "1; mode=block"
    Referrer-Policy = "strict-origin-when-cross-origin"

    # CSP for public content
    Content-Security-Policy = """
      default-src 'self';
      script-src 'self' 'unsafe-inline' https://www.googletagmanager.com;
      style-src 'self' 'unsafe-inline';
      img-src 'self' data: https:;
      font-src 'self' data:;
      connect-src 'self' https://www.google-analytics.com;
      frame-ancestors 'none';
    """

# Stricter CSP for internal content
[[headers]]
  for = "/blog/*"
  [headers.values]
    Content-Security-Policy = """
      default-src 'self';
      script-src 'none';
      style-src 'self' 'unsafe-inline';
      img-src 'self' data:;
      font-src 'self';
      frame-ancestors 'none';
    """
    X-Robots-Tag = "noindex, nofollow, noarchive, nosnippet"

[[headers]]
  for = "/internal/*"
  [headers.values]
    Content-Security-Policy = """
      default-src 'self';
      script-src 'none';
      frame-ancestors 'none';
    """
    X-Robots-Tag = "noindex, nofollow, noarchive, nosnippet"
```

#### Access Control Implementation
```javascript
// static/js/access-control.js

// Simple access control for internal content
(function() {
  const path = window.location.pathname;
  const isInternal = path.startsWith('/internal/') || path.startsWith('/blog/');

  if (isInternal) {
    // Check for access token
    const hasAccess = localStorage.getItem('internal_access') === 'true';

    if (!hasAccess) {
      // Redirect to home with message
      sessionStorage.setItem('access_denied', 'true');
      window.location.href = '/';
    }

    // Add warning banner
    const banner = document.createElement('div');
    banner.className = 'internal-banner';
    banner.innerHTML = '⚠️ Internal Content - Not for Public Distribution';
    document.body.insertBefore(banner, document.body.firstChild);
  }
})();
```

### Verification Steps - Phase 6
```bash
# 1. Check image optimization
find static/images -name "*.webp" | wc -l

# 2. Validate SEO meta tags
curl -s http://localhost:1313/ | grep -E "<meta.*robots|og:|twitter:"

# 3. Test performance budget
hugo server -D
# Open browser console and check performance metrics

# 4. Verify security headers
curl -I http://localhost:1313/ | grep -E "X-Frame|X-Content|CSP"

# 5. Run full performance audit
./scripts/monitor-performance.sh
```

---

## FINAL IMPLEMENTATION CHECKLIST

### Pre-Implementation
- [ ] Backup entire site
- [ ] Document current URLs for redirect mapping
- [ ] Notify team of planned changes
- [ ] Set up staging environment

### Phase Execution
- [ ] **Phase 1**: Infrastructure Foundation (Day 1)
  - [ ] Fix Hugo configuration
  - [ ] Update build process
  - [ ] Establish performance baseline

- [ ] **Phase 2**: Core Structure (Days 2-3)
  - [ ] Reorganize directories
  - [ ] Implement URL schemes
  - [ ] Add navigation weights

- [ ] **Phase 3**: Content Migration (Days 4-5)
  - [ ] Fix broken links
  - [ ] Categorize content
  - [ ] Execute migration

- [ ] **Phase 4**: Template System (Day 6)
  - [ ] Categorize templates
  - [ ] Implement hub-and-spoke
  - [ ] Set up access control

- [ ] **Phase 5**: User Experience (Days 7-8)
  - [ ] Update navigation
  - [ ] Configure search
  - [ ] Implement accessibility

- [ ] **Phase 6**: Technical Optimization (Day 9)
  - [ ] Optimize assets
  - [ ] Configure SEO
  - [ ] Set up monitoring

### Post-Implementation
- [ ] Run full site audit
- [ ] Test all redirects
- [ ] Verify search indexing
- [ ] Monitor 404 errors for 1 week
- [ ] Gather user feedback
- [ ] Document lessons learned

### Rollback Plan
```bash
# If issues occur at any phase:
./scripts/rollback.sh [phase_number]

# Full rollback:
rm -rf content/
mv backup-[timestamp]/ content/
hugo --gc --minify --cleanDestinationDir
```

---

## SUCCESS METRICS

### Technical Metrics
- ✅ Build warnings: 0
- ✅ Broken links: 0
- ✅ Page load time: < 2s
- ✅ Lighthouse score: > 90

### Content Metrics
- ✅ Internal content separated: 100%
- ✅ Educational content organized: 100%
- ✅ Templates categorized: 100%
- ✅ Duplicate content removed: 100%

### User Experience Metrics
- ✅ Navigation clarity: Clear separation
- ✅ Search accuracy: Public content only
- ✅ Mobile usability: Fully responsive
- ✅ Accessibility: WCAG 2.1 AA compliant

---

*Implementation Plan Version 1.0 - September 14, 2025*
*Total Implementation Time: 9 days*
*Rollback Available: Yes, at each phase*