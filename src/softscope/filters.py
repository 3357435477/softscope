from __future__ import annotations

from softscope.models import SoftwareRecord


def filter_records(records: list[SoftwareRecord], query: str) -> list[SoftwareRecord]:
    terms = [term.casefold() for term in query.split() if term.strip()]
    if not terms:
        return records

    return [record for record in records if _matches_all_terms(record, terms)]


def _matches_all_terms(record: SoftwareRecord, terms: list[str]) -> bool:
    searchable = " ".join(
        (
            record.name,
            record.version,
            record.publisher,
            record.install_location,
            record.source,
        )
    ).casefold()
    return all(term in searchable for term in terms)
