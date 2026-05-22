+++
title = 'FTS5 Fallback: How Zero Search Results Became Five (ICO Dogfood Day One)'
slug = 'icos-dogfood-zero-to-five-fts-fallback'
date = 2026-05-21T08:00:00-05:00
draft = false
tags = ["dogfood", "fts5", "search", "debugging", "tdd", "intentional-cognition-os"]
categories = ["Technical Deep-Dive"]
description = "First real dog-food run of Intentional Cognition OS scored 0/5 question engagement against a corpus that contained every answer. Root cause: AND-only FTS5 query construction plus a possessive normalization order-of-operations bug. Fix: strict-then-broad fallback. Result: 5/5, 28 citations, ~$0.20."
+++

Five questions in. Zero answers out. The corpus had every answer; the search layer refused to admit it. Twenty-four hours later, against the same compiled workspace and the same five questions, ICO returned 5/5 engaged with 28 citations for about twenty cents in API spend. Only the query construction changed. This is the story of two compounding bugs in 30 lines of TypeScript and the dog-food loop that surfaced them.

## The setup

Intentional Cognition OS (ICO) compiles a directory of source documents into a structured wiki — source pages, concept pages, topic pages, contradictions, gaps — and then answers free-form questions over that wiki via FTS5 retrieval plus Claude. The retrieval stage is the load-bearing piece: ICO uses FTS5 to surface candidate pages, hands the top-ranked subset to Claude, and Claude writes a cited answer. If retrieval returns zero rows, ICO never calls Claude at all. It returns a "no compiled knowledge found" stub and exits clean.

The v0.1 dog-food bank is five hand-authored question/answer pairs about `intent-eval-core`, an internal package whose docs ICO had just compiled — 19 source files, 132,000 tokens through the compile pipeline, about sixty cents to build the wiki. The questions are not trick questions. They are the questions any new contributor on `intent-eval-core` would actually ask on day one.

Why dog-food at all? Because the OPS-class bugs — the ones that fire when a real user types a real question against real docs — are the ones unit tests never write. The compiler had 466 passing tests. None of them asked ICO a question.

## The disaster

Session 2 ran the v0.1 bank against the freshly compiled `intent-eval-core` workspace. Result: every single question hit the pre-Claude fallback. Zero API calls on the asks. The wiki itself was healthy — 19 source pages, 6 concept pages, 2 topic pages, 5 contradictions, 4 gaps, all populated correctly. Retrieval just couldn't find any of it.

| Q   | Question shape                                                  | Outcome                            |
|-----|------------------------------------------------------------------|-------------------------------------|
| Q01 | "What is intent-eval-core's role… and what does it not do?"     | No compiled knowledge found        |
| Q02 | "Which contradictions did ICO surface in this corpus?"           | No compiled knowledge found        |
| Q03 | "What gaps did ICO flag, and what would close them?"             | No compiled knowledge found        |
| Q04 | "How does intent-eval-core relate to the broader platform?"      | No compiled knowledge found        |
| Q05 | "What's the public API surface of intent-eval-core?"             | No compiled knowledge found        |

The pivotal anomaly came when a manual, deliberately-short query was typed against the same workspace: `"What is intent-eval-core?"`. That query engaged fine — 13,000 tokens through Claude, 10 citations, a rich answer pulling from four source pages. Same workspace. Same FTS5 index. Same retrieval code path. Only the question phrasing differed.

That single contrast was the whole signal. Whatever was wrong, it was not the compile output and it was not Claude. It was the layer that turned a question string into an FTS5 MATCH clause. Filed as bead `intentional-cognition-os-fmo`, P1.

## Root cause: AND-only construction and order-of-operations

Two bugs in `packages/compiler/src/ask/analyze.ts`. Either one alone would have caused intermittent misses. Together they made compound questions un-answerable.

**Bug 1 — AND-only FTS5 query construction.** `buildFtsQuery` extracted tokens from the question and joined them with implicit AND. FTS5 treats space-separated terms in a MATCH clause as AND by default. So Q01's residual tokens after stopword filtering looked roughly like:

```
intent eval core role inside platform explicitly does not do
```

Eleven tokens, all required to co-occur on a single page. No single page in the wiki — not even the densest concept page — contained all eleven. FTS5 dutifully returned zero rows. The BM25 ranker that would have happily surfaced the best-matching pages never got a chance, because nothing matched at all.

The fix is the oldest move in IR: precision-then-recall. Try AND first; if it returns nothing, fall back to OR and let BM25 sort the results. Not novel. Just absent.

**Bug 2 — possessive normalization order-of-operations.** `extractTokens` had two transformations: strip non-word characters, and normalize possessives (`core's` → `core`). The transformations ran in that order. Strip first, then possessive-normalize. Which meant `core's` lost its apostrophe in step one, became `cores` (with a trailing s), and step two's possessive regex never matched because the apostrophe was already gone.

The downstream effect: the FTS5 index had been built with the singular form `core`, but the query was hunting for the plural-looking `cores`. Q01 specifically said *"intent-eval-core's role"* — that possessive collapsed to a token the index didn't contain. Pattern correct. Ordering wrong.

```typescript
// Before
const stripped = raw.replace(/[^\w\s]/g, ' ');
const normalized = stripped.replace(/(\w+)'s\b/g, '$1');

// After
const normalized = raw.replace(/'s\b/g, '');
const stripped = normalized.replace(/[^\w\s]/g, ' ');
```

