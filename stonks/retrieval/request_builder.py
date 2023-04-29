"""Definitions of the requests."""
from dataclasses import dataclass


@dataclass
class Request:
    base_url: str


@dataclass
class RapidAPIRequest(Request):
    content_type: str = "application/octet-stream"
    x_rapidapi_key: str = "d3e6db282emsh4fafb3bbd7fde49p16dfb1jsn448c3b411a42"
    x_rapidapi_host: str = "yahoo-finance15.p.rapidapi.com"

    @property
    def headers(self):
        return {
            "content-type": self.content_type,
            "X-RapidAPI-Key": self.x_rapidapi_key,
            "X-RapidAPI-Host": self.x_rapidapi_host,
        }


@dataclass
class YahooFinanceRequest(RapidAPIRequest):
    base_url: str = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/"
    query_parameters: tuple = (
        "asset-profile",
        "income-statement",
        "balance-sheet",
        "cashflow-statement",
        "default-key-statistics",
        "calendar-events",
        "sec-filings",
        "upgrade-downgrade-history",
        "institution-ownership",
        "fund-ownership",
        "insider-transactions",
        "insider-holders",
        "earnings-history",
    )

    @staticmethod
    def format_query_string(query_parameters: tuple) -> dict:
        return {"module": ",".join(query_parameters)}

    def overview(self, ticker_symbol: str, query_parameters: tuple) -> None:
        self.format_query_string(query_parameters)
        self.url = f"{self.base_url}mo/module/{ticker_symbol}"
