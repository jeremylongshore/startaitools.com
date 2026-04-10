+++
title = 'Landing Page Conversion Optimization and Legal Pages'
slug = 'landing-page-conversion-optimization-legal-pages'
date = 2026-01-20T10:00:00-06:00
draft = false
tags = ["intent-solutions-landing", "jeremylongshore", "conversion-optimization", "legal", "portfolio", "terms-of-service", "privacy-policy"]
categories = ["Development Journey"]
description = "Building a 17-project showcase for the landing page, rewriting Learn/Colab for conversion, and adding CTA buttons, Terms of Service, and Privacy Policy to the personal site."
+++

Four commits across two repos. The work split between making the Intent Solutions landing page actually convert visitors and adding the legal foundation that a professional services company needs.

## intent-solutions-landing: Projects Showcase

The landing page listed services but didn't show work. The new projects showcase surfaces 17 active projects with consistent metadata:

- Project name and one-line description
- Tech stack badges (React, Firebase, Vertex AI, etc.)
- Status indicator (active/maintained/archived)
- Link to live demo or documentation

The showcase renders as a responsive grid -- three columns on desktop, two on tablet, single column on mobile. Each card is intentionally minimal: name, description, stack, status. No screenshots, no long descriptions. The goal is density -- a visitor should scan all 17 projects in under 30 seconds and find the ones relevant to their needs.

The project data lives in a JSON file (`data/projects.json`) rather than hardcoded in the template. Adding a new project means adding a JSON object, not editing HTML.

### Learn and Colab Rewrite

The Learn and Colab pages from yesterday's work were informational but not conversion-oriented. The rewrite adds:

**Learn page** -- restructured around the visitor's problem, not Intent Solutions' content library. Instead of "here are our blog posts," the page now opens with "what are you trying to build?" and routes visitors to relevant content based on their use case. Three paths: "I need an AI agent," "I need to integrate AI into existing systems," "I need to understand what's possible."

**Colab page** -- the engagement model page gained a clear call-to-action flow. The previous version described the process but didn't ask for anything. The rewrite adds a "Start a Conversation" button at the bottom of each section, not just at the end of the page. Each button deep-links to the contact form with the relevant project type pre-selected.

## jeremylongshore.com: CTA Buttons and Legal Pages

### CTA Buttons

The personal site added call-to-action buttons linking to Intent Solutions. The buttons appear at the bottom of portfolio-related posts and on the About page. The design matches the charcoal slate theme -- muted blue button with white text, subtle hover animation.

### Terms of Service

A standard Terms of Service page covering:

- Service description (consulting, development, training)
- Intellectual property (client owns deliverables, Intent Solutions retains reusable frameworks)
- Payment terms (Net 30, milestone-based for projects over $10K)
- Limitation of liability (standard cap at contract value)
- Termination (either party with 30 days notice, immediate for material breach)
- Governing law (State of Georgia)

The ToS is written in plain English, not legalese. Each section is a paragraph, not a wall of subsections. A lawyer reviewed the final version, but the draft was written to be readable by the people who'd actually agree to it.

### Privacy Policy

The Privacy Policy covers:

- Data collected (name, email, company from contact forms)
- Data not collected (no tracking cookies, no analytics beyond server logs)
- Data retention (contact form submissions retained for 24 months)
- Third-party services (Firebase, SendGrid -- both with their own privacy policies linked)
- GDPR compliance (deletion requests honored within 30 days)
- Contact information for privacy questions

The policy is deliberately minimal because the data collection is minimal. No cookies, no analytics scripts, no user accounts. The contact form is the only data collection point.

## What Changed

| Repo | Change | Purpose |
|------|--------|---------|
| intent-solutions-landing | 17-project showcase | Show, don't tell |
| intent-solutions-landing | Learn/Colab rewrite | Convert visitors, not just inform them |
| jeremylongshore.com | CTA buttons | Bridge personal site to business |
| jeremylongshore.com | Terms of Service | Legal foundation |
| jeremylongshore.com | Privacy Policy | GDPR/privacy compliance |

## Related Posts

- [Post-Merge Cleanup, Landing Redesign, and Portfolio Theme Overhaul](/posts/post-merge-cleanup-landing-redesign-portfolio-theme/) -- the previous day's landing page and theme work
- [Model-Agnostic Positioning and the IAE Branding Back-and-Forth](/posts/intent-solutions-landing-model-agnostic-positioning/) -- earlier positioning struggles on the same site
- [COPPA Compliance: Youth Sports App Real Implementation](/posts/coppa-compliance-youth-sports-app-real-implementation-process/) -- another legal compliance implementation
