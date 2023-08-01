"""Test API Client."""

import responses
from unittest import TestCase

from stonks.retrieval.api_client import APIClient


class TestAPIClient(TestCase):
    """Test API Client."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up API Client test class."""

        class MockAPIKeys:
            def __init__(self):
                self.rapidapi_key = "mock_key"

        cls.api_client = APIClient(MockAPIKeys())

    def test_instantiation(self):
        """Test class instantiation."""
        self.assertTrue(isinstance(self.api_client, APIClient))

    @responses.activate
    def test_retrieve(self) -> None:
        """Test method to retrieve company data."""
        body = {
            "method": responses.GET,
            "url": "https://yahoo-finance15.p.rapidapi.com/api/yahoo/mo/module/MOCK?module=asset-profile%2Cincome-statement",
            "body": '{"error": "reason"}',
            "status": 404,
            "adding_headers": {"mock_header": "mock_value"},
        }
        responses.add(**body)
        response = self.api_client.retrieve("MOCK", ("asset-profile", "income-statement"))
        self.assertEqual({"error": "reason"}, response.json())
        self.assertEqual(404, response.status_code)
