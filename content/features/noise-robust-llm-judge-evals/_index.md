+++
title = "Noise-Robust LLM-Judge Evals: Don't Sign a Coin Flip"
slug = 'noise-robust-llm-judge-evals'
date = 2026-07-07T10:00:00-05:00
featured = false
weight = 4
description = "An un-seeded LLM judge is a coin flip even at temperature 0. I stopped signing single-call noise into a transparency log. Fold N recorded votes, gate on agreement, label replay fidelity honestly."
link = '/posts/noise-robust-signed-llm-judge-evals/'
+++

**[Read the full deep-dive →](/posts/noise-robust-signed-llm-judge-evals/)**

Signing one LLM-judge call into a transparency log attests noise as if it were truth. Temperature zero does not fix that. Seeds and a real fold do.

The fix is structural: record N votes, fold them deterministically, separate judge variance from sample variance, and refuse a verdict the agreement gate cannot stand behind. A skill that flip-flopped 6 BLOCK / 1 SHIP now reproduces 7/7, signed and stranger-verifiable, including an honest BLOCK of our own skill.

If you are about to put a signed eval in the ship path, do not sign a coin flip.
