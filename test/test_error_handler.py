"""Test error handler."""

from unittest import TestCase

from stonks.error_handler import raise_fatal_error


class TestErrorHandler(TestCase):
    """Test Error Handler."""

    def test_raise_default_error(self):
        """Test that ValueError is raised by default, from FileNotFoundError."""
        with self.assertRaises(ValueError):
            raise_fatal_error("mock_error", from_exception=FileNotFoundError)

    def test_raise_index_error(self):
        """Test that IndexError is raised when specifying the new exception."""
        with self.assertRaises(IndexError):
            raise_fatal_error("mock_error", new_exception=IndexError)
