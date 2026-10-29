"""
agent.py  (Orchestrator)
------------------------
OrchestratorAgent (Sara) is the root agent exposed to the ADK runtime.

Architecture
============
                        ┌─────────────────────┐
  User ──────────────▶  │  OrchestratorAgent  │  (Sara)
                        │   (root_agent)      │
                        └──────┬──────────────┘
                               │  delegates to
                   ┌───────────┴───────────┐
                   ▼                       ▼
          ┌────────────────┐    ┌────────────────────┐
          │ CarSearchAgent │    │ CarPresenterAgent  │
          │  find_cars()   │    │  A2UI formatting   │
          └────────────────┘    └────────────────────┘

Flow
====
1. User asks Sara a question (e.g. "show me Toyota cars under 5 lakhs").
2. Sara extracts the intent and calls CarSearchAgent with the right params.
3. CarSearchAgent queries the dataset and returns a raw JSON list.
4. Sara passes that JSON to CarPresenterAgent.
5. CarPresenterAgent formats the data into valid A2UI Direct JSON and
   returns it — which Sara forwards to the user.
"""

from google.adk.agents.llm_agent import Agent
from google.adk.tools.agent_tool import AgentTool

from learn_agent.presenter_agent import car_presenter_agent
from learn_agent.search_agent import car_search_agent

# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

root_agent = Agent(
    model="gemini-3.1-flash-lite",
    name="Sara",
    description="Sara – an AI car-buying assistant powered by a team of specialist agents.",
    instruction="""
You are Sara, a friendly AI car-buying assistant.
You coordinate a team of specialist agents to answer user questions about
cars in the marketplace.

## Your team
- **CarSearchAgent** – searches the dataset.
  Call it with: carName (brand or model substring) and/or price (max INR).
- **CarPresenterAgent** – formats raw JSON data into a user-friendly display.
  Always call it AFTER CarSearchAgent so the user sees a polished result.

## Workflow (follow this every time)
1. Understand the user's request. Extract `carName` and/or `price` if mentioned.
2. Call **CarSearchAgent** with those parameters.
3. Take the JSON result (or NO_RESULTS) from CarSearchAgent.
4. Pass it verbatim to **CarPresenterAgent**.
5. Return CarPresenterAgent's output directly to the user.

## Rules
- Never invent car details or prices.
- Never skip CarPresenterAgent — always let it format the final output.
- If the user asks something unrelated to cars, politely explain you only
  help with car searches.
""",
    tools=[
        AgentTool(agent=car_search_agent),
        AgentTool(agent=car_presenter_agent),
    ],
)
