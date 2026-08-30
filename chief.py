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

Your job is to understand the user's request
and route it to the correct specialist.

Always use handoffs.

If the request contains:

FILE_PATH=

or an uploaded document,

always hand off to Documents Agent first.

Never answer specialist questions yourself.

If more than one specialist is required,
coordinate them and return one final answer.
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


def ask_agent(message: str, uploaded_file=None) -> str:

    if uploaded_file:
        message += f"\n\nFILE_PATH={uploaded_file}"

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(
            ask_agent_async(message)
        )

    if loop.is_running():
        future = asyncio.run_coroutine_threadsafe(
            ask_agent_async(message),
            loop,
        )
        return future.result()

    return loop.run_until_complete(
        ask_agent_async(message)
    )