"""Versioned host state: the blog cron manifest and the gate reviewer agents.

Authority map 000-docs/014 sections 2, 3 and 4.1. Hermetic: the drift check reads
fixture crontabs and a temp deployed-agents dir, never the live host.
"""

import hashlib
import importlib.util
import re
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
HOST = ROOT / "scripts/blog/host"
SPEC = importlib.util.spec_from_file_location("host_drift", ROOT / "scripts/blog/host-drift-check.py")
drift = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(drift)

DAYS = {"0": "Sunday", "1": "Monday", "2": "Tuesday", "3": "Wednesday",
        "4": "Thursday", "5": "Friday", "6": "Saturday"}


def when(entry):
    """Render a manifest line's schedule the way the CLAUDE.md table writes it."""
    minute, hour, dom, month, dow = entry.split()[:5]
    clock = f"{int(hour):02d}:{int(minute):02d}"
    if dom == "*" and month == "*" and dow == "*":
        return f"{clock} daily"
    if dom == "*" and month == "*":
        return f"{clock} weekly ({DAYS[dow]})"
    if dom == "1" and month == "*" and dow == "*":
        return f"{clock} monthly (1st)"
    raise AssertionError(f"unrendered schedule: {entry}")


def script_of(entry):
    m = re.search(r"/scripts/blog/([\w.-]+\.(?:sh|py))", entry)
    assert m, entry
    return m.group(1)


def guide_rows():
    text = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    section = text.split("## Autonomous Daily Automation", 1)[1].split("\n## ", 1)[0]
    rows = {}
    for line in section.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3:
            m = re.search(r"`scripts/blog/([\w.-]+\.(?:sh|py))", cells[1])
            if m:
                rows.setdefault(m.group(1), []).append(cells[0])
    return rows


def test_every_blog_cron_job_in_the_manifest_is_in_the_guide_at_the_same_time():
    rows = guide_rows()
    for entry in drift.manifest_entries():
        name = script_of(entry)
        assert name in rows, f"CLAUDE.md schedule table omits {name}"
        assert when(entry) in rows[name], (name, when(entry), rows[name])


def test_the_guide_lists_no_blog_job_the_manifest_does_not_schedule():
    scheduled = {script_of(e) for e in drift.manifest_entries()}
    assert set(guide_rows()) <= scheduled, set(guide_rows()) - scheduled


def test_manifest_lines_are_unique_and_all_blog_jobs():
    entries = drift.manifest_entries()
    assert len(entries) == len(set(entries))
    assert all(drift.MARKER in e for e in entries)
    assert {"blog-crosspost-sweep.sh", "native-metrics-devto.py",
            "blog-recommendation-worker.sh"} <= {script_of(e) for e in entries}


def crontab_from(entries, extra=()):
    return "\n".join(["MAILTO=''", "# a comment mentioning /blog/startaitools/scripts/blog/x.sh",
                      "*/15 * * * * /home/u/bin/unrelated.sh", *entries, *extra]) + "\n"


@pytest.fixture
def deployed(tmp_path):
    d = tmp_path / "agents"
    d.mkdir()
    for name in drift.pinned():
        shutil.copy(HOST / "agents" / name, d / name)
    return d


def run(tmp_path, deployed, crontab_text, *extra):
    tab = tmp_path / "crontab"
    tab.write_text(crontab_text)
    return drift.main(["--crontab", str(tab), "--deployed-agents", str(deployed), *extra])


def test_no_drift_when_host_matches(tmp_path, deployed, capsys):
    assert run(tmp_path, deployed, crontab_from(drift.manifest_entries())) == 0
    out = capsys.readouterr().out
    assert "cron: OK" in out and out.count(": OK repo sha256=") == 2


def test_reports_a_missing_and_an_unexpected_cron_line(tmp_path, deployed, capsys):
    entries = drift.manifest_entries()
    moved = entries[0].replace("0 5 * * *", "5 5 * * *", 1)
    rc = run(tmp_path, deployed, crontab_from(entries[1:], [moved]))
    out = capsys.readouterr().out
    assert rc == 1
    assert f"missing on host:    {entries[0]}" in out
    assert f"unexpected on host: {moved}" in out


def test_reports_a_changed_and_a_missing_deployed_agent(tmp_path, deployed, capsys):
    (deployed / "fact-checker.md").write_text("edited outside review\n")
    (deployed / "article-consistency-checker.md").unlink()
    rc = run(tmp_path, deployed, crontab_from(drift.manifest_entries()))
    out = capsys.readouterr().out
    assert rc == 1
    assert "agent fact-checker.md: DRIFT" in out
    assert "agent article-consistency-checker.md: MISSING" in out
    assert "install -m 0644" in out


def test_repo_copies_match_their_recorded_hashes():
    sums = drift.pinned()
    assert set(sums) == {"fact-checker.md", "article-consistency-checker.md"}
    for name, digest in sums.items():
        assert hashlib.sha256((HOST / "agents" / name).read_bytes()).hexdigest() == digest


def test_an_unrecorded_repo_edit_is_an_error_not_a_pass(tmp_path, deployed, capsys):
    agents = tmp_path / "repo-agents"
    shutil.copytree(HOST / "agents", agents)
    (agents / "fact-checker.md").write_text("tampered\n")
    rc = run(tmp_path, deployed, crontab_from(drift.manifest_entries()),
             "--agents-dir", str(agents))
    assert rc == 2
    assert "does not match SHA256SUMS" in capsys.readouterr().err


def test_reviewer_agents_carry_the_names_roles_requires():
    roles = (ROOT / "scripts/blog/blogpipe/roles.py").read_text(encoding="utf-8")
    for name in drift.pinned():
        agent = name.removesuffix(".md")
        assert f'"{agent}"' in roles or f"'{agent}'" in roles, agent
        head = (HOST / "agents" / name).read_text(encoding="utf-8").split("---")[1]
        assert f"name: {agent}" in head
