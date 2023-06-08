"""API Client."""

import logging
from requests import Session, Response

from stonks.retrieval.request_builder import Request, YahooFinanceRequest


class APIClient:
    """API client used for sending requests."""

    def __init__(self, api_keys: dict[str, str]) -> None:
        """Initialise class instance."""
        logging.info("Creating API Client...")
        self.api_keys = api_keys
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
        request_type: Request = YahooFinanceRequest,
    ) -> Response:
        """Retrieve data from a stock ticker, using default queries if none are specified."""
        # This should clearly not use RAPIDAPI_KEY exclusively. APIKeys should be passed to future factory methods.
        prepared_request = request_type(
            ticker_symbol=ticker,
            query_parameters=queries,
            x_rapidapi_key=self.api_keys.RAPIDAPI_KEY,
        ).prepare()
        return self.session.send(prepared_request)
