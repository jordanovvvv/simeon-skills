import re
from pathlib import Path

import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIRECTORY = REPOSITORY_ROOT / "skills" / "shape-project"
SKILL_FILE = SKILL_DIRECTORY / "SKILL.md"
METADATA_FILE = SKILL_DIRECTORY / "agents" / "openai.yaml"
DISCOVERY_FILE = SKILL_DIRECTORY / "references" / "discovery.md"


def read_skill():
    return SKILL_FILE.read_text(encoding="utf-8")


def test_skill_contains_no_initializer_placeholders():
    content = read_skill()

    assert "[TODO" not in content
    assert not re.search(r"\bTODO\b", content)
    assert "Structuring This Skill" not in content


def test_local_markdown_references_resolve_inside_skill():
    content = read_skill()
    targets = re.findall(r"\[[^\]]+\]\(([^)]+\.md(?:#[^)]+)?)\)", content)

    assert targets
    for target in targets:
        relative_target = target.split("#", maxsplit=1)[0]
        resolved_target = (SKILL_DIRECTORY / relative_target).resolve()
        assert resolved_target.is_relative_to(SKILL_DIRECTORY.resolve())
        assert resolved_target.is_file(), f"Missing reference: {target}"


def test_workflow_stages_are_defined_in_order():
    content = read_skill()
    expected_stages = [
        "`SP-1`",
        "`SP-2`",
        "`SP-3`",
        "`SP-4`",
        "`SP-5`",
        "`SP-6`",
        "`SP-7`",
        "`SP-8.n`",
        "`SP-9`",
    ]
    positions = [content.index(stage) for stage in expected_stages]

    assert positions == sorted(positions)


def test_core_approval_and_ownership_contracts_are_explicit():
    content = read_skill()
    normalized_content = " ".join(content.split())

    assert (
        "Require explicit approval before executing every stage's proposed output "
        "and before making any change."
        in normalized_content
    )
    assert (
        "Before changing anything, present either the complete `SP-6` foundation "
        "package or a named `SP-8.n` implementation slice"
        in normalized_content
    )
    assert (
        "One explicit approval of a complete `SP-6` package or named `SP-8.n` "
        "slice satisfies both the stage and change gate"
        in normalized_content
    )
    assert "Give concurrent writing agents disjoint file ownership" in content
    assert (
        "Never accept a worker's success claim as validation evidence by itself"
        in normalized_content
    )


def test_metadata_default_prompt_invokes_shape_project():
    metadata = yaml.safe_load(METADATA_FILE.read_text(encoding="utf-8"))
    interface = metadata["interface"]

    assert interface["display_name"] == "Shape Project"
    assert "$shape-project" in interface["default_prompt"]


def test_motive_stage_defers_solution_design():
    content = DISCOVERY_FILE.read_text(encoding="utf-8")
    normalized_content = " ".join(content.split())

    assert (
        "Do not recommend a delivery platform, technology stack, architecture, "
        "or detailed feature bundle during `SP-1`."
        in normalized_content
    )
    assert "Defer feature design to `SP-2` and technology choices to `SP-3`." in (
        normalized_content
    )
