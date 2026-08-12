---
name: shape-project
description: Create new software projects from a user-defined motive through clarification, domain modeling, architecture design, approval-gated scaffolding, delegated implementation, validation, and minimal documentation. Use when the user wants to start a codebase from scratch, turn an application idea into an explicit structure, or build a new project step by step with approval before every material stage.
---

# Shape Project

Turn an initial motive into a working, navigable codebase through explicit
decisions and approved stages. Keep the user in control of scope while using
independent agents where they materially improve discovery, design, or delivery.

## Core contract

- Begin with the user's motive. Do not begin by choosing a framework or creating
  files.
- Clarify only information that changes product behavior, architecture,
  operations, or acceptance.
- Maintain a visible stage ledger with stable IDs, scope, deliverables,
  validation, and status.
- Use these statuses: `proposed`, `approved`, `in_progress`, `completed`,
  `blocked`, and `skipped`.
- Require explicit approval before entering every material stage. Treat
  questions and requested revisions as discussion, not approval.
- Perform only the approved stage. Do not bundle optional features or future
  improvements into it.
- Present the complete proposed directory tree and placement rationale before
  creating the project structure.
- Divide work by cohesive modules and independent outcomes, never by arbitrary
  file counts.
- Give concurrent writing agents disjoint file ownership. Keep shared files and
  integration under the coordinating agent.
- Validate every implemented slice and the complete application before calling
  the project finished.
- Keep documentation small, current, and navigable. Do not create speculative
  documentation or empty directory scaffolds.

Clarification and read-only investigation inside the current stage do not need
separate approval. Approval applies to the stage's described outcome, not to
each question, tool call, or file edit.

## Load supporting guidance

- Read [references/discovery.md](references/discovery.md) while clarifying the
  motive, requirements, technology, or domain language.
- Read [references/architecture.md](references/architecture.md) before proposing
  architecture, the directory tree, file placement, or project documentation.
- Read [references/delegation.md](references/delegation.md) before spawning
  independent agents or dividing implementation work.

## Working ledger

Use the task's plan or checklist as the ledger when one exists. Otherwise keep
the ledger in the conversation until the project is created. Do not add a
tracking file merely to hold workflow status.

Use these stable stages:

| ID | Stage | Approved output |
| --- | --- | --- |
| `SP-1` | Motive | Motive brief |
| `SP-2` | Requirements | Prioritized behavior and acceptance criteria |
| `SP-3` | Technology | Technology and operational decisions |
| `SP-4` | Domain | Canonical language, scenarios, and invariants |
| `SP-5` | Architecture | Chosen module design and dependency strategy |
| `SP-6` | Structure | Directory tree, placement manifest, and project foundation |
| `SP-7` | Delivery plan | Dependency-aware implementation slices |
| `SP-8.n` | Implementation slice | Tested vertical behavior |
| `SP-9` | Integration | Validated application and concise handoff |

Skip a stage only when it is genuinely irrelevant and record why. Do not treat
silence, earlier approval of another stage, or approval of the overall idea as
approval of a later stage.

## Stage protocol

For each stage:

1. Reconcile the ledger with confirmed decisions and existing artifacts.
2. Ask focused questions until the stage's exit criteria are satisfied.
3. Separate confirmed facts, recommendations, assumptions, and unresolved
   decisions.
4. Present the proposed output, affected artifacts, validation, risks, and
   material trade-offs.
5. Request explicit approval and yield.
6. After approval, mark the stage `approved`, then `in_progress` when work
   starts.
7. Perform only the approved scope.
8. Run the smallest relevant validation.
9. Report the result and mark the stage `completed`, `blocked`, or `skipped`.
10. Propose the next stage and wait again.

If implementation reveals a materially different requirement or architectural
need, stop the current slice and propose a revision or a new stage. Do not hide
the change inside already-approved work.

## SP-1 through SP-4: discover the project

Follow [references/discovery.md](references/discovery.md). Move from why the
project should exist to what it must do, then select technology, then sharpen
the domain language. Recommend sensible defaults instead of making the user
invent every technical detail.

Keep approved decisions in the conversation until `SP-6` creates the project.
Do not create `PROJECT.md`, `CONTEXT.md`, or other files merely because a term or
requirement was discussed.

## SP-5: design the architecture

Follow [references/architecture.md](references/architecture.md). For a
non-trivial project, use independently produced alternatives after `SP-5` is
approved for exploration. Compare them by interface depth, locality, seam
placement, dependency direction, testability, operations, and reader
navigability. Recommend one design or a clearly explained hybrid.

Prefer cohesive modules with small interfaces and substantial behavior behind
them. Do not force every behavior into a class. Use a class when identity,
state, invariants, or lifecycle justify it; otherwise prefer a function or
module. Add a seam only when behavior genuinely varies across it.

## SP-6: approve placement before scaffolding

Present both the complete proposed tree and a placement manifest before writing
the project foundation. For every proposed file, identify its owner, purpose,
closest structural relationship, allowed dependencies, test location, and why
the responsibility does not belong in another proposed file.

After approval:

- Create only directories that immediately contain approved files.
- Create configuration through the selected ecosystem's standard mechanism.
- Create the minimum project documentation described in
  [references/architecture.md](references/architecture.md).
- Run installation, compilation, lint, or smoke validation appropriate to the
  approved foundation.
- Report generated files separately from authored files.

Do not initialize external services, deploy, publish, push, or create remote
resources unless the user explicitly approves those effects.

## SP-7 and SP-8.n: plan and implement vertical slices

Build a dependency-aware work graph whose slices produce observable behavior.
Avoid plans made only of technical layers such as "models, then repositories,
then controllers" unless the technology requires that order.

For each slice, state:

- behavior and linked requirement IDs;
- owned modules and files;
- interface or data-contract changes;
- dependencies and prerequisites;
- focused validation;
- integration and documentation impact;
- risks and excluded optional work.

Use [references/delegation.md](references/delegation.md) when a slice contains
independent work. After integrating worker results, inspect the actual diff and
run validation from the coordinating agent. Never accept a worker's success
claim as validation evidence by itself.

## SP-9: integrate and hand off

Validate the complete user workflow, important failures, lifecycle behavior,
configuration, build, tests, and documentation links. Inspect the final tree for
misplaced responsibilities, duplicate abstractions, orphaned files, empty
directories, and unexplained configuration.

Trace implemented behavior back to approved requirement IDs. Report anything
approved but not implemented, implemented but not approved, or not validated.

Finish with a concise handoff containing:

- the working outcome;
- how to run, test, and configure it;
- the module map and primary entry points;
- validation performed;
- remaining limitations or operational caveats.

Do not invent additional work merely to keep the workflow active.
