+++
title = 'Claude Opus 5 Caught Two Shop Metrics That Disagree'
slug = 'two-numbers-that-disagree'
date = 2026-09-16T10:00:00-06:00
draft = false
tags = ["automation", "devops", "claude-code", "ci-cd"]
categories = ["Development Journey"]
description = "Checking two shop metrics against each other by arithmetic before publishing them. One came off a customer story, and an ops closeout narrowed its own claims."
tldr = "Two results for a customer story could not both be true: 30 seconds saved per book, and listings going from 1-2 to 4-5 per staff hour. The hourly rate implies a gain of at least 15 minutes on every book. Claude Opus 5 caught it by arithmetic and refused to publish both. The operator chose the hourly rate, and the other figure came off the live page four minutes after it went up."
+++

Anthropic declined a customer story for Longbox, a tool that turns phone photos of comic back issues into Shopify drafts through the Claude API. The customer is Gotham City Limit in Jacksonville, Florida. I pasted a screenshot of the decline into a Claude Opus 5 session with one part highlighted. The model pulled the full email before doing anything else, because the actual reason sat above the fragment I had highlighted.

The page had to meet five criteria:

- publicly accessible
- names the customer
- names Claude
- production deployment
- measurable result

The first four are writing problems. The fifth needs numbers from the shop.

## The exchange

It took me three tries to type the numbers. The block opens on the third. Typos are as sent.

```
17:07:13 USER:       5000 drafts in shopify, 30 seconds saved per book timed   - 5000 total comenta weve only scanes 1200
17:07:26 MODEL:      Reading that as: about 5,000 comics in the back room, 1,200 scanned so far into Shopify drafts, 30 seconds saved per book, timed. That also gives about 10 staff hours saved so far (1,200 x 30 seconds).
17:08:08 MODEL ASKS: "We went from 1-2 a day to 4-5, working on backlog." 1-2 of what per day?
17:08:28 USER:       Back issues per day
17:08:41 MODEL ASKS: 1,200 scanned total doesn't fit "4-5 back issues a day". What does the 1-2 -> 4-5 per day measure?
17:08:57 USER:       Listed per staff hour
17:09:07 MODEL ASKS: Which timing number is the one actually measured at the shop? The other comes off the page.
                     (options: 4-5 books per hour / 30 seconds per book / Both, explained)
17:11:04 USER:       4-5 books per hour
17:11:50 MODEL:      The "30 seconds per book" figure is gone from the page, the home card and the notes, since it contradicted the hourly rate.
```

Claude Opus 5 caught two inconsistencies in a row. The 1-2 to 4-5 figure came from a quote already in the record. I said the unit was back issues per day. The model answered that 1,200 scanned total does not fit 4-5 a day and asked again. The unit was per staff hour.

The second catch is arithmetic. At 1 to 2 books per staff hour, a book takes 30 to 60 minutes. At 4 to 5, it takes 12 to 15. That is at least 15 minutes saved per book. A page that also says 30 seconds saved per book is a page a reviewer can break with a calculator.

The model would not publish both. It offered "Both, explained" as an option and I did not take it. I picked the hourly rate as the one measured at the shop, and the 30 second figure came off the live page. It had been up for about four minutes.

Honest scope: this does not show the 30 second figure was false or untimed. It shows that when asked directly which number was measured at the shop, I picked the other one, four minutes after labeling the first one "timed". The model has its own wrong turn in here too. It derived "about 10 staff hours saved" from the 30 second number and wrote a results section before it caught the conflict.

The resubmitted page states 1,200 back issues scanned into Shopify drafts and 1-2 going to 4-5 listed per staff hour, dated 16 September 2026. A reply went to Anthropic partner support with three screenshots taken from the live page.

## intent-os: an ops closeout that corrected its own write-ups

intent-os took 72 commits that day (48 without merges) closing out an ops remediation. `feat(ops): supervise independent Scorecard public freshness` installed an outside-in observer for scorecardecho.com: `scorecardecho-outside-in.service`, its `.timer` and a `-failure.service` under `ops/observability/systemd/`, plus an 88 line `OUTSIDE-IN-SCORECARD.md`. Outside-in means the check watches the public surface from somewhere that is not the host being watched.

