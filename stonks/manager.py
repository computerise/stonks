"""Application manager controlling the flow of the program."""

from retrieval.api_client import APIClient
from retrieval.request_builder import YahooFinanceRequest


class ApplicationManager:
    """Controls the flow of the program."""

    def __init__(self):
        self.client = APIClient()

    def start(self):
        yf_request = YahooFinanceRequest()
        yf_overview = yf_request.overview(
            "AAPL", query_parameters=yf_request.query_parameters
        )
        return self.client.get(yf_overview)
