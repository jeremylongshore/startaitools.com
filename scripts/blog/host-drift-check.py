#!/usr/bin/env python3
"""host-drift-check.py: compare the versioned blog host state with the live host. Read-only.

Two things live on the host but are owned by this repository (authority map
000-docs/014 sections 2, 3 and 4.1):

  1. The blog cron schedule. scripts/blog/host/blog-cron.manifest holds every host
     crontab line that runs a scripts/blog/ job, verbatim. This check reads
     `crontab -l` and reports lines missing from the host and blog lines the
     manifest does not know.
  2. The two global gate reviewer agents that blogpipe/roles.py requires
     (fact-checker, article-consistency-checker). scripts/blog/host/agents/ holds
     the reviewed copies and SHA256SUMS their hashes; this check reports a deployed
     copy under ~/.claude/agents that is missing or differs. A producer run can cite
     the hash it printed.

It never edits the crontab or the deployed agents. On drift it prints what differs
and the command a human would run after review.

Exit: 0 no drift, 1 drift, 2 the check itself could not run or the repo copy is
inconsistent with SHA256SUMS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

HOST = Path(__file__).resolve().parent / "host"
MANIFEST = HOST / "blog-cron.manifest"
AGENTS = HOST / "agents"
MARKER = "/blog/startaitools/scripts/blog/"


def entries(text: str, marker: str) -> list[str]:
    return [
        line.rstrip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#") and marker in line
    ]


def manifest_entries(path: Path = MANIFEST) -> list[str]:
    return [
        line.rstrip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def check_cron(live_text: str, manifest: Path, marker: str) -> dict:
    want, have = Counter(manifest_entries(manifest)), Counter(entries(live_text, marker))
    return {
        "entries": sum(want.values()),
        "missing_on_host": sorted((want - have).elements()),
        "unexpected_on_host": sorted((have - want).elements()),
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pinned(agents: Path = AGENTS) -> dict[str, str]:
    sums = {}
    for line in (agents / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, name = line.split(maxsplit=1)
            sums[name.strip()] = digest
    return sums


def check_agents(agents: Path, deployed: Path) -> dict:
    rows, inconsistent = [], []
    for name, digest in sorted(pinned(agents).items()):
        repo = agents / name
        if not repo.is_file() or sha256(repo) != digest:
            inconsistent.append(name)
            continue
        target = deployed / name
        live = sha256(target) if target.is_file() else None
        rows.append({
            "agent": name,
            "repo_sha256": digest,
            "deployed_sha256": live,
            "status": "OK" if live == digest else ("MISSING" if live is None else "DRIFT"),
        })
    return {"agents": rows, "repo_inconsistent": inconsistent}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--crontab", type=Path, help="read this file instead of `crontab -l`")
    ap.add_argument("--manifest", type=Path, default=MANIFEST)
    ap.add_argument("--agents-dir", type=Path, default=AGENTS)
    ap.add_argument("--deployed-agents", type=Path, default=Path.home() / ".claude/agents")
    ap.add_argument("--marker", default=MARKER, help="substring that marks a blog cron line")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    try:
        if args.crontab:
            live = args.crontab.read_text(encoding="utf-8")
        else:
            live = subprocess.run(["crontab", "-l"], capture_output=True, text=True,
                                  check=True, timeout=30).stdout
        cron = check_cron(live, args.manifest, args.marker)
        agents = check_agents(args.agents_dir, args.deployed_agents)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"ERROR: drift check could not run: {exc}", file=sys.stderr)
        return 2

    drift = bool(cron["missing_on_host"] or cron["unexpected_on_host"]
                 or any(row["status"] != "OK" for row in agents["agents"]))
    rc = 2 if agents["repo_inconsistent"] else (1 if drift else 0)
    if args.json:
        print(json.dumps({"rc": rc, "cron": cron, **agents}, indent=2))
        return rc

    if cron["missing_on_host"] or cron["unexpected_on_host"]:
        print(f"cron: DRIFT against {args.manifest.name} ({cron['entries']} entries)")
        for line in cron["missing_on_host"]:
            print(f"  missing on host:    {line}")
        for line in cron["unexpected_on_host"]:
            print(f"  unexpected on host: {line}")
        print("  Reconcile by reviewed change: update the manifest or the crontab, never both blind.")
    else:
        print(f"cron: OK ({cron['entries']} entries match {args.manifest.name})")
    for row in agents["agents"]:
        print(f"agent {row['agent']}: {row['status']} repo sha256={row['repo_sha256']}"
              + ("" if row["status"] == "OK" else f" deployed={row['deployed_sha256']}"))
        if row["status"] != "OK":
            print(f"  after review: install -m 0644 {args.agents_dir / row['agent']} "
                  f"{args.deployed_agents / row['agent']}")
    for name in agents["repo_inconsistent"]:
        print(f"ERROR: {args.agents_dir / name} does not match SHA256SUMS", file=sys.stderr)
    return rc


if __name__ == "__main__":
    sys.exit(main())
