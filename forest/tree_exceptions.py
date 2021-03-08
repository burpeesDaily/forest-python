# Copyright © 2021 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Tree Exception Definitions."""


class DuplicateKeyError(Exception):
    """Raised when a key already exists."""

    def __init__(self, key: str) -> None:
        Exception.__init__(self, f"{key} already exists.")
