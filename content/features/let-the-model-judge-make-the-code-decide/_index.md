+++
title = 'Let the Model Judge. Make the Code Decide.'
slug = 'let-the-model-judge-make-the-code-decide'
date = 2026-07-17T08:00:00-05:00
featured = true
weight = 1
description = "The model owns judgment. Deterministic code owns the gates, the commit, and the audit trail. How I rebuilt a daily writing pipeline so a hung session can no longer brick tomorrow."
link = '/posts/let-the-model-judge-make-the-code-decide/'
+++

**[Read the full deep-dive →](/posts/let-the-model-judge-make-the-code-decide/)**

I ran kitchens long enough to know a line check is not a vibe. Pass or you do not open. Same rule for a publishing pipeline.

Daily posts used to die when a model session hung, timed out, or wrote half a file. The fix was not a smarter prompt. It was a hard seam: the language model may judge and draft; bash verifies preconditions, commits, dual-publishes, and quarantines anything incomplete. Produce, land, syndicate. If the produce step fails, tomorrow still runs, because the land step never trusted the model with git.

That is the whole piece. One rule, enforced where the audit trail lives.
