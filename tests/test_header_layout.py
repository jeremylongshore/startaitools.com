"""The header and card grids never push the page wider than the screen (startaitools-saj).

Measured 2026-11-02 on the live site: the header row (tagline, six links, CTA,
labelled search, toggle) needs about 1300px inside a 1200px wrapper, so the page
scrolled sideways at every width from 761px to 1366px (by up to 544px), and fixed
minimum grid columns overflowed 320-351px phones. These checks pin the breakpoints
and grid rules that a headless-Chrome sweep from 320px to 1600px verified.
"""

import re
from pathlib import Path

CSS = (Path(__file__).resolve().parents[1] / "assets/css/custom.css").read_text()


def media_block(query):
    start = CSS.index(f"@media ({query}) {{")
    depth, i = 0, CSS.index("{", start)
    while True:
        depth += {"{": 1, "}": -1}.get(CSS[i], 0)
        if depth == 0:
            return CSS[start:i + 1]
        i += 1


def test_links_collapse_into_the_menu_below_the_width_where_they_fit():
    collapse = media_block("max-width: 1199px")
    assert ".nav-links { display: none;" in collapse
    assert ".mobile-menu-btn { display: inline-flex; }" in collapse
    assert "@media (max-width: 760px)" not in CSS and "@media (max-width: 1080px)" not in CSS


def test_desktop_row_drops_the_tagline_and_search_label():
    desktop = media_block("min-width: 1200px")
    assert ".header-brand .brand-tag { display: none; }" in desktop
    assert ".search-trigger span { display: none; }" in desktop
    assert ".search-trigger kbd { display: none; }" in desktop


def test_small_phones_tighten_the_header():
    phone = media_block("max-width: 420px")
    assert ".header-inner { gap: var(--sp-2);" in phone
    assert ".search-trigger { display: none; }" in phone
    assert "#theme-toggle { display: none; }" in media_block("max-width: 360px")


def test_no_grid_column_demands_more_than_the_screen():
    fixed = re.findall(r"minmax\(\d+px,", CSS)
    assert not fixed, fixed
    assert len(re.findall(r"minmax\(min\(100%, \d+px\), 1fr\)", CSS)) >= 5


def test_signup_input_can_shrink_below_its_basis():
    rule = CSS.split('.post-cta .cta-form input[type="email"] {', 1)[1].split("}", 1)[0]
    assert "min-width: 0" in rule and "max-width: 100%" in rule
