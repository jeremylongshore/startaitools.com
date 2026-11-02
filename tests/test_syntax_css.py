"""Code blocks stay readable in both themes and on phones (startaitools-ogg).

Hugo used to write inline light colours into every code block while custom.css gave
code text the theme foreground, so dark-mode code was near-white on light grey
(measured 1.05:1). These checks pin the class-based highlighting, its theme scoping,
token contrast against the site's code box, and the phone layout rule.
"""

import importlib.util
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / "assets/css/syntax.css").read_text()
GENERATOR = ROOT / "scripts/blog/gen-syntax-css.py"
spec = importlib.util.spec_from_file_location("gen_syntax_css", GENERATOR)
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)

SCOPES = ('[data-theme="dark"]', '[data-theme="light"]', ":root:not([data-theme])")
# sRGB of the code box (tokens.css --bg-inset), as rendered by Chrome on 2026-11-02.
CODE_BOX = {"dark": (4, 4, 6), "light": (251, 252, 252)}


def luminance(rgb):
    def channel(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def hex_rgb(value):
    value = value.lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def rules(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    return re.findall(r"([^{}]+)\{([^}]*)\}", css)


def test_highlighting_emits_classes_not_inline_colours():
    config = (ROOT / "config/_default/config.toml").read_text()
    block = config.split("[markup.highlight]", 1)[1].split("[", 1)[0]
    assert re.search(r"^\s*noClasses\s*=\s*false\s*$", block, re.M)


def test_head_loads_the_syntax_stylesheet():
    header = (ROOT / "layouts/partials/header.html").read_text()
    assert 'resources.Get "css/syntax.css"' in header


def test_every_rule_is_scoped_to_a_theme_and_carries_no_chroma_background():
    found = set()
    for selectors, body in rules(CSS):
        for selector in selectors.split(","):
            selector = selector.strip()
            if selector.startswith("@media"):
                continue
            scope = next((s for s in SCOPES if selector.startswith(s)), None)
            assert scope, f"unscoped selector: {selector}"
            found.add(scope)
        if re.search(r"\.chroma\s*$", selectors.split(",")[0].strip()):
            assert "background-color" not in body
    assert found == set(SCOPES)
    assert "#f0f0f0" not in CSS and ".bg " not in CSS


def _token_colours(theme):
    marker = {"dark": "/* Dark", "light": "/* Light */"}[theme]
    section = CSS.split(marker, 1)[1].split("\n\n", 1)[0]
    for selectors, body in rules(section):
        if re.search(r"\.(w|line|cl|lnlinks|lntd|lntable|hl|lnt|ln)\b", selectors):
            continue  # whitespace, layout and line-number rules are not code text
        colour = re.search(r"(?<!background-)color:(#[0-9a-fA-F]{3,6})", body)
        own_bg = re.search(r"background-color:(#[0-9a-fA-F]{3,6})", body)
        if colour:
            # A token with its own background (the error token) is read against it.
            bg = hex_rgb(own_bg.group(1)) if own_bg else CODE_BOX[theme]
            yield selectors.split(",")[0].strip(), hex_rgb(colour.group(1)), bg


@pytest.mark.parametrize("theme", ["dark", "light"])
def test_every_code_token_meets_4_5_to_1_on_the_code_box(theme):
    colours = list(_token_colours(theme))
    assert len(colours) > 30
    weak = [(sel, round(contrast(rgb, bg), 2)) for sel, rgb, bg in colours
            if contrast(rgb, bg) < 4.5]
    assert not weak, weak


def test_generator_drops_backgrounds_and_prefixes_each_scope():
    sample = (
        "/* Background */ .bg { color:#111;background-color:#f0f0f0; }\n"
        "/* PreWrapper */ .chroma { color:#111;background-color:#f0f0f0; }\n"
        "/* Keyword */ .chroma .k { color:#007020;font-weight:bold }\n"
    )
    out = gen.scoped(sample, ['[data-theme="dark"]', ":root:not([data-theme])"])
    assert out == [
        '[data-theme="dark"] .chroma, :root:not([data-theme]) .chroma { color:#111; }',
        '[data-theme="dark"] .chroma .k, :root:not([data-theme]) .chroma .k '
        "{ color:#007020;font-weight:bold }",
    ]


@pytest.mark.skipif(shutil.which("hugo") is None, reason="hugo binary not installed")
def test_committed_stylesheet_matches_the_generator():
    result = subprocess.run(
        ["python3", str(GENERATOR), "--check"],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr


def test_phone_code_blocks_use_the_full_width_and_never_wrap():
    custom = (ROOT / "assets/css/custom.css").read_text()
    phone = custom.split("/* Phones: code uses the full screen width", 1)[1].split("\n}\n", 1)[0]
    assert "width: 100vw" in phone and "margin-left: calc(50% - 50vw)" in phone
    assert "font-size: 0.8rem" in phone
    assert "white-space" not in phone  # lines scroll; wrapping would break indentation
