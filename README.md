# SoftScope

SoftScope is a small Python CLI that inventories installed desktop software and can optionally ask `winget` whether known packages have updates. It is designed for students, help-desk technicians, and small teams who need a simple, auditable report without installing an agent.

## Features

- Scans Windows uninstall registry keys for installed applications.
- Captures application name, version, publisher, install date, install location, uninstall command, and source.
- Falls back gracefully on non-Windows systems so development and tests still work.
- Exports reports as a console table, JSON, or CSV.
- Optionally enriches records with `winget upgrade` results when `winget` is available.
- Includes tests, lint configuration, GitHub Actions, and a clean package layout.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
softscope scan
```

Export a report:

```powershell
softscope scan --format json --output reports/software.json
softscope scan --format csv --output reports/software.csv
```

Filter a report:

```powershell
softscope scan --filter microsoft
softscope scan --filter "visual studio"
```

Check update hints with Winget:

```powershell
softscope scan --updates
```

## Example

```text
Name                  Version      Publisher            Update
--------------------  -----------  -------------------  ---------
Python 3.12.5         3.12.5       Python Software...   unknown
Git                   2.46.0       The Git Development  available
Visual Studio Code    1.92.2       Microsoft Corp...    current
```

## Privacy

SoftScope runs locally and does not upload inventory data. Reports can include sensitive internal application names or install paths, so review generated files before sharing them.

## Development

```powershell
pip install -e ".[dev]"
pytest
ruff check .
```

## Roadmap

- Add signed executable builds.
- Add optional vulnerability matching from a user-provided advisory file.
- Add a lightweight desktop UI.
- Add Linux package-manager collectors.

## License

MIT
