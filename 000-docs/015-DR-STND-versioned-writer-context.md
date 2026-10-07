# 015 — Versioned slim writer context, with a before/after inventory

| Field | Value |
|---|---|
| Date | 2026-10-06 |
| Status | Standard. `writer-context/v1` released; contract check in **observation mode** until run date 2026-10-21 |
| Bead | `startaitools-9a8.1.4` (E01-T05, epic `startaitools-9a8.1`, GitHub #121) |
| Authority | `scripts/blog/writer-context/writer-context-v1.md` (text) and `scripts/blog/blogpipe/writer.py` (renderer, pins, contract check) |
| Owner roles | Editorial lead (the text), pipeline maintainer (renderer and switch) |

## 1. What changed

The writer agent used to receive whatever the producer assembled: a 9 KB instruction template
(when the producer followed it), the day's git log, PR bodies, beads list, a transcript digest
and the first 200 lines of several CLAUDE.md files. Nothing recorded what a given writer saw.

Now the writer receives one rendered brief built from a **versioned file** and a **fixed slot
object**:

| Kept (what the writer needs) | Dropped (what it never used) |
|---|---|
| The step 1b reader brief (`finding`: sentence, reader, problem, outcome, source evidence, destination) | Classifier dimensions, confidence and flags |
| `sources`: only the excerpts that back the finding (at most 12, 2,000 characters each) | The full git log, all PR bodies, the beads list |
| Tier name, length target and one tier structure block | The other two tier blocks |
| Voice facet, register rules, the persona-is-not-evidence rule, the dash ban, pointers to the deny-list and glossary files | CLAUDE.md excerpts from other repositories |
| Models roster and a short collaboration note (at most 1,200 characters) | The why-this-template-exists rationale |
| Front matter shape, including the mandatory `tldr` the old template omitted | |
| Related-post candidates (at most 8) | |

`python3 -B -m blogpipe writer-context render` refuses any slot outside that list, so the
context cannot grow back by accident. It writes `.blog-staging/DATE.RUNID.writer-context.json`
and prints the brief. The producer copies the record's `audit` object into
`agent_audit.writer_context` (`version`, `template_sha256`, `brief_sha256`, `brief_bytes`).

**Versions are immutable.** `writer.VERSIONS` pins each file's sha256 and
`tests/test_blog_writer_context.py` fails if a released file changes. A change is a new file
(`writer-context-v2.md`) and a new version, so every post can be tied to the exact text its
writer received.

## 2. Context size, before and after

Measured from the producer transcripts of the five most recent daily runs (2026-10-01 to
2026-10-05): the bytes of the prompt handed to the writer agent, and the input tokens of the
writer agent's first turn.

| Measure | Before | After (`v1`) |
|---|---|---|
| Fixed instruction text (slots empty) | 9,097 bytes (legacy template) | 3,959 bytes (Tier 1) |
| Whole writer brief, median of the five runs | 13,194 bytes (range 4,357 to 20,333) | 3,988 bytes when re-rendered from the same finding |
| Whole brief, the two runs that followed the template (2026-10-04, 2026-10-05), source material carried untrimmed | 15,067 and 20,333 bytes | 8,718 and 11,385 bytes (42% and 44% smaller) |
| Writer agent first-turn input | 91,611 to 98,319 tokens | not changed by this work (see §4) |

Three of the five runs did not follow the template at all: the producer wrote a free-form
prompt each time, so the shape of the writer's instructions varied day to day. Removing that
variance is the main gain; the byte saving is secondary.

## 3. Observation mode and the dated switch

The contract check (`blogpipe/writer.py: gaps`) uses the shared dated switch
(`blogpipe/switch.py`), like the reader-brief (2026-10-14) and record-schema (2026-10-17)
switches:

- Every validation prints `PRODUCER-CONTRACT: WRITER-CONTEXT: version=... brief_bytes=...`
  (the per-run record of which context was used and its size) and
  `PRODUCER-CONTRACT: ADVISORY: writer context (observation until 2026-10-21): ...`.
  The daily summary email shows both on its `Writer context:` line, and the wrapper logs the
  version the run's workspace offered (`WRITER-CONTEXT: available ...`).
- **Observation window:** run dates 2026-10-07 to 2026-10-20. A gap (missing record, a legacy
  fallback, a hash or size that does not match the staged brief) is advisory only.
- **Enforcement:** from run date **2026-10-21** the same gap refuses. The readiness countdown
  starts three days before; fewer than seven consecutive complete runs after the switch is an
  URGENT notice. `BLOG_WRITER_CONTEXT_ENFORCE_FROM=YYYY-MM-DD|off` moves or disables it with
  no code change. Moving the date is the rollback.
- **Evidence to flip:** seven consecutive `Writer context: ... complete` lines. If they are not
  there by 2026-10-20, move the date.

## 4. Known limit, filed separately

The writer agent's first turn is about 92,000 to 98,000 input tokens, and the brief is roughly
4,000 to 5,000 of them. The rest is context the agent harness gives every subagent (system
prompt, tool definitions, and the user-level and repository CLAUDE.md files). A brief cannot
remove it; reducing it means changing how the producer launches agents, which is a separate
decision.

## 5. Rollback

Set `BLOG_WRITER_CONTEXT_ENFORCE_FROM=off` to stop any refusal. To stop using the context,
revert the instruction change in the private skills repository; the legacy template remains
as the recorded fallback.
