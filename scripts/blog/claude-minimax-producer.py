#!/usr/bin/env python3
"""Run the existing Claude skill toolchain with the established static MiniMax key.

Only the child process environment changes. OAuth files and global settings are
untouched; no key is passed in argv or diagnostic output. The daily wrapper owns
the process deadline, Git mutation guard and deterministic publication gate.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path


def child_environment(environ, decrypt=subprocess.run):
    result = dict(environ)
    key = result.get("MINIMAX_API_KEY", "").strip()
    if not key:
        source = result.get(
            "API_PROVIDERS_SOPS",
            str(Path.home() / ".config/intentsolutions/api-providers.sops.json"),
        )
        decrypted = decrypt(
            ["sops", "-d", "--input-type", "json", "--output-type", "json", source],
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        )
        key = json.loads(decrypted.stdout).get("minimax", {}).get("key", "").strip()
    if not key:
        raise ValueError("configured key unavailable")
    result.update(
        {
            "ANTHROPIC_BASE_URL": "https://api.minimax.io/anthropic",
            "ANTHROPIC_API_KEY": key,
            "ANTHROPIC_AUTH_TOKEN": "",
            "ANTHROPIC_MODEL": "MiniMax-M3",
            "ANTHROPIC_SMALL_FAST_MODEL": "MiniMax-M3",
            "ANTHROPIC_DEFAULT_SONNET_MODEL": "MiniMax-M3",
            "ANTHROPIC_DEFAULT_OPUS_MODEL": "MiniMax-M3",
            "ANTHROPIC_DEFAULT_HAIKU_MODEL": "MiniMax-M3",
        }
    )
    return result


def agent_definitions(skill_dir):
    """Register the skill's custom agents explicitly; reading is not dispatch."""
    result = {}
    for name in ("blog-classifier", "blog-consistency-checker", "blog-fact-checker"):
        text = (skill_dir / "agents" / f"{name}.md").read_text()
        pieces = text.split("---", 2)
        if len(pieces) != 3:
            raise ValueError("invalid configured agent definition")
        description = re.search(r"^description:\s*(.*)$", pieces[1], re.MULTILINE)
        if description is None:
            raise ValueError("configured agent description missing")
        result[name] = {
            "description": description.group(1).strip('"'),
            "prompt": pieces[2].strip(),
            "model": "inherit",
        }
    return result


def execution_contract(skill, environ):
    root, run_id = environ.get("BLOG_REPO_DIR"), environ.get("BLOG_RUN_ID")
    manifest = environ.get("BLOG_RUN_MANIFEST")
    diagnostics = environ.get("BLOG_RUN_DIAGNOSTICS_DIR")
    helper = environ.get("BLOG_RUN_WORKSPACE_HELPER")
    if not all((root, run_id, manifest, diagnostics, helper)):
        raise ValueError("bound daily workspace/session/diagnostic context missing")
    return (
        f"Authoritative daily instructions: {skill / 'SKILL.md'} and "
        f"{skill / 'references/run-contract.md'}. Read both before production. "
        f"This run workspace is {root}; session/run_id is {run_id}. "
        f"Registered run manifest: {manifest}; diagnostics directory: {diagnostics}; "
        f"trusted workspace helper: {helper}. "
        "These current instructions override stale installed Skill references and path examples. "
        "Publication writes and their app helper paths MUST use the bound workspace. "
        "Staging candidates permit only DATE.RUN_ID.JSONLABEL.json where JSONLABEL uses "
        "letters, digits, underscores or hyphens; never place logs or scratch files there. "
        "For command stderr use the registered BLOG_RUN_WORKSPACE_HELPER diagnostic command "
        "with BLOG_RUN_MANIFEST; it retains bounded evidence in BLOG_RUN_DIAGNOSTICS_DIR "
        "outside the checkout. Do not redirect stderr or write files there directly. "
        "Do not write to the shared primary repository or use Git mutations. "
        "Mandatory real Agent gates must return their genuine structured "
        "blog_gate_receipt on final draft bytes; never invent receipts, "
        "classifiers, readiness or transcripts to clear a missing/blocked gate. "
        "Use run-scoped candidate filenames and the transactional append helper. "
        "Before claiming completion, run the shared verifier against the actual "
        "UUID session transcript outside the workspace and resolve every nonzero result. "
        "Do not read, print or modify credentials or unrelated user files."
    )


def main():
    try:
        environment = child_environment(os.environ)
        skill = Path(
            os.environ.get("BLOG_SKILL_DIR", str(Path.home() / ".claude/skills/blog-backfill"))
        )
        agents = agent_definitions(skill)
        contract = execution_contract(skill, os.environ)
    except (OSError, ValueError, TypeError, AttributeError, subprocess.SubprocessError):
        print("blog producer: configured MiniMax credential unavailable", file=sys.stderr)
        return 69
    os.execvpe(
        "claude",
        [
            "claude",
            "--agents",
            json.dumps(agents),
            "--append-system-prompt",
            contract,
            *sys.argv[1:],
        ],
        environment,
    )


if __name__ == "__main__":
    sys.exit(main())
