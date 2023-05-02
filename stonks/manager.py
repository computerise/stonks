"""Application manager controlling the flow of the program."""

from retrieval.api_client import APIClient
from retrieval.request_builder import YahooFinanceRequest


class ApplicationManager:
    """Controls the flow of the program."""

    def __init__(self):
        """Initialise class instance."""
        self.client = APIClient()

    def start(self):
        """Start the application."""
        yf_request = YahooFinanceRequest(ticker_symbol="GD")
        return self.client.get(yf_request)
