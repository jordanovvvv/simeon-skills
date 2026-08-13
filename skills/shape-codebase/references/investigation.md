# Repository Investigation

Use this guide for `SC-1` and `SC-2`. Build an evidence-backed model of the
repository before judging its structure.

## Establish the evidence boundary

Record:

- the fixed revision and any uncommitted changes;
- in-scope packages, applications, workflows, and environments;
- vendored, generated, fixture, snapshot, migration, and build-output paths;
- authoritative product requirements or specifications;
- repository instructions and ecosystem conventions;
- commands that can safely validate behavior without changing external state.

Keep investigation strictly read-only. Do not normalize, create, edit, delete,
move, rename, format, install, generate, migrate, update snapshots or lock files,
or run a command with a fix or write mode. Treat existing user changes as
evidence to preserve, not noise to discard. If investigation requires a
mutation, propose it as a named remediation slice and wait for explicit approval.

## Use evidence in precedence order

Use approved user intent as the authority for desired behavior. For implemented
behavior, prefer evidence in this order while reporting conflicts:

1. Reproduced runtime behavior and executable contracts.
2. Tests that exercise supported behavior.
3. Build, dependency, schema, deployment, and runtime configuration.
4. Callers and implementations.
5. Current documentation and comments.
6. Naming, directory layout, and historical convention.

Tests can encode bugs and documentation can be stale. Precedence identifies
stronger evidence; it does not make any source unquestionable.

## Map behavior before files

Trace representative successful and failing workflows:

1. Identify the external trigger or entry point.
2. Follow orchestration and domain decisions.
3. Locate state reads, writes, transactions, and emitted events.
4. Identify remote calls and other irreversible effects.
5. Record retry, cancellation, timeout, and recovery behavior.
6. Find the observable result and the tests that protect it.

Then map files to those responsibilities. This avoids mistaking a folder tree
for the actual architecture.

## Produce the repository map

Include only information that helps explain change and risk:

- runtime and build entry points;
- user- or domain-facing capabilities;
- modules and their interfaces;
- dependency direction and cycles;
- persistent data ownership and transaction boundaries;
- external systems and their adapters;
- shared state, caches, queues, jobs, and lifecycle hooks;
- configuration and secrets boundaries;
- tests by behavior and level;
- generated sources and their source of truth;
- important hotspots where unrelated behavior converges.

For each important module, state its callers, responsibility, interface,
implementation dependencies, observable outcomes, and test surface.

## Select independent review tracks

For a non-trivial repository, use independent read-only tracks only when each
can produce distinct evidence. Examples:

- correctness, invariants, failure handling, and concurrency;
- module interfaces, ownership, dependency direction, and duplication;
- tests, fixtures, contracts, and change safety;
- configuration, data lifecycle, migrations, observability, and operations.

Give each track the same scope and fixed revision. Ask for evidence locations
and reproduced behavior, not general impressions. The coordinator must verify
material claims, deduplicate overlapping findings, and resolve contradictions.

## Investigation traps

- Do not review only the largest or most complicated-looking files.
- Do not assume repeated code should be shared; duplication may preserve useful
  independence.
- Do not infer a seam from an interface keyword or base class.
- Do not call code dead until callers, reflection, configuration, generation,
  and operational entry points have been checked.
- Do not treat low test coverage alone as a defect; identify the unprotected
  behavior and consequence.
- Do not propose a rewrite merely because the current design is unfamiliar.
