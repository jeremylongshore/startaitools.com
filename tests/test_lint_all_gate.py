"""lint-all.sh must take each check's own exit status, never a pipeline's last stage.

Its pytest step was `if python3 -m pytest ... | tail -1`, so the gate reported "tests pass"
when the suite failed and when pytest was not installed at all.
"""

import re
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/blog/lint-all.sh"


def code_lines():
    return [ln for ln in SCRIPT.read_text().splitlines() if not ln.lstrip().startswith("#")]


def test_no_check_is_judged_through_a_pipe():
    piped = [ln for ln in code_lines() if re.match(r"\s*(if|elif)\b.*\|\s*(tail|head|tee)\b", ln)]
    assert piped == [], piped


def test_pytest_status_is_captured_and_absence_is_a_failure():
    text = "\n".join(code_lines())
    assert "PYTEST_RC=$?" in text
    assert 'missing_tool pytest' in text
