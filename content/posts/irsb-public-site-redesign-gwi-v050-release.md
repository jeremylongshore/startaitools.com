+++
title = 'IRSB Public Site Redesign and git-with-intent v0.5.0 Release'
slug = 'irsb-public-site-redesign-gwi-v050-release'
date = 2026-01-26T10:00:00-06:00
draft = false
tags = ["irsb", "git-with-intent", "ui-design", "release-engineering", "bounties", "jeremylongshore", "mobile-ux"]
categories = ["Development Journey"]
description = "IRSB dashboard becomes a gated landing page with dark zinc theme and mobile hamburger nav. git-with-intent v0.5.0 ships gwi gate with interactive approval and local diff ReviewerAgent. Bounties mobile UI and portfolio updates round out an 18-commit day."
+++

Eighteen commits across four repos. The IRSB dashboard turned into a proper landing page, git-with-intent shipped its most important command yet, and the bounties platform stopped being unusable on phones.

## IRSB: Dashboard to Landing Page

The old IRSB site was a dashboard. If you landed on it without context, you saw data grids and charts that meant nothing. The redesign flips the model: the public site is a landing page that explains what IRSB does, and the dashboard lives behind authentication.

### Dark Zinc Theme

The entire color system moved to zinc-based dark mode. Not trendy dark-for-dark's-sake — the protocol's target audience is operators running monitoring infrastructure who already live in dark terminals. Meeting them where they are.

The palette: zinc-950 backgrounds, zinc-100 text, emerald-500 accents for positive states, red-500 for alerts. Every component got updated. The contrast ratios all clear WCAG AA.

The landing page hero uses a gradient from zinc-950 to zinc-900 with a subtle grid pattern overlay. Below the fold: three feature cards (enforcement, evidence, monitoring) with emerald-500 icon accents, a protocol architecture diagram, and a "Request Access" CTA that feeds into the gated docs flow.

### Gated Documentation

Documentation used to be public. Now it's behind a Firebase Auth gate. The reasoning: IRSB documentation includes operational details about the enforcement layer and the evidence pipeline. Making that public before the protocol is audited creates unnecessary attack surface.

The gate is lightweight — sign in with GitHub, get a session cookie, access docs. No role hierarchy yet, just authenticated vs. not. The session expires after 7 days. On expiry, the user gets redirected to the landing page with a "Session expired" toast rather than a raw 401.

The gating also applies to the API reference docs. The public site shows endpoint names and descriptions, but request/response schemas are behind auth. This is intentional — enough information for an evaluator to understand the API surface, not enough for someone to build a client without engaging with the team.

### Mobile Hamburger Navigation

The desktop nav had six items. On mobile they stacked vertically and pushed the content below the fold. Standard hamburger pattern: collapsed by default, slide-in panel on tap, close on outside click or navigation.

The implementation uses CSS transforms rather than JavaScript show/hide. The menu is always in the DOM, just translated off-screen. This avoids the repaint cost of adding/removing elements and makes the animation smooth on older phones.

The close-on-outside-click handler uses a transparent overlay div rather than a document-level click listener. The overlay approach is simpler to reason about and doesn't interfere with other click handlers on the page.

## git-with-intent v0.5.0: The Gate Command

This is the release that makes git-with-intent useful for real workflows. `gwi gate` intercepts a commit and runs it through an approval flow before it lands.

### Interactive Approval

`gwi gate` presents the staged diff in a TUI with accept/reject/comment options per hunk. Accept all hunks and the commit proceeds. Reject any hunk and the commit aborts with the rejection reason logged.

The interaction model borrows from `git add -p` but adds persistence. Every approval decision gets recorded — which hunks were accepted, which were rejected, who approved, and when. This creates the audit trail that compliance teams actually want.

### Local Diff ReviewerAgent

The ReviewerAgent runs locally and provides a first-pass review before the human sees the diff. It checks for common issues: secrets in code, TODO comments in production paths, test files with no assertions, imports from deprecated packages.

The agent is configurable via `.gwi/reviewers.toml`. Teams can add custom checks (regex patterns, AST queries for supported languages, or shell commands that exit 0/1). The default configuration catches the obvious mistakes. The custom configuration catches the team-specific ones.

The agent runs in under 2 seconds for diffs under 500 lines. Above that it parallelizes by file. The performance constraint matters because gate is in the commit path — if it's slow, developers disable it.

## Bounties: Mobile UI and CI Fix

The bounties platform had a CSS grid that assumed desktop widths. Cards overflowed on anything under 768px. The fix swaps the grid for a single-column flex layout on mobile, with the card metadata collapsing into a horizontal pill bar instead of a sidebar.

The reward amount and deadline — the two pieces of information a bounty hunter cares about most — now sit at the top of the mobile card instead of in a sidebar that was getting clipped. The status badge moved from a colored border (invisible at small sizes) to an inline pill with text.

The CI fix was a flaky Playwright test that depended on animation timing. The card expand animation took 300ms, and the test asserted card content at 250ms. Bumped the wait to `waitForSelector` on the expanded content instead of a fixed timeout. This is the same class of bug that shows up in every E2E suite — never assert on timing, assert on DOM state.

## jeremylongshore.com Portfolio Updates

Updated the portfolio page with current project descriptions and screenshots. The IRSB section got the new landing page screenshot. The git-with-intent section added the gate command demo GIF. Minor copy updates across the other project cards.

The portfolio page also got a project count badge and a "last updated" timestamp in the header. Small things, but they signal that the portfolio is maintained rather than abandoned. A portfolio with a 2024 timestamp in 2026 looks like a ghost town regardless of what's on it.

---

Eighteen commits. IRSB has a public face. git-with-intent has its killer feature. The bounties platform works on phones. A productive Monday.

### Related Posts

- [IRSB Monorepo v1.0.0: Extracting Shared Packages and Unifying a Blockchain Platform](/posts/irsb-monorepo-v1-extracting-shared-packages/)
- [git-with-intent v0.9 to v0.10: Docker Upgrades, README Rewrites, and Strategic Research](/posts/git-with-intent-v090-v0100-docker-upgrades/)
- [GWI RBAC Governance and Hustle CI Stabilization](/posts/gwi-rbac-governance-hustle-ci-stabilization/)
