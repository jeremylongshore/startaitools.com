#!/usr/bin/env node
/*
 * blog-packet-html.cjs — render the Ezekiel posting-packet HTML from a JSON
 * payload. Reuses the proven "v3" layout (Gmail thread 19f1e4b93f9158cc):
 * greeting → live+canonical callout → "post it to N places" → before-posting
 * notes → Substack → Medium → X long-form article → X box → LinkedIn personal
 * (+first comment) → LinkedIn company (+first comment) → verbatim-disclaimer footer.
 *
 * Usage:
 *   node blog-packet-html.cjs < payload.json > packet.html
 *   node blog-packet-html.cjs --in payload.json --out packet.html
 *
 * Payload schema (all optional except post_title + canonical_url + destinations):
 * {
 *   "post_title": "...", "canonical_url": "https://startaitools.com/posts/slug/",
 *   "tier": 2, "date": "2026-07-05",
 *   "destinations": ["x","li_personal","li_company","substack","medium","x_article"],
 *   "before_notes": ["verbatim-required disclaimer/guardrail strings"],
 *   "links": { "x": "url?utm_source=x", "li_personal": "...", "li_company": "...",
 *              "x_article": "url?utm_source=x&utm_content=x_article",
 *              "substack_canonical": "bare-url", "medium_canonical": "bare-url" },
 *   "x_post": "raw text", "x_is_thread": false,
 *   "li_personal": "text", "li_personal_comment": "Deep-dive: ...\nCode: ...",
 *   "li_company": "text", "li_company_comment": "...",
 *   "substack_subtitle": "...", "footer": "disclaimer footer",
 *   "x_article_title": "...", "x_article_subtitle": "...",
 *   "hold": false, "hold_reason": ""
 * }
 */
'use strict';
const fs = require('fs');

function arg(name) {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] : null;
}
const inFile = arg('--in');
const outFile = arg('--out');
// --fragment: emit just this post's block (title callout → footer), no outer
// <div> wrapper and no "Ezekiel —" greeting. Used to merge N posts into one
// email on a multi-post backfill day.
const fragment = process.argv.includes('--fragment');
const raw = inFile ? fs.readFileSync(inFile, 'utf8') : fs.readFileSync(0, 'utf8');
const p = JSON.parse(raw);

const esc = (s) => String(s == null ? '' : s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
// Linkify bare URLs inside already-escaped text (for the plain body, not the
// <pre> boxes — those stay literal so Ezekiel copies exactly what posts).
const linkify = (escaped) => escaped.replace(
  /(https?:\/\/[^\s<)]+)(?![^<]*<\/a>)/g,
  '<a href="$1" target="_blank">$1</a>');

const dest = new Set(p.destinations || []);
const links = p.links || {};
const canonical = p.canonical_url;
const box = (txt) =>
  `<pre style="white-space:pre-wrap;word-break:break-word;border:1px solid #d0d7de;border-radius:6px;padding:12px;font-size:13px;font-family:ui-monospace,Menlo,Consolas,monospace">${esc(txt)}</pre>`;

// A destination was requested but its copy came back empty. Previously the
// `dest.has(x) && p.x_post` guard made the whole section vanish, so an empty
// li_personal silently deleted Post #2 from the packet: the numbered checklist
// above still said "post it to 3 places" and only two boxes existed. Ezekiel had
// no way to tell a dropped section from a section that was never meant to be
// there. Degrade loudly instead: keep the section, say what is missing.
const degradedBox = (what) =>
  `<div style="border:2px dashed #b54708;background:#fffaf0;border-radius:6px;padding:12px">
    <strong style="color:#b54708">⚠ COPY MISSING — write this one manually</strong>
    <p style="margin:6px 0 0;font-size:14px">The pipeline produced no ${esc(what)} copy for this post. Everything else in this packet is good; write this box from the article and post it as normal. If this keeps happening, tell Jeremy.</p>
  </div>`;

let out = [];
if (!fragment) {
  out.push(`<div style="font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;font-size:15px;line-height:1.55;color:#1a1a1a;max-width:720px">`);
}

if (p.hold) {
  out.push(`<div style="border:2px solid #b42318;background:#fff4f2;border-radius:8px;padding:14px;margin-bottom:16px">
    <strong style="color:#b42318;font-size:16px">⛔ HOLD — DO NOT POST YET</strong>
    <p style="margin:6px 0 0">${esc(p.hold_reason || 'A required disclaimer is not approved for this post. Jeremy must approve wording before this goes out.')}</p>
  </div>`);
}

if (!fragment) out.push(`<p>Ezekiel —</p>`);
out.push(`<p>The article <strong>&quot;${esc(p.post_title)}&quot;</strong> is <strong>live and canonical</strong> here:</p>`);
out.push(`<p style="font-size:16px">👉 <a href="${esc(canonical)}" target="_blank"><strong>${esc(canonical)}</strong></a></p>`);

