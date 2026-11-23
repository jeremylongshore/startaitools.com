"""lint-all.sh must be runnable on the pipeline host and must report pytest's own verdict.

Its pytest step was `python3 -m pytest`. On the host pytest is a uv tool and the system
Python has no pytest module, so the gate failed on every run and the weekly recommendation
worker never opened a pull request.
"""

from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/blog/lint-all.sh"


def code():
    lines = SCRIPT.read_text().splitlines()
    return "\n".join(ln for ln in lines if not ln.lstrip().startswith("#"))


def test_pytest_on_path_is_tried_before_the_module():
    text = code()
    assert "command -v pytest" in text
    assert text.index("command -v pytest") < text.index("python3 -m pytest")


def test_pytest_status_is_captured_and_absence_is_a_failure():
    text = code()
    assert "PYTEST_RC=$?" in text
    assert "missing_tool pytest" in text
