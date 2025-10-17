+++
title = "Add AI to Your Website"
date = "2001-01-01T00:00:00+00:00"
draft = false
author = "Jeremy Longshore"
tags = ["start ai tools"]
categories = ["AI"]
canonical_url = "https://startaitools.com/posts/add-ai-to-your-website/"
+++

<h1 id="add-ai-to-your-website">
 Add AI to Your Website
<p><a class="anchor" href="#add-ai-to-your-website">#</a></p>
</h1>
<p>Quick integration guide for adding AI to your existing site.</p>
<h2 id="frontend-integration">
 Frontend Integration
<p><a class="anchor" href="#frontend-integration">#</a></p>
</h2>
<div class="highlight"><pre class="chroma" tabindex="0"><code class="language-html" data-lang="html"><span class="line"><span class="cl"><span class="c">&lt;!-- Add to your HTML --&gt;</span>
</span></span><span class="line"><span class="cl"><span class="p">&lt;</span><span class="nt">div</span> <span class="na">id</span><span class="o">=</span><span class="s">"ai-chat"</span><span class="p">&gt;&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="p">&lt;</span><span class="nt">script</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl"><span class="kr">async</span> <span class="kd">function</span> <span class="nx">askAI</span><span class="p">(</span><span class="nx">question</span><span class="p">)</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl"> <span class="kr">const</span> <span class="nx">response</span> <span class="o">=</span> <span class="kr">await</span> <span class="nx">fetch</span><span class="p">(</span><span class="s1">'/api/chat'</span><span class="p">,</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl"> <span class="nx">method</span><span class="o">:</span> <span class="s1">'POST'</span><span class="p">,</span>
</span></span><span class="line"><span class="cl"> <span class="nx">headers</span><span class="o">:</span> <span class="p">{</span> <span class="s1">'Content-Type'</span><span class="o">:</span> <span class="s1">'application/json'</span> <span class="p">},</span>
</span></span><span class="line"><span class="cl"> <span class="nx">body</span><span class="o">:</span> <span class="nx">JSON</span><span class="p">.</span><span class="nx">stringify</span><span class="p">({</span> <span class="nx">message</span><span class="o">:</span> <span class="nx">question</span> <span class="p">})</span>
</span></span><span class="line"><span class="cl"> <span class="p">});</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"> <span class="kr">const</span> <span class="nx">data</span> <span class="o">=</span> <span class="kr">await</span> <span class="nx">response</span><span class="p">.</span><span class="nx">json</span><span class="p">();</span>
</span></span><span class="line"><span class="cl"> <span class="k">return</span> <span class="nx">data</span><span class="p">.</span><span class="nx">reply</span><span class="p">;</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span>
</span></span><span class="line"><span class="cl"><span class="p">&lt;/</span><span class="nt">script</span><span class="p">&gt;</span>
</span></span></code></pre></div><h2 id="backend-api">
 Backend API
<p><a class="anchor" href="#backend-api">#</a></p>
</h2>
<div class="highlight"><pre class="chroma" tabindex="0"><code class="language-javascript" data-lang="javascript"><span class="line"><span class="cl"><span class="c1">// Express.js example
</span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="nx">app</span><span class="p">.</span><span class="nx">post</span><span class="p">(</span><span class="s1">'/api/chat'</span><span class="p">,</span> <span class="kr">async</span> <span class="p">(</span><span class="nx">req</span><span class="p">,</span> <span class="nx">res</span><span class="p">)</span> <span class="p">=&gt;</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl"> <span class="kr">const</span> <span class="p">{</span> <span class="nx">message</span> <span class="p">}</span> <span class="o">=</span> <span class="nx">req</span><span class="p">.</span><span class="nx">body</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"> <span class="kr">const</span> <span class="nx">reply</span> <span class="o">=</span> <span class="kr">await</span> <span class="nx">openai</span><span class="p">.</span><span class="nx">chat</span><span class="p">.</span><span class="nx">completions</span><span class="p">.</span><span class="nx">create</span><span class="p">({</span>
</span></span><span class="line"><span class="cl"> <span class="nx">model</span><span class="o">:</span> <span class="s2">"gpt-3.5-turbo"</span><span class="p">,</span>
</span></span><span class="line"><span class="cl"> <span class="nx">messages</span><span class="o">:</span> <span class="p">[{</span> <span class="nx">role</span><span class="o">:</span> <span class="s2">"user"</span><span class="p">,</span> <span class="nx">content</span><span class="o">:</span> <span class="nx">message</span> <span class="p">}]</span>
</span></span><span class="line"><span class="cl"> <span class="p">});</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"> <span class="nx">res</span><span class="p">.</span><span class="nx">json</span><span class="p">({</span> <span class="nx">reply</span><span class="o">:</span> <span class="nx">reply</span><span class="p">.</span><span class="nx">choices</span><span class="p">[</span><span class="mi">0</span><span class="p">].</span><span class="nx">message</span><span class="p">.</span><span class="nx">content</span> <span class="p">});</span>
</span></span><span class="line"><span class="cl"><span class="p">});</span>
</span></span></code></pre></div><h2 id="next-steps">
 Next Steps
<p><a class="anchor" href="#next-steps">#</a></p>
</h2>
<ul>
<li>Add authentication</li>
<li>Implement rate limiting</li>
<li>Create custom UI components</li>
</ul>
