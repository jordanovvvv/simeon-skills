---
name: sub-router
description: Decide whether a subagent is worthwhile, select the appropriate specialist, and define a minimal task contract. Use before delegating code search, research, review, testing, or other bounded subagent work.
---

# Sub-Router

Choose whether to delegate and, if so, make the purpose and bounds explicit.
The router is a decision skill, not a reason to create a subagent.

## Decision rule

Delegate only when isolation, parallel exploration, or a specialized context
will save more work than the setup and handoff cost.

Choose direct work when the answer is already in context, the user provides an
exact file or location, or a small bounded check can answer the question. Do
not delegate merely to avoid reading a file or running a simple search.

## Routing loop

1. State the objective in one sentence and identify the smallest evidence
   needed for a decision.
2. Classify the task:
   - **Direct** — known context, exact paths, or a small bounded lookup.
   - **Isolated search** — broad or uncertain code discovery; route to
     `sub-graper`.
   - **Specialist work** — a named available skill or distinct expertise can
     resolve the task more reliably than the main conversation.
   - **Independent parallel exploration** — only when two or more independent
     questions must be answered and parallel results materially reduce total
     work.
3. Compare the expected savings with setup, context transfer, result review,
   and coordination cost. If the saving is not clear, choose direct work.
4. If delegating, select one specialist or a small set of independent
   specialists. Name each specialist's purpose; do not create duplicate or
   competing work.
5. Send each delegated task a minimal contract and enforce its stop condition.
6. Review the concise result, make the final decision in the main conversation,
   and record only reusable conclusions—not raw tool output or agent process.

## Delegation contract

Every delegated task receives only:

- objective;
- relevant paths or source material;
- a hard turn and tool budget;
- desired output shape;
- stop condition.

Never forward the full main conversation by default. Include only facts that
materially affect the work. Start with one turn and permit another only when a
specific unresolved question remains. Ask for at most the evidence needed for
the final decision.

## Specialist selection

- Route broad or ambiguous code-location and implementation-flow questions to
  `sub-graper`.
- Route work to another specialist only when that skill or agent is available
  and its narrower context materially improves the outcome.
- Use parallel delegates only for independent questions; otherwise use one
  delegate that can perform tool calls in parallel within its task.
- If no specialist qualifies, keep the work direct.

## Decision record

Before delegation, retain a compact internal record:

```text
Decision: direct | delegate
Purpose: <why isolation or specialization saves work>
Route: <specialist, if delegated>
Budget: <turns and tools>
Stop: <sufficient result condition>
```

Do not turn this record into user-facing ceremony unless the user asks how the
work will be handled.

## What not to do

- Do not delegate a simple, bounded task by default.
- Do not dispatch multiple agents to discover the same answer.
- Do not use a subagent as a substitute for making the final decision.
- Do not continue an agent after its stop condition is met.
