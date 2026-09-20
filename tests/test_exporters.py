from softscope.exporters import format_table
from softscope.models import SoftwareRecord


def test_format_table_contains_records() -> None:
    table = format_table(
        [
            SoftwareRecord(
                name="Example Application",
                version="1.0.0",
                publisher="Example Publisher",
                update_available=True,
                latest_version="1.1.0",
            )
        ]
    )

    assert "Example Application" in table
    assert "available (1.1.0)" in table


def test_format_table_handles_empty_records() -> None:
    assert format_table([]) == "No installed software records were found."
