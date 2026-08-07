import importlib.util
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "skills"
    / "sub-graper"
    / "scripts"
    / "sub_graper.py"
)


def load_sub_graper_module():
    spec = importlib.util.spec_from_file_location("sub_graper_paths", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sub_graper = load_sub_graper_module()


def test_cache_root_precedence(tmp_path, monkeypatch):
    project_root = tmp_path / "project"
    project_root.mkdir()
    environment_cache = tmp_path / "environment-cache"
    monkeypatch.setenv(sub_graper.CACHE_ENV_VAR, str(environment_cache))

    explicit_result = sub_graper.resolve_cache_root(
        project_root,
        "explicit-cache",
        {"cache_dir": "configured-cache"},
    )
    assert Path(explicit_result) == project_root / "explicit-cache"

    environment_result = sub_graper.resolve_cache_root(
        project_root,
        config={"cache_dir": "configured-cache"},
    )
    assert Path(environment_result) == environment_cache

    monkeypatch.delenv(sub_graper.CACHE_ENV_VAR)
    configured_result = sub_graper.resolve_cache_root(
        project_root,
        config={"cache_dir": "configured-cache"},
    )
    assert Path(configured_result) == project_root / "configured-cache"

    default_result = sub_graper.resolve_cache_root(project_root, config={})
    assert Path(default_result) == project_root / ".codex" / "sub-graper-cache"


def test_project_key_is_stable_and_distinguishes_paths(tmp_path):
    first_project = tmp_path / "first" / "project"
    second_project = tmp_path / "second" / "project"

    first_key = sub_graper.project_key(first_project)

    assert first_key == sub_graper.project_key(first_project)
    assert first_key != sub_graper.project_key(second_project)
    assert first_key.endswith("-project")


def test_validate_span_accepts_existing_lines_inside_project(tmp_path):
    project_root = tmp_path / "project"
    project_root.mkdir()
    source_file = project_root / "example.py"
    source_file.write_text("first\nsecond\nthird\n", encoding="utf-8")

    valid, reason = sub_graper.validate_span(project_root, "example.py:1-3")

    assert valid is True
    assert reason == ""


def test_validate_span_rejects_file_outside_project(tmp_path):
    project_root = tmp_path / "project"
    project_root.mkdir()
    outside_file = tmp_path / "outside.py"
    outside_file.write_text("outside\n", encoding="utf-8")

    valid, reason = sub_graper.validate_span(
        project_root,
        f"{outside_file}:1",
    )

    assert valid is False
    assert "outside the project" in reason


def test_validate_span_rejects_missing_file(tmp_path):
    project_root = tmp_path / "project"
    project_root.mkdir()

    valid, reason = sub_graper.validate_span(project_root, "missing.py:1")

    assert valid is False
    assert "file no longer exists" in reason


def test_validate_span_rejects_line_past_end_of_file(tmp_path):
    project_root = tmp_path / "project"
    project_root.mkdir()
    source_file = project_root / "example.py"
    source_file.write_text("only line\n", encoding="utf-8")

    valid, reason = sub_graper.validate_span(project_root, "example.py:1-2")

    assert valid is False
    assert "line range no longer exists" in reason
