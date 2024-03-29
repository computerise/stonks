"""Templates for all request objects."""

from requests import Request

from stonks.error_handler import raise_fatal_error


class RapidAPIRequest(Request):
    """Request for all Rapid API (https://rapidapi.com/hub) requests."""

    def __init__(
        self,
        x_rapidapi_key: str,
        *args,
        **kwargs,
    ) -> None:
        """Initialise RapidAPI request."""
        super().__init__(self, *args, **kwargs)
        self.method = "GET"
        self.url = "https://rapidapi.com/"
        self.set_headers(x_rapidapi_key)

    def set_headers(self, x_rapidapi_key: str) -> None:
        """Format request headers as a dictionary."""
        self.headers = {"X-RapidAPI-Key": x_rapidapi_key}


class YahooFinanceRequest(RapidAPIRequest):
    """Request for YahooFinance API (https://rapidapi.com/sparior/api/yahoo-finance15)."""

    def __init__(
        self,
        ticker_symbol: str,
        query_parameters: tuple[str] = None,
        segments: tuple[str] = ("mo/", "module/"),
        base_url: str = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/",
        *args,
        **kwargs,
    ) -> None:
        """Initialise Yahoo Finance Request."""
        super().__init__(*args, **kwargs)
        self.set_url(ticker_symbol, segments, base_url)
        self.set_params(query_parameters)

    def set_url(self, ticker_symbol: str, segments: list[str], base_url: str) -> None:
        """Format and set the request URL as an attribute."""
        self.url = f"{base_url}{''.join(segments)}{ticker_symbol}"

    def set_params(
        self,
        query_parameters: tuple[str],
        default_queries: tuple[str] = (
            "financial-data",
            "income-statement",
            "balance-sheet",
            "cashflow-statement",
            "default-key-statistics",
        ),
    ) -> None:
        """Format and set query parameters for the request."""
        if not query_parameters:
            query_parameters = default_queries
        if not type(query_parameters) is tuple:
            raise_fatal_error(
                f"Received non-tuple argument for queries: {query_parameters}. Queries should be a tuple of strings.",
                new_exception=TypeError,
            )
        formatted_queries = self.format_queries(query_parameters)
        self.params = formatted_queries

    def format_queries(
        self, query_parameters: tuple[str], max_query_parameters: int = 5
    ) -> dict[str, str]:
        """Format a maximum of 5 valid query parameters."""
        number_of_params = len(query_parameters)
        if number_of_params <= max_query_parameters:
            if self.valid_query_parameters(query_parameters):
                return {"module": ",".join(query_parameters)}
        else:
            raise_fatal_error(
                f"{number_of_params} query parameters specified; exceeds maximum of {max_query_parameters}."
            )

    def valid_query_parameters(self, query_parameters: tuple[str]) -> bool:
        """Raise and exception if any query parameters are invalid, otherwise return True."""
        # Parameters like these could be stored in a configuration file for each endpoint.
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
            "financial-data",
            "earnings",
        )
        for query in query_parameters:
            if query not in valid_query_parameters:
                raise raise_fatal_error(
                    f"""
                    Invalid query parameter '{query}' was specified. Queries are limited to:
                    {','.join(valid_query_parameters)}
                    """
                )
        return True
