# Changelog

All notable changes to pytest-rag are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **RG-0.2**: project skeleton. `pyproject.toml` with hatchling backend and
  src-layout; minimal `src/pytest_rag/{__init__,plugin,cli}.py` stubs (no
  side effects on import — I-ISOLATION); `tests/test_smoke.py`; `README.md`.
  Core dependencies: `pytest>=7.0`, `numpy>=1.24`. Extras: `dev` (ruff, mypy,
  nox, pytest-cov, pytest-xdist) and `report` (empty placeholder, populated in
  RG-6.5/RG-6.6 per AGENTS.md §6). Entry points: `[project.scripts] rag-eval`
  → `pytest_rag.cli:main`, `[project.entry-points.pytest11] pytest_rag` →
  `pytest_rag.plugin`. Lint/type/test toolchain configured (ruff, mypy --strict,
  pytest with `--strict-markers`). `uv sync --all-extras` resolves 29 packages
  in < 10 s; `uv run pytest -q` → 4 passed; `uv run mypy --strict src` →
  no issues; `uv run ruff {check,format} src tests` → clean.

### Notes
- **RG-0.1 deferred**: PyPI/TestPyPI account creation and Trusted Publishing
  (OIDC) are deferred to P9/RG-9.5 by owner decision. GitHub repository
  `github.com/ChayannFamali/pytest-rag` is in place; package names `pytest-rag`
  and `pytest-retrieval` are reserved (verified free on PyPI, TestPyPI, GitHub).
- **Memory**: I-ISOLATION proof at the scaffold level — the plugin module
  imports cleanly without registering any `--rag-*` options or altering the
  default pytest session. Full pytester-based isolation test is scheduled
  for RG-8.4.
- **Toolchain**: nox sessions (`lint`, `types`, `tests`, `metrics-verify`,
  `selftest`, `docs`) are scheduled for RG-0.3; for now the equivalent
  commands are run directly via `uv run`.

[0.0.1]: https://github.com/ChayannFamali/pytest-rag/releases/tag/v0.0.1
