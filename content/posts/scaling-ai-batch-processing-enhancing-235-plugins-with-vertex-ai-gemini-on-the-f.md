+++
title = "Scaling AI Batch Processing: Enhancing 235 Plugins with Vertex AI Gemini on the Free Tier"
date = "2025-10-19T22:00:00-05:00"
draft = false
author = "Jeremy Longshore"
tags = ["start ai tools"]
categories = ["AI"]
canonical_url = "https://startaitools.com/posts/scaling-ai-batch-processing-enhancing-235-plugins-with-vertex-ai-gemini-on-the-free-tier/"
+++

<h2 id="the-problem-235-plugins-need-comprehensive-documentation">The Problem: 235 Plugins Need Comprehensive Documentation</h2>
<p>I maintain <a href="https://github.com/jeremylongshore/claude-code-plugins">claude-code-plugins</a>, a marketplace with 235 plugins for Claude Code. Each plugin needed enhanced SKILL.md files (8,000-14,000 bytes) following Anthropic’s Agent Skills standards. Doing this manually would take weeks.</p>
<p><strong>The goal:</strong> Process all 235 plugins overnight using Vertex AI Gemini 2.0 Flash - entirely on the free tier.</p>
<p><strong>The constraints:</strong></p>
<ul>
<li>Must stay within Vertex AI free tier limits</li>
<li>Need 100% success rate (no corrupted files)</li>
<li>Require full audit trail for compliance</li>
<li>Zero tolerance for API quota violations</li>
</ul>
<h2 id="the-journey-from-ultra-conservative-to-optimized">The Journey: From Ultra-Conservative to Optimized</h2>
<h3 id="phase-1-initial-system-design">Phase 1: Initial System Design</h3>
<p>I built <code>overnight-plugin-enhancer.py</code> with these core components:</p>
