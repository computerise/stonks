"""Test response handler."""

from unittest import TestCase
from requests.models import Response

from stonks.retrieval.response_handler import handle_response


class TestResponseHandler(TestCase):
    def build_mock_response(self, url: str, ok: bool, status_code: int, json_value: dict) -> Response:
        """Build a mock Response object."""
        response = Response
        response.url = url
        response.ok = ok
        response.status_code = status_code
        response.json = lambda: json_value
        return response

    def test_handle_bad_response(self) -> None:
        """Test handling of a 404 bad response."""
        response = self.build_mock_response("mock_url", False, 404, {"mock": "json"})
        with self.assertRaises(ValueError):
            handle_response("mock_output", response)
