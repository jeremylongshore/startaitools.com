"""One authority per concern: prose in the repository guide must match the code.

Guards for 000-docs/014-AT-ADEC-blog-pipeline-authority-map.md sections 4.5 (front-matter
offset) and 4.6 (tier-creep thresholds). Each test names the code that decides.
"""

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude/skills/blog-backfill/scripts"
GUIDE = ROOT / "CLAUDE.md"
ENFORCED, ADVISORY = "2099-01-01", "2000-01-01"


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lint = load("lint-post-voice")


def post(date_line):
    return f"+++\ntitle = 'A Title'\nslug = 'a-title'\n{date_line}\ndraft = false\n+++\n\nBody.\n"


# --- 4.5: one front-matter offset ----------------------------------------------------


def test_host_offset_constant_matches_the_host_clock_comment_in_lib_cron_common():
    lib = (ROOT / "scripts/blog/lib-cron-common.sh").read_text()
    assert "fixed -06:00 zone" in lib
    assert lint.HOST_OFFSET == "-06:00"


def test_host_offset_passes_and_date_only_is_left_to_the_contract():
    for line in ("date = 2026-10-05T08:00:00-06:00", "date = '2026-10-05T08:00:00-06:00'",
                 "date = 2026-10-05"):
        assert lint.lint_date_offset(post(line), "p.md", ENFORCED) == ([], [])


def test_other_offset_warns_before_the_switch_and_fails_after():
    text = post("date = 2026-10-05T08:00:00-05:00")
    hard, warns = lint.lint_date_offset(text, "p.md", ADVISORY)
    assert hard == [] and len(warns) == 1 and "-05:00" in warns[0]
    assert f"advisory until {lint.DATE_OFFSET_RULE_ENFORCE_FROM}" in warns[0]
    hard, warns = lint.lint_date_offset(text, "p.md", ENFORCED)
    assert warns == [] and len(hard) == 1 and "new posts use -06:00" in hard[0]


def test_utc_and_missing_offsets_are_also_flagged():
    for line in ("date = 2026-10-05T08:00:00Z", "date = 2026-10-05T08:00:00"):
        assert lint.lint_date_offset(post(line), "p.md", ENFORCED)[0]


def test_yaml_front_matter_is_checked_too():
    text = "---\ntitle: A\ndate: 2026-10-05T08:00:00-05:00\n---\n\nBody.\n"
    assert lint.lint_date_offset(text, "p.md", ENFORCED)[0]


def test_article_lint_reports_the_offset(tmp_path, capsys):
    path = tmp_path / "content/posts/a-title.md"
    path.parent.mkdir(parents=True)
    path.write_text(post("date = 2026-10-05T08:00:00-05:00"))
    issues = lint.lint_file(path)
    reported = issues + [capsys.readouterr().err]
    assert any("front-matter date uses -05:00" in item for item in reported)


def test_repository_guide_states_one_offset():
    guide = GUIDE.read_text()
    stamps = re.findall(r"^date = \S+T[0-9:]+([+-]\d\d:\d\d)", guide, re.M)
    assert stamps and set(stamps) == {"-06:00"}
    assert "may use `-05:00`" not in guide
    assert "New posts use the `-06:00` offset" in guide


# --- 4.6: tier-creep thresholds printed as the code has them ------------------------


def test_guide_and_guard_print_the_real_alert_thresholds():
    guard = load("tier-creep-guard")
    summary = guard.alert_summary(guard.BANDS)
    assert summary == "T2 > 40, T1 < 52, T3 > 12, T1 > 85"
    row = next(line for line in GUIDE.read_text().splitlines()
               if "blog-tier-creep-guard.sh" in line and line.startswith("|"))
    assert f"alerts at {summary}" in row
    assert "against tolerance bands (T1 60-70" not in row
    assert summary in " ".join((guard.__doc__ or "").split())
