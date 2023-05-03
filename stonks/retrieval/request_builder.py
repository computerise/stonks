"""Definitions of the requests."""
import os
from dotenv import load_dotenv
from dataclasses import dataclass

# Load .env file.
load_dotenv()


@dataclass
class Request:
    """Base class for all requests."""

    base_url: str
    content_type: str


@dataclass
class RapidAPIRequest(Request):
    """Base class for all Rapid API (https://rapidapi.com/hub) requests."""

    content_type: str = "application/octet-stream"
    x_rapidapi_key: str = os.getenv("RAPID_API_KEY")
    x_rapidapi_host: str = "yahoo-finance15.p.rapidapi.com"

    @property
    def headers(self):
        """Format request headers as a dictionary."""
        return {
            "content-type": self.content_type,
            "X-RapidAPI-Key": self.x_rapidapi_key,
            "X-RapidAPI-Host": self.x_rapidapi_host,
        }

    def valid_query_parameters(self, query_parameters: tuple[str]) -> bool:
        """Raise and exception if any query parameters are invalid, otherwise return True."""
        valid_query_parameters = (
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
        for query in query_parameters:
            if query not in valid_query_parameters:
                raise ValueError(
                    f"Invalid query parameter '{query}' was specified. Queries are limited to: {','.join(valid_query_parameters)}"
                )
        return True


@dataclass
class YahooFinanceRequest(RapidAPIRequest):
    """Request object YahooFinance API (https://rapidapi.com/sparior/api/yahoo-finance15)."""

    ticker_symbol: str = "AAPL"
    segments: tuple[str] = ("mo/", "module/")
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

    def __post_init__(self) -> None:
        """Post initialisation."""
        self.url = self.build_url(self.ticker_symbol, self.segments)
        self.query_string = self.format_query_string(self.query_parameters)

    def build_url(self, ticker_symbol: str, segments: list[str]) -> str:
        """Format the request url."""
        return f"{self.base_url}{''.join(segments)}{ticker_symbol}"

    def format_query_string(self, query_parameters: tuple[str]) -> dict:
        """Format a maximum of 5 valid query parameters as a string."""
        if len(query_parameters) <= 5:
            if self.valid_query_parameters(query_parameters):
                return {"module": ",".join(query_parameters)}
        else:
            raise ValueError(
                f"{len(query_parameters)} query parameters specified; exceeds maximum of 5."
            )
