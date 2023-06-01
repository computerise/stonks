from typing import Any

from stonks.processing.cash_flow import (
    most_recent_cash_flow,
    historical_cash_flows,
    historical_cash_flow_increase_rate,
    future_cash_flows,
)
from stonks.processing.models import discounted_cash_flow


def discounted_cash_flow_valuation(
    shares_outstanding: int,
    current_share_price: float,
    cash_flow_statements: list[dict[str, Any]],
    discount_rate: float = 0.05,
) -> dict[str, float]:
    historical = historical_cash_flows(cash_flow_statements)
    cash_flow_increase_rate = historical_cash_flow_increase_rate(historical)
    forecast_cash_flows = future_cash_flows(
        most_recent_cash_flow(historical),
        cash_flow_increase_rate,
        number_of_periods=5,
    )
    dcf = discounted_cash_flow(forecast_cash_flows, discount_rate)
    dcf_valuation_per_share = dcf / shares_outstanding
    return {
        "cash_flow_increase_rate": cash_flow_increase_rate,
        "dcf_valuation_per_share": dcf_valuation_per_share,
        "dcf_discount_per_share": dcf_valuation_per_share - current_share_price,
        "dcf_discount_ratio": dcf_valuation_per_share / current_share_price,
    }


def filter_valuation(
    dcf_valuation: dict[str, Any],
    cash_flow_growth_lower_bound: float = 0,
    cash_flow_growth_upper_bound: float = 1,
    price_ratio_criterion: float = 1,
) -> bool:
    """Filter a valuation based on eligibility criteria."""
    return (
        cash_flow_growth_lower_bound
        <= dcf_valuation.get("cash_flow_increase_rate")
        <= cash_flow_growth_upper_bound
        and dcf_valuation.get("dcf_discount_ratio") >= price_ratio_criterion
    )
