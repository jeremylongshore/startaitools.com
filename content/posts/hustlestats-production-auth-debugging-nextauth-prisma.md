+++
title = 'HustleStats Production Auth Meltdown: NextAuth, PrismaAdapter, and the Cascade That Blocked Every User'
slug = 'hustlestats-production-auth-debugging-nextauth-prisma'
date = 2025-10-21T10:00:00-05:00
draft = false
tags = ["debugging", "nextauth", "prisma", "production", "nextjs", "email", "authentication"]
categories = ["Technical Deep-Dive"]
description = "A customer was locked out of hustlestats.io. What looked like one auth bug turned into five cascading failures across NextAuth, Prisma, email encoding, and database migrations."
+++

## The Customer Was Blocked

A user tried to log into hustlestats.io and got a generic "Configuration" error. No stack trace. No useful message. Just a NextAuth error page with a single word.

This was a paying customer on a custom domain. The app had been working in development. It had been working on the default Vercel URL. But on the production custom domain, login was completely dead.

What followed was a 14-commit debugging marathon where every fix uncovered a new failure. The kind of session where you fix the auth, then registration breaks, then emails break, then the database schema is wrong, and you realize the entire deployment pipeline had been silently broken for days.

## Fix 1: NextAuth v5 Doesn't Trust Your Domain

The "Configuration" error is NextAuth's catch-all. It means something went wrong during the OAuth/credentials flow, and NextAuth chose not to tell you what.

After adding detailed logging to the auth callback, the actual error surfaced:

```
UntrustedHost: Host "hustlestats.io" is not trusted.
```

NextAuth v5 introduced a breaking change from v4: it no longer automatically trusts the host it's running on. If you're on a custom domain — not `*.vercel.app` — you need to explicitly opt in:

```typescript
// auth.ts
export const { handlers, signIn, signOut, auth } = NextAuth({
  trustHost: true,  // Required for custom domains in NextAuth v5
  providers: [
    CredentialsProvider({
      // ...
    }),
  ],
});
```

One line. That's the fix for the first bug. But `trustHost: true` is not documented prominently in the NextAuth v5 migration guide. It's buried in the API reference. If you're migrating from v4 and testing only on `localhost` or `*.vercel.app`, you'll never hit this — until production.

## Fix 2: PrismaAdapter Is Incompatible with CredentialsProvider

With `trustHost` fixed, login still failed. Different error this time — a database error from the Prisma adapter trying to create a session record.

Here's the thing about NextAuth adapters: they exist to persist sessions to a database. PrismaAdapter creates session rows, account rows, and verification token rows. This makes sense for OAuth providers where NextAuth manages the full session lifecycle.

But CredentialsProvider doesn't use sessions that way. Credentials auth is stateless — you validate the password, issue a JWT, and that's it. There's no session record to persist. PrismaAdapter tries to write one anyway and fails.

The fix was removing PrismaAdapter entirely:

```typescript
// BEFORE: PrismaAdapter fights CredentialsProvider
import { PrismaAdapter } from "@auth/prisma-adapter";

export const { handlers, signIn, signOut, auth } = NextAuth({
  adapter: PrismaAdapter(prisma),
  secret: process.env.NEXTAUTH_SECRET,
  providers: [CredentialsProvider({ /* ... */ })],
});

// AFTER: No adapter needed for credentials-only auth
export const { handlers, signIn, signOut, auth } = NextAuth({
  trustHost: true,
  session: { strategy: "jwt" },
  providers: [CredentialsProvider({ /* ... */ })],
});
```

I also removed the explicit `secret` config. NextAuth v5 reads `AUTH_SECRET` from the environment automatically — the old `NEXTAUTH_SECRET` pattern with explicit config is deprecated.

### Why Not the Obvious Approach?

You might think: "Just use OAuth instead of CredentialsProvider." Fair point. But HustleStats targets youth sports coaches — people who want a username and password, not a Google sign-in button. The product decision drives the auth architecture, not the other way around.

You might also think: "Use the database strategy with PrismaAdapter and skip JWTs." That works for OAuth flows. For credentials, NextAuth explicitly recommends JWT strategy. The adapter assumes it owns the user lifecycle. With credentials, *you* own the user lifecycle.

## Fix 3: The Email Encoding Disaster

Auth was working. Users could log in. Then a new user tried to register and got a 500 error.

The registration endpoint sends a welcome email via Resend. The email template was a standard HTML string with inline CSS. The error was a JSON parse failure deep in the Resend SDK.

