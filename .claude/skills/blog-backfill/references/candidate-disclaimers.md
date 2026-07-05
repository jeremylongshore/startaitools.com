# Candidate disclaimers — PROPOSALS awaiting Jeremy's approval

**Governance rule (WS2):** the posting packet only ever uses **Jeremy-approved**
disclaimer text from `disclaimer-library.json`. The pipeline never auto-generates
or auto-adds a disclaimer. This file is the staging area: Claude (or anyone)
**proposes** candidate strings here; Jeremy reviews and, for any he approves, a
human copies the **exact** approved string into `disclaimer-library.json`. Nothing
in this file is live until it is moved there.

## How the packet uses the library

- When a published post's body matches an entity's `match` terms, the packet
  injects that entity's approved disclaimer(s) into the packet's "before posting"
  notes, marked verbatim-required (Ezekiel may not edit or omit them).
- If a post matches an entity that is in the library with an **empty** `approved`
  array, the packet **fails closed**: it emits a HOLD banner and flags Jeremy
  rather than handing Ezekiel un-disclaimed copy. Use this to gate a sensitive
  entity ("any post mentioning <client> must HOLD until I approve wording").

## Currently approved (live in disclaimer-library.json)

- **default_footer** — the generic fact-checked/verify footer.
- **anthropic** — "Keep the tone fair to Anthropic — this is an
  ownership/verifiability argument, not 'theirs is insecure.'"

## Proposed — NOT yet approved (do not use until moved to the library)

> Jeremy: strike, edit, or approve. Approved ones get copied verbatim into
> `disclaimer-library.json`.

1. **AI-assisted-content disclosure (generic)** — proposed for posts that are
   substantially AI-drafted, if you want a transparency line:
   > "Portions of this post were drafted with AI assistance and reviewed by a
   > human before publishing."

2. **Partner/client mention (gate example)** — if you want any post naming an
   active client to HOLD until you approve wording, add the client as an entity
   with an empty `approved` array, e.g.:
   ```json
   "acme-corp": { "match": ["acme"], "approved": [] }
   ```
   The packet will then HOLD any post mentioning "acme" and flag you.

3. **Forward-looking / roadmap statements** — for posts describing unreleased
   work:
   > "Roadmap and timelines described here are directional, not commitments."

_Add proposals below as they come up. Keep this file; it is the audit trail of
what was considered and why._
