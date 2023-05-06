"""API Client."""

from requests import Session, Response
import logging

from stonks.retrieval.request_builder import Request, YahooFinanceRequest


class APIClient:
    """API client used for sending requests."""

    def __init__(self) -> None:
        """Initialise class instance."""
        logging.info("Created API Client.")
        self.start_session()

    def start_session(self) -> None:
        self.session = Session()
        logging.info("Started Session.")

    def retrieve(
        self,
        ticker: str,
        queries: tuple[str] = None,
        request_type: Request = YahooFinanceRequest,
    ) -> Response:
        """Retrieve data from a stock ticker, using default queries if none are specified."""
        prepared_request = request_type(
            ticker_symbol=ticker, query_parameters=queries
        ).prepare()
        return self.session.send(prepared_request)
