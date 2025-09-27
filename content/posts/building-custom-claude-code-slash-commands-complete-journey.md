---
title: "Building Custom Claude Code Slash Commands: The Complete Implementation Journey"
date: 2025-09-27T17:00:00-06:00
draft: false
tags: ["claude-code", "automation", "hugo", "workflow", "developer-tools", "ai", "documentation"]
author: "Jeremy Longshore"
description: "The complete story of building custom slash commands for automated blog publishing - including false starts, troubleshooting, and iterative refinements that led to a working system"
---

How we built custom Claude Code slash commands that analyze git history, generate contextual blog posts, and automatically deploy to production Hugo sites - including every misstep, troubleshooting session, and design iteration along the way.

## The Starting Point: A Misdiagnosis

"My blogs aren't posting - how many posts do you show in relation to GitHub commits that should have posted new content?"

That's how this session started. I was convinced my blog deployment was broken. Turns out, after checking the filesystem and live sites, everything was working perfectly - 27 posts in source, 27 posts published, all visible on startaitools.com with proper pagination.

**The real problem wasn't broken deployment. It was that I wanted an easier way to create posts.**

This misdiagnosis actually led somewhere better: recognizing that the friction wasn't in the system being broken, but in the publishing workflow being too manual.

## The Actual Problem: Documentation Friction

Once we established the blogs were working, the conversation pivoted:

**Me:** "I want Claude to make a blog post on what we are working on... I'm working on a document system and I think 'oh this would be a cool blog post' - I want to run a slash command that gives Claude instructions to create a blog post on our past work since my last blog post."

**The Vision:**
- Be deep in work on any project
- Think "this would make a great blog post"
- Run a slash command
- Claude analyzes recent git history and conversation context
- Generates technical narrative about what was built
- Auto-publishes to blog

Two separate commands:
- `/blog-startaitools` - Technical teaching content (Intent Solutions audience)
- `/blog-jeremylongshore` - Personal portfolio/CV style

## The Design Conversation

We talked through what these commands should actually do:

