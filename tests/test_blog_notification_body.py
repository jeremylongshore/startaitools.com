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
