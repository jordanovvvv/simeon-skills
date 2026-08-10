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

## Step granularity

Default to one architectural layer per step (e.g. schema, then service, then API), unless those layers are tightly coupled and cannot be independently verified — in that case, combine them into a single step and say so explicitly in the proposal. A step should always be independently revertable and independently testable; if a step can't be validated on its own, it's sized wrong and should be split or merged.

## Progress tracking

Maintain a progress ledger from the first proposal through completion. Give every step a stable ID and record its scope, status, validation, and result. Use these statuses consistently: `proposed`, `approved`, `in_progress`, `completed`, `blocked`, and `skipped`.

- Use the task's built-in plan or checklist as the default ledger when one is available.
- **Default fallback:** when no built-in ledger and no repository issue/PR tracking system exists, maintain the ledger in-conversation. This requires no approval — it's the default, not an escalation.
- Only propose a durable repository artifact (issue, PR description, planning doc) — and get approval before creating or modifying it — when the work explicitly needs to survive across sessions or beyond this conversation.
- Do not add an ad hoc tracking file to the repository by default.
- Update the ledger when proposing or revising a step, receiving approval, starting implementation, and completing validation.
- When resuming interrupted work, reconcile the ledger with the codebase and latest validation evidence before continuing. Do not treat an unrecorded step as approved.

## Working loop

Repeat this loop until the objective is complete:

1. Inspect the current implementation and relevant tests, then reconcile the progress ledger.
2. Add or update the next `proposed` step in the ledger and describe it:
   - objective;
   - behavioral changes;
   - files or modules likely affected;
   - schema or migration implications;
   - validation to run;
   - important tradeoffs.
3. Separate required work from optional suggestions.
4. Yield to the user and request explicit approval.
5. When approved, record it as `approved`, then mark it `in_progress` when implementation starts.
6. Implement only the approved scope.
7. Run focused tests and relevant static checks.
8. Record the validation result, mark the step `completed` or `blocked`, and report:
   - what changed;
   - observable behavior;
   - validation result;
   - any discovered concern;
   - the next proposed step.
9. Wait for approval again.

If the user approves multiple named steps, implement them sequentially and validate each before moving to the next approved step.

## Interpreting user responses

Treat responses such as these as approval:

- "Yes."
- "Do it."
- "Apply step 2."
- "Continue with steps 4 and 5."
- "Proceed with the proposed change."

Treat questions, concerns, and requests for explanation as discussion, not approval.

**Partial approval.** If the user approves part of a proposed step but not all of it (e.g. "do step 2 but skip the migration part"), do not record or implement anything yet. Ask a clarifying question to pin down the resulting scope, then re-propose the adjusted step for approval before implementing.

**Outright rejection.** If the user declines a proposed step without offering a modification, remove it from the ledger entirely rather than marking it `skipped`. It was never approved, so it isn't part of the work's history — the ledger should reflect what was done and what's pending, not a log of declined ideas. (If the rejection carries a reason the user wants preserved for later, note that only if the user asks you to.)

**Silence or topic change.** If the user moves on without responding to a proposed step, leave it as `proposed` and don't chase it. If the user later returns to the topic, mention the still-pending step once before continuing, then drop it if they don't engage with it again.

**Ambiguous approval target.** If more than one step is pending at once (for example, a new step was proposed before the user replied to an earlier one) and the user replies with a bare approval like "yes," do not guess which step it applies to. Ask which step the approval refers to before recording or implementing anything.

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

Never silently implement a "suggested later" item.

If implementation reveals a materially different requirement, stop and propose it as a new step.

**Dependencies discovered mid-implementation.** If implementing an approved step turns out to require touching something outside the approved scope (e.g. adding a column turns out to require an unapproved migration file), stop immediately. Do not implement the dependency. Mark the current step `blocked`, explain what was discovered and why it's out of scope, and propose the dependency as a new step for approval.

## Repository-aware design and migration rules

- Discover the repository's architecture, persistence, migration, event, naming, and test conventions before proposing a design.
- Follow established conventions unless the objective requires changing them. Explain and seek approval for material deviations.
- Use the repository's established schema-management mechanism and source of truth. Keep code-level mappings, generated schemas, and migrations consistent where applicable.
- Choose a migration strategy from the actual data volume, deployment model, rollback needs, and compatibility constraints. Use a staged pattern such as expand/backfill/contract only when those constraints warrant it, not as a universal default.
- Preserve backward compatibility only where consumers or deployment sequencing require it. Make later cleanup a separate approved step when appropriate.
- Place events, interfaces, DTOs, repositories, and tests according to the repository's existing module boundaries rather than assuming a particular package layout.
- Prefer interfaces that hide meaningful implementation complexity without adding abstractions the codebase does not need.
- Do not overload one field with distinct domain meanings. Model timestamps and other state according to their actual semantics and the repository's conventions.

## Validation

After each step, run the smallest relevant checks, such as:

- focused unit tests;
- persistence or migration tests;
- concurrency tests;
- linting;
- type checking.

**On validation failure.** If a focused check fails partway through an approved step, do not attempt a fix unilaterally. Mark the step `blocked`, report the failure to the user, and ask whether the fix should be treated as part of the current step (same approval, continue) or proposed as a new step. Proceed only once the user has indicated which.

After the final implementation step, validate the complete workflow:

- the primary end-to-end behavior;
- affected lifecycle operations, such as creation, updates, and deletion;
- relevant failure, fallback, rollback, and compatibility behavior;
- schema and data consistency when persistence is affected;
- relevant test suites and production builds for affected components;
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
   - main processing flow;
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

Each step's report (step 8 of the working loop) already covers what changed, observable behavior, and validation results for that step — the completion handoff should not repeat those per-step details. Instead, provide a concise handoff that synthesizes across the whole ledger:

- overall outcome, in terms of the original objective (not a re-listing of each step);
- important architectural behavior that spans multiple steps, if any;
- unresolved operational caveats collected across all steps;
- links to the primary implementation and documentation files, and to the ledger itself if it lives in a durable location.

If the user wants the full change-by-change detail, point them to the ledger rather than reproducing it in the handoff.

Do not propose additional implementation merely to keep the workflow active.
