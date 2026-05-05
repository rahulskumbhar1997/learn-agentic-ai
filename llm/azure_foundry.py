from .base import BaseLLM
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage

class AzureFoundry(BaseLLM):

    def __init__(self, tools=None):
        self._llm = AzureChatOpenAI(
            azure_deployment="gpt-4.1-mini",
            api_version="2025-01-01-preview",
            temperature=0.1,
        )
        self._agent = create_agent(self._llm, tools=tools, checkpointer=InMemorySaver())


    def name(self) -> str:
        return "azure_foundry"


    async def invoke(self, messages: list, thread_id: str):

        config = {"configurable": {"thread_id": thread_id}}
        response = await self._agent.ainvoke({
            "messages": messages
        }, config=config)

        return response
