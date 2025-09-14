## Relevant Files

- `hugo.toml` - Main Hugo configuration file for deprecation fixes and theme settings
- `netlify.toml` - Deployment configuration for build settings and headers
- `content/docs/_index.md` - Documentation section index with navigation weights
- `content/blog/_index.md` - Blog section index (will contain all posts including internal)
- `static/css/arcade-theme.css` - New arcade theme stylesheet to create
- `static/js/tech-glossary.js` - Auto-linking glossary JavaScript to create
- `static/js/beginner-friendly.js` - Skill level adaptation and progress tracking
- `layouts/robots.txt` - Robots template for SEO control
- `scripts/fix-broken-links.sh` - Script to fix all broken internal links
- `scripts/migrate-content.sh` - Content migration and reorganization script
- `data/glossary.json` - Tech glossary data structure
- `content/glossary/_index.md` - Interactive glossary page

### Notes

- All scripts should be created in a `scripts/` directory for organization
- CSS and JS files go in `static/` for direct serving
- Test each phase locally with `hugo server -D` before moving to next phase
- Use `npx jest` to run any tests if created

## Tasks

- [ ] 1.0 Fix Infrastructure Foundation
  - [ ] 1.1 Update hugo.toml to fix Twitter deprecation (change privacy.twitter to privacy.x)
  - [ ] 1.2 Add SEO configuration with meta description and keywords to hugo.toml params
  - [ ] 1.3 Add Open Graph image defaults to params section
  - [ ] 1.4 Configure robotsNoIndex for blog sections in params
  - [ ] 1.5 Set markup.goldmark.renderer.unsafe to false for security
  - [ ] 1.6 Create robots.txt template in layouts/ blocking sensitive paths
  - [ ] 1.7 Update netlify.toml with Hugo version 0.150.0
  - [ ] 1.8 Add security headers (X-Robots-Tag, Cache-Control) to netlify.toml
  - [ ] 1.9 Add netlify-plugin-checklinks for broken link detection
  - [ ] 1.10 Create package.json with postbuild scripts
  - [ ] 1.11 Create performance-baseline.sh monitoring script
  - [ ] 1.12 Test build with no warnings

- [ ] 2.0 Restructure Content Organization
  - [ ] 2.1 Create scripts/ directory for all automation scripts
  - [ ] 2.2 Write fix-broken-links.sh script with backup functionality
  - [ ] 2.3 Run comprehensive link audit with grep commands
  - [ ] 2.4 Fix all /docs/journey/ links to redirect to /blog/
  - [ ] 2.5 Fix /tasks/ links to use correct paths
  - [ ] 2.6 Fix /library/ links to redirect to /resources/
  - [ ] 2.7 Update all "blog archive" text references to just "blog"
  - [ ] 2.8 Create weight assignment script for consistent navigation
  - [ ] 2.9 Apply weights to all _index.md files (10-100 scale)
  - [ ] 2.10 Add Hugo aliases to all moved content for zero broken URLs
  - [ ] 2.11 Create migration-report.md documenting all changes
  - [ ] 2.12 Verify all redirects work with curl tests

- [ ] 3.0 Implement Arcade Theme
  - [ ] 3.1 Create static/css/arcade-theme.css file
  - [ ] 3.2 Define Pac-Man color variables (yellow, cyan, pink, orange, black)
  - [ ] 3.3 Create ghost color scheme for different sections
  - [ ] 3.4 Add pac-chomp animation keyframes
  - [ ] 3.5 Add ghost-float animation keyframes
  - [ ] 3.6 Add power-pellet-glow animation for CTAs
  - [ ] 3.7 Style navigation with gaming hover effects and transitions
  - [ ] 3.8 Apply arcade styling to headers with glow effects
  - [ ] 3.9 Style code blocks with terminal/matrix green theme
  - [ ] 3.10 Create button styles with gradient backgrounds
  - [ ] 3.11 Add responsive mobile styles for touch devices
  - [ ] 3.12 Test theme across all page types and browsers
  - [ ] 3.13 Add prefers-reduced-motion support
  - [ ] 3.14 Import arcade-theme.css in main site CSS

- [ ] 4.0 Build Auto-Linking Glossary System
  - [ ] 4.1 Clone and import Kong API Glossary (Apache 2.0 license)
  - [ ] 4.2 Import Awesome Developer Dictionary (MIT license)
  - [ ] 4.3 Fetch Free Dictionary API tech terms
  - [ ] 4.4 Combine all sources into unified glossary.json (1000+ terms)
  - [ ] 4.5 Implement tech-glossary.js auto-linking script
  - [ ] 4.6 Add tooltip styling for term definitions
  - [ ] 4.7 Create progress tracking for viewed/learned terms
  - [ ] 4.8 Build interactive glossary page with search/filters
  - [ ] 4.9 Add achievement system for glossary exploration
  - [ ] 4.10 Test glossary performance with full dataset
  - [ ] 4.11 Test glossary on mobile devices

- [ ] 5.0 Optimize Beginner Experience
  - [ ] 5.1 Create beginner-friendly.js for skill level tracking
  - [ ] 5.2 Build skill-level selector interface (newbie/intermediate/advanced)
  - [ ] 5.3 Implement content adaptation based on selected skill level
  - [ ] 5.4 Add localStorage for progress tracking persistence
  - [ ] 5.5 Create visual progress bars and completion percentages
  - [ ] 5.6 Build achievement system with unlock notifications
  - [ ] 5.7 Design achievement badges (First Steps, Half Way Hero, AI Master)
  - [ ] 5.8 Write "5-minute setup" quick start guide in getting-started/
  - [ ] 5.9 Create "Never Coded Before?" beginner path documentation
  - [ ] 5.10 Design welcoming hero section for landing page
  - [ ] 5.11 Add "What can I build right now?" quick wins section
  - [ ] 5.12 Create onboarding modal for first-time visitors
  - [ ] 5.13 Add skill-based content filtering
  - [ ] 5.14 Test complete beginner flow (< 10 minutes to success)

- [ ] 6.0 Test and Launch
  - [ ] 6.1 Run full internal link validation with grep
  - [ ] 6.2 Test responsive design at 375px (mobile)
  - [ ] 6.3 Test responsive design at 768px (tablet)
  - [ ] 6.4 Test responsive design at 1024px+ (desktop)
  - [ ] 6.5 Run Lighthouse audit for performance score (target > 90)
  - [ ] 6.6 Run Lighthouse audit for accessibility score (target > 90)
  - [ ] 6.7 Run Lighthouse audit for SEO score (target > 90)
  - [ ] 6.8 Verify all Hugo aliases and redirects work
  - [ ] 6.9 Test glossary auto-linking on Chrome
  - [ ] 6.10 Test glossary auto-linking on Firefox
  - [ ] 6.11 Test glossary auto-linking on Safari
  - [ ] 6.12 Test glossary tooltips on mobile touch devices
  - [ ] 6.13 Verify achievement system saves to localStorage
  - [ ] 6.14 Test complete user journey from landing to first success
  - [ ] 6.15 Create git commit with all changes
  - [ ] 6.16 Push to master branch for Netlify auto-deploy
  - [ ] 6.17 Monitor Netlify build logs for errors
  - [ ] 6.18 Verify production site at startaitools.com