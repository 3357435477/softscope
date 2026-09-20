from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class SoftwareRecord:
    name: str
    version: str = ""
    publisher: str = ""
    install_date: str = ""
    install_location: str = ""
    uninstall_command: str = ""
    source: str = ""
    update_available: bool | None = None
    latest_version: str = ""

    def as_dict(self) -> dict[str, object]:
        return asdict(self)
