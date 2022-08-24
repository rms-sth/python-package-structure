"""
sample module that performs sample operations.
Contains:
    - SampleClass
"""


def create_rules(some_parameter: str | None = None) -> bool:  # noqa: D103
    """compute and parse rules for validation

    Args:
        some_parameter (str | None, optional): parameter for function. Defaults to None.

    Returns:
        bool: parsed rules.
    """
    return True


class SampleClass:
    """Documentation of the SampleClass."""

    def __init__(self) -> None:
        """Initializes samples class."""
        return

    @staticmethod
    def true() -> bool:
        """Return True my friend."""
        return True

    @classmethod
    def false(cls) -> bool:
        """
        Doc strings should not start with Returns...
        Nonetheless, returns False
        """
        return False
