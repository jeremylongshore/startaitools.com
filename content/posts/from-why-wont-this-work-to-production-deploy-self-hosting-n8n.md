+++
title = "From 'Why Won't This Work?' to Production Deploy: Self-Hosting n8n"
date = "2025-10-04T00:00:00+00:00"
draft = false
author = "Jeremy Longshore"
tags = ["start ai tools"]
categories = ["AI"]
canonical_url = "https://startaitools.com/posts/from-why-wont-this-work-to-production-deploy-self-hosting-n8n/"
+++

<p>Today I learned that sometimes the hardest part of deployment isn’t the technology - it’s fighting your own assumptions about how things should work.</p>
<h2 id="the-goal-seemed-simple">The Goal (Seemed Simple)</h2>
<p>Deploy n8n to <code>n8n.intentsolutions.io</code> with HTTPS. Should be straightforward, right?</p>
<p><strong>Spoiler:</strong> It wasn’t.</p>
<h2 id="the-first-wall-why-netlify">The First Wall: “Why Netlify?”</h2>
<p>I started by thinking I could use Netlify since my landing page was there. Made perfect sense to me - one domain, one platform, easy.</p>
