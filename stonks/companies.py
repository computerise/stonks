"""Company and company collection model."""

from dataclasses import dataclass

from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


@dataclass
class Company(Base):
    """
    Database model containing all dynamic attributes of a company.

    Requires:
    CREATE TABLE companies(ticker VARCHAR(5) UNIQUE, name VARCHAR(100) UNIQUE);
    """

    __tablename__ = "companies"
    ticker: str = Column(String(5), primary_key=True)
    name: str = Column(String)
    # index: str = Column(String)
    # exchange: str = Column(String)
    # sector: str = Column(String)
    # industry: str = Column(String)
    # price: float = Column(Float)
    # market_cap: float = Column(Float)


@dataclass
class CompanyCollection:
    """Company collection model for exchanges and indices."""

    id: str
    name: str
    companies: list[Company]