**Context Collection Decisions:**
- **How far back?** Since last blog post date (ensures nothing missed)
- **What to analyze?** Current project only (I'll be diligent about running it)
- **Cross-linking?** Automatic smart search of existing posts

**Content Strategy:**
- Mix case study + tutorial + technical depth
- Honest, truth-based (no "founder's log" fluff)
- Educational value in the repo code itself
- Show what I built AND how I built it

**The Review Step:**
Critical decision: Show draft first, get approval before publishing. Automation is powerful, but blog posts represent professional brand.

## Implementation Attempt #1: The Files That Didn't Work

We created the command files:

```bash
~/.claude/commands/blogstartaitools.md
~/.claude/commands/blogjeremylongshore.md
```

**Tried running them:**
```
Unknown slash command: blogstartaitools
```

**First troubleshooting theory:** Maybe no hyphens? The existing commands use hyphens (`create-prd`, `generate-tasks`).

Renamed to `blog-startaitools.md` and `blog-jeremylongshore.md`.

**Still didn't work:**
```
Unknown slash command: blog-startaitools
```

## Troubleshooting Session: Why Aren't Commands Recognized?

**Investigation steps:**

1. **Check file extensions** - Confirmed all existing working commands use `.md`
2. **Compare file formats** - Looked at `create-prd.md` vs our new files
3. **Check for YAML frontmatter issues** - Our files had frontmatter, working ones didn't
4. **Read Claude Code docs** - Found examples with and without frontmatter

**Key discovery:** We had added YAML frontmatter like this:
```yaml
---
name: blogstartaitools
description: Generate and publish technical blog post
---
```

But the working commands were just **plain text instructions** with no frontmatter at all!

**Fix:** Removed the YAML frontmatter, kept just the instructions.

**Still didn't work.**

## The Actual Solution: Dynamic Command Discovery

Created a test command to verify the system:

```bash
# ~/.claude/commands/test-command.md
This is a test command. Just say "Test command is working!"
```

**Tried it:**
```
Unknown slash command: test-command
```

**Then a few seconds later, tried again - it worked!**

This revealed: Claude Code **DOES** pick up new commands during active sessions, but there might be a slight delay or the command needs to be invoked once to register.

Once `/test-command` worked, `/blog-startaitools` and `/blog-jeremylongshore` started working too.

**The real issue:** Not file format, not naming - just needed the system to discover them. Creating a simple test command first helped verify the discovery mechanism.

## The Missing Context Problem

After the commands worked, I asked a critical question:

**"When you create these posts, are you taking into account what we have been doing in our entire working session?"**

Great catch. The initial implementation only looked at git commits. It missed:
- Our conversation about what workflow I wanted
- The troubleshooting journey (unknown command errors)
- Testing different formats and naming conventions
- The iterative problem-solving process
- Everything we learned along the way

**This was the key insight:** The git commits show the final result. The conversation shows the thinking, the false starts, the learning - which is WAY more valuable for teaching others.

## Updating Commands for Full Context Capture

We revised both command files to analyze:

```markdown
1. **Analyze ENTIRE Working Session**
   - Git History: Commits since last post
   - Current Conversation: COMPLETE conversation history
     - What problem were we solving?
     - What solutions did we try that failed?
     - What troubleshooting steps did we take?
     - What was the iterative process?
     - What did we learn?
   - Project Context: File changes, TODOs, CLAUDE.md
   - The Journey: Capture full story - false starts, pivots, discoveries
```

**Key additions to the instructions:**
- "Show the entire journey - problems, false starts, troubleshooting, solutions"
- "Don't sanitize the process - readers learn more from seeing troubleshooting"
- "If we tried 3 things before one worked, document all 3 attempts"
- "What you're writing about just happened in this session - use that context!"

## The Commands in Action: Testing the System

Ran `/blog-jeremylongshore` first - it worked! Generated a portfolio-style post that included:
- The challenge we were solving
- Our problem-solving approach
- The troubleshooting we did
- Skills demonstrated
- Professional growth narrative

Published successfully to jeremylongshore.com (commit `5e3ca77`).

Now creating this startaitools post to document the technical journey.

## Technical Implementation Details

### Command File Structure

Location: `~/.claude/commands/[command-name].md`

Format: Plain text markdown, no YAML frontmatter needed

```markdown
Generate and publish a technical blog post to startaitools.com.

## Your Task

1. **Analyze ENTIRE Working Session**
   - Git history since last post
   - Complete conversation context
   - Project files and changes

2. **Find Cross-Links**
   - Search existing posts
   - Identify 2-3 related articles

3. **Write the Blog Post**
   - Technical, honest, factual tone
   - Show the journey, not just destination
   - Include false starts and troubleshooting

4. **Show Draft for Review**
   - Display complete post
   - Wait for approval

5. **Publish (After Approval)**
   - Create markdown file
   - Run Hugo build
   - Git commit and push
```

### The Workflow

When you run `/blog-startaitools`:

1. Claude reviews the entire conversation
2. Checks git commits since last blog post date
3. Examines current project context
4. Finds 2-3 related posts for cross-linking
5. Generates draft with complete journey
6. Shows you the draft
7. After approval: creates file, builds site, commits, pushes

### Design Decisions Worth Noting

**Two Separate Commands**
- Different audiences need different tones
- Technical blog vs portfolio blog serve different purposes
- Same analysis, different narrative presentation

**Conversation Context Over Git Only**
- Git shows what changed
- Conversation shows why and how
- The troubleshooting IS the education

**Review Before Publish**
- Automation handles mechanics
- Human judgment maintains quality
- Best of both worlds

**Current Directory as Context**
- Run from project you're working on
- Natural scoping without extra configuration
- Git history tells the story automatically

## Real-World Results: Repository Cleanup

Today's work that these commands documented:

**startaitools cleanup:**
- Removed 5 empty directories
- Updated .gitignore (added hugo_stats.json)
- Commit: `c57f4aa`

**jeremylongshore cleanup:**
- Removed 5,370 lines of backup theme files
- Cleaned GitHub templates and docs
- Improved .gitignore
- Commit: `f91f3bb`
- Plus this automation work: `5e3ca77`

Both sites tested, built successfully, deployed automatically.

## What We Learned

### 1. Misdiagnosed Problems Lead to Better Solutions

Started thinking deployment was broken. Actually discovered a better workflow for content creation.

### 2. Troubleshooting IS the Education

The journey from "Unknown slash command" to working implementation teaches more than just showing the final code.

### 3. Context > Code

Git commits document what changed. Conversation context documents why decisions were made and how problems were solved. Both matter.

### 4. Simple Formats Win

Plain markdown instructions work better than complex YAML configurations. Easier to write, easier to maintain, easier to debug.

### 5. Iteration Reveals Requirements

Didn't realize we needed full conversation context until after the first implementation. User feedback ("are you taking into account our entire session?") drove the refinement.

### 6. Test with Simple Cases First

Creating `/test-command` helped verify the command discovery mechanism before debugging complex command files.

## Related Posts

- [Complete Hugo Site Operations Guide](/posts/complete-hugo-site-operations-guide/) - Production Hugo workflows and deployment strategies
- [From Chaos to One-Paste Magic](/posts/ai-dev-chaos-to-magic-complete-series/) - Building AI-powered documentation pipelines
- [Speed DevOps Methodology](/posts/speed-devops-methodology-48-hour-deployments/) - Rapid deployment workflows in 48-72 hours

## Next Steps & Possibilities

**Immediate Use:**
- Run these commands from any project when work is done
- Automatic documentation becomes natural part of workflow
- Zero-friction publishing encourages consistent output

**Future Enhancements:**
- Additional commands for different content types
- Integration with analytics for performance tracking
- Automated cross-promotion between sites
- Template variations for different post structures

**Broader Applications:**
The principle extends beyond blogging. Any repetitive workflow with clear structure becomes a candidate for intelligent automation through custom slash commands.

## Try It Yourself

The command files are in this blog's repository. To implement your own:

1. Create `~/.claude/commands/your-command.md`
2. Write clear instructions for what you want
3. Test with a simple command first (`/test-command`)
4. Iterate based on results
5. Don't overthink the format - plain text works

The value isn't just in the automation - it's in the forcing function that makes documentation a natural byproduct of development work rather than a separate chore.

---

**Implementation Note:** This post was generated by the `/blog-startaitools` command we just built, demonstrating the system documenting its own creation. Meta, but practical.

*Complete command implementation available in the [startaitools repository](https://github.com/jeremylongshore/startaitools.com) at `~/.claude/commands/blog-startaitools.md` for reference.*