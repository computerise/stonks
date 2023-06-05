"""Discounted Cash Flow (DCF) valuation model."""


def discounted_cash_flow(future_cash_flows: list[float], discount_rate: float) -> float:
    """
    Calculate Discounted Cash Flow (DCF).

    See https://www.investopedia.com/terms/d/dcf.asp for details.
    """
    dcf = 0
    year = 1
    for yearly_cash_flow in future_cash_flows:
        dcf += yearly_cash_flow / (1 + discount_rate) ** year
        year += 1
    return dcf


def weighted_average_cost_of_capital(
    equity_market_value: float,
    debt_market_value: float,
    cost_of_equity: float,
    cost_of_debt: float,
    corporate_tax_rate: float,
) -> float:
    """
    Calculate the Weighted Average Cost of Capital (WACC), commonly used as the 'Discount Rate' for DCF valuation.

    See https://www.investopedia.com/terms/w/wacc.asp for details.
    """
    v = equity_market_value + debt_market_value
    weighted_value_of_equity_capital = cost_of_equity * equity_market_value / v
    weighted_value_of_debt_capital = (1 - corporate_tax_rate) * cost_of_debt * debt_market_value / v
    wacc = weighted_value_of_equity_capital + weighted_value_of_debt_capital
    return wacc


def capital_asset_pricing_model(risk_free_rate: float, beta_of_investment: float, expected_return_of_market: float) -> float:
    """
    Calculate the expected return of an investment using the Capital Asset Pricing Model (CAPM).

    See https://www.investopedia.com/terms/c/capm.asp for details.
    Note that the accuracy of CAPM is disputed. For alternatives, see:
     - Arbitrage Pricing Theory (https://www.investopedia.com/terms/a/apt.asp)
     - Fama and French Three Factor Model (https://www.investopedia.com/terms/f/famaandfrenchthreefactormodel.asp)
    """
    market_risk_premium = expected_return_of_market - risk_free_rate
    expected_return_of_investment = risk_free_rate + beta_of_investment * market_risk_premium
    return expected_return_of_investment