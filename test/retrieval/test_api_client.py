"""Test api_client.py."""

import responses
from unittest import TestCase

from stonks.retrieval.api_client import APIClient
from stonks.retrieval.request_builder import Request


class TestAPIClient(TestCase):
    """Test API Client."""

    def __init__(self, *args, **kwargs):
        super(TestAPIClient, self).__init__(*args, **kwargs)
        self.api_client = APIClient()

        # Mock request
        self.request = Request("http://example.com/api/123", "application/json")
        self.request.url = self.request.base_url
        self.request.headers = {"mock_header": "mock_value"}
        self.request.query_string = {"module": "query,string"}

    def test_instantiation(self):
        self.assertTrue(isinstance(self.api_client, APIClient))

    @responses.activate
    def test_get(self):
        responses.add(
            **{
                "method": responses.GET,
                "url": self.request.url,
                "body": '{"error": "reason"}',
                "status": 404,
                "content_type": self.request.content_type,
                "adding_headers": self.request.headers,
            }
        )
        response = self.api_client.get(self.request)
        self.assertEqual({"error": "reason"}, response.json())
        self.assertEqual(404, response.status_code)
