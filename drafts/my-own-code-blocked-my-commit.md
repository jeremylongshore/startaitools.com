+++
title = "My Own Code Blocked My Commit Today. That Was the Point."
slug = "my-own-code-blocked-my-commit"
date = 2026-07-20T09:00:00-05:00
draft = true
tags = ["governance", "typescript", "ai-agents", "seam", "guardrails", "claude-code"]
categories = ["Development Journey"]
description = "I added a firewall so an AI model's score can never decide what becomes durable. Then a second guardrail I had already written refused to let me commit the first one. Both refusals are the same idea: govern by code, not by discipline."
+++

I spent this morning making it impossible for a model to decide what my system remembers. Then a piece of governance I wrote weeks ago refused to let me ship it. Both things are the same idea, so this is a short note about what it looks like when your own rules stop you, on purpose.

The system is a governed knowledge base. It has one hard rule, the whole product really: the model proposes what is worth remembering, but deterministic code decides what actually becomes durable. Above a line, a model retrieves, ranks, reranks, suggests. Below that line, only plain code writes durable state, and every write leaves a receipt. The line is the product. Everything else is commodity.

The problem with a line like that is it lives in your head. A code reviewer can enforce it on a good day. On a bad day, someone adds a reranker, wires its score into the thing that decides what gets promoted, the demo works, and the line is gone. Quietly. That is the failure I care about most, because it does not show up as a bug. It shows up as a system that looks fine and is no longer the thing you built.

## Make the wrong thing not compile

So today's work was to move that rule out of my head and into the type system. The govern side scores candidates with deterministic rules (things like content length, source trust, relevance by structure). Those scores were plain numbers. A rerank score is also a plain number. Nothing stopped one from standing in for the other.

The fix is a branded type:

```ts
export type DeterministicScore = number & {
  readonly __brand: 'deterministic-govern-score';
};

export function deterministicScore(value: number): DeterministicScore {
  return value as DeterministicScore;
}
```

Then the govern result stops accepting a raw number:

```ts
export interface RuleResult {
  outcome: 'pass' | 'fail' | 'flag';
  reason: string;
  score?: DeterministicScore; // was: number
}
```

A `DeterministicScore` is still a number at runtime. It reads like a number, adds like a number, costs nothing. But a plain `number` is no longer assignable to it. The only way to mint one is the factory, which lives inside the govern package and imports nothing from retrieval. So a rerank score, a plain number produced above the line, cannot be placed where a govern decision reads it. The compiler says no.

I did not have to go find the places this rule was being relied on. The typecheck did. The moment I changed the type, the build lit up with the three deterministic rules that produce a score, each now failing because it was handing a raw number to a branded field. That is the tell that this was the right move: the type surfaced every producer automatically, and every one of them is deterministic govern code that should have been going through the factory all along. Retrieval was not on that list, because retrieval cannot reach the factory. That is the firewall.

I paired it with a dependency rule so the barrier is not just a type. The govern package is now forbidden from importing the retrieval package at all. Type barrier plus import barrier: a rerank score cannot become a govern score, and the module that could produce one cannot even be imported into the room where the decision happens.

The test is the part I like. It does not run anything. It just refuses to compile if the firewall ever breaks:

```ts
it('a raw number cannot be a govern score', () => {
  const rerankScore = 0.99;
  // @ts-expect-error a raw number cannot become a DeterministicScore
  const forbidden: DeterministicScore = rerankScore;
  void forbidden;
});
```

If a future change ever made a plain number assignable to a govern score, that `@ts-expect-error` would report an unused directive and fail the build. The test passes only as long as the wrong thing stays impossible.

## Then my own guardrail stopped me

Here is the part that made me laugh. I staged the change, wrote the commit, and the commit was blocked. Not by a linter complaining about style. By a governance tripwire I had written earlier and forgotten about:

```
policy-hash: POLICY_TAMPERED: governance ruleset has changed without --init

  A staged file under packages/policy-engine/src/rules/ has changed,
  but .policy-hash no longer matches the current files.

  Commit BLOCKED.
```

The rules directory holds the code that decides what is allowed to become durable. It is the most sensitive code in the system, so it has a hash pin. Any change to a governance rule fails the commit unless you deliberately re-pin the manifest, which forces you to stop and acknowledge that you are editing governance code, not ordinary code. I had changed three rule files to route their scores through the factory. Innocent change. The tripwire does not know innocent. It knows the govern ruleset moved, and it stopped the commit until I re-pinned it on purpose.

So in one morning, two different mechanisms refused to let a mistake through. One refused to let a model score touch a durable decision. The other refused to let me change governance code without saying so out loud. Neither is a policy document. Neither is a code-review checklist. Both are code that runs.

## The lesson, net net

Everyone building AI memory says the model helps decide what to keep. The interesting question is not whether the model helps. It is whether the model can be stopped, structurally, from being the thing that decides. A rule you enforce with discipline is a rule you will break the week you are tired. A rule the compiler enforces is a rule you cannot break without noticing.

I ran kitchens for years before I wrote production code. A line check is not a suggestion. If the station is not ready, you do not open, and the rule does not care how good you feel about the station. The seam between what a model proposes and what code makes durable is a line check. Today it stopped me twice. That is not friction. That is the system working exactly as designed, on the person most likely to cut the corner: me.

Related: [the plan for who decides what is durable](/posts/who-decides-what-is-durable/) and the receipts that back it.
