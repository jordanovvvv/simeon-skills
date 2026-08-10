import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "skills"
    / "sub-graper"
    / "scripts"
    / "sub_graper.py"
)


def load_sub_graper_module():
    spec = importlib.util.spec_from_file_location("sub_graper_matching", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sub_graper = load_sub_graper_module()


def test_slugify_normalizes_text():
    assert sub_graper.slugify("  HTTP Request Handler!!!  ") == (
        "http-request-handler"
    )


def test_slugify_uses_fallback_for_text_without_alphanumerics():
    assert sub_graper.slugify("---") == "query"


def test_tokenize_removes_search_stopwords():
    assert sub_graper.tokenize("Where is the code for the payment handler?") == {
        "payment",
        "handler",
    }


def test_match_score_returns_one_for_equivalent_queries():
    score = sub_graper.match_score(
        "find the payment handler",
        "where is payment handler code",
    )

    assert score == 1.0


def test_match_score_uses_shared_tokens_for_partial_match():
    score = sub_graper.match_score(
        "payment handler",
        "payment handler configuration",
    )

    assert score == pytest.approx(2 / 3)


def test_match_score_rejects_only_one_shared_token():
    score = sub_graper.match_score(
        "payment handler",
        "payment repository",
    )

    assert score == 0.0
