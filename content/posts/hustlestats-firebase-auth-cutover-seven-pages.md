+++
title = 'HustleStats Firebase Auth Cutover: 7 Dashboard Pages, 3-Layer Defense, Zero Prisma'
slug = 'hustlestats-firebase-auth-cutover-seven-pages'
date = 2025-11-15T10:00:00-06:00
draft = false
tags = ["firebase", "authentication", "nextjs", "middleware", "hustlestats", "migration"]
categories = ["Development Journey"]
description = "Cutting over 7 dashboard pages from NextAuth/Prisma to Firebase Auth with a 3-layer defense: edge middleware, layout verification, and page-level guards. 17 commits, 1,402 files touched, zero NextAuth deps remaining."
+++

The Firebase migration (Days 2-7) gave HustleStats a new auth system and data layer. Today was the cutover — making every dashboard page actually use it.

## Phase 1: Planning and Staging

Before touching code, I mapped every page that imported NextAuth or Prisma:

- Dashboard home
- Player list + detail
- Game entry + detail
- Stats overview
- Settings/profile

Seven pages total. Each one imported `getServerSession` from NextAuth and made Prisma queries for data. Every page needed both the auth and data layer swapped.

The staging analysis uncovered an env var blocker. The Firebase Admin SDK needs `FIREBASE_SERVICE_ACCOUNT_KEY` as a JSON string in the environment. Vercel's environment variable UI silently truncates JSON values longer than 4KB. The service account key is ~2.3KB, so it fit — but only after removing all whitespace from the JSON. Formatted JSON with indentation pushed it over the limit.

## Phase 2: Repo Consolidation

Before the cutover, the codebase had accumulated dead code from the migration. Old NextAuth config files, Prisma client wrappers, unused API routes for the PostgreSQL-backed endpoints, test fixtures referencing the old schema.

The consolidation commit: 1,402 files changed, +99,762 lines. That line count is misleading — most of it was `package-lock.json` regeneration after removing Prisma dependencies. The actual code changes were ~200 lines of deletions.

Removed:
- `prisma/` directory (schema, migrations, seed files)
- `@prisma/client`, `prisma`, `@auth/prisma-adapter` packages
- NextAuth route handlers (`/api/auth/[...nextauth]`)
- Old session utility functions
- PostgreSQL connection module

The goal was a clean baseline. No dead imports. No unused packages. No confusion about which auth system was active.

## Phase 3: Dashboard Cutover

Each of the 7 pages got the same treatment:

1. Replace `getServerSession()` with Firebase Admin `verifyIdToken()`
2. Replace Prisma queries with Firestore reads from the new subcollection hierarchy
3. Replace NextAuth session types with Firebase `DecodedIdToken`

The auth defense has three layers:

**Layer 1 — Edge Middleware.** Next.js middleware runs at the CDN edge before the page even loads. It checks for a `session` cookie containing a Firebase ID token. No cookie? Redirect to `/login`. This is the cheapest check — it happens at the edge with zero server compute.

```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  const session = request.cookies.get('session');
  if (!session && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  return NextResponse.next();
}
```

**Layer 2 — Layout Token Verification.** The dashboard layout component (shared by all 7 pages) calls Firebase Admin's `verifyIdToken()` server-side. This validates the token's signature, expiration, and issuer. A valid cookie with an expired or revoked token gets caught here.

```typescript
// app/dashboard/layout.tsx
export default async function DashboardLayout({ children }) {
  const cookieStore = cookies();
  const session = cookieStore.get('session')?.value;

  if (!session) redirect('/login');

  try {
    const decoded = await adminAuth.verifyIdToken(session);
    // Token valid — render dashboard
  } catch {
    redirect('/login');
  }

  return <div className="dashboard-layout">{children}</div>;
}
```

**Layer 3 — Page-Level Defense.** Each individual page verifies the user ID from the token matches the Firestore path it's querying. A valid token for user A cannot read user B's data, even if the middleware and layout checks pass.

Three admin services handle the Firestore operations: `AdminUserService`, `AdminPlayerService`, `AdminGameService`. Each service accepts a `uid` parameter and scopes all queries to that user's subcollections. No service method can operate on data outside the authenticated user's tree.

## The Result

After all 7 pages were migrated:

- Zero imports from `next-auth` anywhere in the codebase
- Zero imports from `@prisma/client`
- Zero references to `getServerSession`
- `package.json` lost 3 dependencies
- Auth flow: cookie → edge check → token verify → scoped query

The E2E flow confirmed: sign up → receive welcome email → log in → see dashboard → navigate all 7 pages → sign out → redirected to login. Every page loads. Every data query returns results from Firestore.

17 commits for the day. The codebase went from "Firebase Auth is available" to "Firebase Auth is the only auth system."

---

**Related Posts:**

- [HustleStats Firebase Migration Days 2-7: Schema, Auth Swap, Data Port, and the Cost Cliff](/posts/hustlestats-firebase-migration-days-two-through-seven/) — The migration that preceded this cutover
- [HustleStats Production Auth Debugging: NextAuth, PrismaAdapter, and the Cascade](/posts/hustlestats-production-auth-debugging-nextauth-prisma/) — The NextAuth problems that motivated leaving it behind
