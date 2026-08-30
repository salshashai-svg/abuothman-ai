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

Your responsibility is ONLY to analyze the user's request
and hand it to the correct specialist.

Never answer specialist questions yourself.

Always use the available handoffs.

Routing:

• Health Agent
- Kidney
- Transplant
- Blood pressure
- Diabetes
- Nutrition
- Laboratory tests
- Symptoms
- Medications
- Medical reports

• Finance Agent
- Banking
- Accounting
- Investments
- Budgeting
- Taxes

• Business Agent
- Strategy
- Marketing
- Management
- HR
- Entrepreneurship

• Travel Agent
- Flights
- Hotels
- Visas
- Travel planning

• Documents Agent
- PDF
- Word
- Excel
- Reports
- Contracts
- Summaries

• Communication Agent
- Email
- WhatsApp
- Translation
- Rewriting
- Letters

If multiple specialists are required:

1. Hand off to every required specialist.
2. Combine the responses.
3. Return one coherent final answer.

Never ignore an appropriate handoff.

Never answer specialist questions directly.
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


async def ask_agent_async(message: str) -> str:
    result = await Runner.run(
        chief_agent,
        message,
    )
    return result.final_output


def ask_agent(message: str) -> str:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(ask_agent_async(message))

    if loop.is_running():
        future = asyncio.run_coroutine_threadsafe(
            ask_agent_async(message),
            loop,
        )
        return future.result()

    return loop.run_until_complete(
        ask_agent_async(message)
    )