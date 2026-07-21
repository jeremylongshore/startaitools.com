# startaitools · with Intent Solutions — Design System

Source of truth for the startaitools.com brand. startaitools is an Intent Solutions
property; it must read as the same family as **intentsolutions.io** (charcoal + ember)
while keeping its editorial reading experience for long-form posts.

Convention borrowed from [nexu-io/open-design](https://github.com/nexu-io/open-design)
(`DESIGN.md` design-system pattern, Apache-2.0).

## Identity

- **Wordmark:** `● startaitools · with Intent Solutions` — `startaitools` lowercase in
  Syne 700; `· with Intent Solutions` in Inter, muted. Ember brand dot leads.
- **Parent brand:** Intent Solutions (intentsolutions.io). Always cross-link back.
- **One-liner:** "AI systems, shipped in production."

## Palette (matches intentsolutions.io "Charcoal Slate + Ember")

| Token | Light | Dark | Use |
|---|---|---|---|
| Charcoal bg | graphite `oklch(98.5% …)` | `#18181B` zinc-900 | page background |
| **Ember (brand)** | `oklch(63% 0.205 40)` | `#F97316` / hover `#FB923C` | links, CTAs, brand dot, accents |
| Text | zinc-900 | zinc-50 | body |
| Muted | zinc-500/600 | zinc-400 | secondary |

Ember is the single interactive/brand color. Implemented as `--brand` / `--brand-hover`
/ `--brand-ink` / `--brand-glow` in `assets/css/tokens.css` (ember overlay block,
appended last so it wins over the editorial amber/cyan defaults).

## Type

- **Display / wordmark:** Syne 600–800 (`--font-display`).
- **Body / UI:** Inter (`--font-sans`).
- **Article prose:** Source Serif 4 (`--font-serif`) — the editorial reading voice, kept.
- **Code:** JetBrains Mono (`--font-mono`).

## Components

- **Ember CTA** (`.btn-ember`, `.nav-cta`): filled ember pill/button, glow shadow.
- **Ghost button** (`.btn-ghost`): outlined, ember on hover.
- **End-of-post CTA** (`.post-cta`, partial `contact-cta.html`): ember-topped card with an
  inline email capture at the highest-intent moment (posts only).
- **Contact form** (`.contact-form`, `content/contact.md`): name / email / company / message.

## Contact capture (the conversion path)

All lead capture posts to the shared **forms-api** on the VPS via the Netlify rewrite
`/api/forms/* → tonsofskills.com/api/forms/:splat`:

- Newsletter → `POST /api/forms/signup` (footer). Lands in Slack leads-newsletter.
- **Lead / hire → `POST /api/forms/contact`** (`{name,email,company,message,source,website}`).
  Lands in **Slack leads-contact** channel + dead-letter spool. Same pipeline as
  intentsolutions.io. Honeypot field is `website`; rate-limited server-side.
- Direct: `mailto:jeremy@intentsolutions.io` everywhere as the always-works fallback.

Three surfaces: persistent header "Work with us" button, end-of-post inline CTA, full
`/contact/` form. Contact is also in the main nav.

## Social / link previews (OG)

Per-post cards generated at build time by `layouts/partials/social-meta.html` via Hugo
`images.Text` over `assets/images/og-base.png` (baked by `scripts/blog/make-og-base.py`).
The post's real title + `CATEGORY · N min` overlay the charcoal+ember base. Home/sections
fall back to `static/images/og-default.png`. Single source of truth for all og/twitter
tags — do not re-add `_internal/opengraph.html` (it double-emitted `og:image`).

## Voice

Operator-turned-builder, blunt, dash-free in posts, no AI slop. See the blog pipeline voice
rules (`~/.claude/skills/blog-backfill/references/write-post.md` + `voice-denylist.json`).
