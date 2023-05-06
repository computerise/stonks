"""Handle data storage."""
from pathlib import Path
from json import load, dump

from stonks.error_handler import raise_error


class DataStorage:
    """Utility class for writing and reading data from the local file system."""

    def read_json(path: Path) -> dict:
        """Load a JSON file as a dictionary."""
        try:
            with open(path, "r") as file:
                return load(file)
        except FileNotFoundError as exc:
            raise_error(
                f"JSON file at '{path}' could not be found.", from_exception=exc
            )

    def write_json(path: Path, data: dict) -> None:
        """Write valid JSON data to a JSON file."""
        if type(data) not in (dict, list, str, int, float, bool) or data is None:
            raise_error("Data to be written is not valid JSON.")
        try:
            with open(path, "w") as file:
                dump(data, file, indent=4)
        except FileNotFoundError as exc:
            raise_error(f"Could not write JSON file to '{path}'.", from_exception=exc)
