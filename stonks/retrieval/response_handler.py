"""Handle API responses."""

import logging
from typing import Any
from pathlib import Path
from requests.models import Response

from stonks.error_handler import raise_fatal_error
from stonks.storage import DataStorage


def handle_response(output_path: Path, response: Response, store: bool = True):
    if response.ok:
        if store:
            DataStorage.write_json(output_path, response.json())
            logging.info(f"Successfully wrote output to {output_path}.")
    else:
        raise_fatal_error(
            f"Endpoint {response.url} responded with non-200 status code '{response.status_code}'.",
        )


class YahooFinanceResponse:
    """Response object for YahooFinance API (https://rapidapi.com/sparior/api/yahoo-finance15)."""

    def get_data_for_discounted_cash_flow(company_data: dict[str, Any]):
        try:
            shares_outstanding = (
                company_data.get("defaultKeyStatistics")
                .get("sharesOutstanding")
                .get("raw")
            )
            current_share_price = (
                company_data.get("financialData").get("currentPrice").get("raw")
            )
            cash_flow_statements = company_data.get("cashflowStatementHistory").get(
                "cashflowStatements"
            )
            return shares_outstanding, current_share_price, cash_flow_statements
        except AttributeError:
            logging.warning(f"Failed to extract get a company data attribute")
