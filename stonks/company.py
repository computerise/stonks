"""Representation of a company."""
from dataclasses import dataclass


@dataclass
class Company:
    """Class containing all parameters that a company may be filtered by."""

    ticker: str
    name: str
    exchange: str
    sector: str
    industry: str
    market_cap: float

    def set_data_attributes(self, company_data: dict) -> None:
        """Set each dictionary key and value as an instance attribute and value."""
        # Potentially a good use case for recursion to set all nested parameters as attributes.
        for attribute, value in company_data.items():
            setattr(self, attribute, value)
