from __future__ import annotations

import argparse
from pathlib import Path

from softscope.collectors import collect_installed_software
from softscope.exporters import write_report
from softscope.winget import enrich_with_winget_updates


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="softscope",
        description="Inventory installed desktop software and export a local report.",
    )
    subparsers = parser.add_subparsers(dest="command")

    scan = subparsers.add_parser("scan", help="scan installed software")
    scan.add_argument(
        "--format",
        choices=("table", "json", "csv"),
        default="table",
        help="report output format",
    )
    scan.add_argument(
        "--output",
        type=Path,
        help="write report to this file instead of stdout",
    )
    scan.add_argument(
        "--updates",
        action="store_true",
        help="use winget to add update availability hints when possible",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command in {None, "scan"}:
        records = collect_installed_software()
        if getattr(args, "updates", False):
            records = enrich_with_winget_updates(records)
        write_report(records, getattr(args, "format", "table"), getattr(args, "output", None))
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2
