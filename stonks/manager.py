"""Application manager controlling the flow of the program."""

import logging
from pathlib import Path

from stonks.storage import DataStorage
from stonks.configuration import ApplicationSettings, APIKeys
from stonks.retrieval.api_client import APIClient
from stonks.retrieval.response_handler import handle_response
from stonks.processing.valuation import discounted_cash_flow_valuation, filter_valuation


class ApplicationManager:
    """Controls the flow of the program."""

    def __init__(self, application_settings: ApplicationSettings, api_keys: APIKeys):
        """Initialise class instance."""
        logging.info("Creating Application Manager...")
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
        candidates = {}
        # FUTURE: Use tickers from user input JSON file.
        tickers = ["MSFT", "AAPL", "GOOGL"]
        # FUTURE: Convert company_data to use Company class and assign calculated metrics as attributes.
        for company in tickers:
            # FUTURE: Move to method to extract relevant parameters for each model.
            company_data = self.get_company_data(company)
            cash_flow_statements = company_data.get("cashflowStatementHistory").get(
                "cashflowStatements"
            )
            shares_outstanding = (
                company_data.get("defaultKeyStatistics")
                .get("sharesOutstanding")
                .get("raw")
            )
            current_share_price = (
                company_data.get("financialData").get("currentPrice").get("raw")
            )
            logging.info(f"Cash flow metrics for '{company}':")
            dcf_valuation = discounted_cash_flow_valuation(
                shares_outstanding, cash_flow_statements
            )
            logging.info(
                f"DCF valuation (price per share): {dcf_valuation.get('dcf_valuation_per_share')}"
            )
            if filter_valuation(current_share_price, dcf_valuation):
                candidates[company] = dcf_valuation
        logging.info("Candidates:")
        logging.info(candidates)

    def get_company_data(self, ticker: str) -> None:
        """Get data associated with a company."""
        if self.settings.request_new_data:
            logging.info(f"Attempting to acquire new data for '{ticker}'.")
            response = self.client.retrieve(ticker)
            handle_response(
                self.create_path(self.settings.storage_directory, ticker),
                response,
                store=self.settings.store_new_data,
            )
            return response.json()
        else:
            logging.info(f"Using archived data for '{ticker}'.")
            return DataStorage.get_json(self.settings.storage_directory, ticker)
