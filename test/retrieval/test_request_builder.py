from unittest import TestCase

from stonks.retrieval.request_builder import RapidAPIRequest, YahooFinanceRequest


class TestRapidAPIRequest(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRapidAPIRequest, self).__init__(*args, **kwargs)
        self.content_type = "mock_content_type"
        self.x_rapidapi_key = "mock_x_rapidapi_key"
        self.x_rapidapi_host = "mock_x_rapidapi_host"
        self.rapidapi_request = RapidAPIRequest(
            ticker_symbol="MOCK",
            content_type=self.content_type,
            x_rapidapi_key=self.x_rapidapi_key,
            x_rapidapi_host=self.x_rapidapi_host,
        )

    def test_instantiation(self):
        self.assertTrue(isinstance(self.rapidapi_request, RapidAPIRequest))

    def test_set_headers(self):
        self.assertEqual(
            self.rapidapi_request.headers,
            {
                "content-type": self.content_type,
                "X-RapidAPI-Key": self.x_rapidapi_key,
                "X-RapidAPI-Host": self.x_rapidapi_host,
            },
        )


class TestYahooFinanceRequest(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestYahooFinanceRequest, self).__init__(*args, **kwargs)
        self.yahoo_finance_request = YahooFinanceRequest("MOCK")
        self.default_query_parameters = (
            "asset-profile",
            "income-statement",
            "balance-sheet",
            "cashflow-statement",
            "default-key-statistics",
        )
        self.params = {
            "module": "asset-profile,income-statement,balance-sheet,cashflow-statement,default-key-statistics"
        }

    def test_instantiation(self):
        self.assertTrue(isinstance(self.yahoo_finance_request, YahooFinanceRequest))

    def test_set_url(self):
        self.assertEqual(
            self.yahoo_finance_request.url,
            "https://yahoo-finance15.p.rapidapi.com/api/yahoo/mo/module/MOCK",
        )

    def test_set_params(self):
        self.assertEqual(self.yahoo_finance_request.params, self.params)
        with self.assertRaises(TypeError):
            self.yahoo_finance_request.set_params(query_parameters="not_a_tuple")

    def test_format_queries(self):
        # Test correct formatting.

        self.assertEqual(
            self.yahoo_finance_request.format_queries(self.default_query_parameters),
            self.params,
        )
        # Test too many parameters.
        with self.assertRaises(ValueError):
            self.yahoo_finance_request.format_queries(
                (
                    "asset-profile",
                    "income-statement",
                    "balance-sheet",
                    "cashflow-statement",
                    "default-key-statistics",
                    "calendar-events",
                )
            )

    def test_valid_query_parameters(self):
        # Test valid parameters.
        self.assertTrue(
            self.yahoo_finance_request.valid_query_parameters(
                ("cashflow-statement", "sec-filings", "balance-sheet")
            )
        )
        # Test invalid parameters.
        with self.assertRaises(ValueError):
            self.yahoo_finance_request.valid_query_parameters(("bad_parameter",))
