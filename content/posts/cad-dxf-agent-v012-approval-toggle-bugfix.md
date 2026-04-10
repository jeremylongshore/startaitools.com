+++
title = "IntentCAD v0.12.0: The Approval Toggle That Wasn't"
slug = 'cad-dxf-agent-v012-approval-toggle-bugfix'
date = 2026-04-01T10:00:00-05:00
draft = false
tags = ["cad", "bug-fix", "release-engineering", "python"]
categories = ["Development Journey"]
description = "A rejected operation couldn't be toggled back to approved. Five commits and a patch release to fix the core approval state machine in IntentCAD."
+++

You reject an operation. You realize you shouldn't have. You click to approve it. Nothing happens.

That was the bug. IntentCAD's operation approval UI allowed toggling approved operations to rejected but not the reverse. Once rejected, always rejected. The state transition was one-way when it should have been bidirectional.

This isn't a dramatic production outage. It's the kind of bug that sits in a codebase for weeks because nobody exercises that specific workflow until someone does, and then it's a support ticket that takes 30 seconds to diagnose and 5 minutes to fix. The interesting part isn't the fix — it's why the bug existed in the first place.

## The State Machine

The approval state machine had three states: `pending`, `approved`, `rejected`. The intended transitions:

```
pending  → approved  ✓
pending  → rejected  ✓
approved → rejected  ✓
rejected → approved  ✗ (missing)
```

The handler checked `if status == 'pending'` before allowing the approved transition. That predicate was correct at the time it was written — the original approval workflow only moved operations from the pending queue to approved. Rejection was added later as a separate feature. The rejection-to-approved path was never implemented because the developer who added rejection (me) didn't update the original approval handler's guard clause.

This is a class of bug that static analysis won't catch. The state machine isn't formalized anywhere — it's implicit in the handler logic. There's no diagram that shows the missing arrow. The only way to catch it is to enumerate all possible transitions and test each one, which is exactly what didn't happen.

## The Fix

One-line predicate change: allow the approved transition from both `pending` and `rejected` states. The diff is almost embarrassingly small:

```python
# Before
if operation.status == 'pending':
    operation.status = 'approved'

# After
if operation.status in ('pending', 'rejected'):
    operation.status = 'approved'
```

The test was more substantive than the fix. It verifies the full round-trip: create an operation (pending), approve it, reject it, re-approve it, confirm the operation ends up in the approved set with the correct audit trail. Each transition is asserted individually.

The test also covers the transitions that should remain invalid. You can't move a completed operation back to pending. You can't approve an operation that's been executed. These negative cases existed before — the new test adds them to the same test function so all state machine behavior is documented in one place.

## Why This Bug Survived

The original test suite had excellent coverage for the happy path. "Approve a pending operation" — tested. "Reject a pending operation" — tested. "Execute an approved operation" — tested. All green. 100% of the intended workflow was covered.

The gap was in the reversal paths. Nobody wrote a test for "reject and then change your mind" because the feature spec didn't mention it. The spec said "users can approve or reject pending operations." It didn't say "users can reverse their decisions." The reversal was an implicit user expectation, not an explicit requirement.

This is a pattern worth recognizing. State machines with more than two states almost always have implicit reversal expectations that don't appear in the spec. If your state machine has states A, B, and C with transitions A→B and A→C, users will expect B→C and C→B to work even if nobody asked for them. The spec describes the forward paths. Users live in the full graph.

## The Lesson: Test the Full Graph

When you add a new state to an existing state machine, you need to check every existing transition handler. Not just the handlers for the new state — the handlers for every state that the new state might transition to or from. The checklist is mechanical:

1. List all states (including the new one).
2. For every pair of states, decide: should this transition be allowed?
3. For every allowed transition, verify a handler exists.
4. For every disallowed transition, verify the handler rejects it.

For a three-state machine, that's 6 potential directed transitions. For a four-state machine, it's 12. The combinatorics grow fast but the effort per check is small. This is the kind of review checklist that belongs in the project's contributing guide, not in someone's head.

The alternative is formal state machine libraries that make the transition table explicit — Python has `transitions`, JavaScript has `xstate`. For IntentCAD's single state machine, that's a dependency for a problem that's already solved by a comprehensive test. If the project grows more state machines, the calculus changes.

## v0.12.0 Release

Five commits total: the state machine fix, the round-trip test, a version bump to 0.12.0, the release report, and the after-action review. Small release. Patch semantics — no new features, no breaking changes, just a bug that made the approval workflow incomplete.

The release report follows the same template as every IntentCAD release: what changed, what was tested, what's next. The AAR noted two things: the original test suite had no coverage for state reversals (now closed), and the state machine should probably be extracted into a formal transition table rather than remaining implicit in handler conditionals. That refactor is on the backlog but not urgent — the current codebase has exactly one state machine and it's now fully tested.

Sometimes a five-commit patch release teaches you more about your testing methodology than a thirty-commit feature release. The bug was trivial. The gap in testing philosophy that allowed it to exist was not.

## Related Posts

- [Shipping a CAD Agent from Zero: DXF Parsing, Edit Engines, and LLM Planner Interfaces](/posts/building-cad-dxf-agent-from-zero-to-v010/) — the original v0.1.0 launch
- [IntentCAD v0.8.0 — Thirteen EPICs, One Day](/posts/intentcad-v080-thirteen-epics-one-day/) — the feature push that introduced the approval workflow
- [From Tool to Platform: IntentCAD's Five EPICs in One Day](/posts/from-tool-to-platform-intentcad-five-epics-one-day/) — earlier architecture evolution
