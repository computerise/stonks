from unittest import TestCase

from stonks.retrieval.request_builder import RapidAPIRequest


class TestRapidAPIRequest(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRapidAPIRequest, self).__init__(*args, **kwargs)
        self.rapid_api_request = RapidAPIRequest(base_url="mock_url")
        self.rapid_api_request.x_rapidapi_key = "mock_key"

    def test_instantiation(self):
        self.assertTrue(isinstance(self.rapid_api_request, RapidAPIRequest))

    def test_headers(self):
        self.assertEqual(
            self.rapid_api_request.headers,
            {
                "content-type": self.rapid_api_request.content_type,
                "X-RapidAPI-Key": self.rapid_api_request.x_rapidapi_key,
                "X-RapidAPI-Host": self.rapid_api_request.x_rapidapi_host,
            },
        )

    def test_valid_query_parameters(self):
        # Test valid parameters.
        self.assertTrue(
            self.rapid_api_request.valid_query_parameters(
                ("cashflow-statement", "sec-filings", "balance-sheet")
            )
        )
        # Test invalid parameters.
        with self.assertRaises(ValueError):
            self.rapid_api_request.valid_query_parameters(("bad_parameter",))
