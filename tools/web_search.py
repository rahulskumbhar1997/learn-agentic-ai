from .base import Tool
from tavily import TavilyClient
import os

class WebSearch(Tool):

    def __init__(self):
        tavily_key = os.environ["TAVILY_API_KEY"] 
        self._client = TavilyClient(api_key=tavily_key)

    @property
    def name(self):
        return "web_search"

    @property
    def description(self):
        return "Search the web for recent information. Use this tool when you need to find up-to-date information or answer questions about current events."
    
    @property
    def parameters(self):
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query, eg. 'What is the capital of France?'"
                }
            },
            "required": ["query"]
        }
    
    def execute(self,query: str, max_results: int = 10):
        """
        Perform a Tavily web search.

        :param query: Search query string
        :param max_results: Number of results to return
        :return: Search results (dict)
        """

        response = self._client.search(
            query=query,
            max_results=max_results
        )

        return response