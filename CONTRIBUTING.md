# Contributing to pytest-rag

> We accept bug reports, feature requests, and questions via the GitHub
> issue templates in [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/).
> Pull requests are welcome for tasks tagged with `T-DONE` in the
> `TODO.md` tracker.

## Where to start

1. Read [`docs/AGENTS.md`](docs/AGENTS.md) — the working contract.
2. Read [`docs/PLANNING.md`](docs/PLANNING.md) — the roadmap and
   per-task acceptance criteria.
3. Read [`docs/TODO.md`](docs/TODO.md) — the current status board.
4. Pick a task with status `TODO` whose dependencies are `DONE`.

## Branching and commits

- One task per branch (`feat/rg-2-4-ndcg`, `fix/rg-3-4-third-party-import`, ...).
- Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`,
  `test:`). The AGENTS.md CLI wrapper auto-strips the `Co-authored-by:`
  trailer on commits made through this CLI; please do not add it manually.
- Reference the task ID in the body, e.g. `Refs: RG-2.4`.

## Local development

```bash
uv sync --all-extras
uv run nox -s lint-3.12 types-3.12 tests-3.12
```

CI runs the same matrix on Python 3.10–3.13 and pytest 7/8 — see
[`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Invariants you must not break

- `I-NOLLM` — no LLM/embedder imports in the runtime package.
- `I-NET` — no network calls in the runtime package.
- `I-ISOLATION` — the plugin must not change the behaviour of tests
  that do not use the `rag` marker.
- `I-DET` — every metric and bootstrap must be seeded explicitly.
- `I-FAILLOUD` — a retriever exception must fail the test, not be
  silently swallowed.

The CI `invariants` job greps for forbidden imports in `src/pytest_rag/`.
The pytester-based isolation test (canonical `I-ISOLATION`) is scheduled
for RG-8.4.

## What "DONE" means

For each task, the Definition of Done is in `PLANNING.md §3`. The
quick heuristics:

- Tests added and passing locally and on CI.
- `CHANGELOG.md` entry under `[Unreleased]`.
- `docs/PLANNING.md` and `docs/TODO.md` updated for that task.
- The branch is rebased on `main` and the CI matrix is green
  (9/9: 8 matrix jobs + invariants).

## Out of scope (do not PR without the maintainer's explicit go-ahead)

- Adding new runtime dependencies (any of `numpy`, `scipy`, `pandas`,
  `sklearn`, `rich`, `jinja2`, `pydantic`, etc.). Per AGENTS.md §6
  these require owner approval.
- Adding a Trusted Publishing or PyPI release workflow. Scheduled for
  P9 / RG-9.5.
- Anything that touches `docs/`. That directory is private and tracked
  by a separate `git init`; the maintainer integrates those changes.

## Code of conduct

The maintainer reserves the right to close issues that are not
constructive. Bug reports without a reproduction are deprioritised.
Feature requests must reference a concrete use case.
