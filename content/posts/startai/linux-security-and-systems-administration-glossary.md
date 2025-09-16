+++
title = "Linux Security and Systems Administration Glossary"
date = "2025-01-13T12:00:00-06:00"
draft = false
author = "Jeremy Longshore"
tags = ["start ai tools"]
categories = ["AI"]
canonical_url = "https://startaitools.com/posts/linux-security-glossary/"
+++

<p><em>This glossary serves as a companion reference to our <a href="https://startaitools.com/posts/ssh-deb-grep-comprehensive-guide/">SSH, Debian, and grep comprehensive guide</a> and <a href="https://startaitools.com/posts/advanced-linux-security-ssh-debian-text-processing/">advanced Linux security guide</a>. Use it to quickly look up unfamiliar terms while learning.</em></p>
<h2 id="quick-navigation">
 Quick Navigation
 
 <a class="anchor" href="#quick-navigation">#</a>
</h2>
<ul>
<li><a href="#ssh--cryptography">SSH &amp; Cryptography</a></li>
<li><a href="#debian-package-management">Debian Package Management</a></li>
<li><a href="#text-processing--regular-expressions">Text Processing &amp; Regular Expressions</a></li>
<li><a href="#security-concepts">Security Concepts</a></li>
<li><a href="#network--system-administration">Network &amp; System Administration</a></li>
</ul>
<hr/>
<h2 id="ssh--cryptography">
 SSH &amp; Cryptography
 
 <a class="anchor" href="#ssh--cryptography">#</a>
</h2>
<h3 id="a-e">
 A-E
 
 <a class="anchor" href="#a-e">#</a>
</h3>
<p><strong>AES (Advanced Encryption Standard)</strong></p>
<ul>
<li>Symmetric encryption algorithm using 128, 192, or 256-bit keys</li>
<li>Hardware-accelerated on modern CPUs via AES-NI instructions</li>
<li>Example: <code>Ciphers aes256-gcm@openssh.com</code></li>
<li>See: <a href="https://startaitools.com/posts/advanced-linux-security-ssh-debian-text-processing/#performance-optimization-through-multiplexing-and-algorithm-selection">SSH cipher selection in our guide</a></li>
</ul>
<p><strong>Authentication Layer</strong></p>
