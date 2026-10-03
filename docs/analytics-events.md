# Site action events and native metrics

What startaitools.com records beyond pageviews, what each signal proves, and what it
does not. Beads `startaitools-bhn.11` (site events, duplicate hosts) and
`startaitools-bhn.12` (platform-native metrics); cluster issue #111. Evidence base:
intent-os `000-docs/226g` §7–8, §10 and `226h` §1–2.

## 1. Collection scope

The Umami tag in `layouts/partials/header.html` carries
`data-domains="startaitools.com,www.startaitools.com"`. The tracker still loads everywhere,
but it records only when `location.hostname` is exactly one of those two hosts. Before this change Umami was recording `startaitools.netlify.app`,
`deploy-preview-*--startaitools.netlify.app`, `www.startaitools.com` and a
`translate.goog` proxy into the production website.

Consequences, all intended:

- Netlify deploy previews, the default Netlify host and `hugo server` record nothing.
- `www.startaitools.com` still records, because it still serves pages (200) until the
  Caddy redirect in §4 is applied. Two `www.` sessions were observed in five months, so
  the host mix is negligible. **Once the redirect is live, narrow the tag to
  `data-domains="startaitools.com"`** and update the two assertions in
  `tests/test_site_events.py`.

## 2. Event catalogue

Two kinds of event, and they must not be reported as the same thing.

**Attempts (`*_click`).** A visitor pressed something. Nothing about the result is known.

| Event | Where | Properties | Proves | Does not prove |
|---|---|---|---|---|
| `outbound_click` | any link to another host (post bodies, footer, CTA) | `dest` = `tonsofskills` \| `intentsolutions` \| `github` \| `support` \| `other`; `host` | the visitor clicked a link leaving the site | that the destination loaded, or anything that happened there |
| `email_click` | any `mailto:` link | none | the visitor opened a mail client handoff | that an email was sent |
| `subscribe_click` | footer Subscribe button | `form` | a subscribe attempt (fires on invalid input too, and on Enter in the field) | a subscription |
| `contact_submit_click` | end-of-post CTA button, `/contact/` Send button | `form` = `startaitools-post-cta` \| `startaitools-contact` | a contact attempt | a lead |
| `work_with_us_click` | header "Work with us" | `location` | intent to view the contact page | a contact attempt |
| `support_widget_click` | Ko-fi floating widget | `provider` = `kofi` | focus moved into the widget iframe (heuristic, at most once per page view) | a payment, or even an opened checkout |

The site carries a Ko-fi widget, not Buy Me a Coffee. Ko-fi draws its button inside an
iframe, so a click never reaches the page; the event fires when the window loses focus
to that iframe. Ko-fi's own dashboard is the authority for supporters.

**Server-acknowledged outcomes (`*_accepted`).** Fired from `assets/js/main.js` only when
the shared forms-api answers 2xx.

| Event | Properties | Proves | Does not prove |
|---|---|---|---|
| `subscribe_accepted` | `form` | forms-api accepted a well-formed email for the list | a confirmed subscriber (there is no double opt-in), delivery, or a later open |
| `contact_accepted` | `form` | forms-api accepted the message (it then goes to Slack) | that anyone read or answered it |

Report rates as `accepted / click` per form, and never sum attempts with outcomes.

`/subscribe-success/` is **not** part of the current flow: the footer form posts with
`fetch` and never navigates there (one pageview in five months). Do not use its pageviews
as a confirmation signal.

## 3. How it is built

- Template-owned controls carry static `data-umami-event*` attributes.
- `assets/js/measure.js` (bundled with `main.js`, about 1 KB minified, no third-party
  code) labels every other external or `mailto:` link at load time. Umami's own click
  handler reads the attributes at click time and delays same-tab navigation until the
  event is sent. Links that already carry an event are left alone.
