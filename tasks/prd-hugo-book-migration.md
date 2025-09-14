# Product Requirements Document: Hugo Book Theme Migration

## Introduction/Overview

This PRD outlines the migration of the StartAITools website from the current Archie theme to Hugo Book theme, transforming it into a comprehensive knowledge base and learning center. The goal is to create a blog-style site with reports, essays, and documents with an indexed directory structure allowing users to "jump around as they please". The site will combine technical documentation with nested chapters, a learning center with tutorials, and a knowledge base with categorized articles and glossary/dictionary features. The site will serve as Jeremy's personal learning repository and professional knowledge showcase.

## Goals

1. **Transform the site into a mixed documentation/blog platform** with indexed, interconnected content
2. **Organize existing content into learning paths and categories** for better knowledge discovery
3. **Implement a glossary/dictionary system** for technical terms and concepts
4. **Maintain clean, minimalistic design** focusing on content accessibility
5. **Preserve SEO value** while improving content organization
6. **Enable immediate deployment** with full feature parity from day one

## User Stories

1. **As a learner**, I want to navigate through interconnected technical documents and tutorials so that I can build knowledge progressively
2. **As a site visitor**, I want to quickly find specific technical information through categorized content and search functionality
3. **As Jeremy**, I want to organize my AI/ML curriculum and supporting documents into a cohesive learning structure
4. **As a technical reader**, I want to access glossary definitions and related content while reading
5. **As a mobile user**, I want to easily navigate the documentation structure on my device
6. **As a contributor**, I want to provide feedback or comments on content

## Functional Requirements

1. **Content Structure**
   - The system must support mixed content types (blog posts, reports, essays, documentation, tutorials, glossaries)
   - The system must organize content into collapsible sidebar sections with "jump around as you please" navigation
   - The system must support nested chapters and sections for documentation
   - The system must maintain blog-style presentation with reports, essays, and documents

2. **Navigation**
   - The system must provide sidebar navigation with collapsible sections (Hugo Book default)
   - The system must include Previous/Next navigation between related pages (important per user)
   - The system must show current location in the content hierarchy
   - The system must support keyboard navigation shortcuts
   - The system must maintain clean, minimalistic interface without breadcrumbs

3. **Content Migration**
   - The system must preserve all existing blog posts (12 posts)
   - The system must reorganize posts into learning paths/categories (user interested in this approach)
   - The system must review and identify AI/ML curriculum content with supporting documents and links
   - The system must maintain all static pages (about, contact, projects, resume)

4. **Search Functionality**
   - The system must implement Hugo Book's built-in search (Lunr.js) as primary search
   - The system must index all content for full-text search
   - The system must provide search results with context snippets

5. **Content Features**
   - The system must generate table of contents for each page
   - The system must provide code syntax highlighting with copy buttons ("all the tech bros use it" - user wants this)
   - The system must support markdown extensions for enhanced formatting
   - The system must enable comments/feedback system integration (user requested)
   - The system must support version/language switcher (user approved)

6. **Glossary System**
   - The system must support a comprehensive technical glossary/dictionary (user specifically wants this)
   - The system must allow inline term definitions
   - The system must provide a centralized glossary page
   - The system must link glossary terms throughout content
   - The system must include dictionary-type word definitions

7. **Learning Paths**
   - The system must organize related content into learning paths (user finds this interesting)
   - The system must utilize existing learning center tutorials by topic/difficulty where material exists
   - The system must support the existing AI/ML curriculum structure

8. **Version Control**
   - The system must support version/language switcher functionality (user approved)
   - The system must provide Edit on GitHub links for content

## Non-Goals (Out of Scope)

1. **Will not** create custom theme modifications beyond Hugo Book's configuration options
2. **Will not** implement custom authentication or user accounts
3. **Will not** build a custom CMS or admin interface
4. **Will not** migrate to a different hosting platform (stays on Netlify)
5. **Will not** implement real-time collaborative features
6. **Will not** create mobile applications
7. **Will not** implement e-commerce or payment features

## Design Considerations

- **Theme**: Use Hugo Book's default clean documentation style (user preference)
- **Customization**: Minimal changes, focus on functionality over aesthetics (user wants clean, minimalistic)
- **Layout**: Clean, minimalistic design with focus on readability (user emphasis on clean/minimal)
- **Typography**: Use theme defaults for consistency
- **Color Scheme**: Maintain Hugo Book's default colors
- **Mobile**: Responsive design with collapsible sidebar for mobile devices
- **Print**: Utilize Hugo Book's print-friendly layouts
- **UX/UI**: Let the system determine what makes most sense for user experience (user delegated this decision)

## Technical Considerations

### Dependencies
- Hugo Book theme (latest version)
- Hugo 0.149.1 (maintain current version for compatibility)
- Lunr.js (included with Hugo Book)
- Node.js 18 (for build process)

### Migration Steps
1. Install Hugo Book theme as Git submodule
2. Create new configuration file for Hugo Book
3. Restructure content directories for book layout
4. Migrate existing content to new structure
5. Set up glossary system using Hugo Book's features
6. Configure search indexing
7. Update Netlify build configuration
8. Test all functionality locally
9. Deploy to production (immediate switch as requested by user)

### URL Strategy
- Maintain `/posts/` for blog content (preserve SEO)
- Add `/docs/` for documentation sections
- Add `/glossary/` for technical terms
- Add `/learning/` for structured tutorials
- Implement 301 redirects for any changed URLs

### Content Organization
```
content/
├── _index.md           # Home page
├── docs/               # Documentation section
│   ├── _index.md
│   ├── getting-started/
│   ├── guides/
│   └── reference/
├── posts/              # Blog posts (existing)
├── learning/           # Learning paths
│   ├── ai-curriculum/
│   ├── linux-security/
│   └── devops/
├── glossary/           # Technical glossary
├── about.md           # Static pages
├── contact.md
├── projects.md
└── resume.md
```

## Success Metrics

1. **All existing content successfully migrated** without broken links
2. **Search functionality returns relevant results** within 200ms
3. **Site builds and deploys successfully** on Netlify
4. **Mobile navigation works smoothly** on all devices
5. **Previous/Next navigation correctly links** related content
6. **Glossary terms are properly linked** throughout content
7. **Comments/feedback system is functional** (if implemented)
8. **Page load time remains under 2 seconds**

## Open Questions

1. **Comments System**: Which commenting platform should be integrated? (Disqus, Utterances, Giscus, or other?)
2. **Analytics**: Should Google Analytics or another analytics platform be configured?
3. **RSS Feeds**: Should separate RSS feeds be maintained for blog and documentation?
4. **Sitemap**: Should a custom sitemap be generated for better SEO?
5. **Content Review**: Which existing posts should be prioritized for learning path organization?
6. **Glossary Scope**: What technical terms should be included in the initial glossary?
7. **Backup Strategy**: Should the current Archie theme setup be preserved as a backup?
8. **Testing Period**: Should there be a staging URL for testing before immediate switch?

## Implementation Notes

This migration represents a significant transformation from a simple blog to a comprehensive knowledge platform. The Hugo Book theme provides all necessary features out of the box, minimizing custom development. The immediate deployment strategy requires careful testing of all functionality before the switch.

The focus should be on:
1. Preserving all existing content and URLs
2. Organizing content logically for learning
3. Maintaining clean, fast performance
4. Ensuring mobile responsiveness
5. Setting up sustainable content management workflows

---

*PRD Created: 2025-09-14*
*Target Implementation: Immediate upon approval*