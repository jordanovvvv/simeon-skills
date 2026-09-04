# Using Simeon Skills

Use the skill name in a prompt as `$skill-name`.

| Skill | Use it for |
| --- | --- |
| `approval-gated-integration` | Controlled changes to an existing codebase, with approval before each material step. |
| `shape-codebase` | Reviewing or reorganizing an existing repository. |
| `shape-project` | Designing and starting a new software project. |
| `sub-router` | Deciding whether a task needs a subagent and selecting one. |
| `sub-graper` | Bounded code discovery after `sub-router` selects isolated search. |

## approval-gated-integration

Use for a feature, refactor, migration, or architecture change where you want
to approve the proposed behavioral slices before implementation. It proposes a
step, waits for approval, implements only that scope, and runs focused checks.

Do not use it for a one-line change or when you want the entire change applied
without review gates.

Examples:

```text
Use $approval-gated-integration to add account lockout after repeated failed logins. Propose the first step and wait for my approval.
```

```text
Use $approval-gated-integration to move email delivery behind an interface. Keep each approved step independently verifiable.
```

## shape-codebase

Use for an evidence-based review of an existing repository: module boundaries,
dependencies, ownership, architecture, and a remediation roadmap. It does not
start refactoring until the relevant stage is approved.

Do not use it to add one isolated feature or fix a single known defect.

Examples:

```text
Use $shape-codebase to review this repository's module boundaries and identify the three highest-value structural improvements.
```

```text
Use $shape-codebase to create an approval-gated refactor roadmap for the billing area without applying changes yet.
```

## shape-project

Use for a new application or service when you need to turn an idea into a
clear domain model, architecture, scaffold, and approved implementation plan.

Do not use it when an existing repository already has a defined feature to
implement.

Examples:

```text
Use $shape-project to design a shared household budget app. Start with discovery and wait for approval before creating files.
```

```text
Use $shape-project to turn this API idea into an approval-gated project plan and initial architecture.
```

## sub-router

Use before delegating research, code search, review, testing, or another
bounded task. It decides whether direct work is cheaper, or selects a
specialist and supplies a minimal task contract.

Do not use it for an answer already visible in the conversation or a simple
read of an exact file and symbol.

Examples:

```text
Use $sub-router to decide whether a subagent is needed to trace how password reset emails are sent. If so, use the smallest useful budget and report the route chosen.
```

```text
Use $sub-router to decide whether this repository-wide dependency review needs a specialist or can be handled directly.
```

## sub-graper

Use through `sub-router` for broad or uncertain code-location and
implementation-flow questions. It runs one isolated search by default and
returns a few decisive file-and-line spans, not raw search output.

Do not use it for an exact file path, a known symbol in a known file, or a
simple bounded lookup.

Examples:

```text
Use $sub-router and route to $sub-graper if warranted: where is session invalidation implemented, and which API handler calls it? Return up to three decisive spans.
```

```text
Use $sub-router and explicitly use $sub-graper to find the retry policy for outbound requests. Search src/integrations first; stop after locating the policy and its caller.
```
