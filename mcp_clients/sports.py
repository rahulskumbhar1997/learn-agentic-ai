from langchain_mcp_adapters.client import MultiServerMCPClient

class SportsMCP:

    def __init__(self):
        self._client = MultiServerMCPClient(
                        {
                    "sports_server": {
                        "url": "https://whensport.com/mcp/cricket",
                        "transport": "streamable_http"
                    }
                }
        )

    
    async def get_tools(self):
        tools =  await self._client.get_tools()
        return tools