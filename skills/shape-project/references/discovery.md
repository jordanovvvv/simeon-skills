# Project Discovery

Use this guide for `SP-1` through `SP-4`. Ask one small group of related
questions at a time. Explain why an answer matters when the consequence is not
obvious, and recommend a default when the user is unlikely to have a useful
preference.

## Question discipline

- Distinguish product decisions from technical decisions.
- Ask about desired outcomes before features and features before technology.
- Prefer concrete scenarios over abstract labels.
- Do not ask the user for information that can be safely inferred or inspected.
- Surface assumptions explicitly and label their confidence.
- Challenge conflicting terms and requirements immediately.
- Do not recommend a delivery platform, technology stack, architecture, or
  detailed feature bundle during `SP-1`. Defer feature design to `SP-2` and
  technology choices to `SP-3`.
- Do not turn discovery into an exhaustive questionnaire. Stop when remaining
  uncertainty no longer changes the current stage's output.

## SP-1: motive

Clarify:

- the problem or opportunity;
- the people or systems affected;
- the outcome that would make the project worthwhile;
- the smallest useful version;
- explicit non-goals;
- business, legal, time, cost, privacy, accessibility, or operational
  constraints;
- observable measures of success.

When the initial motive is vague, respond with motive questions rather than a
candidate solution. Do not fill missing context with a recommended web, mobile,
desktop, CLI, or service form. Use examples only to disambiguate a question,
label them as examples, and avoid presenting them as the proposed product.

Produce a motive brief:

```md
# Motive brief

Purpose:
Primary users:
Desired outcome:
Success evidence:
Initial scope:
Non-goals:
Constraints:
Assumptions:
Unresolved decisions:
```

Exit only when the purpose, user, outcome, and scope boundary are specific
enough to reject at least one plausible but unsuitable feature.

## SP-2: requirements

Walk through the primary successful scenario first, then important variations
and failures. Clarify:

- actors and permissions;
- triggers, inputs, outputs, and state changes;
- persistent data and ownership;
- error, retry, cancellation, and recovery behavior;
- external systems and offline or degraded behavior;
- security, privacy, accessibility, performance, and scale expectations;
- administration, observability, migration, or import needs;
- acceptance evidence.

Assign stable identifiers such as `FR-001` to approved behaviors. Write each
requirement as an observable outcome, followed by concise acceptance criteria.
Prioritize requirements as required now or suggested later; do not mix them in
one approved scope.

Exit only when the smallest useful end-to-end workflow, its significant failure
cases, and the definition of done are testable.

## SP-3: technology and operations

Derive technology from the approved motive and requirements. Clarify only
choices whose consequences matter, including:

- target platforms and supported environments;
- deployment and hosting constraints;
- language or ecosystem constraints;
- persistence and consistency needs;
- integration protocols;
- authentication and authorization;
- expected load and latency;
- maintenance skill, budget, and portability;
- required licensing or compliance.

Recommend a primary option with reasons. Present alternatives only where a real
trade-off exists. Verify current versions and official compatibility before
locking dependencies during scaffolding.

Record decisions, consequences, and deferred choices. Do not select libraries
for requirements that have not been approved.

## SP-4: domain language

Identify domain-specific nouns, actions, states, events, identifiers, and
invariants. Resolve overloaded terms by choosing one canonical term and listing
terms to avoid.

Stress-test the model with concrete scenarios:

- the ordinary successful case;
- the smallest and largest valid case;
- duplicate or repeated actions;
- invalid ordering or timing;
- partial failure and recovery;
- concurrent actions;
- deletion, cancellation, expiry, or reversal where relevant.

Keep `CONTEXT.md` as a glossary only when it is created in `SP-6`. Put behavior
and acceptance in `PROJECT.md`; put implementation decisions in
`ARCHITECTURE.md`; reserve ADRs for decisions that are hard to reverse,
surprising without context, and based on a real trade-off.

Exit only when approved requirements can use the canonical language without
ambiguity and the important invariants are explicit.

## Conflict handling

When two approved statements conflict, quote or summarize both, explain the
behavioral consequence, and ask the user to resolve the conflict. Never choose
the newer, more detailed, or easier statement silently. Update the affected
stage output and request approval again when the resolution materially changes
it.
