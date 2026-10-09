"""Contracts for the category vocabulary used by shipped pipelines.

Every manifest's `category` must be one of the values the manifest schema
allows, or `jsonschema` validation fails at load time and the pipeline cannot
run at all.

This iterates the shipped pipelines rather than naming one, so adding or
removing a pipeline cannot leave the contract untested or pointing at a
manifest that no longer exists.
"""

import json
from pathlib import Path

import pytest

from lib.pipeline_loader import list_pipelines, load_pipeline

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "schemas" / "pipelines" / "pipeline_manifest.schema.json"

ALLOWED_CATEGORIES = set(
    json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))["properties"]["category"]["enum"]
)
PIPELINES = sorted(list_pipelines())


def test_schema_declares_a_category_vocabulary() -> None:
    assert ALLOWED_CATEGORIES, f"{SCHEMA_PATH} declares no category enum"


def test_pipelines_are_discovered() -> None:
    """Guard against the parametrized test below silently covering nothing."""
    assert PIPELINES


@pytest.mark.parametrize("name", PIPELINES)
def test_pipeline_uses_a_schema_supported_category(name: str) -> None:
    category = load_pipeline(name).get("category")
    assert category in ALLOWED_CATEGORIES, (
        f"pipeline {name!r} declares category {category!r}, which is not in the "
        f"manifest schema's enum ({sorted(ALLOWED_CATEGORIES)})"
    )
