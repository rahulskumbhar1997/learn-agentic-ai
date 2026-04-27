from abc import ABC, abstractmethod
from langchain.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
import json

"""
Extend this class to implement different LLM Clients like Amazon BedRock, OpenAI, Azure etc. 
"""
class BaseLLM(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of LLM Client"""
    
    @abstractmethod
    def invoke(self, message: str, tools: list):
        """Send chat completion request to LLM"""

    @staticmethod
    def _convert_message(messages: list[dict], tools: list):

        """
        Convert the message to the format accepted by LLM Client.
        """

        lc_message = []
        for msg in messages:
            role = msg["role"].lower()
            content = msg.get("content") or ""
            if role == "user":
                lc_message.append(HumanMessage(content=content))
            elif role == "system":
                lc_message.append(SystemMessage(content=content))
            elif role == "assistant":
                tool_calls = msg.get("tool_calls")
                if tool_calls:
                    lc_tool_calls = [
                        {
                            "id": tc["id"],
                            "name": tc["function"]["name"],
                            "args": json.loads(tc["function"]["arguments"])
                                    if isinstance(tc["function"]["arguments"], str)
                                    else tc["function"]["arguments"],
                        }
                        for tc in tool_calls
                    ]
                    lc_message.append(
                        AIMessage(content=content, tool_calls=lc_tool_calls)
                    )
                else:
                    lc_message.append(AIMessage(content=content))
            elif role == "tool":
                lc_message.append(ToolMessage(content=content, tool_call_id=msg["tool_call_id"]))
            
        return lc_message

    @staticmethod
    def _parse_response(message: AIMessage):
        result = {
            "role": "assistant",
            "content": message.content,
            "tool_calls": None
        }
        if message.tool_calls:
            result["tool_calls"] = [
                {
                    "id": tc["id"],
                    "function": {
                        "name": tc["name"],
                        "arguments": json.dumps(tc["args"]),
                    }
                }
                for tc in message.tool_calls
            ]

        return result