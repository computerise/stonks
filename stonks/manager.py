"""Application manager controlling the flow of the program."""

from retrieval.api_client import APIClient
from retrieval.request_builder import YahooFinance


class ApplicationManager:
    """Controls the flow of the program."""

    def __init__(self):
        self.client = APIClient()

    def start(self):
        return self.client.get(YahooFinance())
