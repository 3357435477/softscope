from __future__ import annotations

import platform
from collections.abc import Iterable

from softscope.models import SoftwareRecord

REGISTRY_UNINSTALL_PATHS = (
    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
    r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
)


def collect_installed_software() -> list[SoftwareRecord]:
    if platform.system() != "Windows":
        return []

    return sorted(_collect_windows_registry(), key=lambda record: record.name.casefold())


def _collect_windows_registry() -> list[SoftwareRecord]:
    import winreg

    records: dict[tuple[str, str, str], SoftwareRecord] = {}
    roots = (
        (winreg.HKEY_LOCAL_MACHINE, "HKLM"),
        (winreg.HKEY_CURRENT_USER, "HKCU"),
    )

    for root, root_name in roots:
        for uninstall_path in REGISTRY_UNINSTALL_PATHS:
            for record in _read_uninstall_key(winreg, root, root_name, uninstall_path):
                key = (record.name.casefold(), record.version, record.publisher.casefold())
                records.setdefault(key, record)

    return list(records.values())


def _read_uninstall_key(
    winreg_module: object,
    root: int,
    root_name: str,
    uninstall_path: str,
) -> Iterable[SoftwareRecord]:
    try:
        parent = winreg_module.OpenKey(root, uninstall_path)
    except OSError:
        return

    with parent:
        index = 0
        while True:
            try:
                subkey_name = winreg_module.EnumKey(parent, index)
            except OSError:
                break
            index += 1

            record = _read_application_key(
                winreg_module,
                parent,
                subkey_name,
                source=f"{root_name}\\{uninstall_path}",
            )
            if record is not None:
                yield record


def _read_application_key(
    winreg_module: object,
    parent: object,
    subkey_name: str,
    source: str,
) -> SoftwareRecord | None:
    try:
        subkey = winreg_module.OpenKey(parent, subkey_name)
    except OSError:
        return None

    with subkey:
        values = _read_values(winreg_module, subkey)

    name = str(values.get("DisplayName", "")).strip()
    if not name:
        return None

    if str(values.get("SystemComponent", "0")) == "1":
        return None

    release_type = str(values.get("ReleaseType", "")).strip().lower()
    if release_type in {"security update", "update rollup", "hotfix"}:
        return None

    return SoftwareRecord(
        name=name,
        version=str(values.get("DisplayVersion", "")).strip(),
        publisher=str(values.get("Publisher", "")).strip(),
        install_date=_format_install_date(str(values.get("InstallDate", "")).strip()),
        install_location=str(values.get("InstallLocation", "")).strip(),
        uninstall_command=str(values.get("UninstallString", "")).strip(),
        source=source,
    )


def _read_values(winreg_module: object, key: object) -> dict[str, object]:
    values: dict[str, object] = {}
    index = 0
    while True:
        try:
            name, value, _value_type = winreg_module.EnumValue(key, index)
        except OSError:
            break
        values[name] = value
        index += 1
    return values


def _format_install_date(raw: str) -> str:
    if len(raw) == 8 and raw.isdigit():
        return f"{raw[:4]}-{raw[4:6]}-{raw[6:]}"
    return raw
