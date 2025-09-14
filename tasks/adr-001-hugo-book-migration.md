# ADR-001: Migrate from Archie to Hugo Book Theme

**Date**: 2025-09-14
**Status**: Accepted

## Context

The StartAITools website currently uses the Archie theme, which is a minimal blog theme designed for simple article publishing. However, the site's content has grown to include comprehensive technical guides, an AI/ML curriculum, Linux security documentation, and various interconnected learning materials. The current theme lacks the organizational capabilities needed for a knowledge base with glossaries, learning paths, and indexed navigation that allows users to "jump around as they please" through interconnected content.

Jeremy wants to transform the site into a mixed documentation/blog platform that serves as both a personal learning repository and professional knowledge showcase, with features like technical glossaries, categorized articles, and structured learning paths.

## Decision

We will migrate from the Archie theme to the Hugo Book theme, which is specifically designed for documentation sites and knowledge bases. Hugo Book provides built-in support for:
- Hierarchical content organization with collapsible sidebar navigation
- Previous/Next navigation between pages
- Built-in search functionality (Lunr.js)
- Table of contents generation
- Code syntax highlighting with copy buttons
- Clean, minimalistic documentation-focused design
- Mobile-responsive collapsible navigation

## Consequences

### Positive
- **Improved Content Organization**: Hierarchical structure with nested sections perfect for organizing reports, essays, and technical documentation
- **Better Navigation**: Collapsible sidebar and Previous/Next navigation makes it easy to explore interconnected content
- **Enhanced Learning Experience**: Built-in support for learning paths and sequential content progression
- **Glossary Support**: Native capabilities for implementing technical glossaries and dictionaries
- **Search Functionality**: Lunr.js search is lighter weight than current Pagefind integration
- **Documentation-First Design**: Clean, minimalistic interface optimized for reading technical content
- **Feature-Rich Out of Box**: Most requested features (TOC, syntax highlighting, version switcher) are built-in
- **Mobile Optimization**: Responsive design with collapsible navigation works well on all devices
- **Immediate Deployment**: Can switch directly to production once tested

### Negative
- **Migration Effort**: Need to restructure all content to fit Hugo Book's organizational model
- **Learning Curve**: Team needs to learn Hugo Book's specific conventions and configuration
- **URL Changes**: Some URLs may change, requiring redirects to maintain SEO
- **Theme Lock-in**: Future theme changes will be more complex due to Hugo Book's specific structure
- **Customization Limits**: Staying with default theme means less visual differentiation

## Alternatives Considered

### Option 1: Stay with Archie Theme
- **Pros**: No migration needed, familiar system, already configured
- **Cons**: Lacks documentation features, no hierarchical navigation, limited for knowledge base needs
- **Reason for rejection**: Does not meet the requirements for a mixed documentation/blog platform with glossaries and learning paths

### Option 2: Custom Theme Development
- **Pros**: Perfectly tailored to specific needs, unique visual identity
- **Cons**: High development effort, ongoing maintenance burden, longer timeline
- **Reason for rejection**: User wants immediate deployment and minimal customization focus

### Option 3: Docsy Theme
- **Pros**: Google-backed, enterprise documentation features, highly customizable
- **Cons**: More complex setup, heavier framework, steeper learning curve
- **Reason for rejection**: Overly complex for current needs, user prefers clean minimalistic approach

### Option 4: PaperMod Theme (Already in themes/)
- **Pros**: Modern blog theme, already downloaded, good performance
- **Cons**: Still blog-focused, lacks documentation organization features
- **Reason for rejection**: Does not provide the documentation-specific features needed

## Implementation

1. **Install Hugo Book Theme**
   ```bash
   git submodule add https://github.com/alex-shpak/hugo-book themes/hugo-book
   ```

2. **Create New Configuration**
   - Copy current hugo.toml to hugo.toml.backup
   - Create new configuration for Hugo Book with existing site parameters

3. **Content Restructuring**
   ```
   content/
   ├── docs/          # Documentation sections
   ├── posts/         # Blog posts (preserved)
   ├── learning/      # Learning paths
   ├── glossary/      # Technical terms
   └── [static pages] # About, Contact, etc.
   ```

4. **Migration Process**
   - Move blog posts to appropriate sections
   - Create learning path structure for AI/ML curriculum
   - Set up glossary system
   - Configure search indexing
   - Update Netlify build configuration

5. **Testing & Deployment**
   - Test all functionality locally
   - Verify all content renders correctly
   - Check mobile responsiveness
   - Deploy immediately to production (as requested)

## References

- [Hugo Book Theme Documentation](https://github.com/alex-shpak/hugo-book)
- [Hugo Book Demo Site](https://hugo-book-demo.netlify.app/)
- [PRD: Hugo Book Theme Migration](/tasks/prd-hugo-book-migration.md)
- [Current Site Analysis](/tasks/site-audit-2025-09-14.md)
- [Hugo Documentation](https://gohugo.io/documentation/)