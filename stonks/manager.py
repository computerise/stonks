"""Application manager controlling the flow of the program."""

from stonks.retrieval.api_client import APIClient
from stonks.retrieval.request_builder import YahooFinanceRequest
from stonks.retrieval.response_handler import handle_response


class ApplicationManager:
    """Controls the flow of the program."""

    def __init__(self):
        """Initialise class instance."""
        self.client = APIClient()

    def start(self):
        """Start the application."""
        ticker = "AAPL"
        yf_request = YahooFinanceRequest(ticker_symbol=ticker)
        response = self.client.get(yf_request)
        handle_response(f"data/{ticker}.json", response)
