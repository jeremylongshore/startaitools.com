#!/usr/bin/env python3
"""make-post-image.py: generate a per-post image, grounded in that post.

WHY THIS EXISTS
    Posts shipped with either no image or the same generic OG card, so every
    link preview looked like every other link preview. This makes one image per
    post, derived from what that specific post is actually about.

WHAT MAKES THE IMAGE POST-SPECIFIC
    A dedicated step reads the landed post and produces a SCENE: the concrete
    artifact or system the post is about, and the failure or reversal at its
    centre. That scene is the only part of the prompt that varies. Everything
    around it is fixed brand frame plus fixed constraints, so an image is never
    off-brand and never accidentally becomes a stock "AI" picture.

    The full prompt is stored in the ledger entry. A bad image is therefore
    reproducible and diagnosable: read the prompt, see why it produced that.

CONSTRAINTS BAKED INTO EVERY PROMPT
    No text or lettering. Models render type badly, and the card already carries
    the title, so asking for words buys a mangled word.
    Brand frame: charcoal and ember, operator and industrial, physical-systems
    metaphor rather than a screenshot of software.
    An explicit negative list against AI-slop visuals: glowing brains, circuit
    board overlays, robot hands, neon grids, generic "AI" iconography.

PROVIDER
    MiniMax only. It is already paid for and verified entitled, so this adds no
    vendor and no new billing. The registry below is a thin seam: another
    provider can be added by writing one class and one dict entry, and nothing
    else changes. Nothing else is wired today.

    Variation comes from the PROMPT, not from swapping vendors. The model pick
    is SEEDED ON THE POST SLUG across the provider's BRAND-VETTED catalogue, so
    the same post always chooses the same model. That is what makes a bad image
    reproducible, while spreading a corpus of posts across whatever is vetted.
    See MiniMaxProvider for why that catalogue currently holds one model.

FAILURE BEHAVIOUR
    Generate, retry once, then fall back to the deterministic card from
    make-social-card.py. A post never ships with no image because a vendor had a
    bad minute, and the fallback is recorded rather than hidden.

Usage:
  make-post-image.py --post content/posts/slug.md [--provider minimax]
                     [--outdir static/images/posts] [--ledger] [--json]
  make-post-image.py --post ... --prompt-only     # build+print the prompt, no spend
  make-post-image.py --post ... --no-llm          # deterministic scene only

Exit 0 on success (including a recorded card fallback), 2 on usage/IO error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_OUTDIR = os.path.join(ROOT, "static", "images", "posts")
LEDGER = os.path.join(ROOT, ".blog-syndication-ledger.json")
CARD_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "make-social-card.py")
SOPS_FILE = os.path.expanduser("~/.config/intentsolutions/api-providers.sops.json")

# --------------------------------------------------------------------------
# Prompt construction
# --------------------------------------------------------------------------

# MiniMax hard-rejects a prompt over 1500 characters (error 2013). The fixed
# clauses below are deliberately terse so the per-post scene gets the budget;
# see SCENE_BUDGET.
MAX_PROMPT = 1480

BRAND_FRAME = (
    "Charcoal and ember palette: near-black charcoal ground, one warm ember "
    "orange accent, cool grey mid-tones. Industrial operator-grade realism: "
    "physical machinery, workshop and control-room materials, brushed steel, "
    "worn enamel, one hard directional light. Photographic depth of field, "
    "restrained composition, one clear focal point."
)

NO_LETTERING = (
    "No text, lettering, numerals, signage, labels, watermarks, logos, or "
    "user-interface chrome anywhere in the image."
)

BANNED_VISUALS = [
    "glowing brain",
    "digital brain",
    "circuit board",
    "circuitry overlay",
    "robot hand",
    "humanoid robot",
    "android",
    "neon grid",
    "cyberpunk cityscape",
    "binary code",
    "streaming code rain",
    "matrix rain",
    "wireframe head",
    "hologram",
    "holographic interface",
    "floating hexagons",
    "network of glowing nodes",
    "blue technology background",
    "handshake with a robot",
    "crystal ball",
    "lightbulb moment",
]

# The prompt carries a REPRESENTATIVE negative list; the guard above checks the
# EXHAUSTIVE one. Splitting them keeps the prompt inside MiniMax's 1500-character
# ceiling without weakening enforcement: the guard is what actually stops a
# cliche, the prompt clause only steers.
NEGATIVE_CLAUSE = (
    "Avoid AI-stock cliches: glowing brains, circuit-board overlays, robot "
    "hands, humanoid robots, neon grids, binary code, holograms, glowing node "
    "networks, blue technology haze, futuristic sci-fi styling."
)

# Characters left for the per-post scene once the fixed clauses are assembled.
SCENE_BUDGET = MAX_PROMPT - (
    len(BRAND_FRAME) + len(NO_LETTERING) + len(NEGATIVE_CLAUSE) + 8
)

# Terms that, in the SCENE clause, mean the model was asked to render words.
# Checked against the per-post clause only; the fixed constraints above name
# these words precisely in order to forbid them.
LETTERING_TERMS = [
    "text", "lettering", "typography", "typeface", "font", "word", "letter",
    "numeral", "caption", "subtitle", "title card", "signage", "sign that",
    "label", "labelled", "labeled", "writing", "written", "inscription",
    "handwriting", "banner reading", "logo", "watermark",
]


def scene_violations(scene: str) -> list[str]:
    """Return every reason this scene clause is unacceptable.

    Two failure classes: asking the model for words, and asking for a visual
    cliche. Both are rejected before a single token is spent on generation.
    """
    low = scene.lower()
    bad: list[str] = []
    for term in LETTERING_TERMS:
        if re.search(rf"\b{re.escape(term)}s?\b", low):
            bad.append(f"lettering request: {term!r}")
    for cliche in BANNED_VISUALS:
        if cliche in low:
            bad.append(f"banned visual cliche: {cliche!r}")
    return bad


def trim_scene(scene: str, budget: int = SCENE_BUDGET) -> str:
    """Fit the scene inside the character budget, cutting at a sentence end.

    A truncated scene is fine; a rejected 1500-character prompt is not, because
    that is a hard vendor error that costs the whole generation.
    """
    scene = " ".join(scene.split()).strip().strip('"').rstrip(".")
    if len(scene) <= budget:
        return scene
    cut = scene[:budget]
    stop = max(cut.rfind(". "), cut.rfind("; "))
    return (cut[:stop] if stop > budget // 3 else cut.rsplit(" ", 1)[0]).rstrip(" .,;")


def build_prompt(scene: str) -> str:
    """Assemble the full prompt. Raises ValueError if the scene is unsafe."""
    bad = scene_violations(scene)
    if bad:
        raise ValueError("unsafe scene clause: " + "; ".join(bad))
    scene = trim_scene(scene)
    prompt = f"{scene}. {BRAND_FRAME} {NO_LETTERING} {NEGATIVE_CLAUSE}"
    if len(prompt) > MAX_PROMPT:  # belt and braces: the vendor rejects over 1500
        raise ValueError(f"assembled prompt is {len(prompt)} chars, over {MAX_PROMPT}")
    return prompt


# --------------------------------------------------------------------------
# Reading the post
# --------------------------------------------------------------------------

FAILURE_CUES = re.compile(
    r"\b(broke|broken|failed|failing|silently|silent|lied|wrong|regress\w*|"
    r"quarantin\w*|outage|stale|drift\w*|never fired|did not|didn't|"
    r"turned out|reversed|rolled back)\b",
    re.I,
)


def read_post(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    def fm(field: str) -> str:
        m = re.search(rf"^{field}\s*[=:]\s*['\"](.+?)['\"]\s*$", text, re.M)
        return m.group(1) if m else ""

    body = re.sub(r"^\s*[-+]{3}.*?^[-+]{3}\s*$", "", text, count=1, flags=re.S | re.M)
    body_nocode = re.sub(r"```[\s\S]*?```", " ", body)
    headings = re.findall(r"^#{2,3}\s+(.+?)\s*$", body_nocode, re.M)
    sentences = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", body_nocode))
    failure = next((s.strip() for s in sentences
                    if 40 < len(s) < 300 and FAILURE_CUES.search(s)), "")
    return {
        "title": fm("title") or os.path.basename(path).rsplit(".", 1)[0],
        "description": fm("description"),
        "slug": fm("slug") or os.path.basename(path).rsplit(".", 1)[0],
        "headings": headings[:8],
        "failure": failure,
        "body": body_nocode[:6000],
    }


def deterministic_scene(post: dict) -> str:
    """Offline fallback scene. Never contains lettering or a cliche by
    construction: it picks from a fixed set of physical-systems metaphors and
    keys the pick on the slug so it is stable per post."""
    metaphors = [
        "A single industrial control panel in a dim workshop, one ember-lit "
        "indicator glowing while the rest of the board sits dark and cold",
        "A heavy steel gate mechanism half open on a loading dock, its linkage "
        "caught mid-travel, ember light raking across the worn metal",
        "A bank of analogue pressure gauges on a scuffed enamel housing, one "
        "needle pinned hard over into the ember-marked band",
        "A workbench under a single hard lamp, one machined part lifted clear "
        "of an assembly that has been taken apart around it",
        "A junction box opened in a service corridor, cabling fanned out and "
        "one line traced through in ember while the others stay in shadow",
        "A conveyor line stopped dead in a cold plant, a single ember warning "
        "lamp above it, the belt still carrying one unfinished part",
        "An inspection hatch swung open on a large machine, the interior lit "
        "ember from within, tools set down on the plate beside it",
        "A relay rack in a dark equipment room, one relay thrown while the rank "
        "of identical relays beside it stays closed",
    ]
    idx = int.from_bytes(hashlib.sha256(post["slug"].encode()).digest()[:4], "big")
    return metaphors[idx % len(metaphors)]


LLM_PROMPT = """Read this blog post and describe ONE photographic scene that would
illustrate it.

