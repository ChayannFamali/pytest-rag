"""pytest plugin entry point.

Real hooks (markers, CLI options, fixtures, terminal summary) are registered
in RG-3.4. For RG-0.2 this module exists only to satisfy the entry-point and
keep `uv sync --all-extras` working. Import MUST be free of side effects
beyond the implicit plugin registration (see AGENTS.md §4 / I-ISOLATION).
"""

from __future__ import annotations

__all__: list[str] = []
