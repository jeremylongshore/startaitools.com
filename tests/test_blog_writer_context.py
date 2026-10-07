"""E01-T05 (startaitools-9a8.1.4): the versioned slim writer context, in observation mode.

The writer brief is one versioned file rendered from a fixed slot object; the run records
which version it used; the contract reports a missing or inconsistent record as an
advisory line until WRITER_CONTEXT_ENFORCE_FROM and refuses it from that date.
"""

import hashlib
import importlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
from test_blog_producer_contract import DATE, RUN, contract, produced  # noqa: F401

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts/blog"
writer = importlib.import_module("blogpipe.writer")
brief_mod = importlib.import_module("blogpipe.brief")

FINDING = {
    "sentence": "A cron job that reads a mutable checkout runs whatever branch is checked out.",
    "reader": "an operator who schedules jobs from a git clone",
    "problem": "the nightly job ran an unmerged branch",
    "outcome": "point scheduled jobs at a deployed copy of the default branch",
    "source_evidence": ["commit abc123: run the monthly job from a temporary worktree"],
    "destination": None,
    "destination_reason": "no public repository for this script",
}
SLOTS = {
    "tier": 1,
    "slug": "cron-reads-a-mutable-checkout",
    "date": DATE,
    "time": "10:00:00",
    "title": "Your cron job runs whatever branch is checked out",
    "description": "A scheduled job that reads a git clone runs the checked-out branch.",
    "tags": ["automation", "git"],
    "category": "Development Journey",
    "finding": FINDING,
    "sources": [{"ref": "commit abc123", "excerpt": "run the monthly job from a worktree"}],
    "models_used": "Claude Opus 4.8",
    "collaboration": "",
    "related_posts": [{"slug": "older-post", "summary": "an older note"}],
    "rhetorical_structure": "problem-solution",
}
# Lander/workspace rule for run-scoped staging names (blog-run-workspace.py).
STAGE_NAME = re.compile(r"[A-Za-z0-9_-]+\.json")


@pytest.fixture(autouse=True)
def no_override(monkeypatch):
    for env in ("BLOG_WRITER_CONTEXT_ENFORCE_FROM", "BLOG_BRIEF_ENFORCE_FROM",
                "BLOG_RECORD_SCHEMA_ENFORCE_FROM"):
        monkeypatch.delenv(env, raising=False)


# ---- the versioned file ------------------------------------------------------------


def test_every_released_version_is_pinned_to_its_bytes():
    """A released context never changes in place: an edit needs a new file and version."""
    for version, (name, sha) in writer.VERSIONS.items():
        data = (writer.CONTEXT_DIR / name).read_bytes()
        assert hashlib.sha256(data).hexdigest() == sha, f"{version} changed; add a new version"
    assert writer.CURRENT_VERSION in writer.VERSIONS


def test_manifest_names_version_path_hash_and_size():
    m = writer.manifest()
    assert m["version"] == "writer-context/v1"
    assert m["template"] == "scripts/blog/writer-context/writer-context-v1.md"
    assert (ROOT / m["template"]).stat().st_size == m["template_bytes"]


# ---- rendering ---------------------------------------------------------------------


@pytest.mark.parametrize("tier", [1, 2, 3])
def test_render_fills_every_slot_and_keeps_only_its_tier_block(tier):
    brief, stats = writer.render({**SLOTS, "tier": tier}, "/ws")
    assert "{{" not in brief and "<!--" not in brief
    assert f"Tier {tier} structure:" in brief
    assert sum(f"Tier {n} structure:" in brief for n in (1, 2, 3)) == 1
    assert FINDING["sentence"] in brief and "run the monthly job from a worktree" in brief
    assert "/ws/content/posts/cron-reads-a-mutable-checkout.md" in brief
    assert "tldr = " in brief  # the mandatory field the legacy template omitted
    assert stats == {"sources": 1, "truncated": 0}


def test_render_is_deterministic():
    assert writer.render(SLOTS, "/ws") == writer.render(json.loads(json.dumps(SLOTS)), "/ws")


@pytest.mark.parametrize(
    "change, message",
    [
        ({"claude_md_excerpts": "200 lines"}, "unknown slot"),
        ({"git_log": "everything"}, "unknown slot"),
        ({"tier": 4}, "tier must be"),
        ({"sources": []}, "sources must be"),
        ({"sources": [{"ref": "x"}]}, "exactly {ref, excerpt}"),
        ({"finding": {}}, "finding must be"),
        ({"date": "10/05/2026"}, "date must be"),
    ],
)
def test_render_refuses_slots_that_would_grow_or_break_the_context(change, message):
    with pytest.raises(writer.SlotError, match=message):
        writer.render({**SLOTS, **change}, "/ws")


