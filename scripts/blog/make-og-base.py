#!/usr/bin/env python3
"""Bake the startaitools OG base card (charcoal + ember, Intent Solutions brand).

Everything except the per-post title is baked here: background, ember rules,
the "startaitools . with Intent Solutions" wordmark, and the domain. Hugo's
images.Text overlays only the post title (and category . read-time) at build
time onto the empty center band (y ~ 200-440). Run once; commit the output.

Output: assets/images/og-base.png (1200x630).
"""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONTS = os.path.join(ROOT, "assets", "fonts")
OUT = os.path.join(ROOT, "assets", "images", "og-base.png")

W, H = 1200, 630
CHARCOAL = (24, 24, 27)      # #18181B zinc-900
CHARCOAL_DK = (14, 14, 16)   # bottom of gradient
EMBER = (249, 115, 22)       # #F97316 orange-500
WHITE = (250, 250, 250)      # zinc-50
MUTED = (161, 161, 170)      # zinc-400


def load(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f


def main():
    img = Image.new("RGB", (W, H), CHARCOAL)
    px = img.load()
    # subtle vertical gradient for depth
    for y in range(H):
        t = y / H
        r = int(CHARCOAL[0] + (CHARCOAL_DK[0] - CHARCOAL[0]) * t)
        g = int(CHARCOAL[1] + (CHARCOAL_DK[1] - CHARCOAL[1]) * t)
        b = int(CHARCOAL[2] + (CHARCOAL_DK[2] - CHARCOAL[2]) * t)
        for x in range(W):
            px[x, y] = (r, g, b)

    d = ImageDraw.Draw(img)
    # ember rules top + bottom
    d.rectangle([0, 0, W, 8], fill=EMBER)
    d.rectangle([0, H - 8, W, H], fill=EMBER)

    syne = load(os.path.join(FONTS, "Syne-var.ttf"), 40, 700)
    inter = load(os.path.join(FONTS, "Inter-var.ttf"), 34, 400)
    inter_dom = load(os.path.join(FONTS, "Inter-var.ttf"), 26, 500)

    # top-left wordmark: [ember dot] startaitools . with Intent Solutions
    x, y = 70, 54
    dot_r = 9
    cy = y + 26
    d.ellipse([x, cy - dot_r, x + 2 * dot_r, cy + dot_r], fill=EMBER)
    x += 2 * dot_r + 18
    d.text((x, y), "startaitools", font=syne, fill=WHITE)
    wm_w = d.textlength("startaitools", font=syne)
    x += wm_w + 16
    d.text((x, y + 6), "· with Intent Solutions", font=inter, fill=MUTED)

    # bottom-right domain
    dom = "startaitools.com"
    dom_w = d.textlength(dom, font=inter_dom)
    d.text((W - 70 - dom_w, H - 60), dom, font=inter_dom, fill=EMBER)

    img.save(OUT, "PNG")
    print("wrote", OUT, img.size)

    # Default card (home / sections / fallback): base + centered tagline.
    default = img.copy()
    dd = ImageDraw.Draw(default)
    tag_a = load(os.path.join(FONTS, "Syne-var.ttf"), 66, 700)
    tag_b = load(os.path.join(FONTS, "Inter-var.ttf"), 32, 400)
    line1 = "AI systems, shipped"
    line2 = "in production."
    sub = "Field notes, deep-dives, and case studies."
    dd.text((72, 250), line1, font=tag_a, fill=WHITE)
    dd.text((72, 328), line2, font=tag_a, fill=EMBER)
    dd.text((74, 420), sub, font=tag_b, fill=MUTED)
    outdir = os.path.join(ROOT, "static", "images")
    os.makedirs(outdir, exist_ok=True)
    dpath = os.path.join(outdir, "og-default.png")
    default.save(dpath, "PNG")
    print("wrote", dpath, default.size)


if __name__ == "__main__":
    main()
