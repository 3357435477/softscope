from softscope.models import SoftwareRecord


def test_software_record_serializes_to_dict() -> None:
    record = SoftwareRecord(name="Example App", version="1.2.3", publisher="Example Inc.")

    assert record.as_dict()["name"] == "Example App"
    assert record.as_dict()["version"] == "1.2.3"
