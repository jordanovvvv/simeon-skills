# Simeon Skills

Open-source Codex skills maintained by [jordanovvvv](https://github.com/jordanovvvv).

## Approval-Gated Integration

`approval-gated-integration` guides codebase features, refactors, migrations, and architectural changes through small, explicitly approved implementation stages. It inspects first, proposes a bounded step, waits for approval, applies only the approved scope, and validates the result before continuing.

The repository is the source of truth. A copy under `~/.codex/skills` is an installed artifact and should be replaced by reinstalling from this repository when the source changes.

### Install

Ask Codex to install the skill from:

```text
https://github.com/jordanovvvv/simeon-skills/tree/main/skills/approval-gated-integration
```

Or run the bundled skill installer directly on Windows:

```powershell
python "$HOME\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" --repo jordanovvvv/simeon-skills --path skills/approval-gated-integration
```

The installer places the skill at `~/.codex/skills/approval-gated-integration`. It refuses to overwrite an existing destination. To test without disturbing an installed copy, provide a separate destination:

```powershell
python "$HOME\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" --repo jordanovvvv/simeon-skills --path skills/approval-gated-integration --dest "$HOME\codex-skill-test"
```

The skill is available to Codex on the next turn after installation.

### Use

Invoke the skill explicitly in a prompt:

```text
Use $approval-gated-integration to guide this codebase change step by step and wait for approval before each implementation stage.
```

The skill also allows implicit invocation when a request clearly calls for approval-gated implementation.

### Update or reinstall

Because the installer does not overwrite existing skills, move or remove the installed directory before reinstalling. Keep a backup if the installed copy contains local changes.

### Repository layout

```text
skills/
└── approval-gated-integration/
    ├── SKILL.md
    └── agents/
        └── openai.yaml
```

### Validate

The validator requires [PyYAML](https://pypi.org/project/PyYAML/). Run it from an environment where that dependency is installed:

```powershell
python "$HOME\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "skills\approval-gated-integration"
```

## License

Released under the [MIT License](LICENCE.txt).