Two characters of reordering. One bug closed. (Yes, the new regex also strips the `'s` off `it's` and `she's` — both contractions and possessives lose the trailing `s`. That's fine here: pronouns and copulas are stopwords in this index anyway, so the collateral mutation is a no-op on retrieval.)

## The fix

`buildFtsQuery` now returns both a strict (AND-joined) and a broad (OR-joined) query. `analyzeQuestion` tries strict first. If zero rows come back, it retries with broad and lets BM25 rank the candidates. Each token is FTS5-quoted to avoid colliding with reserved keywords.

```typescript
function buildFtsQuery(tokens: string[]): { strict: string; broad: string } {
  const quoted = tokens.map(t => `"${t}"`);
  return {
    strict: quoted.join(' AND '),
    broad:  quoted.join(' OR '),
  };
}

async function analyzeQuestion(q: string, db: Database) {
  const tokens = extractTokens(q);
  const { strict, broad } = buildFtsQuery(tokens);

  let pages = await searchPages(db, strict);
  if (pages.length === 0) {
    pages = await searchPages(db, broad);
  }
  return rankAndTrim(pages);
}
```

The OR path is not "less correct" — it's a recall fallback whose precision is restored by BM25 ranking. A page that hits eight of eleven tokens scores well above a page that hits one. The top-K subset handed to Claude looks essentially the same as the AND case would have looked if the AND case had returned anything.

## Strict TDD detail

Five regression tests went in first, under an `fmo regression` describe block. Three RED. Two unexpectedly GREEN.

The two unexpectedly-green tests were short single-clause questions with no possessives — `"What gaps did ICO flag?"` worked fine even on the broken code, because three tokens with AND can co-occur on a gap-summary page. That signal mattered. It told us the bug fired specifically on compound multi-clause inputs that contained possessives and dashed identifiers, which is precisely the shape of Q01 and Q04 in the bank. The bug was not "FTS is broken." It was "FTS is overconstrained on questions of a specific morphology."

After the fix, all five went GREEN. The five new tests landed inside the same compiler package and brought the suite to 466/466 — the bank-driven regressions are now first-class members of the test set, not a parallel scaffold.

## Validation

Re-ran the v0.1 bank against the same compiled workspace. Run id `2026-05-22T0257Z-intent-eval-core-v1-postfmo`. Result: 5/5 engaged, 28 citations, 48,019 tokens, approximately $0.20 in actual Anthropic API spend.

| Q   | Citations | Tokens (in+out) | Latency (ms) |
|-----|-----------|-----------------|--------------|
| Q01 | 11        | 8,154           | 12,781       |
| Q02 | 6         | 9,570           | 5,462        |
| Q03 | 6         | 8,858           | 12,103       |
| Q04 | 4         | 10,829          | 13,261       |
| Q05 | 1         | 10,608          | 9,349        |

The `verify_rate` field in the metrics still reads 0%, but that's a separate bug: `verify.py` greps the TARGET source tree for citation strings, and ICO now emits compiled-wiki paths (`wiki/sources/...`) rather than original source paths. Filed as `intentional-cognition-os-h99`, P2. The real verify-rate floor only becomes measurable after h99 lands. For day-one dog-food, engagement and citation count are the right signals; verify-rate joins the dashboard once it points at the right filesystem.

## Gemini round

Posted the PR. `/gemini-review`. Three more edge cases came back that the five regression tests didn't cover.

First: smart-quote possessives. The new possessive regex matched ASCII `'` but not U+2018 or U+2019. Anyone pasting a question from a word processor — which is most of them — would hit the original bug. Fix: widen the character class to `/[‘’']s\b/`, covering all three apostrophe codepoints.

Second: token merging on punctuation. The pipeline did split-then-strip, so `foo,bar` became `foobar` instead of `['foo', 'bar']`. The fix is to replace punctuation with whitespace before tokenizing, not after. One-line reorder.

Third: redundant fallback when the query is a single token. If `tokens.length === 1`, `strict` and `broad` are literally the same string. Skip the second `searchPages` call. A guard, not a correctness fix — but it shaved a measurable amount of latency off the short-query path that had been the only working case before all of this.

Two new regression tests for the three issues — the single-token redundancy fix was a guard rather than a behavioral change, and rode along with the smart-quote and punctuation-merge tests. 468/468 passing. v1.2.4 released.

## What dog-food caught that unit tests didn't

The whole retrieval gap was silent. The compiler had 466 tests. None of them constructed a question, ran it through `analyzeQuestion`, and asserted that any pages came back. The closest tests asserted FTS5 schema correctness, token extraction shapes, and BM25 ordering on synthetic fixtures. They all passed throughout the bug's entire lifetime.

The [dog-food loop](/posts/forge-dogfood-plane-plugin-grade-a-and-jrig-verified-loop/) also caught four OPS bugs in `run.sh` along the way — a trailing newline in `basename` output that broke a downstream `find`, the wrong workspace path in the default config, global flags being parsed after the subcommand instead of before, and `ico compile all` not being accepted as a subcommand at all. Plus two `--json` flag bugs in `ask.ts`: the flag was silently ignored on both the happy path and the no-knowledge fallback path. None of those threw errors. None of those failed tests. They were all the kind of bug that ships because nothing red-lights when it happens.

Seven PRs in twenty-four hours, two releases the same day (v1.2.3 then v1.2.4), and the system went from "answers nothing" to "answers everything in the bank with full citations." The unit tests didn't catch any of it. Sitting on the user side of the tool caught all of it.

## Closing

If you run keyword search over user questions and your retrieval ever looks weirdly narrow, two things are worth checking before anything else. First, whether your query joiner is implicit-AND, and whether a strict-then-broad fallback would let BM25 do the work it was designed to do. Second, whether your token normalization pipeline runs its transforms in the right order — possessive stripping has to happen before non-word stripping, or the apostrophe disappears and the possessive regex never matches anything. Both bugs are invisible to unit tests written by the same person who wrote the code under test. Both are loud the first time a real user asks a real question against real docs. That is the test the unit tests don't write.

— Jeremy Longshore
intentsolutions.io
