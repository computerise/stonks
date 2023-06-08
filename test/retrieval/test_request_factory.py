"""Test request factories."""

from unittest import TestCase
from requests import PreparedRequest
from stonks.retrieval.request_factory import RapidAPIRequestFactory, YahooFinanceRequestFactory


class TestRapidAPIRequestFactory(TestCase):
    @classmethod
    def setUpClass(self):
        self.request_factory = RapidAPIRequestFactory("mock_key")

    def test_rapidapi_request_factory(self):
        self.assertIsInstance(self.request_factory.construct_request(), PreparedRequest)


class TestYahooFinanceRequestFactory(TestCase):
    @classmethod
    def setUpClass(self):
        self.request_factory = YahooFinanceRequestFactory("mock_key")

    def test_yahoo_finance_request_factory(self):
        self.assertIsInstance(self.request_factory.construct_request("MOCK"), PreparedRequest)
