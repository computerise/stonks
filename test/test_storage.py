"""Test data storage."""

from unittest import TestCase
from pathlib import Path

from stonks.storage import LocalDataStorage
from stonks.companies import CompanyCollection


class TestLocalDataStorage(TestCase):
    """Test data storage."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up Data Storage test class."""
        cls.invalid_path: str = "/invalid/file/path"

    def test_write_json(self) -> None:
        """Test that invalid path and valid data, and invalid path and invalid data raise ValueError."""
        with self.assertRaises(ValueError):
            LocalDataStorage.write_json(self.invalid_path, "mock_data")
        with self.assertRaises(ValueError):
            LocalDataStorage.write_json(self.invalid_path, ("tuple_data",))

    def test_create_company_collection_from_local(self) -> None:
        """Test creation of CompanyCollection from local data."""
        company_collection = LocalDataStorage.create_company_collection_from_local(Path("input/s&p500.json"))
        self.assertIsInstance(company_collection, CompanyCollection)
