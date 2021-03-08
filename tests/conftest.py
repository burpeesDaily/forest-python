"""Common test data for pytest."""

import pytest


@pytest.fixture
def basic_tree() -> list:
    """Return tree data for building a tree."""
    return [
        (23, "23"),
        (4, "4"),
        (30, "30"),
        (11, "11"),
        (7, "7"),
        (34, "34"),
        (20, "20"),
        (24, "24"),
        (22, "22"),
        (15, "15"),
        (1, "1")
    ]
