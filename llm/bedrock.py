from llm import BaseLLM
from langchain.agents import create_agent
from langchain_aws import ChatBedrockConverse
from langgraph.checkpoint.memory import InMemorySaver
from tools.weather import get_weather
from tools.web_search import web_search
from mcp_clients import TravelMCP
import asyncio


class BedRock(BaseLLM):

    def __init__(self, tools=None):
        self._llm = ChatBedrockConverse(
            model="apac.amazon.nova-lite-v1:0", region_name="ap-south-1"
        )
        
        self._agent = create_agent(self._llm, checkpointer=InMemorySaver(), tools=tools)

    def name(self) -> str:
        return "bedrock"

    async def invoke(self, messages, thread_id):

        config = {"configurable": {"thread_id": thread_id}}
        response = await self._agent.ainvoke({"messages": messages}, config=config)
        return response
