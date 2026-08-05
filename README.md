# Simeon Skills

Open-source Codex skills maintained by [jordanovvvv](https://github.com/jordanovvvv).

The repository is the source of truth. A copy under `~/.codex/skills` is an installed artifact and should be replaced by reinstalling from this repository when the source changes.

## Install

Every skill directory under `skills/` can be installed independently. When asking Codex to install from this repository:

- If no skill is named, install all available skills.
- If one or more skills are named, install only those skills.

To install every skill, ask Codex:

```text
Use $skill-installer to install all skills from https://github.com/jordanovvvv/simeon-skills.
```

To install one specific skill, include its name or GitHub path:

```text
Use $skill-installer to install approval-gated-integration from https://github.com/jordanovvvv/simeon-skills/tree/main/skills/approval-gated-integration.
```

To install directly on Windows, pass one or more explicit skill paths to the bundled installer:

```powershell
python "$HOME\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" --repo jordanovvvv/simeon-skills --path skills/approval-gated-integration
```

For multiple skills, list every path after `--path`:

```powershell
python "$HOME\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" --repo jordanovvvv/simeon-skills --path skills/approval-gated-integration skills/another-skill
```

The command-line installer does not expand `skills/*`; keep the path list synchronized with the skill directories in the repository when installing all skills.

Each skill is installed under `~/.codex/skills/<skill-name>`. The installer refuses to overwrite an existing destination. To test without disturbing installed copies, provide a separate destination:

```powershell
python "$HOME\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" --repo jordanovvvv/simeon-skills --path skills/approval-gated-integration --dest "$HOME\codex-skill-test"
```

Installed skills are available to Codex on the next turn.

## Available skills

### Approval-Gated Integration

`approval-gated-integration` guides codebase features, refactors, migrations, and architectural changes through small, explicitly approved implementation stages. It inspects first, proposes a bounded step, waits for approval, applies only the approved scope, and validates the result before continuing.

#### Use

Invoke the skill explicitly in a prompt:

```text
Use $approval-gated-integration to guide this codebase change step by step and wait for approval before each implementation stage.
```

The skill also allows implicit invocation when a request clearly calls for approval-gated implementation.

## Update or reinstall

Because the installer does not overwrite existing skills, move or remove the installed directory before reinstalling. Keep a backup if the installed copy contains local changes.

## Repository layout

```text
skills/
+-- approval-gated-integration/
    +-- SKILL.md
    +-- agents/
        +-- openai.yaml
```

## Validate

The validator requires [PyYAML](https://pypi.org/project/PyYAML/). Run it from an environment where that dependency is installed:

```powershell
python "$HOME\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "skills\approval-gated-integration"
```

## License

Released under the [MIT License](LICENCE.txt).
