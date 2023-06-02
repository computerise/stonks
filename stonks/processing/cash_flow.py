"""Cash flow calculations."""
import logging
from typing import Any


def most_recent_cash_flow(total_cash_flows: dict[str, float]) -> float:
    """Get the most recent cash flow, assuming cash flows are ordered from most-recent to least recent."""
    return list(total_cash_flows.values())[0]


def historical_cash_flows(
    cash_flow_statements: list[dict[str, Any]],
    cash_flow_items: list[str] = [
        "netIncome",
        "depreciation",
        "totalCashFromOperatingActivities",
        "capitalExpenditures",
        "investments",
        "otherCashflowsFromInvestingActivities",
        "totalCashflowsFromInvestingActivities",
        "dividendsPaid",
        "netBorrowings",
        "otherCashflowsFromFinancingActivities",
        "totalCashFromFinancingActivities",
        "effectOfExchangeRate",
        "repurchaseOfStock",
        "issuanceOfStock",
    ],
) -> dict[str, Any]:
    """Compute historical total cash flow."""
    total_cash_flows = {}
    # Iterate over cash flow statements for each period.
    for statement in cash_flow_statements:
        total_cash_flow = 0
        for item, value in statement.items():
            # Set the `endDate` of the cash flow period as the key for the summed cash flow for the period.
            if item == "endDate":
                end_date = value.get("fmt")
            if item in cash_flow_items:
                total_cash_flow += value.get("raw")
        # Add total cash flow to the dictionary of total cash flows for each period.
        total_cash_flows.update({end_date: total_cash_flow})
    logging.info(f"Historical cash flows: {total_cash_flows}")
    return total_cash_flows


def historical_cash_flow_increase_rate(total_cash_flows: dict[str, float]) -> float:
    """Perform historical cash flow analysis to compute the average rate of cash flow increase over all periods."""
    # Assumes cash flow statements are ordered from most-recent to least-recent.
    previous_cash_flow = None
    percentage_increases = []
    # Iterate through the cash flow periods from least-recent to most-recent.
    for cash_flow_amount in list(total_cash_flows.values())[::-1]:
        if previous_cash_flow is not None:
            cash_flow_increase = cash_flow_amount - previous_cash_flow
            percentage_increase = cash_flow_increase / abs(previous_cash_flow)
            percentage_increases.append(percentage_increase)
        # Update the cash previous cash flow
        previous_cash_flow = cash_flow_amount
    # Take the average percentage increase.
    cumulative_percentage_increase = sum(percentage_increases)
    mean_cash_flow_increase_percentage = cumulative_percentage_increase / len(percentage_increases)
    logging.info(f"Cash flow percentage increases: {percentage_increases}")
    logging.info(f"Mean cash flow increase percentage: {mean_cash_flow_increase_percentage:,}")
    return mean_cash_flow_increase_percentage


def future_cash_flows(
    initial_cash_flow: float,
    cash_flow_increase_percentage: float,
    number_of_periods: int = 5,
) -> dict[str, float]:
    """Generate future cash flow estimates based on the rate of cash flow increase."""
    future_cash_flows = []
    current_cash_flow = initial_cash_flow
    for _ in range(number_of_periods):
        current_cash_flow *= 1 + cash_flow_increase_percentage
        future_cash_flows.append(current_cash_flow)
    logging.info(f"Future cash flows: {future_cash_flows}")
    return future_cash_flows


def free_cash_flow(operating_cash_flow: float, capital_expenditure: float):
    """Compute free cash flow."""
    return operating_cash_flow - capital_expenditure
