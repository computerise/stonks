"""Handle API responses."""

import logging
from typing import Any
from pathlib import Path
from requests.models import Response

from stonks.error_handler import raise_fatal_error
from stonks.storage import LocalDataStorage


def handle_response(output_path: Path, response: Response, store: bool = True) -> None:
    body = response.json()
    if "error" in body:
        logging.warning(f"Endpoint {response.url} responded with error `{body.get('error')}`.")
    elif response.ok:
        if store:
            LocalDataStorage.write_json(output_path, body)
            logging.info(f"Successfully wrote output to {output_path}.")
    else:
        raise_fatal_error(
            f"Endpoint {response.url} responded with non-200 status code `{response.status_code}`.",
        )


class YahooFinanceResponse:
    """Response object for YahooFinance API (https://rapidapi.com/sparior/api/yahoo-finance15)."""

    def get_data_for_discounted_cash_flow(
        company_data: dict[str, Any], quarterly: bool = False
    ) -> tuple[float, float, list[dict[str, Any]]]:
        """Extract the relevant data to compute Discounted Cash Flow."""
        if quarterly:
            cash_flow_statement_history = "cashflowStatementHistoryQuarterly"
        else:
            cash_flow_statement_history = "cashflowStatementHistory"
        shares_outstanding = company_data["defaultKeyStatistics"]["sharesOutstanding"]["raw"]
        current_share_price = company_data["financialData"]["currentPrice"]["raw"]
        cash_flow_statements = company_data[cash_flow_statement_history]["cashflowStatements"]
        return shares_outstanding, current_share_price, cash_flow_statements

    def get_data_for_weighted_average_cost_of_capital(
        company_data: dict[str, Any], quarterly: bool = False
    ) -> tuple[float, float]:
        """Extract the relevant data to compute Weighted Average Cost of Capital."""
        if quarterly:
            balance_sheet_history = "balanceSheetHistoryQuarterly"
        else:
            balance_sheet_history = "balanceSheetHistory"
        balance_sheet_list = company_data[balance_sheet_history]["balanceSheetStatements"]
        balance_sheet = balance_sheet_list[0]
        total_equity = balance_sheet["totalStockholderEquity"]["raw"]
        total_debt = balance_sheet["longTermDebt"]["raw"] + balance_sheet["shortLongTermDebt"]["raw"]
        return total_equity, total_debt

    def get_data_for_capital_asset_pricing_model(
        company_data: dict[str, Any], assumptions: dict[str, Any], exchange: str
    ) -> tuple[float, float, float]:
        """
        Extract the relevant data for the Capital Asset Pricing model.

        Refactor to supply only the relevant assumptions for this company, not all assumptions.
        """
        try:
            beta = company_data["defaultKeyStatistics"]["beta"]["raw"]
        except TypeError:
            raise TypeError('"raw" value for "beta" is invalid.')
        risk_free_rate_of_return = assumptions.usa.get("risk_free_rate_of_return")
        market_rate_of_return = assumptions.usa.get(exchange).get("rate_of_return")
        return risk_free_rate_of_return, market_rate_of_return, beta
