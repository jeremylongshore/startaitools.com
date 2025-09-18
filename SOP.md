# Standard Operating Procedures (SOP)

Last Updated: September 15, 2025

## Daily Operations

### 1. Content Updates

#### Adding New Documentation
1. Create content file: `hugo new docs/section/page-name.md`
2. Add front matter with title, weight, and tags
3. Write content following documentation standards
4. Preview locally: `hugo server -D`
5. Commit and push to master for auto-deployment

#### Adding Blog Posts
1. Create post: `hugo new posts/post-title.md`
2. Set draft to false when ready to publish
3. Include date, tags, and author in front matter
4. Preview and test locally
5. Push to master to publish

### 2. Glossary Management

#### Adding Terms
1. Edit `/static/data/glossary.json`
2. Add new term with definition and category:
```json
{
  "term": "new-term",
  "definition": "Clear, concise explanation",
  "category": "AI/ML"
}
```
3. Terms auto-link across all content (no manual linking needed)
4. Test hover tooltips after deployment

#### Updating Definitions
1. Find term in glossary.json
2. Update definition text
3. Commit changes
4. Auto-links update site-wide automatically

### 3. Theme Customization

#### Changing Colors/Styles
1. Edit `/assets/_custom.scss`
2. Modify CSS variables or add new styles
3. Test locally with `hugo server`
4. Ensure both light and dark modes work
5. Commit changes when satisfied

Current theme settings:
- Link color: #3b82f6 (blue)
- Theme mode: Auto (light/dark)
- Base theme: Archie (minimalist)

### 4. Deployment Process

#### Production Deployment
1. All changes to master branch auto-deploy
2. Netlify builds with: `hugo --gc --minify --cleanDestinationDir`
3. Build typically completes in 1-2 minutes
4. Check live site at startaitools.com

#### Rollback Procedure
1. Revert commit in GitHub
2. Push to master
3. Netlify auto-rebuilds with previous version
4. Verify rollback at live site

### 5. Google Analytics

#### Setup Tracking
1. Get GA4 tracking ID from Google Analytics
2. Replace `G-XXXXXXXXXX` in `hugo.toml` line 8
3. Push changes to deploy
4. Verify in GA real-time dashboard

#### Privacy Compliance
- anonymizeIP: enabled
- respectDoNotTrack: enabled
- No cookies for users with DNT

### 6. Performance Monitoring

#### Build Metrics
- Target build time: < 3 seconds
- Current pages: 100+
- Content focus: Intent Solutions knowledge sharing (AI tools, guides, templates, research)
- Navigation: Zero broken links after reorganization
- Monitor for build warnings/errors

#### Site Performance
- Check Lighthouse scores monthly
- Target: 90+ for all categories
- Monitor page load times
- Review search functionality

### 7. Content Standards

#### Documentation Pages
- Use clear, concise language
- Include code examples
- Add "Next Steps" sections
- Use weighted ordering for navigation
- Tag appropriately for search

#### Blog Posts
- Professional tone
- Include date and author
- Tag for categorization
- Preview images when relevant
- Cross-link related content

### 8. Maintenance Tasks

#### Weekly
- Review and merge any PRs
- Check for broken links
- Update glossary with new terms
- Monitor site analytics

#### Monthly
- Update dependencies if needed
- Review and clean up drafts
- Check theme for updates
- Backup content (GitHub handles this)

#### Quarterly
- Comprehensive content review
- Update documentation templates
- Review site structure
- Plan new content sections

### 9. Troubleshooting

#### Common Issues

**Build Failures**
- Check Hugo version (needs 0.150.0)
- Verify front matter formatting
- Look for broken internal links
- Check theme submodule status

**Glossary Not Working**
- Verify glossary.json syntax
- Check tech-glossary-simple.js loaded
- Clear browser cache
- Test in incognito mode

**Styling Issues**
- Check _custom.scss syntax
- Verify CSS specificity
- Test in multiple browsers
- Check dark/light mode both work

**Deployment Issues**
- Check Netlify build logs
- Verify GitHub webhook active
- Ensure master branch protected
- Check build command correct

### 10. Emergency Procedures

#### Site Down
1. Check Netlify status page
2. Review recent deployments
3. Rollback if needed
4. Contact Netlify support if persists

#### Content Emergency
1. Remove problematic content immediately
2. Push hotfix to master
3. Verify deployment successful
4. Document incident for review

#### Security Issue
1. Take site offline if critical
2. Fix vulnerability
3. Deploy patch
4. Review and update security practices

## Contact Information

**Primary Contact**: Jeremy Longshore
**GitHub**: https://github.com/jeremylongshore/startaitools.com
**Domain**: startaitools.com
**Hosting**: Netlify

## Quick Reference

### Essential Commands
```bash
hugo server -D              # Local dev with drafts
hugo --gc --minify         # Production build
hugo new docs/page.md      # New documentation
git push origin master     # Deploy to production
```

### File Locations
- Content: `/content/docs/`
- Glossary: `/static/data/glossary.json`
- Styles: `/assets/_custom.scss`
- Config: `/hugo.toml`
- Analytics: `/hugo.toml` line 8

### Key Metrics
- Build time: ~2.5 seconds
- Pages: 100+
- Glossary terms: 1,855 with auto-linking
- Content: AI tools, guides, professional templates, research
- Navigation: Zero broken links, expand/collapse functionality
- UX: Copy code buttons, clean glossary link

---

End of SOP - Last Updated: September 15, 2025