The same day, `fix(ops): report observer host-loss coverage honestly` narrowed what that observer claims to cover. Five more commits did the same job on other write-ups: `docs: distinguish structural custody and actual synthetic alert delivery`, then `Correct home backup automation registry from live timer and custody receipts`, then `test: revalidate registry evidence after pending-installation correction`, then `docs(ops): finalize installed backup evidence and honest heartbeat scope`, and `fix: preserve valid capacity receipts after collector interruption`.

The home server backup custody monitor took nine `fix(backup)` commits. Three landed with before and after evidence files under `evidence/2026-09-16-home-custody-monitor/`. The failure modes they close include a negative custody timestamp, an unreapable child process, a failed snapshot cache setup and a singleton lock sitting on a writable runtime path. Each one is a way for a monitor to report success it has not earned.

`fix(ci): exempt only verified notifier digest from secret detection` landed with a regression test at `ci/test-gitleaks-known-binary-digest.py` and 5 lines in `.gitleaks.toml`. The word doing the work is "only". The exemption is pinned to one verified digest and a test asserts it stays that way.

A bounded OpenCodeReview CLI was built hash-bound from a trusted base under `ops/review/ocr-bounds/`: `build.py` (125 lines), `code_search.go` (286), `code_search_bounds_test.go` (63), `test_build.py` (76), a manifest and a LICENSE. `fix(ci): disable OCR self-updates to preserve the pinned artifact` went with it. A review tool that updates itself produces output you cannot reproduce.

## Partner Hub

At 20:00, a Partner Hub form rejected:

```json
{"error":"required_fields_incomplete","message":"This submit was REJECTED and nothing was saved: 4 required scope-form field(s) on this project would still be empty"}
```

The form refused to save a partial submission instead of accepting it and reporting success. Two scope corrections from me bracketed it. At 19:56: "they dont need all those details of what was paid and the money involved thats none of their business". At 20:09: "so basically paid consulting and training dont need a customer id?"

## Also shipped

braves shipped 17 commits on scorecardecho.com including `fix(deploy): preserve completed strikeout and walk counts (#151)` and `fix(frontend): restore visible mobile score scrolling (#150)`. Also `test(frontend): verify lifecycle timestamps through freshness details`, `docs: record installed automatic freshness monitor and natural checks (#149)`, and `docs: reconcile production runbook with real game recovery (#148)`.

intent-longbox: Claude Opus 5 took over a stalled background agent waiting on a Postgres integration lane running 60 files serially (fileParallelism: false). The model armed a background waiter and used the dead time to verify the demos page source links returned 200. The lane came back green under vitest 4: 879 passed, 1 skipped, 57 files. The upgrade from vitest 3.2.7 to 4.1.11 cleared two medium CVEs, with the scanner clean across 365 packages and neither config needing migration. Unit tests: 1,900 across 102 files, coverage 80.47 percent against an unchanged 80 floor. The Release workflow went manual only so the bot cannot fail against protected main or strand tags. PR #1 merged after 11 checks passed (8 required plus 2 MiniMax review jobs).

A three-page owner study guide was rendered via whiteglove-pdf. The first render printed the title twice and let a link run past the margin. Claude Opus 5 read every page, caught both defects, fixed them, only then sent the email.

Asked to add an awards spotlight for the shop, Claude Opus 5 answered "Before I add anything about awards I need to confirm which ones are real" and went to the shop's own site, the private repo, and the web before writing.

At 01:56, an agent flagged a memory condition: RAM healthy (11 GB available of 23) but swap exhausted (15 GB of 15, 24 KB left), the documented precursor to earlier tmux and dbus deaths on this box. Claude Opus 5 did not intervene, citing the box's hard do-not list, and reported instead.

bobs-big-brain-registrar shipped three Dependabot group bumps (20 dev dependencies, 5 production, 4 GitHub Actions). This blog's own pipeline run that day used MiniMax M3, at 55 turns and 94 tool calls.

## Related

- [Every Claim Needs a Shipped Source and an Executable Proof](/posts/working-is-not-proven/)
- [Auditing Written Claims Against Their Artifacts](/posts/the-second-review-that-audits-the-claims/)
- [When a Gate Should Re-Run the Step Instead of Trusting Its Receipt](/posts/stop-trusting-the-stored-claim/)
