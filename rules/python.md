---
paths:
  - "**/*.py"
  - "**/pyproject.toml"
---

# Python

- Python 3.11 or newer. `pyproject.toml` is the single source of metadata and dependencies; manage the
  environment with `uv` (`uv sync`, `uv run`). No `requirements.txt` unless a platform demands it.
- Layout: `src/<package>/` with one module per responsibility, `__main__.py` as the entry point
  (`uv run python -m <package>`), `tests/` mirroring `src/`.
- Type hints on every public signature. Modern syntax: `list[int]`, `X | None`.
- Value objects and config: `@dataclass(frozen=True, slots=True)`. Paths: `pathlib.Path`.
- Config: one `config.py` that reads `config.toml` with `tomllib` into frozen dataclasses, one per
  section. Construct it once in `__main__.py`.
- Numerics: vectorise with NumPy/PyTorch; no Python loops over array elements on hot paths. Keep
  device and dtype explicit.
- `logging` in library code, `print` only in CLI output.
- Lint and format with `ruff` (`ruff format`, `ruff check --fix`). In `pyproject.toml`:

  ```toml
  [tool.ruff]
  line-length = 100
  [tool.ruff.lint]
  select = ["E", "F", "I", "UP", "B", "SIM", "NPY"]
  ```

- Tests with `pytest`. Notebooks are for exploration only; nothing in `src/` imports from them.
- Figures for `details/` use `details/details.mplstyle` so they match the PDF.
