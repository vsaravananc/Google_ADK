"""
search_agent.py
---------------
CarSearchAgent is a sub-agent whose **only** job is to query the
car-marketplace dataset and return raw JSON records.

It knows nothing about how the results will be presented to the user.
That concern belongs to the PresenterAgent.
"""

import pandas as pd
from google.adk.agents.llm_agent import Agent


# ---------------------------------------------------------------------------
# Tool
# ---------------------------------------------------------------------------


def find_cars(
    carName: str | None = None,
    price: str | None = None,
) -> str:
    """Find cars by brand / car name and an optional maximum selling price.

    Args:
        carName: A brand name or car model substring to filter on
                 (case-insensitive). Pass None or "" to skip this filter.
        price:   Maximum selling price in INR as a numeric string.
                 Pass None or "" to skip this filter.

    Returns:
        A JSON string (list of records) of all matching cars, or an empty
        JSON array when nothing matches.
    """
    data = pd.read_excel("src/learn_agent/car_marketplace_dataset.xlsx")

    condition = pd.Series(True, index=data.index)

    if carName and carName.strip():
        condition &= data["Brand"].str.contains(
            carName.strip(), case=False, na=False
        ) | data["Car Name"].str.contains(
            carName.strip(), case=False, na=False
        )

    if price and price.strip():
        try:
            condition &= data["Selling Price (INR)"] < float(price)
        except ValueError:
            pass  # ignore malformed price strings

    matched = data.loc[condition].head(2)
    if matched.empty:
        return "[]"

    return matched.to_json(orient="records")


# ---------------------------------------------------------------------------
# Agent definition
# ---------------------------------------------------------------------------

car_search_agent = Agent(
    model="gemini-3.1-flash-lite",
    name="CarSearchAgent",
    description=(
        "Searches the car-marketplace dataset. "
        "Call this agent with a car name and/or a maximum price "
        "and it will return a JSON list of matching car records."
    ),
    instruction="""
You are CarSearchAgent, a specialist in querying car data.

Your ONLY task:
1. Call the `find_cars` tool with the parameters given by the orchestrator.
2. Return the raw JSON result exactly as the tool gives it back.
3. Do NOT add commentary, formatting, or extra text.

If no cars match, return the string: NO_RESULTS
""",
    tools=[find_cars],
)
