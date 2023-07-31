"""Test data storage."""

from unittest import TestCase

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
        """Test creation of CompanyCollections from local data."""
        company_collection = LocalDataStorage.create_company_collection_from_local(
            "input/s&p500.json", "S&P500", "Standard and Poor's 500"
        )
        self.assertIsInstance(company_collection, CompanyCollection)
