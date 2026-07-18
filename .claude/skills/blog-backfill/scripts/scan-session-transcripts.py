#!/usr/bin/env python3
"""Analyze the day's AI-coding session transcripts for blog-backfill material.

REWRITE (2026-07-16, transcript-audit fix). The old version was a truncated
DUMP of Claude-only plaintext: it discarded tool_use / tool_result / thinking
and capped assistant text at 500 chars, so "how I worked with the models" (the
tool activity, the failures, the course-corrections) never reached the writer.
75% of posts ended up with source_signals.session = absent.

This version is a multi-source ANALYZER. It:
  * pulls transcripts from EVERY AI-coding CLI used that day, not just Claude:
      - Claude Code   ~/.claude/projects/*/*.jsonl   (model per message)
      - Grok          ~/.grok/sessions/<cwd>/prompt_history.jsonl
      - Codex (OpenAI) ~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl
      - Gemini        ~/.gemini/history (stub — no real transcripts stored)
  * names each model EXACTLY for SEO ("Claude Opus 4.8", "Grok 4.5",
    "GPT-5.6 Sol") — never just "Claude" / "Grok" / "ChatGPT". The digest leads
    with a "Models worked with" roster the writer must cite by full name.
  * extracts the COLLABORATION, not the chatter: tool activity (commands, edits,
    agents), failure->fix arcs (errors + recovery), user course-corrections
    ("no", "wrong", "actually"), and per-session metrics.
  * REDACTS secrets (keys/tokens/.env values) deterministically before output —
    the old version only warned in a docstring.

Backwards-compatible: same CLI (--start/--end/--output/--project) and a readable
text digest by default, so gather-material.md flows unchanged. New: --json emits
a structured digest (for the classifier signal + writer beat, pieces 2 and 3),
and --sources restricts which CLIs to scan.

Usage:
    python3 scan-session-transcripts.py --start 2026-07-15
    python3 scan-session-transcripts.py --start 2026-07-15 --end 2026-07-16 --output /tmp/s.txt
    python3 scan-session-transcripts.py --start 2026-07-15 --json
    python3 scan-session-transcripts.py --start 2026-07-15 --sources claude,grok
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import unquote

HOME = Path.home()
CLAUDE_DIR = HOME / ".claude" / "projects"
GROK_DIR = HOME / ".grok" / "sessions"
CODEX_DIR = HOME / ".codex" / "sessions"
CODEX_CONFIG = HOME / ".codex" / "config.toml"
GROK_MODEL_CACHE = HOME / ".grok" / "models_cache.json"

MAX_ASSISTANT_CHARS = 900  # was 500; keep more substance, still bounded
MAX_USER_CHARS = 1200  # user turns are the highest-value signal
MAX_EXCERPTS_PER_SESSION = 30
SESSION_GAP_SECONDS = 1800  # >30 min gap = new session

# ---- Exact model display names (SEO: full names, never the bare vendor) ------
MODEL_DISPLAY = {
    "claude-opus-4-8": "Claude Opus 4.8",
    "claude-opus-4-7": "Claude Opus 4.7",
    "claude-sonnet-5": "Claude Sonnet 5",
    "claude-fable-5": "Claude Fable 5",
    "claude-haiku-4-5": "Claude Haiku 4.5",
    "grok-4.5": "Grok 4.5",
    "grok-4": "Grok 4",
    "gpt-5.6-sol": "GPT-5.6 Sol",
    "gpt-5-codex": "GPT-5 Codex",
    "gpt-4o": "GPT-4o",
    "deepseek-chat": "DeepSeek V3",
    "deepseek-reasoner": "DeepSeek R1",
    "deepseek-v3": "DeepSeek V3",
    "deepseek-r1": "DeepSeek R1",
    "minimax-m3": "MiniMax M3",
    "minimax-m2": "MiniMax M2",
    "minimax-text-01": "MiniMax Text 01",
}

# Brand-correct capitalization for vendor tokens (generic fallback casing).
_VENDOR_CASE = {
    "gpt": "GPT",
    "openai": "OpenAI",
    "deepseek": "DeepSeek",
    "minimax": "MiniMax",
    "gemini": "Gemini",
    "grok": "Grok",
    "claude": "Claude",
    "qwen": "Qwen",
    "llama": "Llama",
}


def display_model(raw: str | None) -> str | None:
    """Map a raw model id to its exact SEO display name. None for synthetic/empty.

    Handles a leading provider prefix ("deepseek/deepseek-chat" -> "deepseek-chat")
    and a trailing date stamp, then a known-id table, then a brand-cased generic
    fallback. A full name always beats the bare vendor for SEO.
    """
    if not raw or raw == "<synthetic>":
        return None
    raw = raw.strip()
    if "/" in raw:  # provider/model form
        raw = raw.split("/")[-1]
    if raw in MODEL_DISPLAY:
        return MODEL_DISPLAY[raw]
    base = re.sub(r"-\d{6,8}$", "", raw)  # strip a trailing date stamp
    if base in MODEL_DISPLAY:
        return MODEL_DISPLAY[base]
    parts = base.split("-")
    if len(parts) >= 2:
        vendor = _VENDOR_CASE.get(parts[0].lower(), parts[0].capitalize())
        rest = []
        for p in parts[1:]:
            rest.append(
                p.replace(".", "").capitalize()
                if not any(c.isdigit() for c in p)
                else p.replace("-", ".")
            )
        return f"{vendor} " + " ".join(rest)
    return _VENDOR_CASE.get(base.lower(), base)


# ---- Secret redaction (enforced, not just warned) ---------------------------
_SECRET_PATTERNS = [
    re.compile(r"sk-ant-[A-Za-z0-9_\-]{16,}"),
    re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
    re.compile(r"gh[opsur]_[A-Za-z0-9]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9\-]{10,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"AGE-SECRET-KEY-[A-Z0-9]{20,}"),
    re.compile(r"age1[ac-hj-np-z02-9]{25,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._\-]{16,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----"),
    # KEY=secretvalue / "token": "secretvalue" style assignments
    re.compile(
        r"(?i)\b([A-Z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD|PASSWD|API|AUTH)[A-Z0-9_]*)\b(\s*[:=]\s*[\"']?)([A-Za-z0-9._\-/+]{12,})"
    ),
    # Bare high-entropy token: a 24+ char alphanumeric run with mixed case AND a
    # digit (credential-like). Catches raw key values that leak into errors/logs
    # with no KEY= prefix. Spares git SHAs (lowercase hex, no uppercase) and UUIDs
    # (contain dashes), which are safe to show.
    re.compile(
        r"\b(?=[A-Za-z0-9]{24,}\b)(?=[A-Za-z0-9]*[a-z])(?=[A-Za-z0-9]*[A-Z])(?=[A-Za-z0-9]*[0-9])[A-Za-z0-9]{24,}\b"
    ),
]


def redact(text: str) -> str:
    if not text:
        return text
    for pat in _SECRET_PATTERNS:
        if pat.groups >= 3:
            text = pat.sub(lambda m: f"{m.group(1)}{m.group(2)}[REDACTED]", text)
        else:
            text = pat.sub("[REDACTED]", text)
    return text


# ---- Collaboration signals ---------------------------------------------------
_STEER = re.compile(
    r"(?i)(^|\s)(no[,.]|nope|that'?s wrong|thats wrong|wrong\b|actually[,]|wait[,]|stop\b|"
    r"not what i|don'?t\b|instead\b|revert\b|undo\b|that'?s not|incorrect|redo\b|scrap that|"
    r"back up|hold on|never ?mind|not quite|you missed|try again)"
)
# Strong failure signatures only. The bare words "error"/"failed" match log OUTPUT
# the operator pastes in, which inflated the count; require real failure markers so
# errors_hit is a trustworthy signal for the classifier (piece 2).
_ERROR = re.compile(
    r"traceback \(most recent call|"
    r"\bexit code [1-9]\d*\b|"
    r"command not found|"
    r"no such file or directory|"
    r"\bSyntaxError\b|\bModuleNotFoundError\b|\bAssertionError\b|\bTypeError\b|\bNameError\b|"
    r"npm ERR!|"
    r"^fatal:|"
    r"\bpanic:|segmentation fault|"
    r"permission denied|"
    r"non-zero exit|returned non-zero|"
    r"compilation failed",
    re.IGNORECASE | re.MULTILINE,
)


def is_correction(text: str) -> bool:
    return bool(text) and len(text) < 600 and bool(_STEER.search(text))


def tool_result_error(block: dict) -> tuple[bool, str]:
    if block.get("is_error") is True:
        content = _flatten(block.get("content"))
        return True, _first_error_line(content)
    content = _flatten(block.get("content"))
    if content and _ERROR.search(content[:2000]):
        return True, _first_error_line(content)
    return False, ""


def _first_error_line(text: str) -> str:
    for line in (text or "").splitlines():
        if _ERROR.search(line):
            return redact(line.strip())[:160]
    return redact((text or "").strip().splitlines()[0] if text else "")[:160]


def _flatten(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        out = []
        for b in content:
            if isinstance(b, dict):
                out.append(b.get("text") or b.get("content") or "")
            elif isinstance(b, str):
                out.append(b)
        return "\n".join(x for x in out if x)
    return ""


def describe_tool(name: str, inp: dict) -> str:
    inp = inp if isinstance(inp, dict) else {}
    if name == "Bash":
        return f"$ {redact(str(inp.get('command', '')))[:120]}"
    if name in ("Edit", "Write", "NotebookEdit", "Read"):
        return f"{name} {inp.get('file_path', '')}"
    if name in ("Task", "Agent"):
        return (
            f"dispatch {inp.get('subagent_type', 'agent')}: {str(inp.get('description', ''))[:80]}"
        )
    if name in ("Grep", "Glob"):
        return f"{name} {inp.get('pattern', '')}"
    if name == "WebSearch":
        return f"search: {str(inp.get('query', ''))[:80]}"
    if name == "WebFetch":
        return f"fetch: {inp.get('url', '')}"
    return name


# ---- Event model -------------------------------------------------------------
def _event(ts, source, model, project, role, kind, text="", tool="", is_error=False, note=""):
    return {
        "ts": ts,
        "source": source,
        "model": model,
        "project": project,
        "role": role,
        "kind": kind,
        "text": text,
        "tool": tool,
        "is_error": is_error,
        "note": note,
    }


def _parse_ts(s: str) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00")).replace(tzinfo=None)
    except (ValueError, TypeError):
        return None


def _project_from_dir(dirname: str) -> str:
    name = dirname.lstrip("-")
    for prefix in ("home-jeremy-000-projects-", "home-jeremy-"):
        if name.startswith(prefix):
            name = name[len(prefix) :]
            break
    if "--claude-worktrees" in name:
        name = name.split("--claude-worktrees")[0]
    return name or dirname


def _project_from_cwd(cwd: str) -> str:
    if not cwd:
        return "unknown"
    p = cwd.rstrip("/")
    marker = "/000-projects/"
    if marker in p:
        return p.split(marker, 1)[1].split("/")[0]
    return Path(p).name or "home"


# ---- Adapters (each yields events; each guarded, never crashes the run) ------
def claude_adapter(start, end):
    if not CLAUDE_DIR.exists():
        return
    for pdir in sorted(CLAUDE_DIR.iterdir()):
        if not pdir.is_dir():
            continue
        project = _project_from_dir(pdir.name)
        for jf in sorted(pdir.glob("*.jsonl")):
            try:
                for line in jf.open(encoding="utf-8", errors="replace"):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        o = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if o.get("type") not in ("user", "assistant"):
                        continue
                    ts = _parse_ts(o.get("timestamp"))
                    if not ts or ts < start or ts >= end:
                        continue
                    msg = o.get("message") or {}
                    if not isinstance(msg, dict):
                        continue
                    role = msg.get("role", o.get("type"))
                    model = display_model(msg.get("model"))
                    content = msg.get("content")
                    if isinstance(content, str):
                        content = [{"type": "text", "text": content}]
                    if not isinstance(content, list):
                        continue
                    for b in content:
                        if not isinstance(b, dict):
                            continue
                        bt = b.get("type")
                        if bt == "text":
                            t = redact((b.get("text") or "").strip())
                            if t:
                                yield _event(
                                    ts, "Claude Code", model, project, role, "text", text=t
                                )
                        elif bt == "tool_use" and role == "assistant":
                            yield _event(
                                ts,
                                "Claude Code",
                                model,
                                project,
                                role,
                                "tool_use",
                                tool=describe_tool(b.get("name", ""), b.get("input", {})),
                            )
                        elif bt == "tool_result" and role == "user":
                            err, note = tool_result_error(b)
                            yield _event(
                                ts,
                                "Claude Code",
                                model,
                                project,
                                role,
                                "tool_result",
                                is_error=err,
                                note=note,
                            )
            except (OSError, PermissionError):
                continue


def _grok_model():
    # Grok transcripts don't record the per-session model, and models_cache.json
    # lists AVAILABLE models, not the active one. Prefer an env override, then a
    # default-flagged cache entry, else the current Grok default.
    import os

    if os.environ.get("GROK_MODEL_DISPLAY"):
        return os.environ["GROK_MODEL_DISPLAY"]
    try:
        cache = json.loads(GROK_MODEL_CACHE.read_text())
        models = cache.get("models") if isinstance(cache, dict) else None
        if isinstance(models, list):
            for m in models:
                if isinstance(m, dict) and m.get("default") and (m.get("id") or m.get("name")):
                    return display_model(m.get("id") or m.get("name")) or "Grok 4.5"
    except Exception:
        pass
    return "Grok 4.5"


def grok_adapter(start, end):
    if not GROK_DIR.exists():
        return
    model = _grok_model()
    for cdir in sorted(GROK_DIR.glob("%2F*")):
        if not cdir.is_dir():
            continue
        project = _project_from_cwd(unquote(cdir.name))
        ph = cdir / "prompt_history.jsonl"
        if not ph.exists():
            continue
        try:
            for line in ph.open(encoding="utf-8", errors="replace"):
                line = line.strip()
                if not line:
                    continue
                try:
                    o = json.loads(line)
                except json.JSONDecodeError:
                    continue
                ts = _parse_ts(o.get("timestamp"))
                if not ts or ts < start or ts >= end:
                    continue
                t = redact((o.get("prompt") or "").strip())
                if t:
                    yield _event(ts, "Grok", model, project, "user", "text", text=t)
        except (OSError, PermissionError):
            continue


def _codex_model():
    try:
        for line in CODEX_CONFIG.read_text().splitlines():
            m = re.match(r'\s*model\s*=\s*"([^"]+)"', line)
            if m:
                return display_model(m.group(1)) or "Codex"
    except Exception:
        pass
    return "GPT-5.6 Sol"


def codex_adapter(start, end):
    if not CODEX_DIR.exists():
        return
    model = _codex_model()
    # Files are partitioned YYYY/MM/DD; only walk dates in range.
    day = start
    while day < end:
        ddir = CODEX_DIR / f"{day:%Y}" / f"{day:%m}" / f"{day:%d}"
        day += timedelta(days=1)
        if not ddir.is_dir():
            continue
        for jf in sorted(ddir.glob("rollout-*.jsonl")):
            project = "unknown"
            try:
                for line in jf.open(encoding="utf-8", errors="replace"):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        o = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    ts = _parse_ts(o.get("timestamp"))
                    payload = o.get("payload") or {}
                    if o.get("type") == "session_meta":
                        project = _project_from_cwd(payload.get("cwd", ""))
                        continue
                    if not ts or ts < start or ts >= end:
                        continue
                    if o.get("type") != "response_item":
                        continue
                    role = payload.get("role")
                    if role not in ("user", "assistant"):
                        continue
                    t = redact(_flatten(payload.get("content")).strip())
                    if t:
                        yield _event(ts, "Codex", model, project, role, "text", text=t)
            except (OSError, PermissionError):
                continue


def gemini_adapter(start, end):
    # ~/.gemini/history stores project-root markers / checkpoints, not
    # conversation transcripts. Registered for completeness; yields nothing.
    return
    yield  # pragma: no cover


ADAPTERS = {
    "claude": claude_adapter,
    "grok": grok_adapter,
    "codex": codex_adapter,
    "gemini": gemini_adapter,
}


# ---- Collaboration signal (deterministic; piece 2 feeds this to the classifier)
def _collab_score(m: dict) -> float:
    """0-1 collaboration richness from a day's metrics. Weighted to human steering
    (course-corrections — the rarest, truest signal of a real back-and-forth
    NARRATIVE) and the debugging drama (failures), so it can separate a genuine
    journey from a merely busy day. Thresholds are set high on purpose: any heavy
    day trips a few transient errors, so 'strong' should require real intensity."""
    tool = min(m.get("tool_calls", 0) / 150, 1.0)  # ~150 calls = substantial
    fail = min(m.get("errors_hit", 0) / 12, 1.0)  # ~12 real failures = a rough day
    corr = min(m.get("corrections", 0) / 5, 1.0)  # ~5 course-corrections = heavy steering
    span = min(m.get("span_minutes", 0) / 240, 1.0)
    return round(0.25 * tool + 0.30 * fail + 0.35 * corr + 0.10 * span, 3)


def _signal(score: float) -> str:
    if score >= 0.6:
        return "strong"
    if score >= 0.35:
        return "moderate"
    if score > 0.12:
        return "weak"
    return "absent"


def _rollup_by_date(days: list[dict]) -> dict:
    """Aggregate per-project days into one signal per DATE (the unit the tier
    classifier keys on). Sums activity across the day's projects, unions models,
    and writes a one-line hint the classifier + writer can lift verbatim."""
    by_date = defaultdict(list)
    for d in days:
        by_date[d["date"]].append(d)
    out = {}
    for date, ds in by_date.items():
        totals = {
            "tool_calls": sum(d["metrics"]["tool_calls"] for d in ds),
            "corrections": sum(d["metrics"]["corrections"] for d in ds),
            "errors_hit": sum(d["metrics"]["errors_hit"] for d in ds),
            "span_minutes": max((d["metrics"]["span_minutes"] for d in ds), default=0),
        }
        models = []
        for d in ds:
            for m in d["models"]:
                if m not in models:
                    models.append(m)
        score = _collab_score(totals)
        sig = _signal(score)
        hint = (
            f"{sig}: {totals['errors_hit']} failure-to-fix, {totals['corrections']} "
            f"course-corrections, {totals['span_minutes']} min"
            + (f" across {', '.join(models)}" if models else "")
        )
        out[date] = {
            "models": models,
            "session_signal": sig,
            "collaboration_score": score,
            "totals": totals,
            "hint": hint,
        }
    return out


# ---- Analysis ----------------------------------------------------------------
def collect(start, end, sources):
    events = []
    for name in sources:
        fn = ADAPTERS.get(name)
        if not fn:
            continue
        try:
            events.extend(fn(start, end))
        except Exception as e:  # noqa: BLE001 - one bad source never kills the rest
            print(f"[WARN] source '{name}' failed: {e}", file=sys.stderr)
    events.sort(key=lambda e: (e["ts"], e["project"]))
    return events


def analyze(events):
    """Group events by (project, date); compute models roster, metrics, arcs."""
    buckets = defaultdict(list)
    for e in events:
        buckets[(e["project"], e["ts"].strftime("%Y-%m-%d"))].append(e)

    out = []
    all_models = []
    for (project, date), evs in sorted(buckets.items()):
        evs.sort(key=lambda e: e["ts"])
        models = []
        for e in evs:
            if e["model"] and e["model"] not in models:
                models.append(e["model"])
        for m in models:
            if m not in all_models:
                all_models.append(m)

        # sessions by time gap
        sessions = 1
        for i in range(1, len(evs)):
            if (evs[i]["ts"] - evs[i - 1]["ts"]).total_seconds() > SESSION_GAP_SECONDS:
                sessions += 1

        tool_calls = [e for e in evs if e["kind"] == "tool_use"]
        errors = [e for e in evs if e["kind"] == "tool_result" and e["is_error"]]
        corrections = [
            e
            for e in evs
            if e["kind"] == "text" and e["role"] == "user" and is_correction(e["text"])
        ]
        tool_breakdown = Counter(e["tool"].split()[0] if e["tool"] else "?" for e in tool_calls)
        span_min = int((evs[-1]["ts"] - evs[0]["ts"]).total_seconds() // 60) if len(evs) > 1 else 0

        metrics = {
            "turns": sum(1 for e in evs if e["kind"] == "text"),
            "tool_calls": len(tool_calls),
            "corrections": len(corrections),
            "errors_hit": len(errors),
            "span_minutes": span_min,
            "tools": dict(tool_breakdown.most_common()),
        }
        score = _collab_score(metrics)
        out.append(
            {
                "project": project,
                "date": date,
                "sources": sorted({e["source"] for e in evs}),
                "models": models,
                "sessions": sessions,
                "metrics": metrics,
                "collaboration": {"score": score, "signal": _signal(score)},
                "failure_arcs": [
                    {"time": e["ts"].strftime("%H:%M"), "note": e["note"]} for e in errors
                ][:12],
                "corrections_list": [
                    {"time": e["ts"].strftime("%H:%M"), "text": e["text"][:200]}
                    for e in corrections
                ][:12],
                "excerpts": _excerpts(evs),
            }
        )
    return {"models_used": all_models, "date_signals": _rollup_by_date(out), "days": out}


def _excerpts(evs):
    ex = []
    for e in evs:
        if e["kind"] == "text":
            cap = MAX_USER_CHARS if e["role"] == "user" else MAX_ASSISTANT_CHARS
            t = e["text"]
            if e["role"] == "assistant" and len(t) < 40:
                continue  # skip short acks; the user turns + tools carry the story
            ex.append(
                {
                    "time": e["ts"].strftime("%H:%M"),
                    "role": e["role"],
                    "source": e["source"],
                    "text": t[:cap] + ("..." if len(t) > cap else ""),
                }
            )
        elif e["kind"] == "tool_use":
            ex.append(
                {
                    "time": e["ts"].strftime("%H:%M"),
                    "role": "tool",
                    "source": e["source"],
                    "text": e["tool"],
                }
            )
        elif e["kind"] == "tool_result" and e["is_error"]:
            ex.append(
                {
                    "time": e["ts"].strftime("%H:%M"),
                    "role": "error",
                    "source": e["source"],
                    "text": e["note"],
                }
            )
    return ex[: MAX_EXCERPTS_PER_SESSION * 4]


# ---- Output ------------------------------------------------------------------
def format_text(a) -> str:
    L = []
    if not a["days"]:
        return "No AI-coding session activity found in the given date range."
    L.append("## Models worked with (cite by EXACT name for SEO)")
    L.append(", ".join(a["models_used"]) if a["models_used"] else "(no model recorded)")
    L.append("")
    if a.get("date_signals"):
        L.append("## Session signal (per date; the tier classifier keys on this)")
        for date, s in sorted(a["date_signals"].items()):
            L.append(f"{date}: {s['hint']}")
        L.append("")
    for d in a["days"]:
        m = d["metrics"]
        L.append(f"=== {d['project']} ({d['date']}) ===")
        L.append(f"Sources: {', '.join(d['sources'])} | Models: {', '.join(d['models']) or 'n/a'}")
        L.append(
            f"~{d['sessions']} session(s) | {m['turns']} turns | {m['tool_calls']} tool calls | "
            f"{m['corrections']} corrections | {m['errors_hit']} errors hit | "
            f"{m['span_minutes']} min span"
        )
        L.append(
            f"Collaboration signal: {d['collaboration']['signal']} "
            f"(score {d['collaboration']['score']})"
        )
        if m["tools"]:
            L.append("Tool activity: " + ", ".join(f"{k}×{v}" for k, v in m["tools"].items()))
        if d["failure_arcs"]:
            L.append("Failure→fix moments (the debugging story):")
            for f in d["failure_arcs"]:
                L.append(f"  [{f['time']}] {f['note']}")
        if d["corrections_list"]:
            L.append("Course-corrections (how the human steered):")
            for c in d["corrections_list"]:
                L.append(f"  [{c['time']}] {c['text']}")
        L.append("")
        L.append("Transcript (redacted, analyzed excerpts):")
        for e in d["excerpts"]:
            tag = {"user": "User", "assistant": "AI", "tool": "  ↳", "error": "  ✗"}.get(
                e["role"], e["role"]
            )
            body = e["text"]
            if "\n" in body:
                first, *rest = body.split("\n")
                body = first + "\n" + "\n".join("      " + r for r in rest)
            L.append(f"[{e['time']}] {tag} ({e['source']}): {body}")
        L.append("")
        L.append("")
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Analyze the day's multi-model AI-coding transcripts.")
    ap.add_argument("--start", required=True, help="Start date YYYY-MM-DD (inclusive)")
    ap.add_argument("--end", default=None, help="End date YYYY-MM-DD (exclusive). Default start+1.")
    ap.add_argument("--output", "-o", default=None, help="Write to file instead of stdout.")
    ap.add_argument("--project", "-p", default=None, help="Filter to a project (substring).")
    ap.add_argument(
        "--json", action="store_true", help="Emit the structured digest (for pieces 2/3)."
    )
    ap.add_argument(
        "--sources",
        default="claude,grok,codex,gemini",
        help="Comma list of CLIs to scan (claude,grok,codex,gemini).",
    )
    args = ap.parse_args(argv)

    start = datetime.strptime(args.start, "%Y-%m-%d")
    end = datetime.strptime(args.end, "%Y-%m-%d") if args.end else start + timedelta(days=1)
    sources = [s.strip().lower() for s in args.sources.split(",") if s.strip()]

    print(
        f"Scanning {', '.join(sources)} transcripts: {start.date()} to {end.date()}",
        file=sys.stderr,
    )
    events = collect(start, end, sources)
    a = analyze(events)

    if args.project:
        a["days"] = [d for d in a["days"] if args.project.lower() in d["project"].lower()]
        a["models_used"] = sorted({m for d in a["days"] for m in d["models"]})
        a["date_signals"] = _rollup_by_date(a["days"])

    output = json.dumps(a, indent=2, ensure_ascii=False) if args.json else format_text(a)
    try:
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            print(f"Output written to: {args.output}", file=sys.stderr)
        else:
            print(output)
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
        return 0

    print(
        f"Summary: {len(a['days'])} project-day(s), "
        f"models: {', '.join(a['models_used']) or 'none'}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
