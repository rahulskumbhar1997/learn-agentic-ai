from .base import Tool

"""
Implement a registry pattern to manage the tools. With this you can easily plug-in new tools.
"""

class Registry:


    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool):

        self._tools[tool.name] = tool
    
    def get(self, name: str):
        
        return self._tools.get(name) or None
    
    def execute(self, name: str, **kwargs):

        tool = self._tools.get(name)
        if tool is None:
            raise Exception("No tool found")
        
        try:
            return tool.execute(**kwargs)
        except Exception as e:
            return f"Error executing tool {name}. Response: {e}"
    
    def list_tools(self) -> list:
        return [tool for tool in self._tools.keys()]
    
    def get_all_specs(self) -> list:
        return [spec.to_openai_spec() for spec in self._tools.values()]