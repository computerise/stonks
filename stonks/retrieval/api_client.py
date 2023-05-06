"""API Client."""

import logging
from requests import Session, Response

from stonks.configuration import APIKeys
from stonks.retrieval.request_builder import Request, YahooFinanceRequest


class APIClient:
    """API client used for sending requests."""

    def __init__(self, api_keys: APIKeys) -> None:
        """Initialise class instance."""
        logging.info("Created API Client.")
        self.start_session(api_keys)

    def start_session(self, keys: APIKeys) -> None:
        self.session = Session()
        self.session.api_keys = keys
        logging.info("Started Session.")

    def retrieve(
        self,
        ticker: str,
        queries: tuple[str] = None,
        request_type: Request = YahooFinanceRequest,
    ) -> Response:
        """Retrieve data from a stock ticker, using default queries if none are specified."""
        prepared_request = request_type(
            ticker_symbol=ticker,
            query_parameters=queries,
            x_rapidapi_key=self.session.api_keys.rapidapi_key,
        ).prepare()
        return self.session.send(prepared_request)
