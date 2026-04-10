+++
title = 'Intent Blueprint Docs Phases 2-5, Hustle E2E, and the Turbopack Body Bug'
slug = 'intent-blueprint-docs-phases-two-five-hustle-e2e-turbopack'
date = 2026-01-05T10:00:00-06:00
draft = false
tags = ["documentation", "next-js", "e2e-testing", "turbopack", "ci-cd", "integrations"]
categories = ["Development Journey"]
description = "Intent Blueprint Docs rapid-builds four phases in a day — interview engine, platform integrations, marketplace, enterprise. Hustle E2E hits a Turbopack body consumption bug."
+++

Thirty-six commits across six repos. The day split cleanly: documentation infrastructure in the morning, E2E debugging in the afternoon.

## Intent Blueprint Docs: Four Phases, One Day

Intent Blueprint Docs went from Phase 1 scaffolding (laid down on the 4th) to Phase 5 enterprise features by end of day. That's four phases of a documentation generation platform in a single session.

**Phase 2: Interview Engine** — The system now asks questions. Instead of generating docs from static templates, Phase 2 introduced a conversational interview flow. The engine asks about your architecture, your deployment model, your team structure, and generates documentation tailored to the answers. Think of it as a documentation wizard, except the wizard actually understands software systems.

**Phase 3: Platform Integrations** — GitHub, Linear, Jira, and Notion. The interview engine can now pull context directly from your existing tools. Connect your GitHub repo and it reads your directory structure, CI config, and README. Connect Linear and it pulls your project taxonomy. The generated docs reflect what actually exists, not what someone remembers to type into a form.

Four integrations in one phase sounds aggressive. It works because each integration follows the same pattern: OAuth flow, data fetch, schema normalization. The integration interface is generic. Each platform adapter implements three methods: authenticate, fetch, normalize. The platform-specific logic stays in the adapter. The doc generation engine never knows which platform it's talking to.

**Phase 4: Marketplace** — A directory where teams can share doc templates. If your team builds a great onboarding doc template, publish it. Other teams can fork it, customize it, and contribute improvements back. Standard marketplace dynamics — the platform gets more valuable as more people contribute.

**Phase 5: Enterprise** — Role-based access, audit trails, compliance templates. The features that enterprise buyers require before signing a contract. SOC 2 documentation templates, GDPR data flow diagrams, incident response runbook scaffolding. Not exciting to build. Critical to sell.

Four phases in one day is only possible because the architecture was designed for it. Each phase extends the system without rewriting the previous one. The interview engine (Phase 2) feeds the integrations (Phase 3) which populate the marketplace (Phase 4) which enterprise features gate (Phase 5). Linear dependency chain, each layer building on the last.

## Hustle E2E: The Turbopack Body Consumption Bug

The afternoon belonged to Hustle's E2E test suite, which was failing in CI but passing locally. The classic "works on my machine" situation, except this time the machine difference was Turbopack.

Hustle runs on Next.js 15 with Turbopack as the dev server bundler. Turbopack is faster than Webpack for development builds. It's also newer, which means edge cases.

The bug: POST requests with JSON bodies were silently failing in the E2E tests when running under Turbopack in CI. The request would arrive at the API route, but `request.json()` would return an empty object. The body was consumed somewhere in the middleware chain before the route handler could read it.

This is a known Turbopack behavior (not quite a bug, more of a gap). In Webpack mode, the request body stream can be read multiple times because Webpack's dev server buffers it. Turbopack's dev server doesn't buffer — it passes the raw stream, and once middleware reads it, it's gone.

The workaround: clone the request before middleware processing. The middleware gets a clone, the route handler gets the original. Both can read the body independently.

```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  // Clone before reading - Turbopack doesn't buffer
  const cloned = request.clone();
  // ... middleware logic using cloned request
  return NextResponse.next();
}
```

The standalone build issue was related but different. CI was building in standalone mode for Docker deployment, and the standalone output was missing some API routes. The fix was explicit in the `next.config.js` output file tracing — telling Next.js exactly which files the standalone build needs to include.

Between the body consumption workaround and the standalone tracing fix, Hustle's E2E suite went from 60% pass rate in CI to 100%.

## The Split

Morning: build infrastructure that generates documentation from interviews and platform data. Afternoon: debug a request body stream that vanishes in a specific bundler mode under a specific build configuration.

That's software development. The morning felt productive. The afternoon felt like archaeology. Both were necessary.

The Blueprint Docs platform now has a real feature set. Hustle now has reliable CI. Neither would've happened if I'd spent the whole day on just one.

---

## Related Posts

- [Session Cookies, Forgot Password, Flaky E2E Tests](/posts/session-cookies-forgot-password-flaky-e2e-tests/) — More E2E debugging in the same stack
- [HustleStats: Production Auth Debugging with NextAuth + Prisma](/posts/hustlestats-production-auth-debugging-nextauth-prisma/) — Earlier Hustle infrastructure and auth work
- [Building Production CI/CD: Documentation to Deployment](/posts/building-production-ci-cd-documentation-to-deployment/) — CI/CD pipeline patterns used across these projects
