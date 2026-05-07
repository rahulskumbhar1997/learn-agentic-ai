from llm import BedRock, AzureFoundry
from langchain.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
from mcp_clients import TravelMCP, SportsMCP
from tools import web_search, get_weather
from rich.console import Console
from rich.markdown import Markdown
import asyncio


def main():
    while True:
        user_input = input("\n> ")
        if user_input == "":
            continue
        elif user_input.lower() == "exit":
            break
        else:
            response = asyncio.run(
                llm_client.invoke(
                    [
                        SystemMessage(content=system_prompt),
                        HumanMessage(content=user_input),
                    ],
                    thread_id=thread_id,
                )
            )
            final_response = response["messages"][-1].content
            md = Markdown(final_response)
            console.print(md, style="bold green")


if __name__ == "__main__":
    load_dotenv()
    console = Console(markup=True)
    travel_mcp = TravelMCP()
    travel_mcp_tools = asyncio.run(travel_mcp.get_tools())

    sports_mcp = SportsMCP()
    sports_mcp_tools = asyncio.run(sports_mcp.get_tools())

    tools = [web_search, get_weather] + travel_mcp_tools + sports_mcp_tools
    for tool in tools:
        print(f"tool: {tool.get_name()}")

    # llm_client = BedRock(tools=tools)
    llm_client = AzureFoundry(tools=tools)

    system_prompt = """
    You are an AI assistant and you should answer all queries of user. Strictly use the tools provided for
    answering the question. Also let the user know you have used the tool. Answer mostly in one or two 
    lines.
    """

    thread_id = "test_thread_v2"

    main()
