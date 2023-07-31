"""Application manager controlling the flow of the program."""

import logging
from pathlib import Path

from stonks.storage import LocalDataStorage, PostgreSQLDatabase
from stonks.configuration import ApplicationSettings, MetricAssumptions, APIKeys
from stonks.companies import Company, CompanyCollection  # noqa
from stonks.retrieval.api_client import APIClient
from stonks.retrieval.response_handler import handle_response, YahooFinanceResponse
from stonks.processing.valuation import discounted_cash_flow_valuation, filter_valuation
from stonks.processing.models import (
    weighted_average_cost_of_capital,
    capital_asset_pricing_model,
    cost_of_debt,
)


class ApplicationManager:
    """Controls the flow of the program."""

    def __init__(
        self,
        application_settings: ApplicationSettings,
        metric_assumptions: MetricAssumptions,
        api_keys: APIKeys,
    ):
        """Initialise class instance."""
        logging.info("Creating Application Manager...")
        self.client = APIClient(api_keys)
        self.settings = application_settings
        self.assumptions = metric_assumptions
        self.database = PostgreSQLDatabase(self.settings.database_name, self.settings.postgres_url)
        logging.info("Created Application Manager.")

    @staticmethod
    def create_path(directory: str, ticker: str) -> Path:
        """Generate a path to the file named according to the stock's ticker."""
        return Path(directory, ticker).with_suffix(".json")

    def start(self) -> None:
        """
        Start the application.

        If `request_new_data` is `True`, new data will be requested from the endpoint.
        If `request_new_data` is `False`, the application will search for archived data in data storage.

        If `store_new_data` is `True`, upon a successful response the data will be stored.
        If `store_new_data` is `False` the data will be discarded.
        """
        candidates = {}
        tickers = LocalDataStorage.read_json(self.settings.input_file_path).keys()
        # FUTURE: Convert company_data to use Company class and assign calculated metrics as attributes.
        for company in tickers:
            company_data = self.get_company_data(company)
            # Move to retrieval.response_handler. Set required values as attributes of company.
            try:
                dcf_data = YahooFinanceResponse.get_data_for_discounted_cash_flow(company_data)
                wacc_data = YahooFinanceResponse.get_data_for_weighted_average_cost_of_capital(company_data)
                capm_data = YahooFinanceResponse.get_data_for_capital_asset_pricing_model(
                    company_data, self.assumptions, "sp500"
                )
            except (KeyError, TypeError) as exc:
                logging.warning(f"Failed to extract a company data attribute for `{company}`.")
                logging.debug(exc)
                continue

            logging.info(f"Cash flow metrics for '{company}':")
            debt_cost = cost_of_debt(
                self.assumptions.usa.get("risk_free_rate_of_return"),
                self.assumptions.usa.get("sp500").get("average_credit_spread"),
                self.assumptions.usa.get("corporate_tax_rate"),
            )
            capm = capital_asset_pricing_model(*capm_data)
            wacc = weighted_average_cost_of_capital(
                wacc_data[0],
                wacc_data[1],
                capm,
                debt_cost,
                self.assumptions.usa.get("corporate_tax_rate"),
            )
            dcf_valuation = discounted_cash_flow_valuation(*dcf_data, wacc)
            logging.info(f"DCF valuation (price per share): {dcf_valuation.get('dcf_valuation_per_share')}")
            if filter_valuation(dcf_valuation):
                candidates[company] = dcf_valuation
                logging.info(
                    f"""
                    Added `{company}` to the candidates list with an absolute discount of
                    `{dcf_valuation.get('dcf_discount_per_share')}` per share and a discount ratio of
                    `{dcf_valuation.get('dcf_discount_ratio')}`.
                    """
                )

        logging.info("Candidates:")
        logging.info(candidates)
        candidates_path = Path(self.settings.output_directory_path, LocalDataStorage.timestamped_file("candidates", ".json"))
        LocalDataStorage.write_json(candidates_path, candidates)

    def get_company_data(self, ticker: str) -> None:
        """Get data associated with a company."""
        if self.settings.request_new_data:
            logging.info(f"Attempting to acquire new data for '{ticker}'.")
            response = self.client.retrieve(ticker)
            handle_response(
                self.create_path(self.settings.storage_directory_path, ticker),
                response,
                store=self.settings.store_new_data,
            )
            return response.json()
        else:
            logging.info(f"Using archived data for '{ticker}'.")
            return LocalDataStorage.get_json(self.settings.storage_directory_path, ticker)

    def load_local_data(self) -> CompanyCollection:
        """Load local data from JSON files as a CompanyCollection."""
        company_collection = LocalDataStorage.create_company_collection_from_local(
            self.settings.input_file_path, "S&P500", "Standard and Poor's 500"
        )
        print(company_collection)

    def insert_data(self) -> None:
        """Insert CompanyCollection to database."""
        raise NotImplementedError
