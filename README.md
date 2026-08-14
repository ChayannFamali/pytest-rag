# pytest-rag

> **CI gate for retrieval quality.** nDCG / recall / MRR, paired bootstrap, per-query diff.
> No LLM. No network. Deterministic.

Status: **pre-alpha** (P0 / RG-0.2 scaffold). See [`docs/PLANNING.md`](docs/PLANNING.md)
for the roadmap and [`docs/AGENTS.md`](docs/AGENTS.md) for the working contract.

## What this is

A pytest plugin that turns retrieval quality into a merge gate. You give it one
function `(query, k) -> list[doc_id]` and a golden set; it computes
nDCG/recall/MRR, compares against a frozen baseline, filters out noise with a
paired bootstrap, and fails the test on a statistically significant regression —
with a per-query diff showing which document dropped out of top-k and where it
landed.

## What this is not

- Not **ragas** — no LLM judge, no generation metrics.
- Not **BEIR** — no research harness, no public dataset downloads.
- Not a **RAG framework** — we do not index, chunk, or embed.

## Quickstart (placeholder, will be expanded in RG-9.1)

```bash
pip install pytest-rag
pytest --rag --rag-dataset golden.jsonl
```

## Development

```bash
uv sync --all-extras
uv run pytest -q
uv run ruff check src tests
uv run mypy --strict src
```

## License

MIT — see [`LICENSE`](LICENSE) (RG-0.5).
