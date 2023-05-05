"""Handles errors."""

import logging
from typing import Callable


def raise_error(
    message: str,
    log_level: Callable = logging.critical,
    new_exception: Exception = ValueError,
    from_exception: Exception = None,
) -> None:
    """Log an error message and raise an exception."""
    log_level(message)
    if from_exception:
        raise new_exception(message) from from_exception
    else:
        raise new_exception(message)
