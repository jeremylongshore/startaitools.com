"""Pilot release gate (startaitools-9a8.2.4): no pilot article lands before RG0-RG2 evidence.

Offline. A fake `bd` serves gate records from a JSON file, so no test reads the
real backlog. The lander block itself is executed with its effects stubbed, to
prove the refusal happens before any commit and that daily posts never consult
the gate beads.
"""

from __future__ import annotations

import importlib.util
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts/blog"
LAND = (SCRIPTS / "blog-land.sh").read_text(encoding="utf-8")
GATE_SCRIPT = SCRIPTS / "pilot_release_gate.py"

spec = importlib.util.spec_from_file_location("pilot_release_gate", GATE_SCRIPT)
gate = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gate  # dataclasses resolve their module by name
spec.loader.exec_module(gate)

EVIDENCED = "Observed clean: evidence matrix row 4, run log https://github.com/o/r/actions/runs/1"
DAILY_POST = '+++\ntitle = "Daily"\ndate = 2026-10-04\ntags = ["ops"]\n+++\nBody\n'
PILOT_POST = '+++\ntitle = "Pilot 1"\npilot = "skill-frontmatter"\n+++\nBody\n'
CANONICAL_POST = (
    '---\ntitle: "Pilot"\ncanonicalURL: "https://tonsofskills.com/blog/pilot-1/"\n---\nBody\n'
)


def fake_bd(tmp_path: Path, records: dict[str, dict] | None, calls: Path) -> Path:
    """A bd stand-in. records=None makes every call fail (and records the call)."""
    store = tmp_path / "gates.json"
    store.write_text(json.dumps(records or {}))
    bd = tmp_path / "bd"
    bd.write_text(
        "#!/usr/bin/env python3\n"
        "import json, sys\n"
        f"open({str(calls)!r}, 'a').write(' '.join(sys.argv[1:]) + '\\n')\n"
        f"data = json.load(open({str(store)!r}))\n"
        f"if {records is None!r} or sys.argv[2] not in data: sys.exit(1)\n"
        "print(json.dumps([dict(id=sys.argv[2], **data[sys.argv[2]])]))\n"
    )
    bd.chmod(0o755)
    return bd


def all_closed(reason: str = EVIDENCED) -> dict[str, dict]:
    return {bid: {"status": "closed", "close_reason": reason} for _, bid in gate.GATES}


def write(tmp_path: Path, text: str) -> Path:
    post = tmp_path / "post.md"
    post.write_text(text)
    return post


@pytest.mark.parametrize(
    ("text", "pilot"),
    [
        (DAILY_POST, False),
        (PILOT_POST, True),
        (CANONICAL_POST, True),
        ('+++\ntitle = "x"\npilot = false\n+++\n', False),
        ('+++\ntitle = "x"\ncanonicalURL = "https://startaitools.com/posts/x/"\n+++\n', False),
        ("no front matter at all\npilot = yes\n", False),
    ],
)
def test_pilot_detection(text, pilot):
    assert (gate.pilot_marker(gate.front_matter(text)) is not None) is pilot


def test_daily_post_is_not_applicable_and_never_calls_bd(tmp_path):
    calls = tmp_path / "calls"
    bd = fake_bd(tmp_path, None, calls)
    verdict = gate.evaluate(write(tmp_path, DAILY_POST), str(bd), str(tmp_path))
    assert verdict.passed and not verdict.applicable
    assert not calls.exists()


def test_pilot_passes_only_when_all_three_gates_closed_with_evidence(tmp_path):
    calls = tmp_path / "calls"
    bd = fake_bd(tmp_path, all_closed(), calls)
    verdict = gate.evaluate(write(tmp_path, PILOT_POST), str(bd), str(tmp_path))
    assert verdict.applicable and verdict.passed, verdict.reasons
    assert calls.read_text().count("--json") == 3


@pytest.mark.parametrize("gate_index", [0, 1, 2])
def test_any_open_gate_refuses(tmp_path, gate_index):
    records = all_closed()
    records[gate.GATES[gate_index][1]] = {"status": "open"}
    bd = fake_bd(tmp_path, records, tmp_path / "calls")
    verdict = gate.evaluate(write(tmp_path, PILOT_POST), str(bd), str(tmp_path))
    assert not verdict.passed
    assert f"{gate.GATES[gate_index][0]} " in " ".join(verdict.reasons)


