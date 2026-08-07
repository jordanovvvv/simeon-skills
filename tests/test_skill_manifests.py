import re
from pathlib import Path

import pytest
import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
SKILL_DIRECTORIES = sorted(
    path for path in SKILLS_ROOT.iterdir() if path.is_dir()
)
ALLOWED_FRONTMATTER_FIELDS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
}
MAX_SKILL_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024


def load_frontmatter(skill_directory):
    skill_file = skill_directory / "SKILL.md"
    assert skill_file.is_file(), f"Missing {skill_file}"

    content = skill_file.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", content, re.DOTALL)
    assert match, f"{skill_file} must begin with YAML frontmatter"

    frontmatter = yaml.safe_load(match.group(1))
    assert isinstance(frontmatter, dict), (
        f"{skill_file} frontmatter must be a YAML mapping"
    )
    return frontmatter


@pytest.mark.parametrize(
    "skill_directory",
    SKILL_DIRECTORIES,
    ids=lambda path: path.name,
)
def test_skill_manifest_is_valid(skill_directory):
    frontmatter = load_frontmatter(skill_directory)

    unexpected_fields = set(frontmatter) - ALLOWED_FRONTMATTER_FIELDS
    assert not unexpected_fields, (
        f"Unexpected frontmatter fields: {sorted(unexpected_fields)}"
    )

    name = frontmatter.get("name")
    assert isinstance(name, str) and name.strip(), (
        "Skill name must be a non-empty string"
    )
    assert name == name.strip(), "Skill name cannot have surrounding whitespace"
    assert len(name) <= MAX_SKILL_NAME_LENGTH
    assert re.fullmatch(r"[a-z0-9-]+", name), (
        "Skill name must use lowercase hyphen-case"
    )
    assert not name.startswith("-") and not name.endswith("-")
    assert "--" not in name
    assert name == skill_directory.name, (
        "Skill name must match its directory name"
    )

    description = frontmatter.get("description")
    assert isinstance(description, str) and description.strip(), (
        "Skill description must be a non-empty string"
    )
    assert len(description) <= MAX_DESCRIPTION_LENGTH
    assert "<" not in description and ">" not in description, (
        "Skill description cannot contain angle brackets"
    )