def test_missing_required_slot_is_refused():
    slots = dict(SLOTS)
    slots.pop("title")
    with pytest.raises(writer.SlotError, match="missing slot"):
        writer.render(slots, "/ws")


def test_oversized_inputs_are_clipped_and_counted():
    many = [{"ref": f"s{i}", "excerpt": "x" * 5000} for i in range(writer.MAX_SOURCES + 2)]
    brief, stats = writer.render({**SLOTS, "sources": many}, "/ws")
    assert stats["sources"] == writer.MAX_SOURCES
    assert stats["truncated"] == writer.MAX_SOURCES + 2
    assert brief.count("[truncated]") == writer.MAX_SOURCES


def run_cli(*args, cwd=SCRIPTS):
    env = {k: v for k, v in os.environ.items() if not k.startswith("BLOG_")}
    return subprocess.run(
        [sys.executable, "-B", "-m", "blogpipe", "writer-context", *args],
        cwd=cwd, capture_output=True, text=True, env=env, timeout=60,
    )


def test_cli_render_writes_the_run_record_and_prints_the_brief(tmp_path):
    slots = tmp_path / "slots.json"
    slots.write_text(json.dumps(SLOTS))
    result = run_cli("render", "--slots", str(slots), "--run-id", RUN, "--repo", str(tmp_path))
    assert result.returncode == 0, result.stderr
    out = tmp_path / ".blog-staging" / f"{DATE}.{RUN}.writer-context.json"
    record = json.loads(out.read_text())
    assert STAGE_NAME.fullmatch(out.name[len(f"{DATE}.{RUN}."):])
    assert sorted(p.name for p in out.parent.iterdir()) == [out.name]  # no temp leftovers
    assert record["brief"] == result.stdout
    assert record["audit"] == {
        "version": "writer-context/v1",
        "template_sha256": writer.VERSIONS["writer-context/v1"][1],
        "brief_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
        "brief_bytes": len(result.stdout.encode()),
    }
    assert "WRITER-CONTEXT: {" in result.stderr


def test_cli_refusal_exits_2_and_writes_nothing(tmp_path):
    slots = tmp_path / "slots.json"
    slots.write_text(json.dumps({**SLOTS, "git_log": "x"}))
    result = run_cli("render", "--slots", str(slots), "--run-id", RUN, "--repo", str(tmp_path))
    assert result.returncode == 2 and "WRITER-CONTEXT: REFUSED: unknown slot" in result.stderr
    assert not (tmp_path / ".blog-staging").exists()


def test_cli_manifest():
    result = run_cli("manifest")
    assert result.returncode == 0
    assert json.loads(result.stdout) == writer.manifest()


# ---- contract: observation, then enforcement ----------------------------------------


def stage_context(repo, audit_change=None):
    """Render for the fixture run and copy the audit object into the run's audit row."""
    brief, stats = writer.render(SLOTS, str(repo))
    record = writer.build_record(brief, stats, DATE, RUN, SLOTS["slug"], 1)
    writer.staged_path(repo, DATE, RUN).write_text(json.dumps(record))
    path = repo / contract.DECISIONS
    rows = contract.records(path)
    rows[-1]["agent_audit"]["writer_context"] = dict(record["audit"])
    (audit_change or (lambda ctx: None))(rows[-1]["agent_audit"]["writer_context"])
    path.write_text("".join(json.dumps(row) + "\n" for row in rows))


def lines(stderr, marker):
    found = [line for line in stderr.splitlines() if marker in line]
    assert found, stderr
    return found[-1]


@pytest.fixture
def enforce(monkeypatch):
    monkeypatch.setattr(writer, "WRITER_CONTEXT_ENFORCE_FROM", DATE)


def test_observation_reports_a_missing_record_and_never_refuses(produced, capsys):  # noqa: F811
    repo, _, _, transcript = produced
    assert contract.validate(repo, DATE, RUN, transcript)["outcome"] == "complete"
    err = capsys.readouterr().err
    assert lines(err, "ADVISORY: writer context").endswith(
        "(observation until 2026-10-21): missing agent_audit.writer_context"
    )
    assert lines(err, "WRITER-CONTEXT:").endswith("version=none brief_bytes=unknown")


