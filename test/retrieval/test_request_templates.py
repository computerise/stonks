"""Test request templates."""

from unittest import TestCase

from stonks.retrieval.request_templates import RapidAPIRequest, YahooFinanceRequest


class TestRapidAPIRequest(TestCase):
    """Test RapidAPI Request class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up RapidAPIRequest test class."""
        cls.x_rapidapi_key = "mock_x_rapidapi_key"
        cls.rapidapi_request = RapidAPIRequest(x_rapidapi_key=cls.x_rapidapi_key)

    def test_instantiation(self) -> None:
        """Test class instantiation."""
        self.assertTrue(isinstance(self.rapidapi_request, RapidAPIRequest))

    def test_set_headers(self) -> None:
        """Test method to set headers."""
        self.assertEqual(
            self.rapidapi_request.headers,
            {
                "X-RapidAPI-Key": self.x_rapidapi_key,
            },
        )


class TestYahooFinanceRequest(TestCase):
    """Test YahooFinance Request."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialise Yahoo Finance request test."""
        super(TestYahooFinanceRequest, self).__init__(*args, **kwargs)
        self.yahoo_finance_request = YahooFinanceRequest("MOCK", x_rapidapi_key="mock_key")
        self.default_query_parameters = (
            "financial-data",
            "income-statement",
            "balance-sheet",
            "cashflow-statement",
            "default-key-statistics",
        )
        self.params = {"module": "financial-data,income-statement,balance-sheet,cashflow-statement,default-key-statistics"}

    def test_instantiation(self) -> None:
        """Test class instantiation."""
        self.assertTrue(isinstance(self.yahoo_finance_request, YahooFinanceRequest))

    def test_set_url(self) -> None:
        """Test method to set URL."""
        self.assertEqual(
            self.yahoo_finance_request.url,
            "https://yahoo-finance15.p.rapidapi.com/api/yahoo/mo/module/MOCK",
        )

    def test_set_params(self) -> None:
        """Test method to set query parameters."""
        self.assertEqual(self.yahoo_finance_request.params, self.params)
        with self.assertRaises(TypeError):
            self.yahoo_finance_request.set_params(query_parameters="not_a_tuple")

    def test_format_queries(self) -> None:
        """Test correct formatting and too many query parameters."""
        self.assertEqual(
            self.yahoo_finance_request.format_queries(self.default_query_parameters),
            self.params,
        )
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

    def test_valid_query_parameters(self) -> None:
        """Test valid and invalid query parameters."""
        self.assertTrue(self.yahoo_finance_request.valid_query_parameters(("cashflow-statement", "sec-filings", "balance-sheet")))
        with self.assertRaises(ValueError):
            self.yahoo_finance_request.valid_query_parameters(("bad_parameter",))
