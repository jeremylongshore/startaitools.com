# Dispatch Design System

The visual + interaction system for startaitools.com. Code lives in `assets/css/tokens.css` (tokens) and `assets/css/custom.css` (components). This doc is the human-readable map.

## Aesthetic

**Editorial dark with terminal accents.** Dark default, light toggle. The body type is editorial-weight serif (Source Serif 4); UI labels are sharp Inter; code is JetBrains Mono with ligatures. Motion is functional — hover lift on cards, fade-up on sections, pulse on the live-dispatch indicator. No parallax, no particles, no marquee.

## Tokens

Tokens are OKLCH-based for perceptual uniformity. Light and dark themes each define their own ladder; auto-detect via `prefers-color-scheme` if no explicit preference is stored.

### Surface ladder (dark)
| Token | OKLCH | Use |
|---|---|---|
| `--bg-base` | 14% / 0.008 | Page background |
| `--bg-elev-1` | 18% / 0.009 | Cards, header (with backdrop-filter) |
| `--bg-elev-2` | 22% / 0.010 | Card hover state |
| `--bg-elev-3` | 28% / 0.011 | Modals, dropdowns |
| `--bg-inset` | 11% / 0.007 | Code blocks, deeply recessed surfaces |

### Text
| Token | Use |
|---|---|
| `--fg` | Body text, headings |
| `--fg-muted` | Secondary text, post summaries |
| `--fg-subtle` | Metadata, captions |
| `--fg-faint` | Disabled states, footer copyright |

### Accents (only two — that's the rule)
- `--accent-warm` — amber `oklch(80% 0.16 65)` in dark mode. Brand mark, primary CTA, "live" indicators, hover state on text.
- `--accent-cool` — cyan `oklch(74% 0.14 220)` in dark mode. Categories, info badges, secondary links.

Anything more chromatic = banned. Two accents, one warm, one cool.

## Type scale

1.250 modular scale, base 17px on desktop / 16px ≤600px:

```
--fs-xs:    0.75rem    (12.75px)
--fs-sm:    0.875rem   (14.875px)
--fs-base:  1rem       (17px)
--fs-md:    1.125rem   (19.125px)
--fs-lg:    1.25rem    (21.25px)
--fs-xl:    1.5625rem  (26.5px)
--fs-2xl:   1.953rem   (33.2px)
--fs-3xl:   2.441rem   (41.5px)
--fs-4xl:   3.052rem   (51.9px)
--fs-5xl:   3.815rem   (64.9px)
```

- Headings: Inter (UI), tight tracking (-0.015 to -0.03em).
- Body: Source Serif 4, line-height 1.7.
- Code: JetBrains Mono, ligatures off (`liga: 0`, `calt: 1`).
- Hero h1 + post h1 use serif at large size for editorial weight.

## Spacing & layout

4px-rhythm spacing scale (`--sp-1` through `--sp-24`). Layout containers:

- `--reading-col: 720px` — single-post reading column
- `--container: 1200px` — section grid
- `--container-wide: 1440px` — feature wide layouts

## Components inventory

| Component | Selector | Where used |
|---|---|---|
| Hero | `.hero` | Homepage |
| Post card | `.post-card` | Recent grid + section listings |
| Feature card | `.feature-card` (+`--hero` modifier) | Featured grid |
| Series tile | `.series-tile` | Ongoing series row |
| Recap card | `.recap-card` | Monthly recaps row |
| Stat | `.stat` (+`.stat-number[data-count]`) | Hero strip |
| TOC | `.toc` | Single posts with `toc = true` |
| TLDR | `.tldr` | Single posts with `tldr = "..."` |
| Tags | `.tags`, `.tags a` | Post footer |
| Search trigger | `.search-trigger` | Header |
| Theme toggle | `#theme-toggle` | Header |
| Reading progress | `.reading-progress` | Single posts |
| Chapter list | `.chapter-list`, `.chapter-list a::before` (counter) | Feature cover |
| Chapter sidebar | `.chapter-sidebar` | Feature single |
| Chapter nav | `.chapter-nav` | Feature single |
| Subscribe form | `.subscribe-form` | Footer (Netlify form schema preserved verbatim) |

## Motion

| Animation | Trigger | Duration | Easing |
|---|---|---|---|
| Card hover lift | `:hover` on `.post-card`, `.feature-card`, `.series-tile`, `.recap-card`, `.btn` | `--dur-base` (200ms) | `cubic-bezier(0.2, 0.8, 0.2, 1)` |
| Fade-up reveal | `IntersectionObserver` on `[data-reveal]` | `--dur-slow` (320ms) | same |
| Brand dot pulse | always | 2.4s loop | same |
| Theme toggle | click on `#theme-toggle` | View Transitions API where available | browser default |
| Stats counter | `IntersectionObserver` once visible | 1200ms | ease-out cubic |
| Reading progress | scroll | 80ms linear | linear |

`prefers-reduced-motion: reduce` disables every animation, sets `[data-reveal]` to `opacity:1; transform:none`, and removes hover-lift transforms. The live-dispatch dot freezes.

## Accessibility

- Color contrast: every fg/bg pair tested for WCAG AA 4.5:1. Light + dark independently.
- Focus rings: 2px outline, 3px offset, `--focus-ring` color (cyan in both modes).
- Skip links: not currently provided — TODO if accessibility audit demands.
- Heading hierarchy: one h1 per page, h2 for sections, h3 for sub-sections. The theme's `# ` markdown-style prefix is suppressed via `::before { content: '' !important }`.
- Keyboard:
  - `⌘K` / `Ctrl+K` opens search modal
  - `/` opens search (when nothing else focused)
  - `Esc` closes search modal
  - All buttons reachable via tab order
- ARIA: header `aria-label="Primary"`, toggle `aria-label="Toggle theme"`, current page marked `aria-current="page"`, search modal `role="dialog" aria-modal="true"`.

## Implementation notes

- Archie theme override: we replace `partials/header.html` (the `<head>`) and `partials/head.html` (the visible `<header>`) — note the inverted naming Archie uses.
- The theme's `main.css` and `dark.css` are still loaded by archie's logic, but our `tokens.css` + `custom.css` come AFTER and override every selector that matters. We don't fork the theme.
- Pagefind is wired into Netlify's build command (`hugo … && npx pagefind --site public`); the script in `main.js` lazy-loads `/pagefind/pagefind-ui.js` only when the user opens the search modal.
- Fonts are loaded from `fonts.bunny.net` (privacy-respecting Google Fonts mirror — same files, no Google fingerprinting). Swapping to self-hosted woff2 is a 2-line change in `partials/header.html` if cookie/consent posture demands it later.

## Files of record

| Concern | File |
|---|---|
| Tokens (palette, type, spacing) | `assets/css/tokens.css` |
| Components, layouts | `assets/css/custom.css` |
| Theme bootstrap (FOUC-free) | `<script>` in `layouts/partials/header.html` |
| Interaction (toggle, scroll, search, counter) | `assets/js/main.js` |
| Visible header | `layouts/partials/head.html` |
| Footer (incl. Netlify form) | `layouts/partials/footer.html` |
