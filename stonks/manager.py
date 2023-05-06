"""Application manager controlling the flow of the program."""

import logging
from pathlib import Path

from stonks.storage import DataStorage
from stonks.configuration import ApplicationSettings, APIKeys
from stonks.retrieval.api_client import APIClient
from stonks.retrieval.response_handler import handle_response


class ApplicationManager:
    """Controls the flow of the program."""

    def __init__(self, application_settings: ApplicationSettings, api_keys: APIKeys):
        """Initialise class instance."""
        self.client = APIClient(api_keys)
        self.settings = application_settings
        logging.info("Created Application Manager.")

    @staticmethod
    def create_path(directory: str, ticker: str) -> Path:
        """Generate a path to the file named according to the stock's ticker."""
        return Path(directory, f"{ticker}.json")

    def start(self) -> None:
        """
        Start the application.

        If `request_new_data` is `True`, new data will be requested from the endpoint. If `request_new_data` is `False`, the application will search for archived data in data storage.
        If `store_new_data` is `True`, upon a successful response the data will be stored. If `store_new_data` is `False` the data will be discarded.
        """

        # Use tickers from user input JSON.
        tickers = ["GOOGL"]
        for company in tickers:
            self.get_company_data(company)

    def get_company_data(self, ticker: str) -> None:
        """Get data associated with a company."""
        if self.settings.request_new_data:
            response = self.client.retrieve(ticker)
            handle_response(
                self.create_path(self.settings.storage_directory, ticker),
                response,
                store=self.settings.store_new_data,
            )
        else:
            self.read_company_data(ticker)

    def read_company_data(self, ticker: str):
        """Read data associated with a company."""
        DataStorage.get_json(self.settings.storage_directory, ticker)
