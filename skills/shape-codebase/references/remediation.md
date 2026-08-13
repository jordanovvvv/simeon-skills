# Incremental Remediation

Use this guide for `SC-5` through `SC-7`. Convert approved findings and target
design into small, behavior-preserving improvements.

## Build change slices

Prefer vertical slices that improve an observable workflow or establish a
complete module interface. Avoid plans made only of technical layers such as
"create interfaces, move files, then fix tests."

Planning a slice is read-only. Present the complete slice, yield, and wait for
explicit user approval before changing anything. Approval of findings, a target
design, the remediation plan, or a different slice does not authorize the
proposed slice. A broad instruction to fix the repository does not authorize
details that have not yet been presented.

Each slice must contain:

```md
### SC-6.1: Slice name

Linked findings:
Observable improvement:
Owned modules and files:
Interface or contract changes:
Prerequisites:
Compatibility and migration:
Focused validation:
Integration validation:
Rollback or recovery:
Documentation impact:
Explicit exclusions:
```

Order slices so the repository remains buildable and behavior remains
observable. Prefer introducing a tested replacement before switching callers,
then remove the superseded path as soon as the switch is complete.

The user may approve one named slice or several named slices. Apply only those
slices, in dependency order, and validate each separately. If the approval
target is ambiguous, ask which slice is approved before editing any file. A
broad request such as "fix everything" does not identify several pending slices;
ask the user to name or explicitly approve the intended slices.

## Characterize before changing

When behavior is unclear or weakly tested, include characterization tests in
the proposed slice before adding them at the stable interface. Do not freeze
incidental implementation details. Capture successful outcomes, important
failures, state changes, and external effects that the slice must preserve or
intentionally change.

For a known defect, write validation that demonstrates the failure when doing
so is practical and safe. Obtain approval for intentionally changed behavior;
do not disguise it as refactoring.

## Deepen by replacement

When consolidating shallow modules:

1. Define the smallest useful external interface.
2. Move repeated caller knowledge behind it.
3. Keep implementation-only seams private.
4. Inject only dependencies that genuinely vary or cross remote/external seams.
5. Switch callers incrementally where compatibility permits.
6. Test observable outcomes through the new interface.
7. Delete old pass-through modules, obsolete tests, and temporary adapters.

Do not layer a new abstraction permanently over the old one. If a compatibility
layer must remain, name its consumers, removal condition, and expected lifetime.

## Protect risky changes

For state, schema, protocol, or deployment changes, specify:

- backward- and forward-compatibility expectations;
- ordering across application and infrastructure changes;
- data backfill, dual-read, dual-write, or reconciliation behavior;
- retry, idempotency, cancellation, and partial-failure handling;
- observability needed to detect a bad rollout;
- rollback limits once state has changed.

Do not install or update dependencies, update lock files or snapshots, execute
migrations, deploy, publish, push, or mutate external systems unless those
specific effects were disclosed in and authorized by the approved slice.

## Validate each slice

Run the smallest checks that establish the linked improvement, then appropriate
integration checks. Inspect the actual diff for:

- unrelated cleanup;
- behavior changes not covered by the approval;
- duplicated old and new paths;
- widened interfaces or leaked implementation details;
- stale tests and documentation;
- generated files edited instead of their source of truth.

Record commands, results, and anything not run. A worker or tool's success claim
is not validation evidence until the coordinating agent inspects the diff and
relevant output.

If a validation command can rewrite files, regenerate artifacts, update
snapshots, migrate data, or otherwise mutate state, disclose it in the slice
proposal. Do not run it under a generic authorization to "run tests."

If implementation or validation uncovers an out-of-scope change, stop. Do not
apply the change as cleanup or an automatic fix. Explain why it is needed and
propose a revised or additional slice for approval.

## Complete the remediation

At integration, trace every changed responsibility to an approved finding and
slice. Report:

- findings resolved, partially resolved, deferred, or invalidated;
- behavior intentionally changed and preserved;
- final module interfaces and dependency direction;
- focused and system-level validation;
- remaining compatibility layers and removal conditions;
- operational monitoring, rollout, or recovery caveats.

Stop when the approved outcomes are met. Further cleanup requires a new finding
and decision.
