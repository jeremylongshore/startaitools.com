"""Actual wrapper notification function, with an offline no-send transport."""

import hashlib
import json
import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("size", [200_000, 1_000_000])
@pytest.mark.parametrize("sender_rc", [0, 1])
def test_large_notification_file_preserves_bytes_and_cleans_private_source(
    tmp_path, size, sender_rc
):
    wrapper = (ROOT / "scripts/blog/blog-backfill-daily.sh").read_text()
    start = wrapper.index("send_notification() {")
    end = wrapper.index('\nif [ -n "$TARGET_ARG" ]; then', start)
    payload = tmp_path / "input.txt"
    body = ("Incident failure and full evidence\n" + "x" * size).encode()
    payload.write_bytes(body)
    receipt = tmp_path / "receipt.json"
    tools = tmp_path / "tools"
    tools.mkdir()
    node = tools / "node"
    node.write_text(
        "#!/usr/bin/env python3\n"
        "import sys,os,json,pathlib,hashlib\n"
        "assert '--body' not in sys.argv\n"
        "p=pathlib.Path(sys.argv[sys.argv.index('--body-file')+1])\n"
        "assert p.stat().st_mode & 0o077 == 0\n"
        "assert p.parent.stat().st_mode & 0o077 == 0\n"
        "d={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}\n"
        "pathlib.Path(os.environ['RECEIPT']).write_text(json.dumps(d))\n"
        "sys.exit(int(os.environ['SENDER_RC']))\n"
    )
    node.chmod(0o700)
    script = tmp_path / "actual-notification.sh"
    script.write_text(
        "set -uo pipefail\n"
        + wrapper[start:end]
        + '\nBODY=$(cat "$INPUT")\n'
        + 'send_notification "Root-cause incident" "$BODY"\n'
    )
    env = dict(
        os.environ,
        PATH=str(tools) + os.pathsep + os.environ["PATH"],
        INPUT=str(payload),
        RECEIPT=str(receipt),
        SENDER_RC=str(sender_rc),
        EMAIL_SCRIPT="offline-unused-no-send",
    )
    result = subprocess.run(["bash", str(script)], env=env, capture_output=True, text=True)
    assert result.returncode == sender_rc, result.stderr
    proof = json.loads(receipt.read_text())
    assert proof["sha256"] == hashlib.sha256(body).hexdigest()
    assert not Path(proof["path"]).parent.exists()


def test_summary_notification_failure_withholds_success(tmp_path):
    wrapper = (ROOT / "scripts/blog/blog-backfill-daily.sh").read_text()
    start = wrapper.index('if ! send_notification "$SUBJECT" "$BODY"')
    end = wrapper.index("\nfi", start) + len("\nfi")
    script = tmp_path / "actual-summary.sh"
    script.write_text(
        "set -uo pipefail\n"
        "send_notification() { return 1; }\nlog() { :; }\n"
        "STATUS=OK; SUBJECT=incident; BODY=evidence; LAND_RESULT=published\n"
        + wrapper[start:end]
        + '\nprintf "%s" "$STATUS"\n'
    )
    result = subprocess.run(
        ["bash", str(script)],
        env={**os.environ, "LOG": str(tmp_path / "sender.log")},
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith("FAILED (notification delivery failed;")


@pytest.mark.parametrize("census_result", ["valid", "invalid", "error"])
def test_wrapper_reports_owner_and_external_quarantine_and_refuses_invalid_census(
    tmp_path, census_result
):
    """Execute the storage stage against distinct owner/workspace/registry paths."""
    wrapper = (ROOT / "scripts/blog/blog-backfill-daily.sh").read_text()
    start = wrapper.index("# --- Bounded retention + storage census")
    end = wrapper.index("# --- Consecutive-failure escalation", start)
    owner = tmp_path / "owner"
    workspace = tmp_path / "isolated"
    owner.mkdir()
    workspace.mkdir()
    helper = tmp_path / "census.py"
    report = {
        "registry_bytes": 8_000_000_000,
        "workspace_bytes": 6_000_000_000,
        "protected_bytes": 6_000_000_000,
        "runs": [
            {"status": "quarantined", "workspace_bytes": 3_000_000_000, "quarantine_bytes": 40_000},
            {"status": "quarantined", "workspace_bytes": 3_000_000_000, "quarantine_bytes": 50_000},
        ],
    }
    if census_result == "invalid":
        report["protected_bytes"] = "unknown"
    helper.write_text(
        "import json,sys\n"
        f"assert sys.argv[1:] == ['census','--repo',{str(owner)!r},"
        f"'--state-dir',{str(tmp_path / 'registry')!r}]\n"
        f"print({json.dumps(report)!r})\n"
        f"sys.exit({2 if census_result == 'error' else 0})\n"
    )
    script = tmp_path / "actual-storage-stage.sh"
    script.write_text(
        "set -uo pipefail\n"
        'log() { printf \'%s\\n\' "$*" >> "$LOG"; }\n'
        "prune_run_logs() { printf 0; }\n"
        "quarantine_census() {\n"
        '  [ "$1" = "$BLOG_SOURCE_DIR/.blog-quarantine" ] || exit 99\n'
        "  QUARANTINE_COUNT=11; QUARANTINE_MB=1; return 0;\n}\n"
        "STATUS=OK\n" + wrapper[start:end] + 'printf \'%s\\n\' "$STATUS" "$QUARANTINE_COUNT" '
        '"${EXTERNAL_QUARANTINE_BYTES:-unknown}" "$QUARANTINE_NOTE" "$REGISTRY_NOTE"\n'
    )
    result = subprocess.run(
        ["bash", str(script)],
        env={
            **os.environ,
            "BLOG_SOURCE_DIR": str(owner),
            "BLOG_DIR": str(workspace),
            "WORKSPACE_HELPER": str(helper),
            "BLOG_RUN_STATE_DIR": str(tmp_path / "registry"),
            "HOME": str(tmp_path),
            "LOG": str(tmp_path / "storage.log"),
            "LOG_DIR": str(tmp_path),
        },
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    rows = result.stdout.splitlines()
    if census_result == "valid":
        assert rows[0] == "OK"
        assert rows[1:3] == ["13", "6000090000"]
        assert "13 entries across owner and external registry" in rows[3]
        assert json.loads(rows[4])["protected_bytes"] == 6_000_000_000
    else:
        assert rows[0].startswith("FAILED (run-registry storage census;")
        assert rows[4] == "unavailable"
