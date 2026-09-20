from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import TextIO

from softscope.models import SoftwareRecord

FIELDS = (
    "name",
    "version",
    "publisher",
    "install_date",
    "install_location",
    "uninstall_command",
    "source",
    "update_available",
    "latest_version",
)


def write_report(records: list[SoftwareRecord], report_format: str, output: Path | None) -> None:
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8", newline="") as stream:
            _write(records, report_format, stream)
        return

    _write(records, report_format, sys.stdout)


def _write(records: list[SoftwareRecord], report_format: str, stream: TextIO) -> None:
    if report_format == "json":
        json.dump([record.as_dict() for record in records], stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    elif report_format == "csv":
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(record.as_dict() for record in records)
    else:
        stream.write(format_table(records))
        stream.write("\n")


def format_table(records: list[SoftwareRecord]) -> str:
    if not records:
        return "No installed software records were found."

    rows = [
        (
            _clip(record.name, 34),
            _clip(record.version, 16),
            _clip(record.publisher, 24),
            _format_update(record),
        )
        for record in records
    ]
    headers = ("Name", "Version", "Publisher", "Update")
    widths = tuple(
        max(len(str(value)) for value in column)
        for column in zip(headers, *rows, strict=False)
    )
    template = "  ".join(f"{{:<{width}}}" for width in widths)
    divider = "  ".join("-" * width for width in widths)

    output = [template.format(*headers), divider]
    output.extend(template.format(*row) for row in rows)
    return "\n".join(output)


def _format_update(record: SoftwareRecord) -> str:
    if record.update_available is True:
        return f"available ({record.latest_version})" if record.latest_version else "available"
    if record.update_available is False:
        return "current"
    return "unknown"


def _clip(value: str, length: int) -> str:
    if len(value) <= length:
        return value
    return value[: length - 1] + "..."
