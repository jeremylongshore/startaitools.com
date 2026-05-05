+++
title = 'Tests That Actually Catch Regressions'
weight = 20
date = 2026-05-05T08:00:00-05:00
description = 'Chapter two — what an "anti-slop" test framework looks like in practice, and three real bugs it caught inside its own implementation.'
+++

**Source post:** [Anti-slop framework finds three bugs inside itself](/posts/anti-slop-framework-found-three-bugs-inside-itself/)

A test suite that mocks the function under test is theater. It runs green, it produces coverage numbers, it makes the dashboard look healthy — and it catches nothing. The function it's "testing" never actually executes.

The anti-slop principles are simple and they aren't new. What's new is treating them as a CI gate that an AI agent cannot escape:

- **Don't mock the function under test.** Mock its dependencies; let the function itself run.
- **Use exact assertions, not "is truthy."** A test that passes when the answer is `42` and also when it's `"42"` is not a test.
- **Use asymmetric inputs.** A test on `add(2, 2)` that passes returns `4` from a function that does `a * b` is a tautology.
- **No tautologies.** `assert(x == x)` is not a test, even when `x` is a function call.

## The bugs the framework found in itself

The post linked above documents three real bugs the framework caught when it was first turned loose on its own implementation. The most embarrassing one was a "happy path" test that asserted the wrong field — passed for two months before the framework's own escape-scan flagged it.

The pattern matters more than the specific bugs. **Any test framework worth running gets pointed at itself first.** If it can't catch the slop in its own implementation, it won't catch it anywhere else.

## How this connects to MCP

An MCP server has two test surfaces that matter: the JSON-RPC contract (does the wire format match the spec?) and the tool semantics (does the tool actually do what the docstring claims?). The first is straightforward. The second is where the slop creeps in — and where the anti-slop rules earn their cost.

The next chapter picks up the deploy story: four production-deploy gotchas that the tests didn't catch because they only manifest in the seam between the build and the runtime.
