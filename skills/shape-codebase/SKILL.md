---
name: shape-codebase
description: Review and reshape an existing software codebase through scoped investigation, evidence-backed findings, target architecture design, approval-gated remediation slices, and validation. Use when the user wants a repository-wide code review, asks what should be fixed or reorganized, wants to improve module boundaries or project structure, needs a refactor roadmap, or wants an existing codebase incrementally brought toward a clearer architecture.
---

# Shape Codebase

Turn an existing repository into an understood, prioritized, and incrementally
improved codebase. Treat the running code, tests, configuration, and repository
history as evidence; do not infer the intended design from folder names alone.

## Core contract

- Start by agreeing on the review objective, scope, fixed revision, constraints,
  and desired outcome: findings only, target design, or implemented repairs.
- Keep review, investigation, findings, target design, and remediation planning
  strictly read-only. Approval for any of those stages does not authorize a
  repository change.
- Maintain a visible stage ledger with stable IDs, scope, deliverables,
  validation, and status.
- Use these statuses: `proposed`, `approved`, `in_progress`, `completed`,
  `blocked`, and `skipped`.
- Require explicit approval before executing every stage's proposed output and
  before making any change. Questions, revisions, and general enthusiasm are
  not approval.
- Before changing anything, present a named remediation slice with its purpose,
  exact behavioral scope, affected files or modules, risks, exclusions, and
  validation. Yield and wait for the user to approve that slice explicitly.
- Treat broad requests such as "fix everything" or approval of the target design
  as intent to continue planning, not approval of unspecified changes.
- Separate observed facts, interpretations, recommendations, assumptions, and
  unresolved decisions.
- Support every finding with a precise code location or reproducible behavior.
  Do not report taste, novelty, or theoretical purity as defects.
- Rank findings by consequence, not by ease of implementation or visual
  prominence in the code.
- Preserve sound conventions unless evidence shows they create a problem.
- Design deep modules: substantial behavior behind a small interface, placed at
  a justified seam and tested through the same interface callers use.
- Implement only approved remediation slices. Do not hide unrelated cleanup in
  a nearby change.
- Validate each implemented slice and the integrated system before declaring
  the codebase improved.

Read-only investigation inside an approved review stage does not need separate
approval. Before approval of a named remediation slice, do not create, edit,
delete, move, rename, format, or generate files; install or update dependencies;
update snapshots or lock files; run migrations or fix-mode tools; or mutate
databases, remote systems, repository state, or other external state. Include
any necessary mutation in the slice proposal rather than treating it as an
incidental implementation or validation step.

## Load supporting guidance

- Read [references/investigation.md](references/investigation.md) before mapping
  the repository, selecting review tracks, or drawing conclusions from tests,
  documentation, or history.
- Read [references/architecture-review.md](references/architecture-review.md)
  before evaluating module depth, interfaces, seams, dependency direction,
  project structure, or a target design.
- Read [references/findings.md](references/findings.md) before recording,
  prioritizing, deduplicating, or presenting findings.
- Read [references/remediation.md](references/remediation.md) before proposing a
  remediation plan or changing code.

## Working ledger

Use the task plan as the ledger when one exists. Otherwise keep the ledger in
the conversation; do not create a tracking file solely for workflow state.

| ID | Stage | Approved output |
| --- | --- | --- |
| `SC-1` | Review contract | Scope, revision, constraints, questions, and review mode |
| `SC-2` | Repository map | Behavior, module, dependency, data, operations, and test map |
| `SC-3` | Findings | Verified, prioritized findings and strengths |
| `SC-4` | Target design | Recommended module design, dependency strategy, and placement changes |
| `SC-5` | Remediation plan | Dependency-aware, approval-ready change slices |
| `SC-6.n` | Remediation slice | One tested, integrated improvement |
| `SC-7` | Integration | Validated system and concise handoff |

Skip `SC-4` through `SC-7` when the user asks only for a review. Skip a stage
only when it is genuinely irrelevant and record why.

## Stage protocol

For every stage:

1. In a read-only proposal phase, reconcile the ledger with confirmed decisions
   and repository evidence already available in the approved scope.
2. Ask only questions whose answers materially change the stage and prepare its
   proposed output without changing repository or external state.
3. Present the proposed scope, output, validation, exclusions, and risks.
4. Request explicit approval and yield.
5. After approval, mark the stage `approved`, then `in_progress` when work starts.
6. Perform only the approved work and run the smallest relevant validation.
7. Report evidence, limitations, and conflicts; mark the stage `completed`,
   `blocked`, or `skipped`.
8. Propose the next stage without beginning it.

