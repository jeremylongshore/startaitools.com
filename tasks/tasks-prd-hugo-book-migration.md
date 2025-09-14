## Relevant Files

- `themes/hugo-book/` - Hugo Book theme directory (to be added as submodule)
- `hugo.toml` - Main Hugo configuration file (needs complete rewrite for Hugo Book)
- `hugo.toml.backup` - Backup of original Archie configuration
- `netlify.toml` - Netlify build configuration (needs update for new build process)
- `content/_index.md` - Home page content (needs restructuring)
- `content/docs/` - New documentation section directory
- `content/learning/` - New learning paths directory
- `content/glossary/` - New glossary/dictionary directory
- `layouts/` - Custom layout overrides (may need updates)
- `assets/css/` - Custom CSS files (review for compatibility)

### Notes

- Hugo Book uses a different configuration structure than Archie
- Content organization will follow Hugo Book's hierarchical model
- Search will switch from Pagefind to Lunr.js (built into Hugo Book)
- All existing blog posts will be preserved but reorganized

## Tasks

- [ ] 1.0 Theme Installation and Setup
  - [ ] 1.1 Add Hugo Book theme as Git submodule
  - [ ] 1.2 Verify theme installation and file structure
  - [ ] 1.3 Create backup of current Archie theme configuration
  - [ ] 1.4 Document current customizations for reference

- [ ] 2.0 Configuration Migration
  - [ ] 2.1 Create new hugo.toml for Hugo Book configuration
  - [ ] 2.2 Migrate site parameters (title, subtitle, social links)
  - [ ] 2.3 Configure Hugo Book specific parameters
  - [ ] 2.4 Set up menu structure for sidebar navigation
  - [ ] 2.5 Configure search settings for Lunr.js

- [ ] 3.0 Content Structure Creation
  - [ ] 3.1 Create /content/docs/ directory for documentation
  - [ ] 3.2 Create /content/learning/ directory for learning paths
  - [ ] 3.3 Create /content/glossary/ directory for technical terms
  - [ ] 3.4 Set up _index.md files for each section with proper front matter
  - [ ] 3.5 Configure bookHidden parameters for TOC-only sections

- [ ] 4.0 Content Migration and Organization
  - [ ] 4.1 Analyze existing 12 blog posts for categorization
  - [ ] 4.2 Identify AI/ML curriculum posts and supporting documents
  - [ ] 4.3 Move posts to appropriate sections (docs/learning/posts)
  - [ ] 4.4 Update front matter for Hugo Book compatibility
  - [ ] 4.5 Create learning path structure for AI curriculum
  - [ ] 4.6 Migrate static pages (about, contact, projects, resume)
  - [ ] 4.7 Set up proper weight parameters for content ordering

- [ ] 5.0 Feature Implementation
  - [ ] 5.1 Configure table of contents generation
  - [ ] 5.2 Set up Previous/Next navigation
  - [ ] 5.3 Implement code syntax highlighting with copy buttons
  - [ ] 5.4 Create initial glossary entries
  - [ ] 5.5 Set up comments system integration
  - [ ] 5.6 Configure version/language switcher
  - [ ] 5.7 Add Edit on GitHub links

- [ ] 6.0 Testing and Verification
  - [ ] 6.1 Test local development server
  - [ ] 6.2 Verify all content renders correctly
  - [ ] 6.3 Test navigation and sidebar functionality
  - [ ] 6.4 Verify search functionality works
  - [ ] 6.5 Test mobile responsiveness
  - [ ] 6.6 Check all internal links and references
  - [ ] 6.7 Validate Previous/Next navigation flow

- [ ] 7.0 Deployment Preparation
  - [ ] 7.1 Update netlify.toml for Hugo Book
  - [ ] 7.2 Remove Pagefind configuration
  - [ ] 7.3 Set up 301 redirects for changed URLs
  - [ ] 7.4 Test build command locally
  - [ ] 7.5 Create deployment checklist

- [ ] 8.0 Production Deployment
  - [ ] 8.1 Commit all changes to Git
  - [ ] 8.2 Push to main branch
  - [ ] 8.3 Monitor Netlify build process
  - [ ] 8.4 Verify production site functionality
  - [ ] 8.5 Test key user journeys on live site