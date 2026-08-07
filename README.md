# Simeon Skills

Open-source Codex skills maintained by [jordanovvvv](https://github.com/jordanovvvv).

## Skills

| Skill | Problem it addresses | What it does |
| --- | --- | --- |
| [`approval-gated-integration`](skills/approval-gated-integration/SKILL.md) | Large or sensitive code changes can move ahead without enough review, making scope creep and regressions harder to control. | Breaks implementation into small, explicit approval gates and validates each approved step before continuing. |
| [`sub-graper`](skills/sub-graper/SKILL.md) | Repeated codebase searches consume the main conversation's context and duplicate previously completed discovery work. | Delegates each search to one focused subagent and caches validated file-and-line results for later queries. |

## Install

Ask Codex to install every skill:

```text
Use $skill-installer to install all skills from https://github.com/jordanovvvv/simeon-skills.
```

Or install one skill:

```text
Use $skill-installer to install <skill-name> from https://github.com/jordanovvvv/simeon-skills/tree/main/skills/<skill-name>.
```

Skills are installed under `~/.codex/skills` and become available on the next turn.

## Update

This repository is the source of truth. The installer does not overwrite an existing skill, so move or remove its installed directory before reinstalling it.

## Validate

The bundled validator requires [PyYAML](https://pypi.org/project/PyYAML/):

```powershell
python "$HOME\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "skills\<skill-name>"
```

## License

Released under the [MIT License](LICENCE.txt).

## Contributing

Contributions are welcome. If you find an error, outdated instruction, validation failure, or have an idea for a new skill or improvement, please [open an issue](https://github.com/jordanovvvv/simeon-skills/issues/new) with the affected skill, reproduction steps, and the expected behavior. Pull requests are also welcome for focused fixes and improvements.
