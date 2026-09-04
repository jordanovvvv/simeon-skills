# Simeon Skills

Open-source Codex skills maintained by [jordanovvvv](https://github.com/jordanovvvv).

## Skills

| Skill | Problem it addresses | What it does |
| --- | --- | --- |
| [`approval-gated-integration`](skills/approval-gated-integration/SKILL.md) | Large or sensitive code changes can move ahead without enough review, making scope creep and regressions harder to control. | Breaks implementation into small, explicit approval gates and validates each approved step before continuing. |
| [`shape-codebase`](skills/shape-codebase/SKILL.md) | Existing codebases can accumulate unclear ownership, shallow abstractions, risky dependencies, and unprioritized cleanup without an evidence-backed improvement path. | Maps the repository, verifies and prioritizes findings, designs a target architecture, and applies approved remediation slices with focused validation. |
| [`shape-project`](skills/shape-project/SKILL.md) | New project ideas can turn into code before their purpose, requirements, architecture, and file ownership are clear. | Clarifies the motive, gains approval at every material stage, designs an explicit structure, and coordinates validated implementation slices. |
| [`sub-router`](skills/sub-router/SKILL.md) | Subagent setup and handoff can cost more than a task saves when delegation is automatic. | Decides whether to work directly or delegate, selects a specialist, and supplies a minimal bounded task contract. |
| [`sub-graper`](skills/sub-graper/SKILL.md) | Broad or uncertain code discovery can create search noise and unnecessary repeated exploration. | Performs a bounded isolated code search only after `sub-router` selects it, with optional reuse caching for recurring questions. |

`sub-router` is the delegation decision point. It uses a subagent only when
isolation, parallel exploration, or specialized context saves more work than
the setup and handoff cost. `sub-graper` is its code-search specialist, not a
general-purpose delegation entry point.

For concise usage guidance and ready-to-use prompts, see
[INSTRUCTION.md](INSTRUCTION.md).

## Install

Use the interactive [`skills` CLI](https://github.com/vercel-labs/skills) to
choose which skills to install, which coding agents should receive them, and
whether to install them for the current project or globally:

```powershell
npx skills@latest add jordanovvvv/simeon-skills
```

To install every skill globally for Codex without prompts:

```powershell
npx skills@latest add jordanovvvv/simeon-skills --skill --agent codex --global --yes
```

Install one skill by name:

```powershell
npx skills@latest add jordanovvvv/simeon-skills --skill <skill-name> --agent codex --global --yes
```

Global Codex skills are installed under `~/.codex/skills` and become available
on the next turn.

## Update

Update every installed global skill without deleting and reinstalling it:

```powershell
npx skills@latest update --global
```

Update latest changes and pick globally, projects and all:
```powershell
npx skills update
```

Or update one skill:

```powershell
npx skills@latest update --global <skill-name>
```

Updates refresh skills already tracked by the installer. To discover skills
added to this repository later, rerun the install-all command. If a skill is
renamed or removed upstream, remove its old installed name explicitly:

```powershell
npx skills@latest remove --global <old-skill-name>
```

This repository remains the source of truth; local edits to installed copies
may be overwritten during an update.

## Validate

The bundled validator requires [PyYAML](https://pypi.org/project/PyYAML/):

```powershell
python "$HOME\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "skills\<skill-name>"
```

## License

Released under the [MIT License](LICENCE.txt).

## Contributing

Contributions are welcome. If you find an error, outdated instruction, validation failure, or have an idea for a new skill or improvement, please [open an issue](https://github.com/jordanovvvv/simeon-skills/issues/new) with the affected skill, reproduction steps, and the expected behavior. Pull requests are also welcome for focused fixes and improvements.
