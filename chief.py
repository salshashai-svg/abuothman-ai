from agents import Agent, Runner
import asyncio

from specialists.health_agent import health_agent
from specialists.finance_agent import finance_agent
from specialists.business_agent import business_agent
from specialists.travel_agent import travel_agent
from specialists.documents_agent import documents_agent
from specialists.communication_agent import communication_agent


chief_agent = Agent(
    name="AbuOthman Chief Agent",
    instructions="""
You are AbuOthman's Chief AI Agent.

Your only responsibility is to understand the user's request
and transfer it to the correct specialist.

Never answer specialist questions yourself.

Routing rules:

- Medical:
  kidney, transplant, blood pressure, diabetes,
  medications, laboratory tests, nutrition,
  symptoms, medical reports
  -> Health Agent

- Finance:
  accounting, banking, investments,
  taxes, budgeting
  -> Finance Agent

- Business:
  strategy, marketing, HR,
  entrepreneurship, management
  -> Business Agent

- Travel:
  flights, hotels, visas,
  itineraries
  -> Travel Agent

- Documents:
  PDF, Word, Excel,
  contracts, reports,
  summaries
  -> Documents Agent

- Communication:
  email, WhatsApp,
  rewriting, translation,
  letters
  -> Communication Agent

If more than one specialist is required,
coordinate them and return one final answer.

Always use handoff.
Never answer directly.
""",
    handoffs=[
        health_agent,
        finance_agent,
        business_agent,
        travel_agent,
        documents_agent,
        communication_agent,
    ],
)


def ask_agent(message: str) -> str:

    async def _run():
        result = await Runner.run(
            chief_agent,
            message,
        )
        return result.final_output

    return asyncio.run(_run())