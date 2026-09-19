+++
title = "The BitLocker Helper Lifetime Receipt Pack Ran a Full Day"
slug = "the-helper-lifetime-receipt-pack-ran-for-a-full-day"
date = 2026-09-15T10:00:00-06:00
draft = false
tags = ["bitlocker", "windows", "testing", "release-engineering"]
categories = ["Development Journey"]
description = "One day's worth of BitLocker helper hardening on intent-blue-gold, captured as fix/probe/receipt triples. The system design is unchanged; the evidence index is wider."
tldr = "On 2026-09-15, intent-blue-gold absorbed 180 commits and 100+ PRs that all fit the same shape: a bounded fix to the BitLocker cross-token helper, a synthetic proof probe, and a hosted receipt pinning run, source, input and artifact hashes to a DOC/RTM/changelog update. Nothing in the system changed shape; the evidence index got wider, with the same NOT_EXECUTED list as every prior day in the FY6.32 sweep."
+++

On 2026-09-15, intent-blue-gold absorbed 180 commits and 100+ PRs that all fit the same shape. Three pieces every time: a bounded fix to the BitLocker cross-token helper, a synthetic probe that proves the fix without live provider or customer data, and a hosted receipt pinning run, source, input, and both artifact hashes to a DOC/RTM/fy6.32 execution authorization/changelog update. Zero commits landed on any other repo. The receipt pack ran for a full day, and the system envelope did not move.

The PR body template is the receipt pack's spine. Every PR opens the same way, then names what it did NOT prove. Here is the closing paragraph of PR 127, lifted verbatim:

> Machine comparison of receipt source, required/passed tests, input hashes, and both artifact SHA256 files passed. Local make check 14/14 and planning/Beads audits passed. Live batch-key publisher and delivery remain NOT_EXECUTED; production parent still couples one fresh session/token key. This is not UAC/provider/C01/C02/bounded non-mutation/READY/GOLD/release authority. No real customer data or destructive tests.

That list is the day's quality bar. Each PR is honest about what stayed unproved: runas/UAC, live provider, C01/C02 customer data, bounded non-mutation, READY/GOLD/release authority. The envelope is the same; only the proof surface is wider.

Six themes recur across the day's PRs.

Helper lifetime hardening: boot-expiry watchdog, post-provider timeout, collector exit detection. The helper process owns a cross-token launch and a named pipe; the watchdog closes a hole where a stale process kept the pipe handle open past a parent restart.

Native I/O completion deadlines. The helper's native I/O path now rejects late completions. The probe supplies a synthetic I/O ring and asserts the deadline fires before the next provider call.

CIM conversion precision. Resolve the WMI conversion method through the method set, parse WMI output cleanly into WipingStatus and siblings. The PR supplies the precision input that the original code was silently dropping.

Cross-token handshake failure classification. Classify the stages of a closed handshake: which side closed, which frame failed to land, whether the post-response pipe boundary held. The probe injects each stage and asserts the right classifier fires.

ARM64 standard-user client probes. ShellExecuteExW to the production launch call site under a temporary medium-integrity account. The probe reaches the call site without connecting IPC, transferring a key, or executing the provider. Synthetic, disposable, no UAC.

Receipt-pack evidence index. Machine comparison of source/test hashes, replay index. Each receipt pins the run, the source SHA, the input hashes, and both artifact SHA256 files. The replay index is what makes a synthetic probe auditable months later.

Where this sits on the path: parent process, helper (elevated, cross-token), COM, named-pipe IPC, CIM conversion (WMI ExecMethod), WMI output parsing, cross-token handshake (verify pipe end after helper exit). The day's changes land across the helper lifetime and the IPC/handshake boundary. Nothing new was added. Nothing was removed. The CIM conversion precision PR is a fix to a silent drop, not a new boundary.

What did NOT change: the system design. The module count is the same, the boundaries are the same, the boundary contracts are unchanged. The envelope holds; the evidence index is wider. That is what makes Tier 1 honest today. The day's work is a continuation, not a paradigm shift, and the receipt pack is the audit trail.

Tomorrow is the same.

Related: [The pipeline landed its own output today]({{< ref "/posts/the-pipeline-landed-its-own-output-today/" >}}) · [Three gates on standard-user BitLocker state observation]({{< ref "/posts/three-gates-on-standard-user-bitlocker-state-observation/" >}}) · [Sealing a 168-bead planning graph took three reviews]({{< ref "/posts/sealing-a-168-bead-planning-graph-took-three-reviews-and-a-seven-seat-council/" >}}).
