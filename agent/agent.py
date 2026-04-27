from llm.bedrock import Bedrock
from .memory import Memory
from tools import Registry
import config
import json
import re
from rich.console import Console
from rich.markdown import Markdown



SYSTEM_PROMPT = """
You are a helpful AI assistant with access to tools. 
Strictly you should only use the tools to answer.
Always think step-by-step before acting.
When you have enough information, provide a clear and concise final answer.

If the user asks you to remember something, confirm that you've stored it.
If asked to recall something, check your memory first.

I will be printing the output on terminal so don't give me html tags (<thinking>) in output. Give me something that will
display or highlight the output.
"""

class Agent:

    def __init__(self, tool_registry: Registry = None):
        self._bedrock = Bedrock()
        self._memory = Memory()
        self._memory.add_message(role="system", content=SYSTEM_PROMPT)
        self._tool_registry = tool_registry
        self._console = Console(markup=True)


    def run(self, user_input: str):

        self._memory.add_message(role="user", content=user_input)
        messages = self._memory.get_messages()

        for step in range(config.MAX_AGENT_STEPS): 
        
            # Make the LLM call
            response = self._bedrock.invoke(message=messages, tools=self._tool_registry.get_all_specs())

            # If LLM response has tool call then execute the tool else return the final response
            if response.get("tool_calls"):

                # Iterate over the tools called by LLM 
                for tool in response["tool_calls"]:

                    # Tool details
                    fn_name = tool["function"]["name"]
                    fn_args = json.loads(tool['function']['arguments'])
                    tool_id = tool["id"]

                    assistant_msg = {
                    "role": "assistant",
                    "content": response.get("content"),
                    "tool_calls": response["tool_calls"],
                    }
                    # Add the assistant response to message history for next LLM call
                    messages.append(assistant_msg)

                    # Execute the tool
                    tool_execution_response = self._tool_registry.execute(name=fn_name, **fn_args)
                    tool_msg = {
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "content": tool_execution_response
                    }

                    # Add the tool response to message history for next LLM call
                    messages.append(tool_msg)

                    # print the thinking text message
                    for item in response.get("content"):
                        if item["type"] == "text":
                            match = re.search(r"<thinking>(.*?)</thinking>", item['text'], re.DOTALL)
                            if match:
                                thinking_text = match.group(1).strip()
                                self._console.print("\r[bold yellow]Thinking...[/bold yellow]", end="")
                                self._console.print(thinking_text + "\n", style="bold yellow")
            else:

                # Update the final response and print it on terminal
                final_response = response.get("content", "Sorry I am not able to help here.")
                final_response = final_response.replace("<thinking>", "").replace("</thinking>", "")
                self._memory.add_message(role=response["role"], content=final_response)
                md = Markdown(final_response)
                self._console.print(md, style="bold green")
                print("\n")
                return final_response
                