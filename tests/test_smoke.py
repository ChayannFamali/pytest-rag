"""Smoke tests for RG-0.2.

These verify the package + entry-points resolve cleanly under
`uv sync --all-extras` and that the import has no side effects
(I-ISOLATION at the scaffolding level).
"""

from __future__ import annotations

import pytest_rag


def test_version_is_string() -> None:
    assert isinstance(pytest_rag.__version__, str)
    assert pytest_rag.__version__ == "0.0.1"


def test_public_api_is_minimal() -> None:
    assert pytest_rag.__all__ == ["__version__"]


def test_plugin_module_imports_with_empty_public_api() -> None:
    from pytest_rag import plugin

    assert plugin.__all__ == []


def test_cli_main_returns_zero() -> None:
    from pytest_rag.cli import main

    assert main() == 0
