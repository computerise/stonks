"""API Clients."""

import requests
import logging

from stonks.retrieval.request_builder import Request, YahooFinanceRequest


class APIClient:
    """API client used for sending requests."""

    def __init__(self):
        """Initialise class instance."""
        logging.info("Created API Client.")

    def get(self, request: Request):
        """Get the specified request and return the response as a JSON object."""
        return requests.get(
            request.url, headers=request.headers, params=request.query_string
        )

    def retrieve(self, ticker: str, queries: tuple[str] = None):
        """Retrieve data from a stock ticker, using default queries if none are specified."""
        if queries:
            yf_request = YahooFinanceRequest(
                ticker_symbol=ticker, query_parameters=queries
            )
        else:
            yf_request = YahooFinanceRequest(ticker_symbol=ticker)
        return self.get(yf_request)