- Known gap: labelling runs once, at load. An external link injected later is not
  labelled. Today nothing on the site injects one: Pagefind search results link only to
  pages on this site (which are never labelled), and the Ko-fi button is an iframe
  handled by the focus heuristic. Revisit if a script that injects outbound links is
  added.
- Tests: `tests/test_site_events.py` (source, built HTML, and the classifier executed
  under node).

## 4. Duplicate hosts

Checked read-only with `curl -sI` on 2026-10-03:

| Host | Before | Owner of the config | Action |
|---|---|---|---|
| `startaitools.netlify.app` | 200, served by Netlify | this repo (`netlify.toml`) | 301 to `https://startaitools.com/:splat`, host-scoped (in this change). Takes effect on Netlify's next build of `master`. Previews and a DNS rollback (custom host) are unaffected. |
| `www.startaitools.com` | 200, served by Caddy on the VPS (`http://` gives 308 to `https://www.`) | intent-os `ops/deploy/startaitools/Caddyfile.fragment` | **owner approval needed**, not changed here |

Proposed Caddy change (for owner approval; edit the intent-os fragment, then
`caddy validate` and `systemctl reload caddy`, never restart):

```caddyfile
# was: startaitools.com, www.startaitools.com {
startaitools.com {
	# ... existing block unchanged ...
}

www.startaitools.com {
	redir https://startaitools.com{uri} 308
}
```

Verify afterwards: `curl -sI https://www.startaitools.com/posts/x/` returns 308 with
`location: https://startaitools.com/posts/x/`.

## 5. Platform-native metrics (Layer A)

`scripts/blog/native-metrics-devto.py` is a read-only collector. It calls
`GET https://dev.to/api/articles/me/published` with the existing `DEVTO_API_KEY`
(environment first, then the parent `blog/.env` line that `post-to-devto.sh` already
uses; the key is never printed) and appends one observation per article to
`.native-metrics.jsonl` (gitignored):

```json
{"surface": "devto", "status": "ok", "article_id": 1, "url": "...", "canonical_url": "...",
 "published_at": "...", "page_views": 412, "reactions": 7, "comments": 2,
 "observed_at": "2026-10-03T12:00:00Z", "source": "devto_api"}
```

- Counts are cumulative lifetime numbers; consumers take deltas between observations.
- A missing key, 401/403, 5xx, network error or malformed body writes **one** status row
  (`unavailable` or `auth_failed`) and no article rows. A missing field is `null`.
  Neither is ever written as zero.
- Each run also appends one status row per surface without a collector:

| Surface | Status | Why |
|---|---|---|
| Hashnode | `paid_api` | post views need the Pro API |
| Substack | `unavailable_without_dashboard` | no stats API; views, opens and subscribers are dashboard-only |
| Medium | `unavailable_without_dashboard` | API exposes no stats |
| LinkedIn company | `unavailable_without_dashboard` | Marketing API approval required |
| LinkedIn personal | `unavailable_without_dashboard` | no member post analytics API |
| X | `unavailable_without_dashboard` | metrics need a paid API tier, not provisioned |

- **One observation per UTC day.** Before calling Dev.to the collector reads the log; if it
  already holds a Dev.to `ok` (or `ok_empty`) row observed on the current UTC date, the run
  writes nothing, logs `skip:` to stderr and exits 0. A day whose only rows are
  `unavailable`/`auth_failed` is retried on the next run. `--force` writes a second
  observation anyway; consumers should still key on (`surface`, `article_id`, date of
  `observed_at`) and keep the latest row if a forced run exists.

`--list-surfaces` prints the registry; `--dry-run` collects without writing.

**Proposed schedule (not installed):** daily 06:15, after the 05:30 crosspost sweep and
before the 06:30 analytics brief:

```cron
15 6 * * * /home/jeremy/000-projects/blog/startaitools/scripts/blog/native-metrics-devto.py
```

Dev.to page views are Dev.to's own count of views on Dev.to. They are not comparable with
Umami sessions or with any other platform's impressions.
