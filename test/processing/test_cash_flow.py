"""Test cash flow."""

from unittest import TestCase

from stonks.processing.cash_flow import (
    historical_cash_flow,
    historical_cash_flow_increase_rate,
    future_cash_flow,
    most_recent_cash_flow,
)


class TestCashFlow(TestCase):
    """Test cash flow calculations."""

    def __init__(self) -> None:
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

        self.sample_company_data = {
            "cashflowStatementHistory": {
                "cashflowStatements": [self.sample_cash_flow_statement * 4],
                "maxAge": 86400,
            }
        }

    def test_historical_cash_flow(self):
        pass

    def test_historical_cash_flow_increase_rate(self):
        pass

    def test_future_cash_flow(self):
        pass

    def test_most_recent_cash_flow(self):
        pass
