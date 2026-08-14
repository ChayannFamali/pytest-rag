---
name: Bug report
about: Something doesn't work
title: "[bug] "
labels: ["bug", "needs-triage"]
assignees: []
---

## Summary

<One-line description of the bug.>

## Reproduction

```python
# Minimal code that triggers the bug
```

### Dataset

- `dataset` path or hash:
- `pytest` version: `pytest --version`
- `pytest-rag` version: `pip show pytest-rag`
- Python version: `python --version`

### Retriever

- Module / function under test:
- `k` value:
- `--rag-seed` value (if any):

## Expected

<What you expected to happen.>

## Actual

<What actually happened, including the full pytest output.>

## Environment

- OS / arch:
- CI or local:
- Did this work before? If yes, last known-good version:

## I-ISOLATION check

- [ ] Failing without `--rag-*` options:
- [ ] Failing with `--rag-skip-baseline` (if applicable):
- [ ] Failing without the `rag` marker:

Refs: https://github.com/ChayannFamali/pytest-rag/blob/main/docs/AGENTS.md
