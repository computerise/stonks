from typing import Any

from stonks.processing.cash_flow import (
    most_recent_cash_flow,
    historical_cash_flows,
    historical_cash_flow_increase_rate,
    future_cash_flows,
)
from stonks.processing.models.discounted_cash_flow import discounted_cash_flow


def discounted_cash_flow_valuation(
    shares_outstanding: int,
    cash_flow_statements: list[dict[str, Any]],
    discount_rate: float = 0.05,
):
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
    }


def filter_valuation(
    current_share_price: float,
    dcf_valuation: dict,
    cash_flow_growth_threshold: float = 1,
    price_ratio_criterion: float = 1,
) -> bool:
    """Filter a valuation based on eligibility criteria."""
    return (
        dcf_valuation.get("cash_flow_increase_rate") <= cash_flow_growth_threshold
        and dcf_valuation.get("dcf_valuation_per_share") / current_share_price
        >= price_ratio_criterion
    )
