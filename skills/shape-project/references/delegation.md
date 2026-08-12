# Delegation and Integration

Use this guide when independent agents can improve architecture exploration,
research, implementation, testing, or review. Delegation is a means of reducing
uncertainty or elapsed time, not a goal by itself.

## Decide whether to delegate

Delegate when work has independent inputs and outputs, such as:

- alternative architecture designs;
- focused technology or compatibility research;
- vertical slices with disjoint module ownership;
- an independent validation or review pass.

Keep work with the coordinating agent when it changes shared configuration,
central registries, cross-module contracts, migrations, or tightly coupled
files. Sequence tasks whose outputs are prerequisites for other tasks.

## Coordinator responsibilities

The coordinating agent must retain the full motive, approved requirements,
domain language, architecture, stage ledger, and work graph. It must:

- define and approve work packages;
- assign non-overlapping ownership;
- keep shared files unassigned or owned by one designated integrator;
- reconcile contradictory results;
- inspect every resulting change;
- run integration validation;
- report deviations from approved scope.

Do not ask workers to rediscover the project's purpose independently.

## Work graph and ownership

Represent implementation as a dependency graph, not merely a list. A node must
have an observable deliverable, prerequisites, owned files or modules, and
validation. Run nodes concurrently only when neither writes files or contracts
owned by the other.

Maintain an ownership register during each approved implementation slice:

| Work ID | Agent | Owned paths | Shared contracts | Depends on | Validation |
| --- | --- | --- | --- | --- | --- |

Use one coordinator plus the smallest useful number of workers. Prefer three
strong, independent work packages over many tiny assignments.

## Task packet

Give every worker a self-contained packet:

```md
Work ID:
Approved stage and slice:
Motive and user outcome:
Linked requirement IDs:
Relevant domain terms and invariants:
Objective:
Owned files or modules:
Files that must not be changed:
Interfaces and contracts to preserve:
Required inputs and dependencies:
Expected deliverable:
Validation to run:
Return format:
```

Provide relevant source artifacts, not the coordinator's preferred answer, when
asking for alternative designs or independent validation.

## Writing protocol

- Do not begin worker writes before the containing stage or slice is approved.
- Assign disjoint paths before launching concurrent writers.
- Require workers to preserve unrelated changes.
- Stop a worker that discovers a need to cross its ownership boundary.
- Route shared contract changes back to the coordinator for a new proposal.
- Make the coordinator responsible for shared configuration, dependency locks,
  indexes, and final documentation reconciliation.

Workers must return changed paths, observable behavior, validation results,
assumptions, and concerns. A worker may not declare the full slice complete.

## Integration protocol

After workers finish:

1. Confirm that changes stay inside assigned ownership.
2. Inspect interfaces, dependency direction, terminology, and placement.
3. Reconcile duplicated or contradictory implementations.
4. Apply shared-file integration centrally.
5. Run focused checks for each work package.
6. Run the slice's integration checks from the coordinator.
7. Compare behavior and files with the approved scope.
8. Report validation evidence and deviations before proposing another slice.

If two workers need the same file or interface, do not merge competing edits
blindly. Pause, select or redesign the contract, update the ownership register,
and request revised approval when the resolution changes approved behavior or
architecture.

## Independent validation

Use fresh agents for forward tests or reviews when practical. Give them the
skill or project artifacts and a realistic request without leaking the expected
answer. A validation pass should fail when the workflow is unclear; do not coach
the reviewer toward success.

The coordinating agent must reproduce critical checks. Treat a worker's test
report as evidence, not as a substitute for integration validation.
