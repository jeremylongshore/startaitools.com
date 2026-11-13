"""The cross-post body stripper (bead startaitools-7l2): JSON-LD and any other <script> block
is removed before a body reaches Dev.to or Hashnode, which escape script tags into visible
text; prose, code fences and inline HTML that is not a script survive byte-for-byte."""

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".claude/skills/blog-backfill/scripts/strip-script-blocks.py"
spec = importlib.util.spec_from_file_location("strip_script_blocks", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

JSONLD = (
    '<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n'
    '  "@type": "FAQPage",\n  "mainEntity": [{"@type": "Question", "name": "Why?"}]\n}\n</script>\n'
)


def test_jsonld_block_is_removed_and_prose_untouched():
    body = "Intro paragraph.\n\n## Heading\n\nSome text.\n\n" + JSONLD + "\nTrailing note.\n"
    cleaned, count = mod.strip_script_blocks(body)
    assert count == 1
    assert "<script" not in cleaned and "@context" not in cleaned
    assert cleaned.startswith("Intro paragraph.\n\n## Heading\n\nSome text.\n")
    assert cleaned.rstrip().endswith("Trailing note.")
    assert "\n\n\n" not in cleaned


def test_multiple_blocks_and_case_insensitive_tags():
    body = "a\n<SCRIPT>alert(1)</SCRIPT>\nb\n" + JSONLD + "c\n"
    cleaned, count = mod.strip_script_blocks(body)
    assert count == 2
    assert cleaned == "a\nb\nc\n"


def test_code_fence_mentioning_script_in_prose_is_not_a_block():
    body = "Use `<script>` tags sparingly.\n\n```html\n<div>not a script tag</div>\n```\n"
    cleaned, count = mod.strip_script_blocks(body)
    assert count == 0
    assert cleaned == body


def test_cli_passes_body_through_stdin_and_reports_count():
    body = "x\n" + JSONLD
    proc = subprocess.run([sys.executable, str(SCRIPT)], input=body, capture_output=True, text=True)
    assert proc.returncode == 0
    assert proc.stdout == "x\n"
    assert "removed 1 block(s)" in proc.stderr


def test_posters_strip_before_sending():
    """Both cross-post scripts must pipe the body through the stripper (the defect was that
    they sent the markdown verbatim)."""
    for name in ("post-to-devto.sh", "post-to-hashnode.sh"):
        text = (ROOT / ".claude/skills/blog-backfill/scripts" / name).read_text()
        assert "strip-script-blocks.py" in text, name
        body_line = next(line for line in text.splitlines() if line.startswith("body=$("))
        assert "strip-script-blocks.py" in body_line, (name, body_line)
