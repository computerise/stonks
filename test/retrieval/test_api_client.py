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

    def test_instantiation(self):
        self.assertTrue(isinstance(self.api_client, APIClient))

    @responses.activate
    def test_get(self):
        request = Request("http://example.com/api/123", "application/json")
        request.url = request.base_url
        request.headers = {"X-Foo": "Bar"}
        request.query_string = {"module": "query,string"}
        responses.add(
            **{
                "method": responses.GET,
                "url": request.url,
                "body": '{"error": "reason"}',
                "status": 404,
                "content_type": request.content_type,
                "adding_headers": request.headers,
            }
        )
        response = self.api_client.get(request)
        self.assertEqual({"error": "reason"}, response.json())
        self.assertEqual(404, response.status_code)
