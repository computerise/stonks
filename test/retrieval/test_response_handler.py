"""Test response handler."""

from unittest import TestCase
from unittest.mock import patch, MagicMock
from requests.models import Response

from stonks.retrieval.response_handler import handle_response


class TestResponseHandler(TestCase):
    def build_mock_response(self, url, ok, status_code, json_value):
        """Build a mock Response object."""
        response = Response
        response.url = url
        response.ok = ok
        response.status_code = status_code
        response.json = lambda: json_value
        return response

    @patch("json.dump", MagicMock(return_value={"mock_json"}))
    def test_handle_good_response(self):
        """Test handling of 200 OK response."""
        response = self.build_mock_response("mock_url", True, 200, {"mock": "json"})
        handle_response("mock_output", response)
        self.assertTrue(response.ok)

    def test_handle_bad_response(self):
        """Test handling of a 404 bad response."""
        response = self.build_mock_response("mock_url", False, 404, {"mock": "json"})
        with self.assertRaises(ValueError):
            handle_response("mock_output", response)
