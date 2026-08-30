from agents import Agent, Runner
import asyncio
import os

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

If the user uploads a file,
the file path will be included in the message.

Always send document-related requests
to Documents Agent.

Never ignore uploaded files.

Always use handoffs.
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


def ask_agent(message: str, uploaded_file=None) -> str:

    if uploaded_file is not None:
        message += (
            f"\n\nUploaded file:\n"
            f"Name: {uploaded_file.name}\n"
            f"Path: {uploaded_file}"
        )

    async def _run():
        result = await Runner.run(
            chief_agent,
            message,
        )
        return result.final_output

    return asyncio.run(_run())