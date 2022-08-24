from my_module.libs.rules import rules


def test_rules() -> None:
    """Just asserts True."""
    assert rules.create_rules() is True


def test_all_rules() -> None:
    """Just asserts True."""
    assert rules.create_rules() is True
