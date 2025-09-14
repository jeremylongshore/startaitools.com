---
title: "Founder's Log: Juggling Google Calls, Scraping Bugs, and Startup Hustle"
date: 2025-09-09T00:00:00Z
draft: false
tags: ["Founder's Log", "Startups", "AI", "Development", "Google Cloud", "Web Scraping", "BigQuery", "Daily Updates", "Entrepreneurship", "Bug Fixes"]
---

It's been an intense but productive time here at Intent Solutions. Building a startup is a constant juggling act, and this week has been no exception.

### High-Level Hustle

The momentum on the business front is exciting and, frankly, a bit overwhelming since getting a call from Google. It's a reminder of the potential we're tapping into. We're also swinging for the fences and have submitted a request for Google Ad credits—we'll see what happens!

On the marketing side, we've brought on Jules with a two-week plan to see if he can execute on our vision. To facilitate collaboration, we've set up a new Slack channel, `#big-picture-research-thoughts-ideas`, where the team can comment, post, and generate new ideas in threads.

### Technical Deep Dive: The Scraping Challenge

I spent about an hour and a half this week on a technical rabbit hole. I was trying out a JSON scraping hack I saw from [@theahmadosman on X](https://x.com/theahmadosman), which involves grabbing URLs and appending `.json` to them. While I was able to get the URLs, I hit a wall when trying to wire up the headless browser to process them.

I kept getting 403 Forbidden errors. The code is up on our GitHub in the `scrapers` directory of the Diagnostic Pro repo if anyone wants to take a look. It's a frustrating contrast to the last big data pull I did directly from the Reddit API, where I successfully grabbed over 11,000 data items.

We're also looking for an expert to help with building out our chat capabilities after the initial AI diagnostics are complete. I've been chatting with a promising contact from YouTube on LinkedIn about this.

### A Founder's Learning Curve

As a self-described "non-tech bro," the learning curve has been steep, but incredibly rewarding. I've learned a ton about Linux, Ubuntu/Debian, the command line, and of course, AI. But the biggest challenge often comes from the simplest-sounding tasks.

For instance, the Google Cloud migration I mentioned on the roadmap? I wouldn't have to do it at all, but I screwed up the billing accounts. I started with a Gmail account and then added a domain account, which somehow locked me out of the original. It was a mess.

My most persistent frustration, however, is my current inability to figure out a smooth workflow for creating and uploading a file from my mobile devices. I'm on my iPhone a ton and my iPad at night, but getting a file from them to my Contabo VM is a struggle. My old laptop won't connect to my phone's hotspot anymore (I think one of the kids crushed it), so a mobile-first workflow is essential.

It's not for lack of trying. I've implemented FileBrowser and Caddy. I'm using Termius, which has its own SFTP, and I've experimented with a whole stack of tools: Textastic, Koder, Secure ShellFish, and Working Copy. I know I'm missing something simple. Maybe I should read the manual, but it shouldn't be that hard, should it?

It's a humbling process. I can get a VM running with 48GB of RAM to host an LLM, but I'm getting tripped up moving a text file. It's all part of the journey.

### The Immediate Roadmap

The to-do list is long, but here are the critical next steps:

1.  **Finalize the LLC:** This is a top priority. It's blocking our applications for several startup programs, including the NVIDIA startup program.
2.  **Cloud Migration:** We need to begin the process of moving everything from Loveable and Supabase to Google Cloud.
3.  **Investigate Coder:** I need to install GTM 5 (or Coder) and evaluate its capabilities and pricing.

It's a lot to manage while still working a full-time job, and it's becoming clear that we'll need more help to keep up the pace. But the challenges are part of the journey, and we're excited for what's next.
