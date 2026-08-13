# Evidence-Backed Findings

Use this guide for `SC-3`. Report problems the user can decide and act on, not a
catalog of preferences.

## Verify before reporting

A suspected issue becomes a finding only after checking relevant callers,
tests, configuration, generated sources, and runtime behavior. Reproduce the
problem when practical. If reproduction is unsafe or impossible, label the
claim as an inference and explain what evidence is missing.

Do not report:

- formatting or naming differences already handled consistently by the repo;
- hypothetical scale, extension, or reuse requirements;
- a missing abstraction without repeated caller complexity;
- code that merely differs from the reviewer's preferred pattern;
- test coverage percentages without an exposed behavior or risk;
- multiple symptoms of one root cause as unrelated findings.

## Finding schema

Assign stable identifiers such as `F-001`. Each finding must include:

```md
### F-001: Imperative title

Priority:
Confidence:
Status: verified | inferred | unresolved
Evidence:
Affected behavior:
Consequence:
Root cause:
Recommended direction:
Alternatives or trade-offs:
Focused validation:
Linked findings:
```

Use exact file and line locations for evidence. When the issue spans a flow,
include the smallest set of locations that demonstrates cause and consequence.

## Prioritize by consequence

Use repository-specific impact and likelihood. As a default:

| Priority | Meaning |
| --- | --- |
| `P0` | Immediate loss, corruption, security compromise, or unusable critical workflow |
| `P1` | Likely serious failure or a design defect blocking safe near-term change |
| `P2` | Material maintainability, reliability, performance, or testability cost |
| `P3` | Localized improvement with limited present consequence |

Do not inflate architectural findings to `P0` or `P1` without an active failure
or credible near-term change constraint. Report uncertain severity as a range or
request the missing operational context.

Use confidence to distinguish evidence quality:

- `high`: reproduced or directly established by executable evidence;
- `medium`: strongly supported by callers and configuration but not reproduced;
- `low`: plausible inference requiring additional evidence.

Low-confidence observations belong in an unresolved section unless their
potential consequence justifies explicit attention.

## Present a decision-ready review

Order findings by priority, then consequence. Include:

1. Scope, fixed revision, and validation performed.
2. A short repository map or link to the approved map.
3. Material findings with precise evidence.
4. Strengths and conventions worth preserving.
5. Cross-cutting root causes and dependency relationships.
6. Unresolved questions and review limitations.
7. Recommended next stage without beginning implementation.

Use inline code comments only for tightly located actionable findings. Keep the
full consequence, design context, and remediation relationship in the review
summary.
