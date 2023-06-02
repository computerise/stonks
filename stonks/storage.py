"""Handle data storage."""
from pathlib import Path
from json import load, dump
from typing import Any

from stonks.error_handler import raise_fatal_error


class DataStorage:
    """Utility class for writing and reading data from the local file system."""

    def get_json(directory_path: Path, file_name: str) -> dict[str, Any]:
        """Get JSON data from a file within the directory path, where the `file_name` can also just be the ticker."""
        file_path = Path(directory_path, file_name)
        if not file_path.suffix == ".json":
            file_path = Path(f"{file_path}.json")
        return DataStorage.read_json(file_path)

    def read_json(path: Path) -> dict[str, Any]:
        """Load a JSON file as a dictionary."""
        try:
            with open(path, "r") as file:
                return load(file)
        except FileNotFoundError as exc:
            raise_fatal_error(
                f"JSON file at '{path}' could not be found.",
                from_exception=exc,
            )

    def write_json(path: Path, data: dict[str, Any]) -> None:
        """Write valid JSON data to a JSON file."""
        if (
            type(data) not in (dict[str, Any], list, str, int, float, bool)
            or data is None
        ):
            raise_fatal_error("Data to be written is not valid JSON.")
        try:
            with open(path, "w") as file:
                dump(data, file, indent=4)
        except FileNotFoundError as exc:
            raise_fatal_error(
                f"Could not write JSON file to '{path}'.",
                from_exception=exc,
            )
