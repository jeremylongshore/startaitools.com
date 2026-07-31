# Runbook — startaitools.com Netlify → Contabo VPS migration

**Status (2026-07-31):** VPS checkout, pinned Hugo build, command-restricted deploy, and validated Caddy vhost are staged. DNS still points to Netlify until the corrected content/workflow change lands. The repo-scoped Tailscale workload identity remains blocked by the rejected administrative API credential; do not weaken SSH to work around it.

**Migrating to mirror jeremylongshore.com**, which already lives on the VPS at `100.88.144.55` / `167.86.106.29`. Consolidated hosting = single ingress via Caddy, no remaining Netlify dependency.

---

## Pre-migration checklist

- [x] **GH Actions deploy workflow in place** — `.github/workflows/deploy.yml` calls the shared `jeremylongshore/.github/.github/workflows/vps-deploy.yml@53d6be37…` reusable workflow. Variable inputs match the canonical pattern: `variant=static`, `srv-path=/srv/startaitools`, `health-check-url=https://startaitools.com/healthz`. (Verified against `jeremylongshore.com` PR #11 + #15.)
- [x] **Build command reproducible** — `hugo --buildFuture --gc --minify --cleanDestinationDir` (no Pagefind on this build; the post corpus doesn't use full-text search).
- [x] **Hugo version pinned** — `0.150.0` (matches `netlify.toml` HUGO_VERSION, also matches what jeremylongshore.com tested)
- [x] **Submodules** — `themes/archie` is the only submodule (`.gitmodules`); recursive fetch is on.
- [x] **Caddy vhost** on VPS — canonical source is `intent-os/ops/deploy/startaitools/Caddyfile.fragment`
- [ ] **DNS cutover at Porkbun** — see step 2
- [ ] **netlify.toml removal** — see step 3
- [x] **Static file_server setup at /srv/startaitools/dist** — see step 0
- [ ] **Health-check endpoint** — `/healthz` route, see step 1
- [ ] **Verify** — see step 4

---

## Step 0: Prepare the VPS filesystem

```bash
ssh intentsolutions sudo mkdir -p /srv/startaitools /srv/startaitools/dist
ssh intentsolutions sudo chown -R intentsolutions:intentsolutions /srv/startaitools
```

The reusable workflow expects `srv-path` to exist and to be writable by the SSH user. The reviewed force-command builds with pinned Hugo 0.150.0 into a fresh temporary directory, then rsyncs it into `srv-path/dist/`. Canonical deploy assets live in `intent-os/ops/deploy/startaitools/`.

## Step 1: Caddy vhost (single-server block, mirrors jeremylongshore.com)

Install the byte-reviewed fragment from `intent-os/ops/deploy/startaitools/Caddyfile.fragment`. It includes the JSON health response required by the workflow, all six legacy redirects, the forms reverse proxy without a duplicated path, cache headers, and the static root at `/srv/startaitools/dist`. Intent OS is the authority; do not maintain a second copy of the block in this runbook.

Then validate + reload Caddy:

```bash
ssh intentsolutions sudo caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
ssh intentsolutions sudo systemctl reload caddy
ssh intentsolutions sudo systemctl status caddy
```

**Strict-gate:** Caddy MUST validate before reload. If `caddy validate` fails, do NOT reload — fix the syntax first. The intent-os runbook `ops/host/security-baseline.md` covers the reload discipline.

## Step 2: DNS cutover at Porkbun

The site currently resolves to `75.2.60.5` (Netlify anycast). Cutover steps:

```bash
# Read current records first — verify the carve-out
ssh intentsolutions "dig +short startaitools.com @8.8.8.8"
# Should return 75.2.60.5 (Netlify) before cutover

# Update A record at Porkbun (API call via intent-mail helper)
bash /home/jeremy/000-projects/intent-os/ops/dns/porkbun-update-record.sh \
  startaitools.com edit A '' 167.86.106.29 10 600

# Replace the Netlify CNAME with a VPS A record. The delete is explicit because
# DNS forbids a CNAME and A record at the same owner name.
bash /home/jeremy/000-projects/intent-os/ops/dns/porkbun-update-record.sh \
  startaitools.com delete CNAME www startaitools.netlify.app
bash /home/jeremy/000-projects/intent-os/ops/dns/porkbun-update-record.sh \
  startaitools.com create A www 167.86.106.29 10 600
```

Set TTL to **600 seconds (10 min)** before cutover. After 24h, drop back to 3600.

**Verification window:**
1. `dig +short startaitools.com @8.8.8.8` → should resolve to 167.86.106.29 within 10 min
2. `curl -sI https://startaitools.com/` → should return the VPS's TLS cert (Caddy)
3. Read Caddy's system journal; this vhost does not create an ungoverned file-log exception.

**Sticky-client issue:** some resolvers cache Netlify's old 75.2.60.5 longer than the 10-min TTL thanks to CDN-based caching. If a client fails to resolve to the VPS within 30 min, suspect resolver cache, not the cutover itself.

## Step 3: Remove the Netlify fallback

After step 2 has been verified for ≥48h with no broken edge cases:

```bash
cd /home/jeremy/000-projects/blog/startaitools
git rm netlify.toml
# Also delete the Netlify-side firewall/proxy config at app.netlify.com
# (manual, not in this repo)
git add -A
git commit -m "chore: remove netlify.toml after VPS migration"
git push origin master
```

**Critical:** the `static/_redirects` file contains 6 legacy Netlify-style redirects. These need to be ported into the Caddyfile (or kept as a separate Caddy subdirective) BEFORE removing `static/_redirects`. Step 1 vhost only includes the `/api/forms/*` proxy — it does NOT include the legacy path-level redirects:

```
/en/blogs/*   /posts/:splat  301
/blogs/*      /posts/:splat  301
/projects/*   /posts/        301
/skills       /about         301
/resume       /about         301
/startai/*    /posts/startai/:splat  301
```

The reviewed Intent OS fragment already ports these redirects with named capture groups. Verify each route against Caddy before removing `static/_redirects`; do not translate the Netlify splat syntax ad hoc.

## Step 4: End-to-end verification

```bash
# Smoke
curl -sI https://startaitools.com/healthz
# → 200 OK

# Content smoke (random 5 posts from the corpus)
for slug in $(ls content/posts | head -5); do
  curl -sI "https://startaitools.com/posts/${slug%.md}/" | head -1
done
# → all 200 OK

# Forms API proxy (path rewriting through tonsofskills.com / VPS)
curl -sI https://startaitools.com/api/forms/contact
# → 200 or 405 — never 404

# Cache headers
curl -sI https://startaitools.com/posts/ | grep -i 'cache-control'
# → no-cache, no-store, must-revalidate

curl -sI https://startaitools.com/css/custom.min.*.css | grep -i 'cache-control'
# → public, max-age=300, must-revalidate (matches Netlify semantics)

# DNS
dig +short startaitools.com @1.1.1.1
# → 167.86.106.29
```

## Step 5: Update docs

After cutover:

- startaitools.com/CLAUDE.md § "Cloud Platform" — change `startaitools.com → 75.2.60.5 (Netlify)` to `startaitools.com → 167.86.106.29 (Contabo VPS)`.
- `~/000-projects/blog/CLAUDE.md` ditto.
- The "still served by Netlify" notes in startaitools.com/CLAUDE.md (multiple places) all need updating.

## Rollback

If the cutover goes sideways and rollback is needed within the 10-min TTL window:

```bash
# Revert DNS at Porkbun to Netlify (instant — that's the point of 600s TTL)
bash /home/jeremy/000-projects/intent-os/ops/dns/porkbun-update-record.sh \
  startaitools.com edit A '' 75.2.60.5 10 600
bash /home/jeremy/000-projects/intent-os/ops/dns/porkbun-update-record.sh \
  startaitools.com delete A www 167.86.106.29
bash /home/jeremy/000-projects/intent-os/ops/dns/porkbun-update-record.sh \
  startaitools.com create CNAME www startaitools.netlify.app 10 600
```

Because the deploy.yml DOESN'T delete Netlify config (we keep `netlify.toml` until step 3), Netlify still serves the site from the existing branch — instant rollback. After Netlify is decommissioned (step 3+), rollback requires re-pointing Porkbun to wherever the next host lives.

---

## Acceptance criteria mapping

| Bead criterion | Status |
|---|---|
| `dig +short startaitools.com` → `167.86.106.29` | ⏳ step 2 (Porkbun cutover) |
| push to master triggers VPS deploy, not Netlify | ⏳ step 2 (active deploy.yml fires once Caddy vhost resolves the host) |
| HTML no-cache headers + 6 legacy redirects preserved | ⏳ step 3 (Caddy header matchers + legacy_* redir blocks in this runbook) |
| `netlify.toml` removed; docs updated to VPS | ⏳ step 3 + step 5 |
| blogs pipeline 45s liveness window post-push | ✅ Netlify 45s post-push → VPS should match (verify in step 4) |

Files changed by this PR (deploy.yml + this runbook) are not enough on their own — VPS-side Caddy config + Porkbun DNS cutover are operator actions.
