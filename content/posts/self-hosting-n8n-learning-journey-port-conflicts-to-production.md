---
title: "From 'Why Won't This Work?' to Production Deploy: Self-Hosting n8n"
date: 2025-10-04
draft: false
tags: ["learning", "devops", "problem-solving", "n8n", "self-hosting"]
categories: ["Personal Growth", "Technical Journey"]
---

Today I learned that sometimes the hardest part of deployment isn't the technology - it's fighting your own assumptions about how things should work.

## The Goal (Seemed Simple)

Deploy n8n to `n8n.intentsolutions.io` with HTTPS. Should be straightforward, right?

**Spoiler:** It wasn't.

## The First Wall: "Why Netlify?"

I started by thinking I could use Netlify since my landing page was there. Made perfect sense to me - one domain, one platform, easy.

**Reality check:** Netlify only hosts static sites. n8n is a Node.js backend application.

**Lesson 1:** Know what your tools can actually do before building a plan around them.

## The Second Wall: Port Chaos

Okay, fine. Self-host on my Contabo VPS. Should be easy - just add Caddy for SSL and...

```
Error: failed to bind host port for 0.0.0.0:80
Error: address already in use
```

**My reaction:** "But I NEED port 80 for SSL!"

Turns out my server was already running:
- Apache2 on port 80
- Caddy on port 8080
- Various other services

I tried:
- ❌ Different ports (8888, 8080) - all taken
- ❌ Docker port mapping - conflicts everywhere
- ❌ Stopping Apache - but other stuff needs it

**Lesson 2:** Infrastructure debt is real. Every service you add fights for the same resources.

## The Breakthrough: Stop Fighting, Start Adapting

Instead of trying to force Caddy to work like I *thought* it should, I actually read how it works.

**Discovery:** Caddy doesn't NEED port 80 if you tell it not to try HTTP redirects.

```caddyfile
{
    auto_https disable_redirects  # <-- This changed everything
}

n8n.intentsolutions.io:443 {
    reverse_proxy localhost:5678
}
```

Suddenly, HTTPS worked. Let's Encrypt certificate auto-generated. No port 80 needed.

**Lesson 3:** Sometimes the solution is "stop insisting on the standard approach."

## The Import Nightmare

Got n8n running. Now to import my 15 workflows...

**API Attempt:**
```json
{"message":"request/body must NOT have additional properties"}
```

**Me:** "But this is n8n's own export format!"

Tried:
- ❌ Removing fields manually
- ❌ Different API endpoints
- ❌ Reformatting JSON structure

**Lesson 4:** When the API fails, check if there's a CLI.

```bash
docker exec -u node n8n n8n import:workflow --separate --input=/tmp/workflows/
```

**Output:** "Successfully imported 15 workflows."

**Me:** "WHY DIDN'T I JUST TRY THIS FIRST?!"

## The Stupid Mistakes

**Mistake 1:** Using `git mv` on untracked files
- Error: "fatal: not under version control"
- Fix: Check `git status` before assuming files are tracked

**Mistake 2:** Forgetting `active: false` field
- Error: "SQLITE_CONSTRAINT: NOT NULL constraint failed"
- Fix: Read the actual error message instead of guessing

**Mistake 3:** Trying to use `pass` without GPG configured
- Error: "gpg: decryption failed: No such file or directory"
- Fix: Just use a secure file with `chmod 600` instead

## What Actually Worked

1. **Stop assuming** - Read the actual docs
2. **Use existing infrastructure** - Don't deploy redundant services
3. **Try the CLI** - APIs aren't always the answer
4. **Host networking** - Simplified everything by avoiding port mapping

## The Numbers

- **Time spent fighting assumptions:** 1 hour
- **Time spent on actual solution:** 30 minutes
- **Workflows imported:** 15
- **Monthly cost savings:** $20-50 (n8n Cloud avoided)
- **New understanding gained:** Priceless

## What I'd Do Differently

If I could tell yesterday's me one thing:

> "Just use host networking mode and the n8n CLI. Trust me."

But then I wouldn't have learned about:
- Caddy's `auto_https disable_redirects` option
- n8n's CLI workflow management
- Docker host networking benefits
- How to work with existing server infrastructure

## The Real Win

Yes, I have a production n8n instance at `n8n.intentsolutions.io`. Yes, I saved $20-50/month.

But the real win? **I stopped fighting the problem and started listening to it.**

Every error message was trying to tell me something:
- "Port already in use" = You have infrastructure to work with
- "Additional properties" = Use a different tool
- "Not under version control" = Check your assumptions

## Related Posts

- [Building Scalable Content Systems: RSS Validation Architecture](/posts/building-scalable-content-systems-rss-validation-architecture/)
- [Enterprise Software Transformation: Waygate MCP Case Study](/posts/enterprise-software-transformation-waygate-mcp-case-study/)

## What's Next

Now that n8n is running, I can:
- Migrate workflows from old JSON exports
- Build new automation workflows
- Test webhook integrations
- Set up monitoring and alerts

But more importantly, I learned to **stop assuming I know the right way** and instead **ask "what is this system trying to tell me?"**

That's a lesson that applies way beyond deploying n8n.

---

*Sometimes the best technical solution is just letting go of your assumptions and listening to what the system is actually saying.*