// Build the destination checklist (tier-conditional).
const items = [];
if (dest.has('substack')) items.push(`<strong>Substack</strong> — the long-form article (steps below).`);
if (dest.has('medium')) items.push(`<strong>Medium</strong> — the long-form article, via Import (steps below).`);
if (dest.has('x_article')) items.push(`<strong>X — long-form article</strong> — the whole piece as an X article (steps below).`);
if (dest.has('buymeacoffee')) items.push(`<strong>Buy Me a Coffee</strong> — the whole piece as a public supporter post (steps below).`);
if (dest.has('x')) items.push(`<strong>X / Twitter</strong> — Post #1${p.x_is_thread ? ' (thread)' : ''}.`);
if (dest.has('li_personal')) items.push(`<strong>LinkedIn — Jeremy&#39;s personal profile</strong> — Post #2 (+ first comment).`);
if (dest.has('li_company')) items.push(`<strong>LinkedIn — Intent Solutions company page</strong> — Post #3 (post natively; + first comment).`);
out.push(`<p>Post it to <strong>${items.length}</strong> place${items.length === 1 ? '' : 's'}. Every deep-dive link below is already the live URL, UTM-tagged per platform — no placeholders to swap.</p>`);
out.push(`<ol>${items.map((x) => `<li>${x}</li>`).join('')}</ol>`);

// Image to attach. Ezekiel posts image plus text; a post that goes out bare gets
// materially less reach, so the packet names the files rather than assuming he
// will go looking. `generated` is the per-post art, `card_*` the deterministic
// brand card that always exists as a floor.
const media = p.media || {};
if (media.generated || media.card_og || media.card_square) {
  out.push(`<hr><h2>Image — attach one of these</h2>`);
  // Render as real links so Ezekiel can open and save each one from the email.
  // A bare path was useless to him: he is not on the machine that made the file.
  const media_item = (label, note, target) => target && /^https?:\/\//.test(target)
    ? `<li><strong>${label}</strong> ${note}: <a href="${esc(target)}" target="_blank">${esc(target)}</a></li>`
    : `<li><strong>${label}</strong> ${note}: <code>${esc(target)}</code> (local file, ask Jeremy)</li>`;
  const rows = [];
  if (media.generated) {
    rows.push(media_item('Generated art', '(preferred, made for this post)', media.generated));
  }
  if (media.card_og) {
    rows.push(media_item('Brand card, landscape 1200x630', '(X and LinkedIn link preview)', media.card_og));
  }
  if (media.card_square) {
    rows.push(media_item('Brand card, square 1080x1080', '(in-feed)', media.card_square));
  }
  out.push(`<ul>${rows.join('')}</ul>`);
  if (media.generated_failed) {
    out.push(`<p style="color:#b54708"><em>Image generation failed for this post, so only the brand card is available. That is expected to be rare; if it repeats, tell Jeremy.</em></p>`);
  }
  out.push(`<p style="color:#666;font-size:13px">Attach the image natively on each platform (upload the file). Do not paste a link to it.</p>`);
}

// Before-posting notes (verbatim-required disclaimers/guardrails).
const notes = p.before_notes || [];
if (notes.length) {
  out.push(`<p><strong>Before posting — include these VERBATIM (do not edit or omit):</strong></p>`);
  out.push(`<ul>${notes.map((n) => `<li>${esc(n)}</li>`).join('')}</ul>`);
}

// Substack (tier 2+).
if (dest.has('substack')) {
  out.push(`<hr><h2>Substack (long-form)</h2>`);
  out.push(`<ol>
    <li>Open the live article: ${linkify(esc(canonical))}</li>
    <li>Select the whole body (first paragraph through the References) and copy it — Substack keeps headings, links, and bold on paste.</li>
    <li>New Substack post → paste. Title: <strong>${esc(p.post_title)}</strong>.${p.substack_subtitle ? ` Subtitle: <em>${esc(p.substack_subtitle)}</em>.` : ''}</li>
    <li><strong>SEO — set the canonical.</strong> In <strong>Settings → Canonical URL</strong>, paste this EXACTLY so the syndicated copy doesn&#39;t outrank the original:</li>
  </ol>`);
  out.push(box(links.substack_canonical || canonical));
}

// Medium (tier 2+).
if (dest.has('medium')) {
  out.push(`<hr><h2>Medium (long-form) — easiest via Import</h2>`);
  out.push(`<ol>
    <li>Medium: avatar → <strong>Write</strong> → <strong>⋯</strong> → <strong>Import a story</strong> (or <a href="https://medium.com/p/import" target="_blank">medium.com/p/import</a>).</li>
    <li>Paste ${linkify(esc(canonical))} → <strong>Import</strong>. Medium pulls in the article <strong>and sets the canonical automatically</strong>.</li>
    <li>Review formatting, then Publish. If Import misbehaves: copy-paste from the live page, then set the canonical under <strong>⋯ → Settings → Advanced → Customize canonical link</strong> to exactly:</li>
  </ol>`);
  out.push(box(links.medium_canonical || canonical));
}

