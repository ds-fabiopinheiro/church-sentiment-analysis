# Contributing

Thank you for helping preachers everywhere. Three rules keep this project trustworthy; pull requests that break them are not merged.

1. **Privacy by construction.** No frame, face crop, embedding, tracking id or per-person field — anywhere. `CLAUDE.md` lists the rules; `tests/` and the CI enforce them.
2. **Observed reaction, never inferred feeling.** Text shown to preachers passes `reacao/lint.py`.
3. **Measured, not opined.** New engines go through `bench.py` on the labeled corpus; decisions are recorded in `docs/adr/`.

## Ways to contribute
- **Translations:** copy `README.md` to `README.<lang>.md`, translate, add the link in every README. Native review is welcome for existing translations (hi, bn, ar, zh-CN, ja were machine-assisted).
- **Validation data:** publicly available sermon videos that allow download, with audience shots; add a row to `docs/corpus.csv` with the license.
- **Local law notes:** a short file in `docs/law/<country>.md` describing what a church must do before processing its own recordings.
- **Code:** open an issue first for anything touching `reacao/guard.py`, `reacao/aggregate.py` or the Supabase schema.

## Development
```
uv venv && uv pip install -e ".[dev]"
uv run ruff check . && uv run pytest -q
```
Reference the backlog item in the PR title, e.g. `PBI-104: filtro de cena`.

## Code of conduct
Be kind, be precise, assume good faith. Disagreements are settled with measurements.
