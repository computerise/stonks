"""Handle data storage."""
import logging
from pathlib import Path
from json import load, dump
from typing import Any
from datetime import datetime

from stonks.error_handler import raise_fatal_error


class DataStorage:
    """Utility class for writing and reading data from the local file system."""

    @staticmethod
    def formatted_time_now() -> str:
        """Compute a nicely formatted timestamp string."""
        return str(datetime.now().isoformat())[:-7]

    @staticmethod
    def timestamped_file(name: str, suffix: str) -> Path:
        """Compute a file name based on the current time."""
        return Path(f"{name}_{DataStorage.formatted_time_now()}").with_suffix(suffix)

    def get_json(directory_path: Path, file_name: str) -> dict[str, Any]:
        """Get JSON data from a file within the directory path, where the `file_name` can also just be the ticker."""
        file_path = Path(directory_path, file_name).with_suffix(".json")
        return DataStorage.read_json(file_path)

    def read_json(path: Path) -> dict[str, Any]:
        """Load a JSON file as a dictionary."""
        try:
            with open(path, "r") as file:
                return load(file)
        except FileNotFoundError:
            logging.warning(f"JSON file at '{path}' could not be found.")

    def write_json(path: Path, data: dict[str, Any]) -> None:
        """Write valid JSON data to a JSON file."""
        if type(data) not in (dict, list, str, int, float, bool) or data is None:
            raise_fatal_error("Data to be written is not valid JSON.")
        try:
            with open(path, "w") as file:
                dump(data, file, indent=4)
        except FileNotFoundError as exc:
            raise_fatal_error(
                f"Could not write JSON file to '{path}'.",
                from_exception=exc,
            )
