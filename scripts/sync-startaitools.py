#!/usr/bin/env python3
import os, re, sys, hashlib, datetime, pathlib, shutil
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup

# ---------- CONFIG ----------
FEEDS = [
    # Edit or append additional feeds here
    "https://startaitools.com/index.xml",
]
DEST_DIR = pathlib.Path("content/posts/startai")
IMG_DIR  = pathlib.Path("static/images/startai")
AUTHOR   = "Jeremy Longshore"
CATEGORY = "AI"
TIMEOUT  = 30
# ----------------------------

DEST_DIR.mkdir(parents=True, exist_ok=True)
IMG_DIR.mkdir(parents=True, exist_ok=True)

def slugify(s):
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE).strip().lower()
    s = re.sub(r"[\s_-]+", "-", s)
    return s[:80] if s else hashlib.sha1(s.encode()).hexdigest()[:12]

def fetch(url):
    r = requests.get(url, timeout=TIMEOUT, headers={"User-Agent":"SyncStartAITools/1.0"})
    r.raise_for_status()
    return r.text

def download_image(src_url):
    try:
        r = requests.get(src_url, timeout=TIMEOUT, stream=True, headers={"User-Agent":"SyncStartAITools/1.0"})
        r.raise_for_status()
        name = hashlib.sha1(src_url.encode()).hexdigest() + os.path.splitext(urlparse(src_url).path)[1][:6]
        out = IMG_DIR / name
        with open(out, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        return f"/images/startai/{name}"
    except Exception:
        return src_url  # fall back to remote

def html_to_markdown(html):
    # Minimal HTML → MD. Preserve code blocks. Keep links. Rewrite images.
    soup = BeautifulSoup(html, "html.parser")

    # Images → local copies
    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue
        img["src"] = download_image(src)

    # Convert simple tags to MD-ish text; leave complex HTML as-is inside fenced blocks if needed
    # Use a pragmatic approach: keep HTML, Hugo renders fine. Just ensure image URLs are updated.
    return str(soup)

def ensure_toml_safe(s):
    return s.replace('"', '\\"')

def write_post(item):
    title = item.get("title", "Untitled").strip()
    link  = item.get("link", "").strip()
    date  = item.get("pubDate") or item.get("updated") or item.get("dc:date") or ""
    iso   = ""
    if date:
        try:
            iso = datetime.datetime.fromisoformat(date.replace("Z","+00:00")).isoformat()
        except Exception:
            try:
                from email.utils import parsedate_to_datetime
                iso = parsedate_to_datetime(date).isoformat()
            except Exception:
                iso = datetime.datetime.utcnow().isoformat()

    slug = slugify(title) or slugify(link)
    md_path = DEST_DIR / f"{slug}.md"

    # Pull content
    content_html = item.get("content:encoded") or item.get("content") or item.get("description") or ""
    content_html = content_html.strip()

    body_md = html_to_markdown(content_html)
    # front matter (TOML)
    front = []
    front.append("+++")
    front.append(f'title = "{ensure_toml_safe(title)}"')
    front.append(f'date = "{iso}"')
    front.append('draft = false')
    front.append(f'author = "{AUTHOR}"')
    front.append(f'tags = ["start ai tools"]')
    front.append(f'categories = ["{CATEGORY}"]')
    front.append(f'canonical_url = "{link}"')
    # Keep old StartAI paths as aliases if structure known; safe default:
    # front.append(f'aliases = ["/startai/{slug}/"]')
    front.append("+++")
    front_matter = "\n".join(front)

    # Compose Hugo content
    md = f"{front_matter}\n\n{body_md}\n"

    # Write if new or changed
    old = md_path.read_text("utf-8") if md_path.exists() else ""
    if old != md:
        md_path.write_text(md, encoding="utf-8")
        return True
    return False

def parse_feed(xml_text):
    root = ET.fromstring(xml_text)
    ns = {"content":"http://purl.org/rss/1.0/modules/content/"}
    items = []
    # RSS
    for it in root.findall(".//item"):
        items.append({
            "title": (it.findtext("title") or "").strip(),
            "link": (it.findtext("link") or "").strip(),
            "pubDate": (it.findtext("pubDate") or "").strip(),
            "content:encoded": (it.findtext("content:encoded", namespaces=ns) or "").strip(),
            "description": (it.findtext("description") or "").strip(),
        })
    # Atom
    for it in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
        def g(tag): return it.findtext(f"{{http://www.w3.org/2005/Atom}}{tag}") or ""
        link_el = it.find("{http://www.w3.org/2005/Atom}link")
        link = link_el.get("href") if link_el is not None else ""
        items.append({
            "title": g("title").strip(),
            "link": link.strip(),
            "updated": g("updated").strip(),
            "content": (it.findtext("{http://www.w3.org/2005/Atom}content") or "").strip(),
            "description": (it.findtext("{http://www.w3.org/2005/Atom}summary") or "").strip(),
        })
    return items

def main():
    changed = 0
    for feed in FEEDS:
        try:
            xml = fetch(feed)
            for it in parse_feed(xml):
                if it.get("title") and it.get("link"):
                    if write_post(it):
                        changed += 1
        except Exception as e:
            print(f"[warn] feed failed: {feed}: {e}", file=sys.stderr)
    print(f"[sync] posts changed: {changed}")
    # Exit 0 even if none changed so CI passes
    sys.exit(0)

if __name__ == "__main__":
    main()