// X long-form article (tier 2+). Modelled on the Substack block, with one honest
// difference: Substack and Medium both let you declare a canonical, and an X article
// does not. There is no way to tell a search engine the blog is the original, so the
// link back is the only mitigation and the packet says that out loud rather than
// implying parity with the other two long-form destinations.
//
// The model writes only the title and subtitle here, because the body is the published
// article verbatim. A missing title still renders the section, loudly, for the same
// reason every other destination does.
if (dest.has('x_article')) {
  out.push(`<hr><h2>X (long-form article)</h2>`);
  if (p.x_article_title) {
    out.push(`<ol>
      <li>Open the live article: ${linkify(esc(canonical))}</li>
      <li>Select the whole body and copy it, then paste it into the X article composer (Post → the article option).</li>
      <li>Title: <strong>${esc(p.x_article_title)}</strong>.${p.x_article_subtitle ? ` Subtitle: <em>${esc(p.x_article_subtitle)}</em>.` : ''}</li>
    </ol>`);
  } else {
    out.push(degradedBox('X long-form article title'));
    out.push(`<p>The rest of this destination still stands: open ${linkify(esc(canonical))}, copy the whole body into the X article composer, and write your own title.</p>`);
  }
  out.push(`<p><strong>Put this link in the FIRST paragraph and again at the end:</strong></p>`);
  out.push(box(links.x_article || canonical));
  out.push(`<p style="color:#666;font-size:13px"><em>This one is a reach play, not an SEO-neutral syndication. Substack and Medium set a canonical tag and an X article cannot, so that link back is the only thing pointing at the original.</em></p>`);
}

// Buy Me a Coffee (tier 2+). Ezekiel has credentials. Same long-form republication
// shape as Substack, with two differences worth stating in the packet rather than
// leaving him to guess:
//   1. Visibility is PUBLIC, not supporters-only. The point of this surface here is
//      reach and a link back, not a paid perk. If Jeremy ever wants it gated, that
//      is a deliberate change, not a default to drift into.
//   2. Like the X article and unlike Substack and Medium, there is no canonical tag,
//      so the link back is doing all the SEO work.
if (dest.has('buymeacoffee')) {
  out.push(`<hr><h2>Buy Me a Coffee (supporter post)</h2>`);
  out.push(`<ol>
    <li>Open the live article: ${linkify(esc(canonical))}</li>
    <li>Buy Me a Coffee → <strong>Posts</strong> → new post. Select the whole article body and paste it in.</li>
    <li>Title: <strong>${esc(p.post_title)}</strong>.</li>
    <li><strong>Visibility: Public.</strong> Not supporters-only. This one is for reach; if that ever changes Jeremy will say so.</li>
  </ol>`);
  out.push(`<p><strong>Open with this line</strong> (it is written for the people who already back the work, so keep it as-is):</p>`);
  out.push(p.bmc_note ? box(p.bmc_note) : degradedBox('Buy Me a Coffee supporter note'));
  out.push(`<p><strong>Then put this link in the first paragraph and again at the end:</strong></p>`);
  out.push(box(links.buymeacoffee || canonical));
  out.push(`<p style="color:#666;font-size:13px"><em>No canonical tag here either, same as the X article. The link back is the only thing pointing at the original.</em></p>`);
}

// X post. A requested destination always renders a section: real copy when we
// have it, a loud degraded box when we do not. Never a silent omission.
if (dest.has('x')) {
  out.push(`<hr><h2>Post #1 — X / Twitter${p.x_is_thread ? ' (thread — post in order)' : ''}</h2>`);
  out.push(p.x_post ? box(p.x_post) : degradedBox('X / Twitter'));
}

// LinkedIn personal.
if (dest.has('li_personal')) {
  out.push(`<hr><h2>Post #2 — LinkedIn (Jeremy&#39;s personal profile)</h2>`);
  out.push(p.li_personal ? box(p.li_personal) : degradedBox('LinkedIn personal'));
  if (p.li_personal_comment) {
    out.push(`<p><strong>First comment</strong> (post the links UNDER the post so they don&#39;t suppress reach):</p>`);
    out.push(box(p.li_personal_comment));
  }
}

// LinkedIn company.
if (dest.has('li_company')) {
  out.push(`<hr><h2>Post #3 — LinkedIn (Intent Solutions company page — post natively)</h2>`);
  out.push(p.li_company ? box(p.li_company) : degradedBox('LinkedIn company'));
  if (p.li_company_comment) {
    out.push(`<p><strong>First comment</strong> (links go here, not in the post body):</p>`);
    out.push(box(p.li_company_comment));
  }
}

out.push(`<hr>`);
out.push(`<p style="color:#666;font-size:13px"><em>${esc(p.footer || 'Article fact-checked and verified before publish. Questions on framing → ping Jeremy. — Intent Solutions')}</em></p>`);
if (!fragment) out.push(`</div>`);

const html = out.join('\n');
if (outFile) fs.writeFileSync(outFile, html);
else process.stdout.write(html);
