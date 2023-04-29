"""Definitions of the requests."""
from dataclasses import dataclass


@dataclass
class Request:
    url: str
    content_type: str


@dataclass
class RapidAPI(Request):
    content_type: str = "application/octet-stream"
    x_rapidapi_key: str = "Redacted"
    x_rapidapi_host: str = "yahoo-finance15.p.rapidapi.com"

    @property
    def headers(self):
        return {
            "content-type": self.content_type,
            "X-RapidAPI-Key": self.x_rapidapi_key,
            "X-RapidAPI-Host": self.x_rapidapi_host,
        }


@dataclass
class YahooFinance(RapidAPI):
    url: str = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/ne/news"
