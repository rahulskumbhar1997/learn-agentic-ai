from .base import BaseLLM
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
import config

class AzureFoundry(BaseLLM):

    def __init__(self, tools=None):
        self._llm = AzureChatOpenAI(
            azure_deployment=config.AZURE_DEPLOYMENT_NAME,
            api_version=config.AZURE_DEPLOYMENT_API_VERSION,
            temperature=0.1,
        )
        self._agent = create_agent(self._llm, tools=tools, checkpointer=InMemorySaver())

    @property
    def name(self) -> str:
        return "azure_foundry"

    async def invoke(self, messages: list, thread_id: str):

        config = {"configurable": {"thread_id": thread_id}}
        response = await self._agent.ainvoke({"messages": messages}, config=config)

        return response
