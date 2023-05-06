"""Test cash flow."""

from unittest import TestCase
from typing import Any
from copy import deepcopy

from stonks.processing.cash_flow import (
    historical_cash_flow,
    historical_cash_flow_increase_rate,
    future_cash_flow,
    most_recent_cash_flow,
)


class TestCashFlow(TestCase):
    """Test cash flow calculations."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialise cash flow tests."""
        super(TestCashFlow, self).__init__(*args, **kwargs)
        self.sample_cash_flow_statement = {
            "maxAge": 1,
            "endDate": {"raw": 1663977600, "fmt": "2022-09-24"},
            "netIncome": {
                "raw": 99803000000,
                "fmt": "99.8B",
                "longFmt": "99,803,000,000",
            },
            "depreciation": {
                "raw": 11104000000,
                "fmt": "11.1B",
                "longFmt": "11,104,000,000",
            },
            "changeToNetincome": {
                "raw": 10044000000,
                "fmt": "10.04B",
                "longFmt": "10,044,000,000",
            },
        }
        self.sample_cash_flow_statements = self.generate_sample_cash_flow_statements(
            self.sample_cash_flow_statement
        )
        self.sample_company_data = {
            "cashflowStatementHistory": {
                "cashflowStatements": self.sample_cash_flow_statements,
                "maxAge": 86400,
            }
        }
        self.sample_historical_cash_flow = historical_cash_flow(
            self.sample_cash_flow_statements
        )

    def generate_sample_cash_flow_statements(
        self, cash_flow_statement: dict[str, Any], periods: int = 4
    ) -> list[dict[str, Any]]:
        sample_cash_flow_statements = [
            deepcopy(cash_flow_statement) for _ in range(periods)
        ]
        for period, statement in enumerate(sample_cash_flow_statements):
            statement["endDate"]["fmt"] = str(period + 1)
            statement["netIncome"]["raw"] += (period + 1) * 1e9
        return sample_cash_flow_statements

    def test_historical_cash_flow(self) -> None:
        self.assertEqual(
            self.sample_historical_cash_flow,
            {
                "1": 121951000000.0,
                "2": 122951000000.0,
                "3": 123951000000.0,
                "4": 124951000000.0,
            },
        )

    def test_historical_cash_flow_increase_rate(self) -> None:
        pass

    def test_future_cash_flow(self) -> None:
        pass

    def test_most_recent_cash_flow(self) -> None:
        """Test getting the most recent cash flow."""
        self.assertEqual(
            most_recent_cash_flow(self.sample_historical_cash_flow), 121951000000.0
        )
