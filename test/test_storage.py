"""Test data storage."""

from sys import stdout, __stdout__
from io import StringIO
from unittest import TestCase

from stonks.storage import DataStorage


class TestDataStorage(TestCase):
    invalid_path: str = "/invalid/file/path"

    def test_read_json(self):
        with self.assertRaises(ValueError):
            DataStorage.read_json(self.invalid_path)

    def test_write_json(self):
        # Test with invalid path and valid data
        with self.assertRaises(ValueError):
            DataStorage.write_json(self.invalid_path, "mock_data")

        # Test with invalid path and invalid data
        with self.assertRaises(ValueError):
            DataStorage.write_json(self.invalid_path, ("tuple_data",))
