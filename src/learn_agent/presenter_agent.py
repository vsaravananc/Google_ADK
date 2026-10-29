"""
presenter_agent.py
------------------
PresenterAgent is a sub-agent whose **only** job is to take a raw JSON
list of car records and render it as a valid A2UI Direct JSON response.

It knows nothing about how data is fetched — that is CarSearchAgent's job.
"""

from a2ui.core.basic_catalog import BasicCatalog
from a2ui.core.schema import ProtocolVersion
from a2ui.inference_formats.direct_json import DirectJsonFormat
from google.adk.agents.llm_agent import Agent

# ---------------------------------------------------------------------------
# A2UI setup  (same as the original single-agent, but isolated here)
# ---------------------------------------------------------------------------

inference_format = DirectJsonFormat([BasicCatalog(ProtocolVersion.V0_8)])
a2ui_prompt = inference_format.prompt_generator.generate()

# ---------------------------------------------------------------------------
# Agent definition
# ---------------------------------------------------------------------------

car_presenter_agent = Agent(
    model="gemini-3.1-flash-lite",
    name="CarPresenterAgent",
    description=(
        "Formats a raw JSON list of car records into a beautiful A2UI "
        "Direct JSON response for the end-user. Call this agent after "
        "CarSearchAgent returns its data."
    ),
    instruction=f"""
You are CarPresenterAgent, a specialist in rendering car data for users.

You will receive either:
  • A JSON array of car records (from CarSearchAgent).
  • The string NO_RESULTS if no cars matched the search.

Your job:
1. If the input is NO_RESULTS, produce a friendly A2UI message explaining
   that no matching cars were found in the marketplace.
2. Otherwise, parse the JSON and produce a valid A2UI Direct JSON output
   that displays each car with:
     - Car Name
     - Brand
     - Selling Price (INR)
     - Manufacturing Year
     - Fuel Type
     - Transmission
   Format prices in a human-readable way (e.g., ₹5,00,000).

A2UI rules you MUST follow:
{a2ui_prompt}

Output ONLY the A2UI JSON — no extra prose outside the JSON structure.
""",
    tools=[],  # no tools needed – this agent only formats data
)
