#!/bin/bash

# Content Migration Script for StartAITools.com
# This script reorganizes content while preserving all URLs using Hugo aliases
# Date: September 14, 2025

echo "=== StartAITools.com Content Migration Script ==="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
CONTENT_DIR="content"
BACKUP_DIR="migration-backup-$(date +%Y%m%d-%H%M%S)"
REDIRECT_FILE="url-redirects.md"
DRY_RUN=${1:-true}

# Function to create backup
create_backup() {
    echo -e "${YELLOW}Creating backup in ${BACKUP_DIR}...${NC}"
    cp -r "$CONTENT_DIR" "$BACKUP_DIR"
    echo -e "${GREEN}✓ Backup created${NC}"
}

# Function to ensure directory exists
ensure_dir() {
    if [ ! -d "$1" ]; then
        if [ "$DRY_RUN" = "false" ]; then
            mkdir -p "$1"
            echo -e "${GREEN}✓ Created directory: $1${NC}"
        else
            echo -e "${BLUE}[DRY RUN] Would create: $1${NC}"
        fi
    fi
}

# Function to add Hugo aliases to preserve old URLs
add_aliases() {
    local file=$1
    local old_url=$2
    local temp_file="${file}.tmp"

    if [ "$DRY_RUN" = "false" ]; then
        # Read existing front matter
        awk '
        /^---$/ {
            if (NR==1) {
                print $0
                in_fm=1
                next
            } else if (in_fm) {
                # Add aliases before closing front matter
                print "aliases:"
                print "  - \"'$old_url'\""
                print $0
                in_fm=0
                next
            }
        }
        { print }
        ' "$file" > "$temp_file"

        mv "$temp_file" "$file"
        echo -e "${GREEN}✓ Added alias to: $file${NC}"
    else
        echo -e "${BLUE}[DRY RUN] Would add alias '$old_url' to: $file${NC}"
    fi
}

# Function to migrate content with URL preservation
migrate_with_redirects() {
    local src=$1
    local dest=$2
    local preserve_url=$3

    if [ -f "$src" ]; then
        if [ "$DRY_RUN" = "false" ]; then
            cp "$src" "$dest"
            if [ "$preserve_url" = "true" ]; then
                # Calculate old URL from source path
                old_url=$(echo "$src" | sed 's|content||' | sed 's|\.md$|/|' | sed 's|_index/|/|')
                add_aliases "$dest" "$old_url"
            fi
            echo -e "${GREEN}✓ Migrated: $src -> $dest${NC}"
        else
            echo -e "${BLUE}[DRY RUN] Would migrate: $src -> $dest${NC}"
        fi
    else
        echo -e "${RED}✗ File not found: $src${NC}"
    fi
}

