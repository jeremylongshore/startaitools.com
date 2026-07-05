#!/usr/bin/env node
/*
 * blog-packet-html.cjs — render the Ezekiel posting-packet HTML from a JSON
 * payload. Reuses the proven "v3" layout (Gmail thread 19f1e4b93f9158cc):
 * greeting → live+canonical callout → "post it to N places" → before-posting
 * notes → Substack → Medium → X box → LinkedIn personal (+first comment) →
 * LinkedIn company (+first comment) → verbatim-disclaimer footer.
 *
 * Usage:
 *   node blog-packet-html.cjs < payload.json > packet.html
 *   node blog-packet-html.cjs --in payload.json --out packet.html
 *
 * Payload schema (all optional except post_title + canonical_url + destinations):
 * {
 *   "post_title": "...", "canonical_url": "https://startaitools.com/posts/slug/",
 *   "tier": 2, "date": "2026-07-05",
 *   "destinations": ["x","li_personal","li_company","substack","medium"],
 *   "before_notes": ["verbatim-required disclaimer/guardrail strings"],
 *   "links": { "x": "url?utm_source=x", "li_personal": "...", "li_company": "...",
 *              "substack_canonical": "bare-url", "medium_canonical": "bare-url" },
 *   "x_post": "raw text", "x_is_thread": false,
 *   "li_personal": "text", "li_personal_comment": "Deep-dive: ...\nCode: ...",
 *   "li_company": "text", "li_company_comment": "...",
 *   "substack_subtitle": "...", "footer": "disclaimer footer",
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
if (dest.has('x')) items.push(`<strong>X / Twitter</strong> — Post #1${p.x_is_thread ? ' (thread)' : ''}.`);
if (dest.has('li_personal')) items.push(`<strong>LinkedIn — Jeremy&#39;s personal profile</strong> — Post #2 (+ first comment).`);
if (dest.has('li_company')) items.push(`<strong>LinkedIn — Intent Solutions company page</strong> — Post #3 (post natively; + first comment).`);
out.push(`<p>Post it to <strong>${items.length}</strong> place${items.length === 1 ? '' : 's'}. Every deep-dive link below is already the live URL, UTM-tagged per platform — no placeholders to swap.</p>`);
out.push(`<ol>${items.map((x) => `<li>${x}</li>`).join('')}</ol>`);

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

// X post.
if (dest.has('x') && p.x_post) {
  out.push(`<hr><h2>Post #1 — X / Twitter${p.x_is_thread ? ' (thread — post in order)' : ''}</h2>`);
  out.push(box(p.x_post));
}

// LinkedIn personal.
if (dest.has('li_personal') && p.li_personal) {
  out.push(`<hr><h2>Post #2 — LinkedIn (Jeremy&#39;s personal profile)</h2>`);
  out.push(box(p.li_personal));
  if (p.li_personal_comment) {
    out.push(`<p><strong>First comment</strong> (post the links UNDER the post so they don&#39;t suppress reach):</p>`);
    out.push(box(p.li_personal_comment));
  }
}

// LinkedIn company.
if (dest.has('li_company') && p.li_company) {
  out.push(`<hr><h2>Post #3 — LinkedIn (Intent Solutions company page — post natively)</h2>`);
  out.push(box(p.li_company));
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
