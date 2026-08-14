"""Repo-file metadata guards for RG-0.5.

These tests exercise the project meta package layer only: LICENSE,
CHANGELOG.md, README.md, CONTRIBUTING.md, MANIFEST.in, and the
issue templates under .github/ISSUE_TEMPLATE/. They do not exercise
any runtime behaviour; they exist so the answer to "is the
distribution artifact complete?" is a single `pytest` invocation.
"""

from __future__ import annotations

import pathlib
import re

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


def test_license_file_present() -> None:
    assert (REPO_ROOT / "LICENSE").is_file()


def test_license_mit_with_copyright() -> None:
    text = (REPO_ROOT / "LICENSE").read_text()
    assert "MIT License" in text
    assert "Copyright (c) 2026 ChayannFamali" in text
    # Standard MIT marker phrase
    assert "Permission is hereby granted, free of charge" in text


def test_license_expression_matches_pyproject() -> None:
    pyproject = (REPO_ROOT / "pyproject.toml").read_text()
    # The pyproject.toml has license = { text = "MIT" } for now; we
    # accept either "text = \"MIT\"" or "expression = \"MIT\"" form.
    assert re.search(r'license\s*=\s*\{[^}]*(text|expression)\s*=\s*"MIT"', pyproject), (
        "pyproject.toml does not declare MIT as the license"
    )


def test_changelog_present() -> None:
    assert (REPO_ROOT / "CHANGELOG.md").is_file()
    text = (REPO_ROOT / "CHANGELOG.md").read_text()
    # Keep-a-Changelog marker
    assert "## [Unreleased]" in text


def test_readme_present() -> None:
    assert (REPO_ROOT / "README.md").is_file()


def test_contributing_present() -> None:
    assert (REPO_ROOT / "CONTRIBUTING.md").is_file()
    text = (REPO_ROOT / "CONTRIBUTING.md").read_text()
    # Should signpost the private docs/ repo
    assert "docs/AGENTS.md" in text
    assert "docs/PLANNING.md" in text
    # Should NOT promise SLAs or timelines (AGENTS.md §15)
    assert "eta" not in text.lower()
    assert "sla" not in text.lower()


def test_manifest_in_present() -> None:
    assert (REPO_ROOT / "MANIFEST.in").is_file()
    text = (REPO_ROOT / "MANIFEST.in").read_text()
    # Must include LICENSE, CHANGELOG.md, README.md, the issue templates
    # dir. We only inspect the lines that start with `include` or
    # `recursive-include` so a comment mentioning docs/ is not a false
    # positive.
    include_lines = [
        ln for ln in text.splitlines() if ln.lstrip().startswith(("include ", "recursive-include "))
    ]
    include_blob = "\n".join(include_lines)
    assert "include LICENSE" in include_blob
    assert "include CHANGELOG.md" in include_blob
    assert "include README.md" in include_blob
    assert "ISSUE_TEMPLATE" in include_blob
    # And must NOT include docs/ (private repo)
    assert "docs/" not in include_blob, "MANIFEST.in must not include the private docs/ dir"


def test_manifest_in_excludes_docs_dir() -> None:
    """Verify the MANIFEST.in active lines do not include docs/."""
    text = (REPO_ROOT / "MANIFEST.in").read_text()
    include_lines = [
        ln
        for ln in text.splitlines()
        if ln.lstrip().startswith(("include ", "recursive-include ", "recursive-exclude "))
    ]
    for ln in include_lines:
        assert "docs/" not in ln, f"MANIFEST.in must not include the private docs/ dir: {ln!r}"


def test_issue_templates_directory() -> None:
    tpl_dir = REPO_ROOT / ".github" / "ISSUE_TEMPLATE"
    assert tpl_dir.is_dir()
    expected = {"bug.md", "feature.md", "question.md", "config.yml"}
    actual = {p.name for p in tpl_dir.iterdir() if p.is_file()}
    missing = expected - actual
    assert not missing, f"missing issue templates: {sorted(missing)}"


def test_issue_templates_have_yaml_frontmatter() -> None:
    for name in ("bug.md", "feature.md", "question.md"):
        text = (REPO_ROOT / ".github" / "ISSUE_TEMPLATE" / name).read_text()
        assert text.startswith("---\n"), f"{name}: missing YAML frontmatter"
        assert "name:" in text.split("---")[1]
        assert "labels:" in text


def test_config_yml_disables_blank_issues() -> None:
    text = (REPO_ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml").read_text()
    assert "blank_issues_enabled: false" in text


def test_no_codeowners_in_scope() -> None:
    """AGENTS.md §6: CODEOWNERS is 'owner approval required'. We do not
    create it in RG-0.5; the maintainer adds it explicitly. This test
    documents the decision so a future PR that adds CODEOWNERS without
    owner approval is caught."""
    codeowners = REPO_ROOT / ".github" / "CODEOWNERS"
    assert not codeowners.exists(), (
        "CODEOWNERS is out-of-scope for RG-0.5 (AGENTS.md §6). "
        "Remove this assertion only when the owner has approved the file."
    )


def test_no_security_md_in_scope() -> None:
    """AGENTS.md §6: SECURITY.md is 'owner approval required'."""
    security = REPO_ROOT / "SECURITY.md"
    assert not security.exists(), (
        "SECURITY.md is out-of-scope for RG-0.5 (AGENTS.md §6). "
        "Remove this assertion only when the owner has approved the file."
    )
