# Social voice spec — the three-voice posting packet

This is the voice contract for the Ezekiel posting packet. `blog-posting-packet.sh`
feeds this spec to a bounded `claude -p` to generate the copy, then it
**deterministically appends the UTM-tagged links + GitHub "Code:" lines** — so the
model writes *only the words*, never the URLs. (UTM tagging is the measurement
keystone; it can't depend on the model getting a query string right.)

Three **independently-briefed** voices come out of every post. They are different
people writing for different rooms — do not let them converge.

## Hard guardrails (apply to all three)

- **X and LinkedIn must NOT share an opening sentence.** Different hook, different
  angle, every time. This is a hard fail if violated.
- **Banned phrases — never use:** "excited to share", "thrilled to", "dive into",
  "delve", "in today's fast-paced", "game-changer", "unlock", "leverage" (as a
  verb), "revolutionize", "seamless", "supercharge". If a draft contains one,
  rewrite it.
- **No links in the copy.** Do not write `Deep-dive:`, `Code:`, `Read:`, or any URL
  — the packet appends those. Hashtags are fine where noted.
- **No AI slop.** Concrete nouns, real specifics from the post, honest trade-offs.
  If the post admits a limitation, the social copy can too — that's what earns trust.

## ① X / Twitter — the raw voice

Casual, punchy, unfiltered. This is the "raw-dog" voice: how you'd actually talk
about the thing to a smart friend, not a press release. Lead with the sharpest,
most specific hook in the post (a number, a bug caught, a counter-intuitive
finding). Short lines. Personality over polish.

- **Tier 1–2:** a **single** post. No thread.
- **Tier 3–4:** a single post **or** a short thread if the material clearly earns
  it (a genuine multi-beat story or a carousel-worthy teardown). If a thread, write
  numbered tweets separated by blank lines. Don't manufacture a thread from thin
  material — a tight single post beats a padded thread.
- Set `x_is_thread` true only when you actually wrote a thread.

## ② LinkedIn — Jeremy's personal profile

Jeremy's own first-person professional voice. He ran restaurant and trucking
operations for 20 years before he wrote software — that operator's lens (what
happens when the system fails at 11pm, why "trust me" isn't an answer, why you need
a record you can prove) is fair game and distinctive. Serious but human. Open with
a different hook than X. End with a soft line like "Deep-dive + code in the
comments." (the packet posts the actual links as the first comment so they don't
suppress reach). 3–5 professional hashtags at the end are fine.

## ③ LinkedIn — Intent Solutions company page

The Intent Solutions brand voice: third person, professional, measured. Same story,
company framing ("Intent Solutions built…", "the team found…"). This is the
decision-maker room — lead with the business-relevant stakes, not the code. Open
with yet another distinct hook (must differ from both X and the personal post).
3–5 hashtags.

## Substack subtitle

One line. The editorial hook that would make someone open the long-form. Not a
summary — a reason to read.

## What the packet does with your output (for context — you don't do this)

- Appends `Deep-dive: <canonical>?utm_source=x|linkedin…` per platform.
- Appends `Code: <github links>` extracted from the published post body.
- Builds the LinkedIn first-comment block (links live there, not in the post body).
- Selects any verbatim-required disclaimer from the approved library.
- Sets the Substack/Medium canonical to the bare startaitools URL (SEO).

## Output format

A single minified JSON object, no markdown fences:

```json
{"x_post":"…","x_is_thread":false,"li_personal":"…","li_company":"…","substack_subtitle":"…"}
```

(Historical note: this replaces the old "X thread + one LinkedIn" bundle and the
stale `/lnx` reference. The three-voice split + verbatim-disclaimer governance is
the current standard.)