Root cause: special characters in the HTML template were breaking JSON serialization. Apostrophes, copyright symbols, trademark symbols, and emoji characters — all valid HTML, all poison for template strings that get serialized to JSON.

```html
<!-- BEFORE: These characters break JSON encoding in Resend -->
<p>Here's your account</p>
<p>© 2025 HustleStats™</p>
<p>🎉 Welcome aboard!</p>

<!-- AFTER: HTML entities survive any encoding -->
<p>Here&#39;s your account</p>
<p>&#169; 2025 HustleStats&#8482;</p>
<p>&#127881; Welcome aboard!</p>
```

This took three separate commits to fully resolve. The first pass caught apostrophes. Then the copyright and trademark symbols failed in the next deploy. Then I found single quotes in CSS `font-family` declarations inside the email template — those broke the JSON encoding too:

```css
/* BEFORE: Single quotes in template literal → JSON encoding failure */
font-family: 'Helvetica Neue', Arial, sans-serif;

/* AFTER: Double quotes survive JSON serialization */
font-family: "Helvetica Neue", Arial, sans-serif;
```

Every character that isn't ASCII-safe in a JSON string context is a landmine when your email library serializes HTML templates as JSON payloads. Use HTML entities for everything non-alphanumeric. No exceptions.

## Fix 4: The Missing Database Column

Registration was working. Emails were sending. Then users couldn't see the analytics page — 404.

Two problems in one. First, the analytics page route simply didn't exist. That was a missing file, straightforward to add.

Second, the production database was missing the `birthday` column on the users table. The migration script used `CREATE TABLE IF NOT EXISTS` — which is idempotent for creating the table but does nothing if the table already exists with a different schema. The `birthday` column was added after the initial table creation, and the migration never ran `ALTER TABLE`.

The migration endpoint also failed with a PostgreSQL prepared statement error when I tried to send multiple SQL statements in a single query:

```sql
-- BEFORE: Multiple statements in one query → prepared statement error
CREATE TABLE IF NOT EXISTS users (...);
ALTER TABLE users ADD COLUMN IF NOT EXISTS birthday DATE;
CREATE TABLE IF NOT EXISTS analytics (...);

-- AFTER: Split into individual statements, executed sequentially
await sql`CREATE TABLE IF NOT EXISTS users (...)`;
await sql`ALTER TABLE users ADD COLUMN IF NOT EXISTS birthday DATE`;
await sql`CREATE TABLE IF NOT EXISTS analytics (...)`;
```

PostgreSQL's prepared statement protocol doesn't support multiple statements. Every migration tutorial shows multi-statement SQL files, but that's for `psql` — not for application-level query drivers that use the extended query protocol.

## Fix 5: Everything Else

With the critical path fixed, the remaining commits were cleanup:

- **Admin email verification endpoint** — early users had registered during the broken email period and never got verified. Built a manual verification endpoint to unblock them.
- **Sidebar contrast improvements** — customer feedback that the navigation was hard to read against the background.
- **Dependabot configuration** — first grouped all updates into a single weekly PR, then disabled it entirely. For a small team shipping fast, dependency update noise is worse than the risk it mitigates.
- **Vite security patch** — one moderate vulnerability that dependabot had flagged before I killed it.

## The Pattern: Cascading Production Failures

Here's what made this session brutal: each fix was invisible until the previous fix landed. You can't discover that email encoding is broken until auth works. You can't discover that the database schema is wrong until registration succeeds. You can't discover the analytics page is missing until users actually get past login.

This is the nature of production debugging on a system that was deployed but never used end-to-end on the production domain. Dev works. Staging works. The production custom domain has a completely different trust model, different environment variables, and a database that drifted from the migration scripts.

The total damage: 14 commits, 4,287 lines changed, and comprehensive debugging documentation so the next production fire has a playbook.

**Lesson: test your custom domain auth flow before you hand the URL to a customer.** Not on localhost. Not on `*.vercel.app`. On the actual domain with the actual database.

---

**Related Posts:**

- [Session Cookie Auth, Forgot-Password Timeouts, and Killing Flaky E2E Tests](/posts/session-cookies-forgot-password-flaky-e2e-tests/) — Another HustleStats auth debugging saga, this time with Firebase session cookies
- [The Silent Killer in Your Web App: How Bare catch {} Blocks Hide Failures](/posts/silent-killer-bare-catch-blocks-hide-failures/) — When error handling actively hides the bugs you need to find
- [Deploying Next.js 15 to Google Cloud Run: From Zero to HTTPS in 2 Hours](/posts/deploying-nextjs-15-google-cloud-run-custom-domain-ssl/) — The deployment side of the Next.js production story
