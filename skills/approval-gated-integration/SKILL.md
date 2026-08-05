---
name: approval-gated-integration
description: Guide codebase features, refactors, migrations, and architectural changes through explicit approval-gated steps. Use when the user asks to work step by step, approve each stage, review suggested changes before application, incrementally integrate a feature, or optionally document the completed implementation.
---

# Approval-Gated Integration

Guide the user through incremental implementation while keeping them in control of material changes.

## Core contract

- Inspect the codebase before proposing implementation steps.
- Divide the work into small, coherent, independently verifiable steps.
- Explain the purpose, affected areas, risks, and expected outcome of each step.
- Wait for explicit user approval before applying a proposed step.
- Apply only the approved step or explicitly approved group of steps.
- Do not include optional improvements inside an approved step without authorization.
- Run focused validation after every implemented step.
- Run complete integration validation after the final implementation step.
- Preserve unrelated user changes.

Do not request approval for read-only inspection, analysis, or validation within the approved scope.

Do not require approval for every individual file edit inside an approved step. Approval applies to the described behavioral scope.

## Working loop

Repeat this loop until the objective is complete:

1. Inspect the current implementation and relevant tests.
2. Describe the next proposed step:
   - objective;
   - behavioral changes;
   - files or modules likely affected;
   - schema or migration implications;
   - validation to run;
   - important tradeoffs.
3. Separate required work from optional suggestions.
4. Yield to the user and request explicit approval.
5. When approved, mark the step in progress.
6. Implement only the approved scope.
7. Run focused tests and relevant static checks.
8. Report:
   - what changed;
   - observable behavior;
   - validation result;
   - any discovered concern;
   - the next proposed step.
9. Wait for approval again.

If the user approves multiple named steps, implement them sequentially and validate each before moving to the next approved step.

## Interpreting user responses

Treat responses such as these as approval:

- “Yes.”
- “Do it.”
- “Apply step 2.”
- “Continue with steps 4 and 5.”
- “Proceed with the proposed change.”

Treat questions, concerns, and requests for explanation as discussion, not approval.

When the user asks a question about the proposed step:

1. Answer it directly.
2. Adjust the proposal if the answer changes the design.
3. Continue waiting for approval.

If the user rejects or modifies a proposal, update the plan without applying the rejected behavior.

## Suggested changes

At each approval boundary, distinguish:

- **Required now** — necessary to achieve the stated objective safely.
- **Suggested later** — useful improvements outside the current approved scope.
- **Operational caveats** — deployment, concurrency, migration, compatibility, or maintenance concerns.

Never silently implement a “suggested later” item.

If implementation reveals a materially different requirement, stop and propose it as a new step.

## Design and migration rules

- Keep the database migration as the production schema source of truth.
- Use model annotations for persistence mapping, not as a substitute for migrations.
- Use expand/backfill/contract migrations when moving existing data.
- Preserve compatibility until the approved cleanup step.
- Place events in the repository’s established events package.
- Follow existing module, repository, DTO, and test conventions.
- Prefer small interfaces that hide indexing, persistence, scoring, or synchronization complexity.
- Keep high-frequency observations separate from content update timestamps.

## Validation

After each step, run the smallest relevant checks, such as:

- focused unit tests;
- persistence or migration tests;
- concurrency tests;
- linting;
- type checking.

After the final implementation step, validate the complete workflow:

- creation or capture;
- approval;
- runtime use;
- updates;
- cache or index refresh;
- usage recording;
- deactivation and deletion;
- fallback behavior;
- migration consistency;
- backend test suite;
- frontend production build when affected;
- repository diff and whitespace checks.

Do not report the integration as complete until required validation passes. Clearly report checks that could not be run.

## Documentation

Do not automatically create documentation unless the user requests it.

When the user requests documentation:

1. Inspect existing documentation conventions and indexes.
2. Read the final implementation and tests as the source of truth.
3. Document current behavior, not abandoned plans or speculative behavior.
4. Cover only relevant topics, potentially including:
   - purpose;
   - domain model;
   - lifecycle;
   - matching or processing flow;
   - invariants;
   - administration;
   - endpoints;
   - migrations;
   - operational caveats;
   - implementation map;
   - validation coverage.
5. Distinguish current limitations from future recommendations.
6. Add the document to an existing documentation index when appropriate.
7. Validate Markdown formatting and local links.

If the user asks only for a documentation proposal or draft outline, present it and wait for approval. If the user directly asks to create the document, treat that request as approval for the documentation step.

## Completion

At completion, provide a concise handoff containing:

- implemented outcome;
- important architectural behavior;
- migrations added;
- validation performed;
- unresolved operational caveats;
- links to primary implementation and documentation files.

Do not propose additional implementation merely to keep the workflow active.