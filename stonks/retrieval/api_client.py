"""API Client."""

import logging
from requests import Session, Response

from stonks.configuration import APIKeys
from stonks.retrieval.request_factory import RequestFactory, YahooFinanceRequestFactory


class APIClient:
    """API client used for sending requests."""

    def __init__(self, api_keys: APIKeys, request_factory_type: RequestFactory = YahooFinanceRequestFactory) -> None:
        """Initialise class instance."""
        logging.info("Creating API Client...")
        self.api_keys = api_keys
        self.request_factory = request_factory_type(self.api_keys.rapidapi_key)
        self.start_session()
        logging.info("Created API Client.")

    def start_session(self) -> None:
        logging.info("Starting Session...")
        self.session = Session()
        logging.info("Started Session.")

    def retrieve(
        self,
        ticker: str,
        queries: tuple[str] = None,
    ) -> Response:
        """Retrieve data from a stock ticker, using default queries if none are specified."""
        prepared_request = self.request_factory.construct_request(ticker_symbol=ticker, query_parameters=queries)
        return self.session.send(prepared_request)
