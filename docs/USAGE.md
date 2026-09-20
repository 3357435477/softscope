# Usage Guide

SoftScope is intentionally small: one command gathers local software inventory and prints or writes the report.

## Scan Installed Software

```powershell
softscope scan
```

On Windows, SoftScope reads standard uninstall registry locations under `HKLM` and `HKCU`. On other systems, the scanner returns an empty result so contributors can still run tests and develop the CLI.

## Export JSON

```powershell
softscope scan --format json --output reports/software.json
```

JSON is best for follow-up processing or importing into another tool.

## Export CSV

```powershell
softscope scan --format csv --output reports/software.csv
```

CSV is useful for spreadsheet review.

## Check Update Hints

```powershell
softscope scan --updates
```

When `winget` is installed, SoftScope runs `winget upgrade` and matches update hints by application name. If `winget` is unavailable or times out, the inventory still completes.

## Fields

- `name`: Display name from the software installer.
- `version`: Installed version when available.
- `publisher`: Publisher or vendor.
- `install_date`: Install date normalized from `YYYYMMDD` to `YYYY-MM-DD`.
- `install_location`: Local install path when recorded by the installer.
- `uninstall_command`: Registered uninstall command.
- `source`: Registry location used for the record.
- `update_available`: `true`, `false`, or `null` when update status is unknown.
- `latest_version`: Latest version from `winget` when an update is found.
