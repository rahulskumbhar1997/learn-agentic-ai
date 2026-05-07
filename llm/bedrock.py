from llm import BaseLLM
from langchain.agents import create_agent
from langchain_aws import ChatBedrockConverse
from langgraph.checkpoint.memory import InMemorySaver
import config


class BedRock(BaseLLM):

    def __init__(self, tools=None):
        self._llm = ChatBedrockConverse(
            model=config.BEDROCK_MODEL, region_name=config.BEDROCK_REGION
        )

        self._agent = create_agent(self._llm, checkpointer=InMemorySaver(), tools=tools)

    @property
    def name(self) -> str:
        return "bedrock"

    async def invoke(self, messages, thread_id):

        config = {"configurable": {"thread_id": thread_id}}
        response = await self._agent.ainvoke({"messages": messages}, config=config)
        return response
