+++
title = "Applying Universal Directory Standards to a Prompt Engineering Repository"
date = "2025-10-08T23:30:00-06:00"
draft = false
author = "Jeremy Longshore"
tags = ["start ai tools"]
categories = ["AI"]
canonical_url = "https://startaitools.com/posts/applying-universal-directory-standards-to-a-prompt-engineering-repository/"
+++

<h2 id="the-problem-inconsistent-file-naming-across-master-systems">The Problem: Inconsistent File Naming Across Master Systems</h2>
<p>I had a prompt engineering repository with 150+ templates organized in a logical category structure, but the <code>000-master-systems/</code> directory had inconsistent file naming. Some files used <code>CATEGORY-###-description-MMDDYY.md</code>, others didn’t. I needed to apply universal directory standards without breaking the existing structure.</p>
<p>The repository: <a href="https://github.com/jeremylongshore/prompts-intent-solutions">prompts-intent-solutions</a></p>
<h2 id="the-challenge-two-different-naming-conventions">The Challenge: Two Different Naming Conventions</h2>
<p>Here’s where it got interesting. I initially thought the pattern was:</p>
<pre tabindex="0"><code>CATEGORY-###-description-MMDDYY.md
</code></pre><p>Looking at existing files in <code>000-master-systems/github/</code>:</p>
