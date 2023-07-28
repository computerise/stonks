"""Company and company collection model."""

from dataclasses import dataclass


@dataclass
class StaticCompany:
    """Object containing all static attributes of a company."""

    ticker: str
    name: str
    index: str = None
    exchange: str = None
    sector: str = None
    industry: str = None


@dataclass
class Company(StaticCompany):
    """Model containing all dynamic attributes of a company."""

    price: float = None
    market_cap: float = None


@dataclass
class CompanyCollection:
    """Company collection model for exchanges and indices."""

    id: str
    name: str
    companies: list[Company]
