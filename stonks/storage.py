"""Handle data storage."""
import logging
from pathlib import Path
from json import load, dump
from typing import Any
from datetime import datetime
from urllib.parse import urlparse

from psycopg2 import connect

from stonks.error_handler import raise_fatal_error
from stonks.companies import Company, CompanyCollection


class LocalDataStorage:
    """Utility class for writing and reading data from the local file system."""

    @staticmethod
    def formatted_time_now() -> str:
        """Compute a nicely formatted timestamp string."""
        return str(datetime.now().isoformat()).replace(":", "-")[:-7]

    @staticmethod
    def timestamped_file(name: str, suffix: str) -> Path:
        """Compute a file name based on the current time."""
        return Path(f"{name}_{LocalDataStorage.formatted_time_now()}").with_suffix(suffix)

    @staticmethod
    def get_json(directory_path: Path, file_name: str) -> dict[str, Any]:
        """Get JSON data from a file within the directory path, where the `file_name` can also just be the ticker."""
        file_path = Path(directory_path, file_name).with_suffix(".json")
        return LocalDataStorage.read_json(file_path)

    @staticmethod
    def read_json(path: Path) -> dict[str, Any]:
        """Load a JSON file as a dictionary."""
        try:
            with open(path, "r") as file:
                return load(file)
        except FileNotFoundError:
            logging.warning(f"JSON file at '{path}' could not be found.")

    @staticmethod
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

    @staticmethod
    def create_databases_from_local(self):
        """Create a new database from local data"""
        # Generate CompaniesCollection from local data.
        raw_companies_list = LocalDataStorage.read_json(self.settings.input_file)
        companies = []
        for key in raw_companies_list:
            companies.append(Company(ticker=key, name=raw_companies_list["name"]))
        company_collection = CompanyCollection("S&P500", "Standard and Poor's 500", companies)  # noqa
        cursor = self.database_connection.cursor()  # noqa
        # cursor.execute("CREATE DATABASE companies (ticker varchar(5), name varchar(255), index varchar(16));")

    @staticmethod
    def update_database_from_local(self):
        raise NotImplementedError


class PostgreSQLDataStorage:
    """Data storage for PostgreSQL."""

    def __init__(self, postgres_url: str) -> None:
        """Initialise PostgreSQLDataStorage."""
        self.url = postgres_url

    def connect(self, url: str) -> Any:
        """Connect to the database URL."""
        parsed = urlparse(url)
        return connect(
            database=parsed.path[1:], user=parsed.username, password=parsed.password, host=parsed.hostname, port=parsed.port
        )
