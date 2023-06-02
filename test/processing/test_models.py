"""Test Discounted Cash Flow calculations."""

from unittest import TestCase

from stonks.processing.models import (
    discounted_cash_flow,
    weighted_average_cost_of_capital,
)


class TestDiscountedCashFlow(TestCase):
    """Test Discounted Cash Flow calculations."""

    def test_discounted_cash_flow(self) -> None:
        """Test that Discounted Cash Flow is calculated correctly."""
        cash_flows = [1e6, 1e6, 4e6, 4e6, 6e6]
        self.assertEqual(int(discounted_cash_flow(cash_flows, 0.05)), 13_306_727)

    def test_weighted_average_cost_of_capital(self) -> None:
        """Test that Weighted Average Cost of Capital is calculated correctly."""
        wacc = weighted_average_cost_of_capital(
            equity_market_value=35_197.29,
            debt_market_value=3_411,
            cost_of_equity=0.094,
            cost_of_debt=0.025,
            corporate_tax_rate=0.21,
        )
        self.assertAlmostEqual(wacc, 0.08744009)
