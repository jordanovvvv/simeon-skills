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

For example, install Sub-Graper with:

```text
Use $skill-installer to install sub-graper from https://github.com/jordanovvvv/simeon-skills/tree/main/skills/sub-graper.
```

To install directly on Windows, pass one or more explicit skill paths to the bundled installer:

```powershell
python "$HOME\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" --repo jordanovvvv/simeon-skills --path skills/approval-gated-integration
```

For multiple skills, list every path after `--path`:

```powershell
python "$HOME\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" --repo jordanovvvv/simeon-skills --path skills/approval-gated-integration skills/sub-graper
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

### Sub-Graper

`sub-graper` delegates repository-wide code searches to one isolated subagent and caches confident file-and-line results per project. It checks the cache before searching, validates that cached files and line ranges still exist, and treats expired, weak, or invalid entries as misses.

#### Use

Invoke it explicitly when locating or understanding code:

```text
Use $sub-graper to find where authentication middleware is configured.
```

The skill also handles cache maintenance requests:

```text
Use $sub-graper to invalidate the cached authentication middleware result.
Use $sub-graper to clear its cache for this project.
```

#### Cache configuration

Sub-Graper stores runtime state outside its installed skill directory. It resolves the cache root in this order:

1. The `--cache-dir` command option.
2. The `SUB_GRAPER_CACHE_DIR` environment variable.
3. `cache_dir` in the skill's `config.json`.
4. `<project-root>/.codex/sub-graper-cache`.

Entries use a 14-day TTL by default. Repository revisions do not invalidate entries automatically; users can invalidate one selected entry or clear the current project's cache when needed. The cache index uses JSONL, while resolved spans and notes are stored as Markdown entry files.

## Update or reinstall

Because the installer does not overwrite existing skills, move or remove the installed directory before reinstalling. Keep a backup if the installed copy contains local changes.

## Repository layout

```text
skills/
+-- approval-gated-integration/
|   +-- SKILL.md
|   +-- agents/
|       +-- openai.yaml
+-- sub-graper/
    +-- SKILL.md
    +-- config.json
    +-- scripts/
        +-- sub_graper.py
```

## Validate

The validator requires [PyYAML](https://pypi.org/project/PyYAML/). Run it from an environment where that dependency is installed:

```powershell
python "$HOME\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "skills\approval-gated-integration"
python "$HOME\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "skills\sub-graper"
```

Sub-Graper's cache manager requires Python 3.9 or newer. Its cache lifecycle can be exercised safely by passing `--cache-dir` with a temporary directory.

## License

Released under the [MIT License](LICENCE.txt).
