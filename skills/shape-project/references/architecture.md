# Architecture and Placement

Use this guide for `SP-5` and `SP-6`. Design for obvious ownership, small
interfaces, cohesive behavior, testability, and straightforward navigation.

## Explore alternatives

After the user approves architecture exploration for a non-trivial project,
commission at least three independent designs with the same approved motive,
requirements, domain language, and constraints. Give each a distinct emphasis:

1. Minimize the external interface and maximize leverage.
2. Optimize the common workflow and reader comprehension.
3. Maximize justified extensibility without speculative abstractions.
4. Add a ports-and-adapters alternative when remote or external dependencies
   materially shape the project.

Require each design to provide:

- modules and their interfaces;
- a typical caller flow;
- invariants and error modes;
- dependency direction and external adapters;
- persistence and operational implications;
- test strategy;
- proposed directory tree;
- trade-offs and likely change points.

Compare the alternatives by interface depth, locality, seam placement,
dependency direction, testability, operability, and navigation. Recommend one
or a deliberate hybrid; do not present an unranked menu.

## Shape modules

- Organize behavior around domain or product capabilities before technical
  mechanisms.
- Give each module one understandable responsibility and one external
  interface.
- Hide meaningful complexity behind the interface.
- Keep internal helpers private to the owning module.
- Introduce an adapter only when production and testing, or two real runtime
  implementations, justify the seam.
- Inject remote or true external dependencies through a narrow interface.
- Test observable outcomes through the same interface callers use.
- Avoid generic `utils`, `helpers`, `common`, or `shared` folders until a
  specific, stable shared responsibility exists.
- Avoid one file per tiny class when the result is a chain of pass-through
  abstractions.

Use a class when it protects identity, state, invariants, or lifecycle. Use a
function for stateless transformation or orchestration that gains nothing from
object identity. Optimize for the reader locating responsibility, not for a
target line count.

## Design the project tree

Present the complete proposed tree before creating it. Adapt ecosystem-standard
locations rather than imposing one universal layout. Keep tests close to their
behavior when the ecosystem supports it, or mirror the source tree consistently
when it does not.

Create a placement-manifest row for every authored file:

| Field | Meaning |
| --- | --- |
| Path | Exact proposed location |
| Owner | Module or project concern responsible for it |
| Purpose | One explicit responsibility |
| Relationship | Closest callers, dependencies, or related configuration |
| Allowed dependencies | What it may import or invoke |
| Test location | Where its behavior is verified |
| Placement reason | Why this location and why a new file are justified |

Identify generated files separately and explain which tool owns them. Do not
hand-edit generated files when their generator is the source of truth.

## Keep documentation simple

Create only artifacts that have an immediate role:

- `README.md`: entrypoint with purpose, setup, run, test, and links.
- `PROJECT.md`: approved motive, scope, requirement IDs, acceptance criteria,
  constraints, and non-goals.
- `CONTEXT.md`: concise domain glossary with canonical terms and avoided
  synonyms; no implementation details.
- `ARCHITECTURE.md`: module map, interfaces, dependency direction, important
  flows, placement rules, and source-of-truth notes.
- `AGENTS.md`: durable instructions future coding agents must enforce.
- `docs/adr/`: create lazily only for decisions that are hard to reverse,
  surprising without context, and based on a genuine trade-off.

Use `README.md` as the navigation root. Link outward instead of duplicating
content. Do not create a README in every directory or documentation for an
unimplemented feature.

## Evidence and precedence

Treat approved user intent as the authority for desired behavior. Treat tests,
contracts, and executable configuration as evidence of implemented behavior.
Treat documentation and nearby patterns as evidence that can become stale.

When evidence conflicts, surface the conflict and its consequence. Do not use a
legacy convention merely because it already exists, and do not replace a sound
convention merely because a newer pattern is fashionable.

## SP-6 approval package

Before requesting approval to scaffold, provide:

- the final architecture recommendation;
- complete directory tree;
- placement manifest;
- authored versus generated files;
- configuration and dependency list;
- documentation plan;
- commands that may create or modify files, install dependencies, update lock
  files, generate artifacts, or otherwise mutate state;
- initial read-only and write-capable validation commands, clearly separated;
- external side effects requiring separate authorization;
- important trade-offs and deliberately deferred work.

After approval, create only that foundation. If the selected framework's
generator produces materially different files, stop, show the difference, and
request revised approval before continuing.
