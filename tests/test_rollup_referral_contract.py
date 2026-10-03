"""The weekly rollup's model narrates deterministic referral numbers; it never makes them.

Intent-os audit 226g section 9 reproduced the 2026-09-21 rollup: the model chose its own
UTM query, reported 10 LinkedIn arrivals of which about 3 were human, misstated the prior
week, and printed Substack/Medium zeros for links that carry no tags. The numbers now come
from weekly_metrics.py (web-analytics skill); these tests pin the prompt to that contract.
"""

import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "scripts/blog/blog-team-rollup.sh"


def prompt_text():
    text = WRAPPER.read_text()
    start = text.index('PROMPT="')
    end = text.index('Write ONLY to ${OUTPUT_HTML}."', start)
    return text[start:end]


def test_model_is_not_asked_to_query_or_compute_utm():
    prompt = prompt_text()
    assert "UTM report" not in prompt
    assert "utm_source filtering" not in prompt
    assert "When querying UTM" not in prompt
    assert "Do not query Umami for traffic, UTM or referral numbers" in prompt


def test_zero_rules_are_explicit_for_unmeasurable_and_failed_surfaces():
    prompt = prompt_text()
    assert "sites[].referrals" in prompt
    assert "'untagged — unmeasurable'" in prompt
    assert "never print a 0 for it" in prompt
    assert "'unavailable' means the query failed" in prompt
    assert not re.search(r"If a source shows zero, say so plainly", prompt)


def test_posting_is_never_assumed_only_reported_unverified():
    prompt = prompt_text()
    assert "ASSUME" not in prompt
    assert "report such rows only as unverified" in prompt
    assert "Zero arrivals are not evidence that nobody posted" in prompt


def test_filtered_tier_is_the_headline_and_never_the_total_audience():
    prompt = prompt_text()
    assert "The headline numbers are the FILTERED tier; raw is context." in prompt
    assert "Never call a filtered figure the total audience" in prompt


def test_offline_dry_run_still_produces_a_report_without_mail(tmp_path):
    harness = ROOT / "scripts/blog/test-weekly-rollup-auth.sh"
    env = {k: v for k, v in os.environ.items() if not k.startswith(("ANTHROPIC_", "MINIMAX_"))}
    result = subprocess.run(["bash", str(harness), str(WRAPPER), "success"], capture_output=True,
                            text=True, timeout=120, env=env)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "no mail sent" in result.stdout
