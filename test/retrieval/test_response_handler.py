"""Test response handler."""

from unittest import TestCase
from requests.models import Response

from stonks.retrieval.response_handler import handle_response


class TestResponseHandler(TestCase):
    def build_mock_response(self, url, ok, status_code, json_value):
        response = Response
        response.url = url
        response.ok = ok
        response.status_code = status_code
        response.json = lambda: json_value
        return response

    def test_handle_bad_response(self):
        response = self.build_mock_response("mock_url", False, 404, {"mock": "json"})
        with self.assertRaises(ValueError):
            handle_response("mock_output", response)
