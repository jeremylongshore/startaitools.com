+++
title = "Self-Hosting n8n on Contabo VPS: Enterprise Automation for $0/Month"
date = "2025-10-04T00:00:00+00:00"
draft = false
author = "Jeremy Longshore"
tags = ["start ai tools"]
categories = ["AI"]
canonical_url = "https://startaitools.com/posts/self-hosting-n8n-on-contabo-vps-enterprise-automation-for-0/month/"
+++

<p>We just deployed a production-ready n8n instance at <code>n8n.intentsolutions.io</code> with zero monthly software costs. Here’s the complete technical architecture and deployment process.</p>
<h2 id="the-business-case">The Business Case</h2>
<p><strong>Before:</strong> Paying $20+/month for n8n Cloud
<strong>After:</strong> $0/month on existing Contabo VPS
<strong>Setup Time:</strong> 2 hours
<strong>ROI:</strong> Infinite (one-time setup, zero recurring cost)</p>
<h2 id="architecture-overview">Architecture Overview</h2>
<pre tabindex="0"><code>┌─────────────────────────────────────┐
│ n8n.intentsolutions.io (DNS) │
│ ↓ │
│ 194.113.67.242:443 (HTTPS) │
│ ↓ │
│ Caddy Reverse Proxy │
│ - Auto SSL (Let's Encrypt) │
│ - Port 443 (HTTPS) │
│ ↓ │
│ Docker Container: n8n │
│ - Port 5678 (internal) │
│ - SQLite database │
│ - Persistent data: ./data │
│ - Backups: ./backups │
└─────────────────────────────────────┘
</code></pre><h2 id="technical-challenge-port-conflicts">Technical Challenge: Port Conflicts</h2>
<p>The server was already running:</p>
