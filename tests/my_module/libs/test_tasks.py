from my_module.libs.tasks import tasks


def test_tasks() -> None:
    """Just asserts True."""
    assert tasks.create_tasks() is True


def test_all_tasks() -> None:
    """Just asserts True."""
    assert tasks.create_tasks() is True
