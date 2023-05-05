"""Discounted Cash Flow valuation model."""


def discounted_cash_flow(cash_flows: list[float], discount_rate: float):
    """Calculate discounted cash flow."""
    dcf = 0
    year = 1
    for yearly_cash_flow in cash_flows:
        dcf += yearly_cash_flow / (1 + discount_rate) ** year
        year += 1
    return dcf


def weighted_average_cost_of_capital(
    equity_market_value: float,
    debt_market_value: float,
    cost_of_equity: float,
    cost_of_debt: float,
    corporate_tax_rate: float,
):
    """Calculate the WACC, commonly used as the 'Discount Rate' for DCF valuation."""
    v = equity_market_value + debt_market_value
    weighted_value_of_equity_capital = cost_of_equity * equity_market_value / v
    weighted_value_of_debt_capital = (
        (1 - corporate_tax_rate) * cost_of_debt * debt_market_value / v
    )
    return weighted_value_of_equity_capital + weighted_value_of_debt_capital
