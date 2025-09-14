# PRD: Hugo Website Arcade Theme Restructure

**Date**: September 14, 2025
**Author**: Jeremy Longshore
**Status**: Approved
**Implementation Timeline**: 3-4 days

## Introduction/Overview

Transform StartAITools.com into a beginner-friendly AI learning playground with an engaging retro arcade aesthetic and intelligent auto-linking glossary system. This restructure will create clear separation between internal business content and public educational resources while making the site irresistibly fun and approachable for new developers.

**Problem**: Current site has navigation issues, broken links, mixed content types, and isn't optimized for beginners who want quick wins with AI tools.

**Solution**: Complete technological restructure with arcade theme, auto-linking glossary, and newbie-friendly content organization that gets users building in under 10 minutes.

## Goals

1. **Achieve < 10 minute time-to-first-success** for complete beginners
2. **Implement clean content separation** (internal/blog vs public/educational)
3. **Create engaging arcade-themed UI** that makes learning fun without being childish
4. **Deploy auto-linking glossary** for 50-100 core tech terms
5. **Fix all broken links and navigation issues** identified in audit
6. **Maintain zero downtime** during migration with proper redirects

## User Stories

1. **As a complete beginner**, I want to build my first AI tool in under 10 minutes so that I feel accomplished and motivated to continue learning.

2. **As a junior developer**, I want technical terms automatically explained via tooltips so that I can understand content without constantly googling.

3. **As a returning visitor**, I want to track my learning progress and unlock achievements so that I stay engaged and motivated.

4. **As a mobile user**, I want a responsive experience that works perfectly on my phone so that I can learn on the go.

5. **As the site owner**, I want internal business content separated from public content so that PRDs and personal projects aren't indexed by search engines.

## Functional Requirements

### Phase 1: Core Infrastructure (Priority: Critical)
1. System must fix all Hugo deprecation warnings (Twitter → X)
2. System must update Hugo version to 0.150.0
3. System must implement SEO configuration blocking internal content
4. System must create robots.txt blocking /blog/, /internal/, /tasks/
5. System must add security headers for internal content

### Phase 2: Content Restructuring (Priority: Critical)
6. System must reorganize directories into /docs/ (public) and /blog/ (internal)
7. System must implement navigation weights for consistent ordering
8. System must fix all broken internal links automatically
9. System must remove /docs/journey/ and migrate to /blog/
10. System must create Hugo aliases for all moved content (zero broken URLs)

### Phase 3: Content Migration (Priority: Critical)
11. System must move all PRDs, ADRs, and tasks to /internal/
12. System must update all "blog archive" references to just "blog"
13. System must separate templates (educational → /docs/reference/, business → /internal/)
14. System must maintain all existing URLs via redirects

### Phase 4: Arcade Theme (Priority: High)
15. System must implement Pac-Man color scheme (yellow, cyan, pink, black)
16. System must add subtle animations (no performance impact)
17. System must create gaming-inspired navigation with hover effects
18. System must maintain professional appearance suitable for tech audience

### Phase 5: Auto-Linking Glossary (Priority: High)
19. System must auto-link 50-100 core tech terms in all content
20. System must show tooltips on hover with definitions
21. System must track which terms users have viewed/learned
22. System must provide glossary page with all terms searchable
23. System must exclude code blocks from auto-linking

### Phase 6: Beginner Experience (Priority: High)
24. System must provide skill-level selector (beginner/intermediate/advanced)
25. System must adapt content visibility based on skill level
26. System must show progress tracking with visual indicators
27. System must implement achievement system for milestones
28. System must provide "5-minute setup" quick start guide

### Phase 7: Mobile Optimization (Priority: Medium)
29. System must be fully responsive at 375px, 768px, 1024px+ widths
30. System must have touch-friendly navigation with adequate tap targets
31. System must optimize animations for mobile performance

## Non-Goals (Out of Scope)

1. Will NOT implement authentication or login systems
2. Will NOT add sound effects or music (too annoying)
3. Will NOT create PWA or offline functionality
4. Will NOT import full 1000+ term glossaries (start small)
5. Will NOT implement commenting or community features
6. Will NOT integrate external APIs or services
7. Will NOT change from Hugo to another platform

## Design Considerations

- **Theme**: Subtle retro arcade aesthetic - professional with gaming hints
- **Colors**: Pac-Man palette but muted for readability
- **Typography**: Monospace for headers, clean sans-serif for body
- **Animations**: CSS-only, respect prefers-reduced-motion
- **Mobile**: Touch targets minimum 44x44px
- **Accessibility**: WCAG 2.1 AA compliant

## Technical Considerations

- **Hugo Version**: Must work with 0.150.0 (no upgrades)
- **Build Time**: Keep under 30 seconds
- **Page Weight**: Under 500KB per page
- **JavaScript**: Minimal, progressive enhancement only
- **Browser Support**: Last 2 versions of major browsers
- **Hosting**: Netlify with existing configuration
- **Dependencies**: No new build tools or npm packages

## Success Metrics

1. **Time to first success**: < 10 minutes for beginners
2. **Build warnings**: 0
3. **Broken links**: 0
4. **Lighthouse scores**: > 90 for performance, accessibility, SEO
5. **Mobile usability**: 100% responsive
6. **Glossary engagement**: > 30% of users click at least one term
7. **Page load time**: < 2 seconds on 3G
8. **Bounce rate reduction**: -20% within first month

## Open Questions

1. Should we add a "copy code" button to all code blocks?
2. Do we want to track anonymous analytics for learning paths?
3. Should glossary terms have pronunciation guides?
4. Do we want to add social sharing for achievements?
5. Should we implement a sitemap.xml for better SEO?