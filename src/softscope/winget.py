from __future__ import annotations

import shutil
import subprocess

from softscope.models import SoftwareRecord


def enrich_with_winget_updates(records: list[SoftwareRecord]) -> list[SoftwareRecord]:
    updates = _load_winget_updates()
    if not updates:
        return records

    enriched: list[SoftwareRecord] = []
    for record in records:
        latest = _match_update(record.name, updates)
        if latest:
            enriched.append(
                SoftwareRecord(
                    **{
                        **record.as_dict(),
                        "update_available": True,
                        "latest_version": latest,
                    }
                )
            )
        else:
            enriched.append(SoftwareRecord(**{**record.as_dict(), "update_available": False}))
    return enriched


def _load_winget_updates() -> dict[str, str]:
    if shutil.which("winget") is None:
        return {}

    try:
        result = subprocess.run(
            ["winget", "upgrade", "--accept-source-agreements"],
            check=False,
            capture_output=True,
            text=True,
            timeout=45,
        )
    except (OSError, subprocess.TimeoutExpired):
        return {}

    if result.returncode not in {0, 1}:
        return {}

    return _parse_winget_upgrade_output(result.stdout)


def _parse_winget_upgrade_output(output: str) -> dict[str, str]:
    updates: dict[str, str] = {}
    lines = [line.rstrip() for line in output.splitlines() if line.strip()]

    separator_index = next((index for index, line in enumerate(lines) if set(line) == {"-"}), None)
    if separator_index is None:
        return updates

    for line in lines[separator_index + 1 :]:
        if line.lower().startswith("the following packages"):
            break
        if len(line.split()) < 4:
            continue

        columns = line.rsplit(maxsplit=4)
        if len(columns) < 5:
            continue

        name, _package_id, _current_version, available_version, _source = columns
        updates[name.strip().casefold()] = available_version.strip()

    return updates


def _match_update(name: str, updates: dict[str, str]) -> str:
    lowered = name.casefold()
    if lowered in updates:
        return updates[lowered]

    for winget_name, latest in updates.items():
        if lowered in winget_name or winget_name in lowered:
            return latest
    return ""
