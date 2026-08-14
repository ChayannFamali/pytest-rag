"""Confirms the noxfile boots on the working interpreter and advertises the
mandated sessions. Per AGENTS.md §13 those are: lint, types, tests,
metrics-verify, selftest, docs. RG-0.3 asserts *presence* only; correctness
per session is checked when each session is run.
"""

from __future__ import annotations

import inspect
import runpy

# Importing the noxfile as a module would not run the top-level nox.sessions
# decorators against the same registry that ``nox --list`` reads, so we
# execfile the noxfile with a throwaway globals dict and then probe the
# resulting module. This is what ``nox --list`` does internally.
_NOXFILE_GLOBALS: dict[str, object] = runpy.run_path("noxfile.py", run_name="__noxfile__")


def _has_session(name: str) -> bool:
    """Return True if a nox session named ``name`` was registered by the file."""
    return name in _NOXFILE_GLOBALS


def test_required_sessions_registered() -> None:
    for name in ("lint", "types", "tests", "metrics_verify", "selftest", "docs"):
        assert _has_session(name), f"missing nox session {name!r}"


def test_required_sessions_are_nox_sessions() -> None:
    # nox.session(...) returns a FunctionAlias that wraps the original
    # function. We check the type via the __nox_session__ attribute that
    # current nox versions stamp on the wrapper.
    for name in ("lint", "types", "tests", "metrics_verify", "selftest", "docs"):
        attr = _NOXFILE_GLOBALS[name]
        assert hasattr(attr, "__wrapped__") or hasattr(attr, "__nox_session__"), (
            f"{name!r} is not a nox session"
        )


def test_coverage_threshold_matches_agents_md() -> None:
    """AGENTS.md §14 sets the gate at 85 % for the runtime package."""
    assert _NOXFILE_GLOBALS["COVERAGE_THRESHOLD"] == 85


def test_python_versions_match_planning_do_d() -> None:
    """PLANNING.md §1 DoD: matrix is 3.10-3.13 x pytest 7/8."""
    assert _NOXFILE_GLOBALS["PYTHON_VERSIONS"] == ["3.10", "3.11", "3.12", "3.13"]


def test_default_sessions_match_agents_md() -> None:
    """AGENTS.md §13 sequence is lint, types, tests; metrics-verify/selftest/docs
    run explicitly only when the relevant phase ships."""
    opts = _NOXFILE_GLOBALS["nox"].options
    assert list(opts.sessions) == ["lint", "types", "tests"]


def test_no_nox_sessions_use_subprocess_flags_unsafely() -> None:
    """Sanity: no session runs an interactive command via ``nox.run``."""
    for name in ("lint", "types", "tests"):
        src = inspect.getsource(_NOXFILE_GLOBALS[name])
        assert "--interactive" not in src, f"{name}: --interactive found"
        assert "--pdb" not in src, f"{name}: --pdb found"
