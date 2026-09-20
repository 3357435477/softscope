# Contributing

Thanks for helping improve SoftScope.

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Checks

```powershell
pytest
ruff check .
```

## Pull Requests

- Keep changes focused.
- Add or update tests for behavior changes.
- Avoid committing generated reports or local environment files.
- Review reports before sharing because inventory data can expose internal software names and paths.
