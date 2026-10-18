"""Render qualitative suggestions with metric references resolved by code.

The model supplies JSON, never HTML or numeric measurements. Evidence lines carry
their own population, period, tier and unit. Unknown references and numeric prose
refuse the report before delivery. This verifies numbers, not the merits of advice.
"""
import argparse
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

NUMBER_WORDS = re.compile(
    r"\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|"
    r"forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion|"
    r"percent|percentage|double|doubled|triple|tripled|half|quarter|dozen)\b", re.I,
)


def prose(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 1000:
        raise ValueError("expected nonempty prose of at most 1000 characters")
    if any(c.isnumeric() for c in value) or NUMBER_WORDS.search(value) or "%" in value:
        raise ValueError("numeric prose is not allowed; use a metric reference")
    if any(c in value for c in "<>{}"):
        raise ValueError("prose must be plain text")
    return escape(value.strip())


def count(value):
    if type(value) is not int or value < 0:
        raise ValueError("invalid verified metric")
    return value


def catalog(data):
    """Stable keys -> complete, inseparable evidence labels; unavailable != zero."""
    result = {}
    sites = data["sites"]
    if not sites:
        raise ValueError("empty site population")
    for row in sites:
        for period in ("week", "prior_week"):
            tier = row.get("filtered", {}).get(period)
            if tier and "unavailable" not in tier:
                raw = row["periods"][period]
                if (count(tier["visitors_raw"]) != count(raw["visitors"])
                        or count(tier["pageviews_raw"]) != count(raw["pageviews"])):
                    raise ValueError("filtered and raw populations disagree")
                if any(count(tier[m]) > count(raw[m]) for m in ("visitors", "pageviews")):
                    raise ValueError("filtered counts exceed raw population")
    cohort = data["fixed_cohort"]
    domains = cohort["domains"]
    if not domains:
        raise ValueError("empty fixed cohort")
    members = [r for r in sites if r["domain"] in domains]
    if len(members) != len(domains) or len({r["domain"] for r in sites}) != len(sites):
        raise ValueError("missing or duplicate cohort/site rows")
    groups = [("fixed", cohort.get("name", "fixed cohort"), members)]
    groups += [(r["domain"], r["domain"], [r]) for r in sites]
    for key, label, rows in groups:
        for period in ("week", "prior_week"):
            for tier in ("raw", "filtered"):
                values = [r["periods"][period] if tier == "raw"
                          else r.get("filtered", {}).get(period) for r in rows]
                prefix = f"{label}; {period.replace('_', ' ')}; {tier}"
                if any(not v or "unavailable" in v for v in values):
                    text = "measurement unavailable (not zero)"
                else:
                    sessions = sum(count(v["visitors"]) for v in values)
                    views = sum(count(v["pageviews"]) for v in values)
                    text = f"{sessions:,} sessions; {views:,} pageviews"
                result[f"{key}/{period}/{tier}"] = f"{prefix}: {text}."
    for row in sites:
        for period, referrals in row.get("referrals", {}).items():
            if period not in ("week", "prior_week"):
                continue
            for ref in referrals:
                for kind in ("tagged", "any"):
                    prefix = (f"{row['domain']}; {period.replace('_', ' ')}; "
                              f"{ref['surface']}; {kind} arrivals")
                    raw = ref.get(f"{kind}_raw")
                    filtered = ref.get(f"{kind}_filtered")
                    if ref["status"] != "ok":
                        value = "unavailable (query failed; not zero)"
                    elif not ref["tagged"] and (kind == "tagged" or raw == 0):
                        value = "untagged - unmeasurable"
                    else:
                        head = "unavailable" if filtered is None else f"{count(filtered):,}"
                        value = f"{head} filtered sessions; {count(raw):,} raw sessions"
                    key = f"{row['domain']}/{period}/referral/{ref['surface']}/{kind}"
                    result[key] = f"{prefix}: {value}."
    return result


def keys(value, expected):
    if not isinstance(value, dict) or set(value) != set(expected):
        raise ValueError("unexpected narrative fields")


def render(draft, evidence):
    keys(draft, ("interpretation", "referrals", "evergreen", "actions"))

    def section(title, items, minimum, maximum):
        if not isinstance(items, list) or not minimum <= len(items) <= maximum:
            raise ValueError("invalid narrative section length")
        html = f"<h3>{title}</h3>"
        for item in items:
            keys(item, ("text", "evidence"))
            text = prose(item["text"])
            refs = item["evidence"]
            if not isinstance(refs, list) or not 1 <= len(refs) <= 4:
                raise ValueError("each suggestion needs verified evidence")
            if any(not isinstance(r, str) or r not in evidence for r in refs):
                raise ValueError("unknown metric reference")
            html += f"<p>{text}</p><ul>" + "".join(
                f"<li>{escape(evidence[r])}</li>" for r in refs) + "</ul>"
        return html

    html = ('<div style="font-family:Arial,sans-serif;color:#17253b">'
            '<h2>Interpretation and next actions</h2>')
    html += ('<p>Suggestions are model-written; the labeled evidence below '
             'is rendered from verified metrics. Filtering removes suspected '
             'automation; it does not identify verified human visitors.</p>')
    html += section("Interpretation", draft["interpretation"], 1, 3)
    html += section("Referral arrivals", draft["referrals"], 1, 3)
    evergreen = draft["evergreen"]
    keys(evergreen, ("url", "angle"))
    url = evergreen["url"]
    if not isinstance(url, str) or any(c.isspace() for c in url):
        raise ValueError("invalid evergreen URL")
    parts = urlsplit(url)
    if (parts.scheme != "https" or parts.netloc != "startaitools.com"
            or not parts.path.startswith("/posts/") or parts.path == "/posts/"
            or parts.query or parts.fragment or any(c in url for c in '<>"\\')):
        raise ValueError("evergreen must link directly to a StartAI Tools post")
    html += '<h3>Evergreen re-share nomination</h3>'
    html += f'<p><a href="{escape(url, quote=True)}">Read the nominated post</a></p>'
    html += f'<p>{prose(evergreen["angle"])}</p>'
    html += section("Amplify these", draft["actions"], 2, 3)
    return html + "</div>"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--draft")
    args = parser.parse_args()
    try:
        evidence = catalog(json.loads(Path(args.metrics).read_text()))
        output = (render(json.loads(Path(args.draft).read_text()), evidence) if args.draft
                  else json.dumps(evidence, indent=2))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        reason = (str(exc) if type(exc) is ValueError else type(exc).__name__)
        parser.exit(1, f"Narrative validation failed: {reason}; no report rendered\n")
    Path(args.out).write_text(output)


if __name__ == "__main__":
    main()
