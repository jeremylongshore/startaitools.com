+++
title = "Debugging a Critical Marketplace Schema Validation Failure: How One Invalid Field Blocked All Installations"
date = "2025-10-16T22:30:00-06:00"
draft = false
author = "Jeremy Longshore"
tags = ["start ai tools"]
categories = ["AI"]
canonical_url = "https://startaitools.com/posts/debugging-a-critical-marketplace-schema-validation-failure-how-one-invalid-field-blocked-all-installations/"
+++

<p>At 10:16 PM ET on October 16th, 2025, a user reported they couldn’t install the Claude Code Plugins marketplace. The error message was clear but devastating:</p>
<pre tabindex="0"><code>✘ Failed to add marketplace: Invalid schema: plugins.1: Unrecognized key(s) in object: 'enhances'
</code></pre><p><strong>Impact:</strong> ZERO users could install the marketplace. Complete installation failure.</p>
<p>This is the story of how we debugged it, fixed it, added legal compliance, resolved CI/CD issues, and deployed security improvements - all in under 3 hours.</p>
