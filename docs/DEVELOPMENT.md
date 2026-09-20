# Development Notes

## Milestone 1: Project Foundation

- Package metadata in `pyproject.toml`.
- Source layout under `src/`.
- Tests under `tests/`.
- CI with GitHub Actions.

## Milestone 2: Inventory Scanner

- Windows uninstall registry collector.
- Structured `SoftwareRecord` model.
- Basic filtering for system components and Windows hotfix entries.

## Milestone 3: Reports and Update Hints

- Table, JSON, and CSV outputs.
- Optional `winget` update enrichment.
- User-facing README and usage guide.

## Quality Gates

Run these before pushing:

```powershell
pytest
ruff check .
```
