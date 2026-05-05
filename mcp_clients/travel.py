

from langchain_mcp_adapters.client import MultiServerMCPClient

class TravelMCP:

    def __init__(self):
        self._client = MultiServerMCPClient(
                        {
                    "travel_server": {
                        "url": "https://mcp.kiwi.com",
                        "transport": "streamable_http"
                    }
                }
        )

    
    async def get_tools(self):
        tools =  await self._client.get_tools()
        return tools
    