+++
title = 'Infrastructure Maintenance: MCP Server Upgrade, npm Security Fixes, and a Portfolio Rebuild'
slug = 'infrastructure-maintenance-mcp-upgrade-portfolio-overhaul'
date = 2026-01-08T10:00:00-06:00
draft = false
tags = ["devops", "web-development", "firebase", "architecture"]
categories = ["Development Journey"]
description = "Fourteen commits across four repos. MCP server bumped to v2.8.0, npm audit vulnerabilities patched, Hustle TypeScript fixes, and jeremylongshore.com rebuilt as a Linktree-style hub with Firebase hosting."
+++

Maintenance days are the ones nobody plans and everybody needs. January 8th was fourteen commits across four repos, and not one of them added a new feature. Every commit either fixed something broken, upgraded something outdated, or replaced something that had outgrown its original design.

The temptation is always to skip maintenance and build the next thing. But deferred maintenance is invisible debt. The MCP server falling behind means you miss a race condition fix. The npm audit warnings piling up means you stop reading them. The personal site being stale means it's actively misrepresenting what you do.

## MCP Server v2.8.0 and npm Security Sweep

The MCP server powering ai-devops and intent-blueprint was pinned at v2.6.x. Two minor versions behind. The changelog between 2.6 and 2.8 included connection pooling improvements and a fix for a race condition in concurrent tool calls that we'd been working around with retry logic.

The upgrade itself was clean — bump the dependency, run the test suite, verify the tool registration handshake. The only hiccup was a minor breaking change in how v2.8.0 handles tool parameter validation. The new version rejects `undefined` values in tool input schemas where the old version silently coerced them to `null`. Two tool definitions needed explicit optional markers on parameters that had been implicitly optional before.

What wasn't clean was the npm audit output afterward. Both repos had accumulated moderate-severity vulnerabilities in transitive dependencies. The kind that `npm audit` flags and everyone ignores until they can't.

Fixed them. Most were one `npm audit fix` away. Two required manual resolution — a deprecated `glob` version nested three levels deep in a dev dependency, and a prototype pollution vector in a JSON schema validator. Neither was exploitable in our context, but clean audit output means you notice the next real vulnerability instead of ignoring it in a sea of known warnings.

The principle is simple: keep audit clean so the signal stays clean. A codebase with 47 known warnings is a codebase where warning 48 gets ignored. A codebase with zero warnings makes the first new vulnerability impossible to miss.

Both repos now have `npm audit` as a CI step. Not blocking — a moderate-severity vulnerability in a dev dependency shouldn't prevent a production deploy. But the audit runs, the output is visible in the PR checks, and it's much harder to ignore a new warning when the baseline is zero.

## Hustle: Stripe and Zod TypeScript Fixes

The Hustle codebase had TypeScript errors that CI was catching but not blocking. Strict mode wasn't enforced on the billing module, so Stripe webhook handlers were using `any` types freely. The Zod validation schemas for API request bodies had inference mismatches — the schemas were correct, but the TypeScript types derived from them didn't match the function signatures consuming them.

Five commits to fix it. Each one narrowing a type, adding a `z.infer<typeof schema>` annotation, or replacing an `any` with the actual Stripe event type. The typical fix looked like this:

```typescript
// Before: any
const event = req.body as any;

// After: typed
const event = req.body as Stripe.Event;
const invoice = event.data.object as Stripe.Invoice;
```

The Zod fixes were more subtle. A schema like `z.object({ amount: z.number() })` produces a type `{ amount: number }`, but the handler function was typed as `{ amount: number | undefined }` from an earlier iteration. The types compiled because TypeScript allows narrower assignment to wider types, but the runtime behavior was wrong — Zod would reject undefined at validation time while the function signature promised to handle it.

The billing module now compiles clean under `strict: true`. Not glamorous. But "the types are wrong" is how you get a production incident where a missing field silently passes validation and corrupts downstream data.

TypeScript strict mode is a one-way door. Once you turn it on, you can't turn it off without introducing regressions. The right time to enable it is when the module is small. The billing module has maybe 800 lines of actual logic. Fixing type errors in 800 lines is an afternoon. Fixing them in 8,000 lines is a sprint.

## jeremylongshore.com: Linktree-Style Rebuild

The personal site was a Hugo blog. It had been a Hugo blog for a year. But the actual use case had shifted — people landing on jeremylongshore.com weren't reading blog posts. They were looking for links. GitHub, LinkedIn, the portfolio, the blog at startaitools.com.

Tore out the blog layout and rebuilt it as a single-page link hub. One hero section with a photo and tagline, then a vertical stack of links. Firebase Hosting for deployment. Google Analytics wired up to track which links actually get clicked.

The Hugo blog content moved to startaitools.com (which is where the technical writing belongs anyway). The personal site became what visitors actually needed: a directory.

The design is intentionally minimal. No animations, no JavaScript frameworks, no build step. A single HTML file with inline CSS. When the entire site is one file, deployment is trivial, performance is instant, and there's nothing to break. The page loads, the links work, and there's nothing else to go wrong.

The Linktree comparison is apt but the implementation is different. Linktree is a hosted service that owns your URL and analytics. This is a static file on Firebase Hosting — I own the domain, I own the data, and the monthly cost is literally zero.

Firebase Hosting is overkill for a static page, but it's free-tier and it means the deploy pipeline is `firebase deploy --only hosting`. No build step, no CDN configuration, no certificate management. The page loads in under 200ms. Good enough.

Google Analytics is the one addition that wasn't strictly necessary but is worth having. The analytics answer a real question: what do people actually click when they land on the page? If 80% of visitors click the GitHub link and nobody clicks LinkedIn, that tells you something about the audience. Data-driven portfolio design instead of guessing.

The deployment was straightforward: `firebase init hosting`, point it at the directory with the single HTML file, `firebase deploy --only hosting`. Total time from init to live site: about twelve minutes. Most of that was writing the content, not configuring the infrastructure.

## The Maintenance Mindset

Fourteen commits in a day sounds productive. It is — but it's also a signal that maintenance had been deferred too long. If the MCP server had been upgraded when v2.7.0 dropped, the v2.8.0 upgrade would have been a one-commit bump. If the npm audits had been run monthly, there would have been two warnings instead of seven. Maintenance compounds in both directions — do it regularly and each session is quick. Defer it and the backlog grows superlinearly.

---

Fourteen commits. Zero new features. Everything that was broken is fixed, everything that was outdated is current, and the personal site finally matches how people actually use it.

### Related Posts

- [Waygate MCP v2.1.0: From Forensic Analysis to Production Enterprise Server](/posts/waygate-mcp-v2-1-0-forensic-analysis-to-production-enterprise-server/)
- [Building Idempotent Stripe Billing Enforcement in Firestore](/posts/building-idempotent-stripe-billing-enforcement-firestore/)
- [New Year's Eve: Go CLI Security Fix and Two Releases](/posts/new-years-eve-go-cli-security-fix-two-releases/)
