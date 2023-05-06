"""Cash flow calculations."""
from typing import Any

from stonks.processing.models.discounted_cash_flow import discounted_cash_flow


def historical_cash_flow(cash_flow_statements: list[dict[str, Any]]) -> dict:
    total_cash_flows = {}
    # Iterate over cash flow statements for each period.
    for statement in cash_flow_statements:
        total_cash_flow = 0
        for item, value in statement.items():
            # Exclude `maxAge` field.
            if item != "maxAge":
                # Set the `endDate` of the cash flow period as the key for the summed cash flow for the period.
                if item == "endDate":
                    end_date = value.get("fmt")
                # Sum all cash flow items for the period.
                else:
                    total_cash_flow += value.get("raw")
        # Add total cash flow to the dictionary of total cash flows for each period.
        total_cash_flows.update({end_date: total_cash_flow})
    return total_cash_flows


def historical_cash_flow_increase_rate(total_cash_flows: dict[str, float]) -> float:
    """Perform historical cash flow analysis to compute the average rate of cash flow increase over all periods."""
    # Assumes cash flow statements are ordered from most-recent to least-recent.
    initial_cash_flow = None
    cumulative_percentage_increases = []
    # Iterate through the cash flow periods from least-recent to most-recent.
    for cash_flow_amount in list(total_cash_flows.values())[::-1]:
        if initial_cash_flow is not None:
            cash_flow_increase = cash_flow_amount - previous_cash_flow
            percentage_increase = previous_cash_flow / cash_flow_increase
            cumulative_percentage_increases.append(percentage_increase)
        # Update the cash previous cash flow
        previous_cash_flow = cash_flow_amount
    # Take the average percentage increase.
    cumulative_percentage_increase = sum(cumulative_percentage_increases)
    average_cash_flow_increase_percentage = cumulative_percentage_increase / len(
        cumulative_percentage_increases
    )
    return average_cash_flow_increase_percentage


def most_recent_cash_flow(total_cash_flows: dict[str, float]) -> float:
    """Get the most recent cash flow, assuming cash flows are ordered from most-recent to least recent."""
    return list(total_cash_flows.values())[0]


def future_cash_flow(
    initial_cash_flow: float,
    cash_flow_increase_percentage: float,
    number_of_periods: int = 5,
):
    future_cash_flows = []
    current_cash_flow = initial_cash_flow
    for _ in range(number_of_periods):
        current_cash_flow *= 1 + cash_flow_increase_percentage
        future_cash_flows.append(current_cash_flow)
    return future_cash_flows


def process_cash_flow(company_data: dict[str, Any]):
    cash_flow_statements = company_data.get("cashflowStatementHistory").get(
        "cashflowStatements"
    )
    historic_cash_flows = historical_cash_flow(cash_flow_statements)
    future_cash_flows = future_cash_flow(
        most_recent_cash_flow(historic_cash_flows),
        historical_cash_flow_increase_rate(historic_cash_flows),
        number_of_periods=5,
    )
    return discounted_cash_flow(future_cash_flows, discount_rate=0.05)
