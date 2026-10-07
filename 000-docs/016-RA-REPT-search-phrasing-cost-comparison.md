# 016 — Search phrasing: per-run cost, and the skill against a plain search prompt

| Field | Value |
|---|---|
| Date | 2026-10-06 |
| Status | Measurement record. **Decision: no expansion.** The step stays off; any expansion is routed to E15 (held) |
| Bead | `startaitools-9a8.3.5` (E03-T05, epic `startaitools-9a8.3`, GitHub #123) |
| Spend | $0 new. Agent compute from the existing plan; no paid API; scratch directories only |
| Cost tooling | `scripts/blog/blogpipe/phrasing_cost.py` (`python3 -B -m blogpipe search-phrasing-cost`) |

## 1. Per-run cost logging

The optional search-phrasing step (`BLOG_SEARCH_PHRASING=1`, `blogpipe/phrasing.py`) now
runs as one subagent whose description starts with `search phrasing`. When the flag is on,
the daily wrapper measures that subagent from its own transcript, which the producer cannot
edit, and records:

- turns; input, cache-creation, cache-read and output tokens (each API message counted once);
- tool calls by name and `web_calls` (WebSearch plus WebFetch; the step's budget is 6);
- wall seconds from first to last transcript event.

The line `SEARCH-PHRASING-COST: {...}` goes to the run log and one row per run goes to the
append-only budget ledger `search-phrasing-cost.jsonl` beside the daily run logs. A run with
the flag off records nothing. Measurement never fails a run.

## 2. Comparison: the keyword-research skill against a plain search prompt

**Method.** The recorded findings of three recent daily posts (2026-10-03, 2026-10-04,
2026-10-05). For each, two arms in separate scratch directories, same model, same named terms,
same 6-call budget and the same output schema:

- **skill**: load the `keyword-research` skill and follow the narrow brief in the producer's
  `search-phrasing.md` verbatim;
- **plain**: a plain prompt asking for the same search with WebSearch, no skill.

Every output was scored by the production consumer (`blogpipe/phrasing.py`: candidates kept
after validation, candidates dropped, distinct evidence URLs) and every run was measured by
`search-phrasing-cost` from its own transcript.

| Day | Arm | Kept | Dropped | URLs | Web calls | Turns | Total tokens | Fresh input | Cache read | Output | Wall (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 10-03 | plain | 6 | 1 | 5 | 3 | 4 | 364,401 | 79,884 | 282,480 | 2,037 | 33.7 |
| 10-03 | skill | 5 | 0 | 5 | 4 | 6 | 579,202 | 86,158 | 491,281 | 1,763 | 42.5 |
| 10-04 | plain | 6 | 1 | 6 | 3 | 4 | 364,523 | 79,940 | 282,579 | 2,004 | 31.6 |
| 10-04 | skill | 6 | 0 | 6 | 3 | 6 | 580,855 | 85,943 | 492,279 | 2,633 | 41.4 |
| 10-05 | plain | 6 | 0 | 5 | 3 | 4 | 364,145 | 79,853 | 282,566 | 1,726 | 30.0 |
| 10-05 | skill | 2 | 3 | 2 | 4 | 6 | 578,858 | 86,105 | 490,537 | 2,216 | 40.4 |
| **Total** | plain | **18** | 2 | 16 | 9 | 12 | 1,093,069 | | | | 95.3 |
| **Total** | skill | **13** | 3 | 13 | 11 | 18 | 1,738,915 | | | | 124.3 |

**Result.** The skill arm cost about 59% more tokens (almost all extra cache reads from two
extra turns plus the skill load) and about 30% more wall time, and it kept fewer usable
candidates (13 against 18; one day kept only 2). Both arms stayed inside the 6-call budget and
neither changed the subject. On these three days the skill adds cost without adding
evidence.

**Decision.** No expansion. The step stays off (`BLOG_SEARCH_PHRASING` unset). If the owner
later turns it on, the plain search prompt is the cheaper arm; adopting the skill, or any
wider use of keyword research, is an E15 decision (held, needs its own budget).

## 3. Limits of this comparison

- **Three days, one run per arm.** Enough to see a cost difference that is consistent across
  all three days; not enough to rank title quality, which no person has judged here.
- **Model.** Both arms ran on the interactive session's model, not on the daily producer's
  runtime. The producer runs Claude Code against a different provider endpoint, and whether
  WebSearch is available there was not tested. The first scheduled run with the flag on would
  show it in its `SEARCH-PHRASING-COST` line (`web_calls: 0` with a `no_web` skip).
- **Harness overhead dominates.** About 80,000 fresh input tokens per arm are the context the
  agent harness gives every subagent, before any search. That overhead is shared by both arms
  and by every other subagent in the daily run.
- **Free-tier search only.** No paid keyword-volume source was used, by design (S08). Search
  volume, difficulty and ranking were not measured.
