#!/usr/bin/env python3
"""Run the existing Claude skill toolchain with the established static MiniMax key.

Only the child process environment changes. OAuth files and global settings are
untouched; no key is passed in argv or diagnostic output. The daily wrapper owns
the process deadline, Git mutation guard and deterministic publication gate.
"""
import json
import os
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
        decrypted = decrypt(["sops", "-d", "--input-type", "json", "--output-type", "json", source],
                            capture_output=True, text=True, timeout=30, check=True)
        key = json.loads(decrypted.stdout).get("minimax", {}).get("key", "").strip()
    if not key:
        raise ValueError("configured key unavailable")
    result.update({"ANTHROPIC_BASE_URL": "https://api.minimax.io/anthropic",
                   "ANTHROPIC_API_KEY": key, "ANTHROPIC_AUTH_TOKEN": "",
                   "ANTHROPIC_MODEL": "MiniMax-M3", "ANTHROPIC_SMALL_FAST_MODEL": "MiniMax-M3",
                   "ANTHROPIC_DEFAULT_SONNET_MODEL": "MiniMax-M3",
                   "ANTHROPIC_DEFAULT_OPUS_MODEL": "MiniMax-M3",
                   "ANTHROPIC_DEFAULT_HAIKU_MODEL": "MiniMax-M3"})
    return result


def main():
    try:
        environment = child_environment(os.environ)
    except (OSError, ValueError, TypeError, AttributeError, subprocess.SubprocessError):
        print("blog producer: configured MiniMax credential unavailable", file=sys.stderr)
        return 69
    os.execvpe("claude", ["claude", *sys.argv[1:]], environment)


if __name__ == "__main__":
    sys.exit(main())
