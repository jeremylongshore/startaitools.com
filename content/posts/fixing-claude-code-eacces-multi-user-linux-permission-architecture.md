+++
title = "Fixing Claude Code EACCES: Multi-User Linux Permission Architecture"
date = "2025-10-23T14:45:00-06:00"
draft = false
author = "Jeremy Longshore"
tags = ["start ai tools"]
categories = ["AI"]
canonical_url = "https://startaitools.com/posts/fixing-claude-code-eacces-multi-user-linux-permission-architecture/"
+++

<p>When you’re running Claude Code across multiple Linux user accounts and hit <code>EACCES: permission denied</code>, the solution isn’t just <code>chmod 777</code>. This is the complete troubleshooting journey from error to production-ready multi-user architecture.</p>
<h2 id="the-problem-two-users-one-claude-code-instance">The Problem: Two Users, One Claude Code Instance</h2>
<p><strong>Initial symptom:</strong> User <code>jeremy</code> couldn’t start Claude Code:</p>
<pre tabindex="0"><code>EACCES: permission denied, open
syscall: "open",
 errno: -13,
 code: "EACCES"
</code></pre><p><strong>Context:</strong></p>
<ul>
<li>Two user accounts: <code>jeremy</code> (master) and <code>admincostplus</code> (admin)</li>
<li>Both need to run Claude Code independently</li>
<li>Shared configuration desired (plugins, MCP servers, slash commands)</li>
<li>No permission conflicts or ownership battles</li>
</ul>
<p>The naive approach? “Just give both users access.” The correct approach? Architect a system that scales.</p>
