"""Configures the application."""

import logging
from os import makedirs
from sys import stdout
from decouple import config, UndefinedValueError
from pathlib import Path
from tomllib import load
from typing import Any

from stonks.storage import DataStorage
from stonks.error_handler import raise_fatal_error
from stonks.command_line_interface import CommandLineInterface

SUCCESS_CREATE_DIRECTORY_MESSAGE = "Created directory at "
FAIL_CREATE_DIRECTORY_MESSAGE = "Failed to create directory at "


def create_directory(directory_path: Path) -> bool:
    """Create a directory if it does not already exist."""
    if not directory_path.exists():
        try:
            makedirs(directory_path)
            logging.info(f"{SUCCESS_CREATE_DIRECTORY_MESSAGE}`{directory_path}`.")
            return True
        except FileNotFoundError:
            raise_fatal_error(
                message=f"{FAIL_CREATE_DIRECTORY_MESSAGE}`{directory_path}`.",
                from_exception=FileNotFoundError,
            )
    return False


def configure_logging(level: str, log_directory: Path, date_format: str) -> None:
    """Configure log level and log file name."""
    created_directory = create_directory(log_directory)
    # Save to log directory, ISO format to remove space, remove colons, remove microseconds.
    log_path = Path(log_directory, DataStorage.timestamped_file("stonks", ".log"))
    file_handler = logging.FileHandler(log_path)
    stdout_handler = logging.StreamHandler(stdout)
    logging.basicConfig(
        encoding="utf-8",
        level=logging.getLevelName(level),
        datefmt=date_format,
        format="%(asctime)s %(levelname)-8s %(message)s",
        handlers=(file_handler, stdout_handler),
    )
    if created_directory:
        logging.info(f"{SUCCESS_CREATE_DIRECTORY_MESSAGE}`{log_directory}`.")


class APIKeys:
    def __init__(self, api_key_names: list[str]) -> None:
        self._set_api_keys(api_key_names)

    def _set_api_keys(self, api_key_names: list[str]) -> None:
        """Set API Keys from environment variables, named in settings.toml."""
        logging.info("Loading API Keys...")
        api_keys = {}
        for name in api_key_names:
            try:
                api_keys[name] = config(name)
            except UndefinedValueError as exc:
                raise_fatal_error(
                    f"Environment variable `{name}` is not set. Declare it in a `.env` file as described in `README.md`",
                    from_exception=exc,
                )
        self.__dict__ = api_keys
        logging.info("Loaded API Keys.")


class TOMLConfiguration:
    """Base class for all TOML configuration objects."""

    def load_config(self, path) -> dict[str, Any]:
        """Load a TOML file."""
        with open(path, "rb") as file:
            return load(file)


class ApplicationSettings(TOMLConfiguration):
    """All settings associated with the operation of the application."""

    def __init__(self, settings_path: str) -> None:
        """Initialise class instance."""
        settings = self.load_config(settings_path).get("application")
        for key, value in settings.items():
            if key in ("input_file", "log_directory", "storage_directory", "output_directory"):
                settings[key] = Path(value)
        self.__dict__.update(settings)
        self.__dict__.update(self.load_config("pyproject.toml").get("tool").get("poetry"))
        self.date_format = "%Y-%m-%dT%H:%M:%S"

    def configure_application(self) -> None:
        """Configure the application."""
        CommandLineInterface.outro_duration_seconds = self.outro_duration_seconds
        configure_logging(level=self.log_level, log_directory=self.log_directory, date_format=self.date_format)
        create_directory(Path(self.storage_directory))
        create_directory(Path(self.output_directory))


class MetricAssumptions(TOMLConfiguration):
    """All assumptions of metrics used to processing."""

    def __init__(self, assumptions_path: str) -> None:
        """Initialise class instance."""
        self.__dict__ = self.load_config(assumptions_path)
