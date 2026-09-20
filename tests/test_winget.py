from softscope.winget import _parse_winget_upgrade_output


def test_parse_winget_upgrade_output() -> None:
    output = """
Name                 Id                    Version      Available    Source
---------------------------------------------------------------------------
Git                  Git.Git               2.45.0       2.46.0       winget
Visual Studio Code   Microsoft.Visual...   1.91.0       1.92.2       winget
"""

    updates = _parse_winget_upgrade_output(output)

    assert updates["git"] == "2.46.0"
    assert updates["visual studio code"] == "1.92.2"
