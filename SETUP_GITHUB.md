# GitHub Repository Setup Instructions

> **Obsolete.** This file describes a different, older repository (`My-Hugo-blog` / jeremylongshore.com) and its retired Netlify setup. startaitools.com deploys to the VPS via `.github/workflows/deploy.yml`; it needs no Netlify secrets. See CLAUDE.md.

Follow these steps to complete your GitHub repository configuration:

## 1. Repository Settings
Go to: https://github.com/jeremylongshore/My-Hugo-blog/settings

### General Settings
1. **Repository name:** Change from `My-Hugo-blog` to `jeremylongshore.com`
2. **Description:** Add:
   ```
   🌐 Personal blog and portfolio - AI engineering, software development, and startup insights
   ```
3. **Website:** Set to `https://jeremylongshore.com`
4. **Topics:** Click "Add topics" and add:
   - `hugo`
   - `personal-website`
   - `blog`
   - `portfolio`
   - `jamstack`
   - `static-site`
   - `ai-engineering`
   - `developer-blog`
   - `tech-blog`
   - `personal-blog`
   - `hugo-theme`
   - `hermit-v2`
   - `markdown`
   - `open-source`

### Features
Enable these checkboxes:
- ✅ Issues
- ✅ Projects
- ✅ Wiki (optional)
- ✅ Discussions (optional)

## 2. Create First Release
Go to: https://github.com/jeremylongshore/My-Hugo-blog/releases/new

1. **Tag version:** `v2.0.0`
2. **Release title:** `v2.0.0 - Professional Documentation & Start AI Tools Integration`
3. **Description:** Copy from RELEASES.md for v2.0.0
4. Click "Publish release"

## 3. Set Up Environments
Go to: Settings → Environments → New environment

### Production Environment:
- **Name:** `production`
- **Environment URL:** `https://jeremylongshore.com`
- **Deployment branch rules:** Only `main` branch
- **Required reviewers:** Optional (your username if you want reviews)

## 4. Secrets for GitHub Actions
No Netlify secrets. Deploy secrets (Tailscale OIDC, VPS deploy key) are documented in `.github/workflows/deploy.yml`.

## 5. Social Preview Image
Go to: Settings → General → Social preview

Upload an image (1280×640px) that represents your brand/blog.
You can create one at: https://www.canva.com/

Suggested design:
- Your name/logo
- "AI Engineer | Developer | Entrepreneur"
- Website URL
- Clean, professional design

## 6. GitHub Pages (Optional)
If you want a backup deployment:

Go to: Settings → Pages
- **Source:** Deploy from a branch
- **Branch:** `gh-pages` (create this branch first)
- **Folder:** `/` (root)

## 7. Branch Protection (Optional)
Go to: Settings → Branches → Add rule

For `main` branch:
- ✅ Require pull request reviews before merging
- ✅ Dismiss stale pull request approvals
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ Include administrators

## 8. Update Local Repository
After renaming on GitHub:

```bash
# Update your local remote URL
git remote set-url origin https://github.com/jeremylongshore/jeremylongshore.com.git

# Verify the change
git remote -v
```

## 9. Verify Everything Works
- [ ] Repository renamed successfully
- [ ] Website deploys to the VPS from a GitHub Release
- [ ] GitHub Actions run successfully
- [ ] Topics and description visible
- [ ] Release appears in releases tab
- [ ] Environments show in deployments

## Need Help?
- GitHub Docs: https://docs.github.com
- Hugo Docs: https://gohugo.io/documentation

---

Once complete, your repository will be fully professional and ready to showcase! 🎉