The blog is a working engineer's journal. Every post is about a real system that
was built, broke, or got fixed. Your scene must be grounded in the specific post below: what it
is actually about, the concrete artifact or system at its centre, and the failure
or reversal that makes it a story.

Rules for the scene you describe:
- Describe a PHYSICAL scene. Real machinery, workshop, control room, industrial
  equipment. Translate the software idea into a physical-systems metaphor. Never
  describe a screen, a terminal, a dashboard, or a user interface.
- Describe NO text, words, letters, numbers, labels, signs, or logos. Do not use
  any of those words in your answer.
- Do not describe any of these tired stock visuals: glowing brains, circuit
  boards, robot hands, humanoid robots, neon grids, binary code, holograms,
  networks of glowing nodes, lightbulbs.
- One focal point. TWO SENTENCES MAXIMUM, under 400 characters total. No colour
  palette (that is added separately). No camera settings.
- Output the scene and NOTHING else. Do not explain your reasoning, do not
  narrate what you read, do not preface it with "Scene:" or "Here is". Your
  entire reply is the scene description itself.

POST TITLE: {title}

POST SUMMARY: {description}

SECTION HEADINGS: {headings}

THE FAILURE OR REVERSAL AT ITS CENTRE: {failure}

Output ONLY the scene description. No preamble, no quotes, no explanation."""


def llm_scene(post: dict, timeout: int = 120) -> str:
    """Ask a bounded `claude -p` for a post-specific scene. Returns "" on any
    failure so the caller falls back to the deterministic metaphor."""
    if not shutil.which("claude"):
        return ""
    prompt = LLM_PROMPT.format(
        title=post["title"],
        description=post["description"] or "(none)",
        headings="; ".join(post["headings"]) or "(none)",
        failure=post["failure"] or "(not stated explicitly)",
    )
    try:
        out = subprocess.run(
            ["claude", "-p", prompt, "--model",
             os.environ.get("IMAGE_SCENE_MODEL", "claude-sonnet-5")],
            capture_output=True, text=True, timeout=timeout, check=False,
        )
    except (subprocess.TimeoutExpired, OSError):
        return ""
    if out.returncode != 0:
        return ""
    return clean_scene(out.stdout)


# Sentences where the model narrates the task instead of describing the scene.
# It leaks these despite being told not to ("Reading through the failure to
# ground the scene in the actual mechanism, ..."), and they waste the scene
# budget on words the image generator cannot use.
_META_CUE = re.compile(
    r"\b(reading through|here is|here's|scene|i(?:'ll| will| have)|based on|"
    r"to ground|the post|the article|this describes|description:)\b", re.I)


def clean_scene(raw: str) -> str:
    """Strip preamble and labels, then fit the budget.

    Keeps only sentences that describe the picture. A reply that is entirely
    meta returns "" so the caller falls back to the deterministic metaphor.
    """
    text = " ".join(raw.split()).strip().strip('"')
    text = re.sub(r"^(scene|image|description)\s*:\s*", "", text, flags=re.I)
    kept = [s for s in re.split(r"(?<=[.!?])\s+", text)
            if s.strip() and not _META_CUE.search(s)]
    return trim_scene(" ".join(kept)) if kept else ""


# --------------------------------------------------------------------------
# Provider registry
# --------------------------------------------------------------------------


class MiniMaxProvider:
    """MiniMax image generation. Verified entitled on the existing key.

    CATALOGUE, and why it has one entry.

    MiniMax exposes two image models and both authenticate, both accept the same
    request shape, and both return {"data": {"image_urls": [url]}}. They are NOT
    two variants of one model. Generating the same post through each on
    2026-08-09 produced:

      image-01       dark industrial photography, ember accents, physical
                     subject matter. Exactly the brand frame.
      image-01-live  stylized game and anime illustration, cyan glow, flat
                     rendering. It ignored the charcoal-and-ember palette and
                     the photographic instruction entirely.

    So `models` is the BRAND-VETTED pick list, not everything the vendor sells.
    Seeding across a model that will not honour the brand frame is not variation,
    it is a coin flip on whether the post gets an off-brand image. Variation comes
    from the per-post prompt, which is where the plan always put it.

    `all_models` stays available for --model, so image-01-live can still be
    reached deliberately. If MiniMax ships a second photographic model, vet it
    and add it to `models`: the seeded pick already spreads across whatever is
    in that list.
    """

    name = "minimax"
    models = ["image-01"]
    all_models = ["image-01", "image-01-live"]
    endpoint = "https://api.minimax.io/v1/image_generation"

    def __init__(self) -> None:
        self._key: str | None = None

    def api_key(self) -> str:
        if self._key:
            return self._key
        key = os.environ.get("MINIMAX_API_KEY", "").strip()
        if not key and os.path.isfile(SOPS_FILE) and shutil.which("sops"):
            try:
                out = subprocess.run(["sops", "-d", SOPS_FILE], capture_output=True,
                                     text=True, timeout=30, check=True)
                key = (json.loads(out.stdout).get("minimax", {}).get("key") or "").strip()
            except (subprocess.SubprocessError, ValueError, KeyError):
                key = ""
        if not key:
            raise RuntimeError(
                "no MiniMax API key (set MINIMAX_API_KEY or provision "
                f"{SOPS_FILE})")
        self._key = key
        return key

    def generate(self, prompt: str, model: str, timeout: int = 180) -> bytes:
        body = json.dumps({
            "model": model,
            "prompt": prompt,
            "aspect_ratio": "16:9",
            "n": 1,
            "response_format": "url",
        }).encode()
        req = urllib.request.Request(
            self.endpoint, data=body, method="POST",
            headers={"Authorization": f"Bearer {self.api_key()}",
                     "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read())
        status = payload.get("base_resp", {})
        if status.get("status_code") != 0:
            raise RuntimeError(
                f"minimax error {status.get('status_code')}: {status.get('status_msg')}")
        urls = (payload.get("data") or {}).get("image_urls") or []
        if not urls:
            raise RuntimeError("minimax returned no image_urls")
        with urllib.request.urlopen(urls[0], timeout=timeout) as img:
            return img.read()


PROVIDERS = {MiniMaxProvider.name: MiniMaxProvider}


def resolve_provider(name: str):
    if name not in PROVIDERS:
        raise ValueError(
            f"unknown image provider {name!r}; known: {sorted(PROVIDERS)}")
    return PROVIDERS[name]()


def pick_model(slug: str, models: list[str]) -> str:
    """Deterministic, slug-seeded model choice.

    Stable per post so the same post always regenerates identically and a bad
    image can be reproduced. Spread across the catalogue so a corpus of posts
    does not all land on one model.
    """
    if not models:
        raise ValueError("provider exposes no image models")
    digest = hashlib.sha256(slug.encode("utf-8")).digest()
    return models[int.from_bytes(digest[:8], "big") % len(models)]


# --------------------------------------------------------------------------
# Fallback + ledger
# --------------------------------------------------------------------------


def repo_rel(path: str) -> str:
    """Repo-relative when the path is inside the repo, absolute otherwise.

    os.path.relpath alone produced ../../../../../tmp/... for a scratch outdir,
    which is neither readable nor usable by the packet.
    """
    real = os.path.realpath(path)
    root = os.path.realpath(ROOT)
    return os.path.relpath(real, root) if real.startswith(root + os.sep) else real


def render_card(post_path: str, outdir: str) -> dict:
    out = subprocess.run(
        [sys.executable, CARD_SCRIPT, "--post", post_path,
         "--outdir", os.path.join(outdir, "cards"), "--json"],
        capture_output=True, text=True, check=False)
    if out.returncode != 0:
        return {}
    try:
        return json.loads(out.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return {}


def record_in_ledger(slug: str, record: dict, ledger_path: str = LEDGER) -> bool:
    if not os.path.isfile(ledger_path):
        return False
    try:
        with open(ledger_path, encoding="utf-8") as fh:
            entries = json.load(fh)
    except (OSError, ValueError):
        return False
    hit = False
    for entry in entries:
        if entry.get("slug") == slug:
            entry["image"] = record
            hit = True
    if not hit:
        return False
    tmp = f"{ledger_path}.tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(entries, fh, indent=2)
        fh.write("\n")
    os.replace(tmp, ledger_path)
    return True


# --------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--post", required=True, help="Path to the landed Hugo post")
    ap.add_argument("--provider", default=os.environ.get("IMAGE_PROVIDER", "minimax"))
    ap.add_argument("--outdir", default=DEFAULT_OUTDIR)
    ap.add_argument("--prompt-only", action="store_true",
                    help="Build and print the prompt; generate nothing, spend nothing")
    ap.add_argument("--no-llm", action="store_true",
                    help="Skip the scene step; use the deterministic metaphor")
    ap.add_argument("--model",
                    help="Override the seeded model pick (for regenerating a bad "
                         "image or comparing models on one prompt)")
    ap.add_argument("--ledger", action="store_true",
                    help="Write the result into .blog-syndication-ledger.json")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.post):
        print(f"no such post: {args.post}", file=sys.stderr)
        return 2

    post = read_post(args.post)
    slug = post["slug"]

    scene, scene_source = "", "deterministic"
    if not args.no_llm:
        candidate = llm_scene(post)
        if candidate:
            bad = scene_violations(candidate)
            if bad:
                print(f"scene rejected ({'; '.join(bad)}); using deterministic scene",
                      file=sys.stderr)
            else:
                scene, scene_source = candidate, "llm"
    if not scene:
        scene = deterministic_scene(post)

    try:
        prompt = build_prompt(scene)
    except ValueError as e:
        # The deterministic scene is safe by construction, so reaching here means
        # the guard itself is broken. Fail loudly rather than spend on a bad prompt.
        print(f"prompt guard rejected the scene: {e}", file=sys.stderr)
        return 2

    if args.prompt_only:
        print(prompt)
        return 0

    os.makedirs(args.outdir, exist_ok=True)
    result = {"slug": slug, "scene_source": scene_source, "prompt": prompt}

    try:
        provider = resolve_provider(args.provider)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 2
    allowed = getattr(provider, "all_models", provider.models)
    if args.model and args.model not in allowed:
        print(f"model {args.model!r} not exposed by {provider.name}; "
              f"known: {allowed}", file=sys.stderr)
        return 2
    model = args.model or pick_model(slug, provider.models)
    result.update(provider=provider.name, model=model)

    image_path = os.path.join(args.outdir, f"{slug}.png")
    last_error = ""
    for attempt in (1, 2):
        try:
            data = provider.generate(prompt, model)
            with open(image_path, "wb") as fh:
                fh.write(data)
            result.update(image=repo_rel(image_path), fallback=False)
            break
        except Exception as e:  # noqa: BLE001 - any vendor failure falls back
            last_error = f"{type(e).__name__}: {e}"
            print(f"generation attempt {attempt} failed: {last_error}", file=sys.stderr)
    else:
        result.update(image=None, fallback=True, error=last_error)
        print("falling back to the deterministic card", file=sys.stderr)

    cards = render_card(args.post, args.outdir)
    if cards:
        result["cards"] = {k: repo_rel(v) for k, v in cards.items()}

    if args.ledger:
        result["ledger_written"] = record_in_ledger(slug, result)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{'CARD FALLBACK' if result.get('fallback') else 'IMAGE'}: "
              f"{result.get('image') or result.get('cards', {}).get('og', 'none')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
