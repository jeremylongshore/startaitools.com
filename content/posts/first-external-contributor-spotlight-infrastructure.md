+++
title = 'First External Contributor, Spotlight Infrastructure, and a 9,770-Line Delete'
slug = 'first-external-contributor-spotlight-infrastructure'
date = 2025-10-14T10:00:00-05:00
draft = false
tags = ["claude-code", "open-source", "community", "astro", "developer-experience"]
categories = ["Development Journey"]
description = "Merging the first external contributor into the Claude Code plugin marketplace, building spotlight and announcement infrastructure, and scorched-earth rewriting the landing site."
+++

A marketplace that only accepts your own code isn't a marketplace. It's a portfolio.

The Claude Code plugin hub launched on October 10th with 225+ plugins. All mine. The site was live, the CI pipeline was running, the validation framework was scoring badges. But there was an uncomfortable question hanging over it: would anyone else actually contribute?

Four days later, @cdnsteve submitted the Sugar plugin. First external contribution to the Claude Code plugin hub. The merge itself was straightforward. What wasn't obvious was how much infrastructure you need to make that moment visible to everyone who visits the site afterward.

## The Sugar Plugin Merge

Sugar came in as a pull request from Steve at cdnsteve. The merge PR landed cleanly. Created `sugar.json` (37 lines of plugin metadata), updated CHANGELOG with the new contributor entry, added Steve to CONTRIBUTORS, and reflected the addition in README. 137 insertions total across the spotlight commit. Standard open-source intake workflow.

The `sugar.json` followed the same metadata schema every plugin uses — name, description, commands, agents, version. No special treatment for external contributions. The validation pipeline doesn't care who wrote the code, just whether it meets the spec. That's the point. The contribution bar is the spec, not a relationship.

But merging it surfaced a gap. The site had no mechanism to make contributions visible. A new plugin entry would appear in the directory — alphabetically buried between hundreds of others. No announcement. No attribution. No signal that this marketplace accepts outside work.

If you want a second external contributor, the first one needs to be visible.

Open-source projects die quietly when contributions disappear into a commit log. The marketplace had a great plugin intake pipeline — metadata validation, badge scoring, CI checks. What it lacked was the social layer. That's a community problem, not a code problem.

## Spotlight Infrastructure

Three commits built the answer. Each one added a different layer of visibility, from homepage presence to site-wide announcements to a dedicated contributor page.

**Spotlight section on index.astro** — 55 lines added to the homepage. Featured contributors get a visible callout above the fold. Not a generic "contributors" list buried at the bottom of a README. A designed section with context about who built what and why it's worth trying.

The homepage already had a plugin directory and category navigation. The spotlight section sits between those — it's the first thing you see after the hero. The positioning is deliberate. Category browsing is how you find what you need. The spotlight is how you discover what you didn't know existed.

**Announcement bar and banner** — a reusable template for time-sensitive callouts. New releases, featured plugins, community milestones. The announcement bar sits at the top of every page with a dismissible UI. Created `announcement-template.md` for standardized formatting, `release-notes.md` for version announcements, and a spotlight SVG badge for visual differentiation. 77 insertions across the PR.

The template matters more than this specific announcement. Every future contributor spotlight, version release, or community milestone now has a consistent format and a visible placement. One-time infrastructure, repeated payoff.

**Dedicated Spotlight page** — `spotlight.astro` at 56 lines. A standalone page linked from the announcement bar where featured contributors get a full write-up. Not just a name and a link. Context about the plugin, the contributor, and why it matters to the ecosystem.

Version bumped to v1.0.38 with updated badges and plugin count across README and docs. Two commits handled the version housekeeping — one for the version number itself, one for the badge and count updates. Keeping those separate makes the changelog cleaner.

## Landing Site: Scorched Earth

Same day, different repo. While the marketplace was getting community infrastructure, the Intent Solutions landing page got a complete rewrite. Or more accurately, a complete deletion.

The numbers tell the story: 98 files changed, 141 insertions, 9,770 deletions. The entire React/Vite codebase — gone. Every component, every config file, every `node_modules` reference, every build artifact from the old stack. What remained was the Astro site that had been growing alongside it for weeks.

This wasn't a migration. It was acknowledging that the migration had already happened. The React/Vite code hadn't been touched in weeks. The Astro components were the actual production site. Deleting 9,770 lines of dead code just made the repo honest about what it was running.

The 141 lines of insertions were Astro component updates — refreshed hero copy, updated service descriptions, tightened the value proposition language. Standard landing page iteration. The meaningful work was the deletion. Every React component, every Vite config, every package-lock entry for a framework nobody was importing anymore. Gone in one commit.

No gradual deprecation. No compatibility shims. No feature flags pointing at the old code. Delete the old world, update the new one, push.

The kind of commit that's terrifying if you're not sure which codebase is production and trivial if you are. Astro was production. React/Vite was archaeology.

## Two Repos, One Theme

The thread connecting the marketplace work and the landing site rewrite is the same: stop carrying dead weight.

The marketplace was carrying the assumption that only the maintainer would contribute. No spotlight, no announcement system, no visible contributor attribution. The landing site was carrying 9,770 lines of a framework nobody was importing. Both problems had the same shape: the repo said one thing and reality said another.

Both got fixed on the same day by building what was actually needed and deleting what wasn't.

The plugin hub went from "project I built" to "project others contribute to" in a single merge. That transition requires more than accepting a PR. It requires visible infrastructure that tells the next potential contributor: your work will be seen here, not buried in a directory listing.

The spotlight page, announcement bar, and contributor section are that infrastructure. Seven commits across two repos. None of it is technically complex. All of it was missing four days ago.

The real test comes when contributor number two shows up. If the infrastructure works, they'll see Sugar featured on the homepage and know the process is real. They'll see the announcement bar, the spotlight page, the CONTRIBUTORS file. They'll know that contributing here isn't throwing code into a void.

That's the bet. Build the stage before you need the second act.

---

*Related posts:*
- [Claude Code Plugin Marketplace Launch](/posts/claude-code-plugin-marketplace-launch/) -- the initial marketplace build four days before this
- [Verified Plugins Program: Quality Signal for the Marketplace](/posts/verified-plugins-program-quality-signal-for-the-marketplace/) -- the badge scoring system contributors' plugins run through
- [Brand Consistency: CSS Variables and Sponsor Page Redesign](/posts/brand-consistency-css-variables-sponsor-page-redesign/) -- later design system work that built on these visual patterns
