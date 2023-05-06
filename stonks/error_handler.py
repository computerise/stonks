"""Handles errors."""

import logging
from traceback import format_exc

from stonks.command_line_interface import CommandLineInterface


def raise_fatal_error(
    message: str,
    new_exception: Exception = ValueError,
    from_exception: Exception = None,
) -> None:
    """Log an error message and raise an exception."""
    logging.critical(format_exc())
    logging.critical(from_exception)
    logging.critical(message)

    CommandLineInterface.outro(
        f"Program execution cannot continue due to the fatal error:\n'{message}'"
    )
    logging.critical("Terminated application execution.")
    if from_exception:
        raise new_exception(message) from from_exception
    else:
        raise new_exception(message)
