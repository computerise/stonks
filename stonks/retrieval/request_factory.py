"""Factories to instantiate all request objects."""

from requests import Request

from stonks.retrieval.request_templates import RapidAPIRequest, YahooFinanceRequest


class RequestFactory:
    """Request factory for generating all requests."""

    def __init__(self, api_key: str) -> None:
        """Instantiate the request factory with the API key."""
        self.api_key = api_key

    def construct_request() -> Request:
        """Construct a request."""
        raise NotImplementedError


class RapidAPIRequestFactory(RequestFactory):
    """Request factory for generating all RapidAPI requests."""

    def __init__(self, api_key: str) -> None:
        """Instantiate the RapidAPI request factory with the RapidAPI key."""
        super().__init__(api_key)

    def construct_request(self, content_type: str) -> RapidAPIRequest:
        """Construct a prepared RapidAPIRequest."""
        return RapidAPIRequest(content_type, self.api_key).prepare()


class YahooFinanceRequestFactory(RapidAPIRequestFactory):
    """Request factory for generating all Yahoo Finance API requests."""

    def __init__(
        self,
        api_key: str,
        content_type: str = "application/octet-stream",
        segments: tuple[str] = ("mo/", "module/"),
        base_url: str = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/",
    ) -> None:
        """Instantiate the Yahoo Finance API request factory with parameters that will never change."""
        super().__init__(api_key)
        self.content_type = content_type
        self.segments = segments
        self.base_url = base_url

    def construct_request(
        self,
        ticker_symbol: str,
        query_parameters: tuple[str] = None,
    ) -> YahooFinanceRequest:
        """Construct a prepared Yahoo Finance API Request."""
        return YahooFinanceRequest(ticker_symbol, self.segments, self.base_url, query_parameters, self.api_key).prepare()
