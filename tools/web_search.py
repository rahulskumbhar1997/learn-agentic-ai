from .base import Tool
from tavily import TavilyClient

class WebSearch(Tool):

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
    
    def execute(self,query: str, max_results: int = 5):
        """
        Perform a Tavily web search.

        :param query: Search query string
        :param max_results: Number of results to return
        :return: Search results (dict)
        """

        client = TavilyClient(api_key="")

        response = client.search(
            query=query,
            max_results=max_results
        )

        return response