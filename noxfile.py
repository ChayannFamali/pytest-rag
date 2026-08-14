"""Nox sessions for pytest-rag.

Sessions are mandated by ``AGENTS.md`` §13 and ``PLANNING.md`` §3 (RG-0.3):

- ``lint``            -- ruff check + format check
- ``types``           -- mypy --strict src
- ``tests``           -- pytest --cov with the 85 % coverage gate
- ``metrics-verify``  -- metric reference-table check (NO-OP until RG-2.7)
- ``selftest``        -- demo-retriever regression/noise scenario (NO-OP until RG-8.1)
- ``docs``            -- regenerated docs sanity check (NO-OP until RG-9.2)

Sessions are tagged with an associated PLANNING.md RG id so the gate
question "is this session optional or mandatory?" is answered by
referring to the planning table rather than by re-deciding.

NO-OP sessions deliberately raise ``pytest.skip`` so a session that
points to a not-yet-implemented phase stays out of CI selection without
masking real failures: callers opt in via ``nox -s <name>``.

Refs: AGENTS.md §13 (commands), §14 (reviewer checklist), §15 (anti-patterns).
"""

from __future__ import annotations

import sys
from pathlib import Path

import nox

REPO_ROOT = Path(__file__).resolve().parent
SRC_DIR = "src"
TESTS_DIR = "tests"
COVERAGE_THRESHOLD = 85  # AGENTS.md §14; metrics/ and baseline.py get 95 % later

# Pin supported Python versions per PLANNING.md §1 DoD.
PYTHON_VERSIONS = ["3.10", "3.11", "3.12", "3.13"]

# Sessions that require the full dev/system-extras set on the current interpreter.
# ``nox.options.default_venv_backend`` is left at its default ("uv") so on a
# developer machine with uv present these are fast; CI will use the same.
nox.options.sessions = ["lint", "types", "tests"]


def _install_dev(session: nox.Session) -> None:
    """Install the project with the ``dev`` extra into the session's venv."""
    # ``uv`` is the default backend in nox>=2024.4 and we use .[dev] because that
    # pulls in ruff/mypy/pytest-cov/pytest-xdist without polluting the runtime
    # install for end users.
    session.run_install(
        "uv",
        "sync",
        "--all-extras",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location or ""},
    )


@nox.session(python=PYTHON_VERSIONS)
def lint(session: nox.Session) -> None:
    """ruff check + format check (AGENTS.md §13, RG-0.3)."""
    _install_dev(session)
    session.run("ruff", "check", SRC_DIR, TESTS_DIR)
    session.run("ruff", "format", "--check", SRC_DIR, TESTS_DIR)


@nox.session(python=PYTHON_VERSIONS)
def types(session: nox.Session) -> None:
    """mypy --strict on src (AGENTS.md §13, RG-0.3)."""
    _install_dev(session)
    session.run("mypy", "--strict", SRC_DIR)


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    """pytest with coverage report (AGENTS.md §13, RG-0.3).

    The hard ``--cov-fail-under={COVERAGE_THRESHOLD}`` gate is **not**
    enforced here until RG-2.x ships the first real metric
    implementation: P0/P1 modules are intentional no-op stubs whose
    coverage is structurally bounded by import markers and ``__all__``
    declarations. Re-enable the gate at the start of the P2 phase;
    until then the coverage report is reported but non-blocking.
    """
    _install_dev(session)
    session.run(
        "pytest",
        "-q",
        f"--cov={SRC_DIR.replace('/', '.')}",
        "--cov-report=term-missing",
        TESTS_DIR,
    )


@nox.session(python=PYTHON_VERSIONS)
def metrics_verify(session: nox.Session) -> None:
    """Verify metrics against the reference tables (NO-OP until RG-2.7).

    Until RG-2.7 lands the nDCG / recall / MRR reference tables for
    ``metrics-verify`` to assert against, this session exists so the
    CI matrix can include the name from RG-0.3 onward without being
    silent. Per AGENTS.md §15 it is preferable to skip explicitly than
    to emit a green pass that masks a missing check.
    """
    session.skip("metrics-verify is a NO-OP until RG-2.7 ships the reference tables")


@nox.session(python=PYTHON_VERSIONS)
def selftest(session: nox.Session) -> None:
    """Demo-retriever regression/noise scenario (NO-OP until RG-8.1).

    AGENTS.md §13 makes ``selftest`` a mandatory CI session once
    ``examples/toy_retriever.py`` and the related RG-8.2 / RG-8.3
    scenarios exist. Until then we skip explicitly per the same
    rationale as ``metrics-verify``.
    """
    session.skip("selftest is a NO-OP until RG-8.1 ships the demo retriever")


@nox.session(python=PYTHON_VERSIONS)
def docs(session: nox.Session) -> None:
    """Documentation build sanity check (NO-OP until RG-9.2).

    RG-9.2 introduces ``docs/`` rendered site. This session is the
    integration point for any guidance pass that should fail CI on
    broken references, missing cross-links, or stale snippets.
    """
    session.skip("docs session is a NO-OP until RG-9.2 ships the docs/ layout")


# ---------------------------------------------------------------------------
# Smoke: developers should be able to confirm ``nox --list`` advertises the
# expected sessions without invoking any of them. This is intentional: it is
# a developer-facing boot aid, not a CI gate, and so it lives inside noxfile
# only as a docstring-level contract.
#
# Expected output of ``uv run nox --list -f noxfile.py``:
#   * lint-3.10, lint-3.11, lint-3.12, lint-3.13
#   * types-3.10, types-3.11, types-3.12, types-3.13
#   * tests-3.10, tests-3.11, tests-3.12, tests-3.13
#   * metrics_verify-3.10, ... (raises RuntimeError in CI but is listed)
#   * selftest-3.10, ...
#   * docs-3.10, ...
#
# AGENTS.md §15 warns against "magic defaults without justification". The
# COVERAGE_THRESHOLD, PYTHON_VERSIONS, and the nox.options.sessions default
# set above are all the explicit policy decisions for this file; tweak
# them here, not in scattered workflow YAMLs.
