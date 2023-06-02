"""Configures the application."""

import logging
from os import makedirs
from sys import stdout
from pathlib import Path
from tomllib import load
from datetime import datetime
from dataclasses import dataclass
from typing import Any

from stonks.error_handler import raise_fatal_error

SUCCESS_CREATE_DIRECTORY_MESSAGE = "Created directory at "
FAIL_CREATE_DIRECTORY_MESSAGE = "Failed to create directory at "


def create_directory(directory_path: Path) -> bool:
    """Create a directory if it does not already exist."""
    if not directory_path.exists():
        try:
            makedirs(directory_path)
            return True
        except FileNotFoundError:
            raise_fatal_error(
                message=f"{FAIL_CREATE_DIRECTORY_MESSAGE}`{directory_path}`.",
                from_exception=FileNotFoundError,
            )
    return False


def configure_logging(level: str, log_directory: Path) -> None:
    """Configure log level and log file name."""
    created_directory = create_directory(log_directory)
    # Save to `logs` directory, ISO format to remove space, remove colons, remove microseconds.
    log_path = Path(log_directory, f"{str(datetime.now().isoformat()).replace(':','-')[:-7]}.log")
    file_handler = logging.FileHandler(log_path)
    stdout_handler = logging.StreamHandler(stdout)
    logging.basicConfig(
        encoding="utf-8",
        level=logging.getLevelName(level),
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)-8s %(message)s",
        handlers=(file_handler, stdout_handler),
    )
    if created_directory:
        logging.info(f"{SUCCESS_CREATE_DIRECTORY_MESSAGE}`{log_directory}`.")


class TOMLConfiguration:
    """Base class for all TOML configuration objects."""

    def load_config(self, path) -> dict[str, Any]:
        """Load a TOML file."""
        with open(path, "rb") as file:
            return load(file)


class ApplicationSettings(TOMLConfiguration):
    """All settings associated with the operation of the application."""

    def __init__(self, path: str = "settings.toml") -> None:
        """Initialise class instance."""
        self.__dict__ = self.load_config(path).get("application")
        self.log_directory = Path(self.log_directory)
        self.input_directory = Path(self.input_directory)
        self.storage_directory = Path(self.storage_directory)
        self.configure_application()

    def configure_application(self) -> None:
        """Configure the application."""
        configure_logging(level=self.log_level, log_directory=self.log_directory)
        self.set_api_keys()
        if create_directory(Path(self.input_directory)):
            logging.info(f"{SUCCESS_CREATE_DIRECTORY_MESSAGE}`{self.input_directory}`.")
        if create_directory(Path(self.storage_directory)):
            logging.info(f"{SUCCESS_CREATE_DIRECTORY_MESSAGE}`{self.storage_directory}`.")

    def set_api_keys(self) -> None:
        self.api_keys = {}
        for api_key in self.api_key_names:
            try:
                self.api_keys[api_key] = config(api_key)
            except Exception as exc:
                print(exc)


class MetricAssumptions(TOMLConfiguration):
    """All assumptions of metrics used to processing."""

    def __init__(self, path: str = "assumptions.toml") -> None:
        """Initialise class instance."""
        self.__dict__ = self.load_config(path)
