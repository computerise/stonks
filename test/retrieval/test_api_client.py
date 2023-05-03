"""Test api_client.py."""

from unittest import TestCase
from stonks.retrieval.api_client import APIClient


class TestAPIClient(TestCase):
    """Test API Client."""

    def test_instantiation(self):
        api_client = APIClient()
        self.assertTrue(isinstance(api_client, APIClient))
