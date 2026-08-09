#!/usr/bin/env python3
"""make-social-card.py: render the per-post social cards. PIL only, no network.

This is the GUARANTEED baseline. Every post gets a card, every time, for free:
no API key, no quota, no vendor, no failure mode beyond "PIL is not installed".
Generated art (make-post-image.py) is the upgrade on top; when generation is
switched off, fails twice, or the key is missing, the card is what ships.

Two sizes, because the platforms want different crops:
  1200x630  landscape, the Open Graph and X/LinkedIn link-preview size
  1080x1080 square, the in-feed image size

Design is inherited from make-og-base.py so the cards read as one family:
charcoal ground, ember rules top and bottom, the wordmark, the domain. What is
new here is per-post content in the middle band: the title, wrapped and
auto-fitted, and an optional pull-quote underneath it.

Auto-fit matters. A 12-word title at a fixed point size runs off the canvas, and
a card that clips its own title is worse than no card. The renderer drops the
title size in steps until the wrapped block fits its band, so a long title comes
out smaller rather than cropped.

Usage:
  make-social-card.py --title "Post title" [--quote "pull quote"] [--slug slug]
                      [--outdir static/images/cards] [--json]
  make-social-card.py --post content/posts/slug.md [--outdir ...] [--json]

Exit 0 on success, 2 on usage/IO error.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:  # pragma: no cover - environment problem, not logic
    print("Pillow is required: pip install Pillow", file=sys.stderr)
    raise SystemExit(2) from exc

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONTS = os.path.join(ROOT, "assets", "fonts")
DEFAULT_OUTDIR = os.path.join(ROOT, "static", "images", "cards")

# Brand palette, identical to make-og-base.py. Do not drift these.
CHARCOAL = (24, 24, 27)
CHARCOAL_DK = (14, 14, 16)
EMBER = (249, 115, 22)
WHITE = (250, 250, 250)
MUTED = (161, 161, 170)

# (width, height, suffix)
SIZES = [(1200, 630, "og"), (1080, 1080, "square")]


def load_font(name: str, size: int, weight: int | None = None) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(os.path.join(FONTS, name), size)
    if weight is not None:
        try:
            font.set_variation_by_axes([weight])
        except Exception:  # noqa: BLE001 - static build of the font, weight is baked
            pass
    return font


def wrap_to_width(draw, text: str, font, max_width: int) -> list[str]:
    """Greedy word wrap against real measured text width, not a character count."""
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def fit_title(draw, text: str, max_width: int, max_lines: int,
              start: int, floor: int, step: int = 4):
    """Shrink the title until its wrapped block fits the band.

    Returns (font, lines). A long title comes out smaller. It never comes out
    clipped, and it never silently loses its tail: at the floor size we accept
    whatever wraps and truncate the overflow with an ellipsis so the failure is
    visible rather than invisible.
    """
    size = start
    while size > floor:
        font = load_font("Syne-var.ttf", size, 700)
        lines = wrap_to_width(draw, text, font, max_width)
        if len(lines) <= max_lines:
            return font, lines
        size -= step
    font = load_font("Syne-var.ttf", floor, 700)
    lines = wrap_to_width(draw, text, font, max_width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(" ,.;:") + "..."
    return font, lines


def render(width: int, height: int, title: str, quote: str = "") -> Image.Image:
    img = Image.new("RGB", (width, height), CHARCOAL)
    px = img.load()
    for y in range(height):
        t = y / height
        px_row = (
            int(CHARCOAL[0] + (CHARCOAL_DK[0] - CHARCOAL[0]) * t),
            int(CHARCOAL[1] + (CHARCOAL_DK[1] - CHARCOAL[1]) * t),
            int(CHARCOAL[2] + (CHARCOAL_DK[2] - CHARCOAL[2]) * t),
        )
        for x in range(width):
            px[x, y] = px_row

    d = ImageDraw.Draw(img)
    rule = max(6, round(height * 0.0127))
    d.rectangle([0, 0, width, rule], fill=EMBER)
    d.rectangle([0, height - rule, width, height], fill=EMBER)

    scale = width / 1200
    margin = round(70 * scale)
    content_w = width - 2 * margin

    # Wordmark, top left.
    wm = load_font("Syne-var.ttf", round(40 * scale), 700)
    wm_sub = load_font("Inter-var.ttf", round(34 * scale), 400)
    x, y = margin, round(54 * scale)
    dot_r = round(9 * scale)
    cy = y + round(26 * scale)
    d.ellipse([x, cy - dot_r, x + 2 * dot_r, cy + dot_r], fill=EMBER)
    x += 2 * dot_r + round(18 * scale)
    d.text((x, y), "startaitools", font=wm, fill=WHITE)
    x += d.textlength("startaitools", font=wm) + round(16 * scale)
    d.text((x, y + round(6 * scale)), "· with Intent Solutions", font=wm_sub, fill=MUTED)

    # Title band. The square crop is taller, so it can carry more lines.
    max_lines = 3 if height <= 700 else 5
    title_font, lines = fit_title(
        d, title, content_w, max_lines,
        start=round(62 * scale), floor=round(30 * scale),
    )
    line_h = round(title_font.size * 1.22)
    quote_font = load_font("Inter-var.ttf", round(28 * scale), 400)
    quote_lines = wrap_to_width(d, quote, quote_font, content_w)[:3] if quote else []
    quote_h = round(quote_font.size * 1.45) * len(quote_lines)
    quote_gap = round(34 * scale) if quote_lines else 0

    band_top = round(150 * scale)
    band_bottom = height - round(110 * scale)
    block_h = line_h * len(lines) + quote_gap + quote_h
    ty = band_top + max(0, (band_bottom - band_top - block_h) // 2)

    for i, line in enumerate(lines):
        # First line ember, rest white. Gives the card a focal point without
        # needing an image behind it.
        d.text((margin, ty + i * line_h), line, font=title_font,
               fill=EMBER if i == 0 else WHITE)
    ty += line_h * len(lines) + quote_gap

    if quote_lines:
        bar_x = margin
        bar_top = ty + round(6 * scale)
        bar_bot = ty + quote_h - round(6 * scale)
        d.rectangle([bar_x, bar_top, bar_x + round(4 * scale), bar_bot], fill=EMBER)
        qx = bar_x + round(20 * scale)
        for i, line in enumerate(quote_lines):
            d.text((qx, ty + i * round(quote_font.size * 1.45)), line,
                   font=quote_font, fill=MUTED)

    # Domain, bottom right.
    dom_font = load_font("Inter-var.ttf", round(26 * scale), 500)
    dom = "startaitools.com"
    d.text((width - margin - d.textlength(dom, font=dom_font),
            height - round(60 * scale)), dom, font=dom_font, fill=EMBER)
    return img


def read_post(path: str) -> tuple[str, str]:
    """Pull (title, pull-quote) out of a Hugo post. TOML or YAML front matter."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.search(r"^title\s*[=:]\s*['\"](.+?)['\"]\s*$", text, re.M)
    title = m.group(1) if m else os.path.basename(path).rsplit(".", 1)[0]
    m = re.search(r"^description\s*[=:]\s*['\"](.+?)['\"]\s*$", text, re.M)
    quote = m.group(1) if m else ""
    return title, quote


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--post", help="Hugo post path; title and quote read from front matter")
    ap.add_argument("--title", help="Card title (overrides --post)")
    ap.add_argument("--quote", default="", help="Optional pull-quote under the title")
    ap.add_argument("--slug", help="Output basename; defaults to the post filename")
    ap.add_argument("--outdir", default=DEFAULT_OUTDIR)
    ap.add_argument("--json", action="store_true", help="Emit the written paths as JSON")
    args = ap.parse_args(argv)

    title, quote, slug = args.title, args.quote, args.slug
    if args.post:
        if not os.path.isfile(args.post):
            print(f"no such post: {args.post}", file=sys.stderr)
            return 2
        p_title, p_quote = read_post(args.post)
        title = title or p_title
        quote = quote or p_quote
        slug = slug or os.path.basename(args.post).rsplit(".", 1)[0]
    if not title:
        print("need --title or --post", file=sys.stderr)
        return 2
    slug = slug or re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60]

    os.makedirs(args.outdir, exist_ok=True)
    written = {}
    for w, h, suffix in SIZES:
        out = os.path.join(args.outdir, f"{slug}-{suffix}.png")
        render(w, h, title, quote).save(out, "PNG")
        written[suffix] = out

    if args.json:
        print(json.dumps(written))
    else:
        for path in written.values():
            print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
