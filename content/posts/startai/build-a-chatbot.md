+++
title = "Build a Chatbot"
date = "2001-01-01T00:00:00+00:00"
draft = false
author = "Jeremy Longshore"
tags = ["start ai tools"]
categories = ["AI"]
canonical_url = "https://startaitools.com/docs/templates/chatbot/"
+++

<h1 id="build-a-chatbot">
 Build a Chatbot
 
 <a class="anchor" href="#build-a-chatbot">#</a>
</h1>
<p>Create your own AI chatbot with this simple template.</p>
<h2 id="quick-start">
 Quick Start
 
 <a class="anchor" href="#quick-start">#</a>
</h2>
<div class="highlight"><pre class="chroma" tabindex="0"><code class="language-javascript" data-lang="javascript"><span class="line"><span class="cl"><span class="kr">const</span> <span class="nx">OpenAI</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="s1">'openai'</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kr">const</span> <span class="nx">openai</span> <span class="o">=</span> <span class="k">new</span> <span class="nx">OpenAI</span><span class="p">({</span>
</span></span><span class="line"><span class="cl"> <span class="nx">apiKey</span><span class="o">:</span> <span class="nx">process</span><span class="p">.</span><span class="nx">env</span><span class="p">.</span><span class="nx">OPENAI_API_KEY</span>
</span></span><span class="line"><span class="cl"><span class="p">});</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kr">async</span> <span class="kd">function</span> <span class="nx">chatbot</span><span class="p">(</span><span class="nx">userMessage</span><span class="p">)</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl"> <span class="kr">const</span> <span class="nx">response</span> <span class="o">=</span> <span class="kr">await</span> <span class="nx">openai</span><span class="p">.</span><span class="nx">chat</span><span class="p">.</span><span class="nx">completions</span><span class="p">.</span><span class="nx">create</span><span class="p">({</span>
</span></span><span class="line"><span class="cl"> <span class="nx">model</span><span class="o">:</span> <span class="s2">"gpt-3.5-turbo"</span><span class="p">,</span>
</span></span><span class="line"><span class="cl"> <span class="nx">messages</span><span class="o">:</span> <span class="p">[</span>
</span></span><span class="line"><span class="cl"> <span class="p">{</span> <span class="nx">role</span><span class="o">:</span> <span class="s2">"system"</span><span class="p">,</span> <span class="nx">content</span><span class="o">:</span> <span class="s2">"You are a helpful assistant."</span> <span class="p">},</span>
</span></span><span class="line"><span class="cl"> <span class="p">{</span> <span class="nx">role</span><span class="o">:</span> <span class="s2">"user"</span><span class="p">,</span> <span class="nx">content</span><span class="o">:</span> <span class="nx">userMessage</span> <span class="p">}</span>
</span></span><span class="line"><span class="cl"> <span class="p">]</span>
</span></span><span class="line"><span class="cl"> <span class="p">});</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"> <span class="k">return</span> <span class="nx">response</span><span class="p">.</span><span class="nx">choices</span><span class="p">[</span><span class="mi">0</span><span class="p">].</span><span class="nx">message</span><span class="p">.</span><span class="nx">content</span><span class="p">;</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c1">// Example usage
</span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="nx">chatbot</span><span class="p">(</span><span class="s2">"Hello, how are you?"</span><span class="p">).</span><span class="nx">then</span><span class="p">(</span><span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">);</span>
</span></span></code></pre></div><h2 id="next-steps">
 Next Steps
 
 <a class="anchor" href="#next-steps">#</a>
</h2>
<ul>
<li>Add conversation history</li>
<li>Implement streaming responses</li>
<li>Add custom personality</li>
</ul>