def test_a_recorded_context_is_complete_and_names_its_version(produced, enforce, capsys):  # noqa: F811
    repo, _, _, transcript = produced
    stage_context(repo)
    assert contract.validate(repo, DATE, RUN, transcript)["outcome"] == "complete"
    err = capsys.readouterr().err
    assert lines(err, "ADVISORY: writer context").endswith("(enforced): complete")
    size = len(writer.render(SLOTS, str(repo))[0].encode())
    assert f"version=writer-context/v1 brief_bytes={size}" in lines(err, "WRITER-CONTEXT:")


BREAK = {
    "version": lambda c: c.update(version="legacy"),
    "template_sha256": lambda c: c.update(template_sha256="0" * 64),
    "does not match the staged brief": lambda c: c.update(brief_bytes=1),
}


@pytest.mark.parametrize("gap", sorted(BREAK))
def test_inconsistent_records_are_advisory_before_and_refused_after(
    produced, monkeypatch, capsys, gap  # noqa: F811
):
    repo, _, _, transcript = produced
    stage_context(repo, BREAK[gap])
    assert contract.validate(repo, DATE, RUN, transcript)["outcome"] == "complete"
    assert gap in lines(capsys.readouterr().err, "ADVISORY: writer context")
    monkeypatch.setattr(writer, "WRITER_CONTEXT_ENFORCE_FROM", DATE)
    with pytest.raises(contract.ContractError, match="writer context incomplete: .*" + gap):
        contract.validate(repo, DATE, RUN, transcript)


def test_missing_staged_record_is_named(produced, capsys):  # noqa: F811
    repo, _, _, transcript = produced
    stage_context(repo)
    writer.staged_path(repo, DATE, RUN).unlink()
    contract.validate(repo, DATE, RUN, transcript)
    assert f"staged {DATE}.{RUN}.writer-context.json" in lines(
        capsys.readouterr().err, "ADVISORY: writer context"
    )


def test_env_lever_moves_or_disables_the_switch(produced, enforce, monkeypatch, capsys):  # noqa: F811
    repo, _, _, transcript = produced
    monkeypatch.setenv("BLOG_WRITER_CONTEXT_ENFORCE_FROM", "off")
    contract.validate(repo, DATE, RUN, transcript)
    assert "enforcement off via BLOG_WRITER_CONTEXT_ENFORCE_FROM" in lines(
        capsys.readouterr().err, "ADVISORY: writer context"
    )
    monkeypatch.setenv("BLOG_WRITER_CONTEXT_ENFORCE_FROM", "soon")
    with pytest.raises(contract.ContractError, match="BLOG_WRITER_CONTEXT_ENFORCE_FROM"):
        contract.validate(repo, DATE, RUN, transcript)


def test_the_proposed_switch_date_and_shared_mechanism():
    assert writer.WRITER_CONTEXT_ENFORCE_FROM == "2026-10-21"
    assert writer.enforced("2026-10-20") is False and writer.enforced("2026-10-21") is True
    assert type(writer.SWITCH) is type(brief_mod.SWITCH)
    assert writer.WRITER_CONTEXT_ENFORCE_FROM > brief_mod.AMENDED_CONTRACT_ENFORCE_FROM


def test_contract_readiness_counts_down_the_writer_switch(tmp_path):
    for day in ("2026-10-16", "2026-10-17"):
        (tmp_path / f"run-{day}.log").write_text(
            "PRODUCER-CONTRACT: ADVISORY: writer context (observation): complete\n"
        )
    env = {k: v for k, v in os.environ.items() if not k.startswith("BLOG_")}
    result = subprocess.run(
        [sys.executable, "-B", "-m", "blogpipe", "contract-readiness", "--log-dir",
         str(tmp_path), "--date", "2026-10-18"],
        cwd=SCRIPTS, capture_output=True, text=True, env=env, timeout=60,
    )
    parts = result.stdout.strip().split(" | ")
    (mine,) = [p for p in parts if p.startswith(("writer context", "URGENT: writer context"))]
    assert mine.startswith("writer context enforcement in 3 day(s) (run date 2026-10-21)")
    assert "consecutive complete 2/7" in mine


def test_wrapper_lifts_the_writer_lines_and_routes_its_urgent_notice():
    text = (SCRIPTS / "blog-backfill-daily.sh").read_text()
    assert "URGENT: (brief|record schema|writer context) " in text
    assert "grep -o 'ADVISORY: writer context .*'" in text
    assert "Writer context: ${WRITER_CONTEXT:-" in text
    assert "blogpipe writer-context manifest" in text
