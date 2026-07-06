from google.adk.agents.llm_agent import Agent


def estimate_budget_tool(budget_level: str) -> dict:
    """
    Estimates a travel budget strategy based on the user's selected budget level.
    This tool is used by the TripPilot agent to provide budget-aware planning.
    """
    strategies = {
        "Low": "Use free attractions, public transport, walking routes, and casual food options.",
        "Medium": "Mix paid attractions with free experiences, use public transport, and include comfortable meals.",
        "High": "Include premium experiences, flexible transport options, reservations, and higher-comfort food choices."
    }

    return {
        "status": "success",
        "budget_level": budget_level,
        "strategy": strategies.get(budget_level, "Use a balanced budget strategy.")
    }


def schedule_risk_tool(number_of_places: int) -> dict:
    """
    Detects whether a one-day itinerary may be too packed.
    The goal is to help organized travelers avoid unrealistic schedules.
    """
    if number_of_places >= 5:
        risk = "High"
        advice = "Reduce the plan to the top 3 attractions and add more transport and rest buffers."
    elif number_of_places >= 3:
        risk = "Medium"
        advice = "The plan is manageable, but transport and rest buffers are recommended."
    else:
        risk = "Low"
        advice = "The schedule appears realistic for a one-day itinerary."

    return {
        "status": "success",
        "risk": risk,
        "advice": advice
    }


root_agent = Agent(
    model="gemini-2.5-flash",
    name="trippilot_agent",
    description="A concierge-style travel planning agent for structured one-day itineraries.",
    instruction="""
You are TripPilot, a travel planning agent for organized travelers.

Your role is to help users create realistic one-day itineraries with:
- time blocks
- budget guidance
- packing checklists
- reservation reminders
- rainy day backup plans
- schedule risk warnings

Use the available tools when budget or schedule risk needs to be estimated.

Security and privacy rules:
- Do not ask users for passport numbers.
- Do not ask for payment details.
- Do not ask for exact home addresses.
- Do not store user data.
- If live information such as opening hours, ticket prices, or transport delays is needed,
  tell users to verify the information before travel.
""",
    tools=[
        estimate_budget_tool,
        schedule_risk_tool
    ],
)