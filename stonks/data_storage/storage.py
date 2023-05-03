"""Handle data storage."""
from json import load, dump


class DataStorage:
    """Utility class for writing and reading data from the local file system."""

    def read_json(path: str) -> dict:
        """Loads a JSON file as a dictionary."""
        try:
            with open(path, "r") as file:
                return load(file)
        except FileNotFoundError as exc:
            raise ValueError(f"JSON file at '{path}' could not be found.") from exc

    def write_json(path: str, data: dict) -> None:
        """Writes valid JSON data to a JSON file."""
        if type(data) not in (dict, list, str, int, float, bool) or data is None:
            raise ValueError("Data to be written is not valid JSON.")
        try:
            with open(path, "w") as file:
                dump(data, file, indent=4)
        except FileNotFoundError as exc:
            raise ValueError(f"Could not write JSON file to '{path}'.") from exc
