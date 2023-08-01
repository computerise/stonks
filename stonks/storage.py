"""Handle data storage."""
import logging
from pathlib import Path
from json import load, dump
from typing import Any
from datetime import datetime
from urllib.parse import urlparse

from sqlalchemy import create_engine
from sqlalchemy.engine import URL, Engine, Connection
from sqlalchemy.orm import sessionmaker


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
    def create_company_collection_from_local(input_file_path: Path) -> CompanyCollection:
        """Create CompanyCollection from local data."""
        raw_companies_list = LocalDataStorage.read_json(input_file_path)
        # Standardise input files with schema.
        index = input_file_path.stem
        try:
            companies = [
                Company(ticker=key, name=raw_companies_list[key]["security"], country="usa", index=index)
                for key in raw_companies_list
            ]
        except KeyError:
            companies = [
                Company(ticker=key, name=raw_companies_list[key]["name"], country="uk", index=index)
                for key in raw_companies_list
            ]
        return CompanyCollection(input_file_path.stem, companies)


class PostgreSQLDatabase:
    """Database model for PostgreSQL."""

    def __init__(self, name: str, url_names: str) -> None:
        """Initialise PostgreSQLDatabase."""
        self.name = name
        self.engine = self.build_engine(url_names)

    def build_engine(self, url: str) -> Engine:
        """Connect to the database URL using SQLAlchemy."""
        logging.info("Building database engine...")
        parsed = urlparse(url)
        database_url = URL.create(
            drivername="postgresql",
            username=parsed.username,
            password=parsed.password,
            host=parsed.hostname,
            port=parsed.port,
            database=parsed.path[1:],
        )
        engine = create_engine(database_url, echo=True)
        logging.info("Built database engine.")
        return engine

    def connect(self) -> Connection:
        """Connect to the database via SQLAlchemy engine."""
        return self.engine.connect()

    def session(self):
        """Connect to the database via SQLAlchemy engine."""
        return sessionmaker(bind=self.engine)()

    def upload_company_collection(self, company_collection: CompanyCollection) -> None:
        """Upload a CompanyCollection object to the database."""
        session = self.session()
        session.add_all(company_collection.companies)
        session.commit()
