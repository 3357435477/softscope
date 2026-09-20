from softscope.collectors import _format_install_date


def test_format_install_date_converts_registry_date() -> None:
    assert _format_install_date("20260920") == "2026-09-20"


def test_format_install_date_leaves_unknown_value() -> None:
    assert _format_install_date("not-a-date") == "not-a-date"