@pytest.mark.parametrize(
    "reason",
    [
        "",
        "done",
        "Closed because seven days went by without problems.",  # elapsed time, no evidence
        "auto-closed by the staleness sweep, see https://example.com/x",
    ],
)
def test_closed_without_evidence_refuses(tmp_path, reason):
    bd = fake_bd(tmp_path, all_closed(reason), tmp_path / "calls")
    verdict = gate.evaluate(write(tmp_path, PILOT_POST), str(bd), str(tmp_path))
    assert not verdict.passed


@pytest.mark.parametrize(
    "reason",
    [
        "Evidence linked: jeremylongshore/startaitools.com#150 merged.",
        "Seven clean daily cycles observed; matrix at recovery/E04-evidence-matrix.md",
        "Decisions recorded in 228, merged as 7c551f1b with owners named.",
    ],
)
def test_evidence_forms_accepted(reason):
    assert gate.evidence_problem(reason) is None


def test_unreadable_gate_refuses_fail_closed(tmp_path):
    bd = fake_bd(tmp_path, None, tmp_path / "calls")
    verdict = gate.evaluate(write(tmp_path, PILOT_POST), str(bd), str(tmp_path))
    assert not verdict.passed and "unreadable" in " ".join(verdict.reasons)
    missing = gate.evaluate(write(tmp_path, PILOT_POST), str(tmp_path / "nope"), str(tmp_path))
    assert not missing.passed


def test_cli_exit_codes(tmp_path, capsys):
    bd = fake_bd(tmp_path, all_closed(), tmp_path / "calls")
    post = write(tmp_path, PILOT_POST)
    assert gate.main(["check", "--post", str(post), "--bd", str(bd),
                      "--beads-dir", str(tmp_path)]) == 0
    assert "PILOT-GATE: PASS" in capsys.readouterr().out
    bd = fake_bd(tmp_path, {}, tmp_path / "calls")
    assert gate.main(["check", "--post", str(post), "--bd", str(bd),
                      "--beads-dir", str(tmp_path)]) == gate.EXIT_REFUSED
    assert "PILOT-GATE: REFUSED" in capsys.readouterr().out


# ---- The lander block itself ------------------------------------------------

BLOCK = LAND[LAND.index("# ---- Pilot release gate") : LAND.index("# ---- Precondition gate")]


def run_block(tmp_path, post_text, records, dry_run=0):
    post = write(tmp_path, post_text)
    calls = tmp_path / "calls"
    bd = fake_bd(tmp_path, records, calls)
    block = BLOCK.replace('"$(dirname "${BASH_SOURCE[0]}")/pilot_release_gate.py"',
                          shlex.quote(str(GATE_SCRIPT)))
    source = f"""
set -uo pipefail
POST={shlex.quote(str(post))}; SLUG=post; TARGET_DATE=2026-10-05; DRY_RUN={dry_run}
log() {{ echo "LOG $*"; }}
urgent_alert() {{ echo "ALERT $1"; }}
{block}
echo "REACHED-PRECONDITIONS"
"""
    proc = subprocess.run(
        ["/bin/bash", "-c", source],
        cwd=tmp_path,
        env={**os.environ, "PILOT_GATE_BD_BIN": str(bd), "PILOT_GATE_BEADS_DIR": str(tmp_path)},
        capture_output=True,
        text=True,
        timeout=30,
    )
    return proc, calls


def test_lander_blocks_a_pilot_before_any_commit_and_alerts(tmp_path):
    proc, _ = run_block(tmp_path, PILOT_POST, {})
    assert proc.returncode == 12
    assert "LAND-RESULT: BLOCKED (pilot release gate" in proc.stdout
    assert "ALERT" in proc.stdout and "REACHED-PRECONDITIONS" not in proc.stdout


def test_lander_dry_run_refuses_without_alert(tmp_path):
    proc, _ = run_block(tmp_path, PILOT_POST, {}, dry_run=1)
    assert proc.returncode == 12 and "ALERT" not in proc.stdout


def test_lander_daily_post_continues_without_consulting_gates(tmp_path):
    proc, calls = run_block(tmp_path, DAILY_POST, None)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PILOT-GATE: NOT-APPLICABLE" in proc.stdout
    assert "REACHED-PRECONDITIONS" in proc.stdout and not calls.exists()


def test_lander_pilot_with_evidence_continues(tmp_path):
    proc, _ = run_block(tmp_path, PILOT_POST, all_closed())
    assert proc.returncode == 0 and "PILOT-GATE: PASS" in proc.stdout


def test_gate_runs_before_every_mutation_and_the_dry_run_exit():
    at = LAND.index("# ---- Pilot release gate")
    for later in ("# ---- Land: commit + push", "# ---- Dual-publish to tonsofskills",
                  'log "LAND-RESULT: OK (dry-run)"', "# ---- Precondition gate"):
        assert at < LAND.index(later), later
