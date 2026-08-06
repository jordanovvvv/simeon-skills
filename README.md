# Simeon Skills

Open-source Codex skills maintained by [jordanovvvv](https://github.com/jordanovvvv).

## Skills

| Skill | Purpose |
| --- | --- |
| [`approval-gated-integration`](skills/approval-gated-integration/SKILL.md) | Implements codebase changes through small, explicitly approved and validated steps. |
| [`sub-graper`](skills/sub-graper/SKILL.md) | Delegates code search to one subagent and caches validated results per project. |

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
