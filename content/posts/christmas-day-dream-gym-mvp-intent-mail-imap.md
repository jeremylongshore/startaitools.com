+++
title = 'Christmas Day: Dream Gym MVP and Intent Mail IMAP Connector'
slug = 'christmas-day-dream-gym-mvp-intent-mail-imap'
date = 2025-12-25T10:00:00-06:00
draft = false
tags = ["web-development", "authentication", "imap", "gemini", "python", "hustle"]
categories = ["Development Journey"]
description = "Christmas Day commits: Dream Gym MVP with registration and auth, Gemini PR reviews, session cookie fixes — plus intent-mail gets an IMAP/SMTP connector for providers beyond Gmail and Outlook."
+++

Yes, I committed code on Christmas. Eight commits on hustle, one on intent-mail.

## Dream Gym MVP

The hustle repo got a new product: Dream Gym. A fitness tracking app aimed at the same youth sports market that HustleStats serves.

The MVP needed three things: user registration, authentication, and a landing page that explained what the product does.

### Registration and Session Cookies

Registration was straightforward Firebase Auth with email/password. The interesting part was the session cookie implementation.

Firebase Auth tokens are JWTs that expire after an hour. For a web app, re-authenticating every hour is a terrible UX. Session cookies extend the auth window — the server validates the Firebase token once, issues a session cookie with a configurable expiration (14 days default), and subsequent requests use the cookie instead of the Firebase token.

The implementation hit the same session cookie pitfall every Firebase Auth project hits: the `sameSite` attribute.

Session cookies with `sameSite=strict` don't survive redirects from external links. A user clicking a link from an email lands on the site, the cookie doesn't send because it's a cross-site navigation, and they see the login page despite being authenticated.

```python
response.set_cookie(
    key="session",
    value=session_cookie,
    max_age=14 * 24 * 60 * 60,
    httponly=True,
    secure=True,
    samesite="lax",  # Not "strict"
)
```

The fix is `sameSite=lax`. It preserves the security properties that actually matter (no CSRF on POST requests) while not breaking the most common user flow in any product that sends emails: click a link, arrive at the app, be logged in.

The rest of the auth setup was standard Firebase patterns: email verification flow, password reset with Firebase's built-in templates, and a middleware chain that checks the session cookie, verifies it with Firebase Admin SDK, and attaches the user context to the request.

### Landing Page

The landing page was deliberately minimal. Product name, one-sentence value prop, a screenshot mockup of the tracking dashboard, and a registration CTA.

No feature grids, no testimonials, no pricing table. For an MVP, the landing page has one job: convert a visitor to a registered user. Everything else is noise.

### Gemini PR Review Catches

Gemini PR reviews caught two issues in the registration flow.

First: the error message on duplicate email registration said "auth/email-already-exists" — a Firebase error code, not a user-facing message. The fix maps Firebase error codes to plain English.

Second: the registration endpoint didn't rate-limit, so an attacker could enumerate valid emails by watching which ones returned "already exists" vs. "created." The fix returns the same success message regardless and sends a verification email in both cases.

Both valid catches. The email enumeration fix is cheap to implement now and expensive to explain in a security audit later.

## Intent Mail: IMAP/SMTP Connector

One commit on intent-mail added the third provider connector: IMAP/SMTP.

Gmail and Outlook have dedicated APIs with delta sync. Everything else — corporate Exchange servers, Fastmail, ProtonMail Bridge, self-hosted Dovecot — speaks IMAP for reading and SMTP for sending.

### IMAP Sync

The IMAP connector follows the same interface as Gmail and Outlook: sync messages to local SQLite, support search via FTS5, send via the provider.

The delta sync equivalent for IMAP is `UIDVALIDITY` and `UIDNEXT` — tracking the highest UID seen and only fetching messages with higher UIDs on subsequent syncs.

IMAP is more finicky than REST APIs. Connection timeouts need aggressive handling because IMAP servers drop idle connections silently. IDLE support varies by server. Folder hierarchies use different delimiters (slash, dot, or pipe depending on the server). Non-ASCII headers still cause encoding issues with older servers.

The connector normalizes all of these: folder delimiters get translated to forward slashes internally, headers get decoded with a fallback chain, and connection drops trigger automatic reconnect.

### Connection Pool and SMTP

The connector wraps Python's `imaplib` with retry logic and a connection pool. The pool keeps 3 connections warm by default, with health checks via NOOP every 5 minutes to prevent server-side timeout.

SMTP sending is simpler — connect, authenticate, send, disconnect. The connector supports both STARTTLS (port 587) and implicit TLS (port 465), with automatic detection based on port number.

Three connectors. Gmail, Outlook, and everything else. Intent-mail can now manage email from any provider that speaks IMAP.

---

Nine commits on Christmas Day. Dream Gym has auth. Intent-mail has universal provider support.

### Related Posts

- [Session Cookies, Forgot Password, and Flaky E2E Tests](/posts/session-cookies-forgot-password-flaky-e2e-tests/)
- [Intent Mail: Full Email Platform in a Day — Gmail, Outlook, and a Rules Engine](/posts/intent-mail-full-platform-gmail-outlook-rules-engine/)
- [HustleStats: Production Auth Debugging with NextAuth and Prisma](/posts/hustlestats-production-auth-debugging-nextauth-prisma/)
