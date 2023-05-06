"""Configures the application."""

import logging
from os import makedirs
from pathlib import Path
from tomllib import load
from datetime import datetime
from dataclasses import dataclass

from stonks.error_handler import raise_fatal_error

CREATED_DIRECTORY_MESSAGE = "Created directory at "


def create_directory(directory_path: Path) -> bool:
    """Create a directory if it does not already exist."""
    if not directory_path.exists():
        try:
            makedirs(directory_path)
            return True
        except FileNotFoundError:
            raise_fatal_error(
                message=f"Failed to create directory at `{directory_path}`.",
                from_exception=FileNotFoundError,
            )
    return False


def configure_logging(level: str, log_directory: Path) -> None:
    """Configure log level and log file name."""
    created_directory = create_directory(log_directory)
    # Save to `logs` directory, ISO format to remove space, remove colons, remove microseconds.
    log_path = Path(
        log_directory, f"{str(datetime.now().isoformat()).replace(':','-')[:-7]}.log"
    )
    logging.basicConfig(
        filename=log_path,
        encoding="utf-8",
        level=logging.getLevelName(level),
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)-8s %(message)s",
    )
    if created_directory:
        logging.info(f"{CREATED_DIRECTORY_MESSAGE}`{log_directory}`.")


@dataclass
class APIKeys:
    """Data class for storing API Access Keys."""

    rapidapi_key: str


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
        self.log_directory = Path(self.log_directory)
        self.input_directory = Path(self.input_directory)
        self.storage_directory = Path(self.storage_directory)
        self.configure_application()

    def configure_application(self) -> None:
        configure_logging(level=self.log_level, log_directory=self.log_directory)
        if create_directory(Path(self.input_directory)):
            logging.info(f"{CREATED_DIRECTORY_MESSAGE}`{self.input_directory}`.")
        if create_directory(Path(self.storage_directory)):
            logging.info(f"{CREATED_DIRECTORY_MESSAGE}`{self.storage_directory}`.")


class MetricAssumptions(TOMLConfiguration):
    """All assumptions of metrics used to processing."""

    def __init__(self, path: str = "assumptions.toml") -> None:
        self.__dict__ = self.load_config(path)
