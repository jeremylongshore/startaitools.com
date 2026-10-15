+++
title = 'When Your Documentation Evaluation Is Driving the Cleanup, Report Gap Answers by Rank Instead of Adding Them to the Scored Set'
slug = 'rank-only-reporting-keeps-the-eval-honest'
date = 2026-10-14T08:00:00-06:00
draft = false
tags = ["retrieval-evaluation", "evaluations", "governance", "doc-ops", "search", "rank-only-reporting"]
categories = ["Technical Deep-Dive"]
description = "A self-improving retrieval evaluation should not grade its own homework. Report the rank of each gap-filler doc in retrieval (answerRank per gap) and leave the fixed scored question set untouched."
tldr = "A retrieval evaluation that drives its own corpus cleanup should not grade the cleanup. Report the rank of each gap-filler doc in retrieval (answerRank per gap) and leave the fixed scored set untouched. The scored questions stay comparable run to run, and the cleanup work has a receipt. The honest cost: a reindex can drop Recall@10 even when the gap answers themselves rank one."
+++

If you are running a search or retrieval evaluation against a documentation corpus, and the same eval is what surfaces the holes you then fill, you have a quiet training problem. The minute you add the gap-filler doc to the scored question set, the eval learns to award the new doc because it exists. Run-to-run comparability on your fixed corpus starts to drift, because each cleanup round reshapes the answer key. You lose the one number you trust: the score on a stable set of graded questions.

The escape valve is rank-only reporting. Keep the scored set fixed. For each gap the eval surfaces, search the new doc against the gap question and print where it ranks in retrieval. Print it as `answerRank` in the JSON output. Do not promote the gap-filler doc into the scored set. The scored questions stay comparable, and the cleanup work has a receipt (a machine-written record proving the step really ran).

On one such codebase, the gap record gained a new field naming the doc that was captured to fill the hole. The eval pipeline prints the rank of that doc against the gap question in JSON. Holes still without an answer print as open. Five gaps from the onboarding round now cite real, governed citations for facts captured that day, and none were added to the forty-five graded questions.

The design choice was deliberate. The estate (every repo, server and service the company runs) eval grades answers under FAMA, Fact-Meaningful Answer, a rubric that scores an answer against a fixed ground truth. Letting the cleanup work leak into the scored set would grade the cleanup, which is grading your own homework. So we kept that fixed and reported rank instead. The decision rule in the PR says exactly this: chose rank-only reporting over adding the gaps to the graded questions because those forty-five questions must stay fixed for FAMA to be comparable run to run.

The mutation test that ships with the change enforces the rule. A mutant that points a gap at one of its own obsolete docs fails the test. The test sits among six in the eval-estate-dataset suite. Six of six passed. qmd-adapter typecheck and eslint came back clean. Without that test, the field drifts toward "any doc looks plausible" by the third cleanup round, because somebody will eventually point a gap at a doc that should have been archived.

The live run on the day of the merge is the number that matters. Before the cleanup, obsolete exposure (the fraction of scored questions whose top hit is an obsolete doc) sat at 0.1556. After the archive plus export plus reindex, it sat at 0.0222. The five onboarding gap answers came back at ranks 1, 1, 1, 2, 1. The new docs are findable. The corpus itself is healthier.

There is a real cost, and the PR does not paper over it. Recall@10 fell from 0.4741 to 0.4333. The cause is tracked and named in the PR: a reindex embedded recent notes, and three canonical answers got displaced by those notes. A bead (a tracked task record in the repo's issue database) carries the trade forward. The umbrella compile-then-govern cycle closed the parent bead, with thirty-four obsolete docs archived and five gap facts governed. The four commits on the umbrella repo (1ae9c1e, 7c291d9, 7a562ba, 312e945) record the close, the new beads, and the brain-stats refresh.

The honest read: rank-only reporting buys run-to-run comparability on the fixed corpus, and it tells you whether the gap fillers are findable. It does not buy you a recall number that goes up just because you filled holes. Recall@10 went down, and the reason was a reindex, not the gap-filling work. Those are two different things, and the data should not be conflated. A naive "after cleanup we got better" narrative would have buried a real regression.

## Use this

- If your eval grades answers under a fixed-key meaning rubric (FAMA or otherwise), do not add your own cleanup docs to the graded set. Add a separate field that reports the rank of the cleanup doc in retrieval for each gap, and keep the graded set untouched.
- Write a mutation test that asserts each gap answer is a real qmd:// citation and never one of the gap's own obsolete docs. The deny-list direction matters: the test should refuse a doc that the gap itself should have retired.
- Track the recall move after any reindex as a separate work item from the gap-filling work. The two are causally distinct, and the bead is where the tradeoff lives until somebody goes back to it.

## Related Posts

- [Why a green check that survived an unrelated change is not a gate](/posts/wrong-mode-green-is-not-a-gate/)
- [Why ranked retrieval beats timestamp-based freshness for eval scoring](/posts/rank-current-truth-with-the-rerank-not-the-clock/)
