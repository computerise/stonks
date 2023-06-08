"""Test data storage."""

from unittest import TestCase

from stonks.storage import DataStorage


class TestDataStorage(TestCase):
    """Test data storage."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up Data Storage test class."""
        cls.invalid_path: str = "/invalid/file/path"

    def test_read_json(self) -> None:
        """Test that an invalid path raises a ValueError."""
        with self.assertRaises(ValueError):
            DataStorage.read_json(self.invalid_path)

    def test_write_json(self) -> None:
        """Test that invalid path and valid data, and invalid path and invalid data raise ValueError."""
        with self.assertRaises(ValueError):
            DataStorage.write_json(self.invalid_path, "mock_data")
        with self.assertRaises(ValueError):
            DataStorage.write_json(self.invalid_path, ("tuple_data",))