# Main migration logic
perform_migration() {
    echo -e "\n${YELLOW}=== Starting Content Migration ===${NC}"

    # Create new structure directories
    ensure_dir "$CONTENT_DIR/docs/guides"
    ensure_dir "$CONTENT_DIR/docs/projects"
    ensure_dir "$CONTENT_DIR/docs/reference"
    ensure_dir "$CONTENT_DIR/docs/reference/templates"
    ensure_dir "$CONTENT_DIR/blog"
    ensure_dir "$CONTENT_DIR/resources"

    # Consolidate blog content
    echo -e "\n${YELLOW}Consolidating blog posts...${NC}"

    # Move posts to blog (with redirects)
    for post in $CONTENT_DIR/posts/*.md; do
        if [ -f "$post" ]; then
            filename=$(basename "$post")
            migrate_with_redirects "$post" "$CONTENT_DIR/blog/$filename" true
        fi
    done

    # Move docs/blog content to main blog (with redirects)
    if [ -d "$CONTENT_DIR/docs/blog" ]; then
        for post in $CONTENT_DIR/docs/blog/*.md; do
            if [ -f "$post" ]; then
                filename=$(basename "$post")
                # Skip _index.md files
                if [ "$filename" != "_index.md" ]; then
                    migrate_with_redirects "$post" "$CONTENT_DIR/blog/archived-$filename" true
                fi
            fi
        done
    fi

    # Reorganize documentation
    echo -e "\n${YELLOW}Reorganizing documentation...${NC}"

    # Move security guides to guides section
    if [ -d "$CONTENT_DIR/docs/security" ]; then
        ensure_dir "$CONTENT_DIR/docs/guides/security"
        for file in $CONTENT_DIR/docs/security/*.md; do
            if [ -f "$file" ]; then
                filename=$(basename "$file")
                migrate_with_redirects "$file" "$CONTENT_DIR/docs/guides/security/$filename" true
            fi
        done
    fi

    # Move AI/ML guides to guides section
    if [ -d "$CONTENT_DIR/docs/ai-ml" ]; then
        ensure_dir "$CONTENT_DIR/docs/guides/ai-ml"
        for file in $CONTENT_DIR/docs/ai-ml/*.md; do
            if [ -f "$file" ]; then
                filename=$(basename "$file")
                migrate_with_redirects "$file" "$CONTENT_DIR/docs/guides/ai-ml/$filename" true
            fi
        done
    fi

    # Move templates to reference section
    if [ -d "$CONTENT_DIR/docs/templates" ]; then
        for file in $CONTENT_DIR/docs/templates/*.md; do
            if [ -f "$file" ]; then
                filename=$(basename "$file")
                migrate_with_redirects "$file" "$CONTENT_DIR/docs/reference/templates/$filename" true
            fi
        done
    fi

    # Create index files for new sections
    echo -e "\n${YELLOW}Creating index files...${NC}"

    # Create guides index
    cat > "$CONTENT_DIR/docs/guides/_index.md.new" << 'EOF'
---
title: "Guides"
weight: 20
bookToc: true
bookCollapseSection: true
description: "Technical guides and tutorials for AI development"
aliases:
  - "/docs/ai-ml/"
  - "/docs/security/"
---

# Technical Guides

Comprehensive guides covering AI/ML, security, architecture, and development workflows.

## Categories

### AI & Machine Learning
- [Prompt Engineering](/docs/guides/ai-ml/prompt-engineering/)
- [Model Selection](/docs/guides/ai-ml/model-selection/)
- [RAG Implementation](/docs/guides/ai-ml/rag-implementation/)

### Security
- [Linux Security](/docs/guides/security/linux-security/)
- [SSH Configuration](/docs/guides/security/ssh-configuration/)
- [Access Control](/docs/guides/security/access-control/)

### Architecture
- [System Design](/docs/guides/architecture/system-design/)
- [Microservices](/docs/guides/architecture/microservices/)
- [Cloud Patterns](/docs/guides/architecture/cloud-patterns/)
EOF

    if [ "$DRY_RUN" = "false" ]; then
        mv "$CONTENT_DIR/docs/guides/_index.md.new" "$CONTENT_DIR/docs/guides/_index.md"
        echo -e "${GREEN}✓ Created guides index${NC}"
    else
        echo -e "${BLUE}[DRY RUN] Would create guides index${NC}"
    fi

    # Create reference index
    cat > "$CONTENT_DIR/docs/reference/_index.md.new" << 'EOF'
---
title: "Reference"
weight: 60
bookToc: true
bookCollapseSection: true
description: "Templates, API documentation, and technical reference"
aliases:
  - "/docs/templates/"
---

# Reference Documentation

Templates, API documentation, and technical reference materials.

## Templates

Professional documentation templates for AI development:

### Development Templates
- [PRD Template](/docs/reference/templates/create-prd/)
- [Tech Spec Template](/docs/reference/templates/create-tech-spec/)
- [API Spec Template](/docs/reference/templates/create-api-spec/)

### Project Management
- [Project Charter](/docs/reference/templates/create-project-charter/)
- [RACI Matrix](/docs/reference/templates/create-raci-matrix/)
- [Risk Register](/docs/reference/templates/create-risk-register/)

### Operations
- [Runbook Template](/docs/reference/templates/create-runbook/)
- [SOP Template](/docs/reference/templates/create-sop/)
- [Post-Mortem Template](/docs/reference/templates/create-post-mortem/)
EOF

    if [ "$DRY_RUN" = "false" ]; then
        mv "$CONTENT_DIR/docs/reference/_index.md.new" "$CONTENT_DIR/docs/reference/_index.md"
        echo -e "${GREEN}✓ Created reference index${NC}"
    else
        echo -e "${BLUE}[DRY RUN] Would create reference index${NC}"
    fi
}

# Function to generate nginx redirect rules
generate_nginx_redirects() {
    echo -e "\n${YELLOW}=== Generating Nginx Redirect Rules ===${NC}"

    cat > "nginx-redirects.conf" << 'EOF'
# Nginx redirect rules for StartAITools.com content migration
# Add these to your server block

# Blog consolidation redirects
location ~ ^/posts/(.*)$ {
    return 301 /blog/$1;
}

location ~ ^/docs/blog/(.*)$ {
    return 301 /blog/$1;
}

# Documentation reorganization redirects
location ~ ^/docs/ai-ml/(.*)$ {
    return 301 /docs/guides/ai-ml/$1;
}

location ~ ^/docs/security/(.*)$ {
    return 301 /docs/guides/security/$1;
}

location ~ ^/docs/templates/(.*)$ {
    return 301 /docs/reference/templates/$1;
}

# Journey to blog archive redirect
location ~ ^/docs/journey/(.*)$ {
    return 301 /blog/$1;
}

# Library to resources redirect
location ~ ^/library/(.*)$ {
    return 301 /resources/$1;
}

# Learning to getting-started redirect
location ~ ^/learning/(.*)$ {
    return 301 /docs/getting-started/$1;
}
EOF

    echo -e "${GREEN}✓ Nginx redirects saved to: nginx-redirects.conf${NC}"
}

# Function to generate Netlify redirect rules
generate_netlify_redirects() {
    echo -e "\n${YELLOW}=== Generating Netlify Redirect Rules ===${NC}"

    cat > "_redirects" << 'EOF'
# Netlify redirect rules for StartAITools.com content migration
# Add these to your public/_redirects file

# Blog consolidation redirects
/posts/*        /blog/:splat    301
/docs/blog/*    /blog/:splat    301

# Documentation reorganization redirects
/docs/ai-ml/*       /docs/guides/ai-ml/:splat       301
/docs/security/*    /docs/guides/security/:splat    301
/docs/templates/*   /docs/reference/templates/:splat 301

# Journey to blog archive redirect
/docs/journey/*     /blog/:splat    301

# Library to resources redirect
/library/*          /resources/:splat   301

# Learning to getting-started redirect
/learning/*         /docs/getting-started/:splat    301
EOF

    echo -e "${GREEN}✓ Netlify redirects saved to: _redirects${NC}"
}

# Function to generate migration report
generate_migration_report() {
    echo -e "\n${YELLOW}=== Generating Migration Report ===${NC}"

    cat > "migration-report.md" << 'EOF'
# Content Migration Report

## Date: $(date)

## Migration Summary

### Old Structure → New Structure

1. **Blog Consolidation**
   - `/posts/` → `/blog/`
   - `/docs/blog/` → `/blog/` (as archived-)

2. **Documentation Reorganization**
   - `/docs/ai-ml/` → `/docs/guides/ai-ml/`
   - `/docs/security/` → `/docs/guides/security/`
   - `/docs/templates/` → `/docs/reference/templates/`
   - `/docs/workflow/` → `/docs/guides/workflow/`

3. **Redirects**
   - `/docs/journey/` → `/blog/`
   - `/library/` → `/resources/`
   - `/learning/` → `/docs/getting-started/`

## URL Preservation

All old URLs are preserved using Hugo aliases. Users visiting old URLs will be automatically redirected to new locations.

## Implementation Steps

1. Run migration script in dry-run mode first
2. Review proposed changes
3. Run migration script in execute mode
4. Deploy and test all redirects
5. Update internal links in content
6. Monitor 404 errors for missed redirects

## Rollback Plan

If issues occur:
1. Restore from backup directory
2. Remove redirect rules
3. Redeploy original structure

## Testing Checklist

- [ ] All old URLs redirect correctly
- [ ] Navigation works in new structure
- [ ] Search index updated
- [ ] No 404 errors for existing content
- [ ] RSS feeds still work
- [ ] External links still valid
EOF

    echo -e "${GREEN}✓ Migration report saved to: migration-report.md${NC}"
}

# Main execution
main() {
    echo -e "${YELLOW}Content Migration Script${NC}"
    echo -e "${YELLOW}Mode: $([ "$DRY_RUN" = "true" ] && echo "DRY RUN" || echo "EXECUTE")${NC}"
    echo ""

    if [ "$DRY_RUN" = "true" ]; then
        echo -e "${BLUE}This is a DRY RUN. No files will be modified.${NC}"
        echo -e "${BLUE}To execute migration, run: $0 false${NC}"
        echo ""
    else
        echo -e "${RED}WARNING: This will reorganize your content structure!${NC}"
        echo -e "${YELLOW}Backup will be created in: $BACKUP_DIR${NC}"
        echo ""
        read -p "Continue with migration? (y/n): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Migration cancelled."
            exit 1
        fi

        create_backup
    fi

    # Perform migration
    perform_migration

    # Generate redirect configurations
    generate_nginx_redirects
    generate_netlify_redirects
    generate_migration_report

    echo ""
    echo -e "${GREEN}=== Migration Complete ===${NC}"

    if [ "$DRY_RUN" = "true" ]; then
        echo -e "${YELLOW}Review the proposed changes above.${NC}"
        echo -e "${YELLOW}To execute migration, run: $0 false${NC}"
    else
        echo -e "${GREEN}✓ Content migrated successfully${NC}"
        echo -e "${GREEN}✓ Backup created in: $BACKUP_DIR${NC}"
        echo -e "${GREEN}✓ Redirect rules generated${NC}"
        echo ""
        echo -e "${YELLOW}Next steps:${NC}"
        echo "1. Add _redirects file to static/ directory"
        echo "2. Run 'hugo server' to test locally"
        echo "3. Commit and deploy changes"
        echo "4. Monitor for 404 errors"
        echo ""
        echo -e "${YELLOW}To rollback:${NC}"
        echo "rm -rf content && mv $BACKUP_DIR content"
    fi
}

# Run main function
main