import project_template


def test_version_is_exposed() -> None:
    assert project_template.__version__
