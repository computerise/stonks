"""Application manager controlling the flow of the program."""

import logging
from pathlib import Path

from stonks.storage import DataStorage
from stonks.configuration import ApplicationSettings, APIKeys
from stonks.retrieval.api_client import APIClient
from stonks.retrieval.response_handler import handle_response
from stonks.processing.cash_flow import process_cash_flow


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
        tickers = ["MSFT"]
        for company in tickers:
            company_data = self.get_company_data(company)
            discounted_cash_flow = process_cash_flow(company_data)
            print(f"{discounted_cash_flow=:_}")

    def get_company_data(self, ticker: str) -> None:
        """Get data associated with a company."""
        if self.settings.request_new_data:
            response = self.client.retrieve(ticker)
            handle_response(
                self.create_path(self.settings.storage_directory, ticker),
                response,
                store=self.settings.store_new_data,
            )
            return response.json()
        else:
            return DataStorage.get_json(self.settings.storage_directory, ticker)
