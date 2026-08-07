import subprocess
import sys
from pathlib import Path

SCRIPT_PATH = (
    Path(__file__).resolve().parents[2]
    / "skills"
    / "sub-graper"
    / "scripts"
    / "sub_graper.py"
)


def run_cli(*arguments):
    return subprocess.run(
        [sys.executable, str(SCRIPT_PATH), *map(str, arguments)],
        capture_output=True,
        check=False,
        text=True,
    )


def test_cache_cli_lifecycle(tmp_path):
    project_root = tmp_path / "project"
    cache_root = tmp_path / "cache"
    project_root.mkdir()
    source_file = project_root / "handler.py"
    source_file.write_text(
        "def handle_request():\n    return 'ok'\n",
        encoding="utf-8",
    )
    query = "find request handler"
    common_arguments = (
        "--project-root",
        project_root,
        "--cache-dir",
        cache_root,
    )

    write_result = run_cli(
        "write",
        *common_arguments,
        "--query",
        query,
        "--spans",
        "handler.py:1-2",
        "--notes",
        "The request handler implementation.",
    )
    assert write_result.returncode == 0, write_result.stderr
    assert "WROTE" in write_result.stdout

    lookup_result = run_cli(
        "lookup",
        *common_arguments,
        "--query",
        query,
    )
    assert lookup_result.returncode == 0, lookup_result.stderr
    assert "HIT" in lookup_result.stdout
    assert "handler.py:1-2" in lookup_result.stdout

    invalidate_result = run_cli(
        "invalidate",
        *common_arguments,
        "--entry",
        "find-request-handler",
    )
    assert invalidate_result.returncode == 0, invalidate_result.stderr
    assert "INVALIDATED find-request-handler" in invalidate_result.stdout

    lookup_after_invalidate = run_cli(
        "lookup",
        *common_arguments,
        "--query",
        query,
    )
    assert lookup_after_invalidate.returncode == 0
    assert "MISS" in lookup_after_invalidate.stdout

    rewrite_result = run_cli(
        "write",
        *common_arguments,
        "--query",
        query,
        "--spans",
        "handler.py:1-2",
        "--notes",
        "The request handler implementation.",
    )
    assert rewrite_result.returncode == 0, rewrite_result.stderr

    clear_result = run_cli("clear", *common_arguments)
    assert clear_result.returncode == 0, clear_result.stderr
    assert "CLEARED" in clear_result.stdout

    lookup_after_clear = run_cli(
        "lookup",
        *common_arguments,
        "--query",
        query,
    )
    assert lookup_after_clear.returncode == 0
    assert "MISS (no cache for this project)" in lookup_after_clear.stdout


def test_write_refuses_invalid_span_without_creating_cache(tmp_path):
    project_root = tmp_path / "project"
    cache_root = tmp_path / "cache"
    project_root.mkdir()
    (project_root / "handler.py").write_text("one line\n", encoding="utf-8")

    result = run_cli(
        "write",
        "--project-root",
        project_root,
        "--cache-dir",
        cache_root,
        "--query",
        "find request handler",
        "--spans",
        "handler.py:1-2",
        "--notes",
        "Invalid line range.",
    )

    assert result.returncode != 0
    assert "REFUSED TO CACHE" in result.stderr
    assert not cache_root.exists()
