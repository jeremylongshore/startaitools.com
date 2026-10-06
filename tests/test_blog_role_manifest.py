"""One per-tier gate table, pinned to the code (startaitools-9a8.1.6, authority map 014 §4.2).

`blogpipe.roles.role_manifest()` states who must run and who must leave a PASS receipt at
each tier, derived by calling the contract's own `required_agents` and `gate_agents`. The
skills repository renders the single "Mandatory roles" table in blog-backfill/SKILL.md from
a committed copy of these bytes and pins the same digest. This file guards the repository
side: the digest, the CLI, and that no per-tier reviewer list reappears in this repo's prose.
"""

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts/blog"
sys.path.insert(0, str(SCRIPTS))

from blogpipe import brief, roles  # noqa: E402

# sha256 of roles.role_manifest(). When a mandatory role changes on purpose: regenerate the
# skill copy with `python3 -B -m blogpipe required-roles > references/required-roles.json`,
# update the SKILL.md "Mandatory roles" table from it, move the pin in BOTH repositories
# (tests/test_contract_instructions.py ROLE_MANIFEST_SHA256 there), and land the skill first.
ROLE_MANIFEST_SHA256 = "e388dbba1acc0df4e505743159504f86ffeaad5f9eba64c787230f3406c1e8be"

# Prose in this repository that once carried its own per-tier gate list.
PROSE = ("CLAUDE.md", "AGENTS.md", "README.md")
RETIRED = ROOT / ".claude/skills/blog-backfill/methodology/publishing-gates.md"


def reviewer_roles() -> set[str]:
    """Every role the manifest names except the writers (writer choice is not a gate list)."""
    manifest = json.loads(roles.role_manifest())
    names = set()
    for tier in manifest["tiers"].values():
        for group in ("run", "pass_receipt"):
            for members in tier[group].values():
                names.update(members)
    return names


def test_role_manifest_matches_the_digest_the_skill_pins():
    digest = hashlib.sha256(roles.role_manifest().encode()).hexdigest()
    assert digest == ROLE_MANIFEST_SHA256, (
        "a mandatory role in blogpipe/roles.py changed: re-sync blog-backfill/references/"
        "required-roles.json and the SKILL.md Mandatory roles table in the skills "
        "repository, then move ROLE_MANIFEST_SHA256 here and in that repository's test"
    )


def test_manifest_is_derived_from_the_enforcing_functions():
    manifest = json.loads(roles.role_manifest())
    assert manifest["tier1_switch"] == brief.AMENDED_CONTRACT_ENFORCE_FROM
    t1, t2, t3 = (manifest["tiers"][t] for t in ("1", "2", "3"))
    assert t1["run"]["from_switch"] == [brief.T1_CONSISTENCY_AGENT]
    assert t1["pass_receipt"]["from_switch"] == [brief.T1_CONSISTENCY_AGENT]
    assert "seo-content-auditor" in t3["run"]["always"]
    assert "seo-content-auditor" in t3["pass_receipt"]["always"]
    assert t3["writer_one_of"] == ["docs-architect"]
    for tier in (t1, t2, t3):
        assert tier["run"]["if_code"] == ["code-reviewer"]
        receipts = {m for members in tier["pass_receipt"].values() for m in members}
        runs = {m for members in tier["run"].values() for m in members}
        assert receipts <= runs, "a PASS receipt can only come from a role that must run"


def test_manifest_ignores_the_operator_switch_lever(monkeypatch):
    expected = roles.role_manifest()
    monkeypatch.setenv(brief.ENFORCE_ENV, "off")
    assert roles.role_manifest() == expected
    assert brief.enforcement_date() is None  # the lever is restored, not consumed


def test_required_roles_cli_prints_the_manifest():
    out = subprocess.run(
        [sys.executable, "-B", "-m", "blogpipe", "required-roles"],
        cwd=SCRIPTS, capture_output=True, text=True, check=True,
    ).stdout
    assert out == roles.role_manifest()


def test_no_second_per_tier_gate_list_in_repository_prose():
    names = reviewer_roles()
    tier = re.compile(r"\bTier\s*[1-3]\b|^\|\s*[1-3]\s*\|")
    for rel in PROSE:
        path = ROOT / rel
        if not path.is_file():
            continue
        for number, line in enumerate(path.read_text().splitlines(), 1):
            where = f"{rel}:{number}"
            assert not re.search(r"\|\s*Quality Gates?\s*\|", line, re.I), (
                f"{where}: per-tier quality-gate column; point at the SKILL.md table instead"
            )
            named = {n for n in names if re.search(rf"(?<![\w-]){re.escape(n)}(?![\w-])", line)}
            assert not (tier.search(line) and len(named) >= 2), (
                f"{where}: per-tier reviewer list {sorted(named)}; point at the SKILL.md table"
            )


def test_verifiability_pass_is_marked_retired_not_a_gate():
    head = RETIRED.read_text().split("\n## ", 1)[0]
    assert "RETIRED" in head and "Not a publishing gate" in head
