from softscope.filters import filter_records
from softscope.models import SoftwareRecord


def test_filter_records_matches_name_and_publisher() -> None:
    records = [
        SoftwareRecord(name="Visual Studio Code", publisher="Microsoft Corporation"),
        SoftwareRecord(name="Python", publisher="Python Software Foundation"),
    ]

    assert filter_records(records, "microsoft") == [records[0]]
    assert filter_records(records, "python") == [records[1]]


def test_filter_records_requires_all_terms() -> None:
    records = [
        SoftwareRecord(name="Visual Studio Code", publisher="Microsoft Corporation"),
        SoftwareRecord(name="Visual Studio Build Tools", publisher="Microsoft Corporation"),
        SoftwareRecord(name="Visual Studio Code", publisher="Community Build"),
    ]

    assert filter_records(records, "microsoft code") == [records[0]]


def test_filter_records_keeps_all_records_for_blank_query() -> None:
    records = [SoftwareRecord(name="Example App")]

    assert filter_records(records, "   ") == records
