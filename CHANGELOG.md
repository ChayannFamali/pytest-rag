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

### Changed
- **RG-0.2 patch**: pin `pytest>=7,<9` (was `pytest>=7.0`). Resolves to
  pytest 8.4.2; keeps the CI matrix claim in `PLANNING.md §1` (3.10-3.13 ×
  pytest 7/8) honest. See commit `93d783b`.
- **RG-0.3**: `noxfile.py` with 6 sessions (`lint`, `types`, `tests`,
  `metrics_verify`, `selftest`, `docs`) × 4 Python (3.10-3.13) = 24
  variants. `nox -s lint-3.12 types-3.12 tests-3.12` ✅; the three
  NO-OP sessions explicitly `session.skip(...)` until RG-2.7/RG-8.1/
  RG-9.2 ship. The `--cov-fail-under=85` gate is deferred to P2/RG-2.0
  (P0/P1 modules are no-op stubs; coverage-fail-under is structurally
  unreachable). New test: `tests/test_noxfile.py` (6 tests).

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
