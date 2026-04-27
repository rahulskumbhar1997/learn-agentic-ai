import config
from .base import BaseLLM
from langchain_aws import ChatBedrockConverse

class Bedrock(BaseLLM):

    def __init__(self):
        self._agent = ChatBedrockConverse(model=config.BEDROCK_MODEL_NAME, region_name=config.AWS_REGION_NAME)

    @property
    def name(self):
        return "bedrock"
    
    def invoke(self, message: list[dict], tools: list | None = None):
        tools = tools or []
        self._agent.supports_tool_choice_values = ["tool"]
        bound_agent = self._agent.bind_tools(tools=tools)
        
        lc_message = self._convert_message(messages=message, tools=tools)
        invokation_response = bound_agent.invoke(lc_message)
        return self._parse_response(invokation_response)

    