Steps 1 through 4 prepare and present a proposal; they do not execute the stage
and require no approval beyond any already-approved read-only investigation
they rely on. Approval moves the stage from proposal into execution. This lets
the user inspect the complete proposed scope before deciding whether it may run.

If new evidence invalidates an approved finding or design, correct the ledger
and explain the change. Do not preserve a conclusion for narrative consistency.

For `SC-1` through `SC-5`, "perform the approved work" means read-only analysis
and planning. Only an explicitly approved `SC-6.n` remediation slice authorizes
changes, and only within that slice's described scope. If several slices are
pending and the user gives ambiguous approval, ask which slice they approve.
One explicit approval of a complete named slice satisfies both the stage and
change gate; do not request duplicate approval. Treat a response such as "yes,"
"do it," or "proceed" as approval only when exactly one complete slice proposal
is pending and the response clearly answers that proposal.

## SC-1: establish the review contract

Clarify the reason for the review and the decisions it should enable. Define:

- repositories, packages, directories, and generated or vendored exclusions;
- the fixed commit, branch, worktree state, or supplied artifact under review;
- desired behavior or specification sources when available;
- supported environments and operational constraints;
- risk priorities such as correctness, maintainability, performance, security,
  testability, migration safety, or reader navigability;
- whether the requested outcome is findings only, target design, a remediation
  plan, or approved implementation.

Record pre-existing uncommitted changes and preserve them. If scope is broad,
recommend a bounded first pass rather than silently sampling the repository.

## SC-2: map the repository

Follow [references/investigation.md](references/investigation.md). Trace primary
user or system workflows from entry point to observable outcome. Identify
module ownership, interfaces, dependency direction, persistence, external
systems, lifecycle behavior, configuration, generated sources, and validation
commands.

For a non-trivial repository, use independent read-only review tracks when
agents are available and their scopes can be separated cleanly. Suitable tracks
include behavior and failure handling, module design and dependencies, tests
and change safety, and operations or data lifecycle. The coordinating agent
must inspect the evidence itself and resolve overlap; independent reports are
leads, not verified findings.

Do not confuse directory layout with architecture. Produce a concise repository
map that explains how behavior actually flows and where important knowledge is
owned or duplicated.

## SC-3: verify and present findings

Follow [references/findings.md](references/findings.md). Test each suspected
problem against callers, tests, configuration, and runtime behavior. Prefer a
small set of material findings over a long inventory of speculative cleanup.

Present findings in descending priority and include strengths worth preserving.
Every finding must state the consequence, evidence, affected surface, proposed
direction, confidence, and focused validation. Clearly label anything that
could not be reproduced or confirmed.

Stop here for a findings-only review.

## SC-4: design the target codebase

Follow [references/architecture-review.md](references/architecture-review.md).
Design from approved findings and desired behavior, not from a preferred
pattern. For non-trivial changes, compare genuinely different module designs
and recommend one or a deliberate hybrid.

Show:

- module ownership and external interfaces;
- typical caller flows and important error paths;
- dependency direction and justified seams;
- persistence, external adapters, lifecycle, and operational consequences;
- test strategy through module interfaces;
- current-to-target responsibility mapping;
- complete affected directory tree and placement rationale;
- compatibility, migration, rollout, and deletion implications.

Do not create abstractions for hypothetical variants. One production adapter
and one test adapter can justify a seam; one implementation alone usually does
not.

## SC-5 and SC-6.n: plan and apply remediation

Follow [references/remediation.md](references/remediation.md). Divide the target
design into independently valuable vertical slices. Each slice must identify:

- linked finding IDs and observable improvement;
- owned files and interfaces;
- prerequisites and compatibility strategy;
- tests, checks, and rollback or recovery considerations;
- documentation impact;
- explicitly excluded cleanup.

After a slice is approved, characterize existing behavior where needed, make
the smallest coherent change, inspect the actual diff, and run focused
validation. Remove superseded code and tests when the new interface fully owns
their behavior; do not leave permanent transitional layers without a named
reason and removal condition.

If implementation or validation reveals a required change outside the approved
slice, stop without making that change. Report the dependency or failure and
propose a revised or additional slice for explicit approval.

## SC-7: integrate and hand off

Validate important successful workflows, failures, lifecycle behavior,
configuration, build, tests, and migrations within the approved scope. Inspect
the final tree for duplicate abstractions, misplaced responsibilities, orphaned
files, stale documentation, unexplained configuration, and unremoved
transitional code.

Trace completed changes back to finding IDs. Finish with:

- what materially improved and what was deliberately preserved;
- primary module interfaces and entry points;
- validation performed and its results;
- unresolved findings, limitations, and operational caveats;
- any follow-up work that still requires a separate decision.

Do not invent further refactoring merely to keep the workflow active.
