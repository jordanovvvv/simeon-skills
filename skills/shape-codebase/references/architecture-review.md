# Architecture Review

Use this guide for `SC-3` and `SC-4`. Judge architecture by the leverage it gives
callers, the locality it gives maintainers, and the behavior it safely supports.

## Review modules through their interfaces

A module is anything with an interface and an implementation: a function,
class, package, or tier-spanning slice. Its interface includes everything a
caller must know, including ordering constraints, errors, configuration,
performance characteristics, and invariants.

A deep module hides substantial behavior behind a small interface. A shallow
module exposes nearly as much complexity as it contains. Look for:

- callers repeating validation, ordering, retry, or cleanup rules;
- chains of pass-through modules whose interfaces add no useful behavior;
- interfaces that expose persistence or transport details to domain callers;
- changes that require coordinated edits across unrelated locations;
- tests that must reach past the public interface to verify behavior;
- modules named by technical mechanism when product behavior has no clear owner;
- generic helper areas that collect unrelated responsibilities;
- hidden global dependencies, lifecycle, or configuration;
- dependency cycles and callbacks that obscure ownership.

Use the deletion test: if deleting a module makes its complexity disappear, it
was likely pass-through. If the complexity spreads back across many callers,
the module was providing useful depth.

## Place seams deliberately

A seam is a place where behavior can change without editing the caller. An
adapter satisfies an interface at a seam.

Classify dependencies before adding or moving a seam:

| Dependency | Preferred treatment |
| --- | --- |
| In-process computation | Keep inside the module; no adapter |
| Local dependency with a realistic test stand-in | Keep the seam internal and test with the stand-in |
| Remote system owned by the organization | Define a narrow port and production/test adapters |
| True external system | Inject a narrow port and use a mock or fake adapter in tests |

Do not expose internal seams merely to make private implementation details easy
to mock. One adapter means the seam may be hypothetical; two justified adapters
usually make it real.

## Evaluate project structure

Prefer ownership and change locality over symmetry:

- organize product or domain behavior before technical mechanisms;
- keep internal helpers private to their owning module;
- colocate tests with behavior or mirror the source tree consistently;
- separate authored files from generated sources;
- place configuration beside the system that owns its meaning;
- avoid `utils`, `helpers`, `common`, or `shared` until one stable shared
  responsibility can be named;
- avoid one file per tiny type when it creates navigation without leverage.

Use a class when identity, state, invariants, or lifecycle justify it. Use a
function for stateless transformation or orchestration that gains nothing from
object identity.

## Design the target

Start from approved findings and required behavior. For every proposed module,
describe:

- responsibility and owner;
- external interface and what it hides;
- primary callers and observable outcomes;
- invariants and error modes;
- allowed dependencies and dependency direction;
- internal and external seams;
- persistence and operational implications;
- tests through the external interface;
- responsibilities and files it replaces.

For a non-trivial redesign, compare at least two genuinely different shapes.
Vary module ownership or seam placement, not just names and folders. Rank them
by interface depth, locality, change safety, testability, operability, migration
cost, and reader navigation. Recommend one or a deliberate hybrid.

## Show placement and movement

Present the complete affected target tree and a current-to-target mapping. For
each added or moved file, state:

| Field | Meaning |
| --- | --- |
| Path | Exact target location |
| Owner | Module responsible for the file |
| Purpose | One explicit responsibility |
| Relationships | Closest callers, dependencies, or configuration |
| Allowed dependencies | What it may import or invoke |
| Test location | Where observable behavior is verified |
| Replacement | Existing responsibility or file it supersedes |
| Placement reason | Why the responsibility belongs here |

Do not turn a target tree into an instruction to move everything at once. The
remediation plan must preserve behavior through incremental slices.
