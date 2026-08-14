"""Standalone CLI entry point.

The real commands (`rag-eval run`, `rag-eval baseline`, `rag-eval report`) are
implemented in P7 (RG-7.1, RG-7.2). For RG-0.2 this provides a minimal
`main()` so the `[project.scripts]` entry point resolves.
"""

from __future__ import annotations

import sys


def main() -> int:  # pragma: no cover
    """Placeholder CLI entry point. Returns 0 in RG-0.2; real CLI in P7."""
    print("pytest-rag 0.0.1: CLI not yet implemented (RG-7.1)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
