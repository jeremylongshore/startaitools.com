+++
title = 'From one adopter to two: the discovery-affordance spec just got named'
slug = 'discovery-affordance-second-adopter'
date = 2026-06-04T08:00:00-05:00
draft = false
tags = ["spec", "ecosystem", "claude-code", "marketplaces", "discovery"]
categories = ["AI Engineering"]
description = "A 39.7k-star skills repo adopted my discovery-manifest pattern by name. What changed, why it matters, and the install_source_url work that comes next."
+++

A few weeks ago I shipped schema 3.4.0 on [claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills). The headline feature: a single machine-crawlable manifest indexing 2,783 skills, ~97 KB gzipped. Any client — a marketplace UI, a CLI installer, a federated search index — can browse or search the catalog without scraping the repo directory by directory.

The point of the manifest wasn't "here is a better README." It was a bet that skill ecosystems past a few hundred entries need an affordance for clients, not just humans. Without one, every new tool has to write a custom crawler against each repo's layout. With one, the work happens once at the spec layer and any compliant index is queryable.

I shipped it. One launch consumer (mine). Whether the bet held depended entirely on whether anyone else built against the same shape.

## The validation moment

Two weeks ago `latentloop07` — building [skillnote](https://github.com/luna-prompts/skillnote) at luna-prompts — opened [issue #596](https://github.com/sickn33/antigravity-awesome-skills/issues/596) on [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills). The repo is a 39,715-star skills library, currently around 1,500 skills across Claude Code, Cursor, Codex CLI, Gemini CLI, Antigravity, and others. The issue title: *"at 1,400 skills, how are users actually picking which to install?"*

The body lays out the discovery problem at scale, then names my work as the existing model:

> jeremylongshore just shipped one for his 2,783-skill `claude-code-plugins-plus-skills` collection (schema 3.4.0, 97 KB gzipped) and it's the cleanest path we've seen for federated discovery so far.

I didn't file the issue. I didn't post in the thread. The pattern got picked up because the artifact was there to point at.

sickn33 — the repo owner — responded by shipping it. The closeout comment is the part worth reading verbatim:

> We addressed it on `main` with a stable discovery-manifest contract rather than asking clients or users to scrape the full repository: kept the root `skills_index.json` as the canonical public manifest in the existing array format; mirrored that manifest exactly to `data/skills_index.json` for compatibility with integrations that already look under `data/`; added `schemas/skills-index.v1.schema.json` so downstream consumers can validate the manifest shape; added `docs/users/discovery-manifest.md` documenting the canonical root manifest, compatibility mirror, array compatibility, lazy-loading pattern, and the expectation that clients should not load every skill up front.
>
> That gives us the **Jeremy Longshore-style discovery affordance** without replacing the existing canonical public manifest or forcing a breaking format change.

That's the line that made me pause. Not the adoption — the naming. A 39.7k-star repo's maintainer wrote "Jeremy Longshore-style discovery affordance" into a public closeout comment, into a file format that lives in the repo on `main`, where future contributors will read it as the canonical reference for why the schema exists.

## Why "spec, not opinion"

Single-repo specs are easy to mistake for what they're not. Anyone can write a JSON schema, slap a version on it, and call it a standard. Until someone else builds against it, the schema is a strongly-held opinion with a `.json` extension.

MarketplaceJsonProvider — the consumer-side abstraction skillnote is building — needed at least two real upstream implementations before its shape could be trusted. With one source, the abstraction quietly inherits everything that source happens to do. With two, the abstraction has to actually hold up against both.

As of the closeout, that's the state:

- `claude-code-plugins-plus-skills` schema 3.4.0 — 2,783 skills, my repo
- `sickn33/antigravity-awesome-skills` `skills-index.v1.schema.json` — ~1,500 skills, independent author

latentloop07's [skillnote](https://github.com/luna-prompts/skillnote) is wiring its `MarketplaceJsonProvider` adapter to ingest both from day one. That's the consumer side of the same spec story: two independent upstreams, one consumer abstraction, and the abstraction has to survive being implemented against both without leaking either schema's quirks.

Two adopters is the floor, not the ceiling. But it's the line below which "spec" doesn't mean anything.

## What this means for tonsofskills.com users

The practical effect for anyone using the [tonsofskills.com](https://tonsofskills.com) marketplace: the catalog isn't trapped in a single-vendor index anymore.

When a third-party tool wants to surface a skill from claude-code-plugins-plus-skills or from antigravity-awesome-skills, it doesn't need a custom integration for either. It reads the manifest, filters by category or risk profile, and lazy-loads only the specific `SKILL.md` bodies it needs to render. The marketplace UX gets to focus on browse-and-install instead of crawl-and-cache.

For end users that translates to one thing: discovery scales past the point where reading a README is feasible. If you've ever tried to find the right skill in a 1,400-entry directory tree without a search box, you've felt the gap the manifest closes.

## What comes next: `install_source_url`

The current schema lets a consumer find a skill. It doesn't yet tell the consumer where to install it from in a fully machine-readable way. The convention right now is heuristic — strip the path, prepend the GitHub raw URL, assume the layout. Works most of the time. Fails silently the rest.

The next schema-feature is a per-entry `install_source_url` field: an explicit, validated URL pointing to the raw `SKILL.md` (or skill bundle) that a client can fetch and install verbatim. No path heuristics. No "assume the repo's layout follows convention X." The skill says where it lives, and the installer respects that.

Why it matters past the immediate convenience:

- **Vendored skills become first-class.** A skill that lives outside the manifesting repo (mirrored, forked, hosted on a CDN) can declare its real install URL without the manifest having to lie about location.
- **Cross-repo installs become safe.** A consumer that pulls from multiple upstreams doesn't have to maintain a per-upstream URL-construction rule. Each entry self-describes.
- **Audit trails get cleaner.** "Where did this skill come from" becomes a single field lookup, not an inference.

latentloop07 mentioned filing the `install_source_url` schema-feature request against my repo this week, sketched against the real sickn33 dataset. That's the next milestone for the spec — the first field added under multi-adopter pressure rather than single-vendor opinion. Different bar.

## The take-home

If you write a spec, you find out fast whether anyone wanted it. The signal isn't stars or downloads — it's whether somebody else, working independently, builds against the same shape and names it the same thing. That's the moment an opinion stops being yours.

In this case, the moment came with a verbatim closeout comment on a 39.7k-star repo and a third-party consumer wiring both upstreams into one abstraction. Two adopters, one spec, one consumer in progress. The next test is whether `install_source_url` survives the same scrutiny — added because both implementers want the same field, not because one repo's maintainer thought it'd be nice.

I'll write up the `install_source_url` design when the schema PR lands. In the meantime:

- The spec lives at [claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills).
- The marketplace surfacing the catalog is at [tonsofskills.com](https://tonsofskills.com).
- The thread that named the pattern: [sickn33/antigravity-awesome-skills#596](https://github.com/sickn33/antigravity-awesome-skills/issues/596).
- The skillnote adapter (consumer side): [luna-prompts/skillnote](https://github.com/luna-prompts/skillnote).

PRs and feedback welcome.
