import os
from tavily import TavilyClient
from langchain.tools import tool


@tool(description="Perform a Tavily web search.")
def web_search(query: str, max_results: int = 5):
    """
    Perform a Tavily web search.

    :param query: Search query string
    :param max_results: Number of results to return
    :return: Search results (dict)
    """

    tavily_api_key = os.environ.get("TAVILY_API_KEY")
    client = TavilyClient(api_key=tavily_api_key)

    response = client.search(query=query, max_results=max_results)

    return response
