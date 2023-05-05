"""Configures the application."""

import logging
from os import makedirs
from os.path import isdir
from tomllib import load
from datetime import datetime


def configure_logging(level: str, log_directory: str) -> None:
    """Configure log level and log file name."""
    if not isdir(log_directory):
        makedirs("logs/")
    # Save to `logs` directory, ISO format to remove space, remove colons, remove microseconds.
    log_file = f"logs/{str(datetime.now().isoformat()).replace(':','-')[:-7]}.log"
    logging.basicConfig(
        filename=log_file, encoding="utf-8", level=logging.getLevelName(level)
    )


class TOMLConfiguration:
    """Base class for all TOML configuration objects."""

    def load_config(self, path) -> dict:
        """Load a TOML file."""
        with open(path, "rb") as file:
            return load(file)


class ApplicationSettings(TOMLConfiguration):
    """All settings associated with the operation of the application."""

    def __init__(self, path: str = "settings.toml") -> None:
        self.__dict__ = self.load_config(path).get("application")
        self.configure_application()

    def configure_application(self) -> None:
        configure_logging(level=self.log_level, log_directory=self.log_directory)


class MetricAssumptions(TOMLConfiguration):
    """All assumptions of metrics used to processing."""

    def __init__(self, path: str = "assumptions.toml") -> None:
        self.__dict__ = self.load_config(path)
